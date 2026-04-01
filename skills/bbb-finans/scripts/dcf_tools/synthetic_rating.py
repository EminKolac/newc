#!/usr/bin/env python3
"""
Sentetik Rating & Spread Tablosu (2024 Güncel)
Damodaran'ın ICR (Interest Coverage Ratio) → Sentetik Rating → Default Spread mapping'i.
Büyük firma (>$5B market cap) ve küçük firma (<$5B) ayrımı ile.

Kullanım: DCF modelinde borç maliyeti (cost of debt) hesaplaması için.
"""

from typing import Optional, Dict, Tuple

# ICR → (Rating, Default Spread bps) for LARGE firms (>$5B market cap)
# Source: Damodaran (January 2024 update)
LARGE_FIRM_TABLE: list[Tuple[float, float, str, float]] = [
    # (ICR_low, ICR_high, Rating, Spread_bps)
    # Synced with Damodaran Excel "Synthetic rating" sheet (Jan 2024)
    (-1e9, 0.20, "D/D", 2000),
    (0.20, 0.65, "C/C", 1700),
    (0.65, 0.80, "CC/CC", 1178),
    (0.80, 1.25, "CCC/Caa", 851),
    (1.25, 1.50, "B-/B3", 648),
    (1.50, 1.75, "B/B2", 497),
    (1.75, 2.00, "B+/B1", 396),
    (2.00, 2.25, "BB-/Ba3", 335),
    (2.25, 2.50, "BB/Ba2", 268),
    (2.50, 3.00, "BB+/Ba1", 213),
    (3.00, 4.25, "BBB-/Baa3", 174),
    (4.25, 5.50, "BBB/Baa2", 136),
    (5.50, 6.00, "BBB+/Baa1", 121),
    (6.00, 6.50, "A-/A3", 108),
    (6.50, 7.50, "A/A2", 98),
    (7.50, 8.50, "A+/A1", 83),
    (8.50, 1e9, "AAA/Aaa", 59),
]

# ICR → (Rating, Default Spread bps) for SMALL firms (<$5B market cap)
SMALL_FIRM_TABLE: list[Tuple[float, float, str, float]] = [
    # Synced with Damodaran Excel "Synthetic rating" sheet (Jan 2024)
    (-1e9, 0.50, "D/D", 2000),
    (0.50, 0.80, "C/C", 1700),
    (0.80, 1.25, "CC/CC", 1178),
    (1.25, 1.50, "CCC/Caa", 851),
    (1.50, 2.00, "B-/B3", 648),
    (2.00, 2.50, "B/B2", 497),
    (2.50, 3.00, "B+/B1", 396),
    (3.00, 3.50, "BB-/Ba3", 335),
    (3.50, 4.00, "BB/Ba2", 268),
    (4.00, 4.50, "BB+/Ba1", 213),
    (4.50, 5.50, "BBB-/Baa3", 174),
    (5.50, 6.00, "BBB/Baa2", 136),
    (6.00, 6.50, "BBB+/Baa1", 121),
    (6.50, 7.00, "A-/A3", 108),
    (7.00, 7.50, "A/A2", 98),
    (7.50, 10.00, "A+/A1", 83),
    (10.00, 13.00, "AA/Aa2", 67),
    (13.00, 1e9, "AAA/Aaa", 59),
]


def get_synthetic_rating(
    icr: float,
    market_cap_usd_b: float = 1.0,
    large_threshold_b: float = 5.0,
) -> Dict[str, any]:
    """
    ICR'den sentetik rating ve default spread hesaplar.
    
    Args:
        icr: Interest Coverage Ratio (EBIT / Interest Expense)
        market_cap_usd_b: Market cap in USD billions
        large_threshold_b: Büyük/küçük firma eşiği (default $5B)
        
    Returns:
        {
            'rating': str,
            'spread_bps': float,
            'spread_pct': float,
            'firm_size': 'large' | 'small',
            'icr': float,
        }
    """
    is_large = market_cap_usd_b >= large_threshold_b
    table = LARGE_FIRM_TABLE if is_large else SMALL_FIRM_TABLE
    
    for low, high, rating, spread_bps in table:
        if low <= icr < high:
            return {
                "rating": rating,
                "spread_bps": spread_bps,
                "spread_pct": round(spread_bps / 100, 4),
                "firm_size": "large" if is_large else "small",
                "icr": icr,
            }
    
    # Fallback: en düşük rating
    return {
        "rating": "D/D",
        "spread_bps": 2000,
        "spread_pct": 20.00,
        "firm_size": "large" if is_large else "small",
        "icr": icr,
    }


def cost_of_debt(
    icr: float,
    risk_free_rate: float,
    country_default_spread: float = 0.0,
    market_cap_usd_b: float = 1.0,
    tax_rate: float = 0.25,
) -> Dict[str, float]:
    """
    Borç maliyeti hesaplar.
    
    Pre-tax Kd = Risk-free + Country Spread + Company Spread
    After-tax Kd = Pre-tax Kd × (1 - tax_rate)
    
    Args:
        icr: Interest Coverage Ratio
        risk_free_rate: Risksiz faiz oranı (decimal, e.g. 0.045)
        country_default_spread: Ülke risk primi (decimal)
        market_cap_usd_b: Market cap USD billions
        tax_rate: Vergi oranı
        
    Returns:
        Dict with pre_tax_kd, after_tax_kd, rating details
    """
    rating_info = get_synthetic_rating(icr, market_cap_usd_b)
    company_spread = rating_info["spread_pct"] / 100  # bps → decimal
    
    pre_tax_kd = risk_free_rate + country_default_spread + company_spread
    after_tax_kd = pre_tax_kd * (1 - tax_rate)
    
    return {
        **rating_info,
        "risk_free_rate": risk_free_rate,
        "country_spread": country_default_spread,
        "company_spread": company_spread,
        "pre_tax_kd": round(pre_tax_kd, 6),
        "after_tax_kd": round(after_tax_kd, 6),
        "tax_rate": tax_rate,
    }


if __name__ == "__main__":
    print("=== Sentetik Rating & Spread Tablosu ===\n")
    
    # Test: various ICR levels
    test_cases = [
        (0.5, 1.0, "Küçük, düşük ICR"),
        (3.0, 0.5, "Küçük, orta ICR"),
        (5.0, 2.0, "Küçük, iyi ICR"),
        (8.0, 10.0, "Büyük, yüksek ICR"),
        (15.0, 20.0, "Büyük, çok yüksek ICR"),
    ]
    
    for icr, mcap, desc in test_cases:
        r = get_synthetic_rating(icr, mcap)
        print(f"  {desc:30s} ICR={icr:5.1f} → {r['rating']:12s} Spread={r['spread_bps']:6.0f}bps ({r['firm_size']})")
    
    print("\n--- Borç Maliyeti Testi ---")
    result = cost_of_debt(
        icr=4.0,
        risk_free_rate=0.045,
        country_default_spread=0.028,
        market_cap_usd_b=2.0,
        tax_rate=0.25,
    )
    print(f"  Rating: {result['rating']}")
    print(f"  Pre-tax Kd: {result['pre_tax_kd']:.4%}")
    print(f"  After-tax Kd: {result['after_tax_kd']:.4%}")
    
    print("\n✅ synthetic_rating.py çalışıyor.")
