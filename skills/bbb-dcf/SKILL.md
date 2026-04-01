---
name: bbb-dcf
description: >-
  Aswath Damodaran metodolojisiyle BIST ve uluslararası hisseler için DCF (İndirgenmiş Nakit Akışı)
  değerleme modeli oluşturur. IAS 29 enflasyon muhasebesi uyumlu, TL/USD tutarlılık kontrollü.
  Kullan: hisse değerlemesi yap, DCF modeli kur, intrinsic value hesapla, WACC hesapla, terminal
  value belirle. Kaya (Analist) bu skill'i kullanır. equity-analyst ile birlikte çalışır.
---

# DCF Değerleme Skill'i

**Versiyon:** 1.0 | **Sahip:** Kaya | **Kaynak:** Aswath Damodaran Valuation (224 slide + Excel + YouTube)

---

## 0. Temel İlkeler

- **Rasyonel analiz.** Ne tutkulu, ne kötümser. Her veri, her varsayım teyit edilmeli.
- **Ownership Verification:** Ortaklık yapısı birincil kaynaktan (KAP, faaliyet raporu, IR sayfası) doğrulanır. Marka adından sahiplik çıkarımı YAPMA. Doğrulanana kadar **[DOĞRULANMADI]** etiketi kullan. *(TBORG kazanımı)*
- **Veri hiyerarşisi:** KAP birincil, İş Yatırım fallback. StockAnalysis/TradingView/Investing.com'dan finansal veri alınmaz.
  → Detaylı hiyerarşi, komutlar, API tablosu: `references/data_sources.md`
- **Türkçe çıktı:** İlk kullanımda kısaltma + Türkçe parantez. → Sözlük: `references/term_glossary.md`

### TTM (Son 12 Ay) Yıllıklandırma — ZORUNLU

Son çeyrek verisi varsa, son 4 çeyreğin GERÇEK toplamı hesaplanır:
```
Kümülatif: TTM = Son Kümülatif Dönem + (Önceki FY - Önceki Yılın Aynı Kümülatif Dönemi)
Çeyreklik: TTM = Q4 + Q1 + Q2 + Q3
Bilanço: TTM hesaplanmaz — son çeyrek sonu bilanço değeri kullanılır.
```
Bu "tahmin" veya "çarparak yıllıklandırma" DEĞİLDİR — gerçek 4 çeyrek verisi toplanır.

### IAS 29 Ülkeleri Veri Kuralı

- Türk şirketleri için IAS 29 düzeltmeli veri seti kullanılır *(İlker talimatı)*
- Nominal veriler SADECE cross-check için
- **TRY IAS 29 düzeltmeli finansalları spot kurla bölüp USD'ye çevirme → YASAK**
- KAP Özet (`--kap-summary`) = IAS 29 düzeltmeli (birincil). BBB Finans Detaylı (`--full`) = Nominal (cross-check).

---

## 0A. Yaygın Hatalar — Özet

Her DCF'te bu listeyi gözden geçir. → **Detaylı açıklamalar:** `references/common_errors.md`

1. **IAS 29 Tuzağı** — IAS 29 TL'yi spot kurla USD'ye çevirme = YANLIŞ
2. **Sentetik Kd Tuzağı** — ICR'da kur farkı dahil etme, sadece gerçek faiz gideri
3. **Kaynak olmadan rakam** — HER ZAMAN BBB Finans veya KAP'tan doğrulanmış veri
4. **S/C tahmin etme** — Sales/Capital hesaplanır, tahmin edilmez
5. **Rf düzeltmesi** — ABD Aa1 default spread çıkar (Rf = 10Y - ~0.23%)
6. **Baz yıl karmaşası** — İş Yatırım vs KAP farklı IAS 29 bazları, USD'de convergence
7. **Currency-Consistent** — WACC, büyüme, terminal g aynı para birimi enflasyonunu yansıtmalı. Fisher cross-check zorunlu.
8. **Peer bulunamadı → araştır** — Birleşme, isim değişikliği, delist kontrolü
9. **CRP tek yaklaşım** — Rating + CDS ikisini de hesapla, blended öner
10. **Fazlar arası tutarsızlık** — Aynı parametreler tüm fazlarda kullanılmalı
11. **Piyasa altı DCF = red flag** — Muhafazakâr varsayımları sorgula
12. **β_U nakit düzeltmeli** — Çift sayımı önle
13. **Capex normalizasyonu** — Gerçek capex/revenue'yu kontrol et, model düşük alıyorsa FCFF şişer
14. **Terminal WACC override unutma** — TR firmaları default'ta CRP sıfırlanır → override ŞART

---

## 0B. DCF Checklist — Her Hesaplama Öncesi

- [ ] Hisse fiyatı BBB Finans'tan mı?
- [ ] Döviz kuru TCMB'den mi?
- [ ] Pay sayısı ödenmiş sermaye ile cross-check edildi mi?
- [ ] Gelir/EBIT şirketin kendi USD raporlamasından mı? (IAS 29 ülkeleri)
- [ ] Parasal Kazanç/Kayıp EBIT'ten çıkarıldı mı? (IAS 29 düzeltmeli tablolarda)
- [ ] Toplam borç KAP bilançosundan mı? (IFRS 16 dahil mi, belirt)
- [ ] β_U nakit düzeltmeli mi?
- [ ] Rf ABD default spread çıkarılmış mı?
- [ ] Kd gerçek rating bazlı mı? (sentetik sadece cross-check)
- [ ] S/C hesaplandı mı? (tahmin değil)
- [ ] CDS verisi güncel mi? (tarih belirt)
- [ ] Tüm parametreler fazlar arasında tutarlı mı?
- [ ] Fisher cross-check planlandı mı? (TL hedef ≈ USD hedef × kur, sapma <%15)

---

## 1. Kullanım

| Senaryo | Çıktı |
|---------|-------|
| "{TICKER} değerle" | Tam DCF raporu |
| "Hedef fiyat hesapla" | DCF + sensitivity |
| "NAV analizi yap" | Holding NAV + DCF |
| "Ucuz mu pahalı mı?" | DCF + göreceli karşılaştırma |

### İki Mod

**🔬 Kaya Modu:** Tüm verileri kendisi toplar, varsayımları oluşturur, modeli çalıştırır.
**🎯 Kullanıcı Modu:** Kullanıcı varsayımlarını girer (büyüme, marj, WACC, terminal g), Kaya hesaplar.

---

## 2. Değerleme Adımları

### Adım 1: Firma Tipi Belirle
- Banka/Sigorta → FCFE modeli (`methodology/dcf_deep_dive.md`)
- Holding → NAV + indirim (`methodology/special_cases.md`)
- Regulated Enerji → RAB modeli
- Diğer → FCFF modeli (bu skill'in ana akışı)

### Adım 2: Veri Topla
KAP'tan son 2 yıl + piyasa verisi + Damodaran referanslar. → `references/data_sources.md`

### Adım 3: Temel Hesaplamalar
```
IC = BV_Equity + BV_Debt - Cash              # Temel
IC = BV_Equity + BV_Debt - Cash + R&D_Asset  # R&D varsa (bkz special_cases.md)
S/C = Revenue / IC
ETR = max(0, Tax / EBT)                      # Negatif EBT → ETR = 0
ICR = EBIT / Interest_Expense                # Sadece gerçek faiz gideri (kur farkı HARİÇ)
```

### Adım 4: WACC Hesapla
→ Detay: `methodology/risk_discount.md` | Formüller: `references/formula_card.md`
```
β_L = β_U × (1 + (1-t) × D/E)
Ke = Rf + β_L × Mature_ERP + λ × Country_ERP
Kd = Rf + Country_Default_Spread + Company_Spread
WACC = Ke × (E/V) + Kd × (1-t) × (D/V)
```

### Adım 5: 10 Yıllık Projeksiyon
→ Detay: `methodology/dcf_deep_dive.md`
- Y1: Analist büyüme + mevcut marj
- Y2-5: CAGR büyüme, marj yakınsama
- Y6-10: Lineer interpolasyon → terminal parametrelere

### Adım 6: Terminal Value
```
RR_terminal = g / ROC_terminal
TV_FCFF = EBIT_10 × (1-t) × (1 + g) × (1 - g/ROC)
TV = TV_FCFF / (WACC_terminal - g)
```
**⚠️** ROC = WACC ise büyüme değer yaratmaz. ROC > WACC = moat.

### Adım 7: Equity Bridge
```
PV(10yr FCFF) + PV(Terminal Value)
× (1 - P_failure) + Distress_Proceeds × P_failure
- Total_Debt - Minority_Interests + Cash + Cross_Holdings - Employee_Options
= Equity_Value ÷ Shares = Value_per_Share
```

### Adım 8: Fisher Cross-Check — ZORUNLU
TL ve USD DCF sonuçları karşılaştırılır:
```
Sapma = |TL_Value/Kur - USD_Value| / Average
  <%10 → Tutarlı ✅  |  %10-15 → Uyar ⚠️  |  >%15 → Parametreleri gözden geçir 🔴
```
Dual-track yapılmıyorsa bile, en az bir basit Fisher check: `TL_hedef ≈ USD_hedef × spot_kur`.

### Adım 9: Sanity Check & Sensitivity
→ Çıktı formatı: `templates/output_format.md`

---

## 3. Türkiye Özel Kurallar — Özet

→ **Detaylı hesaplamalar ve tablolar:** `references/turkey_special.md`

- **IAS 29:** Parasal Kazanç/Kayıp → EBIT'ten çıkar. Nominal Rf + reel büyüme karıştırma!
- **CRP:** Damodaran'dan hazır alınmaz, formülle hesaplanır: `CRP = Default_Spread × σ_E/σ_B (1.5234)`. Rating + CDS iki yaklaşım zorunlu.
- **FX model seçimi:** >%70 USD/EUR → USD DCF | <%30 → TL | %30-70 → Dual-track
- **Holding indirimi:** Baz %20-25 + ek faktörler (HAO, kontrol, IR kalitesi)
- **Time-Varying WACC:** Enflasyon >10pp değişecekse yıllık WACC hesapla
- **HAO indirimi:** Equity bridge'de ayrı satır, WACC'a eklenmez
- **Management filter:** 3 seviyeli güven skoru, direkt kullanma

---

## 4. Tarihsel Analiz & Peer Karşılaştırma — ZORUNLU

**Varsayımlar belirlenmeden ÖNCE yapılmalı:**

- [ ] **Gelir büyümesi:** Son 5-10Y YoY + CAGR (3Y, 5Y, 10Y). Projeksiyon farkı gerekçelendirilmeli.
- [ ] **EBIT marjı:** Son 5-10Y trendi, ortalama + medyan. Hedef marjı bu veriye dayandır.
- [ ] **Peer karşılaştırma:** Min 4-5 peer (yerli + yabancı). Metrikler: Gelir, EBIT Marjı, EV/EBITDA, S/C, ROIC.
- [ ] **Sektör analizi:** S/C sektör ortalaması, büyüme oranları, rekabet yapısı.
- [ ] **Döviz kuru belgeleme:** Gelir tablosu → dönem ortalama kur, bilanço → dönem sonu kur. Kaynak explicit.
- [ ] **Kredi notu:** KAP gerçek S&P/Moody's/Fitch (birincil) vs synthetic (cross-check).
- [ ] **Beta cross-check:** Bottom-up β_U (birincil) vs regression β (cross-check). Fark açıklanır.
- [ ] **ERP & CRP:** Formülden hesaplanır. → Detaylı adımlar: `references/turkey_special.md`

---

## 5. Diagnostics — 17 Damodaran Sorusu

Her DCF tamamlandıktan SONRA 17 soru TEK TEK cevaplanır.
→ **Tam soru listesi:** `references/diagnostics_17q.md`

**Kapsam:** Gelir büyümesi (S1-6), marj (S7-9), yeniden yatırım (S10-12), tutarlılık (S13-14), sermaye maliyeti (S15-17).

Cevaplar varsayımlarla çelişiyorsa → varsayımlar revize edilmeli → model yeniden çalıştırılmalı.
Bu "checklist doldur geç" değil — **gerçek bir gözden geçirme süreci.**

---

## 6. Kalite Kontrol

| Kontrol | Kırmızı Bayrak | Aksiyon |
|---------|----------------|---------|
| Terminal Value Ağırlığı | >%90 | Projeksiyon dönemini uzat |
| Terminal Growth ≥ WACC | Her zaman | ENGELLE |
| Terminal Growth > Rf | Tehlikeli | Uyar, neden sor |
| Negatif FCFF tüm yıllar | Dikkat | Revenue-based büyüme modeli |
| ROC < WACC terminal | Büyüme zararlı | g=0 veya negatif düşün |
| Invested Capital < 0 | Net cash | ROC anlamsız, uyar |
| ETR < 0 | Vergi kazancı | ETR = 0 al |

**Edge case'ler:** Negatif EBIT → Vergi=0, NOL birikir. Negatif BV Equity → geçerli (buyback). Sıfır faiz → ICR=∞ → AAA. Lease çift sayım → IFRS 16 kontrol.

---

## 7. Cross-Agent Entegrasyon

→ **Detaylı API tablosu:** `references/cross_agent_api.md`

**Kritik modüller:** `dcf_tools/wacc.py` (tam WACC pipeline), `dcf_tools/projection_engine.py` (10Y projeksiyon + equity bridge), `dcf_tools/beta_lookup.py` (95 sektör, fuzzy match), `dcf_tools/synthetic_rating.py` (ICR → rating → spread).

---

## 8. Dosya Yapısı

```
skills/bbb-dcf/
├── SKILL.md                          ← Bu dosya (workflow + core kurallar)
├── methodology/                      ← Teorik derinlik
│   ├── valuation_approaches.md       # 3 değerleme yaklaşımı
│   ├── dcf_deep_dive.md              # FCFF vs FCFE, TV, projeksiyon
│   ├── risk_discount.md              # Beta, WACC, CRP
│   ├── growth_estimation.md          # Büyüme tahmini
│   ├── special_cases.md              # R&D, lease, iflas, holding
│   └── turkey_adjustments.md         # IAS 29, CRP, dual-track
├── templates/                        ← Boş şablonlar
│   ├── dcf_template.md
│   ├── input_checklist.md
│   └── output_format.md
├── examples/
│   └── thyao_example.md              # THYAO örnek DCF
└── references/                       ← Detay referanslar (gerektiğinde oku)
    ├── formula_card.md               # Tüm formüller
    ├── industry_data.md              # Sektör ortalamaları
    ├── country_erp.md                # Ülke risk primleri
    ├── data_sources.md               # Veri hiyerarşisi, komutlar, API tablosu
    ├── common_errors.md              # 12 yaygın hata detaylı açıklama
    ├── turkey_special.md             # CRP, holding, HAO, WACC, management filter
    ├── diagnostics_17q.md            # 17 Damodaran sorusu tam metin
    ├── term_glossary.md              # Türkçe terim sözlüğü
    ├── cross_agent_api.md            # Can'ın DCF tools API tablosu
    └── data_pack_template.md         # Faz 1 DATA_PACK şablonu
```

---

## 9. Multi-Phase Execution Protocol — ZORUNLU

> Tek session'da tamamlanmaya çalışılMAZ. THYAO deneyiminden öğrenilen dersler.

### Akış

```
Faz 0: Ön Karar → Para birimi, firma tipi, model seçimi
  ↓
Faz 1: Veri & Araştırma → {TICKER}_DATA_PACK.md (Kaya — Opus)
  ↓    → Detaylı şablon: references/data_pack_template.md
Faz 1.5: Parametre Onayı → 7 Tutarlılık Kontrolü (ZORUNLU) → İlker onay/revizyon → KİLİTLE
  ↓    → Kontrol detayları: references/data_pack_template.md §FAZ 1.5
  ↓    → Kontrol 6: Çelişki Matrisi doğrulaması (equity-analyst T3'ten)
  ↓
Faz 2: Değerleme → {TICKER}_VALUATION.md (Kaya — Opus)
  ↓    KİLİTLİ parametrelerle: WACC → 10Y projeksiyon → TV → Equity Bridge → Sensitivity
  ↓    ⚠️ TEK değerleme noktası — başka fazda hesap YOK
  ↓    ⚠️ Fisher cross-check Faz 2 ÇIKTISI: TL hedef ≈ USD hedef × kur (sapma <%15)
Faz 3: Diagnostics & Review → {TICKER}_FINAL_REPORT.md (Kaya — Opus)
       17 Damodaran sorusu + sanity check. Gerekirse revizyon + yeniden hesaplama.
```

### 6 Temel Kural

1. **Faz Ayrımı Zorunlu** — 4+1 faz (0, 1, 1.5, 2, 3). Tek session'da tamamlanmaya çalışılMAZ.
2. **Parametre Kilidi** — Faz 2'ye girilmeden önce tüm varsayımlar onaylanır. Faz 2 sırasında DEĞİŞTİRİLMEZ.
3. **Dosya-Tabanlı İletişim** — Her faz çıktısını dosyaya yazar. Sonraki faz SADECE dosyadan okur.
4. **Tek Değerleme Noktası** — Nihai DCF hesabı TEK fazda (Faz 2) yapılır.
5. **Para Birimi Tutarlılığı** — Faz 0'da belirlenen para birimi değişmez.
6. **Cross-Check Zorunluluğu** — En az 3: (a) Implied EV/EBITDA vs peer, (b) Implied P/E vs peer, (c) Fisher cross-check (TL ≈ USD × kur). Önerilen: Reverse DCF.

### Orchestrator (Odesus) Sorumlulukları
- **Faz 0:** Para birimi ve firma tipi kararı
- **Faz 1 → 1.5:** DATA_PACK'i oku, varsayım setini İlker'e sun, onay al
- **Faz 2 → 3:** VALUATION.md'ye hafif review, Faz 3'ü tetikle
- **Faz 3 sonrası:** FINAL_REPORT'u İlker'e sun

---

## 10. Skill Geliştirme Döngüsü — ZORUNLU (2026-03-09)

> Her DCF çalışması bu skill'i öğretiyor. Compound learning: skill iyileşirse sonraki analiz daha iyi.

**Kaya, her DCF çalışmasının sonunda şunu yapar:**

1. `skills/skill-creator/SKILL.md` oku
2. Bu skill'i skill-creator rehberiyle değerlendir:
   - Yeni pattern keşfedildi mi? → SKILL.md veya ilgili `references/` dosyasına ekle
   - Hata yapıldı mı? → `references/common_errors.md`'ye ekle (#N+1)
   - Yeni veri kaynağı/komut keşfedildi mi? → `references/data_sources.md`
   - ERP/WACC/kur varsayımı güncellendi mi? → `references/country_erp.md` veya `methodology/risk_discount.md`
   - Türkiye'ye özgü yeni durum mu? → `references/turkey_special.md`
3. Aşağıdaki **BBB Öğrenmeler** bölümüne kayıt düş

**Kural:** Bu adım atlanırsa DCF çalışması tamamlanmış SAYILMAZ (SOUL.md Skill Geri Bildirim Döngüsü).

---

## BBB Öğrenmeler

<!-- Format: - [YYYY-MM-DD] [agent] Bulgu açıklaması -->
- [2026-03-09] Kaya: Skill review tamamlandı — ERP tutarsızlığı (3 dosya → country_erp.md kanonik kaynak), Fisher cross-check 4 noktaya eklendi, output_format.md 84 satır duplikasyon temizlendi, common_errors.md #13-#14 eklendi.
