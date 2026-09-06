from __future__ import annotations

from datetime import datetime
from importlib import import_module
from pathlib import Path
from typing import Any, Dict

context_models = import_module("02_Scene_Context.models")
catalog_module = import_module("03_Recognition_Matching.catalog")
engine_module = import_module("03_Recognition_Matching.engine")

GeoPoint = context_models.GeoPoint
LiveContext = context_models.LiveContext
MotionState = context_models.MotionState
VisionObservation = context_models.VisionObservation
RecognitionEngine = engine_module.RecognitionEngine


class RecognitionService:
    def __init__(self, catalog_path: str | Path) -> None:
        self.engine = RecognitionEngine(catalog_module.load_place_catalog(catalog_path))

    def recognize_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        gps_data = payload.get("gps")
        vision_data = payload.get("vision")
        context = LiveContext(
            session_id=payload["session_id"],
            time=datetime.fromisoformat(payload["time"].replace("Z", "+00:00")),
            motion_state=MotionState(payload["motion_state"]),
            gps=GeoPoint(gps_data["latitude"], gps_data["longitude"]) if gps_data else None,
            route_id=payload.get("route_id"),
            previous_place_id=payload.get("previous_place_id"),
            next_expected_places=tuple(payload.get("next_expected_places", [])),
            vision=VisionObservation(
                labels=frozenset(label.casefold() for label in vision_data.get("labels", [])),
                landmark_candidates=vision_data.get("landmark_candidates", {}),
                embedding=tuple(vision_data["embedding"]) if vision_data.get("embedding") else None,
            ) if vision_data else None,
            guide_voice_hint=payload.get("guide_voice_hint"),
            visitor_question=payload.get("visitor_question"),
            active_timeline=payload.get("active_timeline"),
        )
        return result_to_dict(self.engine.recognize(context))

    def correct(self, session_id: str, place_id: str) -> None:
        self.engine.apply_guide_correction(session_id, place_id)


def result_to_dict(result: Any) -> Dict[str, Any]:
    return {
        "candidates": [
            {
                "place_id": candidate.place_id,
                "name": candidate.name,
                "score": candidate.score,
                "score_breakdown": {
                    "gps": round(candidate.breakdown.gps, 4),
                    "route": round(candidate.breakdown.route, 4),
                    "sequence": round(candidate.breakdown.sequence, 4),
                    "vision": round(candidate.breakdown.vision, 4),
                    "voice": round(candidate.breakdown.voice, 4),
                    "correction": round(candidate.breakdown.correction, 4),
                },
                "evidence": list(candidate.evidence),
                "knowledge_pack_id": candidate.knowledge_pack_id,
            }
            for candidate in result.candidates
        ],
        "selected_place_id": result.selected_place_id,
        "confidence": result.confidence,
        "evidence": list(result.evidence),
        "needs_confirmation": result.needs_confirmation,
    }

