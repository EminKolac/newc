"""Portfolio construction — mean-variance, risk parity, Black-Litterman.

Wraps cvxpy / PyPortfolioOpt / Riskfolio-Lib.
"""
from __future__ import annotations


def mean_variance_optimize(expected_returns: dict, cov: dict, constraints: dict) -> dict:
    raise NotImplementedError


def risk_parity(cov: dict, target_vol_bps: float) -> dict:
    raise NotImplementedError


def black_litterman(prior: dict, views: list[dict]) -> dict:
    raise NotImplementedError


def kelly_size(edge: float, variance: float, kelly_fraction: float = 0.25) -> float:
    """Returns position size as fraction of NAV. Capped Kelly."""
    raise NotImplementedError
