# Türkiye-Spesifik Analiz Rehberi

> BIST hisse analizinde global framework yeterli değildir. Bu rehber Türkiye'ye özgü analitik araçları,
> düzeltmeleri ve çerçeveleri tanımlar. Her BIST analizi öncesinde bu dosyanın ilgili bölümü kontrol edilmelidir.
>
> **IAS 29 kuralları:** Bu dosyada değil → `task2-finansal-modelleme.md` Adım 7
> **CRP hesaplama:** Bu dosyada değil → bbb-dcf/SKILL.md + bbb-dcf/references/country_erp.md

---

## 1. Türkiye İskontosu — Kantitatif Çerçeve

### Sorun

BIST hisseleri gelişmiş piyasa eşdeğerlerine göre sistematik iskontoda işlem görür. Medyan EV/EBITDA 5-7x (BIST) vs 10-14x (S&P 500 / Euro Stoxx). Bu iskonto ne kadar haklı, ne kadar aşırı?

### İskonto Bileşenleri

| Bileşen | Ölçüm Aracı | Güncel Veri Kaynağı | Etki |
|---------|-------------|-------------------|------|
| **Ülke riski (CDS spread)** | 5Y CDS spread (bp) | web_search: "Turkey CDS 5 year" | Doğrudan Ke'ye eklenir (CRP) |
| **Hukukun üstünlüğü** | World Justice Project Rule of Law Index | web_fetch: worldjusticeproject.org | Uzun vadeli yabancı yatırım iştahı |
| **MSCI sınıflandırması** | EM (Emerging Market) | MSCI country classification | Pasif fon akışı |
| **Kur volatilitesi** | TRY/USD 1Y realized vol | TCMB, investing.com | Yabancı yatırımcı için return uncertainty |
| **Enflasyon rejimi** | TÜFE yıllık | TÜİK | Reel getiri belirsizliği |
| **Sermaye kontrolleri riski** | Tarihsel kısıtlamalar | Algısal — CDS'e yansır | Kapital çıkış riski |

### Kantitatif İskonto Tahmini

```
Türkiye İskontosu ≈ f(CDS Spread, Enflasyon Farkı, Hukukun Üstünlüğü Skoru)

Basit yaklaşım:
  Peer Medyanı EV/EBITDA × (1 − İskonto %) = BIST Makul EV/EBITDA

  İskonto % ≈ CDS Spread (bp) / 100 × Katsayı
  Katsayı: Tarihsel kalibrasyon ile belirlenir (~0.08-0.12)

Pratik kural:
  CDS < 250bp → İskonto %15-25 (EM ortalaması)
  CDS 250-500bp → İskonto %25-40 (Yüksek ülke riski)
  CDS > 500bp → İskonto %40-60 (Kriz rejimi)
```

### Analiz İçin Kullanım

Comps tablosunda BIST hissesi yurt dışı peer'lara göre "ucuz" çıktığında şu soru sorulur:

> "Bu iskonto Türkiye iskontosu mu (haklı), yoksa şirkete özgü undervaluation mı (fırsat)?"

**Test:**
1. Aynı sektörün diğer BIST hisselerinin iskontosu ne? (sektör medyanı)
2. Şirket sektör medyanından da iskontoluysa → şirkete özgü fırsat olabilir
3. Şirket sektör medyanına paralelse → Türkiye iskontosu, şirkete özgü fırsat yok

**İlker'in görüşü:** *"Uzun vadeli yabancı yatırımın artması, kurumsal yönetişim ve hukukun üstünlüğüne dair somut adımlar gerekiyor. Cevap hukukun üstünlüğü endeksiyle doğrudan alakalı."*

---

## 2. Holding NAV İskontosu Çerçevesi

### Kapsam

BIST'te 15+ holding: SAHOL, KCHOL, DOHOL, NTHOL, TAVHL, GLYHO, KOZAL, ECZYT ve diğerleri.
Her birinin piyasa fiyatı NAV'ın (Net Varlık Değeri) altında işlem görür — bu "holding iskontosu" evrensel bir fenomen ama Türkiye'de genellikle daha derin.

### NAV Hesaplama (SOTP Temelli)

```
NAV = Σ (İştirak Piyasa Değeri × Sahiplik Payı) + Net Nakit − Net Borç − Holding Giderleri BD

Her iştirak için:
  - Borsada işlem görüyorsa → Piyasa değeri (tarih belirtilmeli)
  - Borsada yoksa → Comps ile tahmin veya son M&A işlemi baz alınır
  - Operasyonel varsa → DCF veya EV/EBITDA ile değerle

NAV İskontosu = (NAV − Holding PD) / NAV × 100
```

### İskonto Nedenleri (6 Faktör)

| # | Faktör | Ölçüm | Derin İskonto (→↑) | Sığ İskonto (→↓) |
|---|--------|-------|--------------------|--------------------|
| 1 | **Transparanlık** | IR kalitesi, segment raporlama | Zayıf raporlama | Detaylı segment raporu |
| 2 | **Temettü Politikası** | Temettü / NAV yield | Düşük veya düzensiz | Yüksek ve istikrarlı |
| 3 | **Yönetim Kalitesi** | Track record, sermaye tahsisi | Kötü M&A geçmişi | Değer yaratan M&A |
| 4 | **Konglomera Karmaşıklığı** | Segment sayısı, iş modeli farkı | 10+ farklı sektör | 2-3 odaklı sektör |
| 5 | **Likidite** | Holding hissesi vs iştiraklerin likiditesi | Düşük free float | Yüksek free float |
| 6 | **Çifte vergilendirme** | İştirak temettüsü → holding → hissedar | Evet (yapısal) | Vergi avantajlı yapı |

### BIST Holding İskontoları (Tarihsel Referans)

| Holding | Tipik İskonto Aralığı | Temel Neden |
|---------|----------------------|-------------|
| SAHOL | %25-40 | Konglomera karmaşıklığı (banka + enerji + sanayi + telecom) |
| KCHOL | %20-35 | Güçlü marka ama çeşitlilik yüksek |
| DOHOL | %30-50 | Likidite düşük, segment karmaşık |
| NTHOL | %35-55 | KKTC risk primi, lisans volatilitesi |
| TAVHL | %15-30 | Operasyonel odaklı (TAV Havalimanları), daha şeffaf |

**Kaynak:** Bu oranlar genel piyasa gözlemi — her analiz için güncel NAV hesaplanmalı.

### Holding Analizi Workflow

1. **NAV hesapla** — her iştirak ayrı değerlendir
2. **İskonto hesapla** — mevcut PD vs NAV
3. **6 faktörle karşılaştır** — iskonto haklı mı?
4. **Katalizör ara** — iskonto ne zaman kapanır? (IPO, spin-off, temettü politikası değişikliği, varlık satışı)
5. **Comps:** Türk holdingler kendi aralarında + global holdingler (Berkshire, CK Hutchison, Jardine Matheson)

---

## 3. Türk Bankacılık Analiz Çerçevesi

### Standart Framework Neden Çalışmaz

Bankalar için ROIC, FCF, EV/EBITDA anlamsızdır. Banka "ürünü" paradır — aktif ve pasif yapısı geleneksel sanayi şirketlerinden tamamen farklıdır.

### Bankacılık Metrikleri (6 Metrik Adaptasyonu)

| Standart Metrik | Banka Karşılığı | Neden |
|----------------|-----------------|-------|
| ROIC | **ROE** | Sermaye getirisi — bankanın "yatırımı" özkaynaktır |
| FCF Marjı | **Temettü Kapasitesi** | Banka FCF üretmez — temettü dağıtım gücü proxy |
| Brüt Marj | **NIM (Net Faiz Marjı)** | Faiz geliri − faiz gideri / ortalama faiz getirili aktifler |
| Net Borç/FAVÖK | **CAR (Sermaye Yeterlilik Rasyosu)** | ≥%12 zorunlu (BDDK) |
| Ciro Büyümesi | **Kredi Büyümesi** | Aktif tarafın büyümesi |
| ROE | **ROE** | Aynı kalır |

### Banka Analiz Sırası (5 Adım)

```
1. NIM Analizi — Faiz marjı trendi, TCMB politika faizi etkisi
   → NIM genişliyor mu, daralıyor mu? Neden?
   → Kısa vadeli yeniden fiyatlama riski

2. Komisyon Geliri — Fee income / toplam gelir oranı
   → Yapısal mı, döngüsel mi? Dijitalleşme etkisi?
   → Bireysel vs kurumsal mix

3. Gider Kontrolü — Cost/Income (C/I) oranı
   → <%40 mükemmel, %40-50 iyi, >%50 zayıf
   → Personel sayısı trendi (şube kapanması, dijitalleşme)

4. Aktif Kalitesi — NPL (Takibe Dönüşüm) Oranı
   → Brüt NPL ve net NPL (karşılık sonrası)
   → NPL coverage ratio (karşılık / brüt NPL) — >%100 güçlü
   → Stage 2 krediler (potansiyel NPL pipeline)
   → Sektörel yoğunlaşma riski (inşaat, enerji, KOBİ)

5. Guidance & Forward — Yönetim hedefleri
   → Kredi büyümesi, NIM, C/I, NPL guidance
   → Guidance track record (son 4 çeyrek)
```

### Banka Değerleme

| Yöntem | Birincil | Açıklama |
|--------|---------|----------|
| **F/DD (Price/Book)** | ✅ Birincil | Bankalar için en yaygın |
| **Gordon Growth** | ✅ Cross-check | PD/DD = (ROE − g) / (Ke − g) |
| **F/K (P/E)** | Yardımcı | Kâr kalitesine dikkat (karşılık manevrası) |
| **Artık Gelir** | İleri seviye | ROE − Ke farkı × BV |
| **EV/EBITDA** | ❌ Kullanılmaz | Bankalar için anlamsız |
| **DCF (FCFE)** | Sınırlı | FCFF değil FCFE — temettü bazlı |

**Earnings Quality Uyarısı:**
- Beat ama düşük kalite (karşılık iptali, vergi avantajı, trading geliri) → sustainable değil
- Kurum "SAT" diyebilir iyi görünen rakamlara rağmen — earnings quality'e bak

### BIST Bankaları Hızlı Referans

| Banka | Tip | Farklılık |
|-------|-----|-----------|
| GARAN | Özel | En yüksek ROE, güçlü fee income |
| AKBNK | Özel | Yüksek NIM, dijital odak |
| YKBNK | Özel | Agresif kredi büyümesi, fee çeşitliliği |
| ISCTR | Kamu | Düşük ROE, yüksek NPL, devlet yönlendirmesi |
| HALKB | Kamu | KOBİ odaklı, governance riski |
| VAKBN | Kamu | Enerji + altyapı kredileri |

**Kamu vs Özel fark:** Kamu bankalarında siyasi yönlendirme riski (seçim öncesi ucuz kredi, NPL erteleme). Bu risk F/DD iskontosuna yansır — kamu bankaları genellikle 0.3-0.6x F/DD, özel bankalar 0.7-1.5x.

### Veri Kaynakları

| Veri | Kaynak |
|------|--------|
| Finansal tablolar | BBB Finans + KAP (BDDK raporlama formatı) |
| Sektör verileri | BDDK Aylık Bülten, TCMB Finansal İstikrar Raporu |
| NIM, C/I, NPL | BBB Finans (gelir tablosu kalemleri) + faaliyet raporu |
| CAR | KAP bildirimi (çeyreklik) |
| Guidance | IR sunumu, analist toplantısı transkripti |
| Global peer | Yahoo Finance (JPM, HSBC, Santander, Itaú) |

---

## 4. Konglomera / Multi-Segment SOTP

### Ne Zaman Kullanılır

Şirketin birden fazla bağımsız iş kolu varsa ve bunlar farklı sektörlerde faaliyet gösteriyorsa:

| Örnek | Segmentler | Neden SOTP |
|-------|-----------|-----------|
| AEFES | Bira (Efes) + Meşrubat (CCI) + İştirakler | Her segment farklı çarpanla değerlenmeli |
| SAHOL | Bankacılık (Akbank) + Enerji (Enerjisa) + Sanayi + Telecom | 10+ alt segment |
| TAVHL | Havalimanı operasyon + duty-free + otel | Her biri farklı ekonomi |
| DOHOL | Cam + otomotiv + finans + enerji | Yüksek çeşitlilik |

### SOTP Hesaplama Şablonu

```
# Parçaların Toplamı Değerlemesi

| Segment | Gelir | FAVÖK | Çarpan | EV | Ağırlık | Kaynak |
|---------|-------|-------|--------|-----|---------|--------|
| Segment A | X mn | X mn | Xx (peer medyanı) | X mn | %X | [peer grubu] |
| Segment B | X mn | X mn | Xx (peer medyanı) | X mn | %X | [peer grubu] |
| Segment C | X mn | X mn | Xx (peer medyanı) | X mn | %X | [peer grubu] |
| **Toplam Firma Değeri** | | | | **X mn** | | |
| − Net Borç (konsolide) | | | | −X mn | | KAP |
| + Nakit | | | | +X mn | | KAP |
| **Equity Değeri** | | | | **X mn** | | |
| ÷ Pay Sayısı | | | | X mn | | KAP |
| **SOTP Hisse Başı** | | | | **X TL** | | |

Konglomera İskontosu: %X → Düzeltilmiş Hisse Değeri: X TL
```

### Her Segment İçin Peer Seçimi

Her segmentin peer grubu o segmentin sektörüne göre ayrı belirlenir:

```
AEFES örneği:
  Bira segmenti → TBORG, AB InBev, Heineken, Carlsberg
  CCI (meşrubat) → CCEP, Coca-Cola İçecek peer'ları
  İştirakler → NAV hesabı (borsada varsa piyasa değeri)
```

### İskonto Uygulaması

Konglomera iskontosu holding iskontosuyla benzer mantıktadır (§2). İki ayrı kavram:
- **Holding iskontosu:** Holding şirketi — iştiraklere sahiplik üzerinden NAV
- **Konglomera iskontosu:** Operasyonel şirket — farklı segmentlerin tek çatı altında olması

İskonto belirlerken: Segment raporlama kalitesi, management focus, cross-subsidy riski değerlendirilir.

---

## 5. Yönetim Analizi — Konferans Çağrısı, Faaliyet Raporu & IR Sunumu

### Kaynaklar ve Öncelik Sırası

| # | Kaynak | Nerede Bulunur | Ne Verir |
|---|--------|---------------|----------|
| 1 | **Faaliyet Raporu** | KAP + şirket IR sayfası | Segment gelir kırılımı, stratejik hedefler, yönetim mektubu, risk faktörleri, çalışan verileri |
| 2 | **Yatırımcı Sunumu** | Şirket IR sayfası (genellikle çeyreklik) | KPI'lar, guidance, stratejik yol haritası, segment performansı |
| 3 | **Analist Toplantısı / Konferans Çağrısı** | Şirket IR sayfası (webcast/transkript), YouTube | Yönetim tonu, guidance dili, soru-cevap dinamikleri, rakam dışı sinyaller |
| 4 | **KAP Özel Durum Açıklamaları** | kap.org.tr | Ani gelişmeler: M&A, yönetim değişikliği, SPK kararları |
| 5 | **Basın Röportajları** | web_search | Yönetimin kamuoyu mesajları, stratejik vizyonu |
| 6 | **Bağımsız Denetim Raporu** | KAP (yıllık) | Görüş türü (olumlu/şartlı/olumsuz), kilit denetim konuları |

### Faaliyet Raporu Analiz Protokolü

Her faaliyet raporu okunduğunda şu bilgiler çıkarılır:

```
Rapor tarihi: [YYYY]
Şirket: [TICKER]

1. YÖNETİM MEKTUBU
   - Ton: [İyimser / Temkinli / Savunmacı]
   - Ana mesaj: [1-2 cümle]
   - Dikkat çeken ifade: [Doğrudan alıntı]

2. STRATEJİK HEDEFLER
   - Kısa vadeli (1Y): [Hedefler]
   - Orta vadeli (3-5Y): [Hedefler]
   - Geçmiş hedef gerçekleşme oranı: [%X — varsa]

3. SEGMENT KIRILIM
   - Gelir segmentleri: [Tablo]
   - Coğrafi kırılım: [Tablo]
   - Segment bazlı büyüme: [Yıllık %]

4. RİSK FAKTÖRLERİ (Şirketin kendi ifadesiyle)
   - [Risk 1]
   - [Risk 2]
   - Yeni eklenen riskler (geçen yıla göre): [varsa]

5. ÇALIŞAN VERİLERİ
   - Toplam çalışan: [X] | Geçen yıl: [Y] | Değişim: [%Z]
   - Coğrafi dağılım: [varsa]

6. DENETİM GÖRÜŞÜ
   - Tür: [Olumlu / Şartlı / Olumsuz]
   - Kilit denetim konuları: [Varsa — ilişkili taraf, varlık değerleme, gelir tanıma]
```

### Yatırımcı Sunumu Analiz Protokolü

```
Sunum tarihi: [YYYY-Q]
Şirket: [TICKER]

1. KPI SLIDE'LARI
   - Hangi KPI'lar raporlanıyor? [Liste]
   - Hangi KPI'lar artık raporlanmıyor? (önceki sunumda vardı, şimdi yok — ⚠️ dikkat)
   - KPI trendleri: [İyileşme / Bozulma / Stabil]

2. GUIDANCE
   | Metrik | Guidance | Önceki Guidance | Değişim |
   |--------|---------|-----------------|---------|
   | Gelir büyümesi | %X | %Y | ↑/↓/→ |
   | FAVÖK marjı | %X | %Y | ↑/↓/→ |
   | CapEx | X mn TL | Y mn TL | ↑/↓/→ |
   | Kredi büyümesi (banka) | %X | %Y | ↑/↓/→ |

3. YENİ STRATEJİK İNİSİYATİFLER
   - [Varsa: yeni pazar girişi, M&A planı, kapasite yatırımı]

4. SLIDE TASARIMINDA DİKKAT ÇEKİCİ DEĞİŞİKLİKLER
   - Önceki sunuma kıyasla çıkarılan/eklenen bölümler
   - Vurgu değişimleri (ör: "büyüme" odağından "karlılık" odağına kayış)
```

### Konferans Çağrısı / Analist Toplantısı Analiz Protokolü

Türkiye'de bu toplantılar çeşitli formatlarda olabilir:
- Webcast (canlı yayın, IR sayfasından erişim)
- Fiziksel analist toplantısı (İstanbul, genellikle büyük kurumlar)
- Zoom/Teams toplantısı (pandemi sonrası yaygınlaştı)
- Transkript (şirket yayınlıyorsa)

```
Toplantı tarihi: [YYYY-MM-DD]
Format: [Webcast / Fiziksel / Video / Transkript]
Katılımcılar: [CEO, CFO, IR Direktörü — kimler konuştu?]
Kaynak: [URL]

1. YÖNETİM TONU ANALİZİ
   - Genel ton: [Güvenli / Temkinli / Savunmacı / Heyecanlı]
   - Sözlü sinyaller:
     - "Hedging" dili (belirsizlik): [örnek cümle varsa]
     - "Confident" dili (güven): [örnek cümle varsa]
     - Kaçınılan sorular: [hangi konular geçiştirildi?]

2. GUIDANCE DETAYLARI
   - Resmi guidance: [tablo — yatırımcı sunumu ile cross-check]
   - Guidance dışı sözel ipuçları:
     - "Pazar payını korumayı hedefliyoruz" → büyüme yavaşlıyor mu?
     - "Agresif yatırım dönemine giriyoruz" → CapEx artışı, kısa vadede FCF baskısı
     - "Maliyet optimizasyonu önceliğimiz" → marj baskısı altında olabilir

3. SORU-CEVAP DİNAMİKLERİ
   - En çok sorulan konu: [X]
   - Yönetimin kaçındığı soru: [varsa]
   - Analist reaksiyonu: [consensus ile uyum/çatışma]

4. RAKAM DIŞI SİNYALLER
   - Yönetim kadrosunda değişiklik ipuçları
   - Organizasyonel yapılanma (yeni bölüm, bölge ofisi)
   - Rekabet hakkında yorumlar (rakip isimleri, pazar dinamikleri)
   - Regülasyon beklentileri
```

### Yönetim Kalitesi Scorecard (task1-arastirma.md §3 ile entegre)

`task1-arastirma.md` Bölüm 3'teki Management Quality Scorecard bu kaynaklardan beslenir:

| Kriter | Birincil Kaynak | İkincil Kaynak |
|--------|----------------|----------------|
| Track Record (guidance gerçekleşme) | Yatırımcı sunumları (son 8 çeyrek) | Faaliyet raporu |
| Sermaye Tahsisi | Faaliyet raporu + KAP | Basın, M&A geçmişi |
| Skin in the Game | MKK pay bildirim, KAP | Faaliyet raporu (yönetim sahipliği) |
| İletişim Kalitesi | Konferans çağrısı tonu + IR yanıt hızı | Analist feedback |
| Yönetim Değişim Riski | KAP özel durum, basın | LinkedIn (yönetici hareketleri) |
| Kurumsal Yönetişim | Bağımsız denetim görüşü + SPK uyum | Faaliyet raporu |

### Kaynak Erişim Şablonu (BIST Şirketleri)

```
# Her şirket için IR kaynaklarını topla:

Şirket: [TICKER]
IR Sayfası: [URL]

Mevcut Kaynaklar:
- [ ] Faaliyet Raporu (yıllık) — [URL veya KAP]
- [ ] Yatırımcı Sunumu (çeyreklik) — [URL]
- [ ] Konferans Çağrısı (webcast/transkript) — [URL]
- [ ] Bağımsız Denetim Raporu — KAP
- [ ] Kurumsal Yönetim Uyum Raporu — KAP

Eksik:
- [ ] [Şirket transkript yayınlamıyor — YouTube'da var mı?]
- [ ] [IR sunumu güncel değil — son sunum tarihi: X]
```

---

## 6. Siyasi Risk — Kantitatif Entegrasyon

### Neden Ayrı Bölüm

Türkiye'de siyasi risk comps iskontosunun ve CRP'nin en büyük bileşenidir. Ama CRP tek başına yeterli olmayabilir — şirkete özgü siyasi maruziyet farklıdır.

### Şirkete Özgü Siyasi Maruziyet Tablosu

| Maruziyet | Yüksek Risk | Düşük Risk | Ölçüm |
|-----------|-------------|------------|-------|
| Kamu ihalesi bağımlılığı | >%30 gelir kamu | <%10 gelir kamu | Gelir kırılımı |
| Regülasyon yoğunluğu | Lisanslı sektör (bankacılık, enerji, telekom) | Serbest piyasa | Sektör sınıflandırması |
| Döviz geliri | <%20 gelir FX | >%60 gelir FX | Coğrafi kırılım |
| Kamu ortaklığı | Devlet hissesi >%20 | Tamamen özel | Ortaklık yapısı |
| Vergi teşviki bağımlılığı | Teşviksiz ETR >%25 fark | Minimal fark | Vergi notu |

**Kullanım:** Bu tablo comps iskontosunu ayarlarken ve risk bölümünde kullanılır. Yüksek siyasi maruziyet = ek iskonto.

---

## Çapraz Referanslar

| Konu | Dosya |
|------|-------|
| IAS 29 düzeltmeleri | `task2-finansal-modelleme.md` Adım 7 |
| CRP hesaplama | bbb-dcf/SKILL.md + bbb-dcf/references/country_erp.md |
| Revenue-weighted CRP | bbb-dcf/SKILL.md |
| Fisher parity cross-check | bbb-dcf/SKILL.md, `SKILL.md` Routing Logic |
| Comps framework | `karsilastirmali-degerleme.md` |
| Yönetim Kalitesi Scorecard | `task1-arastirma.md` Bölüm 3 |
| Holding değerleme (SOTP) | bbb-dcf/methodology/special_cases.md |

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-18 | v1.0 — Türkiye iskontosu kantitatif çerçevesi, holding NAV iskontosu (6 faktör + BIST referans), bankacılık analiz çerçevesi (5 adım + metrik adaptasyonu + değerleme), konglomera SOTP, yönetim analizi (faaliyet raporu + yatırımcı sunumu + konferans çağrısı protokolleri), siyasi risk kantitatif entegrasyonu. |
