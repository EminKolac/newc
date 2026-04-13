# Rekabet Analizi Rehberi — Competitive Landscape Framework v1.0

> Moat analizi (SKILL.md) şirketin **kalıcı avantajını** değerlendirir.
> Bu rehber şirketin **mevcut rekabet pozisyonunu** haritalandırır.
> İkisi birbirini tamamlar ama farklı sorulara cevap verir:
> - Moat: "Bu avantaj 5-10 yıl sürer mi?"
> - Competitive: "Bugün rakiplerine göre nerede duruyor?"

---

## Ne Zaman Kullanılır?

- T1 Şirket Araştırması — Bölüm 7 (Rekabet Pozisyonlaması) yazarken
- Peer comps hazırlarken — hangi şirketler gerçekten comparable?
- Sektör raporu hazırlarken — pazar yapısı ve dinamikleri
- Yatırım tezi yazarken — "neden bu şirket, rakipleri değil?" sorusuna cevap

---

## 1. Rakip Haritalandırma

### Adım 1: Rakip Listesi Oluşturma

4 kaynak, sırasıyla taranır:

| Kaynak | Araç | Ne Bulunur |
|--------|------|------------|
| KAP faaliyet raporu "Rekabet" bölümü | PDF okuma | Şirketin kendi tanımladığı rakipler |
| BIST sektör listesi | BBB Finans / KAP | Aynı sektördeki BIST şirketleri |
| Damodaran Industry Data | web_fetch | Sektör ortalamaları, global peer'lar |
| Yahoo Finance "Similar Companies" | `bbb_yfinance.py quote {TICKER}` | Yurt dışı peer önerileri |

### Adım 2: Rakip Sınıflandırma

Her rakip 3 kategoriden birine atanır:

| Kategori | Tanım | Analiz Derinliği |
|----------|-------|-----------------|
| **Doğrudan rakip** | Aynı ürün/hizmet, aynı müşteri segmenti | Tam analiz (metrik tablosu + kalitatif) |
| **Dolaylı rakip** | Alternatif çözüm sunan | Özet analiz (metrik tablosu) |
| **Potansiyel tehdit** | Bugün değil ama yarın rakip olabilecek | Kısa not (neden tehdit, ne zaman?) |

### Adım 3: Minimum Sayılar

| Analiz Türü | Doğrudan | Dolaylı | Potansiyel | Toplam |
|------------|----------|---------|------------|--------|
| Tam yatırım tezi (T1) | 3-5 | 2-3 | 1-2 | 6-10 |
| Çeyreklik update | 2-3 | — | — | 2-3 |
| Hızlı analiz | 2-3 | 1-2 | — | 3-5 |
| Sektör raporu | 4-6 | 3-4 | 2-3 | 9-13 |

---

## 2. Pozisyonlama Matrisi (2×2)

### Axis Seçimi — Sektöre Göre

Hangi iki boyutun o sektörde en belirleyici olduğunu seç:

| BIST Sektörü | Önerilen Eksenler | Neden |
|-------------|-------------------|-------|
| **Bira/İçecek** | Pazar Payı × Premiumlaşma | Duopol yapıda pazar payı kritik, premiumlaşma marj sürücüsü |
| **Bankacılık** | ROE × Aktif Büyümesi | Kârlılık kalitesi + büyüme hızı |
| **Havacılık** | Load Factor × Birim Maliyet (CASK) | Operasyonel verimlilik iki boyutu |
| **Çimento** | Kapasite × Ton Başı FAVÖK | Ölçek ve kârlılık |
| **Otomotiv** | İhracat Payı × Birim EBITDA | Uluslararası rekabet gücü |
| **Perakende** | Mağaza Sayısı × m² Başı Satış | Ölçek ve verimlilik |
| **Telecom** | Abone Sayısı × ARPU | Penetrasyon ve monetizasyon |
| **Enerji** | Kurulu Güç × Kapasite Faktörü | Ölçek ve kullanım |
| **Sağlık** | Yatak Sayısı × Doluluk Oranı | Kapasite ve verimlilik |
| **Teknoloji/Platform** | Kullanıcı Sayısı × NDR | Ölçek ve müşteri kalitesi |

**Sektör listede yoksa:** İki kriter seç: (1) ölçek/pazar gücü gösteren metrik, (2) verimlilik/kârlılık gösteren metrik.

### Matris Yorumlama

```
         ↑ Yüksek [Metrik 2]
         │
   Q2    │   Q1 ⭐
  (Niche │  (Lider)
  Kârlı) │
         │
────────-┼────────→ Yüksek [Metrik 1]
         │
   Q3    │   Q4
  (Zayıf)│  (Ölçek var
         │   marj yok)
         ↓ Düşük [Metrik 2]
```

| Quadrant | Pozisyon | İmplikasyon |
|----------|---------|-------------|
| Q1 (sağ üst) | **Lider** — ölçek + kârlılık | En güçlü rekabet pozisyonu |
| Q2 (sol üst) | **Niche/Premium** — düşük ölçek, yüksek kârlılık | Savunulabilir ama büyüme sınırlı |
| Q3 (sol alt) | **Zayıf** — düşük ölçek, düşük kârlılık | Konsolidasyon hedefi veya çıkış |
| Q4 (sağ alt) | **Ölçek tuzağı** — büyük ama kârsız | Yapısal sorun, marj baskısı |

**Grafik:** `grafik-uret.py` → `comps_scatter_grafigi()` fonksiyonu ile çizilebilir.

---

## 3. Rakip Profil Şablonu

Her doğrudan rakip için iki tablo:

### A. Metrik Tablosu

```
| Metrik | Değer | Kaynak |
|--------|-------|--------|
| Gelir | X mn TL | (KAP FY2024) |
| Gelir Büyümesi (YoY) | %X | (KAP) |
| Brüt Marj | %X | (KAP) |
| EBIT Marjı | %X | (KAP) |
| ROIC | %X | (Hesaplama) |
| Piyasa Değeri | X mn TL | (BBB Finans) |
| Net Borç/FAVÖK | Xx | (Hesaplama) |
| Pazar Payı | %X | (Sektör kuruluşu) |
```

### B. Kalitatif Değerlendirme

```
| Boyut | Değerlendirme |
|-------|---------------|
| İş modeli | [Tek cümle — ne yapıyor, nasıl para kazanıyor] |
| Güçlü yanlar | [2-3 madde] |
| Zayıf yanlar | [2-3 madde] |
| Strateji | [Mevcut öncelikler] |
| Tehdit seviyesi | [Yüksek / Orta / Düşük — neden] |
```

---

## 4. Karşılaştırmalı Analiz Tablosu

Tüm rakipleri tek tabloda karşılaştır:

```
| Boyut | [Target] ★ | Rakip A | Rakip B | Rakip C | Rakip D |
|-------|-----------|---------|---------|---------|---------|
| Ölçek | ●●● X mn | ●●○ Y mn | ●○○ Z mn | ●●○ W mn | ●●● V mn |
| Büyüme | ●●○ %X | ●●● %Y | ●○○ %Z | ●●○ %W | ●○○ %V |
| Kârlılık | ●●● %X | ●○○ %Y | ●●○ %Z | ●○○ %W | ●●○ %V |
| Moat | ●●○ | ●○○ | ●●● | ●○○ | ●●○ |
```

Derecelendirme: ●●● Güçlü | ●●○ Orta | ●○○ Zayıf

**Her derecelendirmenin yanında rakam olmalı.** Sadece ●●● yetmez.

---

## 5. Rekabet Dinamikleri Analizi

### 5A. Pazar Yapısı Değerlendirmesi

| Yapı | HHI Aralığı | BIST Örnekleri |
|------|-------------|----------------|
| Monopol | >2500 | — (Türkiye'de nadir, regüle sektörler hariç) |
| Sıkı oligopol | 1800-2500 | AEFES+TBORG (bira), Telecom üçlüsü |
| Gevşek oligopol | 1000-1800 | Bankacılık (Big 5), Çimento (bölgesel) |
| Rekabetçi | <1000 | Perakende, yazılım |

HHI hesaplama: HHI = Σ(pazar payı %)². Basit: 2 firma ×%50 → HHI = 5000.

### 5B. Konsolidasyon Trendi

| Gösterge | Anlam |
|----------|-------|
| Son 3 yılda M&A aktivitesi artıyor | Konsolidasyon başlıyor |
| Top 5 pazar payı artıyor | Güçlüler güçleniyor |
| Küçük oyuncular çıkıyor/birleşiyor | Sektör olgunlaşıyor |
| Yeni girişler artıyor | Sektör cazip, henüz konsolide değil |

### 5C. Fiyatlama Dinamikleri

| Durum | İmplikasyon |
|-------|-------------|
| Fiyat lideri belirgin | Stabil marjlar, disciplined competition |
| Fiyat savaşı aktif | Marj baskısı, FCF yıkımı |
| Premium segmentasyon | Farklılaşma mümkün, marj koruması |
| Regülasyon ile fiyatlama | Sınırlı fiyatlama gücü (enerji, sağlık) |

---

## 6. Moat ile Entegrasyon

Rekabet analizi tamamlandıktan sonra, moat değerlendirmesini güçlendir:

```
Rekabet Analizi Bulgusu → Moat İmplikasyonu

"Top 2 firma %95 pazar payı" → Pazar Yapısı moat'ı güçlü (duopoly)
"Son 3 yılda 3 yeni girişçi" → Giriş bariyeri moat'ı zayıflıyor
"Müşteri churn %2/ay" → Değiştirme maliyeti moat'ı düşük
"Patent portföyü 50+ aktif" → Münhasır varlık moat'ı güçlü
```

---

## 7. Çıktı Formatı

T1 Bölüm 7'ye ek olarak, bağımsız rekabet analizi gerektiğinde:

**Dosya:** `research/companies/{TICKER}/{TICKER}_competitive.md` (opsiyonel, sadece derin analizde)

**İçerik:**
1. Rakip listesi (sınıflandırılmış)
2. Pozisyonlama matrisi (2×2)
3. Rakip profilleri (metrik + kalitatif)
4. Karşılaştırmalı analiz tablosu
5. Rekabet dinamikleri (yapı, konsolidasyon, fiyatlama)
6. Moat implikasyonu

---

## Sık Yapılan Hatalar

| Hata | Sonuç | Çözüm |
|------|-------|-------|
| "Herkes rakip" yaklaşımı | Peer grubu anlamsız | Doğrudan/dolaylı/potansiyel ayrımı yap |
| Sadece finansal karşılaştırma | Stratejik boyut eksik | Kalitatif değerlendirme ekle |
| Pazar payı verisi olmadan devam | "Lider" iddiası desteksiz | Sektör kuruluşu verisi bul veya `[VERİ YOK]` |
| 2×2 matriste yanlış axis | Sektöre uygun değil | Yukarıdaki sektör-axis tablosunu kullan |
| Statik analiz (tek dönem) | Trend kaçırılır | Min 3Y pazar payı trendi |
| Holding ile operating karıştırma | Yanlış peer grubu | Holding → holding, operating → operating |

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-17 | v1.0 oluşturuldu — Sektörel axis seçimi, rakip sınıflandırma, 2×2 matris spec, HHI yapı, moat entegrasyonu |
