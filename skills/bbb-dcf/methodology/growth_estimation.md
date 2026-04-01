# Büyüme Oranı Tahmini

## 1. Üç Kaynak

### 1.1 Tarihsel Büyüme
İyi başlangıç noktası ama tek başına yetersiz. Geçmiş-gelecek korelasyonu sınırlı.

### 1.2 Analist Tahminleri
Yararlı referans ama körü körüne güvenme.

### 1.3 Temel Büyüme (Retention × ROC) — Tercih Edilen

**ROC Sabitken:**
```
g = Reinvestment Rate × ROC
```

**ROC Değişiyorken:**
```
g = ROC_{t+1} × RR + (ROC_{t+1} - ROC_t) / ROC_t
```
İkinci terim "verimlilik büyümesi" — geçicidir. Yeni yatırımlardan gelen büyüme sürdürülebilir.

---

## 2. ROC (Return on Capital) Hesaplama

```python
ROC = EBIT(1-t) / Invested_Capital
Invested_Capital = BV_Equity + BV_Debt - Cash
```

### KAP Verileriyle
```python
IC = items['Equity']['CURR'] + items['CurrentBorowings']['CURR'] + items['LongtermBorrowings']['CURR'] - items['CashAndCashEquivalents']['CURR']
NOPAT = items['ProfitLossFromOperatingActivities']['CURR'] * (1 - tax_rate)
ROC = NOPAT / IC
```

---

## 3. Reinvestment Rate

### Damodaran Yöntemi (Sales/Capital)
```python
# Reinvestment = ΔRevenue / Sales_to_Capital
SC = Revenue / Invested_Capital
Reinvestment = (Revenue_t+1 - Revenue_t) / SC
RR = Reinvestment / EBIT(1-t)
```

### Geleneksel
```
RR = (Net CapEx + ΔWC) / EBIT(1-t)
```

---

## 4. Negatif Kazançlı Firmalar

EBIT negatifse g = RR × ROC anlamsız. Alternatif:

```
Revenue Growth ($) = Reinvestment ($) × Sales/Capital
```

1. Gelir büyümesi tahmin et
2. Marjları kademeli olarak sektör ortalamasına yaklaştır
3. Reinvestment = ΔRevenue / Sales-to-Capital

---

## 5. Terminal Growth Rate

### Kurallar
1. **Ekonominin nominal büyümesini AŞAMAZ** — üst sınır
2. Basit proxy: Rf ≈ nominal GDP büyümesi
3. **Para birimi tutarlılığı:** TL → TL nominal; USD → %2-3
4. **Negatif olabilir** — küçülecek firmalar (fosil yakıt, tütün)

### Türkiye Terminal Growth

| Para Birimi | Terminal g | Mantık |
|-------------|-----------|--------|
| Nominal TL | %20-30 (≈ Rf) | Enflasyon dahil |
| Reel TL | %3-4 | Reel GDP potansiyeli |
| USD | %2-3 | Global ekonomi büyümesi |

---

## 6. Terminal Reinvestment Rate

```
RR_terminal = g / ROC_terminal
```

ROC = WACC ise (default): `RR = g / WACC`  
ROC > WACC ise (override): RR düşer → daha yüksek FCFF

---

## 7. Döngüsel Firmalarda EBIT Normalleştirme

Döngüsel firmalar (EREGL, SASA, TUPRS) için mevcut EBIT yanıltıcı.

### Normalleştirme Yöntemleri

1. **Tarihsel ortalama marj:** Son 7-10 yıl EBIT marjı ortalaması × mevcut gelir
2. **Sektör ortalama marj:** Peers ortalamasını referans al
3. **Commodity-linked:** Uzun vadeli emtia fiyat konsensüsü ile normalize
   - EREGL: Long-term HRC $500-600/ton
   - TUPRS: Long-term crack spread $5-7/bbl

**Kural:**
- Döngünün tepesinde: Normalized < Mevcut → normalized kullan (overvaluation riski)
- Döngünün dibinde: Normalized > Mevcut → normalized kullan (undervaluation riski)
