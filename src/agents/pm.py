"""PM Agent — reads all six specialist outputs, decides go/no-go, sizes, writes memo.

This is the only place the largest model (Qwen3-235B) is invoked.
The memo it produces is what the human PM ratifies and what eventually
appears (after editing) in LP letters.
"""
from __future__ import annotations

from ..orchestrator.state import FundState, TradeRecommendation
from .base import AgentBase, AgentSpec

SPEC = AgentSpec(
    name="pm",
    base_model="Qwen3-235B-A22B",
    lora_tag=None,
    temperature=0.2,
    max_tokens=6000,
    rag_namespaces=("cfa_l3_pm", "kelly_criterion", "lessons"),
    output_schema=TradeRecommendation,
)


class PM(AgentBase):
    pass


def run(state: FundState) -> TradeRecommendation:
    """Synthesize all agent outputs, resolve conflicts, decide, write memo.

    Hard contract: every red-team objection in `state.adversarial` MUST appear
    in `addressed_redteam_objections` of the output. Unresolved objections
    block the trade at the PM gate.
    """
    raise NotImplementedError("implemented in Phase 0; see roadmap")
