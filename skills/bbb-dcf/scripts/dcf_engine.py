#!/usr/bin/env python3
"""
DCF Engine - Damodaran FCFF Methodology
BBB DCF Toolkit v2.0

Explicit parametre alir, hesaplar, sonuc doner.
Veri ALMAZ, karar VERMEZ. Tum girdiler disaridan gelir.

Ozellikler:
- Damodaran 10Y projeksiyon mekanigi
- Reinvestment = dRevenue / S/C (Damodaran yontemi)
- Terminal Value: EBIT(1-t) x (1 - g/ROC) / (WACC - g)
- NOL birikimi ve kullanimi
- IAS 29 duzeltmeleri (parasal K/Z cikarma, tek seferlik add-back)
- Time-varying WACC destegi
- Equity Bridge (borc, azinlik, nakit, istirak, opsiyon)
- Bear/Base/Bull senaryo destegi
- Sensitivity grid (WACC vs g, Buyume vs Marj)

Kullanim:
    from dcf_engine import DCFEngine

    engine = DCFEngine(
        base_revenue=27675, base_ebit=2404, ...
    )
    result = engine.calculate()
    print(result.summary())

Referanslar:
    - bbb-dcf/SKILL.md Adim 1-9
    - bbb-dcf/methodology/dcf_deep_dive.md
    - bbb-dcf/references/formula_card.md
    - Damodaran fcffsimpleginzu.xlsx
"""

import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any


# ============================================================
# VERI SINIFLARI
# ============================================================

@dataclass
class ProjectionYear:
    """Tek bir projeksiyon yilinin tum verisi."""
    year: int                    # 1-10
    revenue_growth: float        # %
    revenue: float               # M
    ebit_margin: float           # %
    ebit: float                  # M
    tax_rate: float              # %
    ebit_1_t: float              # EBIT x (1-t), NOL sonrasi
    nol_used: float              # Bu yil kullanilan NOL
    nol_balance: float           # Kalan NOL
    reinvestment: float          # M (Damodaran: dRev / S/C)
    fcff: float                  # M
    sales_to_capital: float      # S/C
    wacc: float                  # % (yillik)
    discount_factor: float       # Kumulatif iskonto faktoru
    pv_fcff: float               # M (bugunku deger)


@dataclass
class TerminalData:
    """Terminal deger hesaplamasi."""
    terminal_revenue: float
    terminal_ebit: float
    terminal_ebit_margin: float
    terminal_ebit_1_t: float
    terminal_roc: float          # % (Return on Capital)
    terminal_reinvestment_rate: float  # g / ROC
    terminal_fcff: float
    terminal_growth: float       # %
    terminal_wacc: float         # %
    terminal_value: float        # M (TV = FCFF / (WACC - g))
    pv_terminal: float           # M (bugunku deger)


@dataclass
class EquityBridge:
    """Firma degerinden ozsermaye degerine kopru."""
    pv_projection: float         # PV(10Y FCFF)
    pv_terminal: float           # PV(TV)
    operating_assets: float      # Toplam faaliyet varlik degeri
    prob_failure: float          # Iflas olasiligi
    distress_proceeds: float     # Iflas halinde tasfiye geliri
    adjusted_value: float        # Iflas duzeltmeli deger
    minus_debt: float            # - Borc
    minus_minority: float        # - Azinlik paylari
    plus_cash: float             # + Nakit
    plus_cross_holdings: float   # + Istirakler
    minus_options: float         # - Calisan opsiyonlari
    equity_value: float          # Ozsermaye degeri
    shares: float                # Pay sayisi (M)
    value_per_share: float       # Hisse basina deger


@dataclass
class DCFResult:
    """Tam DCF sonucu."""
    # Meta
    scenario_name: str           # "Base", "Bull", "Bear"
    currency: str                # "TL", "USD"
    base_year: str               # "FY2025"

    # Girdiler
    base_revenue: float
    base_ebit: float
    base_ebit_margin: float

    # Projeksiyon
    projections: List[ProjectionYear]
    terminal: TerminalData
    bridge: EquityBridge

    # Onemli metrikler
    implied_ev_ebitda: Optional[float]
    implied_pe: Optional[float]
    tv_pct_of_ev: float          # TV / EV yuzdesi

    # Sanity checks
    warnings: List[str]

    def to_dict(self) -> dict:
        d = asdict(self)
        return d

    def to_json(self, indent=2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def summary(self) -> str:
        b = self.bridge
        t = self.terminal
        lines = [
            "=" * 60,
            f"DCF DEGERLEME SONUCU - {self.scenario_name} ({self.currency})",
            f"Baz Donem: {self.base_year}",
            "=" * 60,
            "",
            "PROJEKSIYON OZETI",
            "-" * 60,
            f"{'Yil':<6}{'Gelir':>12}{'Buyume':>8}{'EBIT':>12}{'Marj':>7}{'FCFF':>12}{'WACC':>7}{'PV':>12}",
            "-" * 60,
        ]
        for p in self.projections:
            lines.append(
                f"Y{p.year:<5}{p.revenue:>12,.0f}{p.revenue_growth:>7.1f}%"
                f"{p.ebit:>12,.0f}{p.ebit_margin:>6.1f}%"
                f"{p.fcff:>12,.0f}{p.wacc:>6.1f}%{p.pv_fcff:>12,.0f}"
            )
        lines.extend([
            "-" * 60,
            f"{'Term':<6}{t.terminal_revenue:>12,.0f}{t.terminal_growth:>7.1f}%"
            f"{t.terminal_ebit:>12,.0f}{t.terminal_ebit_margin:>6.1f}%"
            f"{t.terminal_fcff:>12,.0f}{t.terminal_wacc:>6.1f}%",
            "",
            "DEGERLEME",
            "-" * 60,
            f"  PV Projeksiyon:       {b.pv_projection:>15,.0f}",
            f"  PV Terminal:          {b.pv_terminal:>15,.0f}",
            f"  Faaliyet Varlik:      {b.operating_assets:>15,.0f}",
        ])
        if b.prob_failure > 0:
            lines.append(f"  x Iflas duzeltme:     {b.adjusted_value:>15,.0f}")
        lines.extend([
            f"  (-) Borc:             {b.minus_debt:>15,.0f}",
            f"  (-) Azinlik:          {b.minus_minority:>15,.0f}",
            f"  (+) Nakit:            {b.plus_cash:>15,.0f}",
            f"  (+) Istirakler:       {b.plus_cross_holdings:>15,.0f}",
            f"  (-) Opsiyonlar:       {b.minus_options:>15,.0f}",
            f"  = Ozsermaye Degeri:   {b.equity_value:>15,.0f}",
            f"  / Pay Sayisi (M):     {b.shares:>15,.1f}",
            f"  = Hisse Degeri:       {b.value_per_share:>15,.2f}",
            "",
            "SANITY CHECK",
            "-" * 60,
            f"  TV / EV:              {self.tv_pct_of_ev:>14.1f}%",
        ])
        if self.implied_ev_ebitda:
            lines.append(f"  Implied EV/EBITDA:    {self.implied_ev_ebitda:>14.1f}x")
        if self.implied_pe:
            lines.append(f"  Implied P/E:          {self.implied_pe:>14.1f}x")
        if self.warnings:
            lines.extend(["", "UYARILAR", "-" * 60])
            for w in self.warnings:
                lines.append(f"  ! {w}")
        lines.append("=" * 60)
        return "\n".join(lines)


# ============================================================
# DCF ENGINE
# ============================================================

class DCFEngine:
    """
    Damodaran FCFF DCF motoru.

    Tum parametreler explicit olarak verilir.
    Motor hicbir varsayim YAPMAZ, veri ALMAZ, karar VERMEZ.
    """

    def __init__(
        self,
        # Baz yil verileri
        base_revenue: float,           # M
        base_ebit: float,              # M (IAS 29 duzeltilmis ise duzeltilmis EBIT)
        base_da: float = 0.0,         # M (D&A, referans icin)

        # Buyume (10 yillik liste VEYA Y1-5 + Y6-10)
        revenue_growth: Optional[List[float]] = None,  # [%] 10 eleman
        revenue_growth_y1_5: Optional[float] = None,   # % (sabit)
        revenue_growth_y6_10: Optional[float] = None,  # % (sabit)
        terminal_growth: float = 2.0,  # %

        # Marj
        base_ebit_margin: Optional[float] = None,  # % (override, yoksa hesaplanir)
        target_ebit_margin: Optional[float] = None,  # % (terminal marj hedefi)
        margin_convergence_year: int = 7,  # Hedef marja ulasma yili

        # Yeniden yatirim
        sales_to_capital: float = 2.0,       # S/C (Y1-5)
        sales_to_capital_terminal: Optional[float] = None,  # S/C (Y6-10+)

        # Vergi
        tax_rate: float = 25.0,        # % (efektif, Y1-5)
        terminal_tax_rate: Optional[float] = None,  # % (terminal, Y6-10)
        nol_initial: float = 0.0,      # NOL baslangic bakiyesi (M)

        # WACC (listeler = time-varying)
        wacc: Optional[float] = None,           # % (sabit WACC)
        wacc_schedule: Optional[List[float]] = None,  # [%] 10 eleman
        terminal_wacc: Optional[float] = None,   # %

        # Terminal
        terminal_roc: Optional[float] = None,   # % (ROC terminal, yoksa = WACC)

        # Equity Bridge
        total_debt: float = 0.0,       # M
        cash: float = 0.0,             # M
        minority_interest: float = 0.0,  # M
        cross_holdings: float = 0.0,   # M
        employee_options: float = 0.0,  # M
        shares: float = 100.0,         # M

        # Iflas
        prob_failure: float = 0.0,     # 0-1
        distress_proceeds_pct: float = 0.0,  # Tasfiye/EV orani

        # IAS 29 ozel
        monetary_gain_loss: float = 0.0,  # M (cikarilacak)
        one_time_items: float = 0.0,      # M (add-back)

        # Meta
        scenario_name: str = "Base",
        currency: str = "TL",
        base_year: str = "FY2025",

        # Referans (hesaplamaya katilmaz)
        base_ebitda: Optional[float] = None,  # Sanity check icin
        current_price: Optional[float] = None,
    ):
        self.base_revenue = base_revenue
        self.base_da = base_da
        self.terminal_growth = terminal_growth
        self.margin_convergence_year = margin_convergence_year
        self.sales_to_capital = sales_to_capital
        self.sales_to_capital_terminal = sales_to_capital_terminal or sales_to_capital
        self.nol_balance = nol_initial
        self.total_debt = total_debt
        self.cash = cash
        self.minority_interest = minority_interest
        self.cross_holdings = cross_holdings
        self.employee_options = employee_options
        self.shares = shares
        self.prob_failure = prob_failure
        self.distress_proceeds_pct = distress_proceeds_pct
        self.monetary_gain_loss = monetary_gain_loss
        self.one_time_items = one_time_items
        self.scenario_name = scenario_name
        self.currency = currency
        self.base_year = base_year
        self.base_ebitda = base_ebitda
        self.current_price = current_price
        self._warnings = []

        # EBIT duzeltmesi (IAS 29)
        self.base_ebit = base_ebit + one_time_items  # Tek seferlik add-back

        # Baz marj
        if base_ebit_margin is not None:
            self.base_ebit_margin = base_ebit_margin
        else:
            self.base_ebit_margin = (self.base_ebit / base_revenue * 100
                                     if base_revenue > 0 else 0)

        # Hedef marj
        self.target_ebit_margin = target_ebit_margin or self.base_ebit_margin

        # Buyume dizisi (10 yil)
        if revenue_growth is not None:
            if len(revenue_growth) == 10:
                self.growth_schedule = revenue_growth
            else:
                self._warnings.append(
                    f"revenue_growth {len(revenue_growth)} eleman, 10 bekleniyor. "
                    "Son degere pad edildi.")
                self.growth_schedule = (revenue_growth +
                    [revenue_growth[-1]] * (10 - len(revenue_growth)))[:10]
        elif revenue_growth_y1_5 is not None:
            g1 = revenue_growth_y1_5
            g2 = revenue_growth_y6_10 if revenue_growth_y6_10 is not None else terminal_growth
            self.growth_schedule = [g1] * 5
            # Y6-10: lineer interpolasyon -> terminal
            for y in range(5):
                progress = (y + 1) / 5
                self.growth_schedule.append(g1 + (g2 - g1) * progress)
        else:
            self._warnings.append("Buyume orani belirtilmedi, %5 varsayildi")
            self.growth_schedule = [5.0] * 10

        # Vergi dizisi
        self.tax_rate_y1 = tax_rate
        self.terminal_tax = terminal_tax_rate or tax_rate
        self.tax_schedule = self._build_tax_schedule(tax_rate, self.terminal_tax)

        # WACC dizisi
        if wacc_schedule is not None:
            self.wacc_schedule = wacc_schedule[:10]
            if len(self.wacc_schedule) < 10:
                self.wacc_schedule += [self.wacc_schedule[-1]] * (10 - len(self.wacc_schedule))
        elif wacc is not None:
            tw = terminal_wacc or wacc
            # Y1-5 sabit, Y6-10 interpolasyon
            self.wacc_schedule = [wacc] * 5
            for y in range(5):
                progress = (y + 1) / 5
                self.wacc_schedule.append(wacc + (tw - wacc) * progress)
        else:
            self._warnings.append("WACC belirtilmedi, %10 varsayildi")
            self.wacc_schedule = [10.0] * 10

        self.terminal_wacc_val = terminal_wacc or self.wacc_schedule[-1]

        # Terminal ROC
        self.terminal_roc = terminal_roc or self.terminal_wacc_val

    def _build_tax_schedule(self, tax_y1: float, tax_terminal: float) -> List[float]:
        """Vergi orani dizisi: Y1-5 efektif, Y6-10 interpolasyon -> terminal."""
        schedule = [tax_y1] * 5
        for y in range(5):
            progress = (y + 1) / 5
            schedule.append(tax_y1 + (tax_terminal - tax_y1) * progress)
        return schedule

    def _margin_for_year(self, year: int) -> float:
        """EBIT marji interpolasyonu: baz -> hedef (convergence_year'da)."""
        if year >= self.margin_convergence_year:
            return self.target_ebit_margin
        progress = year / self.margin_convergence_year
        return self.base_ebit_margin + (self.target_ebit_margin - self.base_ebit_margin) * progress

    def _sc_for_year(self, year: int) -> float:
        """S/C: Y1-5 = base, Y6-10 interpolasyon -> terminal."""
        if year <= 5:
            return self.sales_to_capital
        progress = (year - 5) / 5
        return self.sales_to_capital + (self.sales_to_capital_terminal - self.sales_to_capital) * progress

    def calculate(self) -> DCFResult:
        """Ana hesaplama. 10Y projeksiyon + TV + Equity Bridge."""

        projections = []
        prev_revenue = self.base_revenue
        cumulative_df = 1.0
        pv_total = 0.0
        nol = self.nol_balance

        for y in range(1, 11):
            # Buyume
            g = self.growth_schedule[y - 1]
            revenue = prev_revenue * (1 + g / 100)

            # EBIT marji
            margin = self._margin_for_year(y)
            ebit = revenue * margin / 100

            # Vergi + NOL
            tax_r = self.tax_schedule[y - 1]
            if ebit > 0:
                if nol > 0 and ebit <= nol:
                    ebit_1_t = ebit  # Tamamen korunmali
                    nol_used = ebit
                    nol -= ebit
                elif nol > 0:
                    ebit_1_t = nol + (ebit - nol) * (1 - tax_r / 100)
                    nol_used = nol
                    nol = 0
                else:
                    ebit_1_t = ebit * (1 - tax_r / 100)
                    nol_used = 0
            else:
                ebit_1_t = ebit  # Negatif, vergi yok
                nol_used = 0
                nol += abs(ebit)  # NOL birikir

            # Reinvestment (Damodaran yontemi: dRevenue / S/C)
            sc = self._sc_for_year(y)
            delta_rev = revenue - prev_revenue
            reinvestment = delta_rev / sc if sc > 0 else 0

            # FCFF
            fcff = ebit_1_t - reinvestment

            # WACC & iskonto
            wacc_y = self.wacc_schedule[y - 1]
            cumulative_df = cumulative_df / (1 + wacc_y / 100)
            pv_fcff = fcff * cumulative_df

            pv_total += pv_fcff

            projections.append(ProjectionYear(
                year=y,
                revenue_growth=round(g, 2),
                revenue=round(revenue, 2),
                ebit_margin=round(margin, 2),
                ebit=round(ebit, 2),
                tax_rate=round(tax_r, 2),
                ebit_1_t=round(ebit_1_t, 2),
                nol_used=round(nol_used, 2),
                nol_balance=round(nol, 2),
                reinvestment=round(reinvestment, 2),
                fcff=round(fcff, 2),
                sales_to_capital=round(sc, 2),
                wacc=round(wacc_y, 2),
                discount_factor=round(cumulative_df, 6),
                pv_fcff=round(pv_fcff, 2),
            ))

            prev_revenue = revenue

        # Terminal Value
        last = projections[-1]
        tg = self.terminal_growth
        t_revenue = last.revenue * (1 + tg / 100)
        t_margin = self.target_ebit_margin
        t_ebit = t_revenue * t_margin / 100
        t_tax = self.terminal_tax
        t_ebit_1_t = t_ebit * (1 - t_tax / 100)

        t_roc = self.terminal_roc
        t_rr = (tg / t_roc) if t_roc > 0 else 0  # g / ROC
        t_fcff = t_ebit_1_t * (1 - t_rr)

        tw = self.terminal_wacc_val
        if tw <= tg:
            self._warnings.append(
                f"KRITIK: Terminal WACC ({tw}%) <= Terminal g ({tg}%). "
                "TV sonsuz. Terminal WACC arttirildi.")
            tw = tg + 1.0

        tv = t_fcff / (tw / 100 - tg / 100)
        pv_tv = tv * cumulative_df

        terminal = TerminalData(
            terminal_revenue=round(t_revenue, 2),
            terminal_ebit=round(t_ebit, 2),
            terminal_ebit_margin=round(t_margin, 2),
            terminal_ebit_1_t=round(t_ebit_1_t, 2),
            terminal_roc=round(t_roc, 2),
            terminal_reinvestment_rate=round(t_rr * 100, 2),
            terminal_fcff=round(t_fcff, 2),
            terminal_growth=round(tg, 2),
            terminal_wacc=round(tw, 2),
            terminal_value=round(tv, 2),
            pv_terminal=round(pv_tv, 2),
        )

        # Equity Bridge
        op_assets = pv_total + pv_tv

        if self.prob_failure > 0:
            distress_val = op_assets * self.distress_proceeds_pct
            adjusted = op_assets * (1 - self.prob_failure) + distress_val * self.prob_failure
        else:
            adjusted = op_assets

        equity_val = (adjusted
                      - self.total_debt
                      - self.minority_interest
                      + self.cash
                      + self.cross_holdings
                      - self.employee_options)

        vps = equity_val / self.shares if self.shares > 0 else 0

        bridge = EquityBridge(
            pv_projection=round(pv_total, 2),
            pv_terminal=round(pv_tv, 2),
            operating_assets=round(op_assets, 2),
            prob_failure=self.prob_failure,
            distress_proceeds=round(op_assets * self.distress_proceeds_pct, 2) if self.prob_failure > 0 else 0,
            adjusted_value=round(adjusted, 2),
            minus_debt=round(self.total_debt, 2),
            minus_minority=round(self.minority_interest, 2),
            plus_cash=round(self.cash, 2),
            plus_cross_holdings=round(self.cross_holdings, 2),
            minus_options=round(self.employee_options, 2),
            equity_value=round(equity_val, 2),
            shares=self.shares,
            value_per_share=round(vps, 2),
        )

        # Sanity checks
        tv_pct = pv_tv / op_assets * 100 if op_assets > 0 else 0
        if tv_pct > 90:
            self._warnings.append(f"TV/EV = {tv_pct:.0f}% (>90%): projeksiyon donemi cok kisa veya buyume cok dusuk")
        elif tv_pct > 75:
            self._warnings.append(f"TV/EV = {tv_pct:.0f}% (>75%): terminal varsayimlarini kontrol et")

        if vps < 0:
            self._warnings.append(f"Hisse degeri negatif ({vps:.2f}): borc > firma degeri?")

        # Implied carpanlar
        implied_ev_ebitda = None
        if self.base_ebitda and self.base_ebitda > 0:
            ev_implied = equity_val + self.total_debt - self.cash
            implied_ev_ebitda = ev_implied / self.base_ebitda

        implied_pe = None
        if self.current_price and self.current_price > 0 and vps > 0:
            implied_pe = vps / (self.base_ebit * (1 - self.tax_rate_y1 / 100) / self.shares) \
                if self.base_ebit > 0 else None

        return DCFResult(
            scenario_name=self.scenario_name,
            currency=self.currency,
            base_year=self.base_year,
            base_revenue=self.base_revenue,
            base_ebit=self.base_ebit,
            base_ebit_margin=round(self.base_ebit_margin, 2),
            projections=projections,
            terminal=terminal,
            bridge=bridge,
            implied_ev_ebitda=round(implied_ev_ebitda, 2) if implied_ev_ebitda else None,
            implied_pe=round(implied_pe, 2) if implied_pe else None,
            tv_pct_of_ev=round(tv_pct, 2),
            warnings=self._warnings,
        )


# ============================================================
# SENSITIVITY GRID
# ============================================================

def sensitivity_grid(engine_params: dict,
                     row_param: str, row_values: List[float],
                     col_param: str, col_values: List[float]) -> List[List[float]]:
    """
    2D sensitivity grid olustur.

    Args:
        engine_params: DCFEngine'e verilecek parametre dict'i
        row_param: Satir ekseni parametresi (orn: "wacc")
        row_values: Satir degerleri
        col_param: Sutun ekseni parametresi (orn: "terminal_growth")
        col_values: Sutun degerleri

    Returns:
        2D liste: grid[row][col] = value_per_share
    """
    grid = []
    for rv in row_values:
        row = []
        for cv in col_values:
            params = dict(engine_params)
            # WACC icin ozel handling (schedule guncellenir)
            if row_param == "wacc":
                base_wacc = rv
                tw = params.get("terminal_wacc", rv)
                params["wacc"] = base_wacc
                params["wacc_schedule"] = None  # Sabit WACC mod
            else:
                params[row_param] = rv

            if col_param == "terminal_growth":
                params["terminal_growth"] = cv
            elif col_param == "wacc":
                params["wacc"] = cv
                params["wacc_schedule"] = None
            else:
                params[col_param] = cv

            try:
                engine = DCFEngine(**params)
                result = engine.calculate()
                row.append(round(result.bridge.value_per_share, 2))
            except Exception:
                row.append(None)
        grid.append(row)
    return grid


def format_sensitivity_grid(grid: List[List[float]],
                            row_label: str, row_values: List[float],
                            col_label: str, col_values: List[float],
                            currency: str = "TL") -> str:
    """Sensitivity grid'i tablo olarak formatla."""
    # Header
    col_headers = [f"{cv:.1f}%" for cv in col_values]
    header = f"{'':>12} | " + " | ".join(f"{ch:>10}" for ch in col_headers)
    separator = "-" * len(header)

    lines = [
        f"Sensitivity: {row_label} vs {col_label}",
        separator,
        header,
        separator,
    ]

    for i, rv in enumerate(row_values):
        vals = []
        for v in grid[i]:
            if v is not None:
                vals.append(f"{v:>10,.2f}")
            else:
                vals.append(f"{'ERR':>10}")
        lines.append(f"{rv:>10.1f}% | " + " | ".join(vals))

    lines.append(separator)
    return "\n".join(lines)


# ============================================================
# CLI
# ============================================================

def main():
    """Basit CLI - gercek kullanim modul import ile."""
    if len(sys.argv) < 2 or sys.argv[1] == "--help":
        print("DCF Engine v2.0 - Modul olarak kullan:")
        print("  from dcf_engine import DCFEngine")
        print("  engine = DCFEngine(base_revenue=..., base_ebit=..., ...)")
        print("  result = engine.calculate()")
        print("  print(result.summary())")
        print()
        print("EBEBK ornek:")
        print("  python dcf_engine.py --demo")
        return

    if sys.argv[1] == "--demo":
        # EBEBK demo (TL bazli, IAS 29 duzeltilmis)
        engine = DCFEngine(
            base_revenue=27675,
            base_ebit=2404,         # Duzeltilmis (vadeli alim add-back)
            base_da=1136,
            revenue_growth=[18, 15, 12, 12, 10, 8, 6, 5, 4, 3],
            terminal_growth=15.0,   # TL nominal
            target_ebit_margin=14.0,
            margin_convergence_year=7,
            sales_to_capital=5.65,
            sales_to_capital_terminal=4.0,
            tax_rate=23.0,
            terminal_tax_rate=25.0,
            wacc=38.38,             # TL (Fisher)
            terminal_wacc=19.35,    # TL (Fisher, terminal)
            terminal_roc=19.35,     # ROC = WACC (moat yok)
            total_debt=3385,
            cash=2854,
            minority_interest=0,
            shares=160,
            one_time_items=65,      # Tuna Cocuk write-down
            monetary_gain_loss=1109,
            scenario_name="Base",
            currency="TL",
            base_year="FY2025",
            base_ebitda=3540,       # Sunum FAVOK
            current_price=61.85,
        )
        result = engine.calculate()
        print(result.summary())

        # Sensitivity
        print()
        params = dict(
            base_revenue=27675, base_ebit=2404, base_da=1136,
            revenue_growth=[18, 15, 12, 12, 10, 8, 6, 5, 4, 3],
            terminal_growth=15.0, target_ebit_margin=14.0,
            margin_convergence_year=7, sales_to_capital=5.65,
            sales_to_capital_terminal=4.0, tax_rate=23.0,
            terminal_tax_rate=25.0, terminal_wacc=19.35,
            terminal_roc=19.35, total_debt=3385, cash=2854,
            shares=160, one_time_items=65, currency="TL",
        )
        wacc_vals = [34.0, 36.0, 38.38, 40.0, 42.0]
        tg_vals = [13.0, 14.0, 15.0, 16.0, 17.0]
        grid = sensitivity_grid(params, "wacc", wacc_vals, "terminal_growth", tg_vals)
        print(format_sensitivity_grid(grid, "WACC", wacc_vals, "Terminal g", tg_vals))


if __name__ == "__main__":
    main()
