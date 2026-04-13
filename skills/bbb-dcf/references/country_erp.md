# Ülke Risk Primleri Referans

**Kaynak:** Damodaran Country ERP (190+ ülke, aylık güncelleme)
**API:** `dcf_tools/erp_updater.py` → `get_country_erp(country)`

> **⚠️ BU DOSYA KANONİK KAYNAK.** ERP/CRP değerleri yalnızca buradan referans alınır.
> Diğer dosyalardaki (risk_discount.md, thyao_example.md) rakamlar formül gösterimi/tarihsel örnek olabilir — güncel değildir.
> **Her DCF'te bu dosyadaki tarihi kontrol et.** Eski ise `erp_updater.py` çalıştır veya Damodaran'dan güncel al.

## Türkiye (Ocak 2026 Damodaran)

| Metrik | Değer |
|--------|-------|
| Moody's Rating | B1 |
| Country Default Spread | %3.83 |
| Country Risk Premium | %5.83 |
| Total ERP | %10.06 (= Mature %4.23 + Country %5.83) |
| Corporate Tax Rate | %25 |

## Mature Market ERP

**Değer:** %4.23 (Ocak 2026)  
**Kaynak:** Implied ERP, S&P 500 bazlı (Damodaran)  
**Güncelleme:** Aylık, her ayın başı

```python
from dcf_tools.erp_updater import get_turkey_erp
erp = get_turkey_erp()
mature_erp = 0.0423  # Ocak 2026 Damodaran implied ERP
```

## Bölge Ortalamaları

| Bölge | Country Risk Premium | Total ERP |
|-------|---------------------|-----------|
| ABD/Kanada | %0 | %4.23 |
| Batı Avrupa | %0.5-1.5 | %4.7-5.7 |
| Doğu Avrupa | %3.37 | %7.60 |
| Latin Amerika | %2.5-5.0 | %6.7-9.2 |
| Asya (gelişmiş) | %0.5-1.5 | %4.7-5.7 |
| Asya (gelişen) | %1.5-4.0 | %5.7-8.2 |
| Afrika | %3.0-8.0 | %7.2-12.2 |

**⚠️ Türkiye:** Bireysel ERP (%5.83) bölge ortalamasından (%3.37) yüksek. B1 rating. **TR-spesifik kullan, bölge ortalaması DEĞİL.**

## Seçilmiş Ülkeler (Ocak 2026 Damodaran)

| Ülke | Rating | Default Spread | Country ERP | Total ERP |
|------|--------|---------------|-------------|-----------|
| ABD | Aaa | %0 | %0 | %4.23 |
| Almanya | Aaa | %0 | %0 | %4.23 |
| Brezilya | Ba2 | %2.18 | %3.27 | %7.50 |
| Hindistan | Baa3 | %1.56 | %2.34 | %6.57 |
| Çin | A1 | %0.63 | %0.94 | %5.17 |
| G. Afrika | Ba2 | %2.56 | %3.84 | %8.07 |
| **Türkiye** | **B1** | **%3.83** | **%5.83** | **%10.06** |
| Rusya | Ca | %11.04 | %16.56 | %20.79 |

**Not:** Değerler zamanla değişir. Güncel veriler için `erp_updater.py` kullan.

## ERP Hesaplama Formülü

```
Country_Default_Spread = Rating → Spread tablosu
CRP = Default_Spread × (σ_equity / σ_bond)     # σ_E/σ_B = 1.5234 (Ocak 2026)
Total_ERP = Mature_ERP + CRP
```

**⚠️ NOT:** Formülde × 1.5 çarpanı **YOKTUR**. Damodaran sadece σ_E/σ_B oranını kullanır.

## Lambda Tablosu (BIST Referans)

| Firma | FX Gelir % | Yurtiçi % | λ (yaklaşık) |
|-------|-----------|-----------|-------------|
| THYAO | ~75% | ~25% | 0.35 |
| ASELS | ~60% | ~40% | 0.55 |
| ENKAI | ~80% | ~20% | 0.28 |
| EREGL | ~50% | ~50% | 0.70 |
| TOASO | ~40% | ~60% | 0.85 |
| FROTO | ~45% | ~55% | 0.75 |
| BIMAS | ~5% | ~95% | 1.35 |
| MGROS | ~5% | ~95% | 1.35 |
| AKBNK | ~15% | ~85% | 1.20 |
| TCELL | ~10% | ~90% | 1.28 |

**Formül:** `λ = firma_yurtiçi% / ortalama_yurtiçi%` (BIST ort. ~%70)
