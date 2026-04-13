# Ç2 Tam Kapsama Raporu — Sayfa Bazlı Şablon v1.0

> **Bu dosyanın rolü:** Raporun FİZİKSEL YAPISI — hangi sayfa neye benzer, hangi bölüm nerede, chart embed noktaları.
> **Bu dosya DEĞİLDİR:** T1-T5 pipeline (→ `SKILL.md` §T1-T5) veya assembly workflow (→ `task5-rapor-montaj.md`).
> **Kaynak:** Orijinal initiating-coverage/assets/report-template.md BBB/BIST uyarlaması.

---

## GENEL KURALLAR

### Raporun Ruhu
- Bu rapor İlker'in yatırımcılara sunacağı profesyonel bir equity research çıktısıdır
- JPMorgan, Goldman Sachs, İş Yatırım, Ak Yatırım kalitesinde olmalıdır
- Her sayfa bilgi yoğun: %60-80 sayfa kaplaması, minimal beyaz alan
- Metin + görsel her sayfada bir arada — sadece metin veya sadece grafik sayfası OLMAZ
- İstisna: Son 4 sayfa (tam sayfa grafikler) — İlker'in bülten DNA'sına uygun

### Format Standartları
| Parametre | Değer |
|-----------|-------|
| Kağıt | A4 (210×297 mm) |
| Font | Arial (tüm rapor) |
| Gövde metin | 11pt, #333333 |
| Başlıklar | 14pt bold, BBB turuncu #f7931a |
| Alt başlıklar | 12pt bold, koyu gri #4d4d4d |
| Tablo başlık satırı | Beyaz metin, #f7931a arka plan |
| Tablo alternatif satır | #FFF3E0 (açık turuncu) |
| Grafik çerçeve | #f7931a birincil, #4d4d4d ikincil, #0d579b mavi, #329239 yeşil |
| Sayfa numarası | Alt orta, 8pt |
| Header | Sol: BBB logosu, Sağ: "Yatırım Araştırma" |
| Footer | Sol: yasal uyarı kısa, Sağ: sayfa no |

### Grafik ve Tablo Numaralama Standardı

**HER grafik ve tablo raporun başından sonuna sıralı numaralanır.**

**Grafik formatı:**
```
Grafik X — [Şirket] [Açıklayıcı Başlık]
[Görsel içerik]
Kaynak: Şirket verileri, BBB tahminleri.
```

**Tablo formatı:**
```
Tablo X — [Açıklayıcı Başlık]
[Tablo içerik]
Kaynak: KAP bildirim, şirket faaliyet raporu, BBB tahminleri.
```

**Kurallar:**
- Numaralama rapor boyunca kesintisiz devam eder (Grafik 1, 2, 3... son grafiğe kadar)
- Grafikler ve tablolar AYRI numaralanır (Grafik 1 ≠ Tablo 1)
- Her görselin altında mutlaka kaynak satırı olmalı
- Kaynak satırı: küçük font (8pt), italik
- Genel "Şirket verileri" YASAK — spesifik kaynak belirt:
  - KAP bildirimi → "Kaynak: KAP, FY2025 konsolide finansal tablolar."
  - IR sunumu → "Kaynak: [Şirket] 4Ç25 yatırımcı sunumu, Şubat 2026."
  - BBB tahmini → "Kaynak: BBB tahminleri."
  - Karma → "Kaynak: KAP FY2025, BBB tahminleri."

### Sayısal Format Kuralları
| Kural | Örnek |
|-------|-------|
| Para birimi | TL (Türk Lirası), USD |
| Büyük sayılar | mn TL (milyon), mrd TL (milyar) |
| Binlik ayırıcı | Nokta: 1.234.567 |
| Ondalık ayırıcı | Virgül: %12,5 |
| Yıllar | G = Gerçekleşme, T = Tahmin: FY2024G, FY2025T, FY2026T |
| Negatif sayılar | Parantez: (150) mn TL |
| Çarpanlar | 12,5x (küçük x) |
| Büyüme | +%15,3 veya -%5,2 |

---

## SAYFA 1: KAPSAM BAŞLATMA (EN ÖNEMLİ SAYFA)

**KRİTİK:** Sayfa 1 geleneksel bir yönetici özeti DEĞİLDİR. Kurumsal equity research formatında bir **Yatırım Güncellemesi** sayfasıdır.

### Layout Yapısı

```
┌─────────────────────────────────────────────────────────┐
│  [BBB Logo]              KAPSAM BAŞLATMA                 │
│                          [Şirket Adı] ([TICKER])        │
│                          [Tarih]                        │
├──────────────────────┬──────────────────────────────────┤
│  RATING KUTUSU       │  Grafik 1 — [Şirket] Hisse      │
│                      │  Fiyatı Performansı              │
│  Verdict:  EKLE/TUT/ │                                  │
│           AZALT      │  [12-24 ay hisse fiyat grafiği   │
│  Fiyat:    X TL      │   BIST-100 karşılaştırmalı]     │
│  Adil Değer: Y TL    │                                  │
│  52 Hf:    A-B TL    │                                  │
│  PD:       X mrd TL  │  Kaynak: BBB, KAP.              │
│  FD:       X mrd TL  │                                  │
│                      │                                  │
│  Analist:            │                                  │
│  Kaya                │                                  │
│  BBB Araştırma       │                                  │
├──────────────────────┴──────────────────────────────────┤
│                                                         │
│  EKLE TAVSİYESİ / KAPSAM BAŞLATMA                      │
│  ─────────────────────────────────────  (gri header)    │
│                                                         │
│  ■ **[Bold Konu Başlığı — ana argüman].** 3-5 cümle    │
│    açıklama: spesifik rakamlar, karşılaştırmalar,      │
│    analiz. Rakamlarla başla. "vs." kullan.              │
│                                                         │
│  ■ **[İkinci Konu Başlığı].** 3-5 cümle detaylı       │
│    açıklama...                                          │
│                                                         │
│  ■ **[Üçüncü Konu Başlığı].** 3-5 cümle detaylı       │
│    açıklama...                                          │
│                                                         │
│  ■ **[Dördüncü Konu Başlığı — opsiyonel].** 3-5 cümle │
│    detaylı açıklama...                                  │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Tablo 1 — Finansal ve Değerleme Metrikleri             │
│                                                         │
│              FY2022G  FY2023G  FY2024G  FY2025T FY2026T │
│  Hasılat     X        X        X        X       X   (mn)│
│  Büyüme      %X       %X       %X       %X      %X     │
│  Brüt Marj   %X       %X       %X       %X      %X     │
│  FAVÖK       X        X        X        X       X   (mn)│
│  FAVÖK Marjı %X       %X       %X       %X      %X     │
│  HBK (TL)   X,XX     X,XX     X,XX     X,XX    X,XX    │
│  F/K (x)    XX,Xx    XX,Xx    XX,Xx    XX,Xx   XX,Xx   │
│  FD/Hasılat  X,Xx     X,Xx     X,Xx     X,Xx    X,Xx   │
│  FD/FAVÖK    XX,Xx    XX,Xx    XX,Xx    XX,Xx   XX,Xx   │
│                                                         │
│  Not: G = Gerçekleşme, T = Tahmin.                      │
│  Kaynak: KAP, BBB tahminleri.                           │
└─────────────────────────────────────────────────────────┘
```

> **Engine Primitive Notları (Sayfa 1):**
> - `skor_karti()` → Rating Kutusunun altına BBB Kalite Skoru bileşeni olarak yerleştirilir
> - `bilgi_kutusu()` → Finansal Metrikler tablosunun (Tablo 1) yanına Key Metrics özet kutusu olarak yerleştirilir
> - `icgoru_kutusu()` → Her ana bölümün başında (Sayfa 1 dahil) kullanılır
>
> **"En Kırılgan Varsayım" notu (bullet'ların altında, tablonun üstünde):**
> T3 Çelişki Matrisi'nden (`{TICKER}_celiski_matrisi.md`, Faz 0'da okunur) türetilir. Tek cümle: varsayım adı + kırılırsa etki + izleme kriteri.
> Raporun dürüstlük katmanı; "neye en az güveniyoruz" Sayfa 1'de görünür.

### ■ Bullet Formatı Detayı

Her bullet şu yapıda olmalı:
```
■ **[Başlık: Ana argümanı özetleyen bold ifade].** Normal metin olarak
  3-5 cümle açıklama. Spesifik rakamlarla başla. Karşılaştırma ve analiz
  içer. Finans terimleri kullan (ROIC, WACC, moat, pricing power).
  Her bullet 60-100 kelime arasında.
```

**Örnek bullet:**
```
■ **Duopol pazar yapısı ve fiyatlama gücü, sürdürülebilir %36+ brüt marjı
  destekliyor.** Ebebek, Türkiye bebek perakende pazarında %45+ pazar payı
  ile lider konumda. En yakın rakibi Joker Baby ile birlikte oluşturulan
  duopol yapı, fiyat rekabetini sınırlıyor. FY2025'te brüt marj %36,1
  ile sektör ortalamasının (CRI %50, MNSO %42 — farklı ürün mix'i dikkate
  alınmalı) altında görünse de, FMCG ağırlıklı ürün portföyü için güçlü.
  Premiumlaşma trendi (organik gıda, ithal marka ağırlığı) marj genişlemesini
  destekliyor.
```

### Rating Kutusu Değerleri

| Alan | Açıklama |
|------|----------|
| Verdict | EKLE / TUT / AZALT (3 kademeli) |
| Fiyat | Raporun yazıldığı tarihteki kapanış fiyatı (TL) |
| Adil Değer Tahmini | T3'ten gelen ağırlıklı adil değer tahmini (TL) |
| Upside/Downside | %X (hedef/mevcut - 1) |
| 52 Haftalık Aralık | En düşük — En yüksek TL |
| Piyasa Değeri (PD) | mn TL veya mrd TL |
| Firma Değeri (FD) | mn TL veya mrd TL |
| Halka Açıklık | %X |
| Günlük Ortalama Hacim | X mn TL (3 aylık) |

---

## SAYFA 2: İÇİNDEKİLER

```
İÇİNDEKİLER

Yatırım Görüşü ve Riskler......................................3
  Yatırım Hipotezi..............................................3
  Thesis Pillar'ları............................................3
  Yatırım Riskleri..............................................5

Şirket 101......................................................6
  Şirket Profili ve İş Modeli...................................6
  Şirket Tarihçesi..............................................7
  Ürünler ve Hizmetler..........................................8
  Yönetim ve Ortaklık Yapısı....................................9
  Müşteri ve Dağıtım Kanalları.................................11

Büyüme Görünümü................................................13
  Büyüme Motorları.............................................13
  Pazar Fırsatı (TAM).........................................14

Sektör Analizi ve Rekabet.......................................15
  Sektör Dinamikleri...........................................15
  Rekabet Analizi..............................................17
  Moat Değerlendirmesi.........................................18

Finansal Analiz ve Projeksiyonlar...............................19
  Tarihsel Performans..........................................19
  Finansal Projeksiyonlar......................................22
  Projeksiyon Varsayımları (Detaylı)...........................24
  Senaryo Analizi (Kötümser/Baz/İyimser)......................26

Değerleme Analizi...............................................27
  DCF (İndirgenmiş Nakit Akışı)................................27
  Karşılaştırmalı Değerleme (Comps)............................29
  Emsal İşlemler (varsa).......................................30
  Değerleme Özeti ve Football Field............................30
  Adil Değer Tahmini ve Tavsiye................................31

Ekler..........................................................32
  Detaylı Finansal Tablolar....................................32
  Veri Kaynakları ve Referanslar...............................34
  Yasal Uyarı..................................................35
```

---

## SAYFALAR 3-5: YATIRIM TEZİ VE RİSKLER

**LAYOUT İLKESİ:** Metin + 2-3 grafik iç içe. Her sayfada hem metin HEM görsel olmalı. Sadece metin veya sadece grafik sayfası YASAK.

### Yatırım Hipotezi (1-2 paragraf)

```
[Açılış: Metafor veya çarpıcı veri noktası — İlker'in tez DNA'sına uygun]

[Ana argüman: Moat, büyüme motoru, Quality Value pozisyonu.
 Neden bu şirket? Neden şimdi? 2-3 paragraf, her biri
 rakamlarla desteklenmiş.]
```

### Thesis Pillar'ları (3-5 Sütun)

**[Pillar 1]: [Başlık — ör. "Duopol Pazar Yapısı ve Fiyatlama Gücü"]**

[Açılış cümlesi: anahtar istatistik]

[Paragraf 1: Pazar fırsatının boyutu]
- Mevcut pazar payı
- Büyüme potansiyeli
- Yapısal avantaj

[Paragraf 2: Şirketin neden kazanacağı]
- Rekabet avantajları
- Kanıtlar ve erken sinyaller

[Paragraf 3: Finansal etki]
- Gelir fırsatı (mn TL)
- Marj etkisi
- Zaman çerçevesi

**[GRAFİK EMBED: Grafik X — [Şirket] TAM Büyüme Grafiği]** — Stacked area, pazar büyümesi + şirket payı

**[Pillar 2]: [Başlık — ör. "Marj Genişleme Potansiyeli"]**

[Aynı yapı — 3 paragraf]

**[GRAFİK EMBED: Grafik X — Rekabet Pozisyonlama Matrisi]** — 2×2, şirket vs rakipler

**[Pillar 3]: [Başlık — ör. "Güçlü FCF Üretimi ve Düşük Kaldıraç"]**

[Aynı yapı — 3 paragraf]

**[GRAFİK EMBED: Grafik X — Marj Genişleme Yolu]** — Waterfall veya çizgi grafik

**[Pillar 4-5]: [Opsiyonel ek pillar'lar]**

### Yatırım Riskleri

**Şirkete Özgü Riskler**

**[Risk 1]: [Başlık — ör. "Müşteri Konsantrasyonu"]**
[Riskin açıklaması, mümkünse sayısal boyut, hafifletici faktörler. 2-3 cümle.]

**[Risk 2]: [Başlık — ör. "Yönetim Riski"]**
[2-3 cümle.]

**[Risk 3-5]: [Ek şirkete özgü riskler]**

**Sektör/Pazar Riskleri**

**[Risk 1]: [Başlık — ör. "Düzenleyici Belirsizlik"]**
[2-3 cümle.]

**[Risk 2-3]: [Ek sektör riskleri]**

**Makroekonomik Riskler**

**[Risk 1]: [Başlık — ör. "Enflasyon ve Tüketici Harcama Baskısı"]**
[2-3 cümle. Türkiye spesifik: kur riski, enflasyon, siyasi belirsizlik]

**[Risk 2]: [Başlık — ör. "TL Değer Kaybı"]**
[2-3 cümle.]

> **Engine Primitive Notları (Sayfalar 3-5):**
> - `zaman_cizelgesi()` → Thesis Pillar'ları bölümünde Kataliz Takvimi olarak yerleştirilir; her pillar'ın beklenen somutlaşma tarihlerini gösterir
> - `icgoru_kutusu()` → Yatırım Hipotezi paragrafının hemen öncesinde bölüm açılış içgörüsü olarak kullanılır

---

## SAYFALAR 6-12: ŞİRKET 101

### Şirket Profili (1 sayfa)

**Genel Bakış**
[3-4 paragraf:
- Şirket ne yapar? (sade dille)
- Nasıl para kazanır? (iş modeli)
- Müşterileri kim? (segment)
- Nerede faaliyet gösteriyor? (coğrafya)
- Ölçek metrikleri (mağaza sayısı, çalışan, gelir)]

**Şirket Künyesi Tablosu**
```
Tablo X — [Şirket] Künyesi
Kuruluş Yılı          [YYYY]
Merkez                 [Şehir, Türkiye]
Çalışan Sayısı         [X]
Mağaza/Şube            [X] (Türkiye: [X], Yurt dışı: [X])
BIST Kodu              [TICKER]
Halka Arz              [YYYY]
Halka Açıklık          %X
Ana Ortak              [İsim] (%X)
```

**[GRAFİK EMBED: Grafik X — İş Modeli Akış Diyagramı]**

### Şirket Tarihçesi (2-3 sayfa)

**Kuruluş ve İlk Yıllar**
[Kuruluş hikayesi: kim, ne zaman, neden, ilk vizyon]

**Kilometre Taşları**
```
Tablo X — [Şirket] Tarihsel Kilometre Taşları
Yıl     Olay
[YYYY]  [Kuruluş]
[YYYY]  [İlk büyük yatırım/ürün]
[YYYY]  [Halka arz / önemli ortaklık]
[YYYY]  [Coğrafi genişleme]
[YYYY]  [Son dönem gelişmeler]
```

**[GRAFİK EMBED: Grafik X — Şirket Zaman Çizelgesi]** — Yatay timeline

**Bugünkü Durum**
[Mevcut strateji, son gelişmeler, odak alanları]

### Yönetim ve Ortaklık Yapısı (2 sayfa)

**Üst Yönetim**

Her yönetici için:
```
[İsim] — [Unvan]

[300-400 kelime biyografi:
- Mevcut rolü ve sorumlulukları
- Önceki deneyim ve şirketler (son 2-3 pozisyon)
- Sektördeki başarıları ve track record
- Eğitim ve sertifikalar
- Sektörde toplam deneyim süresi
- Şirketteki görev süresi]
```

⚠️ **3-4 yönetici × 300-400 kelime = 900-1.600 kelime. KISALTMA YOK.**

**Yönetim Kaynakları:**
1. KAP bildirimleri (yönetim değişiklikleri)
2. Faaliyet raporu (yönetim kurulu bölümü)
3. LinkedIn profilleri
4. Basın röportajları ve haberleri
5. Yatırımcı sunumları

**Ortaklık Yapısı**
```
Tablo X — Ortaklık Yapısı
Ortak                  Pay (%)    Not
[Ana Ortak Adı]        %XX,X      [Kurucu/Holding]
[İkinci Ortak]         %XX,X      [Finansal yatırımcı vb.]
Halka Açık             %XX,X
Toplam                 %100,0

Kaynak: KAP, [tarih].
```

**[GRAFİK EMBED: Grafik X — Ortaklık Yapısı Pasta Grafik]**

### Ürünler ve Hizmetler (2-3 sayfa)

Her ana ürün/segment için:
```
[Ürün/Segment Adı]

Açıklama:
[Ne yapar, temel özellikler]

Hedef Müşteri:
[Kim kullanıyor, kullanım senaryoları]

Gelir Modeli:
[Nasıl fiyatlanır, ortalama sepet/kontrat değeri]

Rekabet Konumu:
[Alternatiflere göre nasıl]

Gelir Payı:
[Toplam gelir içindeki oranı, büyüme trendi]
```

**[GRAFİK EMBED: Grafik X — Ürün Portföy Dağılımı]** — Treemap veya pasta

**[GRAFİK EMBED: Grafik X — Gelir Segment Kırılımı (G03 ⭐)]** — Stacked area, tarihsel + projeksiyon

### Müşteri ve Dağıtım Kanalları (1-2 sayfa)

**Müşteri Profili**
- Toplam müşteri tabanı
- Müşteri segmentleri
- Coğrafi dağılım
- Sadakat programı metrikleri (varsa)

**Dağıtım Kanalları**
- Fiziksel mağazalar (adet, m², bölgesel dağılım)
- E-ticaret (penetrasyon oranı, büyüme)
- Toptan kanal (varsa)

**[GRAFİK EMBED: Grafik X — Mağaza Ağı Büyümesi]** — Bar grafik

**[GRAFİK EMBED: Grafik X — Gelir Coğrafi Kırılım (G04 ⭐)]** — Stacked bar

---

## SAYFALAR 13-14: BÜYÜME GÖRÜNÜMÜ

### Büyüme Motorları

**Kısa Vadeli (1-2 yıl)**
1. [Motor 1: ör. Yeni mağaza açılışları]
2. [Motor 2: ör. E-ticaret penetrasyonu]
3. [Motor 3: ör. Premiumlaşma / mix değişimi]

**Orta Vadeli (3-5 yıl)**
1. [Motor 1: ör. Yurt dışı genişleme]
2. [Motor 2: ör. Özel marka oranı artışı]

Her motor için:
```
[Motor Başlığı]

Mevcut Durum:
[Baz metrikler, bugünkü performans]

Fırsat:
[Pazar büyüklüğü, şirket konumu, büyüme potansiyeli]

Zaman Çizelgesi ve Hedefler:
- Kısa vade (1-2 yıl): [Beklenen ilerleme]
- Orta vade (3-5 yıl): [Beklenen ilerleme]

Risk ve Engeller:
[Bu fırsatın gerçekleşmesini engelleyebilecek faktörler]
```

**[GRAFİK EMBED: Grafik X — Gelir Köprüsü (Waterfall)]** — Büyüme motorlarının katkısı

### Pazar Fırsatı (TAM)

```
Tablo X — Pazar Büyüklüğü ve Hedeflenebilir Pazar
                          Mevcut (2025)    Projeksiyon (2030)   YBBO
Toplam Adreslenebilir     X mrd TL         X mrd TL             %X
Hizmet Verilebilir        X mrd TL         X mrd TL             %X
Hedeflenebilir            X mrd TL         X mrd TL             %X
Şirket Payı               %X               %X (hedef)
```

**[GRAFİK EMBED: Grafik X — TAM Büyüme Grafiği]** — Area chart, segment bazlı

---

## SAYFALAR 15-18: SEKTÖR ANALİZİ VE REKABET

### Sektör Dinamikleri (2 sayfa)

**Sektör Tanımı**
[Sektörün kapsamı, sınırları, NACE kodu]

**Pazar Yapısı**
- Konsolide vs. parçalı
- Düzenleyici ortam (EPDK, BDDK, SPK, TAPDK vb.)
- Giriş engelleri

**Temel Trendler**
1. [Trend 1: Açıklama ve etki]
2. [Trend 2: Açıklama ve etki]
3. [Trend 3: Açıklama ve etki]

**[GRAFİK EMBED: Grafik X — Sektör Büyüme Trendi]** — Area chart, YBBO etiketli

### Rekabet Analizi (1-2 sayfa)

**[GRAFİK EMBED: Grafik X — Rekabet Pozisyonlama Matrisi]** — 2×2 grafik

**Rekabet Karşılaştırma Tablosu**
```
Tablo X — Rekabet Karşılaştırması
Metrik            [Şirket]   Rakip A    Rakip B    Rakip C    Rakip D
Hasılat (mn TL)   X          X          X          X          X
Büyüme            %X         %X         %X         %X         %X
Pazar Payı        %X         %X         %X         %X         %X
Brüt Marj         %X         %X         %X         %X         %X
Mağaza Sayısı     X          X          X          X          X
Farklılaştırıcı   [X]        [X]        [X]        [X]        [X]

Kaynak: KAP, şirket faaliyet raporları, sektör kuruluşları.
```

**[GRAFİK EMBED: Grafik X — Pazar Payı Pasta Grafik]**

### Moat Değerlendirmesi (1 sayfa)

```
Tablo X — Moat Analizi
Moat Türü                   Güç (1-10)  Açıklama
Pazara Giriş Engelleri      X/10        [Açıklama]
Müşteri Değiştirme Maliyeti X/10        [Açıklama]
Ağ Etkisi                   X/10        [Açıklama]
Münhasır Varlık / Marka     X/10        [Açıklama]
Ortalama Moat Skoru         X/10

Moat Barometresi: Terminal ROIC [%X] vs WACC [%X]
Terminal ROIC > WACC → Moat conviction YÜKSEK
Terminal ROIC = WACC → Moat conviction DÜŞÜK
```

---

## SAYFALAR 19-26: FİNANSAL ANALİZ VE PROJEKSİYONLAR

**LAYOUT İLKESİ:** Bu bölüm ÇOK YOĞUN olmalı — 5-7 grafik + finansal tablolar iç içe. Her sayfada birden fazla öğe (tablo + 1-2 grafik).

### Tarihsel Finansal Analiz (3-4 sayfa)

**Gelir Tablosu Özeti (3-5 Yıl)**
```
Tablo X — Tarihsel Gelir Tablosu Özeti ({BİRİM_ETİKETİ})
                    FY2021G   FY2022G   FY2023G   FY2024G   TTM
Hasılat (mn TL)     X         X         X         X         X
  Büyüme            -         %X        %X        %X        %X
Brüt Kâr (mn TL)   X         X         X         X         X
  Marj              %X        %X        %X        %X        %X
FAVÖK (mn TL)       X         X         X         X         X
  Marj              %X        %X        %X        %X        %X
Net Kâr (mn TL)     X         X         X         X         X
  Marj              %X        %X        %X        %X        %X
SNA (mn TL)         X         X         X         X         X

Kaynak: KAP konsolide finansal tablolar, BBB hesaplamaları.
```

⚠️ **IAS 29 uyarısı:** Türk şirketlerinde TL rakamlar enflasyon muhasebesine göre düzeltilmiş olabilir. Raporun başında hangi bazda raporlandığı belirtilmelidir. USD çeviri gerekiyorsa: gelir dönem ortalaması, bilanço dönem sonu kuru kullanılır.

**[GRAFİK EMBED: Grafik X — Hasılat Büyüme Trendi (G02)]** — Çizgi grafik, yıllık büyüme etiketli

**[GRAFİK EMBED: Grafik X — Gelir Segment Kırılımı (G03 ⭐)]** — Stacked area (zaten §6'da da var ama burada finansal bağlamda tekrar)

**[GRAFİK EMBED: Grafik X — Brüt Marj Evrimi (G10)]** — Çizgi grafik, marj sürücüleri açıklamalı

**[GRAFİK EMBED: Grafik X — FAVÖK Marjı Gelişimi (G11)]** — Waterfall veya çizgi grafik

**[GRAFİK EMBED: Grafik X — Serbest Nakit Akışı (G12)]** — Bar + çizgi kombo: Bar = SNA, Çizgi = SNA marjı

**[GRAFİK EMBED: Grafik X — Operasyonel Metrikler Dashboard (G13)]** — Çoklu panel:
- Mağaza sayısı büyümesi
- M²/mağaza veya m² başı hasılat
- Müşteri sayısı veya sepet büyüklüğü
- Çalışan verimliliği

### Finansal Projeksiyonlar (2-3 sayfa)

**Projeksiyon Tablosu**
```
Tablo X — Finansal Projeksiyonlar ({BİRİM_ETİKETİ})
                    FY2025T   FY2026T   FY2027T   FY2028T   FY2029T
Hasılat (mn TL)     X         X         X         X         X
  Büyüme (reel)     %X        %X        %X        %X        %X
Brüt Kâr (mn TL)   X         X         X         X         X
  Marj              %X        %X        %X        %X        %X
FAVÖK (mn TL)       X         X         X         X         X
  Marj              %X        %X        %X        %X        %X
SNA (mn TL)         X         X         X         X         X
  SNA Marjı         %X        %X        %X        %X        %X

{BİRİM_ETİKETİ} = Aşağıdakilerden biri (DCF yaklaşımına göre):
  - "Reel TL, Aralık {BAZ_YIL} sabit satın alma gücü bazında"
  - "Nominal TL"
  - "USD"
Kaynak: BBB tahminleri.
```

**Guidance Rekonsilasyon Kutusu (IAS 29 / reel-nominal farkı olan şirketlerde ZORUNLU):**
```
Projeksiyon tablosunun hemen altında veya dipnotunda aşağıdaki kutu yer alır:

┌──────────────────────────────────────────────────────────┐
│ Guidance Rekonsilasyonu                                  │
│ Yönetim {YYYY} rehberliği: X B TL ({NOMİNAL/REEL}).     │
│ Reel eşdeğer (Dec {BAZ_YIL} bazı): Y B TL.              │
│ Modelimiz ({REEL/NOMİNAL}): Z B TL.                     │
│ → Model, rehberliğin %N {üstünde/altında}.               │
│ Gerekçe: [1-2 cümle neden fark var]                      │
└──────────────────────────────────────────────────────────┘

Guidance mevcut değilse: "Firma {YYYY} için kantitatif rehberlik açıklamamıştır."
```

**[GRAFİK EMBED: Grafik X — Senaryo Karşılaştırması (G14)]** — Grouped bar: Kötümser/Baz/İyimser

### Projeksiyon Varsayımları — Detaylı (2.000-3.000 kelime)

⚠️ **KRİTİK:** Bu bölüm KISALTILMAZ. Ürün/segment bazında varsayım açıklaması zorunlu.

**Hasılat Varsayımları**
[Her segment için ayrı paragraf:
- Mevcut büyüme hızı ve sürücüleri
- Projeksiyon gerekçesi (guidance, sektör büyümesi, pazar payı değişimi)
- Aşağı/yukarı risk faktörleri]

**Kârlılık Varsayımları**
[Brüt marj, FAVÖK marjı, net marj projeksiyonu:
- Hangi faktörler marjı genişletir (ölçek, mix, fiyatlama)
- Hangi faktörler marjı daraltır (rekabet, girdi maliyeti, kur)
- Base senaryoda terminal marj hedefi ve gerekçesi]

**Yatırım Harcaması Varsayımları**
[CapEx/Hasılat oranı:
- Tarihsel trend
- Forward guidance
- Bakım vs büyüme CapEx ayrımı]

**Çalışma Sermayesi Varsayımları**
[NWC/Hasılat, DSO, DPO, stok devir]

### Senaryo Analizi (1.500-2.000 kelime)

⚠️ **KRİTİK:** Bu bölüm de KISALTILMAZ. Her senaryo için spesifik parametreler ve tetikleyiciler.

```
Tablo X — Senaryo Parametreleri
Parametre          Kötümser      Baz          İyimser
Olasılık           %20-25        %50-60       %20-25
Hasılat YBBO       %X            %X           %X
Terminal FAVÖK     %X            %X           %X
Mağaza büyümesi    X/yıl         X/yıl        X/yıl
E-ticaret pay      %X            %X           %X
Hisse Başı Değer   X TL          X TL         X TL
```

**Kötümser Senaryo**
[1-2 paragraf: Hangi koşullar bunu tetikler? Makro bozulma, rekabet yoğunlaşması, marj baskısı. Spesifik değerler.]

**Baz Senaryo**
[1-2 paragraf: Neden bu en olası? Guidance ile uyum, tarihsel trendlerin devamı.]

**İyimser Senaryo**
[1-2 paragraf: Hangi katalizörler bunu tetikler? Yurt dışı genişleme, M&A, pazar konsolidasyonu.]

---

## SAYFALAR 27-31: DEĞERLEME ANALİZİ

### Değerleme Metot Özeti

```
Tablo X — Değerleme Özeti
Yöntem                    Ağırlık   Düşük    Baz      Yüksek   Ağırlıklı
İNA (DCF)                 %50       X TL     X TL     X TL     X TL
Karşılaştırmalı (Comps)   %30       X TL     X TL     X TL     X TL
İleriye Dönük FD/FAVÖK    %20       X TL     X TL     X TL     X TL
                          ─────     ─────    ─────    ─────    ─────
Ağırlıklı Adil Değer Tahmini %100                              X TL

Mevcut Fiyat ([tarih]):              X TL
Upside/Downside:                     %X

Kaynak: BBB tahminleri.
```

> **Engine Primitive Notları (Sayfalar 27-29):**
> - `karar_agaci()` → Değerleme Metot Özeti tablosunun ardından Senaryo Karar Ağacı olarak yerleştirilir; İyimser/Baz/Kötümser senaryolarını ve her senaryodaki adil değer aralıklarını ağaç formatında gösterir
> - `icgoru_kutusu()` → Değerleme bölümünün başında (§27 ilk sayfası) anahtar değerleme içgörüsü olarak kullanılır

### DCF Analizi (1-2 sayfa)

**Temel Varsayımlar**
```
Hasılat YBBO (FY2025-2029T):    %X
Terminal Büyüme:                 %X
AOSM (WACC):                    %X (TL bazlı)
Terminal FAVÖK Marjı:            %X
```

**[GRAFİK EMBED: Grafik X — DCF Duyarlılık Analizi (G28 ⭐)]**

KRİTİK FORMAT: DCF duyarlılığı 2 yönlü ısı haritası tablosu olarak gösterilmeli.

```
Tablo X — DCF Duyarlılık Matrisi (TL/hisse)

                        Terminal Büyüme Oranı
AOSM        %8,4    %9,6    %10,6   %11,6   %12,6
%34,4       XXX     XXX     XXX     XXX     XXX
%36,4       XXX     XXX     XXX     XXX     XXX
%38,4       XXX     XXX     [BAZ]   XXX     XXX
%40,4       XXX     XXX     XXX     XXX     XXX
%42,4       XXX     XXX     XXX     XXX     XXX

Renk kodlama: Yeşil (yüksek) → Sarı (orta) → Kırmızı (düşük)
Baz durum: Merkez hücre, bold + çerçeveli
Kaynak: BBB tahminleri.
```

**Fisher Cross-Check (TL DCF varsa)**
```
TL Hedef: X TL
USD Hedef: $X.XX × [kur] = X TL
Sapma: %X (<%10 olmalı — uyarı: IAS 29 baz yıl farkı olabilir)
```

### Karşılaştırmalı Değerleme (Comps) (1-2 sayfa)

**[GRAFİK EMBED: Grafik X — Peer Çarpan Karşılaştırması (G30)]** — Grouped bar

KRİTİK FORMAT: Comps tablosu İKİ BÖLÜMLÜ olmalı — bireysel veriler + istatistiksel özet.

**Bölüm 1: Bireysel Şirket Verileri**
```
Tablo X — Karşılaştırmalı Değerleme

Şirket        Ticker   PD       FD/Has   FD/Has   FD/FAVÖK  FD/FAVÖK  Hasılat   FAVÖK
                       (mn TL)  2024G    2025T    2024G     2025T     Büyüme    Marjı
Peer A        XXXX     X        X,Xx     X,Xx     XX,Xx     XX,Xx     %X        %X
Peer B        XXXX     X        X,Xx     X,Xx     XX,Xx     XX,Xx     %X        %X
Peer C        XXXX     X        X,Xx     X,Xx     XX,Xx     XX,Xx     %X        %X
Peer D        XXXX     X        X,Xx     X,Xx     XX,Xx     XX,Xx     %X        %X
[Şirket]      XXXX     X        X,Xx     X,Xx     XX,Xx     XX,Xx     %X        %X
```

**Bölüm 2: İstatistiksel Özet (ZORUNLU)**
```
Maksimum              X        X,Xx     X,Xx     XX,Xx     XX,Xx     %X        %X
75. Yüzdelik          X        X,Xx     X,Xx     XX,Xx     XX,Xx     %X        %X
Medyan                X        X,Xx     X,Xx     XX,Xx     XX,Xx     %X        %X
25. Yüzdelik          X        X,Xx     X,Xx     XX,Xx     XX,Xx     %X        %X
Minimum               X        X,Xx     X,Xx     XX,Xx     XX,Xx     %X        %X

Kaynak: KAP, Bloomberg, BBB tahminleri. Piyasa verileri [tarih] itibarıyla.
```

**Prim/İskonto Gerekçesi:**
[1 paragraf: Şirketin peer medyanına göre prim veya iskonto hak edip etmediği — büyüme, marj, moat farkları]

### Emsal İşlemler (Varsa) (0,5-1 sayfa)

⚠️ **Not:** BIST'te emsal işlem verisi kısıtlıdır. Bu bölüm veri mevcutsa doldurulur, yoksa bir cümleyle geçilir.

```
Tablo X — Emsal İşlemler
Tarih    Hedef         Alıcı         İşlem       FD/Has   FD/FAVÖK  Prim   Gerekçe
                                     Değeri(mn)
[MM/YY]  [Şirket A]   [Alıcı A]    X            X,Xx     XX,Xx     %X     [Konsolidasyon]
[MM/YY]  [Şirket B]   [Alıcı B]    X            X,Xx     XX,Xx     %X     [Stratejik]

Medyan                                            X,Xx     XX,Xx     %X

Kaynak: KAP, basın açıklamaları, şirket bildirimleri.
```

**Kontrol Primi Analizi:**
[Emsal işlemlerdeki primler genellikle trading comps'un %20-40 üzerinde. BIST'te kontrol primi ortalama %X.]

### Değerleme Özeti ve Football Field (1 sayfa)

**[GRAFİK EMBED: Grafik X — Değerleme Aralık Grafiği / Football Field (G32 ⭐)]**

KRİTİK FORMAT: Yatay bar grafik — tüm değerleme yöntemlerini gösterir.

```
Değerleme Yöntemi              Düşük ◄──── Aralık ────► Yüksek

İNA (DCF)                      XX TL ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ XXX TL

Karşılaştırmalı (Comps NTM)    XX TL ▓▓▓▓▓▓▓▓▓▓▓▓▓ XXX TL

İleriye Dönük FD/FAVÖK         XX TL ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ XXX TL

Emsal İşlemler (varsa)         XX TL ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ XXX TL
                                                    ↑
                                              Mevcut: XX TL
───────────────────────────────────────────────────────────────
Değerleme Aralığı              XX TL                    XXX TL
Adil Değer Tahmini: XXX TL (ağırlıklı ortalama)

Renk: Her yöntem farklı renk. Mevcut fiyat = kırmızı dikey çizgi. Hedef = siyah dikey çizgi.
```

### Adil Değer Tahmini ve Tavsiye

```
═══════════════════════════════════════════════════════════
YATIRIM TAVSİYESİ
═══════════════════════════════════════════════════════════

Mevcut Fiyat:          X TL ([tarih])
Adil Değer Tahmini:    X TL (12 aylık)
Upside/(Downside):     +%X

Verdict:               EKLE / TUT / AZALT
Conviction:            Yüksek (%80-100) / Orta (%50-79) / Düşük (%20-49)

Değerleme Metodolojisi: İNA (%X) + Comps (%X) + Forward (%X) ağırlıklı

───────────────────────────────────────────────────────────
TEMEL KATALİZÖRLER
───────────────────────────────────────────────────────────

1. [Katalizör 1 — zaman çerçevesi]
   [Beklenen etki ve gerekçe]

2. [Katalizör 2 — zaman çerçevesi]
   [Beklenen etki ve gerekçe]

3. [Katalizör 3 — zaman çerçevesi]
   [Beklenen etki ve gerekçe]

───────────────────────────────────────────────────────────
ADİL DEĞER TAHMİNİNE YÖNELİK RİSKLER
───────────────────────────────────────────────────────────

Aşağı Yönlü Riskler:
1. [Risk — olasılık, etki]
2. [Risk — olasılık, etki]
3. [Risk — olasılık, etki]

Yukarı Yönlü Riskler:
1. [Risk — olasılık, etki]
2. [Risk — olasılık, etki]

═══════════════════════════════════════════════════════════
```

---

## SAYFALAR 32+: EKLER

> **⚠️ Proximity Prensibi (v3.2):** Ekler bölümü SADECE aşağıdaki kategorilerdeki içerikler için kullanılır. Grafikler (EK01-EK07 dahil) ASLA Ekler'e konmaz — her grafik ilgili ana bölümünde yer almalıdır.
>
> **✅ Ekler'de Olabilecek İçerikler:**
> - Teknik muhasebe tabloları (IAS 29 köprüsü, GAAP vs operasyonel reconciliation)
> - Detaylı finansal tablolar (40+ satırlık P&L, bilanço, nakit akış)
> - Genişletilmiş peer karşılaştırma tablosu (10+ sütunlu — ana bölüme sığmaz)
> - Çeyreklik tahmin modeli tablosu (forward-looking granüler detay)
> - Alternatif değerleme tablosu (SOTP, residual income vb.)
> - Konsensüs karşılaştırma tablosu
>
> **❌ Ekler'de OLMAMASI Gerekenler:**
> - Tekil grafikler (mağaza sayısı, pazar payı, stok optimizasyonu, büyüme karşılaştırma)
> - Ana bölümde zaten olan içeriğin tekrarı (duplikasyon)
> - Duyarlılık analizi tablosu (grafik olarak ana bölümde varsa)

### Ek A: Detaylı Finansal Tablolar

**Gelir Tablosu (40-50 kalem)**
```
Tablo X — Detaylı Gelir Tablosu
                          FY2021G  FY2022G  FY2023G  FY2024G  FY2025T  FY2026T
Hasılat                   X        X        X        X        X        X
  Ürün Segment A          X        X        X        X        X        X
  Ürün Segment B          X        X        X        X        X        X
  ...
Satışların Maliyeti       (X)      (X)      (X)      (X)      (X)      (X)
Brüt Kâr                  X        X        X        X        X        X
Pazarlama Giderleri       (X)      (X)      (X)      (X)      (X)      (X)
Genel Yönetim Giderleri   (X)      (X)      (X)      (X)      (X)      (X)
Ar-Ge Giderleri           (X)      (X)      (X)      (X)      (X)      (X)
...
[40-50 kalem devam]

Kaynak: KAP konsolide finansal tablolar (FY2021-2024), BBB tahminleri (FY2025-2026).
```

**Nakit Akış Tablosu (25-35 kalem)**
[Aynı yapı, 25-35 satır — en az FY+1T tahmin sütunu ZORUNLU]

**Bilanço (30-40 kalem)**
[Aynı yapı, 30-40 satır — en az FY+1T tahmin sütunu ZORUNLU]

> **KURAL [v1.1]:** Detaylı finansal tablolarda (Gelir Tablosu, Nakit Akış, Bilanço) en az bir forward tahmin sütunu (FY+1T) ZORUNLUDUR. Bu sütun T2 finansal modelinden alınır. Forward bilanço için T2'deki Özkaynak = Önceki Özkaynak + Net Kâr formülü, forward nakit akış için CFO = FAVÖK + İşletme Sermayesi Değişimi formülü baz alınır. Forward sütun olmadan tablo TAMAMLANMIŞ sayılmaz.

**Konsensüs Karşılaştırma Tablosu (ZORUNLU) [v1.1]**

> T1'de en az 3 broker raporu okunmuşsa, aşağıdaki tablo eklenir (bkz. task1-arastirma.md §13.5):

```
Tablo X — Konsensüs Karşılaştırma: BBB vs Piyasa Beklentileri
| Kurum        | Tarih   | Tavsiye | Hedef Fiyat | FY+1 Hasılat | FY+1 FAVÖK | FY+1 Net Kâr |
|-------------|---------|---------|-------------|-------------|-----------|-------------|
| [Kurum 1]   | [tarih] | [X]     | [X TL]      | [Y mn]      | [Z mn]    | [W mn]      |
| ...         |         |         |             |             |           |             |
| Konsensüs   | —       | —       | [medyan]    | [medyan]    | [medyan]  | [medyan]    |
| BBB Research| [tarih] | [tav]   | [hedef]     | [tahmin]    | [tahmin]  | [tahmin]    |
| BBB vs Kons.| —       | —       | [+/-%X]     | [+/-%X]     | [+/-%X]   | [+/-%X]     |

Kaynak: Kurum raporları (birincil), BBB Research tahminleri | [Tarih]
```

### Ek B: Veri Kaynakları ve Referanslar

⚠️ **Bu sayfa ZORUNLU. Tüm kaynaklar tarihli ve mümkünse tıklanabilir hyperlink olarak.**

**Kaynaklar kategorize edilir:**

```
KAP Bildirimleri
- [Şirket] FY2025 Konsolide Finansal Tablolar, [tarih] — [hyperlink]
- [Şirket] 9M2025 Konsolide Finansal Tablolar, [tarih] — [hyperlink]

Faaliyet Raporları
- [Şirket] FY2024 Faaliyet Raporu — [hyperlink]

Yatırımcı Sunumları
- [Şirket] 4Ç25 Yatırımcı Sunumu, [tarih] — [hyperlink]

Kurum Raporları
- [Kurum] [Şirket] Analiz Raporu, [tarih]
- [Kurum] [Şirket] Hedef Fiyat Güncellemesi, [tarih]

Sektör Kaynakları
- [Kuruluş] [Rapor/Veri], [tarih] — [hyperlink]

Piyasa Verileri
- Bloomberg, [tarih]
- KAP, [tarih]

BBB Araştırma Notları
- BBB DCF Modeli, [tarih]
- BBB Finansal Model, [tarih]
```

### Ek C: Yasal Uyarı

```
YASAL UYARI

Bu rapor yalnızca bilgilendirme amacıyla hazırlanmış olup, herhangi bir menkul
kıymete ilişkin yatırım tavsiyesi niteliği taşımamaktadır.

Raporda yer alan bilgi ve görüşler, güvenilir olduğuna inanılan kaynaklardan
derlenmekle birlikte, doğruluğu ve eksiksizliği garanti edilmemektedir.

Bu rapordaki bilgilere dayanılarak yapılan yatırım işlemlerinin sonuçlarından
Borsada Bir Başına (BBB) sorumlu tutulamaz.

Yatırımcılar, yatırım kararlarını kendi araştırmalarına ve risk-getiri
tercihlerine dayandırmalıdır.

Bu rapor, hazırlandığı tarih itibarıyla geçerli piyasa koşullarını yansıtmaktadır.
Sonraki dönemlerde güncellenmesi yükümlülüğü bulunmamaktadır.

© [Yıl] Borsada Bir Başına — Tüm hakları saklıdır.
```

---

## GRAFİK EMBED HARİTASI — 25-35 GRAFİK × BÖLÜM EŞLEMESİ

**HEDEF: 25-35 grafik rapor boyunca dağıtılmış. Her 200-300 kelimede 1 grafik.**

### Sayfa 1 — Yatırım Özeti (1-2 grafik)
| Grafik | Kod | Tür | Kaynak |
|--------|-----|-----|--------|
| Hisse fiyat performansı | G01 | Çizgi (vs BIST-100) | Harici |
| Gelir/FAVÖK dashboard | G02 | Çoklu panel | T2 |

### Sayfalar 3-5 — Yatırım Görüşü ve Riskler (2-3 grafik)
| Grafik | Kod | Tür | Kaynak |
|--------|-----|-----|--------|
| TAM büyüme | G15 | Stacked area | T1 |
| Rekabet pozisyonlama matrisi | G16 | 2×2 scatter | T1 |
| Marj genişleme yolu | G11 | Waterfall/çizgi | T2 |

### Sayfalar 6-17 — Şirket 101 (6-8 grafik)
| Grafik | Kod | Tür | Kaynak |
|--------|-----|-----|--------|
| Şirket zaman çizelgesi | G05 | Yatay timeline | T1 |
| Organizasyon yapısı | G07 | Org chart | T1 |
| Ürün portföy matrisi | G08 | Treemap/pasta | T1 |
| Müşteri segmentasyonu | G09 | Pasta/treemap | T1 |
| ⭐ Gelir segment kırılımı | G03 | Stacked area | T2 |
| ⭐ Gelir coğrafi kırılım | G04 | Stacked bar | T2 |
| Mağaza/şube ağı büyümesi | G06 | Bar | T1/Harici |
| Pazar payı dağılımı | G17 | Pasta/Donut | T1: Sektör |

### Sayfalar 19-26 — Finansal Analiz (5-7 grafik)
| Grafik | Kod | Tür | Kaynak |
|--------|-----|-----|--------|
| Hasılat büyüme trendi | G02 | Çizgi + etiket | T2 |
| Brüt marj evrimi | G10 | Çizgi + açıklama | T2 |
| FAVÖK marjı gelişimi | G11 | Waterfall/çizgi | T2 |
| Serbest nakit akışı | G12 | Bar + çizgi kombo | T2 |
| Operasyonel metrikler | G13 | Çoklu panel | T2/Harici |
| Senaryo karşılaştırması | G14 | Grouped bar | T2 |
| Gelir köprüsü | G19 | Waterfall | T2 |

### Sayfalar 27-31 — Değerleme (4-5 grafik)
| Grafik | Kod | Tür | Kaynak |
|--------|-----|-----|--------|
| ⭐ DCF duyarlılık ısı haritası | G28 | Heatmap | T3 |
| DCF waterfall | G29 | Waterfall | T3 |
| Peer çarpan karşılaştırması | G30 | Grouped bar | T3 |
| Peer scatter (büyüme vs çarpan) | G31 | Scatter | T3 |
| ⭐ Değerleme football field | G32 | Yatay bar range | T3 |

### Toplam: 25 zorunlu + 10 opsiyonel = 25-35 grafik

---

## SAYFA YOĞUNLUK KURALLARI

### İyi Sayfa vs Kötü Sayfa

**KÖTÜ SAYFA (YASAK):**
```
┌─────────────────────────────┐
│ Başlık                      │
│                             │
│ Bir paragraf metin.         │
│                             │
│                             │
│                             │  ← %70 beyaz alan
│                             │
│                             │
│                             │
└─────────────────────────────┘
```

**İYİ SAYFA:**
```
┌─────────────────────────────┐
│ Başlık                      │
│ Paragraf metin, detaylı     │
│ analiz, rakamlarla dolu.    │
│ ┌─────────────────────────┐ │
│ │ Grafik X — [Başlık]     │ │
│ │ [Görsel: bar/çizgi/vs]  │ │
│ │ Kaynak: KAP, BBB.       │ │
│ └─────────────────────────┘ │
│ Devam eden analiz metni,    │
│ karşılaştırma, veri.        │
│ ┌─────────────────────────┐ │
│ │ Tablo X — [Başlık]      │ │
│ │ Satır1  | X | Y | Z     │ │
│ │ Satır2  | X | Y | Z     │ │
│ │ Kaynak: KAP, BBB.       │ │
│ └─────────────────────────┘ │
│ Ek açıklama paragrafı.      │
└─────────────────────────────┘
```

**Kural:** Her sayfa (İçindekiler hariç) en az bir grafik VEYA tablo içermeli.
**İstisna:** Son 4 sayfa tam sayfa grafik olabilir (İlker'in bülten formatı).

---

## İÇERİK TEKRAR KULLANIM ORANLARI

T5 rapor yazımında içerik kaynakları:

| Kaynak | Oran | Kullanım Şekli |
|--------|------|----------------|
| T1 (Araştırma) | %40-50 verbatim | Şirket 101 bölümü büyük ölçüde T1'den kopyalanır |
| T2/T3 (Model/Değerleme) | %30-40 | Tablolar çıkarılır, finansal analiz metni T2 verisinden yazılır |
| Orijinal yazım | %10-20 | Yatırım tezi, senaryo analizi, varsayım açıklamaları |
| T4 (Grafikler) | %100 embed | Tüm T4 PNG'leri rapora gömülür |

---

## BU DOSYANIN DİĞER DOSYALARLA İLİŞKİSİ

```
rapor-sablonu.md (BU DOSYA)
    │
    │  "Rapor neye benzeyecek?" — Fiziksel yapı
    │
    ├── (c2-sablon.md kaldırıldı — pipeline giriş noktası artık SKILL.md §T1-T5)
    │     "T1-T5 pipeline nasıl çalışır?" — Giriş noktası
    │
    ├── task5-rapor-montaj.md
    │     "Rapor NASIL birleştirilir?" — Assembly workflow
    │
    ├── profesyonel-cikti-rehberi.md
    │     "DOCX formatlama kuralları neler?" — Teknik format
    │
    ├── kalite-kontrol-listesi.md
    │     "Rapor hazır mı?" — 60+ madde QC
    │
    └── task4-grafik-uretim.md
          "Grafikler nasıl üretilir?" — Chart kataloğu + Python
```

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-19 | v1.0 — Orijinal initiating-coverage/assets/report-template.md'den BBB/BIST uyarlaması. Sayfa bazlı layout, grafik embed haritası, Türkçe format kuralları, BIST spesifik comps tablosu, IAS 29 uyarıları, yasal uyarı. |
| 2026-03-23 | **v1.1** — Forward BS/CF tahmin sütunu ZORUNLU hale getirildi (en az FY+1T). Konsensüs Karşılaştırma Tablosu eklendi (T1 §13.5 broker rapor çıkarımı). task2-finansal-modelleme.md v1.8 ile cross-reference |
