"""LangGraph state machine for Argus.

Wires the seven specialist agents + deterministic gates into the production graph
described in docs/architecture.md. This is a runnable skeleton — every node logs
its invocation and returns a placeholder. The agents' real implementations
arrive across Phases 0–1 of the roadmap.
"""
from __future__ import annotations

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver

from .state import FundState, Intent
from ..agents import (
    research_analyst,
    quant_strategist,
    risk_manager,
    macro_analyst,
    event_driven,
    compliance,
    adversarial,
    pm,
)
from ..tools import compliance as compliance_gate
from ..tools import execution


# ----- routing -------------------------------------------------------------

def route_after_classify(state: FundState) -> str:
    if state.intent == Intent.MACRO: return "macro_analyst"
    if state.intent == Intent.EVENT: return "event_driven"
    if state.intent == Intent.RISK: return "risk_manager"
    if state.intent == Intent.REBAL: return "quant_strategist"
    return "research_analyst"


def route_after_thesis(state: FundState) -> list[str]:
    """Fan out: quant + adversarial run in parallel after a thesis exists."""
    return ["quant_strategist", "adversarial"]


def route_after_compliance(state: FundState) -> str:
    if state.compliance is None or state.compliance.verdict == "block":
        return "log_and_terminate"
    return "pm"


def route_after_pm(state: FundState) -> str:
    if state.pm_recommendation is None:
        return "log_and_terminate"
    if abs(state.pm_recommendation.size_bps) > 50:
        return "human_approval"
    return "auto_execute"


# ----- node wrappers -------------------------------------------------------
#
# Each node is a thin adapter that calls the corresponding agent module and
# writes its output back into FundState. Agents are pure functions of state.

def n_classify(s: FundState) -> dict:
    # In the full implementation, an LLM classifies ambiguous payloads.
    # For known intent types it's a passthrough.
    return {}

def n_research(s: FundState) -> dict:
    return {"research": research_analyst.run(s)}

def n_quant(s: FundState) -> dict:
    return {"quant": quant_strategist.run(s)}

def n_risk(s: FundState) -> dict:
    return {"risk": risk_manager.run(s)}

def n_macro(s: FundState) -> dict:
    return {"macro": macro_analyst.run(s)}

def n_event(s: FundState) -> dict:
    return {"event": event_driven.run(s)}

def n_adversarial(s: FundState) -> dict:
    return {"adversarial": adversarial.run(s)}

def n_compliance(s: FundState) -> dict:
    llm_verdict = compliance.run(s)
    deterministic_passed = compliance_gate.deterministic_check(s)
    llm_verdict.deterministic_check_passed = deterministic_passed
    if not deterministic_passed:
        llm_verdict.verdict = "block"
    return {"compliance": llm_verdict}

def n_pm(s: FundState) -> dict:
    return {"pm_recommendation": pm.run(s)}

def n_human_approval(s: FundState) -> dict:
    # langgraph.interrupt() stops the graph and waits for human ack
    from langgraph.types import interrupt
    decision = interrupt({"trade": s.pm_recommendation.model_dump()})
    return {"final_decision": "execute" if decision == "approve" else "reject"}

def n_auto_execute(s: FundState) -> dict:
    execution.submit(s.pm_recommendation)
    return {"final_decision": "execute"}

def n_log_and_terminate(s: FundState) -> dict:
    return {"final_decision": "reject"}


# ----- assembly ------------------------------------------------------------

def build_graph(checkpointer: PostgresSaver | None = None):
    g = StateGraph(FundState)

    g.add_node("classify", n_classify)
    g.add_node("research_analyst", n_research)
    g.add_node("quant_strategist", n_quant)
    g.add_node("risk_manager", n_risk)
    g.add_node("macro_analyst", n_macro)
    g.add_node("event_driven", n_event)
    g.add_node("adversarial", n_adversarial)
    g.add_node("compliance", n_compliance)
    g.add_node("pm", n_pm)
    g.add_node("human_approval", n_human_approval)
    g.add_node("auto_execute", n_auto_execute)
    g.add_node("log_and_terminate", n_log_and_terminate)

    g.set_entry_point("classify")
    g.add_conditional_edges("classify", route_after_classify)

    # thesis fans out to quant + adversarial in parallel
    g.add_conditional_edges("research_analyst", route_after_thesis)
    g.add_conditional_edges("event_driven", route_after_thesis)
    g.add_conditional_edges("macro_analyst", lambda s: "risk_manager")

    # quant and adversarial both feed into risk_manager
    g.add_edge("quant_strategist", "risk_manager")
    g.add_edge("adversarial", "risk_manager")

    g.add_edge("risk_manager", "compliance")
    g.add_conditional_edges("compliance", route_after_compliance)
    g.add_conditional_edges("pm", route_after_pm)

    g.add_edge("human_approval", END)
    g.add_edge("auto_execute", END)
    g.add_edge("log_and_terminate", END)

    return g.compile(checkpointer=checkpointer)
