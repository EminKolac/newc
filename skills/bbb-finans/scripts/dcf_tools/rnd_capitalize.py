"""
BBB Finans DCF Tools — R&D Kapitalizasyonu
MACKO Ar-Ge Dönüştürücü metodolojisi (Damodaran Excel)

Referans: DCF_MOTOR_GELISTIRME_BRIEF.md → Sorun 2: Ar-Ge Kapitalizasyonu
Hazırlayan: Kaya | Uygulayan: Can | Tarih: 2026-02-19
"""

from typing import Optional, List


# ─── Sektörel Amortizasyon Süreleri ──────────────────────────────────────────
# Kaynak: MACKO Ar-Ge Dönüştürücü sayfası (Damodaran global averages)
# Default: 3 yıl (muhafazakâr)

SECTOR_RND_AMORT: dict[str, int] = {
    # Otomotiv
    "Auto & Truck": 10,
    "Auto Parts": 5,
    # İlaç & Biyoteknoloji
    "Drugs (Pharmaceutical)": 10,
    "Drugs (Biotechnology)": 10,
    "Healthcare Products": 5,
    "Healthcare Services": 5,
    # Teknoloji
    "Computer Services": 3,
    "Computers/Peripherals": 5,
    "Electronics (General)": 5,
    "Semiconductor": 5,
    "Semiconductor Equip": 5,
    "Software (System & Application)": 3,
    "Software (Entertainment)": 3,
    # Savunma & Makine
    "Aerospace/Defense": 10,
    "Electrical Equipment": 10,
    "Machinery": 5,
    "Industrial Products": 5,
    # Telekomünikasyon
    "Telecom (Wireless)": 5,
    "Telecom (Wireline)": 5,
    # Kimya & Enerji
    "Chemical (Basic)": 5,
    "Chemical (Specialty)": 5,
    "Oil/Gas (Integrated)": 5,
    # Medya & Reklam
    "Advertising": 2,
    "Entertainment": 3,
    # Diğer
    "Food Processing": 3,
    "Retail (General)": 2,
    "Retail (Grocery and Food)": 2,
    "Retail (Online)": 3,
}


def capitalize_rnd(
    rnd_current: float,
    rnd_history: List[float],
    amortization_years: int,
    tax_rate: float = 0.25,
) -> dict:
    """
    MACKO Ar-Ge Dönüştürücü metodolojisi — R&D Kapitalizasyonu.

    Damodaran: "R&D is not an expense, it's an investment."
    Muhasebe R&D'yi gider yazıyor → ekonomik gerçekliği yansıtmıyor.
    Bu fonksiyon EBIT ve BV Equity'i düzeltiyor.

    Args:
        rnd_current:       Mevcut yıl R&D harcaması (TL, pozitif)
        rnd_history:       [t-1, t-2, ...] Önceki yıllar, azalan sıra (pozitif)
        amortization_years: Sektöre göre amortizasyon süresi (yıl)
        tax_rate:          Vergi oranı (0.0–1.0)

    Returns:
        dict:
            rnd_asset          — Birikmiş amortize edilmemiş R&D varlığı
            amortization_current — Bu yılın amortismanı
            ebit_adjustment    — EBIT'e eklenecek (pozitif = artış)
            equity_adjustment  — BV Equity'e eklenecek (R&D varlığı)
            tax_shield         — Vergi tasarrufu (bilgi amaçlı)
            years_used         — Fiilen kullanılan yıl sayısı
            all_rnd_values     — Hesaplamada kullanılan tüm R&D değerleri

    Formüller (MACKO / Damodaran):
        R&D Varlığı    = Σ(R&D_i × (N - i) / N)   [amortize edilmemiş kısım]
        Amortisman     = Σ(R&D_i / N)               [toplam yıllık amortisman]
        EBIT Düzelt.   = R&D_current - Amortisman    [damodaran: +R&D_curr - amort]
        Vergi kalkanı  = EBIT Düzeltmesi × tax_rate  [bilgi amaçlı]

    Not: EBIT düzeltmesi pozitifse EBIT artar (mevcut yıl R&D > kümülatif amortisman).
    Büyüyen R&D harcamalarında bu her zaman pozitiftir.
    """
    if amortization_years < 1:
        amortization_years = 1

    n = amortization_years

    # Tüm R&D değerleri: mevcut yıl + önceki yıllar (max N-1 tane)
    all_rnd = [rnd_current] + list(rnd_history[: n - 1])
    years_used = len(all_rnd)

    rnd_asset = 0.0
    amort_current = 0.0

    for i, rnd_val in enumerate(all_rnd):
        # i=0 → mevcut yıl → amortize edilmemiş kısım = (N-0)/N = 1 (tam varlık)
        # i=1 → t-1        → amortize edilmemiş kısım = (N-1)/N
        # i=N-1 → en eski  → amortize edilmemiş kısım = 1/N
        unamortized_fraction = (n - i) / n
        rnd_asset += rnd_val * unamortized_fraction
        amort_current += rnd_val / n

    # EBIT düzeltmesi: R&D_current EBIT'ten çıkarılmış, geri ekle; amortisman gider
    ebit_adj = rnd_current - amort_current
    equity_adj = rnd_asset
    tax_shield = ebit_adj * tax_rate

    return {
        "rnd_asset": round(rnd_asset, 0),
        "amortization_current": round(amort_current, 0),
        "ebit_adjustment": round(ebit_adj, 0),
        "equity_adjustment": round(equity_adj, 0),
        "tax_shield": round(tax_shield, 0),
        "years_used": years_used,
        "amortization_years": n,
        "all_rnd_values": [round(v, 0) for v in all_rnd],
    }


def get_rnd_amort_years(sector_name: str, override: Optional[int] = None) -> int:
    """
    Sektöre göre R&D amortizasyon süresini döndür.

    Args:
        sector_name: Damodaran sektör adı (SectorService'ten)
        override:    Kullanıcı override (None ise sektör otomatik)

    Returns:
        int: Amortizasyon süresi (yıl), default 3
    """
    if override is not None and override > 0:
        return override
    return SECTOR_RND_AMORT.get(sector_name, 3)
