from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class AcceptanceMetrics:
    total: int
    top1_correct: int
    top3_correct: int
    unsafe_hard_guesses: int

    @property
    def top1_rate(self) -> float:
        return self.top1_correct / self.total if self.total else 0.0

    @property
    def top3_rate(self) -> float:
        return self.top3_correct / self.total if self.total else 0.0

    @property
    def gate_passed(self) -> bool:
        return (
            self.total >= 10
            and self.top1_rate >= 0.8
            and self.top3_rate == 1.0
            and self.unsafe_hard_guesses == 0
        )


def calculate_metrics(rows: Iterable[dict]) -> AcceptanceMetrics:
    total = top1 = top3 = unsafe = 0
    for row in rows:
        total += 1
        expected = row["expected_place_id"]
        candidates: Sequence[dict] = row["result"]["candidates"]
        ids = [candidate["place_id"] for candidate in candidates]
        top1 += bool(ids and ids[0] == expected)
        top3 += expected in ids[:3]
        unsafe += bool(
            row.get("should_abstain")
            and row["result"].get("selected_place_id") is not None
        )
    return AcceptanceMetrics(total, top1, top3, unsafe)

