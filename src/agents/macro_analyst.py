"""Macro Analyst Agent — daily macro brief, regime classification."""
from __future__ import annotations

from ..orchestrator.state import FundState, MacroBrief
from .base import AgentBase, AgentSpec

SPEC = AgentSpec(
    name="macro_analyst",
    base_model="Qwen2.5-72B",
    lora_tag=None,
    temperature=0.5,
    max_tokens=3500,
    rag_namespaces=(
        "cfa_econ",
        "tcmb_publications",
        "central_bank_minutes",
        "imf_weo",
        "lessons",
    ),
    output_schema=MacroBrief,
)


class MacroAnalyst(AgentBase):
    pass


def run(state: FundState) -> MacroBrief:
    raise NotImplementedError("implemented in Phase 0; see roadmap")
