"""Quant primitives — factor scores, Sharpe, DCF, comps, DuPont."""
from __future__ import annotations


def factor_score(ticker: str, factor: str) -> float:
    """Standardized z-score for a single factor (value, quality, momentum, ...)."""
    raise NotImplementedError


def composite_score(ticker: str, weights: dict[str, float]) -> float:
    raise NotImplementedError


def sharpe(returns: list[float], rf: float = 0.0) -> float:
    raise NotImplementedError


def dcf_model(ticker: str, **assumptions) -> dict:
    """Returns {'value_per_share', 'sensitivity_table', 'assumptions'}."""
    raise NotImplementedError


def comps_model(ticker: str, peers: list[str], multiples: list[str]) -> dict:
    raise NotImplementedError


def dupont(ticker: str, periods: int = 8) -> dict:
    """ROE = NM × AT × EM, decomposed and tracked over time."""
    raise NotImplementedError


def backtest(signal_fn, universe: list[str], start: str, end: str) -> dict:
    """Returns OOS Sharpe, max DD, turnover, hit rate. Look-ahead-safe by data layer."""
    raise NotImplementedError
