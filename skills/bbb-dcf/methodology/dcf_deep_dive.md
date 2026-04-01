# DCF Deep Dive — FCFF, Projeksiyon, Terminal Value

## 1. FCFF vs FCFE

| | FCFF (Firma) | FCFE (Özsermaye) |
|---|---|---|
| **Nakit Akışı** | Borç öncesi, yeniden yatırım sonrası | Borç sonrası, yeniden yatırım sonrası |
| **İskonto** | WACC | Cost of Equity |
| **Sonuç** | Enterprise Value | Equity Value |
| **Tercih** | **Genel kural** — sermaye yapısı değişikliklerinden az etkilenir | Bankalar/finans (borç = hammadde) |

### FCFF Hesaplama

```
FCFF = EBIT × (1 - t) - Reinvestment
Reinvestment = ΔRevenue / Sales_to_Capital_Ratio
```

**⚠️ ÖNEMLİ:** Damodaran reinvestment'ı `CapEx - D&A + ΔWC` olarak DEĞİL, `ΔRevenue / Sales-to-Capital` olarak hesaplar. Bu daha temiz ve CapEx tahmini gerektirmez. CapEx/D&A sadece cross-check için.

### Alternatif (Geleneksel)
```
FCFF = EBIT(1-t) - Net CapEx - ΔWC
Net CapEx = CapEx - Depreciation
ΔWC = Δ(Non-cash Current Assets) - Δ(Non-debt Current Liabilities)
```

---

## 2. Damodaran 10 Yıllık Projeksiyon Mekaniği

### Gelir Büyüme Oranı
- **Yıl 1:** Input (analist/kullanıcı)
- **Yıl 2-5:** Input (CAGR)
- **Yıl 6-10:** Lineer interpolasyon → terminal growth

```python
# Yıl 6-10 interpolasyon
for yr in range(6, 11):
    g[yr] = g[5] - (g[5] - g_terminal) * (yr - 5) / 5
```

### Gelirler
```python
revenue[t] = revenue[t-1] × (1 + g[t])
```

### EBIT Marjı
- **Yıl 1:** Input (mevcut veya override)
- **Yıl 2 → convergence_year:** Lineer interpolasyon → hedef marj
- **Convergence sonrası:** Hedef marj sabit

```python
if yr <= convergence_year:
    margin[yr] = target - (target - yr1_margin) * (convergence_year - yr) / convergence_year
else:
    margin[yr] = target
```

### Vergi Oranı
- **Yıl 1-5:** Efektif vergi oranı
- **Yıl 6-10:** Lineer interpolasyon → marjinal vergi oranı
- **Terminal:** Marjinal (%25 Türkiye)

### EBIT(1-t) — NOL Entegrasyonu
```python
if ebit > 0:
    if ebit < nol_balance:
        nopat = ebit  # Tamamen korumalı
        nol_balance -= ebit
    else:
        nopat = ebit - (ebit - nol_balance) * tax_rate
        nol_balance = 0
else:
    nopat = ebit  # Negatif, vergi yok
    nol_balance += abs(ebit)  # NOL birikir
```

### Reinvestment
```python
# Yıl 1-5
reinvestment[t] = delta_revenue[t] / sales_to_capital_1_5

# Yıl 6-10
reinvestment[t] = delta_revenue[t] / sales_to_capital_6_10

# Terminal
reinvestment_terminal = (g / ROC) × EBIT_terminal(1-t)
```

### WACC
- **Yıl 1-5:** Başlangıç WACC (sabit)
- **Yıl 6-10:** Lineer interpolasyon → terminal WACC
- **Terminal:** `Rf + Mature_Market_ERP` (default) veya override

**⚠️ TR FİRMALARI:** Terminal WACC override ŞART! Default country premium'u sıfırlar.

### Kümülatif İskonto
```python
cdf[1] = 1 / (1 + wacc[1])
cdf[t] = cdf[t-1] / (1 + wacc[t])
```

---

## 3. Terminal Value

### Gordon Growth Model
```
TV = FCFF_{n+1} / (WACC - g)
```

### Genişletilmiş (ROC içeren) Formül
```
TV = EBIT_{n+1}(1-t) × (1 - g/ROC) / (WACC - g)
```

### ⚠️ KRİTİK İÇGÖRÜ: ROC vs WACC

| Durum | Etki | Anlamı |
|-------|------|--------|
| ROC = WACC | Büyüme değer yaratmaz | Terminal value büyümeden bağımsız! |
| ROC > WACC | Büyüme değer yaratır | Rekabet avantajı (moat) var |
| ROC < WACC | Büyüme değer **YOK EDER** | Büyümek zararlı |

**Damodaran default:** Terminal ROC = Terminal WACC (rekabet avantajı eriyip gider).  
**Override:** Güçlü moat varsa ROC > WACC kabul edilebilir (ASELS, BIMAS gibi).

### Terminal Growth Kuralları
1. Ekonominin nominal büyümesini aşamaz
2. Basit proxy: Rf ≈ nominal GDP büyümesi
3. Negatif olabilir (küçülen sektörler)
4. Para birimiyle tutarlı: TL → TL nominal büyüme, USD → %2-3

### Stabil Büyümede Ne Değişmeli
- Beta → 1'e yaklaşmalı
- Borç maliyeti → BBB veya üstü
- Borç oranı artabilir (istikrarlı kazançlar)
- ROC → WACC'e yakınsamalı

---

## 4. Firma → Özsermaye → Hisse Değeri

```
PV(10yr FCFF)                           # Projeksiyon dönemi
+ PV(Terminal Value)                     # Terminal
= Operating Asset Value
× (1 - P_failure) + Distress × P_fail   # İflas düzeltmesi
- Debt (MV)                             # Borç çıkar
- Minority Interests                     # Azınlık payı çıkar
+ Cash                                  # Nakit ekle
+ Cross Holdings (non-op assets)         # İştirakler ekle
- Employee Options (BS)                  # Opsiyonlar çıkar
= Equity Value
÷ Shares Outstanding
= Value per Share
```

---

## 5. Bankacılık FCFE Modeli

Bankalarda FCFF uygulanmaz (borç = hammadde).

```
FCFE = Net Gelir - ΔRegulatory Equity
Equity_Value = Σ FCFE_t/(1+Ke)^t + FCFE_{n+1}/(Ke - g)
```

- İskonto: Cost of Equity (WACC değil)
- Terminal: ROE → Ke yakınsaması
- Kısıt: BDDK SYR ≥ %12

**BIST bankalar:** AKBNK, GARAN, YKBNK, ISCTR, HALKB, VAKBN

---

## 6. Negatif/Düşük Kazanç Durumu

Negatif EBIT'li firmalar için:
1. Gelir büyümesi ve marj iyileşmesi üzerinden modelle
2. `Revenue Growth ($) = Reinvestment ($) × Sales/Capital`
3. Marjları kademeli olarak sektör ortalamasına yaklaştır
4. NOL birikimi takip et
