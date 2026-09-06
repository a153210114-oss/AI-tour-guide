from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class VerifiedRatingSummary:
    verified_tour_count: int
    unique_visitor_group_count: int
    rating_count: int
    average_rating: float
    complaint_count: int
    upheld_complaint_count: int

    def __post_init__(self) -> None:
        counts = (
            self.verified_tour_count, self.unique_visitor_group_count,
            self.rating_count, self.complaint_count, self.upheld_complaint_count,
        )
        if any(value < 0 for value in counts):
            raise ValueError("rating summary counts cannot be negative")
        if not 0 <= self.average_rating <= 5:
            raise ValueError("average rating must be between zero and five")
        if self.upheld_complaint_count > self.complaint_count:
            raise ValueError("upheld complaints cannot exceed total complaints")


@dataclass(frozen=True)
class GuideAssessmentEvidenceBundle:
    bundle_id: str
    guide_id: str
    guide_consent_id: str
    generated_at: datetime
    covered_from: datetime
    covered_to: datetime
    session_ids: tuple[str, ...]
    original_audio_asset_ids: tuple[str, ...]
    transcript_ids: tuple[str, ...]
    rating_summary: VerifiedRatingSummary
    correction_rate: float
    safety_event_ids: tuple[str, ...]
    route_ids: tuple[str, ...]
    language_codes: tuple[str, ...]
    integrity_manifest_sha256: str
    unresolved_integrity_flags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.guide_consent_id:
            raise ValueError("guide consent is required for external assessment")
        if self.covered_to <= self.covered_from:
            raise ValueError("assessment period end must follow its start")
        if not self.session_ids or not self.original_audio_asset_ids:
            raise ValueError("assessment requires verified tours and original audio")
        if not 0 <= self.correction_rate <= 1:
            raise ValueError("correction_rate must be between zero and one")
        if len(self.integrity_manifest_sha256) != 64:
            raise ValueError("assessment manifest must have a SHA-256 checksum")
        try:
            int(self.integrity_manifest_sha256, 16)
        except ValueError as error:
            raise ValueError("assessment manifest checksum must be hexadecimal") from error

    @property
    def ready_for_external_review(self) -> bool:
        return not self.unresolved_integrity_flags


@dataclass(frozen=True)
class ExternalAssessmentDecision:
    bundle_id: str
    assessor_organisation: str
    assessor_id: str
    decided_at: datetime
    framework_version: str
    outcome: str
    verification_uri: str

    def __post_init__(self) -> None:
        if not self.assessor_organisation or not self.assessor_id:
            raise ValueError("external decision requires an identified assessor")
        if not self.verification_uri:
            raise ValueError("external decision requires issuer verification")
