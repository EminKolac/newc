"""Event-Driven Agent — M&A, capital raises, spinoffs (CAIA-grounded)."""
from __future__ import annotations

from ..orchestrator.state import FundState, EventReport
from .base import AgentBase, AgentSpec

SPEC = AgentSpec(
    name="event_driven",
    base_model="Qwen2.5-72B",
    lora_tag="event_v1",
    temperature=0.3,
    max_tokens=3000,
    rag_namespaces=(
        "caia_event",
        "kap_corporate_actions",
        "sec_8k",
        "historical_deals",
        "lessons",
    ),
    output_schema=EventReport,
)


class EventDriven(AgentBase):
    pass


def run(state: FundState) -> EventReport:
    raise NotImplementedError("implemented in Phase 0; see roadmap")
