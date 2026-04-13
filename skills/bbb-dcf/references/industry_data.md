# Sektör Ortalamaları Referans

**Kaynak:** Damodaran Industry Averages (Global dataset, 47,698 firma)  
**Güncelleme:** Yılda 2 kez (Ocak + Temmuz)

## Kullanım

Sektör ortalamaları 3 yerde kullanılır:
1. **Beta:** Sektör unlevered beta → bottom-up
2. **Marj/ROIC:** Target margin ve terminal ROC referansı
3. **Sales/Capital:** Reinvestment verimliliği benchmarkı

## Veri Kaynağı

```
https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/
- betas.html (US, 94 sektör)
- betaGlobal.html (Global, 94 sektör)
- wacc.html (Cost of capital)
- margin.html (Operating margins)
- EVA.html (ROIC, EVA)
```

## BIST İçin Uygun Sektör Eşleştirme

| BIST Sektör | Damodaran Sektör | β_U (yaklaşık) |
|-------------|------------------|-----------------|
| THYAO | Air Transport | 0.90 |
| ASELS | Aerospace/Defense | 0.85 |
| EREGL | Steel | 1.10 |
| FROTO, TOASO | Auto & Truck | 0.90 |
| BIMAS, MGROS | Retail (Grocery) | 0.55 |
| AKBNK, GARAN | Bank (Money Center) | 0.50 |
| TUPRS | Oil/Gas (Integrated) | 0.85 |
| SASA, PETKM | Chemical (Diversified) | 0.95 |
| TCELL, TTKOM | Telecom. Services | 0.55 |
| KCHOL, SAHOL | Diversified | 0.70 |
| ENKAI | Engineering/Construction | 0.80 |
| PGSUS | Air Transport | 0.90 |
| TAVHL | Transportation | 0.75 |
| SISE | Building Materials | 0.80 |

**⚠️ Not:** Global dataset tercih et (daha geniş örneklem). US dataset yalnızca ABD firmaları.

## Tipik Sektör Metrikleri (Yaklaşık, Referans)

| Sektör | EBIT Marjı | ROIC | Sales/Capital | EV/EBITDA |
|--------|-----------|------|---------------|-----------|
| Air Transport | %10-14 | %10-15 | 0.8-1.2 | 5-7x |
| Aerospace/Defense | %12-16 | %15-20 | 1.0-1.5 | 12-16x |
| Steel | %8-12 | %10-14 | 1.0-1.5 | 4-6x |
| Auto & Truck | %6-10 | %10-15 | 1.2-2.0 | 5-8x |
| Retail (Grocery) | %3-5 | %12-18 | 3.0-5.0 | 6-10x |
| Banking | — | ROE %12-18 | — | — |
| Oil/Gas | %10-16 | %8-12 | 0.8-1.2 | 4-6x |
| Telecom | %20-30 | %8-12 | 0.5-0.8 | 5-7x |

**Not:** Değerler döngü pozisyonuna göre değişir. Normalize edilmiş ortalamalar kullanılmalı.

## R&D Amortizasyon Süreleri

Bkz. `dcf_tools/rd_lookup.py` — 90+ sektör mapping. Özet:

| Kategori | Süre |
|----------|------|
| Yazılım | 2-3 yıl |
| İlaç/Biyotek | 8-10 yıl |
| Savunma | 5-10 yıl |
| Otomotiv | 5-6 yıl |
| Elektronik | 3-5 yıl |
| Çelik/Madencilik | 7 yıl |
| Default | 5 yıl |
