"""Research Analyst Agent — fundamental thesis generation (CFA L2-grounded)."""
from __future__ import annotations

from ..orchestrator.state import FundState, ResearchThesis
from .base import AgentBase, AgentSpec

SPEC = AgentSpec(
    name="research_analyst",
    base_model="Qwen2.5-72B",
    lora_tag="research_v3",
    temperature=0.4,
    max_tokens=4000,
    rag_namespaces=(
        "cfa_l2_equity",
        "cfa_l1_fsa",
        "kap_filings",
        "earnings_transcripts",
        "lessons",
    ),
    output_schema=ResearchThesis,
)


class ResearchAnalyst(AgentBase):
    pass


def run(state: FundState) -> ResearchThesis:
    """Produce a ResearchThesis for the ticker(s) in scope."""
    raise NotImplementedError("implemented in Phase 0; see roadmap")
