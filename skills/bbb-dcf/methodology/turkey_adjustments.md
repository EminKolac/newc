# Türkiye'ye Özel DCF Ayarlamaları

## 1. IAS 29 Hiperenflasyon Muhasebesi (2022+)

Türkiye 2022'den beri IAS 29 kapsamında. BIST firmaları enflasyon düzeltmeli tablolar yayınlıyor.

### Etkiler
1. Finansal tablolar satın alma gücüne göre yeniden düzenleniyor
2. Tarihsel maliyet rakamları Yİ-ÜFE endeksiyle düzeltiliyor
3. **Parasal Kalem Kazanç/Kayıpları** gelir tablosuna ekleniyor → EBIT'i bozar!
4. Amortisman düzeltilmiş maliyet üzerinden → CapEx vs D&A farkı yanıltıcı
5. BV Equity düzeltilmiş → ROC hesabı etkilenir

### ⚠️ KRİTİK KURAL: Parasal Kazanç/Kayıp

**EBIT'ten ÇIKAR!** Bu operasyonel nakit akışı DEĞİL, muhasebe düzeltmesi.

- Net nakit pozisyonu olan firmalar → parasal KAYIP (enflasyon nakiti eritir)
- Net borçlu firmalar → parasal KAZANÇ (enflasyon borcu eritir)

```python
# KAP XBRL field
monetary_gain_loss = items.get('GainsLossesOnNetMonetaryPosition', {}).get('CURR', 0)

# EBIT düzeltmesi
adjusted_ebit = ebit - monetary_gain_loss  # Çıkar!
```

### İki Yaklaşım

| | Nominal TL | Reel TL (IAS 29) |
|---|---|---|
| Tablolar | Düzeltilmemiş (nominal) | IAS 29 düzeltilmiş |
| Rf | Nominal TL Rf (~%28-31) | Reel Rf (~%2-3) |
| Kd | Nominal (KAP direkt) | **Fisher ile reel'e çevir!** |
| Büyüme | Nominal (enflasyon dahil) | Reel |
| WACC | Nominal (~%35-45) | Reel (~%12-18) |
| Terminal g | ~Rf nominal | ~%3-4 (reel GDP) |

**⚠️ ASLA karıştırma!** Nominal Rf + Reel büyüme = YANLIŞ. Nominal Kd + Reel Ke = YANLIŞ.

**→ Reel Kd dönüşüm formülü ve detaylı tablo:** `methodology/risk_discount.md` §5B

### Fisher Denklemi
```
(1 + nominal) = (1 + reel) × (1 + beklenen_enflasyon)
reel = (1 + nominal) / (1 + π) - 1
```

### Reel FCFF
```
FCFF_reel = (EBIT_düzeltilmiş - Parasal_Kazanç_Kayıp) × (1-t)
          - Reel_Net_CapEx
          - ΔWC_düzeltilmiş
```

### Pratik Sorunlar
- **2022 öncesi karşılaştırma:** Seriler uyumsuz. 2022+ veri kullan veya geriye dönük restate et
- **ÜFE/TÜFE farkı:** IAS 29 Yİ-ÜFE kullanır, TÜFE değil
- **VUK vs TFRS:** VUK enflasyon düzeltmesi ≠ TFRS → efektif vergi oranı sapabilir → 3 yıl ortalama

---

## 2. Country Risk Premium (CRP)

### Hesaplama
```python
from dcf_tools.erp_updater import get_turkey_erp

erp = get_turkey_erp()
# moodys_rating: B3
# country_default_spread: ~%5-6
# country_risk_premium: ~%7-8
# equity_risk_premium: ~%12 (mature + country)
```

### Lambda ile Firma Bazlı

```python
# Firmanın yurtiçi gelir payını bul
domestic_pct = domestic_revenue / total_revenue
avg_domestic_pct = 0.70  # BIST ortalaması (yaklaşık)
lambda_firm = domestic_pct / avg_domestic_pct

Ke = Rf + β × Mature_ERP + λ × Country_ERP
```

### BIST Referans

| Firma | FX Gelir % | λ (yaklaşık) |
|-------|-----------|-------------|
| THYAO | ~75% | 0.35 |
| ASELS | ~60% | 0.55 |
| EREGL | ~50% | 0.70 |
| FROTO | ~45% | 0.75 |
| BIMAS | ~5% | 1.35 |
| AKBNK | ~15% | 1.20 |

### CRP Dinamik Güncelleme
- TR CDS spreadi çok volatil → DCF tarihindeki CDS kullan
- Alternatif: Son 1 yıl ortalama (smoothing)
- Güncelleme: Aylık Damodaran + kriz dönemlerinde haftalık CDS kontrolü

---

## 3. Model Seçimi — FX Bazlı

```
FX Gelir > %70  → USD DCF birincil
FX Gelir < %30  → Reel TL DCF birincil
FX Gelir %30-70 → Dual-track zorunlu
```

### USD DCF
- Gelir/giderleri USD'ye çevir (PPP-bazlı forward kur önerilir)
- USD Rf (~%4.5), USD ERP, USD terminal g (~%2-3)
- Sonucu spot kur ile TL'ye çevir

### Dual-Track Çapraz Kontrol

```python
from dcf_tools.dual_track import dual_track_analysis

result = dual_track_analysis(tl_inputs, usd_inputs, fx_rate=34.0)
# Sapma < %10: Tutarlı ✅
# Sapma %10-25: Uyar ⚠️
# Sapma > %25: Debug 🔴
```

### Kur Varsayımı (USD DCF için)
PPP-bazlı: `Forward = Spot × (1 + TR_π) / (1 + US_π)`

---

## 4. Terminal WACC Override

**Default problem:** Damodaran Terminal WACC = `Rf + Mature_ERP` → Country premium tamamen sıfırlanır.

**TR için ŞART override:**
```
Terminal_WACC = Rf + Mature_ERP + α × Country_ERP
```
- α = 0.3: İyimser (Türkiye 10 yılda gelişmiş piyasa)
- α = 0.5: Baz senaryo
- α = 0.7: Kötümser

---

## 5. BIST Beta Pratiği

XU100 regresyon betası neden güvenilmez:
1. Bankalar ağırlıklı endeks
2. Düşük likidite → fiyat sıçramaları
3. Kur etkisi yapay korelasyon yaratır
4. Düşük R², yüksek standart hata

**Yöntem:** Damodaran Global sektör unlevered beta → firma D/E ile lever et.

---

## 6. Borç Yapısı Dikkat Noktaları

### TL vs FX Borç
Firmalar TL gelir + USD borç yapısına sahip olabilir (kur şoku riski).

- `4BE` (Net Döviz Pozisyonu) kontrol et
- Yüksek FX borç + TL gelir = iflas riski faktörü

### IFRS 16 Lease Ayrımı
KAP XBRL'dan lease vs banka borç ayrıştır:
```python
bank_debt = total_borrowings - lease_liabilities
```
THYAO gibi havayollarında lease borcun %77'sini oluşturabilir.

---

## 7. Döngüsel Sektörler (BIST)

| Firma | Sektör | Emtia | Normalleştirme Referansı |
|-------|--------|-------|--------------------------|
| EREGL | Çelik | HRC | Long-term $500-600/ton |
| TUPRS | Rafineri | Crack Spread | $5-7/bbl |
| SASA | Petrokimya | PTA/MEG | Spread tarihsel ortalama |
| PETKM | Petrokimya | Naphtha | Spread tarihsel ortalama |

7-10 yıl ortalama EBIT marjı kullan. Spot EBIT → yanlış değerleme.

---

## 8. Karar Ağacı

```
Firma analizi başla
│
├── Bankacılık / Sigorta / Finansal?
│   └── EVET → FCFE modeli (Cost of Equity ile)
│
├── Holding?
│   └── EVET → NAV + Holding indirimi (%15-40)
│
├── EPDK Regulated Enerji?
│   └── EVET → RAB modeli + DCF çapraz kontrol
│
├── FX gelir > %70?
│   └── EVET → USD DCF + Reel TL cross-check
│
├── FX gelir < %30?
│   └── EVET → Reel TL DCF + USD cross-check
│
└── FX gelir %30-70
    └── Dual-track zorunlu → sapma analizine göre ağırlıklı ortalama
```
