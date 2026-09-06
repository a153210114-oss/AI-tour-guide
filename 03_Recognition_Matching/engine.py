from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module
from math import asin, cos, radians, sin, sqrt
from re import findall
from unicodedata import normalize

context_models = import_module("02_Scene_Context.models")
matching_models = import_module("03_Recognition_Matching.models")
LiveContext = context_models.LiveContext
GeoPoint = context_models.GeoPoint
PlaceCandidate = matching_models.PlaceCandidate
ScoreBreakdown = matching_models.ScoreBreakdown
RankedCandidate = matching_models.RankedCandidate
RecognitionResult = matching_models.RecognitionResult


def distance_km(a: GeoPoint, b: GeoPoint) -> float:
    earth_radius_km = 6371.0
    dlat = radians(b.latitude - a.latitude)
    dlon = radians(b.longitude - a.longitude)
    lat1, lat2 = radians(a.latitude), radians(b.latitude)
    h = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * earth_radius_km * asin(sqrt(h))


def _tokens(text: str) -> frozenset[str]:
    normalized = normalize("NFKC", text).casefold()
    return frozenset(findall(r"[\w']+", normalized))


@dataclass
class SessionCorrections:
    """Ephemeral guide corrections; deliberately scoped to one session."""

    _places: dict[str, set[str]] = field(default_factory=dict)

    def remember(self, session_id: str, place_id: str) -> None:
        self._places.setdefault(session_id, set()).add(place_id)

    def contains(self, session_id: str, place_id: str) -> bool:
        return place_id in self._places.get(session_id, set())


class RecognitionEngine:
    def __init__(
        self,
        places: list[PlaceCandidate],
        corrections: SessionCorrections | None = None,
        confirmation_threshold: float = 0.55,
        ambiguity_margin: float = 0.08,
    ) -> None:
        self.places = places
        self.corrections = corrections or SessionCorrections()
        self.confirmation_threshold = confirmation_threshold
        self.ambiguity_margin = ambiguity_margin

    def recognize(self, context: LiveContext) -> RecognitionResult:
        ranked = sorted(
            (self._score(place, context) for place in self.places),
            key=lambda item: item.score,
            reverse=True,
        )[:3]
        if not ranked:
            return RecognitionResult((), None, 0.0, ("no candidates",), True)

        top = ranked[0]
        margin = top.score - ranked[1].score if len(ranked) > 1 else top.score
        confidence = round(min(1.0, top.score * 0.8 + max(0.0, margin) * 0.7), 4)
        ambiguous = len(ranked) > 1 and margin < self.ambiguity_margin
        needs_confirmation = confidence < self.confirmation_threshold or ambiguous
        selected = None if needs_confirmation else top.place_id
        reason = "low confidence or ambiguous" if needs_confirmation else "multi-signal match"
        return RecognitionResult(tuple(ranked), selected, confidence, top.evidence + (reason,), needs_confirmation)

    def apply_guide_correction(self, session_id: str, place_id: str) -> None:
        if place_id not in {place.place_id for place in self.places}:
            raise ValueError(f"Unknown place_id: {place_id}")
        self.corrections.remember(session_id, place_id)

    def _score(self, place: PlaceCandidate, context: LiveContext) -> RankedCandidate:
        evidence: list[str] = []
        gps = 0.0
        if context.gps:
            distance = distance_km(context.gps, place.location)
            gps = 0.34 * max(0.0, 1.0 - distance / 30.0)
            if gps:
                evidence.append(f"gps:{distance:.1f}km")

        route = 0.18 if context.route_id and context.route_id in place.route_ids else 0.0
        if route:
            evidence.append("on current route")

        sequence = 0.0
        if place.place_id in context.next_expected_places:
            position = context.next_expected_places.index(place.place_id)
            sequence = max(0.04, 0.18 - position * 0.04)
            evidence.append(f"expected next:{position + 1}")

        vision = 0.0
        if context.vision:
            provider_score = context.vision.landmark_candidates.get(place.place_id, 0.0)
            label_union = place.visual_labels | frozenset(alias.casefold() for alias in place.aliases)
            overlap = context.vision.labels & label_union
            label_score = len(overlap) / max(1, len(place.visual_labels))
            vision = 0.20 * max(provider_score, min(1.0, label_score))
            if vision:
                evidence.append("vision match")

        voice = 0.0
        if context.guide_voice_hint:
            hint_tokens = _tokens(context.guide_voice_hint)
            names = (place.name, *place.aliases)
            similarity = max(
                (len(hint_tokens & _tokens(name)) / max(1, len(_tokens(name))) for name in names),
                default=0.0,
            )
            voice = 0.10 * min(1.0, similarity)
            if voice:
                evidence.append("guide hint")

        correction = 0.18 if self.corrections.contains(context.session_id, place.place_id) else 0.0
        if correction:
            evidence.append("session correction")

        breakdown = ScoreBreakdown(gps, route, sequence, vision, voice, correction)
        return RankedCandidate(
            place.place_id,
            place.name,
            breakdown.total,
            breakdown,
            tuple(evidence),
            place.knowledge_pack_id,
        )

