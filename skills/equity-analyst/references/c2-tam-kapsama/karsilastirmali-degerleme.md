# Karşılaştırmalı Değerleme — Emsal Şirket Metodolojisi

## Felsefe

Göreceli değerleme, İNA'nın (İndirgenmiş Nakit Akışı) tamamlayıcısı — ikisi birlikte güçlü, tek başına her ikisi de tehlikeli. Karşılaştırmalı değerleme "piyasa bugün ne düşünüyor?" sorusuna cevap verir; İNA "gerçek değer ne?" sorusuna. İkisi arasındaki fark yatırım fırsatını doğurur.

---

## 1. Peer Seçimi

### Zorunlu Kriterler (hepsi karşılanmalı)
- **Aynı sektör/alt-sektör** — NACE kodu veya BIST sektör sınıflandırması baz
- **Benzer büyüklük** — Piyasa değeri ±50% aralığında (ideal); ±100% kabul edilebilir
- **Benzer büyüme profili** — Hasılat CAGR farkı <10pp
- **Benzer coğrafya** — Gelir coğrafyası uyumlu (domestic vs export-ağırlıklı)

### Minimum Peer Sayısı
- Yurt içi: 3-5 BIST peer (ZORUNLU)
- **Yurt dışı: 2-3 global peer (ZORUNLU)** — Yahoo Finance / web araştırması ile [v1.4]
- Toplam: Minimum 5-8, ideal 8-10

**KURAL [v1.4]:** Küresel peer OLMADAN comps tablosu TAMAMLANMIŞ sayılmaz. Türkiye piyasası sığ olduğundan, yalnızca yerli peer kullanımı çarpan karşılaştırmasını dar tutar. En az 2 uluslararası eşenik, tabloda "Küresel Peer" başlığı altında ayrıca gösterilmelidir.

**Küresel peer seçimi T1 aşamasında yapılır** (bkz. task1-arastirma.md §13.6). T3'te comps tablosuna eklenir.

### Peer Aday Kaynakları
| Kaynak | Kullanım |
|--------|----------|
| BIST sektör listesi | Yerli peer adayları |
| KAP faaliyet raporu "Rakipler" bölümü | Şirketin kendi tanımladığı rakipler |
| Damodaran Industry Data | Global sektör ortalamaları |
| Yahoo Finance "Similar Companies" | Yurt dışı peer önerileri (ZORUNLU) |
| Kurum raporları (İş Yatırım, Ak Yatırım) | Peer grubu referansı |

### IAS 29 Comps Kuralı (Türkiye-Spesifik)

⚠️ IAS 29 düzeltmeli TL finansalları spot kurla USD'ye çevirip comps yapmak → **YANLIŞ.**

Doğru yaklaşımlar:
1. Şirketin kendi USD raporlaması varsa → onu kullan
2. Yoksa → yıllık ortalama kur ile çevir (gelir tablosu) / dönem sonu kur (bilanço)
3. Her comps tablosunda para birimi ve kur açıkça belirtilir
4. IAS 29 düzeltmeli vs nominal → comps'ta SADECE biri kullanılır, karıştırılmaz

---

## 2. Metrik Seçimi — "5-10 Kuralı"

5 operating metrik + 5 valuation metrik = 10 toplam. Daha fazlası gürültüdür.

### A. Zorunlu Operating Metrikleri (her analizde)

| Metrik | Formül | Neden Önemli |
|--------|--------|-------------|
| Hasılat | Son FY veya TTM | Ölçek göstergesi |
| Hasılat Büyümesi (YoY) | (Hasılat_t / Hasılat_t-1) - 1 | Büyüme hızı |
| Brüt Kâr Marjı | Brüt Kâr / Hasılat | Fiyatlama gücü |
| EBIT Marjı | EBIT / Hasılat | Operasyonel verimlilik |
| ROIC | NOPAT / Invested Capital | Sermaye verimliliği — İlker'in #1 metriği |

### B. Zorunlu Değerleme Metrikleri (her analizde)

| Metrik | Formül | Neden Önemli |
|--------|--------|-------------|
| Piyasa Değeri (PD) | Hisse fiyatı × pay sayısı | Ölçek |
| Firma Değeri (FD) | PD + Net Borç | Borç yapısı dahil |
| FD/Hasılat | FD / Hasılat | Erken aşama veya zarar eden şirketler |
| FD/FAVÖK | FD / FAVÖK | En yaygın göreceli çarpan |
| F/K | Fiyat / Hisse başı kazanç | Kârlı şirketler |

### C. Opsiyonel Metrikler (sektöre göre seç)

| Sektör | Ek Metrikler |
|--------|-------------|
| Her sektör (kalite filtresi) | P/FCF, Net Borç/FAVÖK, FCF Marjı |
| Bankacılık | NFM, KKO, ROE, F/DD, Sermaye Yeterlilik |
| Havacılık | RPK, ASK, Load Factor, Yield, USD Gelir Payı |
| Perakende | m² başı satış, like-for-like growth, mağaza sayısı |
| Telecom | ARPU, Churn, Fiberleşme oranı |
| Bira/İçecek | Pazar payı %, kişi başı tüketim, ÖTV etkisi |
| Çimento | PD/Klinker, ton başı FAVÖK, KKO |
| Otomotiv | KKO, ihracat payı, per-unit EBITDA (EUR) |
| Enerji | MW kapasite, kapasite faktörü, YEKDEM fiyatı |
| Teknoloji/Platform | ARR, NDR, LTV/CAC, Rule of 40 |

→ Detaylı BIST sektör metrikleri: `references/ortak/bist-sektor-metrikleri.md`

---

## 3. Statistical Summary — Zorunlu

Her comps tablosunun altında istatistiksel özet bulunmalı. Bu sadece "ortalama" demek değil — dağılımı gösterir.

### Zorunlu İstatistikler

| İstatistik | Formül | Ne Söyler |
|-----------|--------|-----------|
| Maximum | MAX(range) | En yüksek çarpan |
| 75th Percentile | QUARTILE(range, 3) | "Premium" şirketler burada |
| Median | MEDIAN(range) | Tipik piyasa değerlemesi |
| 25th Percentile | QUARTILE(range, 1) | "İskonto" bölgesi |
| Minimum | MIN(range) | En düşük çarpan |

### Hangi Sütunlara İstatistik Eklenir?

**EVET (karşılaştırılabilir metrikler):**
Revenue Growth %, Gross Margin %, EBITDA Margin %, ROIC, EV/Revenue, EV/EBITDA, P/E, P/FCF, Net Borç/FAVÖK

**HAYIR (ölçek metrikleri — şirket büyüklüğüne göre değişir):**
Revenue ($), EBITDA ($), Net Income ($), Market Cap, EV

### Target Şirketin Konumlandırması

İstatistik bloğunun ardından target şirketin her metrikte hangi quartile'da olduğunu belirt:

```
[ŞİRKET] EV/EBITDA: 8.2x → Medyan (9.5x) altında, 25th percentile (7.8x) yakınında → İskontolu
```

---

## 4. Çıktı Formatı

### Markdown Comps Tablosu

```
## Comparable Company Analysis: [ŞİRKET]
**Tarih:** [YYYY-MM-DD] | **Para birimi:** [TL/USD] | **Kur:** [X.XX TL/USD, kaynak: TCMB dönem ort.]

### Operating Metrikleri
| Şirket | Gelir (mn) | Büyüme % | Brüt Marj | FAVÖK Marjı | ROIC |
|--------|------------|----------|-----------|-------------|------|
| [Target] ★ | X | X% | X% | X% | X% |
| [Peer 1] | X | X% | X% | X% | X% |
| [Peer 2] | X | X% | X% | X% | X% |
| | | | | | |
| **Median** | - | X% | X% | X% | X% |
| **75th** | - | X% | X% | X% | X% |
| **25th** | - | X% | X% | X% | X% |

### Değerleme Çarpanları
| Şirket | PD (mn) | FD (mn) | FD/Hasılat | FD/FAVÖK | F/K | F/SNA |
|--------|---------|---------|----------|----------|-----|-------|
| [Target] ★ | X | X | Xx | Xx | Xx | Xx |
| ... | | | | | | |
| | | | | | | |
| **Median** | - | - | Xx | Xx | Xx | Xx |
```

### Target Pozisyonlama Özeti

```
### [ŞİRKET] Pozisyonlama
- **FD/FAVÖK:** Xx vs medyan Xx → [%] [iskonto/prim]
- **F/K:** Xx vs medyan Xx → [%] [iskonto/prim]
- **Büyüme:** %X vs medyan %X → [üstünde/altında]
- **ROIC:** %X vs medyan %X → [üstünde/altında]

**Sonuç:** [1-2 cümle — iskonto/prim haklı mı, neden?]
```

---

## 5. Veri Kaynakları

| Kaynak | Kullanım | Komut |
|--------|----------|-------|
| BBB Finans (BIST birincil) | Yerli peer finansallar | `python3 bbb_financials.py {TICKER} --section all --full` |
| Yahoo Finance (yurt dışı) | Global peer | `python3 bbb_yfinance.py fundamentals {TICKER}` |
| Damodaran Industry Data | Sektör ortalamaları | `web_fetch` → pages.stern.nyu.edu |
| Şirket bilgileri | Pay sayısı (2OA), Market Cap (fiyat×pay) | `bbb_financials.py {TICKER} --section balance` (2OA) + `bbb_financials.py {TICKER} --price` (son kapanış) |

---

## 6. Sık Yapılan Hatalar

| Hata | Sonuç | Çözüm |
|------|-------|-------|
| IAS 29 TL'yi spot kurla USD comps | Şişirilmiş çarpanlar | Yıllık ort. kur veya şirketin kendi USD raporlaması |
| Farklı dönemler karıştırma | Yanıltıcı karşılaştırma | Tüm peer'lar aynı FY veya TTM |
| Çok az peer (<3) | İstatistiksel anlamsızlık | Min 4-5 peer |
| Ölçek metriklere istatistik | Saçma ortalamalar | Sadece oran/çarpan metriklerine istatistik |
| **EV hesabında FX karıştırma** | **Tutarsız çarpanlar** | **Aşağıdaki 6A kurallarını uygula** |

### 6A. EV Hesaplamasında FX Harmonizasyonu 🔴 KRİTİK

Farklı para birimindeki peer'ları karşılaştırırken EV bileşenlerinde **3 farklı kur** kullanma riski vardır:
- Market Cap → spot kur
- Net Borç → dönem sonu kur
- EBITDA → yıllık ortalama kur

Bu tutarsızlık EV/EBITDA çarpanını çarpıtır.

**BBB DOĞRU YAKLAŞIM — Yerel Para Biriminde Çarpan:**

```
KURAL: Çarpanları YEREL para biriminde hesapla, kur dönüşümünü ÇIKTIYA uygula.

ADIM 1: Her peer'ın çarpanını KENDİ para biriminde hesapla
  - BIST şirketi: TL EV / TL EBITDA = X.Xx (kur dönüşümü YOK)
  - Global peer: USD EV / USD EBITDA = Y.Yx (kur dönüşümü YOK)
  - Çarpan birimsizdir (X.Xx) → doğrudan karşılaştırılabilir ✅

ADIM 2: Peer medyan çarpanını hedef şirketin KENDİ metriğine uygula
  - Peer medyan EV/EBITDA = 12.5x
  - Hedef şirket TL EBITDA = 3.540 mn TL
  - İma edilen TL EV = 12.5 × 3.540 = 44.250 mn TL (TL bazında, kur yok)

ADIM 3: Equity değerine çevir (tamamı TL)
  - TL Equity = TL EV - TL Net Borç
  - Hisse başı değer = TL Equity / Pay sayısı

YANLIŞ: TL EBITDA'yı USD'ye çevirip → USD peer medyan EV/EBITDA uygulamak
  → Market Cap zaten TL → EV'de kur karışır
```

**ÖZEL DURUM — Gelir tablosu vs Bilanço FX kuralı:**
```
Eğer comps tablosunda para birimi DÖNÜŞÜMÜ yapılacaksa:
  - Gelir tablosu kalemleri (Hasılat, EBITDA): Dönem ortalama kuru
  - Bilanço kalemleri (Varlık, Borç, Nakit): Dönem sonu kuru
  - Market Cap: Spot kur (güncel fiyat)
  - Bu 3 farklı kur AÇIKÇA belirtilmeli (tablo dipnotunda)

  Dipnot örneği: "USD dönüşümlerinde: Gelir tablosu kalemleri 2025 yıllık ortalama
  kuru (32.15 TL/USD), bilanço kalemleri dönem sonu kuru (34.80 TL/USD) kullanılmıştır."
```
| Negative EBITDA + EV/EBITDA | Anlamsız çarpan | EV/Revenue kullan, dipnot ekle |
| Holding + operating company karıştırma | Yanlış peer grubu | Holding → holding peer'ları, operating → operating |

---

## 7. Sanity Checks (Comps Tamamlandıktan Sonra)

| Check | Ne Sor | Red Flag |
|-------|--------|----------|
| **Tarihsel çarpan kontrolü** | Target şirket kendi tarihsel aralığına göre nerede? | 5Y aralığının dışında → açıkla neden |
| **Büyüme-çarpan tutarlılığı** | Yüksek büyüme + düşük çarpan → neden iskonto? | Düşük büyüme + yüksek çarpan → balonlu mu? |
| **Marj-çarpan tutarlılığı** | Yüksek marj genellikle yüksek çarpanı destekler | Yüksek marj + düşük çarpan = fırsat mı, risk mi? |
| **Implied growth check** | Mevcut çarpan hangi büyümeyi fiyatlıyor? | Mantıksız büyüme varsayımı → piyasa yanlış veya biz yanlışız |
| **Peer heterojenliği** | Peer'lar birbirine ne kadar benzer? | Dispersiyon çok yüksekse → peer grubu zayıf, daha homojen alt-grup seç |
| **Cross-reference kuralı** | Valuation çarpanları operating metric'lerle tutarlı mı? | Yüksek EV/EBITDA ama düşük ROIC → fiyatlama hatalı olabilir |

---

## 8. Premium/İskonto Gerekçelendirme Çerçevesi

Comps tablosundan çıkan sonuç → "prim/iskonto haklı mı?" sorusuna cevap VERİLMELİ:

**Prim haklı olabilir (peer medyanın üzerinde çarpan):**
- Daha yüksek büyüme oranı (ve sürdürülebilir)
- Daha güçlü moat (marka, patent, veri tekeli)
- Daha iyi sermaye tahsisi geçmişi (yüksek ROIC)
- Katalist (ürün lansmanı, pazar genişlemesi)
- Daha iyi yönetim kalitesi

**İskonto haklı olabilir (peer medyanın altında çarpan):**
- Düşük büyüme veya daralma
- Zayıf moat veya artan rekabet
- Yüksek kaldıraç (borç riski)
- Ülke riski (Türkiye CRP, IAS 29 belirsizliği)
- Düzenleyici risk (aktif soruşturma, lisans belirsizliği)
- Likidite iskontosu (düşük free float)

**İskonto haklı DEĞİLSE → fırsat.** İskonto haklıysa → value trap riski.

---

## 9. Büyüme Düzeltmeli Comps (Growth-Adjusted Comps) — ZORUNLU

**Neden zorunlu:** Basit FD/FAVÖK veya F/K çarpanları büyüme farklarını görmezden gelir. Yüksek büyüme gösteren bir şirketin FD/FAVÖK'ü yüksek olabilir ama büyümeye göre düzeltildiğinde aslında ucuz olabilir. MS/JPM raporlarında "PEG ratio" ve "EV/EBITDA/Growth" standart göstergelerdir.

### Zorunlu Büyüme Düzeltmeli Metrikler

| Metrik | Formül | Yorumlama |
|--------|--------|-----------|
| PEG Oranı | (F/K) / (YoY EPS Büyümesi %) | <1.0 = ucuz, 1.0-1.5 = makul, >2.0 = pahalı |
| FD/FAVÖK/Büyüme | (FD/FAVÖK) / (FAVÖK CAGR %) | <0.5 = ucuz, 0.5-1.0 = makul, >1.5 = pahalı |
| Forward PEG | (Forward F/K) / (Forward EPS Büyümesi %) | Forward verilere dayalı — daha ileri bakan |
| Rule of 40 | Gelir Büyümesi + FAVÖK Marjı | Teknoloji/SaaS için — >40 = iyi |

### Büyüme Düzeltmeli Comps Tablosu Formatı

```markdown
### Büyüme Düzeltmeli Değerleme — {TICKER}

| Şirket | FD/FAVÖK | FAVÖK Büyüme (%) | FD/FAVÖK/Büyüme | F/K | EPS Büyüme (%) | PEG |
|--------|----------|-----------------|-----------------|-----|----------------|-----|
| {TICKER} | Xx | %X | X.Xx | Xx | %X | X.Xx |
| [Peer 1] | Xx | %X | X.Xx | Xx | %X | X.Xx |
| [Peer 2] | Xx | %X | X.Xx | Xx | %X | X.Xx |
| ... | | | | | | |
| **Medyan** | Xx | %X | X.Xx | Xx | %X | X.Xx |

### Büyüme Düzeltmeli Pozisyonlama
- **FD/FAVÖK/Büyüme:** {TICKER} X.Xx vs medyan X.Xx → [ucuz/pahalı]
- **PEG:** {TICKER} X.Xx vs medyan X.Xx → [ucuz/pahalı]
- **Sonuç:** Basit çarpanlar {TICKER}'ın [iskontolu/primli] gösteriyor ama büyüme düzeltildiğinde [daha ucuz/daha pahalı/aynı]
```

### PEG Kısıtlamaları ve Dikkat Noktaları

| Durum | Sorun | Çözüm |
|-------|-------|-------|
| Negatif EPS büyümesi | PEG negatif → anlamsız | PEG hesaplanmaz, dipnot düş |
| Çok düşük büyüme (<3%) | PEG şişer | FD/FAVÖK/Büyüme tercih et |
| Döngüsel sektörler | Büyüme dönem bağımlı | 3Y CAGR kullan, son yıl değil |
| IAS 29 şirketleri | Reel/nominal büyüme karışıklığı | REEL büyüme kullan, para birimi belirt |
| Zarar eden şirketler | F/K ve PEG anlamsız | FD/Hasılat/Büyüme alternatif |

### Comps Hedef Fiyatına Entegrasyon

Büyüme düzeltmeli çarpanlar basit çarpanlarla çelişiyorsa:
1. Her iki yöntemle ayrı hedef fiyat hesapla
2. Farkın nedenini açıkla (büyüme primi haklı mı?)
3. Ağırlıklandırmada büyüme düzeltmeli çarpanlara %60, basit çarpanlara %40 ağırlık ver (büyüme profili net olan şirketlerde)

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-17 | v1.0 oluşturuldu |
| 2026-03-17 | v1.1 — Sanity checks (6 kontrol), premium/iskonto gerekçelendirme çerçevesi eklendi |
| 2026-03-22 | v1.2 — Büyüme düzeltmeli comps (PEG, FD/FAVÖK/Büyüme, Rule of 40) eklendi |
| 2026-03-22 | **v1.3** — §6A eklendi: EV Hesaplamasinda FX Harmonizasyonu — carpanlar yerel para biriminde, kur donusumu sadece ciktida. Hata tablosuna "EV FX karistirma" satiri eklendi |
| 2026-03-23 | **v1.4** — Küresel peer ZORUNLU hale getirildi: en az 2-3 uluslararası peer, "Küresel Peer" başlığı altında comps tablosuna eklenir. Toplam minimum 5-8 peer (yerli + küresel). T1 §13.6 ile cross-reference |
