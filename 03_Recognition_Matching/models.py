from __future__ import annotations

from dataclasses import dataclass

from importlib import import_module

GeoPoint = import_module("02_Scene_Context.models").GeoPoint


@dataclass(frozen=True)
class PlaceCandidate:
    place_id: str
    name: str
    location: GeoPoint
    route_ids: frozenset[str]
    visual_labels: frozenset[str] = frozenset()
    aliases: tuple[str, ...] = ()
    knowledge_pack_id: str | None = None


@dataclass(frozen=True)
class ScoreBreakdown:
    gps: float
    route: float
    sequence: float
    vision: float
    voice: float
    correction: float

    @property
    def total(self) -> float:
        return round(
            self.gps + self.route + self.sequence + self.vision + self.voice + self.correction,
            4,
        )


@dataclass(frozen=True)
class RankedCandidate:
    place_id: str
    name: str
    score: float
    breakdown: ScoreBreakdown
    evidence: tuple[str, ...]
    knowledge_pack_id: str | None


@dataclass(frozen=True)
class RecognitionResult:
    candidates: tuple[RankedCandidate, ...]
    selected_place_id: str | None
    confidence: float
    evidence: tuple[str, ...]
    needs_confirmation: bool

