# Özel Durumlar ve Ayarlamalar

## 1. R&D Kapitalizasyonu

Muhasebe R&D'yi gider yazar ama mantıken sermaye harcamasıdır.

### Adımlar
1. Sektöre göre amortizasyon süresi belirle (2-10 yıl)
2. Son n yılın R&D harcamalarını topla
3. Amortize edilmemiş kısmı = "araştırma varlığı"

```python
from dcf_tools.rd_lookup import capitalize_rd, get_rd_amort_years

years = get_rd_amort_years("Savunma")  # 10 yıl
result = capitalize_rd(
    rd_expenses=[100, 120, 140, 160, 180],  # Son 5 yıl
    sector="Savunma"
)
# → rd_asset, amortization, adjustment_to_income
```

### Etkiler
- EBIT ↑ (R&D gideri yerine daha düşük amortisman)
- Sermaye ↑ (araştırma varlığı eklenir)
- **FCFF DEĞİŞMEZ!** (Etki EBIT ve CapEx'te birbirini dengeler)
- ROC daha doğru ölçülür

### Sektör Süreleri (Referans)
| Sektör | Yıl |
|--------|-----|
| Yazılım/SaaS | 2-3 |
| İlaç/Biyotek | 8-10 |
| Savunma/Havacılık | 5-7 |
| Otomotiv | 5-6 |
| Elektronik | 3-5 |
| BIST default | 5 |

---

## 2. IFRS 16 Kiralama Düzeltmesi

**IFRS 16 sonrası (2019+):** Kiralamalar zaten bilançoda borç. Damodaran'ın "Operating Lease Converter"ına genelde gerek yok.

### Kontrol
```python
# KAP'tan lease vs banka borç ayrımı
lease_st = items.get('CurrentPortionOfLongTermLeasingDebtsToUnrelatedParties', {}).get('CURR', 0)
lease_lt = items.get('LongTermLeasingDebtsToUnrelatedParties', {}).get('CURR', 0)
total_lease = lease_st + lease_lt

# Eğer borçta zaten dahilse → "No" (çift sayım yapma)
# Eğer off-balance sheet kiralamalar varsa → converter kullan
```

### THYAO Örneği
- ROU Varlıkları: 309.9B TL (toplam varlıkların %53.6'sı — uçak filosu!)
- Lease Borcu: ST 29.8B + LT 171.9B = 201.7B TL
- Bank Borcu: ~61.3B TL
- **Ayrım kritik:** THYAO'da toplam borcun %77'si lease

### Düzeltilmiş EBIT (eski yöntem, IFRS 16 öncesi)
```
Adjusted_EBIT = EBIT + Kd_pretax × PV(Lease Commitments)
```

---

## 3. İflas/Failure Olasılığı

DCF "going concern" varsayar. İflas riski yüksekse düzelt.

```
Adjusted_Value = DCF_Value × P(hayatta) + Distress_Proceeds × P(iflas)
```

### İflas Olasılığı Kaynakları
1. Tahvil fiyatından ters çözüm (bond-based)
2. CDS spread'inden
3. BLS sektörel hayatta kalma verisi
4. Sentetik rating → tarihsel default oranları

### Ne Zaman Kullan
- Negatif EBIT ve yüksek borç
- ICR < 1.5
- CDS spread > 1000 bps
- Döviz borcu yüksek + TL gelir (kur şoku riski)

---

## 4. Holding Değerlemesi — NAV + İndirim

BIST holdingler: SAHOL, KCHOL, TKFEN, TAVHL, GLYHO, DOHOL

### NAV Hesaplama
```
NAV = Σ (İştirak_i × MV × pay%) [borsada işlem görenler]
    + Σ (İştirak_j × EV/EBITDA × EBITDA_j × pay%) [borsada işlem görmeyenler]
    + Holding net nakit
    - Holding borcu
    - Holding merkez giderleri (kapitalize)
```

### Holding İndirimi
```
İndirim = (NAV - Market Cap) / NAV
```
BIST tipik: %15-40

**Etkileyen faktörler:**
- Yönetişim kalitesi (düşük → yüksek indirim)
- Şeffaflık
- Temettü politikası (düşük payout → yüksek indirim)
- Konglomerate discount (ilgisiz sektörler)

---

## 5. Çalışan Opsiyonları

```python
from dcf_tools.option_value import option_value_with_dilution, OptionParams

params = OptionParams(
    num_options=10_000_000,
    exercise_price=50.0,
    expiration_years=3.0,
    stock_price=80.0,
    risk_free_rate=0.05,
    volatility=0.35,
    shares_outstanding=100_000_000
)
result = option_value_with_dilution(params, equity_value=8_000_000_000)
# → total_option_value (equity'den düşülecek)
```

**BIST'te:** Nadiren var, genelde ihmal edilir. Varsa 10K dipnotlarından.

---

## 6. Kontrol Primi & Likidite İskontosu

### Kontrol Primi
```
Kontrol Değeri = Optimal_Yönetim_Değeri - Mevcut_Yönetim_Değeri
```

### Likidite İskontosu
- Özel firmalar: %12-35
- BIST küçük şirketler (düşük likidite): %5-15
- BIST30: Minimal (%0-5)

---

## 7. Nakit Değerlemesi

Nakit her zaman nominal değerinde değildir!

| ROC vs WACC | Nakit Değeri |
|-------------|-------------|
| ROC > WACC | Nominal (yönetim iyi kullanacak) |
| ROC < WACC | Nominal altı (yönetim kötü yatıracak) |
| Ülke riski | Hapsolabilir (country discount) |

---

## 8. Karmaşıklık İskontosu

Çoklu iş kolları, opak muhasebe → karmaşıklık skoru

**Seçenekler:**
1. Nakit akışlarını düzelt
2. İskonto oranını yükselt
3. Büyüme dönemini kısalt
4. Değerden düz iskonto uygula
