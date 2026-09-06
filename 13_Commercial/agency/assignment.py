from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum


class AssignmentStatus(str, Enum):
    OFFERED = "offered"
    ACCEPTED = "accepted"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class LanguageChannels:
    ui_language: str
    guide_prompt_language: str
    guide_narration_language: str
    public_playback_language: str
    visitor_default_language: str


@dataclass(frozen=True)
class CompanyProductVersion:
    company_id: str
    product_id: str
    version: str
    route_id: str
    planned_stop_ids: tuple[str, ...]
    content_pack_versions: tuple[str, ...]
    autoplay_policy_id: str | None
    languages: LanguageChannels
    published_at: datetime


@dataclass(frozen=True)
class CompanyAssignment:
    assignment_id: str
    company_id: str
    product_id: str
    product_version: str
    route_id: str
    driver_id: str
    guide_id: str | None
    vehicle_id: str | None
    scheduled_start: datetime
    scheduled_end: datetime
    pickup_point_ids: tuple[str, ...]
    status: AssignmentStatus = AssignmentStatus.OFFERED
    accepted_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.scheduled_end <= self.scheduled_start:
            raise ValueError("scheduled_end must be after scheduled_start")

    def accept(self, actor_id: str, accepted_at: datetime) -> "CompanyAssignment":
        if actor_id not in {self.driver_id, self.guide_id}:
            raise PermissionError("only the assigned driver or guide can accept")
        if self.status is not AssignmentStatus.OFFERED:
            raise ValueError("only offered assignments can be accepted")
        return replace(self, status=AssignmentStatus.ACCEPTED, accepted_at=accepted_at)

    def reassign_driver(self, driver_id: str) -> "CompanyAssignment":
        if self.status is AssignmentStatus.STARTED:
            raise ValueError("started assignments require a runtime handover event")
        return replace(
            self,
            driver_id=driver_id,
            status=AssignmentStatus.OFFERED,
            accepted_at=None,
        )

