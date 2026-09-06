from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class MotionState(str, Enum):
    STOPPED = "stopped"
    MOVING = "moving"


@dataclass(frozen=True)
class GeoPoint:
    latitude: float
    longitude: float


@dataclass(frozen=True)
class VisionObservation:
    """Provider-neutral output from a camera/vision adapter."""

    labels: frozenset[str] = frozenset()
    landmark_candidates: dict[str, float] = field(default_factory=dict)
    embedding: tuple[float, ...] | None = None


@dataclass(frozen=True)
class LiveContext:
    session_id: str
    time: datetime
    motion_state: MotionState
    gps: GeoPoint | None
    route_id: str | None
    previous_place_id: str | None = None
    next_expected_places: tuple[str, ...] = ()
    vision: VisionObservation | None = None
    guide_voice_hint: str | None = None
    visitor_question: str | None = None
    active_timeline: str | None = None
