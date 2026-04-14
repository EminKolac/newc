"""OMS / FIX wrappers — IBKR (global), TR Prime (BIST)."""
from __future__ import annotations

from ..orchestrator.state import TradeRecommendation


def submit(trade: TradeRecommendation) -> str:
    """Submit a trade through the appropriate venue routing.

    Returns an order ID. Order is logged immutably for the audit trail.
    """
    raise NotImplementedError


def cancel_all() -> int:
    """Kill-switch helper: cancel every open order across every venue."""
    raise NotImplementedError


def get_positions() -> dict:
    """Return current positions (ticker -> {qty, mtm_value, avg_price})."""
    raise NotImplementedError
