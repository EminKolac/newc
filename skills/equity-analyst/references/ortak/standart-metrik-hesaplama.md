# Standart Metrik Hesaplama Rehberi

**Amaç:** Agent'ın her analizde tutarlı metrik hesaplaması yapması. Kalem kodları İş Yatırım'sine (bbb_financials.py) aittir.

---

## 1. Kalem Kodu Referans Tablosu

### 1A. Bilanço (Balance Sheet)

| Kod | Türkçe İsim | İngilizce | Kullanım |
|-----|------------|-----------|----------|
| `1A` | Dönen Varlıklar | Current Assets | NWC |
| `1AA` | Nakit ve Nakit Benzerleri | Cash & Equivalents | Net Borç, IC |
| `1AB` | Finansal Yatırımlar | Financial Investments | Net Borç (kısa vadeli) |
| `1AC` | Ticari Alacaklar | Trade Receivables | NWC |
| `1AF` | Stoklar | Inventories | NWC |
| `1AK` | Duran Varlıklar (toplam) | Non-Current Assets | IC |
| `1BG` | Maddi Duran Varlıklar | PP&E | CapEx kontrolü |
| `1BFAA` | Kullanım Hakkı Varlıkları | Right-of-Use Assets | Leasing, IFRS 16 |
| `1BL` | Toplam Varlıklar | Total Assets | ROA |
| `2A` | Kısa Vadeli Yükümlülükler | Current Liabilities | NWC |
| `2AA` | Kısa Vadeli Finansal Borçlar | ST Financial Debt | Net Borç |
| `2AAGAA` | Ticari Borçlar | Trade Payables | NWC |
| `2B` | Uzun Vadeli Yükümlülükler | Non-Current Liabilities | — |
| `2BA` | Uzun Vadeli Finansal Borçlar | LT Financial Debt | Net Borç |
| `2N` | Toplam Özkaynaklar | Total Equity | IC, ROE |
| `2O` | Ana Ortaklığa Ait Özkaynaklar | Equity (Parent) | PD/DD, ROE |
| `2OA` | Ödenmiş Sermaye | Paid-in Capital | Pay sayısı türetme |

### 1B. Gelir Tablosu (Income Statement)

| Kod | Türkçe İsim | İngilizce | Kullanım |
|-----|------------|-----------|----------|
| `3C` | Satış Gelirleri (Hasılat) | Revenue | Büyüme, S/C |
| `3CA` | Satışların Maliyeti (−) | COGS | Brüt Marj |
| `3CAB` | Brüt Kâr | Gross Profit | Brüt Marj |
| `3DA` | Pazarlama Giderleri (−) | S&M Expense | Opex analizi |
| `3DB` | Genel Yönetim Giderleri (−) | G&A Expense | Opex analizi |
| `3DC` | Ar-Ge Giderleri (−) | R&D Expense | R&D kapitalizasyon |
| `3DF` | Faaliyet Kârı | Operating Income (EBIT) | ROIC, NOPAT |
| `3HACA` | Finansman Gideri Öncesi Faaliyet Kârı | EBITDA proxy | — |
| `3HB` | Finansal Gelirler | Finance Income | — |
| `3HC` | Finansal Giderler (−) | Finance Expense | ICR |
| `3I` | Vergi Öncesi Kâr | Pretax Income | Efektif vergi |
| `3IA` | Vergi Gideri | Tax Expense | Efektif vergi oranı |
| `3J` | Dönem Net Kârı | Net Income | ROE, EPS |

### 1C. Nakit Akış Tablosu (Cash Flow)

| Kod | Türkçe İsim | İngilizce | Kullanım |
|-----|------------|-----------|----------|
| `4B` | Amortisman Giderleri | D&A | EBITDA |
| `4BC` | Yurtiçi Satışlar | Domestic Revenue | Coğrafi kırılım |
| `4BD` | Yurtdışı Satışlar | International Revenue | Coğrafi kırılım, CRP |
| `4C` | İşletme Faaliyetlerinden Nakit | Operating Cash Flow (OCF) | FCF |
| `4CAB` | Amortisman & İtfa | D&A (CFS) | EBITDA cross-check |
| `4CAI` | Sabit Sermaye Yatırımları (CapEx) | Capital Expenditure | FCF, S/C |
| `4CAK` | Yatırım Faaliyetlerinden Nakit | Investing CF | — |
| `4CB` | Serbest Nakit Akım | Free Cash Flow (API) | FCF cross-check |
| `4CBB` | Temettü Ödemeleri | Dividends Paid | Temettü verimi |
| `4CBE` | Finansman Faaliyetlerinden Nakit | Financing CF | — |
| `4BE` | Net Yabancı Para Pozisyonu | Net FX Position | Kur riski |

---

## 2. Standart Metrik Formülleri

### 2A. ROIC — Return on Invested Capital

**Varsayılan formül (Damodaran):**

```
NOPAT = Faaliyet Kârı × (1 − Efektif Vergi Oranı)
      = 3DF × (1 − |3IA / 3I|)

Invested Capital = Toplam Özkaynaklar + Toplam Finansal Borç − Nakit
                 = 2N + (2AA + 2BA) − 1AA

ROIC = NOPAT / Invested Capital
```

**⚠️ Şirket Tipi İstisnaları:**

| Şirket Tipi | ROIC Uyarlaması | Neden |
|-------------|-----------------|-------|
| **Bankalar** | ROIC kullanılmaz → **ROE** (3J / 2O) | Borç = hammadde, IC anlamsız |
| **Holding** | Konsolide IC aldatıcı → **her iştirak ayrı** veya NAV | İştirakler arası sermaye transferi |
| **IFRS 16 ağırlıklı** (havayolu, perakende) | IC'ye `1BFAA` (RoU) dahil et → IC = 2N + 2AA + 2BA + 1BFAA − 1AA | Leasing = operasyonel yatırım |
| **IAS 29 ülkeleri** | Şirketin kendi USD raporlamasını kullan | TRY düzeltmeli rakamlar yanıltıcı |
| **R&D yoğun** | R&D kapitalize et → NOPAT'a geri ekle | 3DC gider yazılmış ama aslında yatırım |

**Önemli:** Ortalama IC kullan (dönem başı + dönem sonu) / 2. Tek dönem IC tek başına yanıltıcı olabilir.

### 2B. FCF — Free Cash Flow

**Varsayılan formül:**

```
FCF = İşletme Faaliyetlerinden Nakit − CapEx
    = 4C − |4CAI|

Not: 4CAI negatif sayı olarak gelir (harcama), mutlak değerini al.
```

**Cross-check:** API'nin kendi `4CB` (Serbest Nakit Akım) değeriyle karşılaştır. Fark > %5 ise nedenini araştır.

**FCF Marjı:**
```
FCF Marjı = FCF / Hasılat = (4C − |4CAI|) / 3C
```

**⚠️ Şirket Tipi İstisnaları:**

| Şirket Tipi | FCF Uyarlaması | Neden |
|-------------|----------------|-------|
| **Bankalar** | FCF kullanılmaz → **temettü kapasitesi** (sermaye yeterliliği) | Banka nakit akışı farklı yapıda |
| **IFRS 16 ağırlıklı** | Leasing ödemeleri OCF'den düşürülüyor (IFRS 16) — gerçek operasyonel FCF daha yüksek. Karşılaştırmada dikkat | Pre-IFRS 16 vs post fark büyük |
| **Yüksek büyüme** | Negatif FCF ≠ kötü (eğer CapEx → büyüme yatırımı). CapEx'i maintenance vs growth olarak ayır | Yatırım dönemi normal |
| **Döngüsel** | Tek yıl FCF yanıltıcı → 3-5Y ortalama FCF kullan | Emtia fiyat dalgalanması |

### 2C. EBITDA

```
EBITDA = Faaliyet Kârı + Amortisman
       = 3DF + 4B

Alternatif (CFS bazlı):
EBITDA = 3DF + 4CAB
```

**⚠️ FAVÖK vs EBITDA:** Türk muhasebe pratiğinde FAVÖK = EBITDA. Ancak bazı şirketlerde "FVÖK" (3DF) kullanılıyor — amortisman hariç. FAVÖK = FVÖK + Amortisman.

### 2D. Net Borç / FAVÖK

```
Net Borç = Toplam Finansal Borç − Nakit
         = (2AA + 2BA) − 1AA

Net Borç / FAVÖK = Net Borç / EBITDA
```

**⚠️ Şirket Tipi İstisnaları:**

| Şirket Tipi | Net Borç Uyarlaması | Neden |
|-------------|---------------------|-------|
| **Bankalar** | KULLANILMAZ → **Tier 1 oranı**, NPL oranı | Borç = mevduat = hammadde |
| **IFRS 16 ağırlıklı** | Leasing borcu (2BA'nın bir kısmı) dahil mi hariç mi? → RAPORDA BELİRT | Pre/post IFRS 16 karşılaştırma bozulur |
| **Holding** | Konsolide Net Borç aldatıcı → **iştirak bazlı** raporla | Bir iştirak borçsuz, diğeri batık olabilir |
| **Nakit zengini** | Net Borç negatif = net nakit pozisyon → Net Borç/FAVÖK anlamsız, "net nakit X milyar TL" yaz | TBORG, bazı teknoloji şirketleri |
| **Finansal yatırımlar yüksek** | 1AB'yi de düşür mü? → Sadece kısa vadeli, kolayca nakde çevrilebilir finansal yatırımlar. Uzun vadeli (1BC) dahil etme | Likidite testi |

**Kural:** Net Borç negatif ise → "Net nakit pozisyon: X milyar TL" yaz. Oran hesaplama.

### 2E. Brüt Marj, EBIT Marjı, Net Marj

```
Brüt Marj    = 3CAB / 3C     (Brüt Kâr / Hasılat)
EBIT Marjı   = 3DF / 3C      (Faaliyet Kârı / Hasılat)
EBITDA Marjı  = (3DF + 4B) / 3C
Net Marj     = 3J / 3C       (Net Kâr / Hasılat)
```

### 2F. ROE — Return on Equity

```
ROE = Net Kâr / Ana Ortaklık Özkaynakları
    = 3J / 2O

Önemli: 2O kullan (ana ortaklık), 2N değil (azınlık dahil toplam).
Ortalama kullan: (dönem başı 2O + dönem sonu 2O) / 2
```

### 2G. Sales/Capital (Damodaran Reinvestment Proxy)

```
Sales/Capital = Hasılat / Invested Capital
             = 3C / IC

IC = 2N + (2AA + 2BA) − 1AA
```

Bu oran Damodaran'ın FCFF modelinde reinvestment oranını türetmek için kullanılır. Yüksek S/C = düşük sermaye yoğunluğu = aynı büyümeyi daha az yatırımla sağlayabilir.

### 2H. Interest Coverage Ratio (ICR)

```
ICR = EBIT / Finansal Giderler
    = 3DF / |3HC|

Not: 3HC negatif gelir, mutlak değerini al.
```

**Kullanım:** Sentetik kredi notu (synthetic rating) için → dcf_tools/synthetic_rating.py
**Dikkat:** 3HC'ye kur farkı zararları dahilse ICR çöker → sentetik Kd şişer. Gerçek kredi notunu baz al, sentetik sadece cross-check.

### 2I. EPS — Earnings Per Share

```
EPS = Net Kâr / Pay Sayısı
    = 3J / (2OA / 1 TL nominal)

BIST'te: Ödenmiş Sermaye (2OA) = Pay Sayısı × 1 TL nominal
Pay Sayısı = 2OA (TL cinsinden)
```

**Dikkat:** Bazı şirketlerde nominal değer 1 TL değildir — şirket bazında kontrol et.

### 2J. PD/DD — Fiyat/Defter Değeri (P/BV)

```
Defter Değeri = Ana Ortaklık Özkaynakları / Pay Sayısı
             = 2O / 2OA

PD/DD = Hisse Fiyatı / Defter Değeri

Piyasa Değeri / Defter Değeri = Market Cap / 2O
```

### 2K. FD/FAVÖK — Enterprise Value / EBITDA

```
Enterprise Value = Piyasa Değeri + Net Borç − Azınlık Payları (opsiyonel)
                 = (Fiyat × Pay Sayısı) + (2AA + 2BA − 1AA)

FD/FAVÖK = EV / EBITDA = EV / (3DF + 4B)
```

**Hisse fiyatı:** `bbb_financials.py {TICKER} --price` ile çek.

---

## 3. TTM (Trailing Twelve Months) Hesaplama

```
TTM = Son Kümülatif Dönem + (Önceki FY − Önceki Yılın Aynı Kümülatif Dönemi)

Örnek (Q3-2025 en son veri):
TTM Hasılat = 9M-2025 + (FY2024 − 9M-2024)
            = (Q1+Q2+Q3 2025) + Q4 2024

⚠️ BİLANÇO KALEMLERİNE TTM UYGULANMAZ — son çeyrek sonu değeri kullanılır.
```

**Not:** bbb_financials.py kümülatif veri döndürür (Q3 = 9 aylık toplam). Çeyreklik izole değer istiyorsan:
```
Q3 izole = Q3 kümülatif − Q2 kümülatif
```

---

## 4. Hesaplama Kontrol Listesi

Her metrik hesaplamasından sonra şu kontrolleri yap:

| # | Kontrol | Ne Yapılacak |
|---|---------|-------------|
| 1 | **Birim tutarlılığı** | Tüm kalemler aynı birimde mi? (bin TL vs TL vs milyon TL) |
| 2 | **Dönem eşleşmesi** | Gelir tablosu TTM ↔ Bilanço son çeyrek sonu? |
| 3 | **İşaret kontrolü** | Gider kalemleri negatif mi? (3CA, 3DA, 3DB, 3HC, 4CAI) |
| 4 | **Cross-check** | Hesaplanan EBITDA ≈ 3HACA? FCF ≈ 4CB? |
| 5 | **Sektör karşılaştırma** | ROIC sektör ortalamasından çok farklıysa neden? |
| 6 | **IAS 29 kontrolü** | Şirket IAS 29 kapsamında mı? → Düzeltmeli rakamları spot kurla USD'ye çevirme |
| 7 | **Şirket tipi** | Banka/holding/IFRS 16 istisnası geçerli mi? |

---

## 5. Yaygın Hatalar (Kaçınılacaklar)

| # | Hata | Sonucu | Doğrusu |
|---|------|--------|---------|
| 1 | NOPAT'ta 3J (Net Kâr) kullanmak | Finansal gelir/gider dahil oluyor → ROIC bozulur | 3DF (Faaliyet Kârı) kullan |
| 2 | IC'de 1AA yerine 1A (Dönen Varlıklar) çıkarmak | IC anlamsız şişer | Sadece nakit ve nakit benzerleri (1AA) çıkar |
| 3 | Banka için Net Borç/FAVÖK hesaplamak | Mevduat = borç değil, hammadde | ROE ve F/DD kullan |
| 4 | IAS 29 TRY rakamları × spot kur = USD | %30-70 sapma | Şirketin kendi USD raporlaması |
| 5 | FCF'te 4CAI'yi pozitif almak | FCF şişer (CapEx zaten negatif sayı) | Mutlak değer al: FCF = 4C − \|4CAI\| |
| 6 | TTM'yi bilanço kalemine uygulamak | Anlamsız | Bilanço = son çeyrek sonu noktasal değer |
| 7 | ROE'de 2N (toplam özkaynak) kullanmak | Azınlık payları dahil → ROE düşer | 2O (ana ortaklık) kullan |
| 8 | ICR'da kur farkı zararı dahil 3HC kullanmak | ICR çöker → sentetik Kd şişer | Gerçek kredi notunu baz al |

---

## 6. Hızlı Hesaplama Şablonu

Bir şirketi ilk kez değerlendirirken şu 6 metriği hesapla:

```
# BBB Finans'tan veri çek
cd ~/.openclaw/workspace/skills/bbb-finans/scripts
python3 bbb_financials.py {TICKER} --section all --full

# Hesapla:
1. ROIC    = [3DF × (1 − |3IA/3I|)] / [2N + 2AA + 2BA − 1AA]
2. FCF     = 4C − |4CAI|
3. Brüt Marj = 3CAB / 3C
4. Net Borç/FAVÖK = (2AA + 2BA − 1AA) / (3DF + 4B)
5. Ciro Büyümesi = (3C_bu_yıl / 3C_geçen_yıl) − 1
6. ROE    = 3J / 2O
```

**⚠️ Şirket tipi kontrolü:**
- Banka → 1, 2, 4 kullanılmaz. ROE + F/DD + NPL + Tier 1
- Holding → 1 konsolide aldatıcı. İştirak bazlı veya NAV
- IFRS 16 ağırlıklı → 1'de IC'ye RoU (1BFAA) ekle

**Veto metrikleri (red flag ise diğerleri ne olursa olsun dikkat):**
- ROIC < %10 → Sermaye verimliliği düşük
- FCF < 0 (3+ yıl kronik) → Para yakıyor
- Net Borç/FAVÖK > 4x → Aşırı kaldıraç

---

*Son güncelleme: 2026-03-18. Kalem kodları İş Yatırım (bbb_financials.py) referanslıdır.*
*THYAO FY2024 verileriyle doğrulanmıştır.*
