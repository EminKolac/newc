"""Risk Manager Agent — VaR, ES, factor decomp, stress (FRM-grounded)."""
from __future__ import annotations

from ..orchestrator.state import FundState, RiskAssessment
from .base import AgentBase, AgentSpec

SPEC = AgentSpec(
    name="risk_manager",
    base_model="Qwen2.5-72B",
    lora_tag="risk_v1",
    temperature=0.0,
    max_tokens=3000,
    rag_namespaces=("frm", "basel", "historical_crises", "lessons"),
    output_schema=RiskAssessment,
)


class RiskManager(AgentBase):
    pass


def run(state: FundState) -> RiskAssessment:
    raise NotImplementedError("implemented in Phase 0; see roadmap")
