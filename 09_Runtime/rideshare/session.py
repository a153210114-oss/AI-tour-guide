from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum
from hashlib import sha256
from hmac import compare_digest


class RelayStatus(str, Enum):
    WAITING_FOR_PASSENGER = "waiting_for_passenger"
    ACTIVE = "active"
    ENDED = "ended"
    EXPIRED = "expired"


class ProviderMode(str, Enum):
    TEST = "test"
    LIVE = "live"


@dataclass(frozen=True)
class RideLanguageRelay:
    relay_id: str
    driver_id: str
    qr_token_sha256: str
    created_at: datetime
    expires_at: datetime
    driver_output_language: str
    status: RelayStatus = RelayStatus.WAITING_FOR_PASSENGER
    passenger_language: str | None = None
    provider_mode: ProviderMode = ProviderMode.TEST
    providers_connected: bool = False
    recording_enabled: bool = False
    retention_class: str = "ephemeral"

    def __post_init__(self) -> None:
        if self.expires_at <= self.created_at:
            raise ValueError("relay expiry must be after creation")
        if len(self.qr_token_sha256) != 64:
            raise ValueError("QR token must be stored as a SHA-256 hash")
        if self.recording_enabled:
            raise ValueError("recording requires a separate consent workflow")
        if self.retention_class != "ephemeral":
            raise ValueError("ordinary ride relay messages must be ephemeral")
        if self.provider_mode is ProviderMode.LIVE and not self.providers_connected:
            raise ValueError("live mode requires connected providers")

    @staticmethod
    def token_hash(raw_token: str) -> str:
        return sha256(raw_token.encode("utf-8")).hexdigest()

    @property
    def live_translation_available(self) -> bool:
        return self.provider_mode is ProviderMode.LIVE and self.providers_connected

    @property
    def driver_interaction_while_moving(self) -> str:
        return "voice_only"

    def join(
        self, *, raw_token: str, passenger_language: str, joined_at: datetime,
    ) -> "RideLanguageRelay":
        if self.status is not RelayStatus.WAITING_FOR_PASSENGER:
            raise ValueError("relay is not accepting a passenger")
        if joined_at >= self.expires_at:
            return replace(self, status=RelayStatus.EXPIRED)
        if not compare_digest(self.qr_token_sha256, self.token_hash(raw_token)):
            raise PermissionError("invalid ride relay QR token")
        if not passenger_language:
            raise ValueError("passenger must select a language")
        return replace(
            self, status=RelayStatus.ACTIVE,
            passenger_language=passenger_language,
        )

    def end(self) -> "RideLanguageRelay":
        return replace(self, status=RelayStatus.ENDED)
