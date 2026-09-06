from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeliveryProfile:
    profile_id: str
    owner_id: str
    source_audio_asset_ids: tuple[str, ...]
    words_per_minute: int | None = None
    pause_pattern: tuple[float, ...] = ()
    emphasis_notes: tuple[str, ...] = ()
    interaction_pattern: tuple[str, ...] = ()
    voice_clone_permission: bool = False

    def __post_init__(self) -> None:
        if self.words_per_minute is not None and self.words_per_minute <= 0:
            raise ValueError("words_per_minute must be positive")

