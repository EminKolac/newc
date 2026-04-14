"""Adversarial / Red-Team Agent — falsify every thesis, surface the bear case.

Inherits from the founder's PhD-level adversarial multi-agent design.
Calibration is tracked: predicted-failure vs. realized-failure Brier score,
target band 0.55–0.65.
"""
from __future__ import annotations

from ..orchestrator.state import FundState, RedTeamReport
from .base import AgentBase, AgentSpec

SPEC = AgentSpec(
    name="adversarial",
    base_model="Qwen2.5-72B",
    lora_tag="redteam_v2",
    temperature=0.7,
    max_tokens=3000,
    rag_namespaces=(
        "behavioral_finance",
        "blowup_case_studies",
        "short_seller_reports",
        "lessons",
    ),
    output_schema=RedTeamReport,
)


class Adversarial(AgentBase):
    pass


def run(state: FundState) -> RedTeamReport:
    raise NotImplementedError("implemented in Phase 0; see roadmap")
