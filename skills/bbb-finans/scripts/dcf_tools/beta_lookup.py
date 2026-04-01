#!/usr/bin/env python3
"""
Industry Beta Lookup
Damodaran 94 sektör × unlevered beta (Global + Emerging Markets).
Static JSON + fuzzy matching + multi-business beta hesaplama.

Source: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html
Data: January 2024 update
"""

from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher

# ─── Damodaran Industry Betas (Jan 2024) ─────────────────────────────────
# Format: industry_name → {global_unlevered_beta, emerging_unlevered_beta, n_firms_global}
# Source: Damodaran "Levered and Unlevered Betas by Industry" (Global + Emerging)
INDUSTRY_BETAS: Dict[str, Dict[str, float]] = {
    "Advertising": {"global": 0.79, "emerging": 0.68, "n": 44},
    "Aerospace/Defense": {"global": 0.95, "emerging": 0.85, "n": 77},
    "Air Transport": {"global": 0.82, "emerging": 0.75, "n": 17},
    "Apparel": {"global": 0.73, "emerging": 0.65, "n": 39},
    "Auto & Truck": {"global": 0.62, "emerging": 0.55, "n": 24},
    "Auto Parts": {"global": 0.87, "emerging": 0.80, "n": 52},
    "Bank (Money Center)": {"global": 0.53, "emerging": 0.48, "n": 9},
    "Banks (Regional)": {"global": 0.41, "emerging": 0.38, "n": 557},
    "Beverage (Alcoholic)": {"global": 0.58, "emerging": 0.52, "n": 22},
    "Beverage (Soft)": {"global": 0.57, "emerging": 0.50, "n": 33},
    "Broadcasting": {"global": 0.73, "emerging": 0.68, "n": 22},
    "Brokerage & Investment Banking": {"global": 0.56, "emerging": 0.50, "n": 33},
    "Building Materials": {"global": 0.78, "emerging": 0.72, "n": 39},
    "Business & Consumer Services": {"global": 0.72, "emerging": 0.65, "n": 159},
    "Cable TV": {"global": 0.75, "emerging": 0.68, "n": 12},
    "Chemical (Basic)": {"global": 0.74, "emerging": 0.68, "n": 38},
    "Chemical (Diversified)": {"global": 0.78, "emerging": 0.72, "n": 5},
    "Chemical (Specialty)": {"global": 0.81, "emerging": 0.74, "n": 89},
    "Coal & Related Energy": {"global": 0.60, "emerging": 0.55, "n": 20},
    "Computer Services": {"global": 0.85, "emerging": 0.78, "n": 99},
    "Computers/Peripherals": {"global": 1.02, "emerging": 0.95, "n": 48},
    "Construction Supplies": {"global": 0.75, "emerging": 0.68, "n": 44},
    "Diversified": {"global": 0.58, "emerging": 0.52, "n": 20},
    "Drugs (Biotechnology)": {"global": 1.15, "emerging": 1.05, "n": 589},
    "Drugs (Pharmaceutical)": {"global": 0.95, "emerging": 0.88, "n": 254},
    "Education": {"global": 0.80, "emerging": 0.72, "n": 32},
    "Electrical Equipment": {"global": 0.92, "emerging": 0.85, "n": 107},
    "Electronics (Consumer & Office)": {"global": 0.89, "emerging": 0.82, "n": 19},
    "Electronics (General)": {"global": 0.85, "emerging": 0.78, "n": 148},
    "Engineering/Construction": {"global": 0.77, "emerging": 0.70, "n": 43},
    "Entertainment": {"global": 0.87, "emerging": 0.80, "n": 95},
    "Environmental & Waste Services": {"global": 0.68, "emerging": 0.62, "n": 60},
    "Farming/Agriculture": {"global": 0.62, "emerging": 0.56, "n": 31},
    "Financial Svcs. (Non-bank & Insurance)": {"global": 0.18, "emerging": 0.15, "n": 223},
    "Food Processing": {"global": 0.56, "emerging": 0.50, "n": 87},
    "Food Wholesalers": {"global": 0.49, "emerging": 0.44, "n": 14},
    "Furn/Home Furnishings": {"global": 0.72, "emerging": 0.65, "n": 28},
    "Green & Renewable Energy": {"global": 0.70, "emerging": 0.64, "n": 22},
    "Healthcare Products": {"global": 0.88, "emerging": 0.80, "n": 241},
    "Healthcare Support Services": {"global": 0.78, "emerging": 0.72, "n": 103},
    "Heathcare Information and Technology": {"global": 0.88, "emerging": 0.80, "n": 116},
    "Homebuilding": {"global": 0.82, "emerging": 0.75, "n": 30},
    "Hospitals/Healthcare Facilities": {"global": 0.60, "emerging": 0.54, "n": 30},
    "Hotel/Gaming": {"global": 0.72, "emerging": 0.66, "n": 58},
    "Household Products": {"global": 0.67, "emerging": 0.60, "n": 120},
    "Information Services": {"global": 0.86, "emerging": 0.78, "n": 57},
    "Insurance (General)": {"global": 0.52, "emerging": 0.47, "n": 19},
    "Insurance (Life)": {"global": 0.61, "emerging": 0.55, "n": 24},
    "Insurance (Prop/Cas.)": {"global": 0.48, "emerging": 0.43, "n": 48},
    "Investments & Asset Management": {"global": 0.65, "emerging": 0.58, "n": 164},
    "Machinery": {"global": 0.84, "emerging": 0.77, "n": 114},
    "Metals & Mining": {"global": 0.82, "emerging": 0.76, "n": 78},
    "Office Equipment & Services": {"global": 0.76, "emerging": 0.69, "n": 18},
    "Oil/Gas (Integrated)": {"global": 0.74, "emerging": 0.68, "n": 5},
    "Oil/Gas (Production and Exploration)": {"global": 0.87, "emerging": 0.80, "n": 185},
    "Oil/Gas Distribution": {"global": 0.57, "emerging": 0.52, "n": 16},
    "Oilfield Svcs/Equip.": {"global": 0.89, "emerging": 0.82, "n": 101},
    "Packaging & Container": {"global": 0.60, "emerging": 0.55, "n": 22},
    "Paper/Forest Products": {"global": 0.62, "emerging": 0.57, "n": 7},
    "Power": {"global": 0.43, "emerging": 0.39, "n": 56},
    "Precious Metals": {"global": 0.79, "emerging": 0.72, "n": 73},
    "Publishing & Newspapers": {"global": 0.62, "emerging": 0.56, "n": 22},
    "R.E.I.T.": {"global": 0.54, "emerging": 0.48, "n": 221},
    "Real Estate (Development)": {"global": 0.58, "emerging": 0.52, "n": 18},
    "Real Estate (General/Diversified)": {"global": 0.52, "emerging": 0.47, "n": 11},
    "Real Estate (Operations & Services)": {"global": 0.63, "emerging": 0.57, "n": 47},
    "Recreation": {"global": 0.68, "emerging": 0.62, "n": 55},
    "Reinsurance": {"global": 0.42, "emerging": 0.38, "n": 2},
    "Restaurant/Dining": {"global": 0.63, "emerging": 0.57, "n": 69},
    "Retail (Automotive)": {"global": 0.65, "emerging": 0.59, "n": 22},
    "Retail (Building Supply)": {"global": 0.80, "emerging": 0.73, "n": 5},
    "Retail (Distributors)": {"global": 0.73, "emerging": 0.66, "n": 68},
    "Retail (General)": {"global": 0.68, "emerging": 0.62, "n": 15},
    "Retail (Grocery and Food)": {"global": 0.46, "emerging": 0.42, "n": 13},
    "Retail (Online)": {"global": 0.98, "emerging": 0.90, "n": 54},
    "Retail (Special Lines)": {"global": 0.72, "emerging": 0.66, "n": 80},
    "Rubber& Tires": {"global": 0.67, "emerging": 0.61, "n": 3},
    "Semiconductor": {"global": 1.18, "emerging": 1.08, "n": 69},
    "Semiconductor Equip": {"global": 1.22, "emerging": 1.12, "n": 30},
    "Shipbuilding & Marine": {"global": 0.65, "emerging": 0.59, "n": 7},
    "Shoe": {"global": 0.74, "emerging": 0.67, "n": 10},
    "Software (Entertainment)": {"global": 1.08, "emerging": 0.98, "n": 85},
    "Software (Internet)": {"global": 1.01, "emerging": 0.92, "n": 29},
    "Software (System & Application)": {"global": 1.05, "emerging": 0.96, "n": 362},
    "Steel": {"global": 0.82, "emerging": 0.75, "n": 33},
    "Telecom (Wireless)": {"global": 0.53, "emerging": 0.48, "n": 15},
    "Telecom. Equipment": {"global": 0.90, "emerging": 0.82, "n": 80},
    "Telecom. Services": {"global": 0.51, "emerging": 0.46, "n": 49},
    "Tobacco": {"global": 0.48, "emerging": 0.43, "n": 14},
    "Transportation": {"global": 0.67, "emerging": 0.61, "n": 17},
    "Transportation (Railroads)": {"global": 0.63, "emerging": 0.57, "n": 6},
    "Trucking": {"global": 0.73, "emerging": 0.66, "n": 34},
    "Utility (General)": {"global": 0.35, "emerging": 0.32, "n": 15},
    "Utility (Water)": {"global": 0.38, "emerging": 0.34, "n": 15},
    "Total Market": {"global": 0.75, "emerging": 0.68, "n": 6130},
}

# ─── Türkiye sektör alias'ları ────────────────────────────────────────────
TURKISH_ALIASES: Dict[str, str] = {
    "Çimento": "Building Materials",
    "Cam": "Building Materials",
    "Demir Çelik": "Steel",
    "Otomotiv": "Auto & Truck",
    "Otomotiv Parça": "Auto Parts",
    "Banka": "Banks (Regional)",
    "Sigorta": "Insurance (General)",
    "Holding": "Diversified",
    "Enerji": "Power",
    "Yenilenebilir Enerji": "Green & Renewable Energy",
    "Telekomünikasyon": "Telecom. Services",
    "Perakende": "Retail (General)",
    "E-Ticaret": "Retail (Online)",
    "Gıda": "Food Processing",
    "İçecek": "Beverage (Soft)",
    "Tekstil": "Apparel",
    "İnşaat": "Engineering/Construction",
    "Havacılık": "Air Transport",
    "Turizm": "Hotel/Gaming",
    "Sağlık": "Healthcare Products",
    "Hastane": "Hospitals/Healthcare Facilities",
    "İlaç": "Drugs (Pharmaceutical)",
    "Teknoloji": "Software (System & Application)",
    "Yazılım": "Software (System & Application)",
    "Kimya": "Chemical (Basic)",
    "Petrokimya": "Chemical (Specialty)",
    "Petrol": "Oil/Gas (Integrated)",
    "Madencilik": "Metals & Mining",
    "Kağıt": "Paper/Forest Products",
    "Ambalaj": "Packaging & Container",
    "Savunma": "Aerospace/Defense",
    "Elektrik": "Electrical Equipment",
    "GYO": "R.E.I.T.",
    "Gayrimenkul": "Real Estate (Development)",
    "Ulaşım": "Transportation",
}


def fuzzy_match(query: str, threshold: float = 0.5) -> Optional[str]:
    """
    Sektör adını fuzzy match ile bul.

    Args:
        query: Sektör adı (İngilizce veya Türkçe)
        threshold: Minimum benzerlik skoru (0-1)

    Returns:
        En yakın sektör adı veya None
    """
    q = query.strip()

    # Direct match
    if q in INDUSTRY_BETAS:
        return q

    # Turkish alias
    if q in TURKISH_ALIASES:
        return TURKISH_ALIASES[q]

    # Case-insensitive match
    q_lower = q.lower()
    for name in INDUSTRY_BETAS:
        if name.lower() == q_lower:
            return name

    # Turkish alias case-insensitive
    for alias, name in TURKISH_ALIASES.items():
        if alias.lower() == q_lower:
            return name

    # Fuzzy match
    best_score = 0.0
    best_match = None
    for name in list(INDUSTRY_BETAS.keys()) + list(TURKISH_ALIASES.keys()):
        score = SequenceMatcher(None, q_lower, name.lower()).ratio()
        if score > best_score:
            best_score = score
            best_match = name

    if best_score >= threshold and best_match:
        if best_match in TURKISH_ALIASES:
            return TURKISH_ALIASES[best_match]
        return best_match

    return None


def get_beta(
    industry: str,
    market: str = "emerging",
) -> Optional[Dict[str, float]]:
    """
    Sektör unlevered beta lookup.

    Args:
        industry: Sektör adı (İngilizce veya Türkçe)
        market: "global" veya "emerging"

    Returns:
        {"industry": str, "unlevered_beta": float, "market": str, "n_firms": int}
    """
    matched = fuzzy_match(industry)
    if not matched:
        return None

    data = INDUSTRY_BETAS[matched]
    beta = data.get(market, data.get("global", 0.75))

    return {
        "industry": matched,
        "unlevered_beta": beta,
        "market": market,
        "n_firms": data.get("n", 0),
    }


def multi_business_beta(
    segments: List[Tuple[str, float]],
    market: str = "emerging",
) -> Dict[str, any]:
    """
    Multi-business şirket için revenue-weighted unlevered beta.
    Damodaran "Cost of capital worksheet" G34:L48 implementasyonu.

    Args:
        segments: [(industry_name, revenue_share), ...] — revenue_share decimal (toplamı 1.0)
        market: "global" veya "emerging"

    Returns:
        {
            "weighted_beta": float,
            "segments": [{"industry": str, "beta": float, "weight": float}, ...],
            "warnings": [str, ...]
        }
    """
    results = []
    warnings = []
    total_weight = 0.0
    weighted_beta = 0.0

    for industry, weight in segments:
        beta_info = get_beta(industry, market)
        if beta_info:
            results.append({
                "industry": beta_info["industry"],
                "beta": beta_info["unlevered_beta"],
                "weight": weight,
            })
            weighted_beta += beta_info["unlevered_beta"] * weight
            total_weight += weight
        else:
            warnings.append(f"Industry not found: {industry}")

    # Normalize if weights don't sum to 1
    if total_weight > 0 and abs(total_weight - 1.0) > 0.01:
        weighted_beta = weighted_beta / total_weight
        warnings.append(f"Weights normalized (sum was {total_weight:.2f})")

    return {
        "weighted_beta": round(weighted_beta, 4),
        "segments": results,
        "warnings": warnings,
    }


if __name__ == "__main__":
    print("=== Industry Beta Lookup ===\n")

    # Test: direct match
    for name in ["Steel", "Semiconductor", "Çimento", "Banka", "software"]:
        r = get_beta(name)
        if r:
            print(f"  {name:30s} → {r['industry']:40s} β_U={r['unlevered_beta']:.2f}")
        else:
            print(f"  {name:30s} → NOT FOUND")

    # Test: fuzzy match
    print("\n  --- Fuzzy Match ---")
    for name in ["Telecom Equipment", "auto parts mfg", "Retail online store"]:
        matched = fuzzy_match(name)
        print(f"  '{name}' → '{matched}'")

    # Test: multi-business
    print("\n  --- Multi-Business Beta ---")
    result = multi_business_beta([
        ("Steel", 0.4),
        ("Enerji", 0.35),
        ("Çimento", 0.25),
    ])
    print(f"  Weighted Beta: {result['weighted_beta']:.4f}")
    for s in result["segments"]:
        print(f"    {s['industry']:30s} β={s['beta']:.2f} w={s['weight']:.0%}")

    print(f"\n  Total industries: {len(INDUSTRY_BETAS)}")
    print("\n✅ beta_lookup.py çalışıyor.")
