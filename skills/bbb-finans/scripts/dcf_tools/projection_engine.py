#!/usr/bin/env python3
"""
10-Year DCF Projection Engine
Damodaran "Valuation output" sheet implementasyonu.

Revenue → Operating Margin Convergence → EBIT(1-t) → Reinvestment → FCFF
→ WACC interpolation → Discount Factor → PV(FCFF) + PV(Terminal Value)
→ Equity Bridge → Value per Share
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class DCFInputs:
    """DCF model girdileri."""
    # Revenue & Growth
    base_revenue: float                    # Current revenue (TTM)
    revenue_growth_rates: Optional[List[float]] = None  # Year 1-N growth rates (if provided)
    revenue_growth_year1: float = 0.10     # Year 1 growth rate (if rates not provided)
    revenue_growth_terminal: float = 0.03  # Terminal growth rate
    growth_convergence_year: int = 5       # Year where growth reaches terminal

    # Operating Margin
    current_op_margin: float = 0.10        # Current operating margin
    target_op_margin: float = 0.15         # Target operating margin (year of convergence)
    margin_convergence_year: int = 10      # Year margin reaches target

    # Tax
    effective_tax_rate: float = 0.25       # Current effective tax rate
    marginal_tax_rate: float = 0.25        # Marginal tax rate (converge to this)
    tax_convergence_year: int = 5          # Year tax reaches marginal

    # NOL
    nol_balance: float = 0.0              # Net operating loss carryforward

    # Reinvestment
    sales_to_capital: float = 2.0          # Sales / Invested Capital ratio

    # WACC
    wacc_current: float = 0.10             # Current WACC
    wacc_terminal: float = 0.08            # Terminal (stable) WACC
    wacc_convergence_year: int = 5         # Year WACC starts converging (6→10)

    # Terminal Value
    terminal_growth: float = 0.03          # g in perpetuity
    terminal_roc: Optional[float] = None   # Return on capital (if None, use WACC)

    # Equity Bridge
    cash: float = 0.0
    total_debt_mv: float = 0.0
    minority_interest: float = 0.0
    cross_holdings: float = 0.0
    option_value: float = 0.0
    shares_outstanding: float = 1.0

    # Failure probability
    prob_failure: float = 0.0
    distress_proceeds: float = 0.0

    # Projection years
    n_years: int = 10


@dataclass
class YearProjection:
    """Tek yıl projeksiyon çıktısı."""
    year: int
    revenue: float
    revenue_growth: float
    ebit: float
    op_margin: float
    tax_rate: float
    ebit_1_t: float          # EBIT(1-t), NOL adjusted
    nol_used: float
    reinvestment: float
    fcff: float
    wacc: float
    cum_discount_factor: float
    pv_fcff: float


@dataclass
class DCFResult:
    """DCF değerleme sonucu."""
    projections: List[YearProjection]
    pv_fcff_total: float
    terminal_fcff: float
    terminal_value: float
    pv_terminal_value: float
    operating_asset_value: float
    # Equity bridge
    plus_cash: float
    minus_debt: float
    minus_minority: float
    plus_cross_holdings: float
    minus_options: float
    equity_value: float
    value_per_share: float
    # Failure adjusted
    failure_adjusted_value: Optional[float] = None
    failure_adjusted_per_share: Optional[float] = None


def _interpolate(current: float, target: float, year: int,
                 start_year: int, end_year: int) -> float:
    """Linear interpolation between start_year and end_year."""
    if year <= start_year:
        return current
    if year >= end_year:
        return target
    frac = (year - start_year) / (end_year - start_year)
    return current + (target - current) * frac


def _compute_growth_rate(inputs: DCFInputs, year: int) -> float:
    """Yıla göre revenue growth rate hesapla.
    
    Damodaran Excel mantığı:
    - Year 1 → growth_convergence_year: revenue_growth_year1 (sabit)
    - growth_convergence_year+1 → n_years: linear interpolation → terminal_growth
    """
    if hasattr(inputs, 'revenue_growth_rates') and inputs.revenue_growth_rates:
        if year <= len(inputs.revenue_growth_rates):
            return inputs.revenue_growth_rates[year - 1]
    # Constant through convergence year, then linear interpolation to terminal
    return _interpolate(
        inputs.revenue_growth_year1, inputs.terminal_growth,
        year, inputs.growth_convergence_year, inputs.n_years
    )


def _compute_op_margin(inputs: DCFInputs, year: int) -> float:
    """Yıla göre operating margin (convergence)."""
    return _interpolate(
        inputs.current_op_margin, inputs.target_op_margin,
        year, 0, inputs.margin_convergence_year
    )


def _compute_tax_rate(inputs: DCFInputs, year: int) -> float:
    """Yıla göre effective → marginal tax convergence."""
    return _interpolate(
        inputs.effective_tax_rate, inputs.marginal_tax_rate,
        year, 0, inputs.tax_convergence_year
    )


def _compute_wacc(inputs: DCFInputs, year: int) -> float:
    """Yıla göre WACC interpolation (convergence_year → n_years)."""
    return _interpolate(
        inputs.wacc_current, inputs.wacc_terminal,
        year, inputs.wacc_convergence_year, inputs.n_years
    )


def run_dcf(inputs: DCFInputs) -> DCFResult:
    """
    10 yıllık DCF projeksiyon çalıştır.

    Damodaran Valuation Output sheet mantığı:
    1. Revenue projection (growth convergence)
    2. Operating margin convergence
    3. EBIT(1-t) with NOL shield
    4. Reinvestment = ΔRevenue / Sales-to-Capital
    5. FCFF = EBIT(1-t) - Reinvestment
    6. WACC interpolation
    7. Cumulative discount factor
    8. PV(FCFF) + PV(Terminal)
    9. Equity bridge
    """
    projections: List[YearProjection] = []
    prev_revenue = inputs.base_revenue
    cum_discount = 1.0
    pv_total = 0.0
    nol_remaining = inputs.nol_balance

    for yr in range(1, inputs.n_years + 1):
        # Growth & Revenue
        growth = _compute_growth_rate(inputs, yr)
        revenue = prev_revenue * (1 + growth)

        # Operating Margin & EBIT
        op_margin = _compute_op_margin(inputs, yr)
        ebit = revenue * op_margin

        # Tax rate
        tax_rate = _compute_tax_rate(inputs, yr)

        # EBIT(1-t) with NOL
        nol_used = 0.0
        if ebit > 0 and nol_remaining > 0:
            taxable = ebit
            nol_used = min(nol_remaining, taxable)
            nol_remaining -= nol_used
            # Tax on (EBIT - NOL_used), but NOPAT includes full EBIT operating
            ebit_1_t = ebit - (ebit - nol_used) * tax_rate
        elif ebit > 0:
            ebit_1_t = ebit * (1 - tax_rate)
        else:
            ebit_1_t = ebit  # Loss: no tax
            # Accumulate NOL
            nol_remaining += abs(ebit)

        # Reinvestment
        delta_revenue = revenue - prev_revenue
        if inputs.sales_to_capital > 0:
            reinvestment = delta_revenue / inputs.sales_to_capital
        else:
            reinvestment = 0.0

        # FCFF
        fcff = ebit_1_t - reinvestment

        # WACC & Discount
        wacc = _compute_wacc(inputs, yr)
        cum_discount = cum_discount / (1 + wacc)
        pv_fcff = fcff * cum_discount
        pv_total += pv_fcff

        proj = YearProjection(
            year=yr, revenue=revenue, revenue_growth=growth,
            ebit=ebit, op_margin=op_margin, tax_rate=tax_rate,
            ebit_1_t=ebit_1_t, nol_used=nol_used,
            reinvestment=reinvestment, fcff=fcff,
            wacc=wacc, cum_discount_factor=cum_discount, pv_fcff=pv_fcff,
        )
        projections.append(proj)
        prev_revenue = revenue

    # ─── Terminal Value ─────────────────────────────────────────
    last = projections[-1]
    terminal_wacc = inputs.wacc_terminal
    g = inputs.terminal_growth

    # Terminal year EBIT(1-t)
    terminal_revenue = last.revenue * (1 + g)
    terminal_ebit = terminal_revenue * inputs.target_op_margin
    terminal_nopat = terminal_ebit * (1 - inputs.marginal_tax_rate)

    # Terminal reinvestment
    roc = inputs.terminal_roc if inputs.terminal_roc else terminal_wacc
    if roc > 0:
        terminal_reinvestment_rate = g / roc
    else:
        terminal_reinvestment_rate = 0.0
    terminal_reinvestment = terminal_nopat * terminal_reinvestment_rate
    terminal_fcff = terminal_nopat - terminal_reinvestment

    # Terminal Value
    if terminal_wacc > g:
        terminal_value = terminal_fcff / (terminal_wacc - g)
    else:
        # Fallback: cap at large multiple
        terminal_value = terminal_fcff * 50

    pv_terminal = terminal_value * last.cum_discount_factor

    # ─── Operating Asset Value ──────────────────────────────────
    op_asset_value = pv_total + pv_terminal

    # ─── Equity Bridge ──────────────────────────────────────────
    equity_value = (
        op_asset_value
        + inputs.cash
        - inputs.total_debt_mv
        - inputs.minority_interest
        + inputs.cross_holdings
        - inputs.option_value
    )

    shares = inputs.shares_outstanding if inputs.shares_outstanding > 0 else 1.0
    value_per_share = equity_value / shares

    result = DCFResult(
        projections=projections,
        pv_fcff_total=round(pv_total, 2),
        terminal_fcff=round(terminal_fcff, 2),
        terminal_value=round(terminal_value, 2),
        pv_terminal_value=round(pv_terminal, 2),
        operating_asset_value=round(op_asset_value, 2),
        plus_cash=inputs.cash,
        minus_debt=inputs.total_debt_mv,
        minus_minority=inputs.minority_interest,
        plus_cross_holdings=inputs.cross_holdings,
        minus_options=inputs.option_value,
        equity_value=round(equity_value, 2),
        value_per_share=round(value_per_share, 4),
    )

    # Failure adjustment
    if inputs.prob_failure > 0:
        adjusted = equity_value * (1 - inputs.prob_failure) + inputs.distress_proceeds * inputs.prob_failure
        result.failure_adjusted_value = round(adjusted, 2)
        result.failure_adjusted_per_share = round(adjusted / shares, 4)

    return result


def print_dcf_result(result: DCFResult) -> None:
    """DCF sonucunu formatla ve yazdır."""
    print(f"\n{'Year':>4} {'Revenue':>14} {'Growth':>7} {'OpMargin':>8} "
          f"{'EBIT(1-t)':>12} {'Reinvest':>12} {'FCFF':>12} "
          f"{'WACC':>7} {'CumDF':>7} {'PV(FCFF)':>12}")
    print("-" * 110)

    for p in result.projections:
        print(f"{p.year:>4} {p.revenue:>14,.0f} {p.revenue_growth:>7.2%} "
              f"{p.op_margin:>8.2%} {p.ebit_1_t:>12,.0f} "
              f"{p.reinvestment:>12,.0f} {p.fcff:>12,.0f} "
              f"{p.wacc:>7.2%} {p.cum_discount_factor:>7.4f} "
              f"{p.pv_fcff:>12,.0f}")

    print(f"\n  PV(FCFF 1-{len(result.projections)}): {result.pv_fcff_total:>18,.0f}")
    print(f"  Terminal FCFF:           {result.terminal_fcff:>18,.0f}")
    print(f"  Terminal Value:          {result.terminal_value:>18,.0f}")
    print(f"  PV(Terminal Value):      {result.pv_terminal_value:>18,.0f}")
    print(f"  Operating Asset Value:   {result.operating_asset_value:>18,.0f}")
    print(f"\n  + Cash:                  {result.plus_cash:>18,.0f}")
    print(f"  - Debt:                  {result.minus_debt:>18,.0f}")
    print(f"  - Minority Interest:     {result.minus_minority:>18,.0f}")
    print(f"  + Cross Holdings:        {result.plus_cross_holdings:>18,.0f}")
    print(f"  - Options:               {result.minus_options:>18,.0f}")
    print(f"  = Equity Value:          {result.equity_value:>18,.0f}")
    print(f"  = Value per Share:       {result.value_per_share:>18,.4f}")

    if result.failure_adjusted_per_share is not None:
        print(f"  = Failure-Adj/Share:     {result.failure_adjusted_per_share:>18,.4f}")


if __name__ == "__main__":
    print("=== 10-Year DCF Projection Engine ===")

    inputs = DCFInputs(
        base_revenue=100_000,
        revenue_growth_year1=0.20,
        revenue_growth_terminal=0.03,
        growth_convergence_year=5,
        current_op_margin=0.08,
        target_op_margin=0.18,
        margin_convergence_year=10,
        effective_tax_rate=0.15,
        marginal_tax_rate=0.25,
        tax_convergence_year=5,
        nol_balance=5_000,
        sales_to_capital=2.5,
        wacc_current=0.12,
        wacc_terminal=0.09,
        wacc_convergence_year=5,
        terminal_growth=0.03,
        terminal_roc=0.12,
        cash=15_000,
        total_debt_mv=30_000,
        minority_interest=2_000,
        cross_holdings=0,
        option_value=1_500,
        shares_outstanding=1_000,
        prob_failure=0.05,
        distress_proceeds=20_000,
    )

    result = run_dcf(inputs)
    print_dcf_result(result)
    print("\n✅ projection_engine.py çalışıyor.")
