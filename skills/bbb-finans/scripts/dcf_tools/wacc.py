#!/usr/bin/env python3
"""
WACC (Weighted Average Cost of Capital) Hesaplama Modülü
Damodaran "Cost of capital worksheet" implementasyonu.

Formüller:
  β_L = β_U × (1 + (1-t) × D/E)
  Ke  = Rf + β_L × Mature_ERP + λ × Country_ERP
  WACC = (E/V)×Ke + (D/V)×Kd×(1-t) + (PS/V)×Kps
"""

from typing import Dict, Optional


def compute_levered_beta(
    unlevered_beta: float,
    tax_rate: float,
    debt_equity_ratio: float,
) -> float:
    """
    Levered beta hesaplar (Hamada equation).
    β_L = β_U × (1 + (1 - t) × D/E)

    Args:
        unlevered_beta: Sektör unlevered beta
        tax_rate: Marginal vergi oranı (decimal, e.g. 0.25)
        debt_equity_ratio: D/E (market value debt / market value equity)

    Returns:
        Levered beta
    """
    if debt_equity_ratio < 0:
        debt_equity_ratio = 0.0
    return unlevered_beta * (1 + (1 - tax_rate) * debt_equity_ratio)


def compute_cost_of_equity(
    rf: float,
    levered_beta: float,
    erp: float,
    country_erp: float = 0.0,
    lambda_factor: float = 1.0,
) -> float:
    """
    Cost of equity hesaplar.
    Ke = Rf + β_L × Mature_ERP + λ × Country_ERP

    Args:
        rf: Risk-free rate (decimal)
        levered_beta: Levered beta
        erp: Mature market equity risk premium (decimal)
        country_erp: Country equity risk premium (decimal)
        lambda_factor: Lambda — şirketin ülke riskine maruziyeti (0-1, default 1.0)

    Returns:
        Cost of equity (decimal)
    """
    return rf + levered_beta * erp + lambda_factor * country_erp


def compute_wacc(
    market_cap: float,
    total_debt_mv: float,
    ke: float,
    kd_pretax: float,
    tax_rate: float,
    preferred_stock_mv: float = 0.0,
    kps: float = 0.0,
) -> float:
    """
    WACC hesaplar.
    WACC = (E/V)×Ke + (D/V)×Kd×(1-t) + (PS/V)×Kps

    Args:
        market_cap: Equity market value
        total_debt_mv: Debt market value
        ke: Cost of equity (decimal)
        kd_pretax: Pre-tax cost of debt (decimal)
        tax_rate: Marginal tax rate (decimal)
        preferred_stock_mv: Preferred stock market value
        kps: Cost of preferred stock (decimal)

    Returns:
        WACC (decimal)
    """
    total_capital = market_cap + total_debt_mv + preferred_stock_mv
    if total_capital <= 0:
        return ke  # fallback: all equity

    w_e = market_cap / total_capital
    w_d = total_debt_mv / total_capital
    w_ps = preferred_stock_mv / total_capital

    return w_e * ke + w_d * kd_pretax * (1 - tax_rate) + w_ps * kps


def compute_full_wacc(
    unlevered_beta: float,
    rf: float,
    erp: float,
    market_cap: float,
    total_debt_mv: float,
    kd_pretax: float,
    tax_rate: float,
    country_erp: float = 0.0,
    lambda_factor: float = 1.0,
    preferred_stock_mv: float = 0.0,
    kps: float = 0.0,
) -> Dict[str, float]:
    """
    Tam WACC hesaplama pipeline'ı.

    Returns:
        Dict with levered_beta, ke, wacc, and all weights.
    """
    de_ratio = total_debt_mv / market_cap if market_cap > 0 else 0.0
    levered_beta = compute_levered_beta(unlevered_beta, tax_rate, de_ratio)
    ke = compute_cost_of_equity(rf, levered_beta, erp, country_erp, lambda_factor)
    wacc = compute_wacc(market_cap, total_debt_mv, ke, kd_pretax, tax_rate,
                        preferred_stock_mv, kps)

    total_capital = market_cap + total_debt_mv + preferred_stock_mv

    return {
        "unlevered_beta": unlevered_beta,
        "levered_beta": round(levered_beta, 4),
        "debt_equity_ratio": round(de_ratio, 4),
        "ke": round(ke, 6),
        "kd_pretax": kd_pretax,
        "kd_aftertax": round(kd_pretax * (1 - tax_rate), 6),
        "wacc": round(wacc, 6),
        "weight_equity": round(market_cap / total_capital, 4) if total_capital > 0 else 1.0,
        "weight_debt": round(total_debt_mv / total_capital, 4) if total_capital > 0 else 0.0,
        "weight_preferred": round(preferred_stock_mv / total_capital, 4) if total_capital > 0 else 0.0,
        "tax_rate": tax_rate,
        "rf": rf,
        "erp": erp,
        "country_erp": country_erp,
    }


if __name__ == "__main__":
    print("=== WACC Hesaplama Modülü ===\n")

    # Test: Türk şirketi örneği
    result = compute_full_wacc(
        unlevered_beta=0.80,
        rf=0.045,       # US 10Y
        erp=0.0472,     # Mature market ERP
        market_cap=50_000,  # $50B (milyon)
        total_debt_mv=20_000,
        kd_pretax=0.08,
        tax_rate=0.25,
        country_erp=0.0726,  # Turkey CRP
        lambda_factor=1.0,
    )

    print(f"  Unlevered Beta:  {result['unlevered_beta']:.4f}")
    print(f"  D/E Ratio:       {result['debt_equity_ratio']:.4f}")
    print(f"  Levered Beta:    {result['levered_beta']:.4f}")
    print(f"  Cost of Equity:  {result['ke']:.4%}")
    print(f"  Pre-tax Kd:      {result['kd_pretax']:.4%}")
    print(f"  After-tax Kd:    {result['kd_aftertax']:.4%}")
    print(f"  WACC:            {result['wacc']:.4%}")
    print(f"  E/V:             {result['weight_equity']:.4f}")
    print(f"  D/V:             {result['weight_debt']:.4f}")

    # Edge case: all equity
    print("\n  --- All Equity ---")
    r2 = compute_full_wacc(0.80, 0.045, 0.0472, 100_000, 0, 0.08, 0.25)
    print(f"  WACC = Ke = {r2['wacc']:.4%}")

    print("\n✅ wacc.py çalışıyor.")
