from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NarrativeScript:
    script_id: str
    fact_ids: tuple[str, ...]
    author_id: str
    language: str
    audience: str
    duration_seconds: int
    text: str
    version: str

    def __post_init__(self) -> None:
        if not self.fact_ids:
            raise ValueError("NarrativeScript must reference verified fact_ids")
        if self.duration_seconds <= 0:
            raise ValueError("duration_seconds must be positive")

