#!/usr/bin/env python3
"""
Dual-Track Çapraz Kontrol Modülü
Reel TL DCF + USD DCF sapma analizi.

İki paralel DCF modeli çalıştırıp sonuçları karşılaştırır:
1. Reel TL DCF: TL cinsinden, enflasyon-düzeltilmiş
2. USD DCF: Dolar cinsinden

Sapma %5'ten büyükse uyarı verir. IAS 29 etkisi analiz edilir.
"""

import sys
from typing import Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class DCFInput:
    """Tek bir DCF modeli için girdi parametreleri."""
    currency: str  # "TL" or "USD"
    revenue: float  # Base revenue
    revenue_growth: float  # Annual growth rate
    operating_margin: float  # EBIT/Revenue
    tax_rate: float
    reinvestment_rate: float  # (CapEx + ΔWC) / NOPAT
    wacc: float
    terminal_growth: float
    projection_years: int = 5
    net_debt: float = 0.0
    shares_outstanding: float = 1.0
    fx_rate: float = 1.0  # TL/USD (for conversion)


def run_simple_dcf(inputs: DCFInput) -> Dict[str, float]:
    """
    Basit N-yıllık DCF modeli.
    
    Returns:
        {
            'firm_value': float,
            'equity_value': float,
            'per_share': float,
            'pv_fcff': float,
            'terminal_value': float,
            'pv_terminal': float,
        }
    """
    revenue = inputs.revenue
    pv_fcff = 0.0
    
    for yr in range(1, inputs.projection_years + 1):
        revenue *= (1 + inputs.revenue_growth)
        ebit = revenue * inputs.operating_margin
        nopat = ebit * (1 - inputs.tax_rate)
        fcff = nopat * (1 - inputs.reinvestment_rate)
        discount = (1 + inputs.wacc) ** yr
        pv_fcff += fcff / discount
    
    # Terminal value
    terminal_revenue = revenue * (1 + inputs.terminal_growth)
    terminal_fcff = terminal_revenue * inputs.operating_margin * (1 - inputs.tax_rate) * (1 - inputs.reinvestment_rate)
    
    if inputs.wacc <= inputs.terminal_growth:
        terminal_value = 0  # Invalid
    else:
        terminal_value = terminal_fcff / (inputs.wacc - inputs.terminal_growth)
    
    pv_terminal = terminal_value / ((1 + inputs.wacc) ** inputs.projection_years)
    firm_value = pv_fcff + pv_terminal
    equity_value = firm_value - inputs.net_debt
    per_share = equity_value / inputs.shares_outstanding if inputs.shares_outstanding > 0 else 0
    
    return {
        "currency": inputs.currency,
        "firm_value": round(firm_value, 2),
        "equity_value": round(equity_value, 2),
        "per_share": round(per_share, 2),
        "pv_fcff": round(pv_fcff, 2),
        "terminal_value": round(terminal_value, 2),
        "pv_terminal": round(pv_terminal, 2),
    }


def dual_track_analysis(
    tl_inputs: DCFInput,
    usd_inputs: DCFInput,
    fx_rate: float,
    threshold_pct: float = 5.0,
) -> Dict[str, Any]:
    """
    Dual-track çapraz kontrol analizi.
    
    Her iki modeli çalıştırır, USD cinsinden normalize eder ve sapma hesaplar.
    
    Args:
        tl_inputs: TL DCF girdileri
        usd_inputs: USD DCF girdileri
        fx_rate: Güncel TL/USD kuru
        threshold_pct: Sapma uyarı eşiği (%)
        
    Returns:
        {
            'tl_result': DCF result,
            'usd_result': DCF result,
            'comparison': {
                'tl_equity_usd': float,  # TL equity → USD'ye çevrilmiş
                'usd_equity_usd': float,
                'deviation_pct': float,
                'deviation_abs_usd': float,
                'warning': bool,
                'warning_msg': str,
            },
            'diagnostics': {...},
        }
    """
    tl_result = run_simple_dcf(tl_inputs)
    usd_result = run_simple_dcf(usd_inputs)
    
    # Convert TL equity to USD
    tl_equity_usd = tl_result["equity_value"] / fx_rate
    usd_equity_usd = usd_result["equity_value"]
    
    # Deviation
    if usd_equity_usd != 0:
        deviation_pct = ((tl_equity_usd - usd_equity_usd) / usd_equity_usd) * 100
    else:
        deviation_pct = float('inf') if tl_equity_usd != 0 else 0
    
    deviation_abs = abs(tl_equity_usd - usd_equity_usd)
    warning = abs(deviation_pct) > threshold_pct
    
    # Diagnostics
    wacc_diff = tl_inputs.wacc - usd_inputs.wacc
    growth_diff = tl_inputs.revenue_growth - usd_inputs.revenue_growth
    implied_inflation = wacc_diff - growth_diff if abs(wacc_diff) > 0 else 0
    
    warning_msg = ""
    if warning:
        warning_msg = f"⚠️ SAPMA YÜKSEK: {deviation_pct:+.1f}% (eşik: ±{threshold_pct}%)"
        if abs(deviation_pct) > 15:
            warning_msg += "\n   🔴 Kritik sapma — model tutarsızlığı kontrol edilmeli"
        elif abs(deviation_pct) > 10:
            warning_msg += "\n   🟡 Yüksek sapma — FX veya enflasyon varsayımlarını gözden geçir"
    
    comparison = {
        "tl_equity_usd": round(tl_equity_usd, 2),
        "usd_equity_usd": round(usd_equity_usd, 2),
        "deviation_pct": round(deviation_pct, 2),
        "deviation_abs_usd": round(deviation_abs, 2),
        "threshold_pct": threshold_pct,
        "warning": warning,
        "warning_msg": warning_msg,
    }
    
    diagnostics = {
        "fx_rate": fx_rate,
        "tl_wacc": tl_inputs.wacc,
        "usd_wacc": usd_inputs.wacc,
        "wacc_differential": round(wacc_diff, 4),
        "tl_growth": tl_inputs.revenue_growth,
        "usd_growth": usd_inputs.revenue_growth,
        "growth_differential": round(growth_diff, 4),
        "implied_inflation_diff": round(implied_inflation, 4),
        "tl_terminal_g": tl_inputs.terminal_growth,
        "usd_terminal_g": usd_inputs.terminal_growth,
    }
    
    return {
        "tl_result": tl_result,
        "usd_result": usd_result,
        "comparison": comparison,
        "diagnostics": diagnostics,
    }


def print_dual_track(result: Dict):
    """Dual-track sonuçlarını yazdır."""
    tl = result["tl_result"]
    usd = result["usd_result"]
    comp = result["comparison"]
    diag = result["diagnostics"]
    
    fmt = lambda x: f"{x:,.0f}"
    
    print(f"\n{'=' * 65}")
    print(f"  DUAL-TRACK ÇAPRAZ KONTROL ANALİZİ")
    print(f"{'=' * 65}")
    
    print(f"\n  {'Metrik':<30s} {'TL DCF':>15s} {'USD DCF':>15s}")
    print(f"  {'─' * 60}")
    print(f"  {'Firma Değeri':<30s} {fmt(tl['firm_value']):>15s} {fmt(usd['firm_value']):>15s}")
    print(f"  {'Özsermaye Değeri':<30s} {fmt(tl['equity_value']):>15s} {fmt(usd['equity_value']):>15s}")
    print(f"  {'Hisse Başı Değer':<30s} {tl['per_share']:>15,.2f} {usd['per_share']:>15,.2f}")
    
    print(f"\n  ── KARŞILAŞTİRMA (USD cinsinden) ──")
    print(f"  FX Kuru: {diag['fx_rate']:.2f} TL/USD")
    print(f"  TL Equity → USD: ${fmt(comp['tl_equity_usd'])}")
    print(f"  USD Equity      : ${fmt(comp['usd_equity_usd'])}")
    print(f"  Sapma           : {comp['deviation_pct']:+.1f}% (${fmt(comp['deviation_abs_usd'])})")
    
    if comp["warning_msg"]:
        print(f"\n  {comp['warning_msg']}")
    else:
        print(f"\n  ✅ Sapma kabul edilebilir seviyede (±{comp['threshold_pct']}% içinde)")
    
    print(f"\n  ── DİAGNOSTİK ──")
    print(f"  WACC farkı (TL-USD): {diag['wacc_differential']:.2%}")
    print(f"  Büyüme farkı: {diag['growth_differential']:.2%}")
    print()


if __name__ == "__main__":
    print("=== Dual-Track Çapraz Kontrol ===\n")
    
    # Örnek: THYAO benzeri şirket
    tl = DCFInput(
        currency="TL",
        revenue=300_000_000,  # 300B TL
        revenue_growth=0.25,  # Nominal TL growth (enflasyon dahil)
        operating_margin=0.14,
        tax_rate=0.25,
        reinvestment_rate=0.35,
        wacc=0.20,  # Yüksek — TL cinsinden
        terminal_growth=0.06,
        net_debt=50_000_000,
        shares_outstanding=1_380_000,
        fx_rate=34.0,
    )
    
    usd = DCFInput(
        currency="USD",
        revenue=300_000_000 / 34.0,  # USD'ye çevir
        revenue_growth=0.08,  # Reel USD growth
        operating_margin=0.14,
        tax_rate=0.25,
        reinvestment_rate=0.35,
        wacc=0.12,  # USD WACC
        terminal_growth=0.03,
        net_debt=50_000_000 / 34.0,
        shares_outstanding=1_380_000,
    )
    
    result = dual_track_analysis(tl, usd, fx_rate=34.0, threshold_pct=5.0)
    print_dual_track(result)
    
    print("✅ dual_track.py çalışıyor.")
