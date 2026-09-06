from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ContentLicenceStatus(str, Enum):
    UNKNOWN = "unknown"
    LINK_ONLY = "link_only"
    ATTRIBUTION_REUSE = "attribution_reuse"
    PARTNER_LICENCE = "partner_licence"


@dataclass(frozen=True)
class OfficialLearningResource:
    resource_id: str
    publisher_name: str
    source_url: str
    title: str
    published_or_updated_at: datetime | None
    retrieved_at: datetime
    licence_status: ContentLicenceStatus
    licence_reference: str | None
    indigenous_cultural_review_required: bool = False

    @property
    def may_copy_into_course(self) -> bool:
        return self.licence_status in {
            ContentLicenceStatus.ATTRIBUTION_REUSE,
            ContentLicenceStatus.PARTNER_LICENCE,
        } and bool(self.licence_reference)


class CredentialKind(str, Enum):
    PLATFORM_COMPLETION = "platform_completion"
    PARTNER_BADGE = "partner_badge"
    INDUSTRY_ACCREDITATION = "industry_accreditation"
    NATIONAL_QUALIFICATION = "national_qualification"


@dataclass(frozen=True)
class GuideCredential:
    credential_id: str
    guide_id: str
    title: str
    kind: CredentialKind
    issuer_name: str
    issued_at: datetime
    expires_at: datetime | None
    evidence_uri: str
    external_verification_uri: str | None = None

    def __post_init__(self) -> None:
        if self.expires_at is not None and self.expires_at <= self.issued_at:
            raise ValueError("credential expiry must be after issue time")
        externally_recognised = {
            CredentialKind.PARTNER_BADGE,
            CredentialKind.INDUSTRY_ACCREDITATION,
            CredentialKind.NATIONAL_QUALIFICATION,
        }
        if self.kind in externally_recognised and not self.external_verification_uri:
            raise ValueError("externally recognised credentials require issuer verification")

    @property
    def is_platform_only(self) -> bool:
        return self.kind is CredentialKind.PLATFORM_COMPLETION
