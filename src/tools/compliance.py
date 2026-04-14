"""Deterministic compliance and risk-envelope checks.

This is intentionally NOT an LLM. The Compliance Agent provides the nuanced
LLM check; this module is the mechanical, deterministic gate that runs after.
**Both** must pass for a trade to proceed.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

from ..orchestrator.state import FundState, TradeRecommendation


# ----- restricted list -----------------------------------------------------

_RESTRICTED_LIST_PATH = Path(__file__).parents[1] / "config" / "restricted_list.yaml"


def is_restricted(ticker: str, on_date: date | None = None) -> bool:
    """True if the name is on the restricted list as of `on_date` (default today)."""
    raise NotImplementedError


# ----- envelope ------------------------------------------------------------

_ENVELOPE_PATH = Path(__file__).parents[1] / "config" / "fund.yaml"


def load_envelope() -> dict:
    return yaml.safe_load(_ENVELOPE_PATH.read_text())["risk_envelope"]


def check_envelope(state: FundState, trade: TradeRecommendation) -> tuple[bool, list[str]]:
    """Apply every hard limit. Returns (passed, breach_list)."""
    raise NotImplementedError


# ----- the unified gate ----------------------------------------------------

def deterministic_check(state: FundState) -> bool:
    """Run every mechanical compliance + risk-envelope check.

    Called from the orchestrator AFTER the LLM Compliance Agent. Returns
    True only if every check passes.
    """
    if state.pm_recommendation is None:
        return False
    if is_restricted(state.pm_recommendation.ticker):
        return False
    passed, _ = check_envelope(state, state.pm_recommendation)
    return passed
