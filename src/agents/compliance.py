"""Compliance Agent — pre-trade rules check (SPK, SEC, MAR-grounded).

Belt-and-braces with the deterministic check in `tools/compliance.py` —
both must pass.
"""
from __future__ import annotations

from ..orchestrator.state import FundState, ComplianceVerdict
from .base import AgentBase, AgentSpec

SPEC = AgentSpec(
    name="compliance",
    base_model="Qwen2.5-32B",
    lora_tag=None,
    temperature=0.0,
    max_tokens=2000,
    rag_namespaces=("spk_regulations", "sec_rules", "mar", "argus_internal_policy"),
    output_schema=ComplianceVerdict,
)


class Compliance(AgentBase):
    pass


def run(state: FundState) -> ComplianceVerdict:
    raise NotImplementedError("implemented in Phase 0; see roadmap")
