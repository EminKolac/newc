"""Risk primitives — VaR, Expected Shortfall, factor decomposition, stress."""
from __future__ import annotations


def var(portfolio: dict, horizon_days: int = 1, confidence: float = 0.99) -> float:
    """Historical-simulation VaR. Returns loss in NAV bps."""
    raise NotImplementedError


def expected_shortfall(portfolio: dict, horizon_days: int = 1, confidence: float = 0.99) -> float:
    raise NotImplementedError


def factor_decomp(portfolio: dict) -> dict[str, float]:
    """Decompose portfolio risk into named factor exposures."""
    raise NotImplementedError


def stress_test(portfolio: dict, scenario: str) -> float:
    """Apply a named scenario (e.g. '2008_crash', 'tr_2018_lira', 'covid_2020')."""
    raise NotImplementedError


def liquidity_score(portfolio: dict, threshold_adv_pct: float = 0.25) -> float:
    """Days-to-liquidate at the given % of ADV. Lower is better; 0–1 normalized."""
    raise NotImplementedError


def correlation_regime(window_days: int = 60) -> str:
    """Classifies current market regime: low-vol, normal, stress, crisis."""
    raise NotImplementedError
