# Profesyonel Cikti Rehberi — Stil, Format ve Ornek Referansi v3.0

> **Bu dosyanin rolu:** DOCX rapor formatlama kurallari, grafik esleme tablosu ve doldurulmus Turkce ornekler.
> **Rapor fiziksel yapisi (sayfa layout, chart embed haritasi):** `references/c2-tam-kapsama/rapor-sablonu.md` (1.050+ satir)
> **T5 Assembly detaylı workflow:** `references/c2-tam-kapsama/task5-rapor-montaj.md` (~960 satır)
> **Kalite kontrol listesi:** `references/c2-tam-kapsama/kalite-kontrol-listesi.md` (standalone, ~400 satır)
> **Giris noktasi (T1-T5 akisi, onkosullar):** `SKILL.md` §T1-T5 bolumleri
> Script: `scripts/rapor-uret.py` (v2.0 — AK Yatirim tarzi dual-column layout)
> Chart uretimi: `scripts/grafik-uret.py` + `references/c2-tam-kapsama/task4-grafik-uretim.md`
> Bilesen kutuphanesi: `references/ortak/cikti-sablonlari.md`
> Ilker'in yazim DNA'si: copywriter skill (core-dna.md + premium-dna.md)
> Finansal veri: `references/c2-tam-kapsama/task2-finansal-modelleme.md` (T2)
> Arastirma: `references/c2-tam-kapsama/task1-arastirma.md` (T1)

---

## 1. Çıktı Türleri ve Minimum Standartlar

### A. Tam Yatırım Tezi Raporu (Initiation)

| Kriter | Minimum | İdeal |
|--------|---------|-------|
| **Sayfa** | 30 | 40-50 |
| **Kelime** | 10.000 | 12.000-15.000 |
| **Chart** | 25 | 30-35 |
| **Tablo** | 12 | 15-20 |
| **Format** | DOCX | DOCX + PDF |

### B. Çeyreklik Güncelleme

| Kriter | Minimum | İdeal |
|--------|---------|-------|
| **Sayfa** | 8 | 10-12 |
| **Kelime** | 3.000 | 4.000-5.000 |
| **Chart** | 8 | 10-12 |
| **Tablo** | 3 | 5-8 |

### C. Sektör Raporu

| Kriter | Minimum | İdeal |
|--------|---------|-------|
| **Sayfa** | 15 | 20-30 |
| **Kelime** | 5.000 | 8.000-10.000 |
| **Chart** | 12 | 18-25 |
| **Tablo** | 6 | 10-15 |

### D. Hızlı Analiz

| Kriter | Minimum | İdeal |
|--------|---------|-------|
| **Sayfa** | 2 | 3-4 |
| **Kelime** | 500 | 800-1.200 |
| **Chart** | 2 | 4-6 |
| **Tablo** | 2 | 3 |

---

## 2. Rapor Yapisi — Sayfa Bazli Spec

> **⚠️ TEK YETKİLİ KAYNAK:** `references/c2-tam-kapsama/rapor-sablonu.md` (1.059 satir)
> Sayfa layout, ■ bullet formati, Grafik/Tablo numaralama, chart embed haritasi, yogunluk kurallari, sayisal format, renk paleti — HEPSI orada.
> Bu dosya (profesyonel-cikti-rehberi.md) sadece §4 DOCX teknik formatlama + §8 ornek metinler icin kullanilir.

*(Sayfa bazli layout, chart embed haritasi, yogunluk kurallari → `rapor-sablonu.md`)*
---

## 3. Assembly Workflow

> **TEK YETKİLİ KAYNAK:** `references/c2-tam-kapsama/task5-rapor-montaj.md` (~960 satır)
> Faz A-G doğrusal workflow, input doğrulama, hard stop gate'ler, DOCX assembly, 14 sık yapılan hata.

---

## 4. DOCX Formatlama Kuralları

### Font ve Stil
| Kullanım | Font | Boyut | Renk |
|----------|------|-------|------|
| Ana metin | Calibri | 9pt | #333333 |
| Başlık (H1) | Calibri Bold | 14pt | #f7931a |
| Alt başlık (H2) | Calibri Bold | 11pt | #f7931a |
| Alt başlık (H3) | Calibri Bold | 9pt | #4d4d4d |
| Tablo içi | Calibri | 8pt | #333333 |
| Tablo başlık (header row) | Calibri Bold | 8pt | #FFFFFF (bg: #f7931a) |
| Tablo üst başlık (baslik_bar) | Calibri Bold | 8pt | #4d4d4d (bg: #EDE7DA) |
| Kaynak notu | Calibri Italic | 7.5pt | #808080 |
| Header/footer | Calibri | 7pt | #808080 |

### Sayfa Kontrolü & Yoğunluk

**`_baslik()` parametreleri (v4.7):**
- `sayfa_sonu=None` (default): H1 başlıkları `page_break_before=False`. Doğal akış korunur. *(v4.7 öncesi True idi.)*
- `sayfa_sonu=True`: Explicit sayfa sonu — sadece kapak sonrası (Yatırım Görüşü) gibi zorunlu geçişlerde kullan.
- `keep_with_next=True`: Başlık, grafik veya tablo sonraki içerikle aynı sayfada kalır (orphan önleme). Otomatik aktif.
- `widow_control=True`: Paragrafın son satırı yeni sayfaya düşmez. Otomatik aktif.

**Uygulama:** `_baslik()`, `grafik_ekle()`, `cift_grafik()`, `tablo_ekle()`, `grafik_kutucuk()`, `bilgi_kutusu()`, `skor_karti()`, `metin_grafik_layout()` fonksiyonlarında `keep_with_next` ve `widow_control` aktif.

### Tablo Stili
- Başlık satırı: BBB turuncu (#f7931a) arka plan + beyaz metin
- Zebra striping: her iki satırda bir açık gri (#F2F2F2)
- Sayısal sütunlar: sağ hizalı
- Metin sütunları: sol hizalı
- Alt satır: kaynak notu (italic, gri)

### Tablo Genişlik Algoritması (v4.6)

**Content-optimal genişlik:** Tablolar varsayılan olarak sayfa genişliğine yayılmaz.
Her sütun, içeriğin tek satırda kalacağı minimum genişlikte olur.
Toplam tablo genişliği = sütunların optimal genişliklerinin toplamı.

- **Otomatik hesaplama:** `tablo_ekle()` fonksiyonu karakter sayısına göre her sütunun optimal genişliğini hesaplar (Arial 8pt ≈ 0.22 cm/karakter + 0.3 cm padding).
- **Sayfa genişliğini aşarsa:** Orantılı olarak küçültülür.
- **Sayfa genişliğinden küçükse:** Tablo dar kalır (content-optimal) — gereksiz yere yayılmaz.
- **`genislik_cm` parametresi:** Aynı sayfadaki birden fazla tablonun genişlik uyumu (harmonizasyon) için kullanılır.

**Kural:** Bir sayfada birden fazla tablo varsa, hepsinin genişliği tutarlı olmalıdır.
`genislik_cm` parametresiyle aynı değeri vererek tablo genişliklerini eşitle.

**Başlık barı simetrisi (v4.14):** `_baslik_bar()` (tablo üst başlığı) ve altındaki veri tablosu artık otomatik olarak aynı genişlikte çizilir. Engine, genişlik hesaplamasını tablo oluşturmadan önce yapar (`_hesapla_tablo_genislik()` helper) ve hesaplanan genişliği `_baslik_bar(genislik_cm=...)` parametresi ile aktarır. Bu, content-optimal modda bile başlık barının tablo genişliğiyle simetrik olmasını sağlar.

```python
# Örnek: Aynı sayfadaki 2 tablonun genişlik uyumu
engine.tablo_ekle(doc, basliklar1, satirlar1, genislik_cm=12.0)
engine.tablo_ekle(doc, basliklar2, satirlar2, genislik_cm=12.0)
```

### Grafik Kuralları
- Grafik üstünde: **insight başlığı** (konu değil, bulgu)
  - ✅ "Grafik 3 — Brüt marj 5 yılda 800bp genişledi"
  - ❌ "Grafik 3 — Brüt Marj Grafiği"
- Grafik altında: "Kaynak: [spesifik kaynak, tarih]"
- Metin içinde organik referans: "Grafik 3'te görüldüğü üzere..."
- `[GRAFİK: dosya.png | Konum: ...]` direktifi **YASAK** (İlker DNA'sı)
- 300 DPI çözünürlük (baskı kalitesi)

### Grafik Boyutları (rapor-uret.py parametreleri)
| Boyut | Genişlik | Kullanım |
|-------|----------|----------|
| TAM | 15.5 cm | Tam sayfa grafik, sensitivity heatmap |
| YARIM | 7.4 cm | Metin akışı içinde, yan sütunda |
| GRID | 7.2 cm | 2'li grafik grid'de yan yana |
| KUCUK | 5.0 cm | Summary box içi, mini chart |

### Sayfa Düzeni
- Sayfa boyutu: A4 (21.0 × 29.7 cm)
- Kenar boşlukları: 2.5 cm (tüm kenarlar)
- Kullanılabilir genişlik: ~16.0 cm
- Yoğunluk: %60-80 sayfa doluluk
- Her sayfada metin + görsel (boş sayfa YOK)

### Sayfa Dengeleme Prensipleri (v4.6)

**Hedef:** Sayfa sayısını azaltmak DEĞİL, her sayfada saçma boşluklar bırakmamak. Her sayfa metin+grafik/tablo ile dengeli olmalı.

**Kurallar:**
1. **Semantik eşleşme:** Metin ve komşu grafik/tablo aynı konuyu anlatmalı. "Coğrafi kırılım" grafiğinin yanında "kategori analizi" metni OLMAZ.
2. **Orphan grafik yasağı:** Tek başına duran grafik olmamalı — ya `metin_grafik_layout()`, ya `cift_grafik()`, ya `grafik_kutucuk()` ile sarmalanmalı.
3. **Mükerrer içerik yasağı:** Aynı veriyi hem özet tablo hem detay tablo olarak gösterme — detaylı olanı tut. Aynı veriyi hem grafik hem tablo olarak gösterme — birini seç.
4. **metin_grafik_layout() kullanımı:** Metin ve grafik semantik olarak eşleştiğinde yan yana layout kullan — sayfa yoğunluğu artar, görsel profesyonellik sağlar.
5. **Metin zenginleştirme:** Tablo veya grafikten sonra açıklayıcı paragraf eksikse, sayfa alt yarısı boş kalır. Her tablo/grafikten sonra en az 1 paragraf sonuç/yorum yazılmalı.
6. **Sayfa sonu politikası (v4.7/v4.14):** H1 başlıkları varsayılan olarak sayfa sonu YAPMAZ. Assembly'de zorunlu sayfa sonları: Kapak sonrası (Yatırım Görüşü), Risk Değerlendirmesi, Şirket Profili, Finansal Derinlemesine Analiz, Adil Değer Tahmini, Ekler, Kaynaklar, Yasal Uyarı. Diğer bölümler doğal akışta kalmalı.
7. **Kısa taşma kontrolü (v4.14):** DOCX/PDF'te bir bölüm sonraki sayfaya sadece 1-5 satır taşıyorsa (kısa overflow) ve sonraki bölüm `sayfa_sonu=True` ile yeni sayfada başlıyorsa, aradaki sayfa neredeyse boş kalır. Bu durumda taşan bölümdeki gereksiz tekrarlar kısaltılarak bölümün kendi sayfası içinde bitmesi sağlanmalıdır. Max 150 kelime azaltma yeterli olmalıdır. Son çare olarak sonraki bölümün `sayfa_sonu=True`'su kaldırılır.
8. **Tablo-paragraf boşluğu (v4.14):** Her tablonun altında en az 10pt boşluk olmalıdır. Engine `_kaynak()` fonksiyonu bunu otomatik sağlar (space_after=10pt). Kaynak satırı olmayan tablolarda engine otomatik spacer paragraf ekler.

### Kapak Sayfası Kuralları (v4.9)

**Zorunlu:** Kapak sayfasında alt boşluk bırakılmaz. Sol panel sayfanın tamamını doldurmalıdır.

#### Sol Panel (60% — ~10.5cm)

- Minimum 5 tez pillar'ı, her biri 4-6 cümle (toplam min 550 kelime)
- Her pillar: dict yapısında `{'baslik': '...', 'metin': '...'}` — metin justified
- Değerleme özeti: min 2-3 cümle (İNA + Peer + potansiyel, WACC, terminal büyüme, peer listesi)
- Risk özeti: min 2-3 cümle (tüm kritik riskler tek paragrafta)
- Alt boşluk kalıyorsa: pillar sayısını 6'ya çıkar veya mevcut pillar'ları genişlet

#### Sağ Panel (40% — ~7.2cm)

- Analist satırı: `"Analist: {Ad} (AI Agent) | {kurum_url}"` — sağa yaslı, kurum URL tıklanabilir hyperlink
- Piyasa Bilgileri tablosu (key-value, min 9 satır) — zebra stili KULLANILMAZ, `tablo_stil()` kullan
- Finansal Özet tablosu (min 10 satır, başlıklar kısa: "2024", "2025T" — FY prefix YOK)
- Değerleme Çarpanları tablosu (min 6 satır) — tüm hücreler dolu olmalı, "—" sadece veri yoksa
- Ortaklık Yapısı tablosu (3-5 satır)
- Fiyat performans grafiği (tam genişlik)
- Alt notlar (grafiğin altında, sağ panel İÇİNDE — max 2-3 not, `*` ve `**` formatında)

#### Çarpanlar Tablosu Kuralları (v4.10)

**Fiyat bazı:**
- **Güncel dönem (aktüel):** Mevcut piyasa fiyatı bazlı (yfinance son kapanıştan otomatik çekilir)
- **İleriye yönelik (tahmin):** Hedef fiyat bazlı (örn: 150 TL → PD=24,0 mrd)
- Alt notta hangi dönemin hangi fiyat bazlı olduğu belirtilmeli

**FAVÖK tutarlılığı:** Kapak çarpanlarındaki FD/FAVÖK, Finansal Özet tablosundaki FAVÖK ile aynı metodolojiyi kullanmalı (adjusted ise ikisi de adjusted).

**IAS 29 şirketlerinde F/K:** Raporlanan Net Kâr bazlı F/K yanıltıcıdır → **düzeltilmiş HBK** (IAS 29 parasal kayıp arındırılmış) bazlı hesapla. `*` notu ile belirt.

**"n.m." kullanımı:** SADECE gerçekten anlamsız durumlarda (negatif pay veya payda). Hesaplanabilir bir veri varsa hesaplanıp yazılmalı.

**"—" kullanımı:** SADECE veri hiç mevcut değilse. Yaklaşık hesap yapılabiliyorsa (örn: FY2026T PD/DD = özkaynak projeksiyonundan) yaklaşık değer yazılmalı.

**Rapor içi tutarlılık:** Kapak çarpanları, raporun Değerleme bölümünde (T3) hesaplanmış çarpanlarla tutarlı olmalı. Rapor içinde hesaplanmış bir çarpan kapakta "—" veya "n.m." olamaz.

#### Alt Not Kuralları (v4.10)

- **Maksimum 2-3 not.** `*` ve `**` formatında. 5+ not profesyonel görünmez.
- Adjusted FAVÖK kullanıldığında: `*IAS 29 düzeltmeli: F/K düzeltilmiş HBK, FAVÖK parasal kayıp hariç (adjusted) bazlıdır.`
- Fiyat bazı notu: `2025: Mevcut fiyat bazlı (X TL). 2026T: Hedef fiyat bazlı (Y TL).`
- Finansal Özet'te `*` kullanılan satırlar alt notlarla eşleşmeli.

#### Panel Ayarları

- **Paneller arası boşluk:** ~0.4cm gap — SADECE sol hücrenin sağ margin'i olarak uygulanır. Sağ hücreye margin eklenmez (tablo genişlik hesaplarını bozar).
- **Tablo genişlikleri:** Tüm sağ panel tabloları `genislik_cm=sag_cm` ile tam panel genişliği kaplamalı. `tablo_ekle()` fonksiyonu cell-içi tablolarda margin payı çıkarmaz (v4.10).
- **Layout XML:** Tüm tablolarda (hem `tablo_ekle()` hem manuel) `tblLayout type="fixed"` + `tblW type="dxa"` zorunlu. `tablo_ekle()` bunu otomatik yapar (v4.10). Manuel tablolarda (Piyasa Bilgileri gibi) açıkça ekle.
- **Cell margin:** Sağ panel iç tablolarında `left=0, right=0` — ek daraltma yapılmaz. Piyasa Bilgileri tablosu: `_tablo_cell_margin_sifirla(tbl, top=15, bottom=15, left=0, right=0)`.

#### Üst Satır (Sektör + Tarih)

- Format: `"{Sektör/Kategori}` `{Ay Yıl}"` — em dash (`—`) ile ayrılmış, tek satır
- İlk metin sola yaslı, tarih sağa yaslı DEĞİL — aynı satırda doğal akışta

#### Veri Kaynağı Kuralları (KRİTİK)

**YASAK:** Kapak sayfasındaki HİÇBİR rakam "kafadan" yazılamaz. Tüm veriler izlenebilir kaynaktan gelmeli:

| Veri Grubu | Kaynak | Açıklama |
|-----------|--------|----------|
| Tez pillar metin | T1 araştırma dokümanı | T1'deki bulgulardan sentez, yeni bilgi üretme |
| Finansal Özet tablosu | T2 Excel finansal modeli | Hasılat, FAVÖK, Net Kâr, FCF vb. — modelden birebir |
| Çarpanlar tablosu | T2 + T3 Excel DCF modeli | F/K, FD/FAVÖK vb. — PD/EV ve model çıktılarından hesapla |
| Ortaklık yapısı | T1 araştırma (KAP verileri) | En güncel KAP bildirimi referans |
| Piyasa bilgileri | **yfinance zorunlu** (v4.14) | Mevcut fiyat, 52-hafta, hacim: `yf.Ticker('{TICKER}.IS')`. PD: fiyat × pay sayısı. EV: PD + T2 net borç. Halka açıklık: KAP (statik) |
| Değerleme özeti | T3 DCF/Comps çıktısı | WACC, terminal büyüme, peer listesi — modelden |
| Risk özeti | T1 risk analizi | Tüm riskler T1'de tanımlanmış olmalı |

**Özel durumlar:**
- **Net Kâr "—" yazılamaz** eğer T2 modelinde projeksiyon varsa → modeldeki tahmini yaz
- **FAVÖK metodolojisi** belirtilmeli: "adjusted" (diğer faaliyet hariç) veya "reported" (EBIT+D&A). Assembly'de yorum satırında açıkla
- **FCF negatifse** tabloya `'(42)'` veya `'n.m.'` yaz, "—" ile atla YASAK
- **Çarpanlar negatif/anlamsızsa** `'n.m.'` (not meaningful) yaz

#### Header/Footer Teknik Kuralları

- **Sağ hizalama:** `w:tab val="right"` ile tab stop kullan. `w:pStyle` elementini paragraftan KALDIR (Word'ün "Header"/"Footer" stilinin varsayılan tab stop'ları miras yoluyla çakışır). Ek olarak `w:tab val="clear" pos="4680"` ve `pos="9360"` ile varsayılan pozisyonları temizle.
- **Tab karakteri:** Python `\t` güvenilmez — `w:tab` XML elementi kullan (`_tab_run_ekle()`)
- **Header sol:** `"{Şirket Adı} ({Ticker}) — Araştırma Raporu"` (Kapsam Başlatma DEĞİL)
- **Header sağ:** `"{Ay Yıl} | BBB Research AI"`
- **Footer sol:** `"{Şirket Adı} ({Ticker}) — Araştırma Raporu"`
- **Footer sağ:** `"Sayfa X / Y"` (PAGE + NUMPAGES field)

### Sayfa Sonu Politikası (v4.7)

**Varsayılan:** `_baslik(level=1)` artık `sayfa_sonu=False` (eski: True). H1 başlıkları önceki içerikle aynı sayfada kalır.

**Zorunlu sayfa sonu kuralı:** Sadece `sayfa_sonu=True` ile explicit olarak belirtildiğinde sayfa kırılır. Assembly'de tipik olarak sadece 1 zorunlu sayfa sonu olmalı: kapak sonrası `Yatırım Görüşü`.

**Yasak:** `_sayfa_sonu(doc)` fonksiyonu kaynaklar/yasal uyarı gibi son bölümlerde KULLANILMAMALI — bu bölümler önceki içerikle doğal akışta kalmalı.

### Spacing Standartları (v4.7)

| Element | Önceki | Yeni |
|---------|--------|------|
| `_paragraf()` space_after | 3pt | **2pt** |
| `_kaynak()` space_after | 4pt | **2pt** |
| `_kaynak()` space_before | 2pt | **1pt** |
| H1 space_before | 12pt | **10pt** |
| H1 space_after | 4pt | **3pt** |
| H2 space_before | 8pt | **6pt** |
| H3 space_before | 5pt | **4pt** |
| H3 space_after | 2pt | **1pt** |
| `icgoru_kutusu` başlık space_after | 4pt | **2pt** |
| `icgoru_kutusu` içerik space_after | 6pt | **3pt** |
| `icgoru_kutusu` cell margin | 80/80 | **60/60** |
| `icindekiler` item space_after | 2pt | **1pt** |

**Boş paragraf yasağı:** `icgoru_kutusu()` sonrası `doc.add_paragraph()` kaldırıldı. Tüm inter-element boşluk spacing ile kontrol edilmeli.

### Orphan Koruma Kuralları (v4.7)

1. **Tablolar:** İlk 2 satıra (header + ilk veri satırı) `keep_with_next = True`. Son satıra UYGULANMAZ (boş sayfa riski).
2. **`grafik_kutucuk()`:** Tüm satırlara `keep_with_next = True` — **son satır HARİÇ**. Son satıra uygulanırsa Word tüm kutuyu sonraki sayfaya iter ve önceki sayfa boş kalır.
3. **Başlıklar:** Tüm `_baslik()` çağrılarında `keep_with_next = True` + `widow_control = True` (engine'de otomatik).
4. **Kural:** `keep_with_next` asla büyük blokların SON elemanına uygulanmamalı — aksi halde Word tüm bloğu taşır ve boş sayfa yaratır.

---

## §4B: Gorsel Hikaye Anlatimi

### Bilgi Hiyerarsisi Prensibi

Her sayfa 3 saniyede taranabilmeli:
- Ilk 1 saniye: **Baslik** → bu bolum ne hakkinda
- Ilk 3 saniye: **Key takeaway** → ana bulgu/sonuc (icgoru_kutusu() ile)
- 30 saniye: **Destekleyici kanit** → grafik + tablo + metin

### Grafik-Metin Entegrasyon Kurallari

- YANLIS: "Grafik 3'te goruldugu gibi, gelirler artmistir."
- DOGRU: "Magaza basi gelir FY2023-2025 arasinda %22 artti (Grafik 3) — bu, yeni acilislarin sadece sayi degil kalite getirdigini kanıtliyor."

Grafik metni destekler, metin grafigi aciklar. Ikisi birbirinden bagimsiz durmamalidır.

**Proximity Prensibi (v3.2):**
- Her grafik, anlattigi hikayenin YANINDA olmalidir. Okuyucu bir iddia okurken destekleyici grafigi ayni sayfada ya da komsu sayfada gormeli.
- EK grafikleri (EK01-EK07) dahil TUM grafikler ilgili ana bolume gomulur. Ekler bolumune grafik "park etme" YASAKTIR.
- Ayni chart dosyasi raporda 2 kez KULLANILMAZ (duplikasyon yasagi). Tekrar referans icin "(bkz. Grafik N)" metin referansi kullan.
- Ayni konuyu hem grafik hem tablo olarak gosterme — birini sec. Ornek: DCF duyarlilik analizi ya grafik ya tablo olsun, ikisi birden gereksiz.

### Sayfa Kompozisyon Kurallari

Her sayfada ideal yapi:
- Baslik + Key Insight kutusu: ~%15
- Ana icerik (metin + grafik/tablo yan yana): ~%60
- Destekleyici detay: ~%20
- Kaynak notu: ~%5

### icgoru_kutusu() Kullanim Ornekleri

Her ana bolumun basinda icgoru_kutusu() kullanilir:
- tip='bilgi' (mavi): Genel bulgu
- tip='olumlu' (yesil): Olumlu gosterge
- tip='uyari' (sari): Dikkat gereken nokta
- tip='risk' (kirmizi): Onemli risk

---

## 5. Icerik, Assembly ve Chart Eslemesi

> Bu konularin TEK YETKILI KAYNAKLARI:
> - **Icerik tekrar kullanim oranlari:** `rapor-sablonu.md` §İÇERİK TEKRAR KULLANIM ORANLARI
> - **Assembly workflow (Faz A-G):** `task5-rapor-montaj.md`
> - **NO SHORTCUTS enforcement (14 hata):** `task5-rapor-montaj.md` §KRİTİK TALİMAT
> - **Chart embed haritasi (25-35 grafik):** `rapor-sablonu.md` §GRAFİK EMBED HARİTASI
> - **Chart uretim detayi:** `task4-grafik-uretim.md`

---

## 8. Doldurulmuş Türkçe Örnek Metinler

> Bu bölüm rapor-uret.py ve agent'a "böyle yazılır" referansı sağlar.
> Kaynaklar: VAKKO tezi, TBORG çeyreklik güncelleme, AK Yatırım / İş Yatırım kurumsal raporları.

### 8A. Sayfa 1 — Özet Kutusu Örneği

```
┌───────────────────────────────────────────────────────┐
│  TÜRK TUBORG BİRA VE MALT SANAYİİ A.Ş.              │
│  BIST: TBORG                                          │
│──────────────────────┬────────────────────────────────│
│  Tavsiye: EKLE       │  Adil Değer Tahmini: 221 TL   │
│  Conviction: YÜKSEK  │  Mevcut Fiyat: 155 TL         │
│  Risk: ORTA          │  Potansiyel Getiri: %42        │
│──────────────────────┴────────────────────────────────│
│                                                        │
│  Sektör: İçecek (Bira)  │  PD: X mrd TL              │
│  Pazar Payı: %49.7      │  FD/FAVÖK: 12.3x           │
│  Brüt Marj: %55.3       │  F/K (İleriye Dönük): 12x  │
│  ROIC: %26              │  Temettü Verimi: %2.8       │
│                                                        │
│  ★ Olumlu: Rekor brüt marj, duopol fiyatlama gücü,   │
│    premiumlaşma trendi                                 │
│  ▲ Risk: Düzenleyici (ÖTV), muhasebe etkisi           │
│    (IAS 29), tek coğrafya bağımlılığı                 │
└───────────────────────────────────────────────────────┘
```

### 8B. Yatırım Tezi Paragrafı Örneği

> **İyi örnek (İlker tarzı):**
>
> Türk Tuborg, Türk bira pazarının %49.7'sini kontrol eden duopol yapısının güçlü tarafıdır. Şirketin yatırım tezi üç yapısal ayak üzerinde durmaktadır: (1) premiumlaşma — Miller, Beck's ve Bomonti markalarıyla ürün karmasını yukarı kaydırma, (2) duopol fiyatlama gücü — iki oyunculu pazar yapısı ÖTV artışlarını tüketiciye yansıtmayı mümkün kılıyor, (3) operasyonel verimlilik — brüt marj 5 yılda 800bp genişleyerek rekor %55.3'e ulaştı.
>
> Kişi başı bira tüketimi 14.45 litre ile Avrupa ortalamasının çok altında; bu, hacim büyümesi için yapısal alan yaratıyor. Ancak düzenleyici risk (ÖTV artışları, reklam yasakları) ve IAS 29 muhasebe etkisi dikkatle izlenmeli.

> **Kötü örnek (KAÇIN):**
>
> "Tuborg iyi bir şirket. Bira pazarı büyüyor. Marjlar güçlü. Hisse ucuz görünüyor." — İçgörü yok, yapısal analiz yok, sayısal kanıt yok.

### 8C. Finansal Tablo Formatı Örneği

```
Tablo 3: Gelir Tablosu Özeti (mn TL)

|                     | FY2022G  | FY2023G  | FY2024G  | FY2025T  | FY2026T  |
|---------------------|----------|----------|----------|----------|----------|
| Hasılat             | 12.450   | 18.720   | 24.150   | 28.100   | 32.500   |
|   YoY Büyüme        | %22      | %50      | %29      | %16      | %16      |
| Brüt Kâr            | 5.600    | 9.360    | 13.050   | 15.500   | 18.200   |
|   Brüt Marj         | %45.0    | %50.0    | %54.0    | %55.2    | %56.0    |
| EBIT                | 2.800    | 5.100    | 7.200    | 8.500    | 10.100   |
|   EBIT Marjı        | %22.5    | %27.2    | %29.8    | %30.2    | %31.1    |
| Net Kâr             | 1.200    | 3.400    | 5.180    | 4.800    | 6.200    |
|   Net Marj          | %9.6     | %18.2    | %21.5    | %17.1    | %19.1    |
|                     |          |          |          |          |          |
| HBK (TL)            | 4.28     | 12.14    | 18.50    | 17.14    | 22.14    |

Kaynak: KAP, BBB Finans, BBB tahminleri
Not: G = Gerçekleşme, T = Tahmin. Tüm rakamlar nominal TL.
```

**Format kuralları:**
- Binlik ayırıcı: nokta (12.450) — Türk standardı
- Yüzde: % işareti rakamdan önce (%22, %45.0)
- Ondalık: virgül DEĞİL nokta (tutarlılık için)
- Her tabloda "Kaynak:" satırı zorunlu
- G/T notasyonu başlıkta, tablo altı notta ve dipnotta

### 8D. Değerleme Bölümü Örneği

> **Göreceli Değerleme:**
>
> TBORG, FD/FAVÖK bazında 12.3x ile global bira peer'larının medyanı olan 14.8x'e karşı %17 iskontolu işlem görüyor. Bu iskonto kısmen Türkiye ülke riskini, kısmen de tek pazara bağımlılığı yansıtıyor. Ancak TBORG'un ROIC'i (%26) global peer grubunun en yükseği — Heineken %15, AB InBev %12. Bu operasyonel üstünlük, iskontonun makul olmadığını düşündürüyor.

> **İNA (DCF) Özeti:**
>
> Baz senaryo varsayımlarımız: 5 yıllık hasılat YBBO %14, terminal FAVÖK marjı %30, AOSM %12.8 (USD bazlı). Bu varsayımlarla hisse başı değer 221 TL, mevcut fiyata göre %42 potansiyel getiri. Duyarlılık analizinde AOSM %11-14 ve terminal büyüme %2-4 aralığında adil değer tahmini 180-275 TL bandında değişiyor.

**Değerleme paragrafı kuralları:**
- Önce göreceli (peer karşılaştırma), sonra mutlak (İNA)
- Sayısal kanıt zorunlu — "ucuz/pahalı" tek başına yetmez
- Peer iskontosu/primi → neden? açıklanmalı
- Curtis Jensen alıntısı hatırlatılmalı: "DCF is like Hubble telescope..."

### 8E. Varsayım Tablosu Örneği

```
Tablo 8: Temel Varsayımlar

| Varsayım                   | Kötümser | Baz      | İyimser  | Kaynak/Gerekçe                    |
|----------------------------|----------|----------|----------|-----------------------------------|
| Hasılat YBBO (5Y)          | %8       | %14      | %18      | Tarihsel: %25, premiumlaşma       |
| Terminal FAVÖK Marjı       | %26      | %30      | %34      | Son 3Y ort: %28, trend yukarı     |
| Nihai Büyüme Oranı         | %2       | %3       | %4       | Nominal GDP büyümesi ~%3          |
| AOSM (USD)                 | %14      | %12.8    | %11.5    | CRP: %6.01 (Damodaran Oca 2025)   |
| CapEx/Hasılat              | %5       | %4       | %3       | 5Y ort: %4.2                      |
| ETR                        | %25      | %22      | %20      | Yasal: %25, teşvik: -%3           |
| S/C                        | 1.8x     | 2.2x     | 2.5x     | 5Y ort: 2.1x, trend yukarı        |

Kaynak: BBB tahminleri, KAP, Damodaran
```

**Varsayım tablosu kuralları:**
- Her satırda "Kaynak/Gerekçe" sütunu zorunlu — boş bırakılamaz
- Senaryo olasılıkları ayrı satırda: Kötümser %25, Baz %50, İyimser %25 (standart)
- Senaryo isimleri: İyimser/Baz/Kötümser (İngilizce Bull/Base/Bear değil)

### 8F. Risk Bölümü Örneği

> **Olumlu Bulgular:**
> 1. **Duopol fiyatlama gücü:** İki oyunculu pazar yapısı, ÖTV artışlarının tüketiciye yansıtılmasını sağlıyor. Son 3 yılda fiyat artışları enflasyonun üzerinde.
> 2. **Premiumlaşma trendi:** Premium segmentin toplam satış içindeki payı FY2022'de %18'den FY2024'te %27'ye yükseldi. Bu, litre başı geliri artırıyor.
> 3. **Operasyonel verimlilik:** Brüt marj 5 yılda 800bp genişleyerek rekor %55.3'e ulaştı. Carlsberg'in global know-how transferi belirleyici.
>
> **Riskler:**
> 1. **Düzenleyici risk (ÖTV):** ÖTV maktu tutar artışları pazar hacmini baskılayabilir. Etkisi: ÖTV %20 artarsa → pazar hacmi -%3 ila -%5, FAVÖK etkisi -%8 ila -%12.
> 2. **Tek coğrafya bağımlılığı:** Hasılatın %100'ü Türkiye. Ülke riski doğrudan hisseye yansır. CRP azaltım yolu yok.
> 3. **IAS 29 muhasebe etkisi:** Net kâr, parasal kazanç/kayıp nedeniyle çeyrekler arası volatil. Yatırımcı algısını bozuyor.
>
> **Çıkış Kriterleri:**
> - [ ] Pazar payı 2 çeyrek üst üste <%47'ye düşerse → tez çöker
> - [ ] Brüt marj <%45'e geriler ve 2 çeyrek toparlamazsa → fiyatlama gücü sorgulanır
> - [ ] ÖTV maktu tutar %50+ artışı → hacim etkisi modellenecek, çıkış değerlendirilecek

**Risk yazım kuralları:**
- Olumlu ve risk ayrı başlıklar — karıştırılmaz
- Her risk maddesi: (1) ne olabilir, (2) tetikleyici, (3) etki büyüklüğü — üçü bir arada
- Çıkış kriterleri checkbox formatında ve ölçülebilir
- "Her iyimser iddia → Ancak/Fakat dengesi zorunlu" (İlker DNA kuralı)

### 8G. Kapanış Paragrafı Örneği

> Sonuç olarak, Türk Tuborg Türk bira pazarının yapısal avantajlarını en iyi kullanan oyuncu konumunda. Duopol yapısı, premiumlaşma ve operasyonel verimlilik üçlüsü, şirkete sektördeki en yüksek ROIC'i (%26) kazandırıyor. FD/FAVÖK bazında global peer'lara karşı %17 iskonto, tek pazara bağımlılık ve ülke riskini kısmen fiyatlıyor — ancak operasyonel kalite primi yansıtılmıyor.
>
> 221 TL adil değer tahminimiz mevcut seviyeye göre %42 potansiyel getiri sunuyor. Bu, hurdle rate'imizi (reel enflasyon + α) rahatlıkla aşıyor. Tavsiyemiz: **EKLE.**
>
> Temel izleme noktaları: (1) TAPDK aylık hacim verileri — pazar payı teyidi, (2) ÖTV takvimi — bir sonraki artış büyüklüğü, (3) premium segment payı — Q1 2026 sonuçlarında teyit bekliyoruz.

**Kapanış kuralları:**
- Tezi 2-3 cümlede özetle (tekrar, ilk kez okuyormuş gibi)
- Adil değer tahmini + potansiyel getiri + tavsiye net söyle
- Sonraki izleme noktaları (1-2-3) ile "film burada bitmiyor" mesajı ver
- Son cümle ileriye dönük olmalı — geçmişe bakarak bitirme

### 8H. Grafik Başlık Örnekleri

| ❌ Kötü Başlık | ✅ İyi Başlık (İçgörü bazlı) |
|---------------|------------------------------|
| "Gelir Grafiği" | "Hasılat 3 yılda 2x büyüdü — premiumlaşma sürücü" |
| "Marj Trendi" | "Brüt marj rekor %55.3 — 5 yılda 800bp genişleme" |
| "Pazar Payı" | "Duopol dengesi: TBORG %49.7 vs AEFES %50.3" |
| "F/K Grafiği" | "İleriye dönük F/K 12x — 5Y ortalamanın %15 altında" |
| "DCF Sensitivity" | "Adil değer tahmini AOSM ve büyümeye duyarlılık: 180-275 TL bandı" |

**Kural:** Her grafik başlığı bir cümle — ve o cümlede en az bir rakam veya karşılaştırma olmalı.

### 8I. Projeksiyon Varsayımları Narratif Şablonu (2.000-3.000 Kelime)

> **Bu bölüm raporun en kritik yeni yazım alanıdır.** Tablo (8E) tek başına yetmez.
> Her varsayımın arkasındaki mantığı, sürücüleri ve riskleri **narratif** olarak açıkla.
> Yapı: Segment bazlı (1.000-1.500 kel) + Coğrafya bazlı (500-800 kel) + Diğer varsayımlar (500-700 kel).

#### A. Segment Bazlı Gelir Varsayımları (1.000-1.500 kelime)

Her ana segment/ürün kategorisi için ayrı alt başlık aç. Minimum 3 segment. Her segment:

```
#### [Segment Adı] Gelir Varsayımları

[Segment] gelirinin FY20XX'teki X mn TL seviyesinden FY20XX+5'te Y mn TL'ye 
ulaşmasını (Z% YBBO) bekliyoruz. Bu büyümenin ana sürücüleri:

1. **[Sürücü 1 — spesifik metrik]:** [2-3 cümle. Tarihsel veri + ileriye dönük 
   beklenti. Sayıyla başla.] (Kaynak: KAP, sektör kuruluşu vb.)
   
2. **[Sürücü 2 — spesifik metrik]:** [2-3 cümle.] (Kaynak: ...)

3. **[Sürücü 3]:** [2-3 cümle.] (Kaynak: ...)

**Yıl bazlı varsayımlar:**
- FY20XXT: %X büyüme — [spesifik faktörler: yeni ürün lansmanı, kapasite artışı vb.]
- FY20XX+1T: %X büyüme — [spesifik faktörler]
- FY20XX+2 – FY20XX+4T: %X YBBO — [yapısal/uzun vadeli faktörler]

**Bu varsayımlara yönelik riskler:** [2-3 madde — her risk spesifik ve ölçülebilir]
```

**Örnek (TBORG Premium Segment):**

> #### Premium Bira Segmenti Gelir Varsayımları
>
> Premium segmentin (Miller, Beck's, Bomonti Filtresiz) FY2025'teki tahmini 7.6 milyar TL gelirden 
> FY2030'da 14.2 milyar TL'ye ulaşmasını (%13.3 YBBO) bekliyoruz. Bu büyümenin sürücüleri:
>
> 1. **Ürün karması kayması:** Premium segmentin toplam satış içindeki payı FY2022'de %18'den 
>    FY2024'te %27'ye yükseldi (KAP faaliyet raporu). Litre başı ortalama fiyat standardın 1.6x'i. 
>    FY2030'da %38 paya ulaşmasını bekliyoruz — Polonya (~%35) ve Çekya (~%42) referans.
>
> 2. **Gastronomi kanalı toparlanması:** Pandemi sonrası gastronomi kanalı hâlâ FY2019 seviyesinin 
>    %85'inde. Tam normalleşme FY2027'ye kadar — bu, premium ürünlerin ana satış kanalı.
>
> 3. **Yeni SKU lansmanları:** Carlsberg'in global portföyünden Türkiye'ye adapte edilen 
>    yıllık 2-3 yeni SKU. FY2025'te Brooklyn Lager lansmanı bekleniyor.
>
> **Yıl bazlı:** FY2026T: %16 (premiumlaşma ivmesi), FY2027T: %14 (gastronomi normalleşmesi),
> FY2028-2030T: %11 YBBO (pazar olgunlaşması).
>
> **Riskler:** (1) ÖTV artışı premium/standart fiyat farkını daraltabilir → geçiş etkisi azalır, 
> (2) Anadolu Efes'in premium yanıtı (Bud, Corona lisansları) pazar payını bölüşebilir.

**Her segment için 8-12 madde detay beklenir. Toplam 3-5 segment = 1.000-1.500 kelime.**

#### B. Coğrafi Gelir Varsayımları (500-800 kelime)

Çok pazarlı şirketlerde (THY, Pop Mart, DOCO) her bölge ayrı alt başlık:

```
#### [Bölge] Gelir Varsayımları

[Bölge] gelirinin toplam içindeki payı FY20XX'te %X'ten FY20XX+5'te %Y'ye 
[artmasını/azalmasını] bekliyoruz. YBBO: %Z.

1. **[Pazar dinamiği — spesifik]:** [2-3 cümle.] (Kaynak: ...)
2. **[Dağıtım genişlemesi]:** [2-3 cümle.] (Kaynak: ...)
3. **[Rekabet pozisyonu]:** [2-3 cümle.] (Kaynak: ...)

**CRP notu:** Bu bölgenin ülke risk primi: %X (Damodaran [tarih]). 
Hasılat-ağırlıklı CRP hesabına katkısı: %X × [pay] = %X.
```

**Tek pazarlı BIST şirketleri için (TBORG, çimento vb.):** Coğrafi bölüm yerine kanal kırılımı 
(perakende vs gastronomi, yurt içi vs ihracat) veya bölgesel kırılım (Marmara, İç Anadolu vb.) 
kullanılır. Kısaca 200-300 kelimeyle yazılabilir.

#### C. Diğer Temel Varsayımlar (500-700 kelime)

```
#### Marj Varsayımları

Brüt marjın FY20XX'teki %X'ten terminal %Y'ye [genişlemesini/daralmasını] bekliyoruz.

**Köprü (margin bridge):**
| Faktör | Etki (bp) | Açıklama |
|--------|----------|----------|
| Fiyat artışı > maliyet artışı | +Xbp | [Gerekçe] |
| Ürün karması iyileşmesi | +Xbp | [Premium paya kayma] |
| Hammadde baskısı | -Xbp | [Arpa, malt fiyatları] |
| **Net etki** | **+Xbp** | |

#### Faaliyet Gideri Varsayımları
- GYG/Hasılat: %X → %Y (ölçek avantajı)
- Pazarlama/Hasılat: %X → %Y (marka yatırımı devam)
- ArGe/Hasılat: %X (sabit — endüstri yapısı)

#### Yatırım Harcaması (CapEx) Varsayımları
- CapEx/Hasılat: %X (5Y ort: %Y) — [Gerekçe: kapasite artışı mı, bakım mı?]
- D&A/CapEx oranı: Xx — [yakınsama beklentisi]

#### Çalışma Sermayesi Varsayımları
- DSO: X gün (5Y ort: Y gün) — [trend stabil/iyileşme/bozulma]
- DIO: X gün — [stok politikası]
- DPO: X gün — [tedarikçi ilişkisi]
- CCC net etki: [X gün iyileşme/bozulma → SNA etkisi]

#### Vergi Varsayımları
- ETR: %X (yasal %Y, teşvik etkisi -%Z) — [gerekçe]
```

**Toplam 8I bölümü: ~2.000-3.000 kelime, 3 alt bölüm (A+B+C), initiation raporunun en emek-yoğun yeni yazım alanı.**

### 8J. DOCX–XLS Çapraz Dosya Tutarlılık Kontrolü

**XLS finansal model (T2 çıktısı) ile DOCX rapor (T5 çıktısı) arasında rakam tutarlılığı zorunludur.**

#### Kontrol Matrisi (Minimum 15 Rakam)

| # | Metrik | XLS Sayfası | DOCX Sayfası | Eşleşme? |
|---|--------|-------------|-------------|----------|
| 1 | FY son yıl Hasılat | GelirModeli | S.1 özet + S.4 tablo | ☐ |
| 2 | FY son yıl EBIT | GelirTablosu | S.1 özet + S.4 tablo | ☐ |
| 3 | FY son yıl Net Kâr | GelirTablosu | S.1 özet + S.4 tablo | ☐ |
| 4 | FY son yıl HBK | GelirTablosu | S.1 özet | ☐ |
| 5 | Terminal yıl Hasılat (T) | GelirModeli | Projeksiyon bölümü | ☐ |
| 6 | Terminal yıl EBIT (T) | GelirModeli | Projeksiyon bölümü | ☐ |
| 7 | 5Y Hasılat YBBO | GelirModeli | Tez + varsayımlar | ☐ |
| 8 | Baz senaryo adil değer tahmini | İNAGirdileri | S.1 + değerleme bölümü | ☐ |
| 9 | AOSM (WACC) | İNAGirdileri | Değerleme bölümü | ☐ |
| 10 | Net Borç | Bilanco | Değerleme bölümü | ☐ |
| 11 | Pay Sayısı | Bilanco | Değerleme bölümü | ☐ |
| 12 | EV/FAVÖK (current) | — | S.1 + comps bölümü | ☐ |
| 13 | Forward F/K | GelirTablosu | Değerleme bölümü | ☐ |
| 14 | Brüt Marj (son FY) | GelirTablosu | S.4 + finansal analiz | ☐ |
| 15 | CapEx/Hasılat (son FY) | NakitAkis | Projeksiyon varsayımları | ☐ |

**Kabul kriteri:** 15 rakamın 15'i de eşleşmeli. Tek bir uyuşmazlık → düzelt, tekrar kontrol et.

**Prosedür:**
1. XLS'ten 15 rakamı çek
2. DOCX'te Ctrl+F ile aynı rakamları bul
3. Eşleşmeyen varsa → XLS kaynağını doğru kabul et (KAP verisi), DOCX'i güncelle
4. Yuvarlama farkları <%0,5 kabul edilir (mn TL → mrd TL dönüşümlerinde)

**Bu kontrol T5 Adım 7 (Kalite Kontrol) checklist'ine entegre edilmiştir.**

---

### 8K. Kaynak & Referans Protokolü

**Kapsam:** Tüm çıktı türleri (Ç1–Ç4) ve her task'tan üretilen her doküman. Sadece DOCX değil, Markdown çıktılar dahil.

---

#### Metin İçi Kaynak Etiketi (Zorunlu)

Her rakam, oran, tarih ve olgusal ifadenin yanına kısa kaynak etiketi eklenir.

**Format:** `(Kaynak, Dönem)`

| Kaynak Türü | Format | Örnek |
|-------------|--------|-------|
| KAP finansal tablo | `(KAP, Q4 2025)` | "Brüt marj %28.3 (KAP, Q4 2025)" |
| KAP faaliyet raporu | `(KAP Faaliyet Raporu, 2025)` | "Pazar payı %47 (KAP Faaliyet Raporu, 2025)" |
| Şirket IR sunumu | `(IR Sunumu, Q4 2025)` | "Capex rehberi 2.1 mrd TL (IR Sunumu, Q4 2025)" |
| Damodaran veri seti | `(Damodaran, Ocak 2026)` | "ERP %5.46 (Damodaran, Ocak 2026)" |
| TCMB / TÜİK | `(TCMB, Şubat 2026)` | "Enflasyon %39.0 (TCMB, Şubat 2026)" |
| Sektör kuruluşu | `(TAPDK, 2025)` | "Toplam pazar 12.44 mhl (TAPDK, 2025)" |
| Yahoo Finance | `(Yahoo Finance, 18.03.2026)` | "LVS EV/EBITDA 12.4x (Yahoo Finance, 18.03.2026)" |
| Web araştırması | `(web araştırması, 18.03.2026)` | — |
| BBB Finans API | `(BBB Finans, Q4 2025)` | "Net Borç 8.2 mrd TL (BBB Finans, Q4 2025)" |

**Kural:** Kaynak belirlenemiyorsa → `[DOĞRULANMADI]` etiketi. Veri kullanılmadan önce teyit edilmeli.

---

#### DOCX Hyperlink Kuralları

DOCX raporlarda kaynak etiketleri **tıklanabilir hyperlink** olarak eklenir.

**Word'de görünüm:** Mavi, altı çizili metin. Ctrl+Click ile kaynak URL'si açılır. Plain text URL değil — display text → hyperlink.

**Kaynak türüne göre link hedefleri:**

| Kaynak | Link Hedefi |
|--------|-------------|
| KAP bildirimi | `https://kap.org.tr/tr/Bildirim/{bildirim-no}` |
| KAP şirket sayfası | `https://kap.org.tr/tr/sirket-bilgileri/ozet/{ticker}` |
| Şirket IR sayfası | Şirketin yatırımcı ilişkileri URL'si |
| Damodaran ERP | `https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html` |
| Damodaran Beta | `https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html` |
| TCMB verisi | `https://www.tcmb.gov.tr/` |
| TÜİK verisi | `https://www.tuik.gov.tr/` |
| Yahoo Finance | `https://finance.yahoo.com/quote/{TICKER}` |
| BBB Finans | Internal (komut çıktısı → KAP kaynaklı, KAP linkine yönlendir) |

**rapor-uret.py entegrasyonu:** Kaynak etiketleri `[LINK: display_text | url]` formatında işaretlenirse script otomatik hyperlink'e dönüştürür.

---

#### Son Sayfa: Kaynaklar & Referanslar

Her DOCX raporun sonuna (Yasal Uyarı'dan önce) ayrı bir "Kaynaklar & Referanslar" sayfası eklenir.

**Sayfa başlığı:** `KAYNAKLAR & REFERANSLAR`
**Font:** Arial 9pt, normal (gövde fontundan küçük)
**Her kaynak:** Kaynak adı (tıklanabilir hyperlink) + tarih

**Yapı ve sıra:**

```
KAYNAKLAR & REFERANSLAR

Finansal Veriler
• [KAP Q4 2025 Finansal Tablo → hyperlink]  (Erişim: 15 Şubat 2026)
• [KAP 2025 Yıllık Faaliyet Raporu → hyperlink]  (Erişim: 28 Şubat 2026)
• BBB Finans API çıktısı — KAP/İş Yatırım kaynaklı

Sektör & Piyasa Verileri
• [TAPDK 2025 Bira Sektörü İstatistikleri → hyperlink]  (Erişim: tarih)
• [OSD Araç Satış Verileri, Ocak 2026 → hyperlink]  (Erişim: tarih)
  (Sektöre göre ilgili kurum eklenir: BDDK, BTK, EPDK, vb.)

Değerleme Referansları
• [Damodaran — Country Risk Premium, Ocak 2026 → hyperlink]
• [Damodaran — Industry Betas, Ocak 2026 → hyperlink]
• [Damodaran — Cost of Capital, Ocak 2026 → hyperlink]

Şirket Kaynakları
• [Şirket Yatırımcı İlişkileri Sunumu Q4 2025 → hyperlink]  (Erişim: tarih)
• [Şirket Web Sitesi → hyperlink]  (Erişim: tarih)

Emsal Şirketler (Peer Comps)
• [Yahoo Finance — {TICKER} → hyperlink]  (Erişim: tarih)
  (Her peer için ayrı satır)

Diğer Kaynaklar
• Web araştırması kaynakları (başlık + URL + tarih)
```

**Kurallar:**
- Her satır tıklanabilir hyperlink içerir
- "Erişim: tarih" BBB Finans/web_fetch zamanını gösterir
- Kaynak listesi alfabetik değil, kategoriye göre sıralanır
- Kategori başlığı olmayan kaynaklar "Diğer Kaynaklar"a gider
- KAP bildirim numarası biliniyorsa URL'ye eklenir

---

#### §8K Kontrol Listesi (T5 QC'ye Eklenir)

```
Kaynaklar & Referanslar Kontrolü:
- [ ] Metin içindeki her rakamda kaynak etiketi var mı?
- [ ] [DOĞRULANMADI] etiketi kalmadı mı?
- [ ] Tüm KAP referansları hyperlink mi?
- [ ] Tüm Damodaran referansları hyperlink mi?
- [ ] IR sunumu / faaliyet raporu referansları hyperlink mi?
- [ ] DOCX son sayfada "Kaynaklar & Referanslar" bölümü var mı?
- [ ] Kategoriler doğru sıralanmış mı? (Finansal → Sektör → Değerleme → Şirket → Peer → Diğer)
- [ ] Her hyperlink Ctrl+Click ile açılıyor mu?
```

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-17 | v1.0 oluşturuldu |
| 2026-03-17 | v2.0 — AK Yatırım tarzı dual-column spec, 7 adımlı assembly workflow, sayfa bazlı detay, content reuse, chart eşleme tablosu, 60+ madde QC checklist |
| 2026-03-17 | v2.1 — Doldurulmuş Türkçe örnek metinler (8A-8H): özet kutusu, tez paragrafı, finansal tablo, değerleme, varsayım, risk, kapanış, grafik başlıkları |
| 2026-03-18 | v2.2 — §8K eklendi: Kaynak & Referans Protokolü. Metin ici kisa format, DOCX hyperlink kurallari, son sayfa yapisi, 8-madde QC kontrol listesi. |
| 2026-03-19 | v3.0 — Rol degisikligi: Detayli T5 assembly → task5-rapor-montaj.md'ye taşındı. QC → kalite-kontrol-listesi.md'ye taşındı. Bu dosya artık stil/format referansı + örnek metinler olarak görev yapar. §2, §3, §5, §6'ya referans notları eklendi. |
| 2026-03-19 | v4.0 — Mimari temizlik: §2 sayfa bazli spec (184 satir) KALDIRILDI → rapor-sablonu.md tek yetkili kaynak. §3 assembly workflow (246 satir) KALDIRILDI → task5-rapor-montaj.md tek yetkili kaynak. §5-§6-§7 (content reuse, NO SHORTCUTS, chart esleme — 79 satir) KALDIRILDI → rapor-sablonu.md + task5 pointer. §4 DOCX teknik formatlama KORUNDI. §8 ornek metinler KORUNDI. Renk #1F4E79 → #f7931a (BBB turuncu). 1.052 → 562 satir. |
