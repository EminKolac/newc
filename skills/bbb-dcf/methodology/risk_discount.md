# Risk ve İskonto Oranı

## 1. Risksiz Oran (Rf)

**Kurallar:**
- Uzun vadeli (10 yıllık devlet tahvili)
- Temerrüt riski olmamalı (default-free)
- **Para birimi eşleşmeli** — TL DCF → TL Rf; USD DCF → US T-Bond

### Türkiye İçin
```
TL Rf = TR 10Y DİBS Getirisi - TR Default Spread
```
Alternatif: `USD Rf + Beklenen Enflasyon Farkı`

**Reel Rf (IAS 29 DCF için):**
- TÜFE endeksli DİBS varsa → direkt reel oran
- Sentetik: US TIPS + TR default spread ≈ %2 + %4 = %6
- Pragmatik: Reel Rf = %2 sabit, CRP ayrı

---

## 2. Equity Risk Premium (ERP)

### Üç Yaklaşım

| Yaklaşım | Açıklama |
|----------|----------|
| Tarihsel | Hisse - risksiz tarihsel fark |
| Implied (tercih) | Mevcut fiyatlardan ters çözüm |
| Ortalama Implied | Tarihi implied ortalaması (~%4-4.5 ABD) |

### Türkiye ERP

```python
# Damodaran tablosundan (erp_updater.py)
turkey = get_turkey_erp()
# → Güncel veriler references/country_erp.md'de
# Ocak 2026: Mature %4.23 + Country %5.83 = Total %10.06
```

**⚠️ ERP değerleri aylık değişir.** Güncel rakamlar için `references/country_erp.md`'ye bak veya `erp_updater.py` çalıştır. Buradaki sayılar yalnızca formül gösterimi içindir.

**Güncelleme:** Damodaran her ayın başında günceller. `erp_updater.py` cache + web fetch yapar.

---

## 3. Beta

### Bottom-up Beta (Tercih Edilen)

XU100 regresyon betası **güvenilmez** (düşük likidite, yüksek noise, bankalar ağırlıklı).

```python
# 1. Sektör unlevered beta al (Damodaran Global)
β_U = damodaran_global_industry_beta[sector]

# 2. Firma kaldıracıyla lever et
β_L = β_U × (1 + (1-t) × (D/E))
```

**D/E hesabı:** Piyasa değeri ağırlıkları kullan.
```
E = Market Cap = Hisse Fiyatı × Pay Sayısı
D = Total Debt (MV) ≈ BV Debt (yaklaşım)
D/E = D / E
```

### Multi-Business Beta
Birden fazla segmentte faaliyet gösteren firmalar:
```
β_U_firm = Σ (Revenue_segment_i / Total_Revenue) × β_U_sector_i
```

### Total Beta (Özel Firmalar)
```
Total β = Market β / Sektörün piyasayla korelasyonu
```

---

## 4. Country Risk Premium (CRP) — TR İçin Kritik

### Hesaplama
```
Country Default Spread = TR Bond Yield - US Bond Yield (eşdeğer vade)
Country ERP = Default Spread × (σ_equity / σ_bond)
```

Güncel veriler `references/country_erp.md`'de. Ocak 2026: Default Spread %3.83 × σ_E/σ_B 1.5234 = CRP %5.83.

### Firma Bazlı — Lambda (λ) Yaklaşımı

```
Ke = Rf + β × Mature_ERP + λ × Country_ERP
```

```python
λ = firma_yurtiçi_gelir_pct / ortalama_firma_yurtiçi_gelir_pct
```

| Firma Tipi | λ | Anlamı |
|-----------|---|--------|
| THYAO (ihracatçı) | 0.3-0.5 | Düşük TR riski |
| BIMAS (iç pazar) | 1.0-1.2 | Tam TR riski |
| ASELS (yarı ihracat) | 0.6-0.8 | Orta |

---

## 5. Cost of Debt (Kd)

### Tercih Sırası
1. İşlem gören tahvil → YTM
2. Kredi notu → rating + spread
3. **Sentetik rating** (en yaygın BIST için)

### Sentetik Rating

```python
from dcf_tools.synthetic_rating import cost_of_debt

result = cost_of_debt(
    icr=4.0,                    # EBIT / Interest Expense
    risk_free_rate=0.045,
    country_default_spread=0.06,
    market_cap_usd_b=2.0,
    tax_rate=0.25
)
# → rating, pre_tax_kd, after_tax_kd
```

### ICR → Rating Tablosu (2024, Büyük Firma)

| ICR Aralığı | Rating | Spread (bps) |
|-------------|--------|-------------|
| > 12.50 | AAA | 54 |
| 9.50-12.50 | AA- | 67 |
| 7.50-9.50 | A+ | 83 |
| 6.50-7.50 | A | 98 |
| 5.50-6.50 | A- | 108 |
| 4.50-5.50 | BBB+ | 121 |
| 3.75-4.50 | BBB | 136 |
| 3.00-3.75 | BBB- | 174 |
| 2.50-3.00 | BB+ | 213 |
| 2.25-2.50 | BB | 268 |
| 2.00-2.25 | BB- | 335 |
| 1.75-2.00 | B+ | 396 |
| 1.50-1.75 | B | 497 |
| 1.25-1.50 | B- | 648 |
| 0.80-1.25 | CCC | 865 |
| < 0.20 | D | 1899 |

**Küçük firmalar (<$5B):** Daha muhafazakâr eşikler (aynı ICR → daha düşük rating).

### Borç Maliyeti
```
Pre-tax Kd = Rf + Country_Default_Spread + Company_Spread
After-tax Kd = Kd × (1 - t)
```

---

## 5B. IAS 29 Reel DCF — Para Birimi Tutarlılık Kuralı ⚠️

> **KRİTİK:** IAS 29 düzeltmeli (reel) tablolara nominal WACC uygulamak EN YAYGIN HATADIR.
> Reel tablolar + nominal WACC = çöp sonuç. ASLA karıştırma!

### Hangi DCF → Hangi Parametreler?

| Parametre | Nominal TL DCF | Reel TL DCF (IAS 29) |
|-----------|---------------|---------------------|
| **Rf** | TR 10Y DİBS (~%28-31) | Reel Rf (~%2-3) |
| **ERP** | Aynı (Damodaran) | Aynı (Damodaran) |
| **CRP** | Aynı (Damodaran) | Aynı (Damodaran) |
| **Beta** | Aynı | Aynı |
| **Ke** | ~%39-42 | ~%12-15 |
| **Kd** | Nominal (KAP'tan direkt) | **Fisher ile reel'e çevir!** |
| **Büyüme** | Nominal (%25-35) | Reel (%5-16) |
| **Terminal g** | Nominal GDP (~%15-20) | Reel GDP (~%3-4) |
| **WACC** | ~%35-45 | ~%12-18 |

### Reel Kd Dönüşümü — Fisher Denklemi (ZORUNLU)

KAP dipnotlarındaki efektif faiz oranı (NOT 13) **nominal**. Reel DCF yapıyorsan dönüştür:

```
Reel Kd = (1 + Nominal Kd) / (1 + Beklenen Enflasyon) − 1

Örnek (EBEBK FY2025):
  Nominal Kd = %53,57 (KV murabaha, NOT 13)
  Beklenen enflasyon = %25 (2026 beklentisi)
  Reel Kd = (1,5357) / (1,25) − 1 = %22,9
  After-tax reel Kd = %22,9 × (1 − 0,23) = %17,6
```

### Reel Ke Hesabı

CAPM bileşenleri zaten reel-uyumlu — Damodaran ERP/CRP doğrudan reel Rf ile kullanılabilir:

```
Reel Ke = Reel Rf + β_L × Mature_ERP + λ × Country_ERP

Örnek:
  Reel Rf = %2,5 (US TIPS + TR default spread proxy)
  β_L × Mature_ERP = 1,2 × %4,23 = %5,1
  λ × Country_ERP = 1,0 × %5,83 = %5,8
  Reel Ke ≈ %13,4
```

### Fisher Cross-Check (ZORUNLU)

Reel ve nominal WACC'ın tutarlılığını doğrula:
```
(1 + Nominal WACC) ≈ (1 + Reel WACC) × (1 + Beklenen Enflasyon)
Sapma <%5 → ✅ Tutarlı  |  %5-10 → ⚠️ Kontrol et  |  >%10 → 🔴 Hata var
```

---

## 6. WACC

```
WACC = Ke × (E/V) + Kd × (1-t) × (D/V)
```

**⚠️ IAS 29 Reel DCF:** Ke ve Kd'nin REEL olduğundan emin ol! (bkz. §5B yukarıda)

### 6A. Small Firm Premium (SFP) — Küçük Şirketler İçin ZORUNLU

> **Gerekçe:** Küçük piyasa değerli şirketler (MCap <$500M) tarihsel olarak büyük şirketlerden daha risklidir: düşük likidite, dar yatırımcı tabanı, yönetişim riski, tek ürün/pazar bağımlılığı. Bu ek risk WACC'a yansıtılmalıdır.

**SFP Tablosu (Ke'ye eklenir):**

| MCap (USD) | SFP | Gerekçe |
|-----------|-----|---------|
| >$5B | %0 | Büyük — SFP gereksiz |
| $1B - $5B | %0-1 | Orta büyük — minimal |
| $500M - $1B | %1-2 | Orta — likidite sınırlı |
| $250M - $500M | %2-3 | Küçük — belirgin risk primi |
| <$250M | %3-5 | Mikro — yüksek risk primi |

**Uygulama:**

```
Ke = Rf + β × (ERP + λ × CRP) + SFP
```

**Karar noktaları:**
- MCap hesabı: Analiz tarihi itibarıyla, güncel hisse fiyatı × toplam pay sayısı
- BIST şirketlerinde $250M-500M aralığı çok yaygın → SFP %2-3 sık uygulanacak
- SFP uygulanmadıysa → gerekçe zorunlu ("SFP neden sıfır?")
- SFP Terminal WACC'ta da korunur mu? → Şirket büyüyüp büyük piyasa değerine ulaşma potansiyeli varsa terminal'de azaltılabilir (ama tamamen sıfırlamak agresif)

**EBEBK Örneği:**
```
MCap = $225M → SFP = %2,5-3,0
Terminal'de MCap büyüme beklentisi varsa → SFP %1,5'e azaltılabilir
```

V = E + D. Piyasa değeri ağırlıkları kullan!

### Piyasa Değeri Borç
```python
MV_Debt = Interest × PV_annuity(n, Kd) + BV_Debt / (1+Kd)^n
# Basitleştirilmiş: MV_Debt ≈ BV_Debt (BIST'te çoğunlukla yeterli)
```

### Optimal Sermaye Yapısı
WACC'i minimize eden D/E oranı. Pratik: Mevcut yapıyı kullan, terminalde sektör ortalamasına yakınsama.

### Terminal WACC

**Default:** `Rf + Mature_Market_ERP` (~%8.2)
- Country premium tamamen düşer
- Beta → 1, borç maliyeti → BBB

**TR Override (önerilen):**
```
Terminal_WACC = Rf + Mature_ERP + α × Country_ERP
# α = 0.3-0.7 (Türkiye'nin 10 yılda tamamen gelişmiş piyasa olma olasılığı?)
```
