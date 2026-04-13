#!/usr/bin/env python3
"""
R&D Amortizasyon Lookup Tablosu
Damodaran'ın sektör bazlı R&D amortizasyon süreleri (yıl).
90+ sektör mapping'i. DCF modelinde R&D kapitalizasyonu için kullanılır.

Kaynak: Damodaran "R&D Convergence" / "R&D Amortization" tabloları.
"""

from typing import Optional, Dict

# Sektör → R&D amortizasyon süresi (yıl)
# Damodaran'ın önerdiği sektör bazlı süreler
RD_AMORTIZATION_YEARS: Dict[str, int] = {
    # Technology
    "Semiconductor": 5,
    "Semiconductor Equip": 5,
    "Software (System & Application)": 3,
    "Software (Internet)": 3,
    "Software (Entertainment)": 3,
    "Computer Services": 3,
    "Computers/Peripherals": 5,
    "Electronics (General)": 5,
    "Electronics (Consumer & Office)": 5,
    "Information Services": 3,
    "IT Services": 3,
    
    # Healthcare & Pharma
    "Drugs (Pharmaceutical)": 10,
    "Drugs (Biotechnology)": 10,
    "Healthcare Products": 7,
    "Healthcare Information and Technology": 5,
    "Healthcare Support Services": 5,
    "Medical Devices": 7,
    "Hospitals/Healthcare Facilities": 7,
    
    # Industrial & Manufacturing
    "Aerospace/Defense": 10,
    "Air Transport": 7,
    "Auto & Truck": 5,
    "Auto Parts": 5,
    "Building Materials": 5,
    "Chemical (Basic)": 10,
    "Chemical (Diversified)": 10,
    "Chemical (Specialty)": 10,
    "Construction Supplies": 5,
    "Electrical Equipment": 5,
    "Engineering/Construction": 5,
    "Environmental & Waste Services": 5,
    "Farming/Agriculture": 5,
    "Food Processing": 5,
    "Food Wholesalers": 5,
    "Furn/Home Furnishings": 3,
    "Green & Renewable Energy": 7,
    "Homebuilding": 5,
    "Household Products": 3,
    "Industrial Services": 5,
    "Machinery": 7,
    "Metals & Mining": 7,
    "Office Equipment & Services": 5,
    "Oil/Gas (Production and Exploration)": 7,
    "Oil/Gas (Integrated)": 7,
    "Oil/Gas Distribution": 7,
    "Packaging & Container": 5,
    "Paper/Forest Products": 5,
    "Power": 7,
    "Precious Metals": 7,
    "Publishing & Newspapers": 3,
    "R.E.I.T.": 5,
    "Real Estate (Development)": 5,
    "Real Estate (General/Diversified)": 5,
    "Real Estate (Operations & Services)": 5,
    "Recreation": 5,
    "Reinsurance": 5,
    "Restaurant/Dining": 3,
    "Retail (Automotive)": 3,
    "Retail (Building Supply)": 3,
    "Retail (Distributors)": 3,
    "Retail (General)": 3,
    "Retail (Grocery and Food)": 3,
    "Retail (Online)": 3,
    "Retail (Special Lines)": 3,
    "Rubber& Tires": 5,
    "Shipbuilding & Marine": 7,
    "Shoe": 3,
    "Steel": 7,
    "Telecom (Wireless)": 5,
    "Telecom. Equipment": 5,
    "Telecom. Services": 5,
    "Tobacco": 5,
    "Transportation": 5,
    "Transportation (Railroads)": 7,
    "Trucking": 5,
    "Utility (General)": 7,
    "Utility (Water)": 7,
    
    # Consumer / Media
    "Advertising": 3,
    "Apparel": 3,
    "Auto Parts": 5,
    "Beverage (Alcoholic)": 5,
    "Beverage (Soft)": 5,
    "Broadcasting": 3,
    "Cable TV": 3,
    "Coal & Related Energy": 7,
    "Education": 5,
    "Entertainment": 3,
    "Hotel/Gaming": 5,
    
    # Diversified / Financial
    "Bank (Money Center)": 2,
    "Banks (Regional)": 2,
    "Brokerage & Investment Banking": 2,
    "Diversified": 5,
    "Financial Svcs. (Non-bank & Insurance)": 3,
    "Insurance (General)": 5,
    "Insurance (Life)": 5,
    "Insurance (Prop/Cas.)": 5,
    "Investments & Asset Management": 2,
    
    # Turkey-specific sectors (BIST)
    "Cam": 7,
    "Çimento": 7,
    "Demir Çelik": 7,
    "Gıda": 5,
    "Havayolu": 7,
    "Holding": 5,
    "İnşaat": 5,
    "Madencilik": 7,
    "Otomotiv": 5,
    "Perakende": 3,
    "Savunma": 10,
    "Teknoloji": 3,
    "Telekomünikasyon": 5,
    "Tekstil": 3,
    "Turizm": 5,
    "Enerji": 7,
}

# Aliases / alternative names
_ALIASES: Dict[str, str] = {
    "pharma": "Drugs (Pharmaceutical)",
    "biotech": "Drugs (Biotechnology)",
    "software": "Software (System & Application)",
    "internet": "Software (Internet)",
    "semiconductor": "Semiconductor",
    "bank": "Bank (Money Center)",
    "banking": "Bank (Money Center)",
    "insurance": "Insurance (General)",
    "telecom": "Telecom. Services",
    "oil": "Oil/Gas (Integrated)",
    "auto": "Auto & Truck",
    "steel": "Steel",
    "mining": "Metals & Mining",
    "retail": "Retail (General)",
    "food": "Food Processing",
    "chemical": "Chemical (Basic)",
    "defense": "Aerospace/Defense",
    "construction": "Engineering/Construction",
    "healthcare": "Healthcare Products",
    "media": "Entertainment",
    "energy": "Power",
}


def get_rd_amort_years(sector: str, default: int = 5) -> int:
    """
    Sektör adına göre R&D amortizasyon süresini döndürür.
    
    Args:
        sector: Sektör adı (exact match veya alias)
        default: Bulunamazsa varsayılan süre
        
    Returns:
        Amortizasyon süresi (yıl)
    """
    # Exact match
    if sector in RD_AMORTIZATION_YEARS:
        return RD_AMORTIZATION_YEARS[sector]
    
    # Alias match
    sector_lower = sector.lower().strip()
    if sector_lower in _ALIASES:
        return RD_AMORTIZATION_YEARS[_ALIASES[sector_lower]]
    
    # Partial match
    for key in RD_AMORTIZATION_YEARS:
        if sector_lower in key.lower():
            return RD_AMORTIZATION_YEARS[key]
    
    return default


def capitalize_rd(
    rd_expenses: list[float],
    sector: str,
    amort_years: Optional[int] = None,
) -> Dict[str, float]:
    """
    R&D harcamalarını kapitalize eder.
    
    Args:
        rd_expenses: Son N yılın R&D harcamaları (en eski → en yeni)
        sector: Sektör adı
        amort_years: Override amortizasyon süresi (None = lookup)
        
    Returns:
        {
            'rd_asset': Kapitalize edilmiş R&D varlık değeri,
            'amortization': Yıllık amortizasyon,
            'amort_years': Kullanılan süre,
            'adjustment_to_income': Gelir tablosu düzeltmesi (R&D - amortizasyon),
        }
    """
    years = amort_years or get_rd_amort_years(sector)
    n = len(rd_expenses)
    
    if n == 0:
        return {"rd_asset": 0, "amortization": 0, "amort_years": years, "adjustment_to_income": 0}
    
    # Kapitalize: her yılın R&D'sini kalan ömrüne göre varlığa ekle
    rd_asset = 0.0
    total_amort = 0.0
    
    for i, expense in enumerate(rd_expenses):
        age = n - i  # kaç yıl önce
        if age <= years:
            unamortized_fraction = 1.0 - (age / years)
            rd_asset += expense * unamortized_fraction
            yearly_amort = expense / years
            total_amort += yearly_amort
    
    current_rd = rd_expenses[-1] if rd_expenses else 0
    adjustment = current_rd - total_amort
    
    return {
        "rd_asset": round(rd_asset, 2),
        "amortization": round(total_amort, 2),
        "amort_years": years,
        "adjustment_to_income": round(adjustment, 2),
    }


def list_sectors() -> list[str]:
    """Tüm sektörleri listeler."""
    return sorted(RD_AMORTIZATION_YEARS.keys())


if __name__ == "__main__":
    print("=== R&D Amortizasyon Lookup Tablosu ===\n")
    print(f"Toplam sektör: {len(RD_AMORTIZATION_YEARS)}\n")
    
    # Test cases
    tests = ["Drugs (Pharmaceutical)", "software", "Steel", "Savunma", "unknown_sector"]
    for t in tests:
        yrs = get_rd_amort_years(t)
        print(f"  {t:40s} → {yrs} yıl")
    
    print("\n--- Kapitalizasyon Testi ---")
    rd_data = [100, 120, 140, 160, 180]  # 5 yıllık R&D
    result = capitalize_rd(rd_data, "Drugs (Pharmaceutical)")
    print(f"  Sektör: Pharma, R&D: {rd_data}")
    print(f"  Sonuç: {result}")
    
    print("\n✅ rd_lookup.py çalışıyor.")
