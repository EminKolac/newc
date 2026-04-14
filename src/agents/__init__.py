"""Specialist agents. Each module exposes `run(state) -> AgentOutput`."""
from . import (
    research_analyst,
    quant_strategist,
    risk_manager,
    macro_analyst,
    event_driven,
    compliance,
    adversarial,
    pm,
)

__all__ = [
    "research_analyst",
    "quant_strategist",
    "risk_manager",
    "macro_analyst",
    "event_driven",
    "compliance",
    "adversarial",
    "pm",
]
