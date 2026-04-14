"""Quant Strategist Agent — factor signals, backtests, sizing (CQF-grounded)."""
from __future__ import annotations

from ..orchestrator.state import FundState, QuantSignal
from .base import AgentBase, AgentSpec

SPEC = AgentSpec(
    name="quant_strategist",
    base_model="Qwen2.5-72B",
    lora_tag="quant_v2",
    temperature=0.2,
    max_tokens=3000,
    rag_namespaces=("cqf", "factor_research_papers", "lessons"),
    output_schema=QuantSignal,
)


class QuantStrategist(AgentBase):
    pass


def run(state: FundState) -> QuantSignal:
    raise NotImplementedError("implemented in Phase 0; see roadmap")
