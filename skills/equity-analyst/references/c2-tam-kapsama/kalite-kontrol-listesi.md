# Kalite Kontrol Listesi — Kapsam Başlatma Raporları

> **Rapor montaj workflow:** `references/c2-tam-kapsama/task5-rapor-montaj.md`
> **Sayfa layout & grafik haritası:** `references/c2-tam-kapsama/rapor-sablonu.md`
> **XLS model standardı:** `references/c2-tam-kapsama/task2-finansal-modelleme.md`

Bu dosya T5 Faz G'de ZORUNLU olarak okunur. Teslimattan önce her madde kontrol edilir.

**⛔ HERHANGİ BİR "BAŞARISIZ" VARSA → TESLİM ETME. DÜZELT, TEKRAR KONTROL ET.**

---

## §0: Kritik Minimumlar

| Kriter | Minimum | İdeal | Gerçek | Geçti? |
|--------|---------|-------|--------|--------|
| Sayfa sayısı | 30 | 40-50 | _____ | ☐ |
| Kelime sayısı | 10.000 | 12.000-16.000 | _____ | ☐ |
| Gömülü grafik | 25 | 30-35 | _____ | ☐ |
| Kapsamlı tablo | 12 | 15-20 | _____ | ☐ |
| Excel model | 6 tab | 6 tab | _____ | ☐ |
| Format | DOCX | DOCX + PDF | _____ | ☐ |

**Aşağıdakilerden herhangi biri geçersizse TESLİM ETME:**

- ❌ DOCX rapor 30 sayfadan az → EKSİK
- ❌ 25'ten az gömülü grafik → EKSİK
- ❌ 12'den az kapsamlı tablo → EKSİK
- ❌ 10.000'den az kelime → EKSİK
- ❌ XLS finansal model yok → EKSİK TESLİMAT
- ❌ Grafikler gerçek PNG dosyaları yerine metin tarifler → BÜYÜK BAŞARISIZLIK
- ❌ `[DOĞRULANMADI]` etiketi raporda kaldı → DÜZELT
- ❌ Markdown syntax görünüyor (`##`, `**`, ` ``` `) → FORMAT HATASI

---

## §1: Teslimatlar

- [ ] DOCX rapor dosyası oluşturuldu
- [ ] XLS finansal model dosyası mevcut
- [ ] Dosyalar doğru isimlendirildi: `{TICKER}_Rapor_{Tarih}.docx` ve `{TICKER}_DCF_Model.xlsx`

---

## §2: Sayfa & Kelime Kontrolü

### Uzunluk

- [ ] Rapor 30-50 sayfa (say: _____ sayfa)
- [ ] Kelime sayısı 10.000-16.000 (say: _____ kelime)
- [ ] 30 sayfanın altındaysa: DUR ve içerik ekle

### Bölüm Kelime Hedefleri

**Bu tablo task5-rapor-montaj.md'deki kelime hedefleriyle BİREBİR TUTARLI olmalıdır.**

| # | Bölüm | Min | Kaynak | Gerçek | Geçti? |
|---|-------|-----|--------|--------|--------|
| 1 | Yatırım Özeti (Sayfa 1) | 500 | Yeni yazım | _____ | ☐ |
| 2 | Yatırım Görüşü | 800 | Yeni yazım | _____ | ☐ |
| 3 | Büyüme Sürücüleri | 800 | Yeni yazım | _____ | ☐ |
| 4 | Risk Değerlendirmesi | 600 | T1 + reorganize | _____ | ☐ |
| 5 | Şirket Tanıtımı | 800 | T1 kopyala | _____ | ☐ |
| 6 | Yönetim Analizi | 400 | T1 kopyala | _____ | ☐ |
| 7 | Ürün/Hizmet Portföyü | 700 | T1 kopyala | _____ | ☐ |
| 8 | Sektör & Rekabet | 1.000 | T1 kopyala | _____ | ☐ |
| 9 | Moat Analizi | 600 | T1 kopyala | _____ | ☐ |
| 10 | Tarihsel Finansal Analiz | 1.200 | Yeni yazım | _____ | ☐ |
| 11 | **Projeksiyon Varsayımları** | **2.000** | **Yeni yazım** | _____ | ☐ ⭐ |
| 12 | **Senaryo Analizi** | **1.500** | **Yeni yazım** | _____ | ☐ ⭐ |
| 13 | Değerleme Metodolojisi | 800 | Yeni yazım | _____ | ☐ |
| 14 | Adil Değer Tahmini & Tavsiye | 300 | Yeni yazım | _____ | ☐ |
| | **TOPLAM** | **~12.000** | | _____ | ☐ |

**Herhangi bir bölüm minimum altındaysa → DUR, içerik ekle, teslim etme.**

---

## §3: Grafik & Görsel Kontrolü

### Zorunlu 4 Grafik

- [ ] G03: Gelir segmentasyonu (stacked area) ⭐
- [ ] G04: Coğrafi gelir kırılımı (stacked bar) ⭐
- [ ] G28: DCF sensitivity heatmap ⭐
- [ ] G32: Değerleme football field ⭐

### Toplam Sayım & Kalite

- [ ] 25-35 gömülü grafik (say: _____ grafik)
- [ ] Tüm grafikler gerçek PNG görsel dosyaları (metin tarifler DEĞİL)
- [ ] Grafik ve tablolar metin boyunca dağıtılmış, sona gruplanmamış
- [ ] Her 200-300 kelimede 1 grafik gömülü
- [ ] Her sayfada metin + görsel (saf metin sayfası YOK)
- [ ] Grafik özet sayfası mevcut (2×3 grid, S.3)
- [ ] %60-80 sayfa doluluk oranı

### Sıralı Numaralama

- [ ] Tüm grafikler "Grafik 1, Grafik 2, Grafik 3..." sıralı numaralı (boşluk yok)
- [ ] Tüm tablolar ayrı sıralama: "Tablo 1, Tablo 2..." (Grafik 1 ≠ Tablo 1)
- [ ] Her grafiğin üstünde başlık: "Grafik X — [Şirket] [İçgörü Cümlesi]"
- [ ] Her grafiğin altında kaynak satırı: italic, gri, 9pt

### Grafik Başlıkları INSIGHT Formatında

- ✅ "Grafik 3 — Brüt marj 5 yılda 800bp genişledi"
- ❌ "Grafik 3 — Brüt Marj Grafiği"

**Kural:** Her başlıkta en az bir rakam veya karşılaştırma olmalı.

---

## §4: Tablo Kontrolü

### Finansal Tablolar

- [ ] Tam Gelir Tablosu (30-40 kalem), 5Y tarihsel + 5Y tahmin
- [ ] Nakit Akış Tablosu (20-30 kalem)
- [ ] Bilanço Özeti (25-35 kalem)

### Segmentasyon Tabloları

- [ ] Gelir segmentasyonu — ürün/kategori (5-15 satır)
- [ ] Gelir segmentasyonu — coğrafya (2-10 satır)

### Değerleme Tabloları

- [ ] İNA (DCF) varsayımlar tablosu (15-20 satır)
- [ ] AÖSM (WACC) hesaplama tablosu (8-10 satır)
- [ ] Sensitivity matrisi (2 boyutlu: AÖSM × terminal büyüme)
- [ ] Değerleme özet tablosu (yöntem ağırlıkları)

### Peer Karşılaştırma Tablosu ⭐ KRİTİK

- [ ] 5-10 peer şirket listelenmiş
- [ ] Hedef şirket ayrı satırda gösterilmiş
- [ ] Aşağıdaki istatistiksel özet satırları tablonun altında MEVCUT:
  - [ ] Maksimum
  - [ ] 75. Persantil
  - [ ] Medyan
  - [ ] 25. Persantil
  - [ ] Minimum

**İstatistiksel özet eksikse → HATA. Tabloyu düzelt, teslim etme.**

### Diğer Tablolar

- [ ] Senaryo karşılaştırma tablosu (İyimser/Baz/Kötümser)
- [ ] Sayfa 1 finansal özet tablosu (tarihsel + tahmin, G/T notasyonu)
- [ ] 1-8 ek tablo (operasyonel metrikler, çalışma sermayesi, makro varsayımlar, risk matrisi vb.)

### Tablo Formatlama

- [ ] Tüm tablolarda G (Gerçekleşme) / T (Tahmin) notasyonu (A/E DEĞİL)
- [ ] Her tabloda başlık satırı BBB turuncu (#f7931a) arkaplanla
- [ ] Her tabloda alt kaynak satırı
- [ ] Zebra striping (açık/koyu satır sıralaması)

---

## §5: Sayfa 1 Format Kontrolü

- [ ] "KAPSAM BAŞLATMA" başlığı mevcut ("Şirket Güncelleme" DEĞİL)
- [ ] Tez odaklı başlık (olay odaklı DEĞİL — "Güçlü Q4 Sonuçları" gibi DEĞİL)
- [ ] Tavsiye kutusu: tavsiye, fiyat, adil değer tahmini, 52 hafta aralık, PD, FD
- [ ] 3-4 bullet ■ karakteriyle + bold başlıklar
- [ ] Her bullet: bold başlık + 3-5 cümle, sayıyla başlamalı
- [ ] Finansal & değerleme metrikleri tablosu, 2-3Y tarihsel + 2Y tahmin
- [ ] Tablo G/T notasyonuyla işaretli
- [ ] Tüm görsellerde kaynak satırları

---

## §6: İçerik Bölümleri Kontrolü

Tüm bölümler mevcut olmalı:

- [ ] İçindekiler (S.2)
- [ ] Görsel Özet Sayfası (S.3, 2×3 grid)
- [ ] Finansallar sayfası (S.4, dual-column tablolar)
- [ ] Yatırım Görüşü & Riskler (3-5 sayfa)
  - [ ] 3-5 tez ayağı (her biri 200-300 kelime)
  - [ ] Büyüme sürücüleri (3-5 sürücü, kantitatif)
  - [ ] 8-12 risk (4 kategoride: şirkete özel, sektör, finansal, makro)
  - [ ] Çıkış kriterleri (min 2 per risk, ölçülebilir, checkbox formatında)
- [ ] Şirket Derinlemesine (6-12 sayfa)
  - [ ] Şirket tanıtımı + tarihçe
  - [ ] Yönetim analizi (150-400 kelime/yönetici × 3-4 yönetici)
  - [ ] Ürün/hizmet portföyü
  - [ ] Sektör analizi
  - [ ] Moat analizi
  - [ ] Rekabet pozisyonlaması
- [ ] Finansal Analiz & Projeksiyonlar (8-11 sayfa)
  - [ ] Tarihsel finansal analiz (1.200+ kelime)
  - [ ] Projeksiyon varsayımları (2.000+ kelime, ürün-ürün detay) ⭐
  - [ ] Senaryo analizi (1.500+ kelime, 3 senaryo + karşılaştırma) ⭐
- [ ] Değerleme Analizi (5-8 sayfa)
  - [ ] İNA (DCF) + sensitivity
  - [ ] Peer karşılaştırma (comps) + istatistiksel özet
  - [ ] Değerleme metodolojisi (800+ kelime)
  - [ ] Adil değer tahmini & tavsiye (300+ kelime)
- [ ] Ekler: Kaynaklar & Referanslar sayfası + Yasal Uyarı

### İçerik Tekrar Kullanım Doğrulama

- [ ] T1 içeriği neredeyse aynen (verbatim) kullanılmış (yeniden yazılmamış)
- [ ] Şirket derinlemesine bölümleri T1'den formatlanmış
- [ ] Yazım eforu kantitatif bölümlere yönelmiş (projeksiyon, senaryo, değerleme)
- [ ] T2/T3 tabloları doğru çıkarılmış ve formatlanmış

### Grafik Yerleştirme & Duplikasyon Kontrolü (v3.2)

- [ ] **Proximity:** Tüm grafikler (EK01-EK07 dahil) ilgili ana bölümde gömülü — Ekler'de grafik YOK
- [ ] **Duplikasyon yok:** Aynı chart dosyası raporda 2+ kez kullanılmamış (grep ile kontrol et)
- [ ] **İçerik örtüşmesi yok:** Aynı konu hem grafik hem tablo olarak gösterilmemiş (ör. duyarlılık analizi sadece 1 formatta)
- [ ] **Ekler sadece tablo:** Ekler bölümünde yalnızca teknik detay tabloları var (IAS 29, peer detay, çeyreklik tahmin, SOTP vb.)
- [ ] **Grafik numaralama:** Tüm grafikler 1'den N'ye kesintisiz sıralı (boşluk veya tekrar yok)

---

## §7: Kaynak & Hyperlink Kontrolü

### Metin İçi Kaynak Etiketleri

- [ ] Her rakam, oran ve olgusal ifadede kaynak etiketi var: `(Kaynak, Dönem)`
- [ ] `[DOĞRULANMADI]` etiketi raporda KALMADI (tüm dokümanı tara — varsa düzelt)
- [ ] Genel "Şirket verisi" yok — spesifik kaynak adı + tarih

### Tıklanabilir Hyperlink'ler ⭐

- [ ] TÜM URL'ler TIKLANABILIR HYPERLİNK (düz metin DEĞİL)
- [ ] KAP bildirimleri hyperlink'li
- [ ] Damodaran referansları hyperlink'li
- [ ] Şirket IR sayfası hyperlink'li
- [ ] Yahoo Finance peer'ları hyperlink'li
- [ ] Ham URL hiçbir yerde görünmüyor — hepsi formatlanmış
- [ ] 5 örnek hyperlink test edildi (Ctrl+Click ile açılıyor mu?)

### Kaynaklar & Referanslar Sayfası

- [ ] "Kaynaklar & Referanslar" sayfası raporun sonunda mevcut
- [ ] Raporda kullanılan TÜM kaynaklar listelenmiş
- [ ] Kaynaklar kategoriye göre organize (Finansal → Sektör → Değerleme → Şirket → Peer)
- [ ] Her kaynakta tarih var
- [ ] Her kaynakta tıklanabilir hyperlink var (mümkünse)

---

## §8: XLS Model Kontrolü

**Detaylı XLS standardı → `task2-finansal-modelleme.md` §Tab Yapısı.**

### 6-Tab Standardı

- [ ] ÖZET tab'ı: Kilit metrikler, hedef fiyat
- [ ] GELİRMODELİ tab'ı: Segment kırılımı, büyüme varsayımları
- [ ] FİNANSALLAR tab'ı: IS + CF + BS
- [ ] İNA (DCF) tab'ı: FCFF projeksiyonu, terminal değer, equity bridge
- [ ] SENARYOLAR tab'ı: İyimser/Baz/Kötümser karşılaştırma (10-15 metrik)
- [ ] HASSASIYET tab'ı: AÖSM × büyüme + çarpan × marj matrisleri

### Model Kalitesi

- [ ] Tüm formüller çalışıyor (varsayım değişince model güncelleniyor)
- [ ] Dairesel referans yok (#REF!, #DIV/0! yok)
- [ ] Girdiler mavi font (hardcoded), formüller siyah font
- [ ] Tutarlı formatlama: başlıklar, kenarlıklar, renk kodlaması
- [ ] Tablo başlıklarında BBB turuncu (#f7931a)

### Çapraz Kontrol

- [ ] XLS hedef fiyat = DOCX hedef fiyat
- [ ] XLS AÖSM = DOCX AÖSM
- [ ] XLS terminal büyüme = DOCX terminal büyüme

---

## §9: Formatlama Kontrolü

### Font & Layout

- [ ] Arial fontu tüm dokümanda tutarlı
- [ ] Header: "[Şirket] — [Rapor Türü]" her sayfada
- [ ] Footer: sayfa numarası
- [ ] İçindekiler mevcut (TOC field)
- [ ] Yasal uyarı son sayfada

### Renk & Stil

- [ ] Tablo başlıkları BBB turuncu (#f7931a) — #1F4E79 (eski mavi) DEĞİL
- [ ] Zebra striping tablolarda
- [ ] Grafik alt kaynak notu: italic, gri, 9pt

### Sayfa Yoğunluğu & Akış Kontrolü

- [ ] Seyrek sayfa yok (her sayfa %60-80 dolu — yarım boş sayfa YASAK)
- [ ] H1 başlıklarda `page_break_before` aktif (default) — seyrek sayfada `sayfa_sonu=False` ile override edilmiş
- [ ] `keep_with_next` aktif: başlık, grafik ve tablo sonraki içerikle aynı sayfada
- [ ] Widow/orphan yok: tek satır başka sayfaya düşmemiş

### Temizlik

- [ ] Markdown syntax GÖRÜNMÜYOR (`**`, `##`, ` ``` `, `- ` yok)
- [ ] Em-dash yok (düz tire `-` kullan)
- [ ] Placeholder metni YOK ("Bu bölümde... ele alınacaktır" YASAK)
- [ ] "Modele bakınız" referansı YOK — veriler çıkarılmış ve yazılmış
- [ ] "Kısaca özetlersek" YOK — her bölüm tam yazılmış

---

## §10: Türkiye Özel Kontroller

- [ ] G/T notasyonu kullanılmış (A/E değil)
- [ ] İyimser/Baz/Kötümser (Bull/Base/Bear, Boğa/Temel/Ayı değil)
- [ ] mn TL / mrd TL ($ değil)
- [ ] Binlik ayırıcı nokta (12.450)
- [ ] EKLE/TUT/AZALT (BUY/HOLD/SELL değil)
- [ ] "Hedef Fiyat" yerine "Adil Değer Tahmini" kullanılıyor
- [ ] "AL/TUT/SAT" yerine "EKLE/TUT/AZALT" kullanılıyor
- [ ] Senaryo terminolojisi: Kötümser/Baz/İyimser (Boğa/Ayı/Bear/Bull DEĞİL)
- [ ] Yasal uyarıda SPK disclaimer mevcut
- [ ] IAS 29 uyarısı (Türkiye şirketi ise): TL IAS 29 düzeltmeli rakamları spot kurla USD'ye çevirme
- [ ] Fisher cross-check notu (dual currency DCF varsa)
- [ ] Projeksiyon tablosu birim etiketi mevcut: "(Reel TL, Aralık {BAZ_YIL} bazı)" veya "(Nominal TL)" veya "(USD)" [v4.21]
- [ ] Guidance Rekonsilasyon Kutusu mevcut (yönetim guidance varsa): nominal→reel çevirisi, sapma yönü ve gerekçesi [v4.21]
- [ ] Tarihsel tablo birim etiketi mevcut (IAS 29 şirketlerinde) [v4.21]

---

## §11: Çapraz Dosya Tutarlılık — 15 Rakam Spot-Check ⭐ KRİTİK

**DOCX rapor ile kaynak dosyalar (T2 financial_analysis.md, T3 valuation_comps.md, XLS model) arasında BİREBİR eşleşme zorunlu.**

| # | Metrik | Kaynak Değeri | DOCX Değeri | Eşleşme? |
|---|--------|---------------|-------------|----------|
| 1 | FY son yıl Hasılat | _________ | _________ | ☐ |
| 2 | FY son yıl EBIT | _________ | _________ | ☐ |
| 3 | FY son yıl Net Kâr | _________ | _________ | ☐ |
| 4 | FY son yıl HBK | _________ | _________ | ☐ |
| 5 | Terminal yıl Hasılat (T) | _________ | _________ | ☐ |
| 6 | Terminal yıl EBIT (T) | _________ | _________ | ☐ |
| 7 | 5Y Hasılat YBBO | _________ | _________ | ☐ |
| 8 | Baz senaryo adil değer tahmini | _________ | _________ | ☐ |
| 9 | AÖSM (WACC) | _________ | _________ | ☐ |
| 10 | Net Borç | _________ | _________ | ☐ |
| 11 | Pay Sayısı | _________ | _________ | ☐ |
| 12 | FD/FAVÖK (güncel) | _________ | _________ | ☐ |
| 13 | Forward F/K | _________ | _________ | ☐ |
| 14 | Brüt Marj (son FY) | _________ | _________ | ☐ |
| 15 | CapEx/Hasılat (son FY) | _________ | _________ | ☐ |

**Kabul kriteri:** 15 rakamın 15'i de eşlemeli. Tek bir uyumsuzluk → düzelt, tekrar kontrol et.
**Yuvarlama farkları <%0,5 kabul edilir** (mn TL → mrd TL dönüşümlerinde).

**Prosedür:**
1. Kaynak dosyalardan (T2/T3/XLS) 15 rakamı çek
2. DOCX'te aynı rakamları bul
3. Eşleşmeyenler → kaynak dosyayı doğru kabul et (KAP verisi), DOCX'i güncelle
4. TAMAMLANMADAN TESLİM ETME

---

## §12: Yazım & İçerik Kalitesi

### Yazım Stili

- [ ] Sayıyla başla ("Hasılat %15 artışla 27.675 mn TL'ye ulaştı" — "Güçlü hasılat" DEĞİL)
- [ ] Direkt ve özlü profesyonel ton
- [ ] İnformel dil yok
- [ ] Aktif cümle yapısı ("Hasılatın X mn TL'ye ulaşmasını bekliyoruz")

### Doğruluk

- [ ] Ticker sembolünde yazım hatası yok
- [ ] Şirket adında yazım hatası yok
- [ ] Tüm tarihler doğru
- [ ] Tüm hesaplamalar doğrulandı
- [ ] Grafikler metin tarifleriyle uyumlu
- [ ] Tüm rakamlar doğru formatlanmış (TL işaretleri, % işaretleri, binlik ayırıcı)

### "NO SHORTCUTS" Kontrolü

- [ ] T1 içeriği verbatim kopyalanmış (yeniden yazılmamış)
- [ ] Yazım eforu kantitatif bölümlere yönelmiş (projeksiyon, senaryo, değerleme)

---

## §13: Final Sayım — ACTUAL COUNT VERIFICATION ⭐

**Teslimattan hemen önce, gerçek sayıları aşağıya yaz:**

```
DOCX RAPOR FİNAL SAYIM
========================
Dosya adı:     _________________________________
Dosya boyutu:  _________ MB
Sayfa sayısı:  _________ sayfa   (MİNİMUM 30)     ☐ GEÇTİ / ☐ BAŞARISIZ
Kelime sayısı: _________ kelime  (MİNİMUM 10.000)  ☐ GEÇTİ / ☐ BAŞARISIZ
Grafik sayısı: _________ grafik  (MİNİMUM 25)     ☐ GEÇTİ / ☐ BAŞARISIZ
Tablo sayısı:  _________ tablo   (MİNİMUM 12)     ☐ GEÇTİ / ☐ BAŞARISIZ

Zorunlu 4 grafik:  G03 ☐  G04 ☐  G28 ☐  G32 ☐
G01 gerçek veri:   yfinance ile üretildi ☐  (placeholder/sentetik veri YASAK)
Piyasa bilgileri:  yfinance ile çekildi ☐  (mevcut fiyat, 52H, hacim, PD — elle girilmesi YASAK)
Comps ist. özet:   Maks ☐  75. ☐  Medyan ☐  25. ☐  Min ☐

15 Rakam Spot-Check:  _____/15 eşleşti   ☐ GEÇTİ / ☐ BAŞARISIZ
Hyperlink Test (5):   _____/5 çalışıyor   ☐ GEÇTİ / ☐ BAŞARISIZ
XLS 6-Tab:            _____/6 tab mevcut   ☐ GEÇTİ / ☐ BAŞARISIZ

SONUÇ: ☐ TÜM KONTROLLER GEÇTİ → TESLİM ET
       ☐ BAŞARISIZ MADDELER VAR → DÜZELT, TEKRAR KONTROL ET
```

**HERHANGİ BİR "BAŞARISIZ" VARSA → TESLİM ETME. DÜZELT, TEKRAR KONTROL ET.**

---

## §14: Analitik Kalite Kontrolleri

| # | Kontrol | Soru | Fail Kriteri |
|---|---------|------|-------------|
| A1 | Bağımsız Keşif | Rapor, piyasa fiyatlamasıyla ilişkisini (örtüşme veya ayrışma) açıkça ortaya koyuyor mu? | Piyasa ilişkisi hiç tartışılmıyor → FAIL |
| A2 | So What Testi | Her bölümün sonunda yatırımcı için çıkarım var mı? | 3+ bölüm "so what" olmadan bitiyor → FAIL |
| A3 | Kanıt Hiyerarşisi | İddialar somut verilerle (rakam, oran, karşılaştırma) destekleniyor mu? | 5+ kalitatif iddia kantitatif destek olmadan → FAIL |
| A4 | Anlatı Tutarlılığı | Raporun başındaki tez, sonundaki değerlemeyle tutarlı mı? | Tez ↔ değerleme kopuk → FAIL |
| A5 | Karşı-Argüman Dengesi | Her olumlu argümanın karşı riski, her olumsuzun potansiyel çözümü var mı? | Tek yönlü argümantasyon → WARN |
| A6 | T2/T3 Sentez | T1 analitik bölümleri T2/T3 bulgularıyla zenginleştirilmiş mi (Analitik Köprü)? | T1 aynen kopyalanmış, hiç analitik köprü yok → FAIL |
| A7 | Entelektüel Dürüstlük | Belirsizlikler, varsayım kırılganlıkları açıkça belirtilmiş mi? | "Emin olduğumuz" tonda, hiç belirsizlik yok → WARN |
| A8 | Sentez Tutarlılık | Faz 0'daki Ana Argüman ve Argüman Dalları rapor boyunca tutarlı mı? Her rapor bölümü en az 1 dala bağlı mı? Faz 0 Çelişki Matrisi'ndeki çözümler raporda ilgili bölümlere yazılmış mı? | Argüman dalı↔bölüm kopukluğu, çözülmemiş çelişki → FAIL |
| A9 | Varsayım Zinciri | Makro→Sektör→Şirket→Değerleme varsayım zinciri tutarlı mı? Terminal büyüme sektör trendi ile uyumlu mu? | Zincirde çelişki var (risk bölümü vs fırsat bölümü) → FAIL |
| A10 | Nedensellik Kontrolü | En kritik 2-3 varsayımın nedensellik yönü belirtilmiş mi? | Korelasyon nedensellik gibi sunulmuş → WARN |
| A11 | Yaratıcı Zorlama | Standart çerçevenin dışında en az 1 non-obvious gözlem var mı? | Tamamen şablona uygun, hiç orijinal gözlem yok → WARN |

**KURAL:** A1, A3, A4, A6, A8 veya A9 FAIL alırsa rapor GERİ ÇEVRİLİR. A2, A5, A10 ve A11 WARN kabul edilir ama düzeltilmesi önerilir.

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-19 | v1.0 — Standalone dosya olarak oluşturuldu. profesyonel-cikti-rehberi §7'den çıkarıldı ve genişletildi. |
| 2026-03-19 | v2.0 — Sıfırdan rewrite. Türkçe karakter düzeltmesi (ASCII-only → UTF-8). task5-rapor-montaj.md ile kelime tablosu senkronize (14 bölüm). Tekrarlayan maddeler elendi (gerçek PNG 4×→2×). §8 XLS Model Kontrolü eklendi (task2'ye pointer + 6-tab checklist + model kalitesi). §3'e sıralı figure/table numaralama kontrolü eklendi. §5+§6 İçerik bölümleri birleştirilip sadeleştirildi. §13+§14 Yazım+İçerik birleştirildi. 330 → ~400 satır (XLS bölümü + detaylı kelime tablosu eklendi). |
| 2026-03-24 | v2.1 — §15 Post-Assembly Kalite Kontrolleri eklendi (yazım stili, sayfa düzeni, yapısal kontroller). v4.14 EBEBK deneyiminden öğrenimler: em dash/arrow yasağı, sayfa overflow detection, tablo-paragraf spacing, baslik_bar simetri, metin duplikasyonu kontrolü. |

---

## §15: Post-Assembly Kalite Kontrolleri (v4.14)

DOCX üretildikten sonra, teslim öncesi aşağıdaki kontroller yapılmalıdır.

### Yazım Stili

| # | Kontrol | Yöntem | Fail Kriteri |
|---|---------|--------|-------------|
| S1 | Em dash sayısı | DOCX metni tarama (tablo/grafik başlıkları hariç) | Em dash (—) rapor gövde metninde >0 |
| S2 | Arrow sayısı | DOCX metni tarama | Arrow (→) rapor metninde >0 |
| S3 | Bold lead-in | İlk paragrafları kontrol et | Hiçbir analitik paragrafta bold lead-in yok |
| S4 | İçgörü seviyesi | Rastgele 5 paragraf seç | 2+ paragraf Seviye 1-2 (salt veri/gözlem) |
| S5 | Tekrar açıklama kontrolü | Faz 0 Tekrar Haritası'ndaki 5 fact için DOCX'te regex tara | Aynı veri noktasının TAM AÇIKLAMASI (2+ cümle aynı bağlam) 3+ kez geçiyor. Terim bahsi sınırsız, icgoru_kutusu istisna. |
| S5b | Bölüm yeni açı kontrolü | Tekrarlanan fact geçen bölümleri karşılaştır | Aynı fact 2 farklı bölümde aynı cümle yapısı/bağlamla geçiyor (farklı perspektif yok) |

### Sayfa Düzeni

| # | Kontrol | Yöntem | Fail Kriteri |
|---|---------|--------|-------------|
| D1 | Sayfa overflow | DOCX/PDF'te sayfa doluluk kontrolü | Herhangi bir sayfa <%15 doluluk (kapak/İçindekiler hariç) |
| D2 | Tablo-paragraf spacing | Görsel kontrol | Tablo bitiminden sonraki paragraf tabloya yapışık |
| D3 | baslik_bar simetri | Tablo üst başlık genişliğini kontrol et | Başlık barı tablo genişliğinden belirgin geniş veya dar |
| D4 | metin_grafik_layout simetri | Metin ve grafik panel yüksekliklerini kontrol et | Panel yükseklik farkı sayfanın %30'undan fazla |

### Yapısal

| # | Kontrol | Yöntem | Fail Kriteri |
|---|---------|--------|-------------|
| Y1 | Yasal Uyarı sayfa sonu | DOCX'te kontrol et | Yasal Uyarı yeni sayfada başlamıyor |
| Y2 | İçindekiler sayfa numaraları | PDF ile karşılaştır | 3+ sayfa numarası hatalı |
| Y3 | H1 sayfa sonu tutarlılığı | Tüm H1 başlıkları kontrol et | H1 başlık sonraki sayfaya tek başına düşüyor (orphan) |
| Y4 | Bölüm sonu kısa taşma | PDF'te kontrol et | Bölüm sonraki sayfaya sadece 1-5 satır taşıyor |

**KURAL:** S1, S2, D1, Y1, Y2 FAIL alırsa rapor GERİ ÇEVRİLİR. Diğerleri WARN kabul edilir ama düzeltilmesi önerilir.

**Y4 (Kısa Taşma) Düzeltme Prosedürü:**
1. Taşan bölümü belirle
2. O bölümdeki gereksiz tekrarları veya aşırı detaylı cümleleri kısalt (max 150 kelime azaltma)
3. Bölümün kendi sayfası içinde bitmesini sağla
4. Sonraki bölüm artık sıradaki sayfadan başlayarak boş sayfa ortadan kalkar
5. Kısaltma yapılamıyorsa: sonraki bölümün `sayfa_sonu=True`'sunu kaldır (son çare)
