#!/usr/bin/env python3
"""
WACC Calculator - Damodaran Methodology
BBB DCF Toolkit v2.0

Damodaran'in Cost of Capital yaklasimini tam uygular:
- Rf duzeltmesi (10Y - Aa1 default spread)
- Beta levering/unlevering (cash-corrected)
- Cost of Equity (CAPM + CRP + lambda)
- Cost of Debt (gercek rating veya sentetik)
- CRP (rating + CDS dual yaklasim)
- Fisher donusumu (USD <-> TL)
- Time-varying WACC destegi

Kullanim:
    # Modul olarak
    from wacc_calculator import calculate_wacc, fisher_convert
    result = calculate_wacc(...)

    # CLI olarak
    python wacc_calculator.py --rf-raw 4.68 --beta-u 0.82 --erp 4.60 ...

Referanslar:
    - Damodaran "Investment Valuation" Ch.4-7
    - bbb-dcf/references/formula_card.md
    - bbb-dcf/references/country_erp.md
    - bbb-dcf/methodology/risk_discount.md
"""

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Tuple


# ============================================================
# SABITLER
# ============================================================

# Damodaran sigma_equity / sigma_bond carpani (CRP hesabi icin)
# Kaynak: Damodaran "Equity Risk Premiums" paper
SIGMA_EQUITY_BOND_RATIO = 1.5234

# Damodaran sentetik rating tablosu (Ocak 2025 guncellemesi)
# Kaynak: pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ratings.html
# Format: (icr_alt, icr_ust, rating, spread_bps) - buyuk firma (market cap > $5B)
SYNTHETIC_RATING_LARGE = [
    (12.50, 999.0, "AAA", 63),
    (8.50, 12.50, "AA", 78),
    (6.50, 8.50, "A+", 98),
    (5.50, 6.50, "A", 108),
    (4.25, 5.50, "A-", 122),
    (3.00, 4.25, "BBB", 156),
    (2.50, 3.00, "BB+", 200),
    (2.00, 2.50, "BB", 240),
    (1.50, 2.00, "B+", 351),
    (1.25, 1.50, "B", 421),
    (0.80, 1.25, "B-", 515),
    (0.50, 0.80, "CCC", 820),
    (0.20, 0.50, "CC", 1063),
    (-999, 0.20, "D", 2000),
]

# Kucuk firma (market cap < $5B)
SYNTHETIC_RATING_SMALL = [
    (12.50, 999.0, "AAA", 63),
    (9.50, 12.50, "AA", 78),
    (7.50, 9.50, "A+", 98),
    (6.00, 7.50, "A", 108),
    (4.50, 6.00, "A-", 122),
    (4.00, 4.50, "BBB", 156),
    (3.50, 4.00, "BB+", 200),
    (3.00, 3.50, "BB", 240),
    (2.50, 3.00, "B+", 351),
    (2.00, 2.50, "B", 421),
    (1.50, 2.00, "B-", 515),
    (1.00, 1.50, "CCC", 820),
    (0.50, 1.00, "CC", 1063),
    (0.20, 0.50, "C", 1400),
    (-999, 0.20, "D", 2000),
]

# Yaygin ulke kredi notlari -> default spread (bps)
# Kaynak: Damodaran country ERP tablosu (Ocak 2025)
SOVEREIGN_SPREADS = {
    "AAA": 0, "AA+": 43, "AA": 54, "AA-": 65,
    "A+": 78, "A": 98, "A-": 122,
    "BBB+": 143, "BBB": 170, "BBB-": 200,
    "BB+": 240, "BB": 288, "BB-": 350,
    "B+": 425, "B": 525, "B-": 625,
    "CCC+": 775, "CCC": 900, "CCC-": 1050,
    "CC": 1200, "C": 1500, "D": 2000,
}


# ============================================================
# VERI SINIFLARI
# ============================================================

@dataclass
class WACCResult:
    """WACC hesaplama sonucu - tum ara degerleri icerir."""

    # Risksiz oran
    rf_raw: float           # Ham 10Y getiri (%)
    rf_default_adj: float   # Aa1 default spread (%)
    rf: float               # Duzeltilmis Rf (%)

    # Beta
    beta_u: float           # Kaldiracsiz beta (cash-corrected)
    beta_l: float           # Kaldıracli beta
    debt_equity: float      # D/E orani

    # Cost of Equity
    erp_mature: float       # Olgun piyasa ERP (%)
    crp: float              # Ulke risk primi (%)
    lambda_factor: float    # Lambda (gelir dagitim faktoru)
    ke_usd: float           # Cost of Equity USD (%)

    # Cost of Debt
    kd_pretax_usd: float    # Vergi oncesi borc maliyeti USD (%)
    kd_source: str          # "actual_rating" veya "synthetic"
    synthetic_rating: Optional[str]  # Sentetik rating (varsa)
    synthetic_icr: Optional[float]   # ICR (varsa)
    tax_rate: float         # Efektif vergi orani
    kd_aftertax_usd: float  # Vergi sonrasi borc maliyeti USD (%)

    # Agirliklar
    equity_weight: float    # E/V
    debt_weight: float      # D/V

    # WACC
    wacc_usd: float         # WACC USD (%)

    # Fisher / TL
    inflation_domestic: Optional[float]  # Yurt ici beklenen enflasyon
    inflation_us: Optional[float]        # ABD beklenen enflasyon
    wacc_tl: Optional[float]             # WACC TL (Fisher)
    ke_tl: Optional[float]               # Ke TL (Fisher)
    kd_pretax_tl: Optional[float]        # Kd TL (Fisher)

    # CRP detay
    crp_rating_based: Optional[float]    # Rating bazli CRP
    crp_cds_based: Optional[float]       # CDS bazli CRP
    crp_blend_weights: Optional[List[float]]  # [rating_w, cds_w]

    # Terminal (opsiyonel)
    terminal_wacc_usd: Optional[float] = None
    terminal_wacc_tl: Optional[float] = None

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent=2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def summary(self) -> str:
        lines = [
            "=" * 55,
            "WACC HESAPLAMA SONUCU",
            "=" * 55,
            "",
            f"  Rf (duzeltilmis):     {self.rf:.2f}%",
            f"  Beta_U:               {self.beta_u:.2f}",
            f"  Beta_L:               {self.beta_l:.2f}",
            f"  ERP (mature):         {self.erp_mature:.2f}%",
            f"  CRP:                  {self.crp:.2f}%",
            f"  Lambda:               {self.lambda_factor:.2f}",
            f"  Ke (USD):             {self.ke_usd:.2f}%",
            "",
            f"  Kd pre-tax (USD):     {self.kd_pretax_usd:.2f}%",
            f"  Kd kaynak:            {self.kd_source}",
            f"  Vergi orani:          {self.tax_rate:.1f}%",
            f"  Kd after-tax (USD):   {self.kd_aftertax_usd:.2f}%",
            "",
            f"  E/V:                  {self.equity_weight:.1f}%",
            f"  D/V:                  {self.debt_weight:.1f}%",
            "",
            f"  WACC (USD):           {self.wacc_usd:.2f}%",
        ]
        if self.wacc_tl is not None:
            lines.extend([
                "",
                f"  Enflasyon (yurt ici): {self.inflation_domestic:.1f}%",
                f"  Enflasyon (ABD):      {self.inflation_us:.1f}%",
                f"  WACC (TL):            {self.wacc_tl:.2f}%",
                f"  Ke (TL):              {self.ke_tl:.2f}%",
                f"  Kd pre-tax (TL):      {self.kd_pretax_tl:.2f}%",
            ])
        if self.crp_rating_based is not None:
            lines.extend([
                "",
                f"  CRP (rating):         {self.crp_rating_based:.2f}%",
                f"  CRP (CDS):            {self.crp_cds_based:.2f}%" if self.crp_cds_based else "",
                f"  CRP (blended):        {self.crp:.2f}%",
            ])
        lines.append("=" * 55)
        return "\n".join(l for l in lines if l is not None)


# ============================================================
# TEMEL FONKSIYONLAR
# ============================================================

def adjust_rf(rf_10y_raw: float, aa1_spread: float = 0.23) -> float:
    """
    Risksiz orani duzelt.
    Damodaran: ABD Aa1'e dusuruldu, Rf = 10Y - default spread.

    Args:
        rf_10y_raw: ABD 10Y Treasury getirisi (%, orn: 4.68)
        aa1_spread: Aa1 default spread (%, orn: 0.23)

    Returns:
        Duzeltilmis Rf (%)
    """
    return rf_10y_raw - aa1_spread


def lever_beta(beta_u: float, debt_equity: float, tax_rate: float) -> float:
    """
    Kaldiracsiz beta'dan kaldıracli beta'ya.
    Formul: Beta_L = Beta_U x (1 + (1-t) x D/E)

    Args:
        beta_u: Kaldiracsiz beta (cash-corrected)
        debt_equity: D/E orani (orn: 0.33 = %33)
        tax_rate: Vergi orani (orn: 0.23 = %23)

    Returns:
        Kaldıracli beta
    """
    return beta_u * (1 + (1 - tax_rate) * debt_equity)


def unlever_beta(beta_l: float, debt_equity: float, tax_rate: float,
                 cash_ratio: float = 0.0) -> float:
    """
    Kaldıracli beta'dan kaldiracsiz beta'ya (cash-corrected).
    Formul: Beta_U = Beta_L / (1 + (1-t) x D/E) / (1 - cash/firm_value)

    Args:
        beta_l: Kaldıracli (gozlemlenen) beta
        debt_equity: D/E orani
        tax_rate: Vergi orani
        cash_ratio: Nakit / Firma Degeri orani (cash correction icin)

    Returns:
        Kaldiracsiz beta (cash-corrected)
    """
    unlevered = beta_l / (1 + (1 - tax_rate) * debt_equity)
    if cash_ratio > 0 and cash_ratio < 1:
        unlevered = unlevered / (1 - cash_ratio)
    return unlevered


def cost_of_equity(rf: float, beta_l: float, erp_mature: float,
                   crp: float = 0.0, lambda_factor: float = 1.0) -> float:
    """
    CAPM + CRP ile ozsermaye maliyeti hesapla.
    Formul: Ke = Rf + Beta_L x ERP_mature + lambda x CRP

    Args:
        rf: Duzeltilmis risksiz oran (%)
        beta_l: Kaldıracli beta
        erp_mature: Olgun piyasa risk primi (%)
        crp: Ulke risk primi (%)
        lambda_factor: Lambda faktoru (0-1, gelir dagilimi bazli)

    Returns:
        Cost of Equity (%)
    """
    return rf + beta_l * erp_mature + lambda_factor * crp


def cost_of_debt(rf: float, country_default_spread: float,
                 company_spread: float) -> float:
    """
    Borc maliyeti hesapla (vergi oncesi, USD bazli).
    Formul: Kd = Rf + Country_Default_Spread + Company_Spread

    Args:
        rf: Duzeltilmis risksiz oran (%)
        country_default_spread: Ulke temerrut spreadi (%)
        company_spread: Sirket spreadi (%)

    Returns:
        Pre-tax Kd (%)
    """
    return rf + country_default_spread + company_spread


def calculate_wacc_rate(ke: float, kd_aftertax: float,
                        equity_weight: float, debt_weight: float) -> float:
    """
    WACC hesapla.
    Formul: WACC = Ke x (E/V) + Kd_aftertax x (D/V)

    Args:
        ke: Cost of Equity (%)
        kd_aftertax: After-tax Cost of Debt (%)
        equity_weight: E/V (0-1)
        debt_weight: D/V (0-1)

    Returns:
        WACC (%)
    """
    return ke * equity_weight + kd_aftertax * debt_weight


# ============================================================
# CRP HESAPLAMA
# ============================================================

def crp_from_rating(sovereign_rating: str) -> Tuple[float, float]:
    """
    Ulke kredi notundan CRP hesapla.
    Formul: CRP = Default_Spread x (sigma_E / sigma_B)

    Args:
        sovereign_rating: S&P sovereign rating (orn: "BB+")

    Returns:
        (country_default_spread_pct, crp_pct) tuple
    """
    spread_bps = SOVEREIGN_SPREADS.get(sovereign_rating)
    if spread_bps is None:
        raise ValueError(f"Bilinmeyen rating: {sovereign_rating}. "
                         f"Gecerli: {list(SOVEREIGN_SPREADS.keys())}")
    default_spread = spread_bps / 100  # bps -> %
    crp = default_spread * SIGMA_EQUITY_BOND_RATIO
    return default_spread, crp


def crp_from_cds(cds_spread_bps: float) -> float:
    """
    CDS spread'inden CRP hesapla.
    Formul: CRP = CDS_Spread x (sigma_E / sigma_B)

    Args:
        cds_spread_bps: 5Y CDS spread (basis points, orn: 280)

    Returns:
        CRP (%)
    """
    cds_pct = cds_spread_bps / 100
    return cds_pct * SIGMA_EQUITY_BOND_RATIO


def crp_blended(crp_rating: float, crp_cds: float,
                weights: Tuple[float, float] = (0.4, 0.6)) -> float:
    """
    Rating ve CDS bazli CRP'leri agirlikli ortalama ile birlestir.
    Varsayilan: %60 CDS + %40 Rating (piyasa agirlikli ama rating tabanli).

    Args:
        crp_rating: Rating bazli CRP (%)
        crp_cds: CDS bazli CRP (%)
        weights: (rating_weight, cds_weight) - toplami 1.0

    Returns:
        Blended CRP (%)
    """
    return crp_rating * weights[0] + crp_cds * weights[1]


# ============================================================
# SENTETIK RATING
# ============================================================

def synthetic_rating(icr: float, is_large: bool = False) -> Tuple[str, float]:
    """
    ICR'dan sentetik kredi notu ve spread hesapla.

    UYARI: Sadece CROSS-CHECK icin kullan! Gercek kredi notunu baz al.
    ICR'da kur farki dahil etme, sadece gercek faiz gideri.

    Args:
        icr: Interest Coverage Ratio (EBIT / Faiz Gideri)
        is_large: Market cap > $5B mi?

    Returns:
        (rating, spread_pct) tuple
    """
    table = SYNTHETIC_RATING_LARGE if is_large else SYNTHETIC_RATING_SMALL
    for low, high, rating, spread_bps in table:
        if low <= icr < high:
            return rating, spread_bps / 100
    # Fallback
    return "D", 20.00


# ============================================================
# FISHER DONUSUMU
# ============================================================

def fisher_convert(rate_base: float, inflation_from: float,
                   inflation_to: float) -> float:
    """
    Fisher denklemi ile faiz oranini para birimleri arasinda donustur.
    Formul: (1 + r_to) = (1 + r_from) x (1 + pi_to) / (1 + pi_from)

    Args:
        rate_base: Kaynak para birimi orani (%, orn: WACC_USD = 10.5)
        inflation_from: Kaynak enflasyon (%, orn: ABD = 2.5)
        inflation_to: Hedef enflasyon (%, orn: TR = 25.0)

    Returns:
        Hedef para birimi orani (%)
    """
    r = rate_base / 100
    pi_from = inflation_from / 100
    pi_to = inflation_to / 100
    r_converted = (1 + r) * (1 + pi_to) / (1 + pi_from) - 1
    return r_converted * 100


def fisher_crosscheck(value_tl: float, value_usd: float,
                      spot_rate: float) -> dict:
    """
    Fisher cross-check: TL deger / kur ≈ USD deger.

    Args:
        value_tl: TL hedef fiyat
        value_usd: USD hedef fiyat
        spot_rate: USDTRY spot kur

    Returns:
        dict with sapma ve degerlendirme
    """
    tl_implied_usd = value_tl / spot_rate
    avg = (tl_implied_usd + value_usd) / 2
    sapma = abs(tl_implied_usd - value_usd) / avg * 100 if avg > 0 else 0

    if sapma < 10:
        verdict = "TUTARLI"
        flag = "OK"
    elif sapma < 15:
        verdict = "UYARI - parametreleri kontrol et"
        flag = "WARN"
    else:
        verdict = "HATA - parametreleri gozden gecir"
        flag = "FAIL"

    return {
        "tl_value": value_tl,
        "usd_value": value_usd,
        "spot_rate": spot_rate,
        "tl_implied_usd": round(tl_implied_usd, 4),
        "sapma_pct": round(sapma, 2),
        "verdict": verdict,
        "flag": flag,
    }


# ============================================================
# TIME-VARYING WACC
# ============================================================

def interpolate_wacc(wacc_y1: float, wacc_terminal: float,
                     years: int = 10, transition_start: int = 5) -> List[float]:
    """
    Time-varying WACC dizisi olustur.
    Y1-transition_start: wacc_y1 sabit
    transition_start+1 - years: lineer interpolasyon -> wacc_terminal

    Args:
        wacc_y1: Baslangic WACC (%)
        wacc_terminal: Terminal WACC (%)
        years: Toplam yil (default 10)
        transition_start: Gecis baslangic yili (default 5)

    Returns:
        [wacc_y1, wacc_y2, ..., wacc_y10] listesi (%)
    """
    result = []
    transition_years = years - transition_start
    for y in range(1, years + 1):
        if y <= transition_start:
            result.append(wacc_y1)
        else:
            progress = (y - transition_start) / transition_years
            wacc = wacc_y1 + (wacc_terminal - wacc_y1) * progress
            result.append(round(wacc, 4))
    return result


# ============================================================
# TERMINAL WACC
# ============================================================

def terminal_wacc(rf: float, erp_mature: float,
                  crp_factor: float = 0.5, crp: float = 0.0) -> float:
    """
    Terminal WACC hesapla.
    Damodaran default: Rf + Mature_ERP (CRP sifirlanir).
    Turkiye override: Rf + Mature_ERP + alpha x CRP

    Args:
        rf: Risksiz oran (%)
        erp_mature: Olgun piyasa ERP (%)
        crp_factor: CRP'nin ne kadari terminal'de kalacak (0-1, default 0.5)
        crp: Mevcut CRP (%)

    Returns:
        Terminal WACC (%)

    Not:
        crp_factor=0 -> Damodaran default (tam gelismis piyasa)
        crp_factor=0.5 -> Turkiye 10 yilda yarisina iner (onerilen)
        crp_factor=1.0 -> CRP hic azalmaz
    """
    return rf + erp_mature + crp_factor * crp


# ============================================================
# ANA HESAPLAMA FONKSIYONU
# ============================================================

def calculate_wacc(
    # Risksiz oran
    rf_10y_raw: float,
    aa1_spread: float = 0.23,

    # Beta
    beta_u: float = 1.0,

    # ERP & CRP
    erp_mature: float = 4.60,
    crp: Optional[float] = None,
    sovereign_rating: Optional[str] = None,
    cds_spread_bps: Optional[float] = None,
    crp_blend_weights: Tuple[float, float] = (0.4, 0.6),
    lambda_factor: float = 1.0,

    # Borc maliyeti
    kd_pretax_usd: Optional[float] = None,
    company_icr: Optional[float] = None,
    is_large_cap: bool = False,
    company_rating: Optional[str] = None,

    # Vergi & Sermaye yapisi
    tax_rate: float = 25.0,
    market_cap: Optional[float] = None,
    total_debt: Optional[float] = None,
    cash: Optional[float] = None,
    debt_to_equity: Optional[float] = None,

    # Fisher
    inflation_domestic: Optional[float] = None,
    inflation_us: float = 2.5,

    # Terminal
    crp_terminal_factor: float = 0.5,
) -> WACCResult:
    """
    Tam WACC hesaplama pipeline'i.

    Oncelik sirasi:
    - CRP: crp (direkt) > sovereign_rating + cds (blended) > sovereign_rating > cds
    - Kd: kd_pretax_usd (direkt) > company_rating > company_icr (sentetik)
    - D/E: debt_to_equity (direkt) > market_cap + total_debt hesaplama

    Args:
        rf_10y_raw: ABD 10Y Treasury getirisi (%, orn: 4.68)
        aa1_spread: Aa1 default spread (%, default 0.23)
        beta_u: Kaldiracsiz beta (cash-corrected)
        erp_mature: Olgun piyasa ERP (%)
        crp: Direkt CRP girisi (%, override)
        sovereign_rating: Ulke kredi notu (S&P, orn: "BB+")
        cds_spread_bps: 5Y CDS spread (bps)
        crp_blend_weights: (rating_w, cds_w)
        lambda_factor: Lambda (gelir dagilim faktoru, 0-1)
        kd_pretax_usd: Vergi oncesi borc maliyeti USD (%, direkt)
        company_icr: Sirket ICR (sentetik rating icin)
        is_large_cap: Market cap > $5B mi?
        company_rating: Sirketin gercek kredi notu (S&P)
        tax_rate: Efektif vergi orani (%)
        market_cap: Piyasa degeri (M, herhangi para birimi)
        total_debt: Toplam borc (M)
        cash: Nakit (M)
        debt_to_equity: D/E orani (direkt)
        inflation_domestic: Yurt ici beklenen enflasyon (%)
        inflation_us: ABD beklenen enflasyon (%)
        crp_terminal_factor: Terminal CRP faktoru (0-1)

    Returns:
        WACCResult dataclass
    """

    # 1. Rf duzeltmesi
    rf = adjust_rf(rf_10y_raw, aa1_spread)

    # 2. CRP hesabi
    crp_rating_val = None
    crp_cds_val = None
    country_default_spread = 0.0

    if crp is not None:
        # Direkt CRP verilmis
        crp_final = crp
    else:
        if sovereign_rating:
            country_default_spread, crp_rating_val = crp_from_rating(sovereign_rating)
        if cds_spread_bps:
            crp_cds_val = crp_from_cds(cds_spread_bps)

        if crp_rating_val is not None and crp_cds_val is not None:
            crp_final = crp_blended(crp_rating_val, crp_cds_val, crp_blend_weights)
        elif crp_rating_val is not None:
            crp_final = crp_rating_val
        elif crp_cds_val is not None:
            crp_final = crp_cds_val
        else:
            crp_final = 0.0

    # 3. D/E orani
    if debt_to_equity is not None:
        de_ratio = debt_to_equity
    elif market_cap and total_debt:
        net_debt = total_debt - (cash or 0)
        ev = market_cap + max(0, net_debt)
        equity_w = market_cap / ev if ev > 0 else 1.0
        debt_w = 1.0 - equity_w
        de_ratio = (total_debt / market_cap) if market_cap > 0 else 0.0
    else:
        de_ratio = 0.0

    # 4. Beta levering
    beta_l = lever_beta(beta_u, de_ratio, tax_rate / 100)

    # 5. Cost of Equity (USD)
    ke_usd = cost_of_equity(rf, beta_l, erp_mature, crp_final, lambda_factor)

    # 6. Cost of Debt (USD)
    syn_rating = None
    syn_icr = None
    kd_source = "unknown"

    if kd_pretax_usd is not None:
        kd_usd = kd_pretax_usd
        kd_source = "direct_input"
    elif company_rating:
        # Gercek rating -> spread
        company_spread_bps = SOVEREIGN_SPREADS.get(company_rating, 200)
        kd_usd = rf + country_default_spread + company_spread_bps / 100
        kd_source = f"actual_rating_{company_rating}"
    elif company_icr is not None:
        # Sentetik rating
        syn_rating, syn_spread = synthetic_rating(company_icr, is_large_cap)
        syn_icr = company_icr
        kd_usd = rf + country_default_spread + syn_spread
        kd_source = f"synthetic_{syn_rating}"
    else:
        # Fallback: BBB spread
        kd_usd = rf + country_default_spread + 1.56
        kd_source = "fallback_BBB"

    kd_aftertax_usd = kd_usd * (1 - tax_rate / 100)

    # 7. Agirliklar
    if market_cap and total_debt:
        net_d = total_debt - (cash or 0)
        ev = market_cap + max(0, net_d)
        eq_w = market_cap / ev * 100 if ev > 0 else 100.0
        dt_w = 100.0 - eq_w
    elif debt_to_equity is not None:
        dt_w = de_ratio / (1 + de_ratio) * 100
        eq_w = 100.0 - dt_w
    else:
        eq_w = 100.0
        dt_w = 0.0

    # 8. WACC (USD)
    wacc_usd = calculate_wacc_rate(ke_usd, kd_aftertax_usd, eq_w / 100, dt_w / 100)

    # 9. Fisher donusumu (TL)
    wacc_tl_val = None
    ke_tl_val = None
    kd_tl_val = None
    if inflation_domestic is not None:
        wacc_tl_val = fisher_convert(wacc_usd, inflation_us, inflation_domestic)
        ke_tl_val = fisher_convert(ke_usd, inflation_us, inflation_domestic)
        kd_tl_val = fisher_convert(kd_usd, inflation_us, inflation_domestic)

    # 10. Terminal WACC
    term_wacc_usd = terminal_wacc(rf, erp_mature, crp_terminal_factor, crp_final)
    term_wacc_tl = None
    if inflation_domestic is not None:
        # Terminal icin daha dusuk enflasyon varsayimi (yaklasim)
        term_inflation = max(inflation_domestic * 0.4, 5.0)  # En az %5
        term_wacc_tl = fisher_convert(term_wacc_usd, inflation_us, term_inflation)

    return WACCResult(
        rf_raw=rf_10y_raw,
        rf_default_adj=aa1_spread,
        rf=round(rf, 4),
        beta_u=beta_u,
        beta_l=round(beta_l, 4),
        debt_equity=round(de_ratio, 4),
        erp_mature=erp_mature,
        crp=round(crp_final, 4),
        lambda_factor=lambda_factor,
        ke_usd=round(ke_usd, 4),
        kd_pretax_usd=round(kd_usd, 4),
        kd_source=kd_source,
        synthetic_rating=syn_rating,
        synthetic_icr=syn_icr,
        tax_rate=tax_rate,
        kd_aftertax_usd=round(kd_aftertax_usd, 4),
        equity_weight=round(eq_w, 2),
        debt_weight=round(dt_w, 2),
        wacc_usd=round(wacc_usd, 4),
        inflation_domestic=inflation_domestic,
        inflation_us=inflation_us,
        wacc_tl=round(wacc_tl_val, 4) if wacc_tl_val else None,
        ke_tl=round(ke_tl_val, 4) if ke_tl_val else None,
        kd_pretax_tl=round(kd_tl_val, 4) if kd_tl_val else None,
        crp_rating_based=round(crp_rating_val, 4) if crp_rating_val else None,
        crp_cds_based=round(crp_cds_val, 4) if crp_cds_val else None,
        crp_blend_weights=list(crp_blend_weights) if (crp_rating_val or crp_cds_val) else None,
        terminal_wacc_usd=round(term_wacc_usd, 4),
        terminal_wacc_tl=round(term_wacc_tl, 4) if term_wacc_tl else None,
    )


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="WACC Calculator - Damodaran Methodology (BBB DCF v2.0)")

    # Rf
    parser.add_argument("--rf-raw", type=float, required=True,
                        help="ABD 10Y Treasury getirisi (%%)")
    parser.add_argument("--aa1-spread", type=float, default=0.23,
                        help="Aa1 default spread (%%, default: 0.23)")

    # Beta
    parser.add_argument("--beta-u", type=float, required=True,
                        help="Kaldiracsiz beta (cash-corrected)")

    # ERP & CRP
    parser.add_argument("--erp", type=float, default=4.60,
                        help="Olgun piyasa ERP (%%, default: 4.60)")
    parser.add_argument("--crp", type=float,
                        help="Direkt CRP girisi (%%)")
    parser.add_argument("--sovereign-rating", type=str,
                        help="Ulke kredi notu (S&P, orn: BB+)")
    parser.add_argument("--cds-bps", type=float,
                        help="5Y CDS spread (bps)")
    parser.add_argument("--lambda", type=float, default=1.0, dest="lambda_f",
                        help="Lambda faktoru (default: 1.0)")

    # Kd
    parser.add_argument("--kd", type=float,
                        help="Pre-tax Kd USD (%%)")
    parser.add_argument("--icr", type=float,
                        help="Sirket ICR (sentetik rating)")
    parser.add_argument("--company-rating", type=str,
                        help="Sirket gercek kredi notu")

    # Sermaye yapisi
    parser.add_argument("--tax", type=float, default=25.0,
                        help="Efektif vergi orani (%%, default: 25)")
    parser.add_argument("--market-cap", type=float,
                        help="Piyasa degeri (M)")
    parser.add_argument("--debt", type=float,
                        help="Toplam borc (M)")
    parser.add_argument("--cash", type=float,
                        help="Nakit (M)")
    parser.add_argument("--de-ratio", type=float,
                        help="D/E orani (direkt)")

    # Fisher
    parser.add_argument("--inflation", type=float,
                        help="Yurt ici beklenen enflasyon (%%)")
    parser.add_argument("--inflation-us", type=float, default=2.5,
                        help="ABD beklenen enflasyon (%%, default: 2.5)")

    # Cikti
    parser.add_argument("--json", action="store_true",
                        help="JSON cikti")

    args = parser.parse_args()

    result = calculate_wacc(
        rf_10y_raw=args.rf_raw,
        aa1_spread=args.aa1_spread,
        beta_u=args.beta_u,
        erp_mature=args.erp,
        crp=args.crp,
        sovereign_rating=args.sovereign_rating,
        cds_spread_bps=args.cds_bps,
        lambda_factor=args.lambda_f,
        kd_pretax_usd=args.kd,
        company_icr=args.icr,
        company_rating=args.company_rating,
        tax_rate=args.tax,
        market_cap=args.market_cap,
        total_debt=args.debt,
        cash=args.cash,
        debt_to_equity=args.de_ratio,
        inflation_domestic=args.inflation,
        inflation_us=args.inflation_us,
    )

    if args.json:
        print(result.to_json())
    else:
        print(result.summary())


if __name__ == "__main__":
    main()
