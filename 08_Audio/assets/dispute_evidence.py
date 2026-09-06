from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum
from hashlib import sha256


class EvidenceAction(str, Enum):
    CREATED = "created"
    VERIFIED = "verified"
    ACCESSED = "accessed"
    EXPORTED = "exported"
    HOLD_APPLIED = "hold_applied"
    HOLD_RELEASED = "hold_released"


@dataclass(frozen=True)
class CompanyEvidencePolicyAcceptance:
    company_id: str
    policy_version: str
    accepted_by_admin_id: str
    accepted_at: datetime
    policy_checkbox_checked: bool
    recording_notice_enabled: bool
    retention_days: int

    def __post_init__(self) -> None:
        if not self.policy_checkbox_checked:
            raise ValueError("company administrator must check the policy acceptance box")
        if not self.recording_notice_enabled:
            raise ValueError("recording notice must be enabled for dispute recording")
        if self.retention_days <= 0:
            raise ValueError("retention_days must be positive")

    def enables_evidence_for(self, company_id: str, policy_version: str) -> bool:
        return self.company_id == company_id and self.policy_version == policy_version


@dataclass(frozen=True)
class CustodyEvent:
    action: EvidenceAction
    actor_id: str
    occurred_at: datetime
    reason: str
    previous_event_hash: str | None
    event_hash: str

    def expected_hash(self) -> str:
        payload = "|".join((
            self.action.value, self.actor_id, self.occurred_at.isoformat(), self.reason,
            self.previous_event_hash or "GENESIS",
        ))
        return sha256(payload.encode("utf-8")).hexdigest()

    @staticmethod
    def create(
        *, action: EvidenceAction, actor_id: str, occurred_at: datetime,
        reason: str, previous_event_hash: str | None,
    ) -> "CustodyEvent":
        draft = CustodyEvent(action, actor_id, occurred_at, reason, previous_event_hash, "")
        return replace(draft, event_hash=draft.expected_hash())


@dataclass(frozen=True)
class DisputeEvidencePackage:
    evidence_id: str
    session_id: str
    assignment_id: str
    audio_asset_ids: tuple[str, ...]
    segment_ids: tuple[str, ...]
    location_event_ids: tuple[str, ...]
    captured_from: datetime
    captured_to: datetime
    timezone: str
    recording_notice_event_id: str
    manifest_sha256: str
    custody_events: tuple[CustodyEvent, ...]
    legal_hold: bool = False

    def __post_init__(self) -> None:
        if self.captured_to <= self.captured_from:
            raise ValueError("evidence end must be after its start")
        if not self.audio_asset_ids:
            raise ValueError("evidence must reference retained original audio")
        if not self.recording_notice_event_id:
            raise ValueError("recording notice evidence is required")
        if len(self.manifest_sha256) != 64:
            raise ValueError("evidence manifest must have a SHA-256 checksum")
        try:
            int(self.manifest_sha256, 16)
        except ValueError as error:
            raise ValueError("evidence manifest checksum must be hexadecimal") from error
        previous = None
        if not self.custody_events:
            raise ValueError("evidence requires a custody trail")
        for event in self.custody_events:
            if event.previous_event_hash != previous:
                raise ValueError("custody event chain is broken")
            if event.event_hash != event.expected_hash():
                raise ValueError("custody event has been altered")
            previous = event.event_hash

    @property
    def deletion_allowed(self) -> bool:
        return not self.legal_hold

    def append_event(
        self, *, action: EvidenceAction, actor_id: str,
        occurred_at: datetime, reason: str,
    ) -> "DisputeEvidencePackage":
        event = CustodyEvent.create(
            action=action, actor_id=actor_id, occurred_at=occurred_at,
            reason=reason, previous_event_hash=self.custody_events[-1].event_hash,
        )
        hold = self.legal_hold
        if action is EvidenceAction.HOLD_APPLIED:
            hold = True
        elif action is EvidenceAction.HOLD_RELEASED:
            hold = False
        return replace(self, custody_events=self.custody_events + (event,), legal_hold=hold)
