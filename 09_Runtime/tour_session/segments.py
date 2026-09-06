from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SegmentType(str, Enum):
    ARRIVAL = "arrival"
    GUIDE_NARRATION = "guide_narration"
    VISITOR_QA = "visitor_qa"
    GUIDE_CORRECTION = "guide_correction"
    FREE_EXPLORATION = "free_exploration"
    TRANSIT = "transit"
    DEPARTURE = "departure"


@dataclass(frozen=True)
class TourSegment:
    segment_id: str
    session_id: str
    segment_type: SegmentType
    started_at: datetime
    ended_at: datetime | None
    timezone: str
    place_id: str | None
    latitude: float | None
    longitude: float | None
    audio_asset_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.ended_at is not None and self.ended_at < self.started_at:
            raise ValueError("segment end cannot precede its start")
        speech_types = {SegmentType.GUIDE_NARRATION, SegmentType.VISITOR_QA}
        if self.segment_type in speech_types and not self.audio_asset_ids:
            raise ValueError("spoken segments must retain at least one audio asset")

