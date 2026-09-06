from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class KnowledgeFact:
    fact_id: str
    claim: str
    source: str
    source_grade: str
    last_verified_at: datetime
    confidence: float

    def __post_init__(self) -> None:
        if self.source_grade not in {"A", "B", "C"}:
            raise ValueError("source_grade must be A, B or C")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")

