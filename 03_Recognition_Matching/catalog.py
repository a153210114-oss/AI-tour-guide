from __future__ import annotations

import json
from importlib import import_module
from pathlib import Path

GeoPoint = import_module("02_Scene_Context.models").GeoPoint
PlaceCandidate = import_module("03_Recognition_Matching.models").PlaceCandidate


def load_place_catalog(path: str | Path) -> list[PlaceCandidate]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    route_id = payload["route_id"]
    knowledge_pack_id = payload.get(
        "knowledge_pack_id", "knowledge.au.vic.great-ocean-road.r1"
    )
    return [
        PlaceCandidate(
            place_id=item["place_id"],
            name=item["name"],
            location=GeoPoint(item["latitude"], item["longitude"]),
            route_ids=frozenset({route_id}),
            visual_labels=frozenset(label.casefold() for label in item.get("visual_labels", [])),
            aliases=tuple(item.get("aliases", [])),
            knowledge_pack_id=knowledge_pack_id,
        )
        for item in payload["places"]
    ]
