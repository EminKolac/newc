# Grafik Uretim Rehberi — T4 Detayli Workflow v3.1

Bu dokuman equity-analyst skill'inin T4 (Grafik Uretim) task'ini adim adim yurutme talimati olarak tanimlar.

## Gorev Ozeti

**Amac**: 25-35 profesyonel finansal grafik uret.
**Cikti**: PNG dosyalari (300 DPI), chart index, charts_v2/ klasorunde.

**On Kosullar**: ⚠️ Baslamadan once dogrula — TUM ONCEKI TASK'LAR GEREKLI
- **Zorunlu**: T1'den sirket arastirma dokumani
- **Zorunlu**: T2'den finansal model
- **Zorunlu**: T3'ten degerleme analizi
- **Zorunlu**: Harici veri erisimi (fiyat verileri)

**⚠️ KRITIK: TASK 1, 2 VE 3 TAMAMLANMADAN BU TASK'I BASLATMA**

Bu task onceki tum calisma urunlerinden veri cikarir. Eksik veriyle baslama — eksik chart uretir.

**EGER TASK 1, 2 VEYA 3'TEN HERHANGI BIRI TAMAMLANMADIYSA**: Dur ve kullaniciya bildir:
- Task 1: Sirket arastirma dokumani (9 chart icin veri saglar)
- Task 2: Finansal model (8 chart icin veri saglar)
- Task 3: Degerleme analizi (6 chart icin veri saglar)
- Harici veri: Fiyat verileri (2 chart icin veri saglar)

Placeholder chart olusturmaya veya eksik veriyle chart uretmeye TESEBBÜS ETME.

---

## Girdi Dogrulama (HARD STOP)

### Task 1 Dogrulama (Sirket Arastirmasi)
- [ ] T1 dokumani mevcut? (`{TICKER}_research.md`, 6-8K kelime)
- [ ] Sirket tarihcesi ve milestones dokumante edilmis? (G05, G06)
- [ ] Yonetim ekibi ve organizasyon yapisi tarif edilmis? (G07)
- [ ] Urun/hizmet portfoyu detaylandirilmis? (G08)
- [ ] Musteri segmentasyonu analiz edilmis? (G09)
- [ ] Rekabet analizi tamamlanmis? (G16, G17, G18)
- [ ] Pazar buyuklugu (TAM) analizi tamamlanmis? (G15)

### Task 2 Dogrulama (Finansal Model)
- [ ] T2 dokumani/modeli mevcut?
- [ ] Urun/segment bazli gelir kirilimi var? (G03 ⭐)
- [ ] Cografi gelir kirilimi var? (G04 ⭐)
- [ ] Tarihsel + tahmini finansallar tamam? (G02, G10, G11, G12)
- [ ] Senaryo analizi (Boga/Temel/Ayi) tamam? (G14)
- [ ] Operasyonel metrikler mevcut? (G13)

### Task 3 Dogrulama (Degerleme)
- [ ] T3 degerleme analizi tamam?
- [ ] DCF sensitivity matrisi mevcut? (G28 ⭐)
- [ ] DCF hesaplama detaylari mevcut? (G29)
- [ ] Emsal sirket (comps) verileri toplanmis? (G30, G31)
- [ ] Degerleme araliklari hesaplanmis? (G32 ⭐)
- [ ] Hedef fiyat senaryolari mevcut? (G33)

### Harici Veri Dogrulama
- [ ] yfinance ile hisse fiyat verisi çekilebildi? `yf.Ticker('{TICKER}.IS').history(period='1y')` (G01 — ZORUNLU gerçek veri)
- [ ] Tarihsel carpan verisine erisilebiliyor? (G34 — opsiyonel)

**HERHANGI BIR DOGRULAMA BASARISIZSA**: Dur ve eksik task'i once tamamla.

---

## Renk Paleti & Stil

### BBB Standart Palet

```python
BBB_COLORS = {
    'primary': '#f7931a',     # BBB turuncu (ana renk)
    'secondary': '#2E75B6',   # Orta mavi
    'accent': '#BDD7EE',      # Acik mavi
    'positive': '#548235',    # Yesil (iyi)
    'negative': '#C00000',    # Kirmizi (kotu)
    'warning': '#FFC000',     # Sari (dikkat)
    'neutral': '#808080',     # Gri
    'background': '#FFFFFF',  # Beyaz
    'text': '#333333',        # Koyu gri
    'orange': '#f7931a',      # BBB turuncu (brand vurgu)
}

BBB_PALETTE = ['#f7931a', '#4d4d4d', '#0d579b', '#329239', '#C00000',
               '#7030A0', '#BDD7EE', '#D9E2F3']
```

**Brand Renk Notu:** BBB standart paleti #f7931a turuncu bazlidir. Tum grafikler bu paleti kullanir:
1. `BBB_COLORS['primary']` yerine sirket brand rengi
2. Palet varyasyonlarini uyumlu tut
3. Raporun geri kalaniyla (rapor-uret.py) tutarlilik sagla

### Genel Ayarlar

```python
DPI = 300           # DOCX icin 300, blog/web icin 150
FIG_WIDTH = 10      # Standart genislik (inch)
FIG_HEIGHT = 6      # Standart yukseklik (inch)
TITLE_SIZE = 14     # Baslik font boyutu
AXIS_SIZE = 11      # Eksen etiketi font boyutu
LABEL_SIZE = 10     # Veri etiketi font boyutu
SOURCE_SIZE = 9     # Kaynak notu font boyutu
```

### Ilker'in Grafik Tercihleri (BBB DNA)

- **Minimalist** — fazla susleme, gradient, 3D efekt yok
- **Turuncu tonlari** — BBB marka rengi (#f7931a primary)
- **Veri etiketleri** — grafigin ustunde, net okunabilir
- **Turkce** — baslik, etiket, kaynak notu hep Turkce
- **Target sirket vurgusu** — koyu renk, diger peer'lar acik renk
- **Kaynak notu** — HER grafigin altinda kaynak yazilmali
- **Baslik = Icgoru** — "Brut Marj Grafigi" degil, "Brut marj 5 yilda 800bp genisledi"
- **`[GRAFIK: ...]` direktifi YASAK** — metin icinde organik referans: "Grafik 3'te goruldugu uzere..."
- **Tarihsel vs Tahmin ayirimi** — dikey kesikli cizgi + "Tahmin →" etiketi
- **Kaynak notunda tahmin yili belirt** — "BBB tahminleri" degil, "2026-27 BBB tahminleri" seklinde hangi yillarin tahmin oldugu acik yazilmali. Sadece gercek veri iceren grafiklerde "BBB tahminleri" ifadesi kullanilmamali.
- **X-ekseni tam sayi zorlamasi** — Yil ekseni kullanan grafikler `_tamsayi_eksen(ax)` veya `ax.set_xticks()` ile tam sayi tick zorlayacak, 2024.5 gibi anlamli olmayan aralik degerler engellenecek. Az veri noktali (2-3) grafikler kategorik x-ekseni kullanmali.
- **Donut chart'ta renk cakismasi onleme** — `pazar_payi_grafigi()` hedef sirket turuncu, diger dilimler turuncusuz paletten secilmeli. Ayni renk farkli verilere atanmamali.
- **Ok isareti zorder** — Timeline grafiklerde annotation zorder > marker zorder olmali (ok ucu noktanin altinda kalmamali). `arrowstyle='-|>'` ile belirgin ok ucu.
- **Farkli olcek verileri ayri panellere** — CCC (gun) ve Stok Devir (gun) gibi olcegi farkli metrikleri ayni Y-eksenine koymak yerine 2-panel subplot kullan.
- **TAM/SAM/SOM** — legend'da acilim belirt: TAM (Toplam Erisilebilir Pazar), SAM (Ulasilabilir Pazar), SOM (Elde Edilebilir Pazar)
- **Degerleme terminolojisi** — "Ozkaynak Degeri" degil "Ozsermaye Degeri" (Equity Value). Bilanco baglaminda "Ozkaynaklar" dogrudur.

---

## Chart Katalogu — 25 Zorunlu + 10 Opsiyonel

### ⭐ 4 ZORUNLU Chart (Olmazsa Olmaz)

| # | Chart | Tur | Kaynak | Python Fonksiyonu |
|---|-------|-----|--------|-------------------|
| G03 | **Gelir Segment Kirilimi** | Stacked Area | T2: Gelir modeli | `gelir_stacked_area()` veya `gelir_segment_grafigi()` |
| G04 | **Gelir Cografi Kirilim** | Stacked Bar | T2: Gelir modeli | `gelir_stacked_bar()` |
| G28 | **DCF Sensitivity** | Heatmap | T3: Degerleme | `dcf_sensitivity_grafigi()` |
| G32 | **Degerleme Aralik Grafigi** | Yatay Cubuk | T3: Degerleme | `football_field_grafigi()` |

### 25 Zorunlu Chart — Tam Liste + Fonksiyon Esleme

**Yatirim Ozeti (1 chart):**

| # | Chart | Tur | Veri Kaynagi | Python Fonksiyonu | Boyut |
|---|-------|-----|-------------|-------------------|-------|
| G01 | Hisse Fiyat Performansi (1Y) | Line + benchmark | **yfinance zorunlu** (`{TICKER}.IS` + `XU100.IS`) | `hisse_fiyat_grafigi()` | KUCUK (S.1) |

**Finansal Performans (7 chart):**

| # | Chart | Tur | Veri Kaynagi | Python Fonksiyonu | Boyut |
|---|-------|-----|-------------|-------------------|-------|
| G02 | Gelir & Marj Trendi | Bar + % overlay | T2: Gelir tablosu | `gelir_marj_grafigi()` | TAM |
| G03 | Gelir Segment Kirilimi ⭐ | Stacked Area | T2: Gelir modeli | `gelir_stacked_area()` | TAM |
| G04 | Gelir Cografi Kirilim ⭐ | Stacked Bar | T2: Gelir modeli | `gelir_stacked_bar()` | TAM |
| G10 | Brut Marj Evrimi | Line | T2: Gelir tablosu | `marj_evrimi_grafigi()` | YARIM |
| G11 | EBIT Marji Trendi | Line | T2: Gelir tablosu | `marj_evrimi_grafigi()` | YARIM |
| G12 | Serbest Nakit Akisi | Bar | T2: Nakit akis | `fcf_bar_grafigi()` | YARIM |
| G14 | Senaryo Karsilastirma (Boga/Temel/Ayi) | Grouped Bar | T2: Senaryolar | `senaryo_karsilastirma_grafigi()` | TAM |

**Sirket Derinlemesine (7 chart):**

| # | Chart | Tur | Veri Kaynagi | Python Fonksiyonu | Boyut |
|---|-------|-----|-------------|-------------------|-------|
| G05 | Sirket Genel Bakis / Zaman Cizelgesi | Timeline | T1: Sirket tarihcesi | Ozel kod gerekli | TAM |
| G06 | Milestones & Buyume | Timeline + bar | T1: Tarihce | Ozel kod gerekli | TAM |
| G07 | Yonetim / Organizasyon Yapisi | Org chart | T1: Yonetim | Ozel kod gerekli | TAM |
| G08 | Urun/Hizmet Portfoyu | Treemap/Pie | T1: Urunler | `pazar_payi_grafigi()` veya treemap | TAM |
| G09 | Musteri Segmentasyonu | Donut/Pie | T1: Musteriler | `pazar_payi_grafigi()` | YARIM |
| G15 | Pazar Buyuklugu (TAM) Evrimi | Stacked Area | T1: Sektor analizi | `pazar_buyuklugu_grafigi()` | TAM |
| G16 | Rekabet Pozisyonlama Matrisi | Scatter/2x2 | T1: Rekabet | `rekabet_pozisyonlama_grafigi()` | TAM |

**Rekabet & Pazar (2 chart):**

| # | Chart | Tur | Veri Kaynagi | Python Fonksiyonu | Boyut |
|---|-------|-----|-------------|-------------------|-------|
| G17 | Pazar Payi Dagilimi | Pie/Donut | T1: Sektor | `pazar_payi_grafigi()` | YARIM |
| G18 | Rekabet Benchmarking (ROIC, Marj vs peer) | Spider/Radar | T2: Comps | Ozel radar kodu gerekli |TAM |

**Degerleme (7 chart):**

| # | Chart | Tur | Veri Kaynagi | Python Fonksiyonu | Boyut |
|---|-------|-----|-------------|-------------------|-------|
| G28 | DCF Sensitivity Heatmap ⭐ | Heatmap | T3: DCF | `dcf_sensitivity_grafigi()` | TAM |
| G29 | DCF Waterfall (EV → Equity bridge) | Waterfall | T3: DCF | `dcf_waterfall_grafigi()` | TAM |
| G30 | Peer Comps Scatter (Buyume vs Carpan) | Scatter | T3: Comps | `comps_scatter_grafigi()` | TAM |
| G31 | Peer Carpan Karsilastirma | Horizontal Bar | T3: Comps | `peer_karsilastirma_grafigi()` | YARIM |
| G32 | Degerleme Aralik Grafigi ⭐ | Yatay Cubuk | T3: Ozet | `football_field_grafigi()` | TAM |
| G33 | Hedef Fiyat Senaryolari | Bar | T3: Senaryolar | `hedef_fiyat_senaryolari()` | TAM |
| G34 | Tarihsel Carpan Bandi (F/K, FD/FAVOK) | Area/Band | Tarihsel veri | `tarihsel_carpan_bandi()` | TAM |

**Toplam: 25 Zorunlu Chart**

### 10 Opsiyonel Chart (30-35 araligi icin)

| # | Chart | Tur | Ne Zaman | Python Fonksiyonu |
|---|-------|-----|----------|-------------------|
| G13 | Operasyonel Metrikler Dashboard | Multi-panel | Detayli analiz | `operasyonel_dashboard()` |
| G19 | Musteri Edinme Trendi | Line | Dijital/platform sirketleri | Ozel |
| G20 | Birim Ekonomi Evrimi (LTV/CAC) | Dual axis | Platform/SaaS | Ozel |
| G21 | Urun Yol Haritasi | Timeline | Buyume tezi | Ozel |
| G22 | Cografi Genisleme | Map/Chart | Cok ulkeli firmalar | Ozel |
| G23 | Ar-Ge Harcama Trendi | Bar | Ilac/teknoloji | `fcf_bar_grafigi()` adapte |
| G25 | Isletme Sermayesi Trendleri | Line | Uretim/perakende | `marj_evrimi_grafigi()` adapte |
| G26 | Borc Vade Profili | Stacked Bar | Kaldıracli firmalar | Ozel |
| G27 | Ortaklik Yapisi | Pie | Onemli ortaklik degisimi | `pazar_payi_grafigi()` adapte |
| G35 | Kurum Hedef Fiyat Dagilimi | Box/Strip | Konsensus karsilastirma | Ozel |

---

## Veri Kaynagi Esleme (Chart → Task)

Her chart'in verisi hangi onceki task'tan gelir:

### Task 1'den (Sirket Arastirmasi) — 9 chart
| Chart | Veri |
|-------|------|
| G05 | Sirket tarihcesi bolumu |
| G06 | Tarihce + milestones |
| G07 | Yonetim ekibi bolumu |
| G08 | Urun/hizmet portfoyu bolumu |
| G09 | Musteri segmentasyonu bolumu |
| G15 | Pazar firsati (TAM) bolumu |
| G16 | Rekabet analizi bolumu |
| G17 | Rekabet analizi — pazar paylari |
| G18 | Rekabet analizi — kiyaslama verileri |

### Task 2'den (Finansal Model) — 8 chart
| Chart | Veri |
|-------|------|
| G02 | Gelir tablosu — hasilat satiri + FAVOK marji |
| G03 ⭐ | Gelir modeli — urun/segment kirilimi |
| G04 ⭐ | Gelir modeli — cografi kirilim |
| G10 | Gelir tablosu — brut kar / hasilat |
| G11 | Gelir tablosu — EBIT / hasilat |
| G12 | Nakit akis — CFO - CapEx |
| G13 | Birden fazla tab — operasyonel metrikler |
| G14 | Senaryolar tabi — Boga/Temel/Ayi |

### Task 3'ten (Degerleme) — 6 chart
| Chart | Veri |
|-------|------|
| G28 ⭐ | DCF sensitivity tabi / matrisi |
| G29 | DCF hesaplama — EV bilesenleri |
| G30 | Comps — sirket bazli buyume vs carpan |
| G31 | Comps — emsal sirket carpanlari |
| G32 ⭐ | Degerleme ozeti — yontem bazli araliklar |
| G33 | Degerleme ozeti — senaryo bazli hedef fiyatlar |

### Harici Kaynaklardan — 2 chart
| Chart | Veri |
|-------|------|
| G01 | **yfinance zorunlu** — `yf.Ticker('{TICKER}.IS').history(period='1y')` + `XU100.IS` benchmark |
| G34 | Yahoo Finance / BBB Finans — tarihsel F/K, FD/FAVOK |

---

## Adim Adim Chart Uretim Workflow

### Adim 1: Ortam Hazirla

```bash
pip install matplotlib seaborn pandas numpy
```

```python
import os, sys
from importlib.machinery import SourceFileLoader

# grafik-uret.py'yi import et
gu = SourceFileLoader('grafik_uret',
    os.path.expanduser('~/.openclaw/workspace/skills/equity-analyst/scripts/grafik-uret.py')
).load_module()
```

### Adim 2: Kaynak Dosyalari Oku ve Veri Cikar

**T1'den veri cikarmak icin:**
```python
# T1 markdown dosyasini oku
# Sirket tarihcesi, milestones, yonetim, urun portfoyu, 
# musteri segmentasyonu, pazar payi, rekabet verileri cikar
```

**T2'den veri cikarmak icin:**
```python
# T2 finansal analiz dosyasini oku
# Gelir segmentasyonu (urun + cografya), marjlar, FCF,
# senaryo parametreleri cikar
# Veya BBB Finans'tan dogrudan cek:
# python3 bbb_financials.py {TICKER} --dcf --json
```

**T3'ten veri cikarmak icin:**
```python
# T3 degerleme dosyasini oku
# DCF sensitivity matrisi, comps verileri, 
# degerleme araliklari, hedef fiyat senaryolari cikar
```

**Harici veri icin:**
```python
# BBB Finans veya Yahoo Finance'tan fiyat verisi cek:
# python3 bbb_financials.py {TICKER} --price
# python3 bbb_yfinance.py quote {TICKER}
```

### Adim 3: 4 Zorunlu Chart'i Once Olustur ⭐

**Her zaman ilk 4 zorunlu chart'la basla — bunlar ASLA atlanamaz.**

#### G03: Gelir Segment Kirilimi ⭐ ZORUNLU

```python
gu.gelir_stacked_area(
    yillar=[2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027],
    segmentler=[
        [4150, 5200, 6230, 7580, 8050, 9153, 10600, 12200],  # FMCG
        [3985, 4990, 5990, 7300, 7728, 8887, 10300, 11900],  # Tekstil
        [1245, 1560, 1872, 2280, 2415, 2768, 3200, 3700],    # Beslenme
        # ... diger segmentler
    ],
    segment_isimleri=['FMCG', 'Tekstil', 'Beslenme', '...'],
    ticker='EBEBK',
    kayit_yolu='charts_v2/EBEBK_G03_kategori_kirilimi.png',
    dpi=300,
    tahmin_baslangic=2025  # Bu yildan sonrasi tahmin
)
```

**Chart ozellikleri:**
- Tur: Stacked area
- X ekseni: Yillar (5Y tarihsel + 5Y tahmin)
- Y ekseni: Gelir (mn TL)
- Legend: Segment isimleri
- Dikey cizgi: Tarihsel | Tahmin ayirimi
- Kaynak notu: "Kaynak: KAP, Sirket IR, BBB tahminleri"

#### G04: Gelir Cografi Kirilim ⭐ ZORUNLU

```python
gu.gelir_stacked_bar(
    yillar=['FY22G', 'FY23G', 'FY24G', 'FY25G', 'FY26T', 'FY27T'],
    bolge_verileri=[
        [12100, 18100, 23810, 27288, 31600, 36600],  # Turkiye
        [350, 620, 340, 387, 500, 600],               # Yurtdisi
    ],
    bolge_isimleri=['Turkiye', 'Yurtdisi (UK + Erbil)'],
    ticker='EBEBK',
    kayit_yolu='charts_v2/EBEBK_G04_cografi_kirilim.png',
    dpi=300
)
```

**BIST notu:** Cogu BIST sirketi tek pazarlidir (Turkiye %95+). Bu durumda 2 bolge yeterlidir. Cok pazarli sirkette (THY, DOCO) 4-6 bolge kullan.

#### G28: DCF Sensitivity Heatmap ⭐ ZORUNLU

```python
import numpy as np

gu.dcf_sensitivity_grafigi(
    wacc_values=[34.4, 36.4, 38.4, 40.4, 42.4],
    growth_values=[8.4, 9.4, 10.4, 11.6, 12.6],
    price_matrix=np.array([
        [153, 161, 170, 181, 191],
        [128, 134, 141, 149, 157],
        [108, 113, 118, 124, 130],
        [92, 96, 100, 104, 109],
        [81, 84, 87, 91, 95],
    ]),
    save_path='charts_v2/EBEBK_G28_dcf_sensitivity.png'
)
```

**Chart ozellikleri:**
- Tur: Heatmap (RdYlGn renk skalasi)
- Satirlar: AOSM (WACC) degerleri
- Sutunlar: Terminal buyume oranlari
- Hucreler: Hisse basi deger (TL)
- Base case vurgusu: Merkez hucre kalinlasmis

#### G32: Degerleme Aralik Grafigi ⭐ ZORUNLU

```python
gu.football_field_grafigi(
    methods=['INA (DCF)', 'Goreceli\n(Comps)', 'Forward\nFD/FAVOK'],
    low_vals=[81, 85, 110],
    high_vals=[153, 130, 165],
    current_price=63.1,
    target_price=117,
    save_path='charts_v2/EBEBK_G32_football_field.png'
)
```

**Chart ozellikleri:**
- Tur: Yatay cubuk (range barlar)
- Her yontem icin min-max aralik
- Mevcut fiyat: kirmizi kesikli dikey cizgi
- Hedef fiyat: mavi dolu dikey cizgi
- Diamond marker: aralik ortasinda

### Adim 4: Kalan 21 Zorunlu Chart'i Olustur

**Her chart icin: (1) veri cikar, (2) fonksiyon cagir, (3) kaydet**

#### G01: Hisse Fiyat Performansi

**⚠️ ZORUNLU: GERÇEK VERİ KURALI (v4.14)**
G01 fiyat performansı grafiği HER ZAMAN `yfinance` gerçek piyasa verisiyle üretilmelidir.
Placeholder, tahmini veya sentetik fiyat verisi YASAKTIR.

```python
import yfinance as yf
import pandas as pd

# Gerçek veri çek (1 yıllık)
hisse = yf.Ticker('{TICKER}.IS')
bist = yf.Ticker('XU100.IS')
df = pd.DataFrame({
    'hisse': hisse.history(period='1y')['Close'],
    'bist': bist.history(period='1y')['Close']
}).dropna()

gu.hisse_fiyat_grafigi(
    tarihler=df.index.tolist(),
    fiyatlar=df['hisse'].tolist(),
    benchmark_fiyatlar=df['bist'].tolist(),
    ticker='{TICKER}',
    benchmark_adi='BIST-100',
    kayit_yolu='charts_v2/{TICKER}_G01_fiyat_performansi.png'
)
```

**Veri kaynagi:** `yfinance` (birincil, zorunlu). Ticker formatı: `{TICKER}.IS` (BIST), `XU100.IS` (BIST-100).
Fallback: `python3 bbb_financials.py {TICKER} --price` veya `bbb_yfinance.py`

#### G02: Gelir & Marj Trendi

```python
gu.gelir_marj_grafigi(
    years=[2020, 2021, 2022, 2023, 2024, 2025],
    revenue=[8500, 11200, 15800, 22100, 24800, 27675],
    margin=[10.2, 11.5, 12.0, 11.8, 12.5, 12.8],  # FAVOK marji %
    ticker='EBEBK',
    save_path='charts_v2/EBEBK_G02_gelir_brut_marj.png'
)
```

#### G05-G09: Sirket Derinlemesine Chart'lari

Bu chart'lar T1 iceriginden uretilir. Standart fonksiyon olmayabilir — ozel kod gerekebilir.

| Chart | Ozel Gereksinim | Alternatif |
|-------|-----------------|-----------|
| G05: Sirket overview | Infographic/timeline | matplotlib text + patches ile ozel layout |
| G06: Milestones | Timeline | matplotlib axvline + annotations |
| G07: Org chart | Organizasyon semasi | graphviz veya matplotlib tree |
| G08: Urun portfoyu | Treemap veya horizontal bar | `matplotlib.pyplot.barh()` |
| G09: Musteri segmentasyonu | Donut chart | `pazar_payi_grafigi()` adapte et |

**Bu chart'lar icin veri T1'den cikarilir.** T1'de verisi olmayan chart icin:
- "Veri mevcut degil" notu ile ATLA (placeholder DEGIL)
- chart_index.txt'e "ATLANDI — veri yok" olarak kaydet

#### G10-G12: Marj ve Nakit Akis Chart'lari

```python
# G10: Brut Marj
gu.marj_evrimi_grafigi(
    yillar=[2020, 2021, 2022, 2023, 2024, 2025],
    marjlar_dict={
        'Brut Marj': [32.5, 33.8, 34.2, 35.0, 35.8, 36.1],
    },
    ticker='EBEBK',
    kayit_yolu='charts_v2/EBEBK_G10_brut_marj_evrimi.png'
)

# G11: EBIT Marji (ayni fonksiyon, farkli veri)
gu.marj_evrimi_grafigi(
    yillar=[2020, 2021, 2022, 2023, 2024, 2025],
    marjlar_dict={
        'EBIT Marji': [8.2, 9.5, 10.0, 9.8, 10.5, 10.8],
        'FAVOK Marji': [10.2, 11.5, 12.0, 11.8, 12.5, 12.8],
    },
    ticker='EBEBK',
    kayit_yolu='charts_v2/EBEBK_G11_favok_marj.png'
)

# G12: FCF
gu.fcf_bar_grafigi(
    yillar=[2020, 2021, 2022, 2023, 2024, 2025],
    fcf_degerleri=[320, 480, 650, 890, 1100, 1429],
    ticker='EBEBK',
    kayit_yolu='charts_v2/EBEBK_G12_fcf.png',
    tahmin_baslangic=2025
)
```

#### G13-G14: Operasyonel ve Senaryo

```python
# G14: Senaryo Karsilastirma
gu.senaryo_karsilastirma_grafigi(
    metrikler=['Hasilat\n(mrd TL)', 'FAVOK\n(mrd TL)', 'FAVOK\nMarji %', 'Hedef\nFiyat TL'],
    bear=[28.5, 3.1, 10.9, 81],
    base=[32.1, 3.8, 11.8, 117],
    bull=[36.0, 4.7, 13.1, 153],
    ticker='EBEBK',
    kayit_yolu='charts_v2/EBEBK_G14_senaryo_karsilastirma.png'
)
```

#### G15-G18: Pazar ve Rekabet Chart'lari

```python
# G15: Pazar Buyuklugu
gu.pazar_buyuklugu_grafigi(
    yillar=[2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027],
    tam=[15, 18, 22, 27, 32, 38, 45, 52],  # TAM (milyar TL)
    sam=[8, 10, 12, 15, 18, 21, 25, 29],   # SAM
    birim='mrd TL',
    kayit_yolu='charts_v2/EBEBK_G15_pazar_buyuklugu.png'
)

# G16: Rekabet Pozisyonlama
gu.rekabet_pozisyonlama_grafigi(
    sirketler=['Ebebek', 'Joker', 'Civil', 'Cimpa', 'LC Waikiki'],
    x_deg=[31, 15, 8, 5, 12],     # Pazar payi %
    y_deg=[36.1, 28, 22, 18, 45], # Brut marj %
    x_label='Pazar Payi (%)',
    y_label='Brut Marj (%)',
    hedef='Ebebek',
    kayit_yolu='charts_v2/EBEBK_G16_rekabet_pozisyonlama.png'
)

# G17: Pazar Payi
gu.pazar_payi_grafigi(
    companies=['Ebebek', 'Joker', 'Civil', 'Cimpa', 'Diger'],
    shares=[31, 15, 8, 5, 41],
    ticker='EBEBK',
    save_path='charts_v2/EBEBK_G17_pazar_payi_nielsen.png'
)
```

#### G28-G34: Degerleme Chart'lari

```python
# G29: DCF Waterfall
gu.dcf_waterfall_grafigi(
    kalemler=['EBIT(1-t)', 'Yeniden\nYatirim', 'FCFF', 'Terminal\nDeger', 'Firma\nDegeri', 
              'Net Borc', 'Diger', 'Ozkaynak\nDegeri'],
    degerler=[3200, -1200, 2000, 8500, 10500, -850, -200, 9450],
    kayit_yolu='charts_v2/EBEBK_G29_dcf_waterfall.png'
)

# G30: Comps Scatter
gu.comps_scatter_grafigi(
    companies=['EBEBK', 'MAVI', 'VAKKO', 'CRI', 'MNSO', 'FIVE'],
    growth_rates=[15, 12, 8, 18, 35, 22],
    multiples=[6.2, 7.8, 5.5, 12.3, 15.2, 10.5],
    target_ticker='EBEBK',
    metric_name='FD/FAVOK',
    save_path='charts_v2/EBEBK_G30_comps_scatter.png'
)

# G31: Peer Carpanlar
gu.peer_karsilastirma_grafigi(
    companies=['EBEBK', 'MAVI', 'VAKKO', 'CRI', 'MNSO', 'FIVE'],
    values=[6.2, 7.8, 5.5, 12.3, 15.2, 10.5],
    metric_name='FD/FAVOK',
    target_ticker='EBEBK',
    save_path='charts_v2/EBEBK_G31_peer_carpan.png'
)

# G33: Hedef Fiyat Senaryolari
gu.hedef_fiyat_senaryolari(
    senaryolar={
        'Ayi': {'fiyat': 81, 'olasilik': 25},
        'Temel': {'fiyat': 117, 'olasilik': 50},
        'Boga': {'fiyat': 153, 'olasilik': 25},
    },
    mevcut_fiyat=63.1,
    ticker='EBEBK',
    kayit_yolu='charts_v2/EBEBK_G33_hedef_fiyat.png'
)

# G34: Tarihsel Carpan Bandi
gu.tarihsel_carpan_bandi(
    yillar=[2020, 2021, 2022, 2023, 2024, 2025],
    dusuk=[4.5, 5.0, 4.8, 5.2, 5.5, 5.8],
    yuksek=[8.5, 9.0, 8.8, 9.2, 9.5, 9.8],
    medyan=[6.5, 7.0, 6.8, 7.2, 7.5, 7.8],
    carpan_adi='FD/FAVOK',
    kayit_yolu='charts_v2/EBEBK_G34_tarihsel_carpan.png'
)
```

### Adim 5: Opsiyonel Chart'lari Ekle (25-35 arasi)

T5'te minimum 25 chart gerekli, ideal 30-35. Opsiyonel chart'lardan en uygun olanlari sec:

| Karar Kriteri | Opsiyonel Chart |
|--------------|-----------------|
| Dijital/e-ticaret sirketi | G19 (musteri edinme), G20 (birim ekonomi) |
| Cok ulkeli firma | G22 (cografi genisleme) |
| Ilac/teknoloji | G23 (Ar-Ge) |
| Perakende/uretim | G25 (isletme sermayesi) |
| Kaldıracli firma | G26 (borc vade profili) |
| Ortaklik degisimi | G27 (ortaklik yapisi) |
| Kurum konsensus mevcut | G35 (kurum hedef fiyat dagilimi) |

### Adim 6: Chart Index Olustur

```python
gu.chart_index_olustur(
    klasor='charts_v2/',
    ticker='EBEBK',
    kayit_yolu='charts_v2/chart_index.txt'
)
```

**chart_index.txt icerik formati:**
```
EBEBK GRAFIK DIZINI
====================
4 ZORUNLU GRAFIK (mutlaka mevcut):
- G03: Gelir segment kirilimi (stacked area) ⭐
- G04: Cografi gelir kirilimi (stacked bar) ⭐
- G28: DCF sensitivity (heatmap) ⭐
- G32: Degerleme aralik grafigi (football field) ⭐

25 ZORUNLU GRAFIK:
  EBEBK_G01_fiyat_performansi.png — Hisse Fiyat Performansi
  EBEBK_G02_gelir_brut_marj.png — Gelir & Marj Trendi
  ... (tum chart'lar listelenir)

OPSIYONEL GRAFIKLER:
  ... (varsa listelenir)

ATLANAN GRAFIKLER:
  G07: Organizasyon yapisi — T1'de veri yok
  ... (varsa neden ile listelenir)

Not: T5 rapor assembly'de TUM grafikler (25-35) metin boyunca gomulecek.
Her 200-300 kelimede 1 grafik yogunlugu hedeflenmektedir.
```

### Adim 7: Kalite Kontrol

**Dogrulama calistir:**

```python
import os

def chart_dogrula(klasor='charts_v2/'):
    """Tum chart dosyalarini dogrula"""
    
    zorunlu = [
        f'{klasor}*_G03_*', f'{klasor}*_G04_*',
        f'{klasor}*_G28_*', f'{klasor}*_G32_*'
    ]
    
    # PNG dosyalarini say
    pngs = [f for f in os.listdir(klasor) if f.endswith('.png')]
    
    print("=" * 60)
    print("GRAFIK DOGRULAMA")
    print("=" * 60)
    
    # 1. Zorunlu chart'lar
    print("\n1. ZORUNLU GRAFIKLER:")
    for z in ['G03', 'G04', 'G28', 'G32']:
        found = any(z in f for f in pngs)
        print(f"   {'✓' if found else '✗ EKSIK'}: {z}")
    
    # 2. Toplam sayi
    print(f"\n2. TOPLAM GRAFIK: {len(pngs)}")
    print(f"   Hedef: 25-35")
    print(f"   Durum: {'✓ GECTI' if 25 <= len(pngs) <= 35 else '⚠ UYARI'}")
    
    # 3. Dosya boyutlari (300 DPI icin min ~50KB)
    print("\n3. DOSYA BOYUT KONTROLU:")
    kucuk = []
    for f in pngs[:5]:
        boyut = os.path.getsize(os.path.join(klasor, f)) / 1024
        if boyut < 50:
            kucuk.append(f)
        print(f"   {f}: {boyut:.0f} KB")
    
    if kucuk:
        print(f"   ⚠ UYARI: {len(kucuk)} dosya dusuk cozunurluk olabilir")
    
    # 4. chart_index.txt mevcut mu
    index_var = os.path.exists(os.path.join(klasor, 'chart_index.txt'))
    print(f"\n4. CHART INDEX: {'✓ Mevcut' if index_var else '✗ EKSIK'}")
    
    # Sonuc
    print("\n" + "=" * 60)
    tum_zorunlu = all(any(z in f for f in pngs) for z in ['G03', 'G04', 'G28', 'G32'])
    if tum_zorunlu and len(pngs) >= 25:
        print("✓ DOGRULAMA GECTI — T5 icin hazir")
    else:
        print("✗ DOGRULAMA BASARISIZ — eksikleri tamamla")
    print("=" * 60)

chart_dogrula()
```

---

## Ceyreklik Guncelleme — 8-12 Grafik

Tam tez yerine ceyreklik guncelleme yapiliyorsa, farkli chart seti gerekir:

| # | Chart | Tur | Not |
|---|-------|-----|-----|
| E01 | Ceyreklik Gelir Trendi (8-12Q) | Bar | Son ceyrek vurgulu |
| E02 | Ceyreklik EPS Trendi (8-12Q) | Bar | Beat/miss gosterilir |
| E03 | Marj Trend (Brut + FAVOK + Net) | Multi-line | 8-12Q |
| E04 | Segment/Cografi Kirilim | Stacked bar | Son Q vs YoY |
| E05 | Operasyonel Metrikler | Multi-line | Sirkete ozel KPI |
| E06 | Beat/Miss Waterfall | Waterfall | Gelir + EPS sapma bilesenleri |
| E07 | Tahmin Revizyonu (Eski → Yeni) | Grouped bar | FY tahminleri |
| E08 | Degerleme Bandi (Tarihsel F/K) | Area/Band | Su anki pozisyon |
| E09-12 | Opsiyonel: peer kiyasi, nakit akis, guidance vs street | Cesitli | Gerektiginde |

---

## Grafik Turleri Referansi

### Hangi Chart Tipi Ne Zaman Kullanilir

| Chart Tipi | Kullanim Alani | Ornek |
|-----------|---------------|-------|
| **Line** | Zaman serisi trendleri | Gelir, marjlar, hisse fiyati |
| **Stacked Area** | Bilesim degisimleri | Gelir segmentasyonu ⭐, pazar buyuklugu |
| **Stacked Bar** | Kategori kiyaslama | Cografi gelir ⭐, ceyreklik kirilim |
| **Grouped Bar** | Senaryo karsilastirma | Boga/Temel/Ayi |
| **Horizontal Bar** | Siralama / peer kiyaslama | Peer carpanlar, degerleme aralik |
| **Heatmap** | 2 boyutlu duyarlilik | DCF sensitivity ⭐ |
| **Waterfall** | Kopru / decomposition | DCF build-up, marj bridge |
| **Scatter/Bubble** | Iliski / pozisyonlama | Buyume vs carpan, rekabet matrisi |
| **Pie/Donut** | Dagılım | Pazar payi, ortaklik yapisi |
| **2×2 Matris** | Pozisyonlama | Rekabet, portfoy |
| **Radar/Spider** | Cok boyutlu kiyaslama | Rekabet benchmarking |
| **Multi-panel** | Dashboard | Operasyonel metrikler |
| **Area/Band** | Tarihsel aralik | Carpan bandi |
| **Timeline** | Kronoloji | Sirket tarihcesi, milestones |

---

## Dosya Isimlendirme Standardi

```
{TICKER}_{chart_kodu}_{kisa_aciklama}.png

Ornekler:
EBEBK_G03_kategori_kirilimi.png
EBEBK_G28_dcf_sensitivity.png
EBEBK_G32_football_field.png
EBEBK_E01_ceyreklik_gelir_trendi.png
EBEBK_EK01_magaza_sayisi.png       (ek grafik)
```

**Chart kodu kurali:**
- `G01-G35`: Tam tez chart'lari (25 zorunlu + 10 opsiyonel)
- `E01-E12`: Ceyreklik guncelleme chart'lari
- `EK01-EK10`: Ek chart'lar (rapor-spesifik)

### Kaydetme Konumu
```
research/companies/{TICKER}/charts_v2/    ← Ana charts klasoru
```

---

## Sik Karsilasilan Sorunlar ve Cozumleri

### Sorun 1: Dusuk Cozunurluk
**Problem**: Chart baskida/DOCX'te piksel piksel gorunuyor
**Cozum**: `dpi=300` kullanildigini dogrula. `plt.savefig(..., dpi=300)` veya `gu._kaydet(fig, yol, dpi=300)`

### Sorun 2: Metin Kesilmesi
**Problem**: Baslik veya etiketler kenarlarda kesiliyor
**Cozum**: `bbox_inches='tight'` kullan: `plt.savefig(..., bbox_inches='tight')`

### Sorun 3: Renk Tutarsizligi
**Problem**: Chart'lar arasi farkli renkler
**Cozum**: Her zaman `BBB_PALETTE` kullan, matplotlib varsayilan paletini KULLANMA

### Sorun 4: Ustuste Binen Etiketler
**Problem**: Eksen etiketleri ustuste biniyor
**Cozum**: `rotation=45, ha='right'` ile dondur veya font boyutunu kucult

### Sorun 5: Bos Alan
**Problem**: Chart etrafinda gereksiz bos alan
**Cozum**: `plt.tight_layout()` kaydetmeden once cagir

### Sorun 6: Seaborn/Pandas Eksik
**Problem**: Import hatasi
**Cozum**: `pip install seaborn pandas`. grafik-uret.py bunlar olmadan da calisir (temel fonksiyonlar) ama heatmap (G28) icin seaborn GEREKLI.

### Sorun 7: Turkce Karakter Problemi
**Problem**: Baslik/etiketlerde bozuk karakter
**Cozum**: matplotlib 3.7+ kullan. Gerekirse: `plt.rcParams['font.family'] = 'DejaVu Sans'`

### Sorun 8: Tarihsel vs Tahmin Ayrimi Yok
**Problem**: Grafiklerde gerceklesme ve tahmin ayrimi belli degil
**Cozum**: `tahmin_baslangic` parametresini kullan — fonksiyonlar otomatik dikey kesikli cizgi + "Tahmin →" etiketi ekler

---

## Basari Kriterleri

Basarili bir chart paketi:

1. **Tum 4 zorunlu chart mevcut** (dogrulandi) ⭐
   - G03: Gelir segmentasyonu (stacked area) ⭐
   - G04: Cografi gelir (stacked bar) ⭐
   - G28: DCF sensitivity (heatmap) ⭐
   - G32: Degerleme football field ⭐

2. **Minimum 25 chart olusturuldu** (dogrulandi)
3. **Opsiyonel: 1-10 ek chart** (26-35 toplam)
4. **Tutarli profesyonel stil** — BBB paleti, ayni font boyutlari
5. **Yuksek cozunurluk** — 300 DPI (DOCX icin)
6. **Her chart'ta kaynak notu** — "Kaynak: [spesifik kaynak, tarih]"
7. **Turkce baslik ve etiketler** — G/T notasyonu tutarli
8. **Insight formatinda basliklar** — "Brut marj 5 yilda 800bp genisledi" (konu degil, bulgu)
9. **Tarihsel vs tahmin ayirimi** — dikey kesikli cizgi + etiket
10. **Target sirket vurgusu** — peer grafiklerde koyu renk
11. **chart_index.txt mevcut** — tum chart'lar listelenmis
12. **Dogrulama gecti** — `chart_dogrula()` calistirildi ve GECTI

---

## Cikti Dosyalari

T4 tamamlandiginda:

```
research/companies/{TICKER}/charts_v2/
├── {TICKER}_G01_fiyat_performansi.png
├── {TICKER}_G02_gelir_brut_marj.png
├── {TICKER}_G03_kategori_kirilimi.png          ⭐ ZORUNLU
├── {TICKER}_G04_cografi_kirilim.png             ⭐ ZORUNLU
├── {TICKER}_G05_sirket_overview.png
├── {TICKER}_G06_milestones.png
├── {TICKER}_G07_yonetim_yapisi.png
├── {TICKER}_G08_urun_portfoyu.png
├── {TICKER}_G09_musteri_segmentasyonu.png
├── {TICKER}_G10_brut_marj_evrimi.png
├── {TICKER}_G11_favok_marj.png
├── {TICKER}_G12_fcf.png
├── {TICKER}_G13_operasyonel_dashboard.png       (opsiyonel)
├── {TICKER}_G14_senaryo_karsilastirma.png
├── {TICKER}_G15_pazar_buyuklugu.png
├── {TICKER}_G16_rekabet_pozisyonlama.png
├── {TICKER}_G17_pazar_payi_nielsen.png
├── {TICKER}_G18_rekabet_benchmarking.png
├── {TICKER}_G28_dcf_sensitivity.png             ⭐ ZORUNLU
├── {TICKER}_G29_dcf_waterfall.png
├── {TICKER}_G30_comps_scatter.png
├── {TICKER}_G31_peer_carpan.png
├── {TICKER}_G32_football_field.png              ⭐ ZORUNLU
├── {TICKER}_G33_hedef_fiyat.png
├── {TICKER}_G34_tarihsel_carpan.png
├── {TICKER}_EK01-EK07.png                      (ek grafikler, varsa)
└── chart_index.txt
```

**Tum chart dosyalari:**
- 300 DPI cozunurluk (baski kalitesi)
- 10×6 inch standart boyut (DOCX gomme icin)
- Beyaz arka plan
- PNG formati (kayipsiz)
- Word'e dogrudan gomulmeye hazir

---

## T4 → T5 Handoff

T4 tamamlandiginda T5'e aktarilacak bilgiler:
- charts_v2/ klasorunun tam yolu
- chart_index.txt (hangi chart hangi bolumde kullanilacak)
- 4 zorunlu chart'in dosya adlari
- Toplam chart sayisi
- Varsa ATLANAN chart'lar ve nedenleri (T5'te "veri mevcut degil" notu icin)

**T5 task5-rapor-montaj.md'deki Grafik-Bolum Esleme Haritasi bu chart'lari hangi sayfaya/bolume yerlestirecegini tanimlar.**

---

| Tarih | Degisiklik |
|-------|-----------|
| 2026-03-17 | v1.0 olusturuldu — 4 grafik turu, BBB stili |
| 2026-03-17 | v2.0 — 25+10 chart katalogu, ceyreklik chart seti (8-12), 7 Python fonksiyonu, DPI standardi, verification checklist |
| 2026-03-22 | v3.1 — 16 grafik kalite iyilestirmesi: X-ekseni integer fix (_tamsayi_eksen helper), kaynak notu pozisyon fix, renk cakisma onleme (donut), ok ucu zorder, tahmin gosterge standardi, TAM/SAM/SOM acilim, Ozsermaye terminolojisi, 2-panel subplot (G25), G04 yurtdisi pay etiketi |
| 2026-03-19 | v3.0 — Tam yeniden yazim: Input Verification (T1/T2/T3/harici checklist), Veri Kaynagi Esleme (25 chart → 4 kaynak), 7 adimli workflow (ortam → veri cikartma → 4 zorunlu → 21 kalan → opsiyonel → chart index → kalite kontrol), Chart-Fonksiyon esleme tablosu (25 chart × Python fonksiyonu), BIST uyarlamalari (tek pazar notu, G/T notasyonu), 8 sik sorun + cozum, 12 basari kriteri, cikti dosya yapisi, T4→T5 handoff. Orijinal task4-chart-generation.md (920 satir) yapisina uyumlu hale getirildi. |
