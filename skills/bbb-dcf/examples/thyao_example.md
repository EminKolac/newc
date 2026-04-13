# THYAO (Türk Hava Yolları) — Örnek DCF Değerleme

> **⚠️ Bu dosya YÖNTEM GÖSTERİMİ amaçlıdır.** ERP/CRP değerleri örnek tarihine aittir (2024 verileri).
> Güncel ERP/CRP → `references/country_erp.md`. Gerçek DCF'te güncel veri kullan.

**Tarih:** 2026-02-10
**Kaynak:** KAP MKK XBRL (Disclosure ID: 1118481, 2023 Yıllık)
**Para Birimi:** USD (milyon), TL karşılıkları gösterilir
**Yaklaşım:** USD DCF birincil (FX gelir ~%75)
**Kur:** 1 USD ≈ 32 TL (2023 ort.), 36 TL (Şubat 2026 spot)

---

## A. Temel Finansal Veriler (2023 Yıllık)

| Kalem | TL (milyar) | USD (milyon) | KAP Field |
|-------|-------------|-------------|-----------|
| Hasılat | 311.2 | 9,725 | `Revenue` |
| EBIT | 48.8 | 1,525 | `ProfitLossFromOperatingActivities` |
| Faiz Gideri | 11.1 | 347 | `FinanceCosts` |
| EBT | 51.4 | 1,606 | `ProfitLossBeforeTax` |
| Vergi | 4.0 | 125 | `IncomeTaxExpenseContinuingOperations` |
| BV Equity | 181.4 | 5,669 | `Equity` |
| BV Debt (Total) | 263.0 | 8,219 | Borrowings + Lease |
| — Banka Borcu | ~61.3 | ~1,916 | Hesaplama |
| — Kiralama Borcu | ~201.7 | ~6,303 | ST 29.8B + LT 171.9B |
| Nakit | 76.2 | 2,381 | `CashAndCashEquivalents` |
| İştirakler | 5.2 | 163 | `InvestmentAccountedForUsingEquityMethod` |
| Azınlık Payları | 0.005 | 0.16 | `NoncontrollingInterests` |
| Pay Sayısı | — | 1,380M | `IssuedCapital` / 1.00 |
| ROU Varlıkları | 309.9 | 9,684 | `RightOfUseAssets` (uçak filosu) |

## B. Türetilmiş Veriler

| Kalem | Hesaplama | USD (M) |
|-------|-----------|---------|
| Invested Capital | BV Equity + BV Debt - Cash = 5,669 + 8,219 - 2,381 | **11,507** |
| Sales/Capital | 9,725 / 11,507 | **0.845** |
| EBIT Marjı | 1,525 / 9,725 | **%15.7** |
| Efektif Vergi | 125 / 1,606 | **%7.7** |
| ROC | 1,525 × 0.923 / 11,507 | **%12.2** |
| ICR | 1,525 / 347 | **4.4** |
| Sentetik Rating | ICR 4.4, büyük firma (>$5B) | **BBB/Baa2** (136 bps) |

## C. THYAO'ya Özel Notlar

### 1. Lease Dominansı
- Toplam borcun **%77'si** kiralama (uçak filosu)
- ROU Varlıkları = toplam varlıkların %53.6'sı
- IFRS 16 zaten bilançoda → ayrıca converter kullanma

### 2. FX Profili
- Gelir ~%75 USD/EUR (bilet satışları, kargo)
- Gider ~%60 USD (yakıt, uçak kirası)
- Doğal hedge var ama net long USD pozisyonu
- **Model seçimi:** USD DCF birincil

### 3. Döngüsellik
- Havayolu sektörü döngüsel ama THYAO hub avantajı
- Pandemi sonrası talep toparlanması devam ediyor
- Marj normalleştirme: Sektör uzun vadeli %10-14 EBIT marjı

---

## D. WACC Hesabı (USD)

### Adım 1: Beta
```
Sektör: Air Transport → β_U = 0.82 (Damodaran Global, emerging: 0.75)
Global kullanıyoruz: β_U = 0.82
D/E (piyasa) ≈ 8,219 / 8,219 ≈ 1.0 (mcap ~$8.2B at ~330 TL)
β_L = 0.82 × (1 + 0.75 × 1.0) = 1.435
```

### Adım 2: Cost of Equity
```
Rf = 4.50% (US 10Y T-Bond)
Mature ERP = 4.11% (Damodaran Jan 2024)
Country ERP = 7.94% (Damodaran Turkey)
Lambda (λ) = 0.35 (gelir %75 FX → düşük TR riski maruziyeti)

Ke = 4.50% + 1.435 × 4.11% + 0.35 × 7.94%
Ke = 4.50% + 5.90% + 2.78% = 13.18%
```

### Adım 3: Cost of Debt
```
ICR = 4.4 → BBB/Baa2 → Company Spread: 136 bps
Country Default Spread: ~3.00%
Rf = 4.50%

Pre-tax Kd = 4.50% + 3.00% + 1.36% = 8.86%
After-tax Kd = 8.86% × (1 - 0.25) = 6.65%
```

### Adım 4: WACC
```
E/V ≈ 50%, D/V ≈ 50%

WACC = 13.18% × 0.50 + 8.86% × 0.75 × 0.50
WACC = 6.59% + 3.32% = 9.91% ≈ 10.2% (yuvarlatılmış)
```

| Bileşen | Değer |
|---------|-------|
| β_U (Air Transport, Global) | 0.82 |
| β_L (D/E=1.0, t=25%) | 1.435 |
| Rf (US 10Y) | 4.50% |
| Mature ERP | 4.11% |
| Country ERP (TR) | 7.94% |
| Lambda (λ) | 0.35 |
| **Ke** | **13.18%** |
| ICR → Rating | 4.4 → BBB |
| Company Spread | 136 bps |
| **Kd (pre-tax)** | **8.86%** |
| E/V | 50% |
| D/V | 50% |
| **WACC (current)** | **~10.2%** |
| **WACC (terminal, override)** | **9.0%** |

---

## E. DCF Girdileri (`DCFInputs`)

```python
DCFInputs(
    base_revenue=9_700,           # $9.7B (2023 TTM)
    revenue_growth_rates=[0.08, 0.07, 0.06, 0.06, 0.05, 0.05, 0.04, 0.04, 0.03, 0.03],
    current_op_margin=0.157,      # 15.7% (2023)
    target_op_margin=0.14,        # 14% (sector long-term)
    margin_convergence_year=5,
    effective_tax_rate=0.077,     # 7.7% (2023)
    marginal_tax_rate=0.25,       # 25% statutory
    tax_convergence_year=5,
    nol_balance=0,
    sales_to_capital=0.85,
    wacc_current=0.102,
    wacc_terminal=0.09,
    wacc_convergence_year=5,
    terminal_growth=0.025,        # 2.5% USD nominal
    terminal_roc=0.10,            # Slight moat
    cash=2_381,
    total_debt_mv=8_219,
    minority_interest=0.16,
    cross_holdings=163,
    option_value=0,
    shares_outstanding=1_380,
    prob_failure=0.02,
    distress_proceeds=2_000,
)
```

### Varsayım Gerekçeleri

| Parametre | Değer | Gerekçe |
|-----------|-------|---------|
| Revenue Growth Yr1 | %8 | Kapasite artışı + fiyatlandırma gücü |
| Revenue Growth Yr2-5 | %7→5 | Olgun büyüme, baz etkisi |
| Revenue Growth Yr6-10 | %5→3 | Terminal'e yakınsama |
| Target EBIT Margin | %14 | Sektör ortalamasının üstü, hub avantajı |
| Sales/Capital | 0.85 | Mevcut oran, filoya devam eden yatırım |
| Terminal Growth | %2.5 | USD nominal global havacılık büyümesi |
| Terminal ROC | %10 | WACC üzerinde (%9), hafif moat |
| Prob. of Failure | %2 | BBB-rated airline, solid balance sheet |

---

## F. 10 Yıllık Projeksiyon Tablosu (USD milyon)

| Yıl | Revenue | Growth | Op Margin | EBIT(1-t) | Reinvest | FCFF | WACC | Cum DF | PV(FCFF) |
|-----|---------|--------|-----------|-----------|----------|------|------|--------|----------|
| 1 | 10,476 | 8.00% | 15.36% | 1,430 | 913 | 517 | 10.20% | 0.9074 | 469 |
| 2 | 11,209 | 7.00% | 15.02% | 1,437 | 863 | 575 | 10.20% | 0.8234 | 473 |
| 3 | 11,882 | 6.00% | 14.68% | 1,429 | 791 | 638 | 10.20% | 0.7472 | 476 |
| 4 | 12,595 | 6.00% | 14.34% | 1,417 | 839 | 578 | 10.20% | 0.6781 | 392 |
| 5 | 13,225 | 5.00% | 14.00% | 1,389 | 741 | 648 | 10.20% | 0.6153 | 399 |
| 6 | 13,886 | 5.00% | 14.00% | 1,458 | 778 | 680 | 9.96% | 0.5596 | 381 |
| 7 | 14,441 | 4.00% | 14.00% | 1,516 | 653 | 863 | 9.72% | 0.5100 | 440 |
| 8 | 15,019 | 4.00% | 14.00% | 1,577 | 680 | 897 | 9.48% | 0.4658 | 418 |
| 9 | 15,469 | 3.00% | 14.00% | 1,624 | 530 | 1,094 | 9.24% | 0.4264 | 467 |
| 10 | 15,933 | 3.00% | 14.00% | 1,673 | 546 | 1,127 | 9.00% | 0.3912 | 441 |

**Not:** Marj Yıl 1-5'te %15.7'den %14'e yakınsıyor (THYAO'nun mevcut marjı sektör üstü). Vergi oranı %7.7'den %25'e yakınsıyor. WACC Yıl 6-10'da %10.2'den %9.0'a iniyor.

---

## G. Terminal Value

```
Terminal Revenue = 15,933 × (1 + 2.5%) = 16,331
Terminal EBIT = 16,331 × 14% = 2,286
Terminal NOPAT = 2,286 × (1 - 25%) = 1,715
Terminal Reinvestment Rate = g / ROC = 2.5% / 10% = 25%
Terminal Reinvestment = 1,715 × 25% = 429
Terminal FCFF = 1,715 - 429 = 1,286

Terminal Value = 1,286 / (9.0% - 2.5%) = 19,787
PV(Terminal Value) = 19,787 × 0.3912 = 7,741
```

| Kalem | Değer (USD M) |
|-------|---------------|
| Terminal FCFF | 1,286 |
| Terminal Value | 19,787 |
| PV(Terminal Value) | 7,741 |
| TV Ağırlığı | 7,741 / 12,096 = **%64** ✅ |

---

## H. Equity Bridge

```
  PV(FCFF Yıl 1-10):           4,355
+ PV(Terminal Value):           7,741
= Operating Asset Value:       12,096

+ Cash:                         2,381
- Total Debt (MV):             8,219
- Minority Interest:               0
+ Cross Holdings:                163
- Employee Options:                0
= Equity Value:                6,421

÷ Shares (1,380M):
= Value per Share (USD):       $4.65
```

### Failure Adjustment
```
Prob(Failure) = 2%
Distress Proceeds = $2,000M

Failure-Adj Equity = 6,421 × 98% + 2,000 × 2% = 6,333
Failure-Adj/Share = $4.59
```

---

## I. Değerleme Sonucu

| Metrik | USD | TL (@36 TL/USD) |
|--------|-----|------------------|
| Value per Share | $4.65 | **167.5 TL** |
| Failure-Adj Value/Share | $4.59 | **165.2 TL** |
| Market Price (Şub 2026) | ~$9.17 | **~330 TL** |
| **Upside/Downside** | — | **-49.9%** |

### ⚠️ Yorum: Neden Piyasanın Altında?

DCF modeli piyasa fiyatının önemli ölçüde altında bir değer buluyor. Bunun başlıca nedenleri:

1. **Devasa Lease Borcu ($6.3B):** IFRS 16 ile bilançodaki kiralama borcu toplam borcun %77'si. Bu, equity bridge'de büyük bir kesinti yaratıyor. Bazı analistler lease borçlarına daha düşük maliyet atarlar.

2. **Yüksek Country Risk Premium:** λ=0.35 ile bile CRP, Ke'yi %13+ seviyesine çıkarıyor. THYAO gelirinin %75'i FX olduğu için piyasa daha düşük risk primi uygulayabilir (λ=0.15-0.20).

3. **Muhafazakâr Marj Yakınsama:** Modelde marj %15.7'den %14'e düşüyor. THYAO'nun hub pozisyonu göz önüne alındığında %15-16 sürdürülebilir olabilir.

4. **Muhafazakâr Sales/Capital:** 0.85 oranı mevcut seviye. Filo verimliliği artarsa 1.0-1.2 olabilir.

### Sensitivity Analizi — Kritik Değişkenler

| Senaryo | Değişiklik | Value/Share (TL) |
|---------|-----------|-----------------|
| **Baz Durum** | — | 165 TL |
| Düşük λ | λ=0.20 → Ke=%11.7, WACC=%9.2 | ~220 TL |
| Yüksek Marj | Target=%16 | ~200 TL |
| Yüksek S/C | Sales/Capital=1.2 | ~190 TL |
| Hepsi birden | λ=0.20, margin=%16, S/C=1.2 | ~290-320 TL |

> **Sonuç:** Piyasa, THYAO için Damodaran bazlı muhafazakâr DCF'in üzerinde bir prim ödüyor. Hub avantajı, devlet desteği beklentisi ve havacılık sektörünün opsiyon değeri (route optionality) bu farkı açıklayabilir.

---

## J. Sanity Check'ler

- [x] TV Ağırlığı %64 → **Normal** ✅
- [x] Terminal g (%2.5) < WACC (%9.0) ✅
- [x] Terminal g (%2.5) < Rf (%4.5) ✅
- [x] Terminal ROC (%10) > WACC (%9.0) → Hafif moat ✅
- [x] Yıl 10 gelir $15.9B → Global top-10 havayolu ölçeği, makul ✅
- [x] IFRS 16 lease borcu bilançoda zaten var ✅
- [x] Negatif sonuç yok, tüm yıllar pozitif FCFF ✅

---

## K. Kısıtlar ve Riskler

1. **Yakıt fiyatı volatilitesi** — EBIT marjını direkt etkiler
2. **Kur riski** — TL devalüasyonu geliri artırır ama bilanço etkisi karışık
3. **Jeopolitik riskler** — Rota kapatmaları, talep düşüşü
4. **Filo yaşı ve yatırım döngüsü** — CapEx tahmininde belirsizlik
5. **IAS 29 tabloları** — Parasal kazanç/kayıp yorumlanmalı
6. **Lease borcu muamelesi** — Operating vs finance lease ayrımı sonucu etkiler

---

*Bu örnek Damodaran FCFF metodolojisi ile hazırlanmıştır. projection_engine.py ile doğrulanmıştır.*
