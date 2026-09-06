from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ConsentStatus(str, Enum):
    EXPLICIT = "explicit"
    GUIDE_ONLY = "guide_only"
    PENDING = "pending"
    DENIED = "denied"


@dataclass(frozen=True)
class UsageRights:
    internal_learning: bool = False
    public_playback: bool = False
    commercial_content: bool = False
    model_training: bool = False
    voice_cloning: bool = False


@dataclass(frozen=True)
class AudioAsset:
    audio_asset_id: str
    session_id: str
    started_at: datetime
    ended_at: datetime
    timezone: str
    place_id: str | None
    route_id: str | None
    speaker_scope: str
    language: str
    original_audio_uri: str
    checksum_sha256: str
    transcript_id: str | None
    narrative_script_id: str | None
    owner_id: str
    consent_status: ConsentStatus
    rights: UsageRights
    retention_class: str = "long_term_original"

    def __post_init__(self) -> None:
        if self.ended_at <= self.started_at:
            raise ValueError("ended_at must be after started_at")
        if len(self.checksum_sha256) != 64:
            raise ValueError("checksum_sha256 must contain 64 hexadecimal characters")
        try:
            int(self.checksum_sha256, 16)
        except ValueError as error:
            raise ValueError("checksum_sha256 must be hexadecimal") from error
        if not self.original_audio_uri:
            raise ValueError("original audio is mandatory")
        if self.retention_class != "long_term_original":
            raise ValueError("original audio must use long_term_original retention")
        restricted = (
            self.rights.commercial_content
            or self.rights.model_training
            or self.rights.voice_cloning
        )
        if restricted and self.consent_status is not ConsentStatus.EXPLICIT:
            raise ValueError("commercial, training and voice-cloning rights require explicit consent")
        if self.rights.voice_cloning and not self.rights.model_training:
            raise ValueError("voice cloning also requires model_training permission")

