"""Nightly lessons distillation — episodic memory -> semantic memory loop.

For each completed run with materialized P&L (or marked-to-market) in the prior
24h, identify outliers (top/bottom decile by impact), distill into a structured
`Lesson`, index into the `lessons` Qdrant namespace.

Anti-overfitting:
  - A lesson must appear in >= 3 distinct outcomes to gain weight
  - Lessons are decay-weighted (older lessons matter less unless reinforced)
  - A lesson cannot contradict a deterministic rule
"""
from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class Lesson(BaseModel):
    run_id: str
    ticker: str
    direction: str
    original_thesis_summary: str
    actual_outcome: str
    assumptions_held: list[str]
    assumptions_broken: list[str]
    early_signal_that_would_have_predicted: str
    one_paragraph_lesson: str
    distilled_at_utc: datetime
    reinforcement_count: int = 1


def distill_nightly() -> int:
    """Run the nightly distillation. Returns count of new lessons indexed."""
    raise NotImplementedError


def reinforce_or_index(lesson: Lesson) -> str:
    """If a near-duplicate lesson exists, increment reinforcement_count.
    Otherwise index as new. Returns the lesson_id."""
    raise NotImplementedError
