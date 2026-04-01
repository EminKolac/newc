# Finansal Modelleme Rehberi — T2 Detaylı Workflow v1.7

> T2 (Finansal Modelleme) task'ının detaylı yürütme rehberi.
> T2 çıktısı → T3 (Değerleme) ve bbb-dcf skill'in Faz 1 DATA_PACK girdisidir.
> DCF hesaplaması → bbb-dcf skill (Faz 2). Bu rehber DCF YAPMAZ.

---

## T2 / bbb-dcf Handoff Kuralı

T2 ve bbb-dcf arasında net bir görev ayrımı var. Çakışma = hata kaynağı.

| İş | T2 (Bu Rehber) | bbb-dcf (Faz 1-2) |
|----|----------------|-------------------|
| Tarihsel finansal tablolar (3-5Y) | ✅ Toplar ve düzenler | Kullanır |
| Gelir segmentasyonu (ürün × coğrafya) | ✅ Kırar ve analiz eder | Büyüme varsayımına girdi |
| Marj analizi ve trend | ✅ Tarihsel trend + peer karşılaştırma | Terminal marj varsayımını belirler |
| TTM hesaplaması | ✅ Hesaplar (kümülatif formül) | Doğrular |
| FCFF/FCFE derivasyonu | ❌ Yapmaz | ✅ Faz 2'de hesaplar |
| WACC hesaplama | ❌ Yapmaz | ✅ Faz 2'de hesaplar |
| 10Y projeksiyon | ❌ Yapmaz | ✅ Faz 2'de yapar |
| Terminal value | ❌ Yapmaz | ✅ Faz 2'de hesaplar |
| Sensitivity analizi | ❌ Yapmaz | ✅ Faz 2'de üretir |
| Senaryo varsayımları (Bull/Base/Bear) | ✅ Hazırlar (parametreler) | Faz 1.5'te onaylanır |
| S/C (Sales/Capital) hesaplama | ✅ Hesaplar | Kullanır |
| ICR, ETR hesaplama | ✅ Hesaplar | Kullanır |

**Kural:** T2 tamamlandığında bbb-dcf Faz 1 DATA_PACK'in finansal veri bölümü hazır olmalı. T2 = veri + analiz. bbb-dcf = değerleme.

---

## Bölüm 0: Temel Metodolojik Referanslar [v1.1]

> Aşağıdaki konular senaryo-metodoloji.md ve bbb-dcf skill dosyalarında **detaylı** olarak tanımlıdır.
> T2 sırasında bu referansları ihlal edecek bir varsayım veya hesaplama yapılmamalıdır.

| Konu | Referans Dosya | Bölüm | T2'de Ne Zaman Geçerli |
|------|---------------|-------|----------------------|
| **Reel vs Nominal baz** | senaryo-metodoloji.md | §0A | Projeksiyon büyüme oranları belirlenirken — reel büyüme + reel WACC VEYA nominal + nominal; ASLA karışık |
| **WACC bileşenleri** | senaryo-metodoloji.md | §0B | DATA_PACK'e Ke/Kd girdileri hazırlanırken — Rf, ERP, CRP, Beta, SFP, MQS kaynakları |
| **Temettü/Payout** | senaryo-metodoloji.md | §0C | Terminal value için payout oranı belirlenirken — TV = NOPAT × (1-g/ROC) / (WACC-g) |
| **Kazanç kalitesi** | senaryo-metodoloji.md | §0D | Tarihsel kâr kalitesini değerlendirirken — 7 maddelik kontrol listesi (CFO/Net Kâr, DSO, Sloan vb.) |
| **Fisher cross-check** | senaryo-metodoloji.md | §0A | Reel↔Nominal dönüşümde tutarlılık kontrolü — (1+Nom)=(1+Reel)×(1+Enf), sapma <%5 |
| **EV FX harmonizasyonu** | karsilastirmali-degerleme.md | §6A | Peer comps hazırlanırken — çarpanlar yerel para biriminde, kur dönüşümü sadece çıktıda |

> **Kural:** T2'de senaryo parametreleri belirlenirken §0A-0D ihlali → **sistemik hata**. Reel büyüme + nominal WACC = %40-60 hedef fiyat sapması.

---

## Ön Koşullar

| Gerekli | Kaynak | Kontrol |
|---------|--------|---------|
| Şirket ticker/isim | İlker'den | ✅ |
| KAP finansal tablolar erişimi | BBB Finans araçları | `bbb_kap.py {TICKER} --kap-summary` çalışıyor mu? |
| Faaliyet raporu (PDF) | KAP veya şirket IR | Segment gelir kırılımı burada |
| **KAP Finansal Tablolar PDF** | KAP bildirimi veya İlker'den | Dipnot doğrulama için zorunlu (bkz. Adım 3G) |
| T1 (Şirket Araştırması) | research/companies/{TICKER}/ | **Zorunlu:** T1 Sentez Notu (research.md sonundaki "## Sentez Notu") okunacak — varsayım kurulurken bağlam sağlar |

### KAP Finansal Tablolar PDF Nedir?

KAP'ta yayınlanan "Finansal Tablolar ve Bağımsız Denetçi Raporu" PDF dosyası. İş Yatırım'dan çektiğimiz 147 kalemin üstüne dipnot detayı verir. T2'nin 4 kritik ihtiyacı bu dosyadan karşılanır:

| Dipnot | Sayfa (tipik) | T2 Kullanımı |
|--------|---------------|-------------|
| NOT: Borçlanmalar | ~S.38 | Efektif faiz oranları → Kd tahmini girdisi |
| NOT: Vergi | ~S.46-47 | Halka arz/teşvik indirimi, ertelenmiş vergi kaynakları → ETR normalizasyonu |
| NOT: Niteliklerine Göre Giderler | ~S.44 | Departman bazlı gider kırılımı (Pazarlama/GYG/Üretim) → OpEx projeksiyonu |
| NOT: İşletme Birleşmeleri/Şerefiye | ~S.31 | Tek seferlik write-down/impairment → Net kar normalizasyonu |
| NOT: Finansal Risk (Döviz) | ~S.51+ | Döviz pozisyon tablosu (USD/EUR/GBP ayrı) → Kur riski değerlendirmesi |
| NOT: İlişkili Taraf | ~S.48 | Transfer fiyatlandırma, ilişkili taraf bakiye → Yönetim kalitesi |

**Dosya konumu:** `research/companies/{TICKER}/{TICKER} {Dönem} Finansal Tablolar.pdf`

**⚠️ İş Yatırım bu bilgileri VERMEZ.** 147 kalem sadece finansal tablo satırlarıdır. Efektif faiz, vergi teşviki, gider kırılımı, döviz pozisyonu gibi dipnot bilgileri YALNIZCA bu PDF'te bulunur.

### 🔴 IAS 29 Veri Hiyerarşisi (Türk Şirketleri İçin Zorunlu)

IAS 29 (TMS 29) uygulayan şirketlerde veri kaynağı seçimi kritiktir. Yanlış kaynak kullanımı YoY büyüme oranlarını 3-4x şişirebilir.

**Hiyerarşi (yukarıdan aşağıya öncelik):**

| # | Kaynak | Komut | Kullanım | Baz Yılı Davranışı |
|---|--------|-------|----------|-------------------|
| 1 | **DCF JSON** (birincil) | `bbb_financials.py {TICKER} --dcf --json` | Tarihsel finansal tablolar (GelirTablosu, Bilanço, NakitAkış) | Her dönem, **son yayımlanan raporun karşılaştırmalısından** alınır. 2025+2024 = Dec 2025 bazında, 2023 = Dec 2024 bazında |
| 2 | **KAP PDF** (doğrulama + dipnot) | Manuel okuma | (a) Güncel dönem cross-check, (b) DİPNOT zenginleştirme | Tek rapor içinde tüm kolonlar aynı bazda (Dec 2025) |
| 3 | **BBB Finans Detay** (referans) | `bbb_financials.py {TICKER} --section all --full` | 147 kalem detaylı tablo, nominal seriler | Nominal (enflasyon düzeltmesiz) |
| 4 | ~~**KAP Summary**~~ | ~~`bbb_kap.py {TICKER} --kap-summary`~~ | ~~**KULLANMA**~~ | ~~Her dönem KENDİ raporunun bazında → YoY karşılaştırma yanıltıcı~~ |

**⚠️ KRİTİK UYARI — `bbb_kap.py --kap-summary` KULLANMA:**

Bu komut her dönemi o dönemin **kendi yıllık raporundan** çeker:
- 2025 verisi → 2025 raporundan (Dec 2025 satın alma gücü)
- 2024 verisi → 2024 raporundan (Dec 2024 satın alma gücü)
- 2023 verisi → 2023 raporundan (Dec 2023 satın alma gücü)

Sonuç: Her dönem **farklı satın alma gücü bazında** → YoY büyüme oranları enflasyon farkını içerir ve **3-4x şişer**. Örnek: EBEBK hasılat büyümesi kap-summary'de %51 görünürken, gerçek reel büyüme %15,4.

**Doğru akış:**
1. `bbb_financials.py --dcf --json` ile tarihsel veri çek
2. Her dönemin baz yılını belgele (footnote ile)
3. KAP PDF'ten güncel dönem gelir tablosu/bilançoyu cross-check et
4. KAP PDF dipnotlarından zenginleştirme yap (NOT 13, 20, 23, 25, 28)
5. Farklı bazdaki dönemler arası YoY büyüme hesaplarken TÜFE katsayısı uygula veya "yaklaşık" notu düş

**TÜFE katsayısı hesaplama:**
```
Katsayı = TÜFE_hedef_baz / TÜFE_kaynak_baz
Örnek: Dec 2024 bazındaki 2023 verisini Dec 2025 bazına taşımak:
  Katsayı = 3.513,87 / 2.684,55 = 1,3088
  2023 Hasılat (Dec 2025 bazında) ≈ 16.400 × 1,3088 ≈ 21.464 M TL
```

**Veri Toplama Komutları:**
```bash
cd ~/.openclaw/workspace/skills/bbb-finans/scripts

# ✅ BİRİNCİL: DCF JSON (programatik, IAS 29 düzeltmeli)
python3 bbb_financials.py {TICKER} --dcf --json > /tmp/{TICKER}_dcf.json

# ✅ REFERANS: Detaylı tablolar (147+ kalem)
python3 bbb_financials.py {TICKER} --start-year 2020 --end-year 2025 --section all --full

# ✅ BİLGİ: Şirket bilgisi
python3 bbb_kap.py {TICKER} --lookup

# ⛔ KULLANMA: KAP summary (baz farkı sorunu)
# python3 bbb_kap.py {TICKER} --kap-summary  ← IAS 29 şirketlerinde YANILTICI
```

---

## Excel Model Standardı — 6 Tab (T5 Assembly İçin Zorunlu)

T2 çıktısı olan Excel model aşağıdaki 6 tab'ı içermelidir. T3 (değerleme) ve T5 (assembly) bu tab'ları kaynak olarak kullanır.

### Tab Yapısı

| # | Tab Adi | Icerik | Satir Hedefi | Not |
|---|---------|--------|-------------|-----|
| 1 | **GelirModeli** | Segment bazli gelir (urun + cografya), 5Y tarihsel + 5Y tahmin | Urun: 5-15 satir, Cografya: 2-10 satir | BIST sirketleri genellikle 3-8 segment; tek pazarli sirkette cografya 2-3 satir yeterli |
| 2 | **GelirTablosu** | Tam P&L: KAP/BIST siralamasi, 5Y tarihsel + 5Y tahmin | **30-40 kalem** | Hasilat → Brut Kar → EBIT → FAVOK → Net Kar + marjlar + buyume oranlari |
| 3 | **NakitAkis** | CFO/CFI/CFF, 5Y tarihsel + 5Y tahmin | **20-30 kalem** | FCF, CapEx/Hasilat, SNA degisimi dahil |
| 4 | **Bilanco** | Varlik/Yukumluluk/Ozkaynak, 5Y tarihsel + 5Y tahmin | **25-35 kalem** | Net Borc, D/E, IC dahil |
| 5 | **Senaryolar** | Boga/Temel/Ayi karsilastirma tablosu | **10-15 metrik** | Hasilat, FAVOK, Marj, YBBO, Hedef Fiyat vb. |
| 6 | **INAGirdileri** | bbb-dcf Faz 2 girdileri: FCFF, WACC parametreleri, terminal varsayimlar | **15-20 parametre** | AOSM, Ke, Kd, Beta, CRP, terminal g, terminal ROIC |

### Veri Availability Kontrolü (Segment/Coğrafya)

**T2 başlangıcında zorunlu kontrol — GelirModeli tab'ının detay seviyesini belirler:**

| Kontrol | Kaynak | EVET → | HAYIR → |
|---------|--------|--------|---------|
| Segment gelir dağılımı mevcut? | IR sunumu, faaliyet raporu | Her segment ayrı satır | Toplam satır + "segment kırılım yok" notu |
| Her segment büyüme beklentisi var? | Management guidance, sektör | Segment bazlı büyüme oranları | Toplam büyüme, gerekcesiyle |
| Coğrafi breakdown mevcut? | KAP faaliyet raporu, IR | Her bölge ayrı satır | Yurtiçi/yurtdışı 2 satır veya "tek pazar" notu |
| Marj bridge faktörleri tanımlanabiliyor? | Tarihsel trend, peer | Faktör bazlı bridge tablosu | Toplam marj trendi + tarihsel baz |

**Bu kontrol sonucu T5'te projeksiyon narratifinin detay seviyesini belirler.**
- Segment MEVCUT → product-by-product narratif (2.000+ kelime)
- Segment KISITLI → toplu büyüme varsayımı + kısa açıklama (500-800 kelime)

### Renk Kodlaması (Endüstri Standardı)

| Renk | Anlam | Örnek |
|------|-------|-------|
| **Mavi metin** | Hardcoded girdi (kullanıcı değiştirebilir) | Büyüme oranı, marj varsayımı |
| **Siyah metin** | Formül/hesaplama | Toplam satırlar, marj %, CAGR |
| **Yeşil metin** | Başka sayfaya link | GelirModeli → GelirTablosu referansı |
| **Kırmızı metin** | Hata/uyarı flag | Negatif EBIT, tutarsızlık |

### Tab Arası Referans Kuralları

- GelirModeli toplam satırı → GelirTablosu Hasılat satırına eşit OLMALI
- NakitAkis Net Kâr → GelirTablosu Net Kâr'a eşit OLMALI
- Bilanco Toplam Varlık = Toplam Yükümlülük + Özkaynak (her dönem)
- INAGirdileri FCFF → NakitAkis'ten türetilmeli (formül ile)

### Excel Formül ve Veri Kuralları (openpyxl ile Üretim)

> **Mevcut durum:** Excel modelleri openpyxl ile hardcoded değerlerle üretiliyor. İleriki hedef: tab arası formül bağlantıları olan dinamik model. Aşağıdaki kurallar aşamalı olarak uygulanacaktır.

**Kural 1 — Hardcoded vs Formül Ayrımı (Renk Kodlu)**

| Hücre Tipi | Renk | openpyxl Örnek | Ne Zaman |
|------------|------|---------------|----------|
| Kullanıcı girdisi (varsayım) | **Mavi metin** | `Font(color="0000FF")` | Büyüme oranı, marj varsayımı, WACC parametresi |
| Hesaplanan değer | **Siyah metin** | `Font(color="000000")` | Toplam, marj %, CAGR, NOPAT |
| Cross-link (başka tab'dan) | **Yeşil metin** | `Font(color="008000")` | GelirModeli → GelirTablosu |
| Hata/uyarı | **Kırmızı metin** | `Font(color="FF0000")` | Negatif EBIT, bilanço dengesizliği |

**Kural 2 — Tab Arası Tutarlılık Doğrulama**

openpyxl ile formül bağlantısı kurulamıyorsa (karmaşıklık nedeniyle), en azından doğrulama satırları ekle:

```python
# Her tab'ın altına doğrulama satırı ekle:
ws['A_last'] = "DOĞRULAMA"
ws['B_last'] = gelir_tablosu_hasilat  # GelirTablosu'ndan
ws['C_last'] = gelir_modeli_toplam    # GelirModeli'nden
ws['D_last'] = "FARK"
ws['E_last'] = gelir_tablosu_hasilat - gelir_modeli_toplam  # 0 olmalı
```

**Kural 3 — Tahmin Yılları Görsel Ayrımı**

| Dönem Tipi | Arka Plan | Not |
|------------|-----------|-----|
| Tarihsel (gerçekleşen) | Beyaz | Değiştirilemez |
| Tahmin (projeksiyon) | Açık sarı | Kullanıcı varsayımlarına bağlı |
| Normalizasyon/düzeltme | Açık mavi | Tek seferlik kalem çıkarılmış |

### Mevcut Durum Notu

`EBEBK_DCF_Model.xlsx` (5 sheet: OZET, DCF, WACC, SENSITIVITY, DIAGNOSTICS) mevcut 6-tab standardından farklıdır. Bu, bbb-dcf scripts tarafından üretilmiş bir DCF-only model. T2'nin tam finansal modeli `{TICKER}_financial_analysis.md` markdown dosyasında tutulmaktadır. İleriki analizlerde Excel'i 6-tab standardına yükseltmek hedeflenmektedir.

---

## Adım 1: Tarihsel Finansal Tablo Düzenleme (3-5Y)

### 1A. Gelir Tablosu Kalemleri (BIST/KAP Sıralama)

BIST şirketleri KAP'ta aşağıdaki sırayı kullanır. İngilizce karşılıklar parantezde.

```
Hasılat
Satışların Maliyeti (COGS)
─────────────────────────────────
BRÜT KÂR (Gross Profit)
  Brüt Kâr Marjı %

Genel Yönetim Giderleri (G&A)
Pazarlama Giderleri (Sales & Marketing)
Araştırma Geliştirme Giderleri (R&D) — varsa
Esas Faaliyetlerden Diğer Gelirler (Other Operating Income)
Esas Faaliyetlerden Diğer Giderler (Other Operating Expenses)
─────────────────────────────────
FAALİYET KÂRI / EBIT (Operating Profit / EBIT)
  EBIT Marjı %

Amortisman & İtfa (D&A) — nakit akıştan çekilir, eklenir
─────────────────────────────────
FAVÖK / EBITDA
  FAVÖK Marjı %

Yatırım Faaliyetlerinden Gelirler/Giderler
Pay Yöntemiyle Değerlenen Yatırımların Kâr/Zararı
Finansman Gelirleri (Finance Income)
Finansman Giderleri (Finance Expense)
  Faiz Gideri (Interest Expense) — ICR hesabı için ayır
  Kur Farkı Gideri — ICR'a DAHİL ETME (bbb-dcf kuralı)
Parasal Kazanç/Kayıp (IAS 29) — EBIT'ten çıkarılmalı
─────────────────────────────────
VERGİ ÖNCESİ KÂR (EBT)

Vergi Gideri (Tax Expense)
  Efektif Vergi Oranı (ETR) = max(0, Tax / EBT)
─────────────────────────────────
NET KÂR
  Net Kâr Marjı %

Ana Ortaklık Payı (Attributable to Parent)
Kontrol Gücü Olmayan Paylar (Minority Interest)

Pay Sayısı (Diluted Shares Outstanding)
Hisse Başı Kazanç (EPS)
```

### 1B. Bilanço Kalemleri

```
VARLIKLAR (ASSETS)
Dönen Varlıklar (Current Assets):
  Nakit ve Nakit Benzerleri (Cash & Equivalents)
  Finansal Yatırımlar (Short-term Investments)
  Ticari Alacaklar (Trade Receivables)
  Stoklar (Inventories)
  Diğer Dönen Varlıklar (Other Current Assets)
  Toplam Dönen Varlıklar

Duran Varlıklar (Non-Current Assets):
  Maddi Duran Varlıklar (PP&E)
  Kullanım Hakkı Varlıkları (Right-of-Use / IFRS 16)
  Maddi Olmayan Duran Varlıklar (Intangible Assets)
  Şerefiye (Goodwill)
  Yatırım Amaçlı Gayrimenkuller
  Özkaynak Yöntemiyle Değerlenen Yatırımlar
  Diğer Duran Varlıklar
  Toplam Duran Varlıklar

TOPLAM VARLIKLAR

YÜKÜMLÜLÜKLER (LIABILITIES)
Kısa Vadeli Yükümlülükler (Current Liabilities):
  Kısa Vadeli Borçlanmalar (Short-term Debt)
  Uzun Vadeli Borçlanmaların Kısa Vadeli Kısmı (Current Portion of LT Debt)
  Ticari Borçlar (Trade Payables)
  Diğer Kısa Vadeli Yükümlülükler
  Toplam Kısa Vadeli Yükümlülükler

Uzun Vadeli Yükümlülükler (Non-Current Liabilities):
  Uzun Vadeli Borçlanmalar (Long-term Debt)
  Kıdem Tazminatı Karşılığı (Employee Benefits)
  Ertelenmiş Vergi Yükümlülüğü (Deferred Tax)
  Diğer Uzun Vadeli Yükümlülükler
  Toplam Uzun Vadeli Yükümlülükler

TOPLAM YÜKÜMLÜLÜKLER

ÖZKAYNAKLAR (EQUITY)
  Ödenmiş Sermaye (Paid-in Capital)
  Sermaye Düzeltmesi Farkları
  Paylara İlişkin Primler
  Geçmiş Yıllar Kârları
  Net Dönem Kârı
  Diğer Kapsamlı Gelir/Gider Unsurları
Ana Ortaklığa Ait Özkaynaklar
Kontrol Gücü Olmayan Paylar

TOPLAM ÖZKAYNAKLAR
TOPLAM YÜKÜMLÜLÜKLER + ÖZKAYNAKLAR

BALANCE CHECK: Toplam Varlıklar = Toplam Yük. + Özkaynaklar → her dönem kontrol
```

### 1C. Nakit Akış Tablosu Kalemleri

```
İŞLETME FAALİYETLERİ (CFO)
  Vergi Öncesi Kâr
  Düzeltmeler:
    Amortisman & İtfa (D&A)
    Kıdem tazminatı karşılığı
    Faiz gideri (nakit dışı kısım)
    Kur farkı (nakit dışı)
    Parasal Kazanç/Kayıp (IAS 29 — nakit dışı)
  İşletme Sermayesi Değişimleri:
    Ticari Alacaklardaki Değişim
    Stoklardaki Değişim
    Ticari Borçlardaki Değişim
    Diğer
  Ödenen Vergiler
  İşletme Faaliyetlerinden Nakit

YATIRIM FAALİYETLERİ (CFI)
  Maddi Duran Varlık Alımları (CapEx)
  Maddi Duran Varlık Satışları
  Yatırım Alım/Satışları
  İştirak/Bağlı Ortaklık Alım/Satışları
  Yatırım Faaliyetlerinden Nakit

FİNANSMAN FAALİYETLERİ (CFF)
  Borçlanma Gelirleri
  Borç Geri Ödemeleri
  Kira Yükümlülüğü Ödemeleri (IFRS 16)
  Temettü Ödemeleri
  Sermaye Artırımı/Azaltımı
  Finansman Faaliyetlerinden Nakit

NET NAKİT DEĞİŞİMİ
Dönem Başı Nakit
Kur Etkisi
DÖNEM SONU NAKİT (= Bilanço Nakit ile eşleşmeli)
```

---

## Adım 2: Gelir Segmentasyonu (Kritik)

### 2A. Ürün/Hizmet Segmentasyonu

Faaliyet raporundan veya yatırımcı sunumundan gelir kırılımını çıkar:

```
                    FY2022  FY2023  FY2024  TTM
Segment A           XX      XX      XX      XX
  % toplam          X%      X%      X%      X%
  YoY büyüme        X%      X%      X%      X%
Segment B           XX      XX      XX      XX
  % toplam          X%      X%      X%      X%
  YoY büyüme        X%      X%      X%      X%
[...]
TOPLAM HASILAT      XX      XX      XX      XX
```

### 2B. Coğrafi Segmentasyon

```
                    FY2022  FY2023  FY2024  TTM
Türkiye             XX      XX      XX      XX
  % toplam          X%      X%      X%      X%
Avrupa              XX      XX      XX      XX
  % toplam          X%      X%      X%      X%
[Diğer bölgeler]
TOPLAM              XX      XX      XX      XX
```

**Coğrafi kırılım → bbb-dcf'e kritik girdi:** Hasılat-ağırlıklı CRP hesabı için zorunlu.

### 2C. Kaynak Kuralı

| Kaynak | Güvenilirlik | Ne Zaman |
|--------|-------------|----------|
| KAP faaliyet raporu segment dipnotu | ✅ Birincil | Her zaman |
| Şirket IR sunumu | ✅ İkincil | Rapor detaylı değilse |
| KAP özet finansallar (BBB Finans) | ✅ Toplam gelir | Her zaman |
| Web araştırma | ⚠️ Cross-check | Yukarıdakiler yetersizse |

**Segment verisi bulunamazsa:** `[SEGMENT VERİSİ YOK — FAAlİYET RAPORU GEREKLİ]` etiketi ile devam et. Tahmin yapma.

### 2D. Bottom-Up Gelir Modeli (Segment Verisi Mevcutsa ZORUNLU)

> **MS/JPM seviyesi:** Kurumsal araştırmada gelir projeksiyonu top-down CAGR extrapolasyonu ile yapılmaz. Bottom-up bileşenlerden inşa edilir. Top-down sadece cross-check olarak kullanılır.

**Bottom-up modeli kurmak için yeterli veri var mı? Kontrol:**

| Sektör | Gerekli Veri | Tipik Kaynak | Model Yapısı |
|--------|-------------|-------------|-------------|
| **Perakende** | Mağaza sayısı, LFL büyüme, mağaza başı ciro | IR sunumu, faaliyet raporu | Mağaza Sayısı × Mağaza Başı Ciro × (1+LFL) |
| **E-ticaret** | Ziyaretçi, dönüşüm oranı, sepet büyüklüğü | IR sunumu, şirket açıklamaları | Ziyaretçi × Dönüşüm × Sepet |
| **Sanayi/üretim** | Kapasite, doluluk, ASP | Faaliyet raporu | Kapasite × Doluluk × ASP |
| **Abonelik/SaaS** | Abone sayısı, ARPU, churn | IR sunumu | Abone × ARPU × (1-Churn) |
| **Banka** | Kredi hacmi, NIM, fee geliri | BDDK, finansallar | Kredi × NIM + Fee |

**Bottom-Up Gelir Modeli Şablonu (Perakende Örneği):**

```markdown
### Bottom-Up Gelir Modeli — {TICKER}

| Bileşen | FY2024 | FY2025 | FY2026T | FY2027T | Kaynak/Varsayım |
|---------|--------|--------|---------|---------|-----------------|
| Mağaza sayısı (YS) | 270 | 300 | 330 | 358 | Guidance: 330 |
| (+) Net yeni mağaza | 35 | 30 | 30 | 28 | Açılım ivmesi normalize |
| Mağaza başı ciro (M TL) | X | Y | Z | W | LFL + enflasyon |
| (-) Kapanan mağaza etkisi | X | Y | | | |
| = Fiziksel mağaza geliri | X | Y | Z | W | |
| E-ticaret geliri | X | Y | Z | W | %pay trendi |
| Diğer gelir | X | Y | Z | W | |
| = **Toplam Hasılat** | **X** | **Y** | **Z** | **W** | |

Cross-check:
  Top-down CAGR: %X → Bottom-up sonuç: %Y → Fark: [açıkla]
```

**Kurallar:**
- Bottom-up model GelirModeli tab'ında Excel'e girilir (tab 1)
- Toplam satırı GelirTablosu Hasılat'a eşit OLMALI
- Veri yetersizse `[BOTTOM-UP VERİ YETERSİZ — TOP-DOWN KULLANILDI]` etiketi ile gerekçelendir
- T1'deki Makro-Mikro Aktarım Zinciri (§5B) ile tutarlılık kontrol edilir

---

## Adım 3: Temel Hesaplamalar

### 3A. TTM (Son 12 Ay) — bbb-dcf ile aynı formül

```
# Kümülatif raporlama (BIST standart):
TTM = Son Kümülatif Dönem + (Önceki FY − Önceki Yılın Aynı Kümülatif Dönemi)

# Örnek (Q3-2025 mevcut):
TTM Gelir = 9M-2025 + (FY2024 − 9M-2024)
```

Bilanço kalemleri → TTM yapılmaz, son çeyrek sonu değeri kullanılır.

### 3B. Invested Capital (IC)

```
IC = BV_Equity + BV_Debt − Cash
   = Özkaynaklar + Toplam Finansal Borç − Nakit

# R&D varsa ve kapitalleştirilmemişse (bkz bbb-dcf special_cases.md):
IC = BV_Equity + BV_Debt − Cash + R&D_Asset
```

### 3C. Sales/Capital (S/C)

```
S/C = Gelir / IC
```

**S/C tahmin edilmez, hesaplanır.** Trend analizi yapılır: S/C 5Y ortalaması ne? Artıyor mu düşüyor mu? Sektör ortalamasıyla karşılaştır (Damodaran Industry Data).

### 3D. ICR (Interest Coverage Ratio)

```
ICR = EBIT / Faiz Gideri
```

**⚠️ KUR FARKI GİDERİ DAHİL EDİLMEZ.** Sadece gerçek faiz gideri. ICR → Sentetik kredi notu için cross-check olarak kullanılır.

### 3E. ETR (Efektif Vergi Oranı)

```
ETR = max(0, Vergi Gideri / VÖK)
# Negatif VÖK → ETR = 0
```

5Y tarihsel ETR trendi kontrol edilir. Anormal düşük/yüksek yıllar (teşvik, karşılık çözümü) normalleştirilir.

### 3F. Çalışma Sermayesi Metrikleri

```
DSO = (Ticari Alacaklar / Gelir) × 365
DIO = (Stoklar / COGS) × 365
DPO = (Ticari Borçlar / COGS) × 365
CCC = DSO + DIO − DPO  (Nakit Dönüşüm Döngüsü)
```

Sektöre göre benchmark: Perakende DIO yüksek, SaaS düşük. Trend bozulması = red flag.

### 3G. Dipnot Doğrulama (KAP Finansal Tablolar PDF)

İş Yatırım 147 kalemi verir ama NEDEN'i vermez. 4 kritik hesaplama dipnot olmadan güvenilir yapılamaz:

**Zorunlu Kontrol 1: Borçlanma Efektif Faiz Oranları → Kd Girdisi**
```
KAP Dipnot: NOT - Borçlanmalar
Çıkar: Her borç kalemi için efektif faiz oranı (%), vade aralığı, teminat durumu
Not: İş Yatırım sadece borç TUTARINI verir. Faiz oranı bu dipnottan gelir.
Örnek: EBEBK FY2025 → Murabaha efektif %60.34, kiralama %20-66.4
Kural: Kd tahmininde bu efektif oranlar baz alınır. Piyasa faizinden tahmin YAPMA.
```

**Zorunlu Kontrol 2: ETR Normalizasyonu → Vergi Varsayımı**
```
KAP Dipnot: NOT - Vergi Varlık ve Yükümlülükleri
Çıkar: (a) Geçerli KV oranı, (b) halka arz/teşvik indirimi ve süresi,
       (c) ertelenmiş vergi kaynakları (stok, IFRS 16, maddi duran varlık farkı)
Not: Halka arz indirimi geçici (tipik 5 yıl) → terminal ETR'de yasal oran kullan.
Örnek: EBEBK → %25 yasal, halka arz ile %23 efektif, 2028'e kadar geçerli.
```

**Zorunlu Kontrol 3: Tek Seferlik Kalem Ayrıştırma → Net Kar Normalizasyonu**
```
KAP Dipnot: NOT - İşletme Birleşmeleri/Şerefiye + NOT - Yatırım Faaliyetleri Gelir/Gideri
Çıkar: Şerefiye write-down, impairment, koşullu bedel iptali, varlık satışı kazancı
Not: Normalize net kar = Raporlanan net kar - tek seferlik kalemler (vergi sonrası)
Örnek: EBEBK FY2025 → Tuna Çocuk şerefiye 65M TL write-down + ertelenmiş vergi 96M TL
       → Raporlanan -17M TL ama normalize +144M TL
```

**Koşullu Kontrol 4: Döviz Pozisyonu → Kur Riski (yurt dışı geliri >%10 olan şirketler)**
```
KAP Dipnot: NOT - Finansal Araçlar (Kur Riski bölümü)
Çıkar: Net döviz pozisyonu (USD, EUR, GBP ayrı), kur hassasiyet tablosu
Not: Revenue-weighted CRP hesabı için coğrafi kırılım + döviz pozisyon birlikte değerlendirilir.
```

**Dipnot Okuma Yöntemi:**
```bash
# PDF metin çıkarma (pdftotext, hızlı)
pdftotext "research/companies/{TICKER}/{TICKER} {Dönem} Finansal Tablolar.pdf" /tmp/{TICKER}_ft.txt

# Veya PyMuPDF ile belirli sayfaları oku (sayfa numaraları önce haritadan belirle):
python3 -c "
import fitz
doc = fitz.open('research/companies/{TICKER}/{TICKER} {Dönem} Finansal Tablolar.pdf')
for i in range(doc.page_count):
    page = doc[i]
    text = page.get_text().strip()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    header = next((l for l in lines[:5] if len(l) > 5 and 'NOT ' in l.upper()), '')
    if header: print(f'S.{i+1}: {header[:100]}')
"
# Bu harita ile hedef dipnotların sayfalarını bul, sonra o sayfaları oku
```

**Dipnot Doğrulama Tablosu (T2 çıktısına eklenecek):**

| Dipnot | Kontrol Edilen | Bulunan Değer | İş Yatırım Verisi | Fark/Not |
|--------|---------------|---------------|-------------------|----------|
| Borçlanmalar | Efektif faiz (%) | X% | Sadece tutar | Kd girdisi |
| Vergi | ETR + teşvik süresi | %X, YYYY'e kadar | ETR hesaplanabilir | Terminal ETR farkı |
| Giderler | Departman kırılımı | Paz X / GYG Y / Üretim Z | Toplam OpEx | Projeksiyon girdisi |
| Şerefiye/Tek seferlik | Write-down tutarı | X M TL | Net kara dahil | Normalizasyon |
| Döviz | Net YPP kırılımı | USD X / EUR Y | Net YPP toplam | CRP girdisi |

---

## Adım 4: Tarihsel Trend Analizi

Bu bölüm bbb-dcf Faz 1 DATA_PACK'in "tarihsel analiz" kısmını oluşturur.

> **⚠️ Çeyreklik veri varsa (çoğu BIST şirketinde var), Adım 4'ün alt bölümlerinde yıllık trendin yanı sıra çeyreklik trend de analiz edilmelidir — bkz. §4F.**

### 4A. Büyüme Analizi

| Metrik | 5Y CAGR | 3Y CAGR | YoY Son | Trend |
|--------|---------|---------|---------|-------|
| Gelir | %X | %X | %X | ↑/→/↓ |
| EBIT | %X | %X | %X | ↑/→/↓ |
| Net Kâr | %X | %X | %X | ↑/→/↓ |
| FCF | %X | %X | %X | ↑/→/↓ |

### 4B. Kârlılık Trend

| Metrik | 5Y Ort | 5Y Medyan | Min | Max | Son | Trend |
|--------|--------|-----------|-----|-----|-----|-------|
| Brüt Marj | %X | %X | %X | %X | %X | ↑/→/↓ |
| EBIT Marjı | %X | %X | %X | %X | %X | ↑/→/↓ |
| Net Marj | %X | %X | %X | %X | %X | ↑/→/↓ |
| ROIC | %X | %X | %X | %X | %X | ↑/→/↓ |

### 4C. Verimlilik & Yatırım

| Metrik | 5Y Ort | Son | Not |
|--------|--------|-----|-----|
| S/C | Xx | Xx | Sektör ort. ile karşılaştır |
| CapEx/Gelir | %X | %X | Normalizasyon gerekli mi? |
| D&A/Gelir | %X | %X | CapEx vs D&A dengesi |
| CCC (gün) | X | X | Bozulma? İyileşme? |

### 4D. Bilanço Sağlığı

| Metrik | Son | Değerlendirme |
|--------|-----|---------------|
| Net Borç/FAVÖK | Xx | <2x iyi, >4x tehlike |
| Toplam Borç/Özkaynak | Xx | Kaldıraç seviyesi |
| Cari Oran | Xx | >1.5x sağlıklı |
| Nakit Pozisyonu | X mn TL | Net cash mı net debt mı? |
| ICR | Xx | >3x güvenli, <1.5x tehlike |

### 4E. Marj Bridge Analizi (ZORUNLU — MS/JPM Seviyesi)

> **Amaç:** "FAVÖK marjı %11,8'den %12,8'e çıktı" demek yetmez. NEDEN çıktığını bileşenlere ayır. Bu, marj projeksiyonlarının gerekçesini oluşturur.

**Marj Bridge Tablosu (FY(n-1) → FY(n)):**

```markdown
### FAVÖK Marjı Köprüsü: FY2024 → FY2025

| Bileşen | Etki (bp) | Açıklama |
|---------|----------|----------|
| FY2024 FAVÖK Marjı | %11,8 | Başlangıç |
| (+) Brüt marj iyileşmesi | +X bp | Özel marka payı artışı, fiyatlama gücü |
| (+) Ölçek kaldıracı (SGA) | +X bp | Mağaza başı sabit gider dağılımı |
| (+) Personel verimliliği | +X bp | Çalışan başı ciro artışı |
| (-) Yeni pazar dilüsyonu | -X bp | UK startup maliyetleri |
| (-) Enflasyon baskısı | -X bp | Enerji, nakliye, kira artışları |
| (+/-) Ürün karması (mix) | ±X bp | Yüksek marjlı segment payı değişimi |
| = **FY2025 FAVÖK Marjı** | **%12,8** | **+100bp** |
```

**Veri Kaynakları:**
- NOT 20 (Niteliklerine Göre Giderler): Departman bazlı gider kırılımı
- Gelir segmentasyonu: Segment marj farkları
- Faaliyet raporu: Personel sayısı, mağaza sayısı, kapasite
- IR sunumu: Operasyonel KPI'lar

**Kurallar:**
- Bridge toplam farkı = gerçek marj değişimi (bp olarak eşleşmeli)
- Her bileşen ±5bp'den küçükse "diğer" kategorisine atılabilir
- **T3'e girdi:** Terminal marj varsayımı bu bridge'e dayanmalı. "Terminal FAVÖK %15 çünkü bridge'deki X ve Y bileşenleri devam edecek."

### 4F. Çeyreklik Trend Analizi (Çeyreklik Veri Mevcutsa ZORUNLU)

> **Amaç:** Yıllık ortalamalar mevsimselliği ve trend kırılmalarını gizler. 8-12 çeyrek görünümü yapısal trend vs geçici sapma ayrımını sağlar.

```markdown
### Çeyreklik Trend — {TICKER} (Son 8-12 Çeyrek)

| Çeyrek | Hasılat | QoQ | YoY | Brüt Marj | FAVÖK Marjı | Not |
|--------|---------|-----|-----|-----------|-------------|-----|
| 1Ç2023 | X | | | %X | %X | |
| 2Ç2023 | X | %X | | %X | %X | |
| ... | | | | | | |
| 4Ç2025 | X | %X | %X | %X | %X | Son |
```

**Mevsimsellik tespiti:**
- En güçlü çeyrek hangisi? (perakende: 4Ç, turizm: 2-3Ç, inşaat: 2-3Ç)
- QoQ dalgalanma genliği ne kadar? >%20 QoQ dalgalanma = güçlü mevsimsellik
- Mevsimsellik son 3 yılda tutarlı mı yoksa değişiyor mu?

**Trend kırılması tespiti:**
- Son 2-3 çeyrekta marj trendi yıllık trendden sapıyor mu?
- Son çeyrekteki sapma "noise" mı yoksa "signal" mı? (bkz. Adım 6C)

**Araç:** `bbb_financials.py {TICKER} --dcf --json` çeyreklik veri içerir. Yoksa KAP PDF'lerden çeyreklik gelir tablosu çıkar.

### 4G. Birim Ekonomi Analizi (Sektör Uygunsa ZORUNLU)

> **Amaç:** Şirketin büyüme stratejisinin ekonomik olarak sürdürülebilir olup olmadığını test et. Her yeni mağaza/fabrika/müşteri ne kadar getiri sağlıyor?

**Perakende Birim Ekonomi Şablonu:**

```markdown
### Birim Ekonomi — {TICKER} (Mağaza Bazlı)

| Metrik | Değer | Kaynak | Not |
|--------|-------|--------|-----|
| Yeni mağaza yatırımı | ~X M TL | CapEx / net yeni mağaza | Yaklaşık |
| İlk yıl ciro (yeni mağaza) | ~X M TL | Toplam ciro / mağaza (proxy) | Olgun mağazadan düşük |
| Olgunlaşma süresi | ~X yıl | LFL veri + sektör deneyimi | |
| Olgun mağaza cirosu | ~X M TL | IR sunumu veya hesaplama | |
| Olgun mağaza FAVÖK marjı | ~%X | Konsolide marj + yeni mağaza etkisi çıkarılarak | |
| Mağaza bazlı FAVÖK | ~X M TL | Ciro × FAVÖK marjı | |
| **Payback süresi** | **~X yıl** | Yatırım / yıllık FAVÖK | <3Y ideal, >5Y dikkat |
| **Mağaza ROIC** | **~%X** | Yıllık FAVÖK / yatırım | WACC üzeri mi? |
```

**Sanayi/Üretim Birim Ekonomi Şablonu:**

```markdown
| Metrik | Değer | Not |
|--------|-------|-----|
| Yeni kapasite yatırımı | X M TL / birim kapasite | |
| Kapasite kullanım oranı (mevcut) | %X | |
| Break-even doluluk | %X | |
| Birim üretim maliyeti | X TL/adet | |
| Birim satış fiyatı | X TL/adet | |
| **Birim katkı marjı** | **%X** | |
```

**Veri yeterliliği notu:** Birim ekonomi verisi genellikle doğrudan raporlanmaz. Proxy hesaplama yapılır:
- Mağaza yatırımı ≈ Son yıl CapEx / net yeni mağaza sayısı
- Mağaza başı ciro ≈ Toplam ciro / ortalama mağaza sayısı
- Proxy olduğunu her zaman belirt, hassasiyet düşük

---

## Adım 5: Peer Karşılaştırma Girdileri

T2 comps tablosunun ham verisini toplar. Detaylı comps analizi → `karsilastirmali-degerleme.md`.

### Peer Listesi Oluşturma

| Kaynak | Amaç |
|--------|------|
| BIST sektör listesi | Yerli peer'lar (min 3-5) |
| KAP faaliyet raporu "Rakipler" | Şirketin kendi tanımı |
| Damodaran Industry Data | Global sektör ortalamaları |
| Yahoo Finance Similar Companies | Yurt dışı peer önerileri (min 2-4) |

### Peer Metrik Tablosu (Ham Veri)

Her peer için en az:
- Gelir, gelir büyümesi %, brüt marj, EBIT marjı, ROIC
- EV/FAVÖK, F/K, P/FCF, EV/Gelir
- Net Borç/FAVÖK

**Araçlar:**
```bash
# BIST peer'lar
python3 bbb_financials.py {PEER_TICKER} --start-year 2023 --end-year 2025 --section all --full

# Yurt dışı peer'lar
python3 ~/.openclaw/workspace/skills/bbb-finans/scripts/bbb_yfinance.py fundamentals {TICKER}
```

---

## Adım 6: Senaryo Varsayımları (Bull/Base/Bear)

T2'nin son adımı: bbb-dcf Faz 1.5'te onaylanacak varsayım setini hazırla.

### 6A. Guidance ve Yönetim Beklentileri — Varsayım Girdisi

Senaryo varsayımları sıfırdan türetilmez. T1'de toplanan yönetim kaynakları burada girdi olarak kullanılır:

**Zorunlu girdi kaynakları (T1'den devir):**
| Kaynak | Varsayıma Etkisi | Dikkat |
|--------|-----------------|--------|
| **Yatırımcı sunumu — guidance** | Gelir CAGR, EBIT marjı, CapEx planı → Base senaryo çerçevesi | Guidance genellikle iyimser — Bear senaryoda guidance'ı -%10-20 düşür |
| **Konferans çağrısı — sözel ipuçları** | Senaryo ağırlıklandırma | "Agresif yatırım dönemine giriyoruz" → CapEx/Gelir yukarı, kısa vadede FCF baskısı |
| **CEO/CFO röportajları — strateji** | Terminal büyüme ve moat varsayımı | Vizyon beyanları kantitatif varsayıma doğrudan dönüşmez — somut yatırım planıyla cross-check et |
| **Kurum raporları — konsensüs beklenti** | Base senaryo kalibrasyonu | 3+ kurum ortalaması → consensus. BBB tahmini consensus'tan sapıyorsa → sebebi açıkla |

**Guidance → Varsayım Dönüşüm Tablosu (zorunlu):**

```markdown
### Guidance vs Varsayım Karşılaştırması — {TICKER}

> **Birim:** Yönetim guidance genellikle NOMİNAL (IAS 29 Dec {YYYY} bazı veya düzeltmesiz).
> BBB senaryo rakamları DCF yaklaşımına göre [REEL Dec {BAZ_YIL} bazı / NOMİNAL] cinsindedir.
> Karşılaştırma öncesi tüm rakamlar AYNI BİRİME çevrilmelidir.

| Metrik | Yönetim Guidance | Birim | Kurum Konsensüs | BBB Bear | BBB Base | BBB Bull | Sapma Notu |
|--------|-----------------|-------|-----------------|----------|----------|----------|------------|
| Gelir (YYYY) | X B TL | [Nom/Reel] | Y B TL | Z B TL | W B TL | V B TL | [Neden farklıyız?] |
| FAVÖK Marjı | %X | — | %Y | %Z | %W | %V | |
| CapEx | X M TL | [Nom/Reel] | — | Y M TL | W M TL | V M TL | |
| Mağaza/Kapasite | X adet | — | — | Y | W | V | |
```

**🔴 Reel ↔ Nominal Rekonsilasyon (IAS 29 şirketlerinde ZORUNLU):**

Guidance nominal, DCF reel (veya tersi) ise, aşağıdaki çevirisi YAPILMADAN karşılaştırma geçersizdir:

```markdown
### Guidance Rekonsilasyonu — {TICKER} (YYYY)

| Kaynak | Hasılat | Birim | Reel Eşdeğer (Dec {BAZ_YIL}) | İma Edilen Reel Büyüme |
|--------|---------|-------|------------------------------|----------------------|
| Yönetim Guidance | X B TL | Nominal | X / (1 + π) = Y B TL | (Y / Baz - 1) = %Z |
| BBB Base (DCF Y1) | W B TL | Reel Dec {BAZ_YIL} | W B TL | %V |
| Fark | | | | +/- %N puan |

π = Beklenen yıl sonu enflasyon (şirketin kendi varsayımı veya TCMB beklenti anketi)
Baz = FY{BAZ_YIL} hasılat (IAS 29 Dec {BAZ_YIL} bazı)

USD DCF + TL Guidance durumunda:
| Yönetim Guidance | X B TL | Nominal TL | X / Ort_Kur_YYYY = Z B USD | (Z / Baz_USD - 1) = %W |
| BBB Base (DCF Y1) | V B USD | USD | V B USD | %U |
Ort_Kur_YYYY = Beklenen yıllık ortalama USD/TL kuru (spot kur DEĞİL, yıl ortalaması)
```

**⚠️ Sapma yönü notu:** DCF guidance'ın üstünde veya altındaysa, bunun BİLİNÇLİ bir tercih olduğunu ve sebebini 1-2 cümleyle açıkla. "Biz guidance'dan agresifiz çünkü..." veya "Biz muhafazakarız çünkü..." — EBEBK'te bu yapılmadı, DCF %15 reel iken guidance %7 reel ima ediyordu, fark açıklanmadı.

**⚠️ Sapma Notu zorunlu:** BBB varsayımı yönetim guidance'ından veya konsensüsten %10+ sapıyorsa (AYNI BİRİMDE karşılaştırıldığında), sebebi 1-2 cümle ile açıklanmalıdır. "Yönetim iyimser" yetmez — *neden* iyimser olduğunu düşündüğün veriyle destekle.

**Guidance Doğruluk Geçmişi (T1'den):** Management Quality Scorecard Kriter 2 (Guidance Doğruluğu) burada referans alınır. Yönetim geçmişte guidance'ı tutturamıyorsa → Bull senaryoda bile guidance'ın altında kal.

### 6B. Varsayım Tablosu

```
| Varsayım | Bear | Base | Bull | Kaynak/Gerekçe |
|----------|------|------|------|----------------|
| Gelir CAGR (5Y) | %X | %X | %X | [Tarihsel trend + sektör büyüme + guidance] |
| Terminal Gelir Büyüme | %X | %X | %X | [Nominal GDP + sektör] |

> **UYARI**: FM terminal buyume MUTLAKA reel GDP + sektor primi (~%3-5) ile sinirli olmalidir. %8+ terminal buyume makroekonomik olarak surdurulebilir degildir. Bkz. senaryo-metodoloji.md Bolum 2.2.
| EBIT Marjı (Terminal) | %X | %X | %X | [Tarihsel trend + peer ortalaması + guidance] |
| CapEx/Gelir | %X | %X | %X | [Tarihsel ort. vs yönetim planı vs normalizasyon] |
| ETR | %X | %X | %X | [Yasal oran + teşvikler] |
| S/C | Xx | Xx | Xx | [Tarihsel ort. + sektör] |
| Net Borç/FAVÖK (Terminal) | Xx | Xx | Xx | [Yönetim hedefi vs trend] |
```

**Her varsayımın yanında kaynak/gerekçe ZORUNLU.**

### 6C. Kaynak Güncelliği Kontrolü

Varsayım tablosu tamamlandıktan sonra her kaynağın güncelliğini doğrula:
- 🟢 ≤6 ay → doğrudan kullan
- 🟡 6-12 ay → `[Kaynak: YYYY-MM — X ay öncesi]` etiketi
- 🔴 >12 ay → birincil varsayım kaynağı olarak KULLANILAMAZ

Detaylı protokol → `task1-arastirma.md §Kaynak Güncelliği Protokolü`

**Signal vs Noise ayrımı:** Son çeyrekteki kısa vadeli sapma (noise) mı, yapısal trend değişimi (signal) mi? Signal → varsayımı güncelle. Noise → normalizasyon.

### 6B: Kantitatif Senaryo Turetim Kurallari (ZORUNLU)

> **Referans**: Detayli turetim formulleri icin bkz. `senaryo-metodoloji.md`

#### Turetim Sirasi

1. **Makro kisitlari belirle**: Terminal buyume tavani = Reel GDP + sektor primi (maks +2pp). Turkiye reel GDP ~%3-4 → terminal g = %2.5-%4.5 MUTLAK ARALIK.
2. **Sirkete ozgu girdileri al** (T1'den): ⭐ [v2.0 — KRİTİK]
   - Yonetim rehberligi → guvenilirlik skoru (G) ile agirliklandi (bkz. senaryo-metodoloji.md 2A.1)
   - Yatirim dongusu tespiti → CapEx ve buyume profili ayarla (bkz. 2A.2)
   - Katalist takvimi → her senaryonun tetikleyici olaylarini belirle (bkz. 2A.3)
   - Sirket rejimi (buyume/olgun/toparlanma) → parametre aralik genisligini ayarla (bkz. 2B)
3. **Tarihsel normalize et**: Son 5Y CAGR'yi hesapla (IAS 29 duzeltmeli, one-off haric)
4. **Peer benchmark olustur**: Comps tablosundan buyume, marj, CapEx/Hasilat Q25/medyan/Q75
5. **Formul uygula + sirkete ozgu harmanlama**:
   - Bear buyume = MIN(Tarihsel - 2pp, Peer Q25, Makro - 1pp) → rehberlik G ile harmanlandi
   - Base buyume = G × Rehberlik + (1-G) × [(Tarihsel + Peer + Makro) / 3]
   - Bull buyume = MAX(Tarihsel + 2pp, Peer Q75, Makro + 2pp) → katalist etkisi ekle
6. **Bottom-up dogrulama**: Segment bazli buyume × segment payi = toplam → formul sonucuyla ±2pp mi? (bkz. 2A.4)
7. **Terminal marj**: Peer medyan ±2pp, tarihsel peak ile kisitli
8. **Ic tutarlilik kontrolu**: Her senaryo icinde buyume↔marj↔CapEx tutarli mi? (bkz. 2C)
9. **FM-DCF tutarlilik kontrolu**: Bolum 4 (senaryo-metodoloji.md) kontrol listesiyle dogrulanir

#### FM-DCF Tutarlilik Zorunlulugu

FM ve DCF senaryolari su parametrelerde BIREBIR esit olmali:
- Terminal buyume (g)
- Vergi orani (ETR)
- Senaryo agirliklari (Bear/Base/Bull olasiliklari)

Sapma durumunda DCF **master** kabul edilir, FM uyumlu hale getirilir.

#### Senaryo Agirliklari — Adaptif Model

Standart: Bear %25 / Base %50 / Bull %25

Duzeltmeler (bkz. senaryo-metodoloji.md Bolum 3):
- MQS 24-30 → Bear -5pp, Bull +5pp
- MQS 12-17 → Bear +5pp, Bull -5pp
- MQS < 12 → Bear +10pp, Bull -10pp
- Risk Matrisi en yuksek risk >= %40 → Bear +5pp, Bull -5pp

---

## Adım 7: Muhasebe Standardı & Para Birimi Kontrolü

Şirket türüne göre aşağıdaki 3 tablodan BİRİNİ uygula:

### 7A. BIST + IAS 29 (Türk şirketlerinin çoğunluğu)

| Kontrol | Durum | Not |
|---------|-------|-----|
| IAS 29 düzeltmeli veri seti mi? | ☐ | KAP Özet = IAS 29. BBB Finans Detaylı = Nominal |
| Parasal Kazanç/Kayıp ayrıştırıldı mı? | ☐ | EBIT'ten çıkarılmalı |
| USD raporlama var mı? | ☐ | Varsa: USD bazlı analiz birincil |
| IAS 29 TL'yi spot kurla USD'ye çevirme | ☐ YASAK | Yıllık ort. kur (gelir) / dönem sonu (bilanço) |
| Nominal vs düzeltmeli karşılaştırma | ☐ | Her ikisi de raporlanır, tek set seçilir |

### 7B. BIST + IAS 29 uygulamayan (nadir ama mümkün)

| Kontrol | Durum | Not |
|---------|-------|-----|
| Nominal TL verisi doğrulandı mı? | ☐ | BBB Finans Detaylı birincil kaynak |
| CFO formülünde Parasal K/K satırı YOK | ☐ | 4 bileşen: FAVÖK + Vergi + Faiz + İS Değişimi |
| FX risk: Döviz pozisyon tablosu okundu mu? | ☐ | KAP dipnot "Finansal Risk" bölümü |
| Gelirin döviz kırılımı mevcut mu? | ☐ | CRP hesabı ve kur duyarlılığı için gerekli |

### 7C. Yurt Dışı Şirket (BIST dışı)

| Kontrol | Durum | Not |
|---------|-------|-----|
| Birincil veri kaynağı: yfinance | ☐ | `bbb_yfinance.py fundamentals {TICKER}` — BBB Finans BIST-only |
| Raporlama para birimi tespit edildi mi? | ☐ | Subtitle'a yaz: "Para birimi: M {CCY}" |
| USD dönüşüm satırı gerekli mi? | ☐ | Raporlama ≠ USD ise GelirModeli'ne 3 satır: Hasılat × Kur = USD |
| Muhasebe standardı: US GAAP / IFRS | ☐ | P&L satır sırası farklı olabilir (R&D ayrı satır, SGA vb.) |
| CFO formülünde Parasal K/K satırı YOK | ☐ | 4 bileşen: FAVÖK + Vergi + Faiz + İS Değişimi |
| FX translation riski var mı? | ☐ | Çok para birimli gelir → hangi kur varsayımı? |
| CRP hesabı: revenue-weighted coğrafya | ☐ | Her coğrafyanın gelir payı + ülke CRP'si |

> **NVO dersi:** DKK raporlayan şirkette GelirModeli'ne "Ortalama USD/DKK", "Hasılat (M USD)" satırları eklendi. Tüm diğer tablar DKK'da kaldı. DCF para birimi kararı Faz 0'da verilir.

---

## T2 Çıktı Formatı

> **🔴 T2'NİN NİHAİ ÇIKTISI EXCEL MODELİDİR, MARKDOWN DEĞİL.**
> Markdown analiz dosyası (`_financial_analysis.md`) ara üründür — agent'ın düşünce sürecini belgeler.
> Excel modeli (`{TICKER}_Finansal_Model_{YYYY-MM-DD}.xlsx`) T3'e handoff edilen nihai deliverable'dır.
> **Excel üretilmeden T2 TAMAMLANMIŞ SAYILMAZ.** Bkz. Adım 8 (Excel Model Üretimi).

T2 tamamlandığında üretilen dosyalar:

**1. Excel Modeli (NİHAİ):** `research/companies/{TICKER}/{TICKER}_Finansal_Model_{YYYY-MM-DD}.xlsx`
**2. Markdown Analiz (ARA):** `research/companies/{TICKER}/{TICKER}_financial_analysis.md`

**Markdown İçerik (minimum):**
1. ✅ Tarihsel finansal tablolar (3-5Y) — Gelir Tablosu, Bilanço, Nakit Akış
2. ✅ Gelir segmentasyonu (ürün + coğrafya)
3. ✅ Bottom-up gelir modeli (segment verisi mevcutsa — §2D)
4. ✅ Temel hesaplamalar (TTM, IC, S/C, ICR, ETR, CCC)
5. ✅ Tarihsel trend analizi (büyüme, kârlılık, verimlilik, bilanço)
6. ✅ Marj bridge (FY(n-1)→FY(n) FAVÖK köprüsü — §4E)
7. ✅ Çeyreklik trend (8-12 çeyrek, mevsimsellik — §4F)
8. ✅ Birim ekonomi (sektör uygunsa — §4G)
9. ✅ Peer karşılaştırma ham verileri
10. ✅ Senaryo varsayımları (Bull/Base/Bear) + gerekçeler
11. ✅ IAS 29 kontrol tablosu (Türk şirketleri)
12. ✅ T2→T3 EBIT Köprüsü (IAS 29 şirketleri — aşağıda)

**T2→T3 EBIT Köprüsü (IAS 29 Şirketleri İçin ZORUNLU)**

> **Kök Sorun:** IAS 29 uygulayan şirketlerde GAAP EBIT parasal kazanç/kayıp dahil eder. Reel DCF'te bu kalem hariç tutulmalıdır. Ama bu karar T2 çıktısında açıkça belgelenmezse, T3'te "hangi EBIT?" sorusu cevapsız kalır.

```markdown
### T2→T3 EBIT Köprüsü — {TICKER}

| Kalem | FY Değer | Not |
|-------|---------|-----|
| GAAP Esas Faaliyet Kârı (EBIT) | X M TL | KAP/İş Yatırım |
| (+) Parasal Pozisyon Kaybı (net) | X M TL | IAS 29 artifact — nakit dışı |
| (+) Tek seferlik kalemler (hariç) | X M TL | Şerefiye write-down, dava karşılığı vb. |
| (-) Tek seferlik gelirler (hariç) | (X) M TL | Koşullu bedel iptali, varlık satışı vb. |
| = **Operasyonel EBIT (DCF girdisi)** | **X M TL** | **Op. EBIT Marjı: %X** |
| Cross-check: FAVÖK - D&A | X M TL | Uyumlu mu? |

**Gerekçe:** Reel TL (USD-eşdeğer) DCF'te parasal K/K hariç tutulur çünkü:
(a) Nakit dışı, yalnızca enflasyon muhasebesi kalemi
(b) DCF zaten reel bazda, çifte sayım olur
(c) Şirketin operasyonel performansını yansıtmaz
```

**Kural:** Bu köprü olmadan T3'e geçilmez. T3'ün DCFProjeksiyon baz yılı bu tablodaki "Operasyonel EBIT" değerini kullanır.

**İlker'in 6 Metriği (ZORUNLU):**

| Metrik | Değer | Değerlendirme |
|--------|-------|---------------|
| ROIC | %X | İyi / Kötü / Mükemmel / 🔴 RED FLAG |
| FCF Marjı | %X | İyi / Kötü / Mükemmel / 🔴 RED FLAG |
| Brüt Kâr Marjı | %X | |
| Net Borç/FAVÖK | Xx | |
| Ciro Büyümesi (Reel) | %X | |
| ROE | %X | |

**Veto Kontrolü:**
- ROIC < %10 → 🔴 RED FLAG (Veto)
- FCF Marjı negatif → 🔴 RED FLAG (Veto)

---

## T2 Doğrulama Checklist

Deliverable teslim öncesi:

- [ ] **🔴 Excel modeli üretildi** (`{TICKER}_Finansal_Model_{YYYY-MM-DD}.xlsx` — 6 tab, formül bazlı, senaryo seçicili). Excel OLMADAN T2 tamamlanmış SAYILMAZ. [v2.0]
- [ ] **🔴 Tab arası formül referansları çalışıyor** (GelirModeli→GelirTablosu hasılat, Senaryolar→tüm projeksiyon girdileri, GelirTablosu→NakitAkış CFO bileşenleri, Bilanço Nakit=PLUG) [v2.0]
- [ ] Tüm rakamlar KAP/BBB Finans'tan — `[DOĞRULANMADI]` etiketi yok
- [ ] TTM doğru hesaplandı (kümülatif formül)
- [ ] Bilanço dengelendi: Varlıklar = Yükümlülükler + Özkaynaklar (her dönem) + conditional formatting aktif [v1.7]
- [ ] Bilanço 3-tablo entegrasyonu: Özkaynaklar = Prior + Net Kâr formülü, Nakit = plug [v1.7]
- [ ] CFO formülü 5 bileşenli: FAVÖK + Vergi + Faiz + Parasal + İS Değişimi [v1.7]
- [ ] Yıl bazlı marj ayrımı: FY26 ve FY27 marjları farklı Senaryolar satırlarından besleniyor [v1.7]
- [ ] S/C, ICR, ETR hesaplandı (tahmin değil)
- [ ] Gelir segmentasyonu kaynak etiketli
- [ ] Peer'lar listelenmiş (min 4-5)
- [ ] Senaryo varsayımları gerekçeli
- [ ] Adım 7 kontrol tablosu doldurulmuş (7A: BIST+IAS29 / 7B: BIST+nominal / 7C: yurt dışı)
- [ ] İlker'in 6 metriği tablosu mevcut + veto kontrolü yapılmış
- [ ] **Dipnot Doğrulama Tablosu doldurulmuş** (Adım 3G: efektif faiz, ETR teşvik, tek seferlik, döviz)
- [ ] **Bottom-up gelir modeli** yapılmış veya `[BOTTOM-UP VERİ YETERSİZ]` notu konmuş (§2D)
- [ ] **Marj bridge** (FAVÖK köprüsü FY(n-1)→FY(n)) doldurulmuş (§4E)
- [ ] **Çeyreklik trend** tablosu (8-12Q) hazırlanmış, mevsimsellik tespit edilmiş (§4F)
- [ ] **Birim ekonomi** analizi yapılmış veya "sektör uygun değil" notu konmuş (§4G)
- [ ] **T2→T3 EBIT Köprüsü** doldurulmuş (IAS 29 şirketleri) — Op. EBIT tanımı açık
- [ ] Excel audit geçti: `python3 dcf-dogrulama.py {TICKER}_Financial_Model.xlsx --audit` → çıktı TEMİZ
- [ ] **🔴 xlsx skill yapısal doğrulama geçti** [v2.1]:
  ```bash
  python3 ~/.openclaw/workspace/skills/xlsx/scripts/validate_model.py \
    {TICKER}_Finansal_Model_{YYYY-MM-DD}.xlsx \
    --sheets GelirModeli,GelirTablosu,NakitAkis,Bilanco,Senaryolar,INAGirdileri \
    --min-formulas 180 \
    --balance-check "Bilanco:TV - TK"
  ```
  → Çıktı: 0 KRİTİK sorun olmalı. Uyarılar kabul edilebilir ama değerlendirilmeli.
- [ ] **🔴 xlsx skill formül recalc geçti** [v2.1]:
  ```bash
  python3 ~/.openclaw/workspace/skills/xlsx/scripts/recalc.py {TICKER}_Finansal_Model_{YYYY-MM-DD}.xlsx
  ```
  → Çıktı: `"status": "success"`. `errors_found` → düzelt ve yeniden çalıştır.
- [ ] **openpyxl tuzakları kontrol edildi** [v2.1]: xlsx SKILL.md "openpyxl Teknik Tuzaklar" bölümü okundu ve 8 tuzak kontrol edildi (iç içe formül, negatif oran, formül değerlendirmesi, DataValidation, conditional formatting, merge_cells, number_format, PLUG döngüsü)

---

## Sık Yapılan Hatalar

| Hata | Sonuç | Çözüm |
|------|-------|-------|
| IAS 29 düzeltmeli TL'yi spot kurla USD'ye çevirme | Şişirilmiş gelir/EBIT | Yıllık ort. kur veya şirketin kendi USD raporlaması |
| ICR'da kur farkı gideri dahil etme | ICR çöker → Kd şişer | Sadece gerçek faiz gideri |
| TTM'yi çeyreklik × 4 ile hesaplama | Mevsimsellik kaçırılır | Kümülatif formül kullan |
| CapEx/Gelir'i tarihsel ortalamadan farklı alma | FCFF şişer/söner | Tarihsel trendi kontrol et |
| Segment verisi olmadan devam etme | Büyüme varsayımı havada | Faaliyet raporu iste veya [SEGMENT VERİSİ YOK] etiketi |
| Nominal ve IAS 29 karıştırma | Tüm oranlar yanlış | Tek set seç, diğerini cross-check |

---

---

## Adım 8: Excel Model Üretimi (openpyxl)

> **🔴🔴🔴 REFERANS MODEL KULLAN — SIFIRDAN YAPMA 🔴🔴🔴**
> 
> **Pattern (6 tekrar):** NTHOL→EBEBK T3→NVO T2→TCELL T2 v1/v2/v3/v4'te her seferinde sıfırdan Excel yazıldı → formül hataları (#AD?), eksik satırlar, yanlış referanslar, eksik sayfalar.
> 
> **ÇÖZÜM — REFERANS MODELLERİ KOPYALA VE ADAPTE ET:**
> 
> **Referans Modeller (BBB standardı, doğrulanmış):**
> ```
> BIST şirketleri için:
>   research/companies/EBEBK/EBEBK_Finansal_Model_v2_2026-03-22.xlsx
>   → 6 sayfa, 183 formül, IAS 29 uyumlu, TL bazlı
> 
> Yurt dışı şirketler için:
>   research/companies/NVO/NVO_Finansal_Model_2026-03-25.xlsx
>   → 6 sayfa, DKK bazlı, yfinance uyumlu, coğrafi kırılım detaylı
> ```
> 
> **Workflow:**
> 1. Uygun referans modeli AÇ ve İNCELE (satır satır, sayfa sayfa)
> 2. Yeni dosya oluştur, referansın YAPISINI birebir kopyala
> 3. Şirkete özel verileri doldur (segment isimleri, tarihsel veriler, coğrafi kırılım)
> 4. Formülleri referanstan kopyala, sadece satır numaralarını güncelle
> 5. Senaryo parametrelerini T1'den al
> 
> **Referans modelde kontrol edilecekler:**
> - GelirModeli: Segment isimleri şirkete özel mi? (Segment 1/2/3 OLMAZ)
> - GelirModeli: Coğrafi kırılım var mı? (Türkiye + yurt dışı)
> - GelirTablosu: SMM/Hasılat, PAZ/Hasılat input satırları var mı?
> - Senaryolar: 30+ parametre var mı? (sadece 10 değil)
> - Bilanco: TFRS 16, Şerefiye, detaylı kırılım var mı?
> 
> **SIFIRDAN EXCEL YAZMAK YASAK. Referans modeli aç, incele, kopyala, adapte et.**

T2'nin nihai çıktısı markdown DEĞİL, **Excel dosyasıdır.** Agent `openpyxl` ile 6 sayfalı Excel modeli üretir.

### Dosya Adlandırma
```
{TICKER}_Finansal_Model_{YYYY-MM-DD}.xlsx
```

### Renk Kodlama Standardı (Her Hücrede)

| Renk | Anlam | Örnek |
|------|-------|-------|
| 🔵 Mavi font | Kullanıcı girdisi / varsayım | Büyüme oranı, marj tahmini |
| ⬛ Siyah font | Formül (hesaplanan) | Toplam gelir, FAVÖK |
| 🟢 Yeşil font | Başka sayfaya referans (link) | =GelirModeli!B5 |
| 🔴 Kırmızı font | Hata / doğrulama ihlali | Bilanço dengelenmedi |
| Gri arka plan | Tarihsel veri (gerçekleşme) | FY2020-FY2024 |
| Beyaz arka plan | Projeksiyon (tahmin) | FY2025T-FY2029T |

### Sayfa 1: Gelir Modeli (GelirModeli)

En kritik sayfa — değerlemenin temeli.

**Yapı:**
```
Satır 1-3: Başlık, şirket adı, para birimi, kaynak
Satır 5: Yıl başlıkları (FY2020-FY2024 gri | FY2025T-FY2029T beyaz)

BÖLÜM A: ÜRÜN/HİZMET SEGMENTLERİ (Satır 7-35)
  Segment A Hacmi (adet/ton/abonelik)    → 🔵 girdi
  Segment A Birim Fiyat                  → 🔵 girdi
  Segment A Gelir = Hacim × Fiyat        → ⬛ formül
  Segment A Büyüme (YoY %)              → ⬛ formül
  [20-30 satır — her ana ürün/hizmet]

BÖLÜM B: COĞRAFİ KIRILIM (Satır 37-55)
  Türkiye Geliri                         → 🟢 link (A bölümünden)
  Türkiye Payı %                         → ⬛ formül
  Avrupa Geliri                          → 🟢 link
  [15-20 satır — her bölge]
  CRP Ağırlıkları (bbb-dcf girdisi)     → ⬛ formül

BÖLÜM C: TOPLAM (Satır 57-62)
  TOPLAM HASILAT                         → ⬛ SUM formülü
  YoY Büyüme %                          → ⬛ formül
  3Y CAGR                               → ⬛ formül
```

**Doğrulama:** A bölümü toplamı = C bölümü toplamı = B bölümü toplamı. Üçü eşleşmiyorsa → 🔴.

### Sayfa 2: Gelir Tablosu (GelirTablosu)

**40-50 satır kalemi.** Adım 1A'daki KAP sıralamasını birebir takip eder.

```
Satır 1-3: Başlık
Satır 5: Yıl başlıkları

Hasılat                                  → 🟢 =GelirModeli!C57
Satışların Maliyeti                      → 🔵 girdi (marj varsayımı üzerinden)
  SMM/Hasılat %                          → 🔵 girdi
BRÜT KÂR                                → ⬛ formül
  Brüt Kâr Marjı %                      → ⬛ formül

GYG                                      → 🔵 girdi (hasılat %'si)
Pazarlama Giderleri                      → 🔵 girdi
ArGe Giderleri                           → 🔵 girdi
Esas Faaliyetlerden Diğer Gelir/Gider   → 🔵 girdi
FAALİYET KÂRI (EBIT)                    → ⬛ formül
  EBIT Marjı %                           → ⬛ formül

Amortisman & İtfa                        → 🟢 =NakitAkis!D_A satırı
FAVÖK                                    → ⬛ = EBIT + D&A
  FAVÖK Marjı %                          → ⬛ formül

Finansman Gelirleri                      → 🔵 girdi
Finansman Giderleri                      → 🔵 girdi
  Faiz Gideri (ayrı satır — ICR için)   → 🔵 girdi
Parasal Kazanç/Kayıp (IAS 29)           → 🔵 girdi
VERGİ ÖNCESİ KÂR                        → ⬛ formül
Vergi Gideri                             → ⬛ = VÖK × ETR
  ETR %                                  → 🔵 girdi
NET KÂR                                 → ⬛ formül
  Net Kâr Marjı %                        → ⬛ formül

Ana Ortaklık Payı                        → 🔵 girdi (minority split)
HBK (EPS)                               → ⬛ = Net Kâr / Pay Sayısı

HESAPLANAN METRİKLER:
ICR = EBIT / Faiz Gideri                → ⬛ formül
ROIC = NOPAT / IC                       → 🟢 = Bilanço link
S/C = Hasılat / IC                      → 🟢 = Bilanço link
```

### Sayfa 3: Nakit Akış Tablosu (NakitAkis)

Adım 1C yapısını takip eder. CapEx satırı özellikle önemli — FCFF hesabının girdisi.

**CFO formülü (5 bileşen):** [v1.7]
```
CFO = FAVÖK + Vergi + Faiz + Parasal K/K + İşletme Sermayesi Değişimi
```
> **NOT:** Eski `CFO = FAVÖK + İS Değişimi` formülü **hatalıdır** — vergi, faiz ve IAS 29 parasal kalemlerini atlıyordu. Her 5 bileşen GelirTablosu'ndan formül referansıyla alınmalıdır (tarihsel hariç).

```
FAVÖK                                    → 🟢 = GelirTablosu FAVÖK satırı
(-) Vergi Ödemesi                        → 🟢 = GelirTablosu Vergi satırı
(-) Net Faiz Ödemesi                     → 🟢 = GelirTablosu Finansman Gid. satırı
(+) Parasal K/K (IAS 29, non-cash)       → 🟢 = GelirTablosu Parasal K/K satırı
İşletme Sermayesi Değişimi               → 🔵 girdi (Senaryolar'dan)
İşletme Faaliyetlerinden Nakit (CFO)     → ⬛ formül (= yukarıdaki 5 satırın toplamı)

YATIRIM FAALİYETLERİ:
  CapEx                                  → 🔵 girdi (= -Hasılat × CapEx/Hasılat%)
  CapEx/Hasılat %                        → ⬛ formül

SNA (FCF) = CFO + CapEx                  → ⬛ formül
  SNA Marjı %                            → ⬛ formül
```

> **CapEx yıl ayrımı:** CapEx/Hasılat(%) FY2026 ve FY2027 için ayrı Senaryolar satırından beslenir (bkz. Sayfa 5 row haritası).

### Sayfa 4: Bilanço (Bilanco)

Adım 1B yapısı. **Üç-tablo entegrasyonu** ile GelirTablosu ve NakitAkış'a bağlı. [v1.7]

**Üç-Tablo Entegrasyon Kuralları:**
1. **Özkaynaklar (projeksiyon):** `= Önceki Dönem Özkaynaklar + Net Kâr − Temettü − Buyback` (GelirTablosu Net Kâr satırına formül referansı).

> **🔴 TEMETTÜ/BUYBACK KONTROLÜ (ZORUNLU — NVO REG-NVO-001 dersi):**
> Özkaynaklar formülünde temettü ve buyback düşülmezse nakit PLUG şişer → bilanço denklem tutar ama ekonomik olarak yanlıştır.
> **Her şirket için T2 başında şu 3 soruyu sor:**
> (a) Şirket temettü ödüyor mu? → Son 3 yılın nakit akış tablosundan "Dividends Paid" satırı
> (b) Şirket buyback yapıyor mu? → "Repurchase of Capital Stock" satırı
> (c) Yıllık toplam nakit çıkışı ne? → Temettü + Buyback = Toplam Shareholder Return
>
> **Formül:** `ÖK(t) = ÖK(t-1) + Net Kâr(t) − Temettü(t) − Buyback(t)`
> Temettü/buyback yoksa 0 yaz ama SORGULAMADAN sıfır kabul etme.
>
> **Sanity:** Nakit PLUG ≈ önceki dönem nakit ± %30 olmalı. Nakit 3x artıyorsa temettü unutulmuş olabilir.

2. **Nakit (projeksiyon):** Bilanço **plug** değişkenidir — `= Toplam Yük. + Özkaynaklar − Duran Varlıklar − Diğer Dönen Varlıklar`. Bu formül bilançonun **her zaman** dengelenmesini garanti eder.
3. **Diğer kalemler:** Tarihsel değerler hardcode, projeksiyon değerleri input (Senaryolar'dan veya doğrudan).

> **Plug neden sirkular değil?** Nakit formülü kendi değerine referans vermez — Toplam Kaynaklar (= TY + ÖK) üzerinden gider, Toplam Dönen Varlıklar üzerinden değil.

```
DÖNEN VARLIKLAR:
  Nakit ve Nakit Benzerleri [PLUG]        → ⬛ formül (= TY + ÖK − TDur − DiğerDV)
  Finansal Yatırımlar                     → 🔵 girdi
  Ticari Alacaklar                        → 🔵 girdi
  Stoklar                                 → 🔵 girdi
  Diğer Dönen Varlıklar                   → 🔵 girdi
Toplam Dönen Varlıklar                    → ⬛ SUM

DURAN VARLIKLAR:
  (tüm alt kalemler)                      → 🔵 girdi
Toplam Duran Varlıklar                    → ⬛ SUM
TOPLAM VARLIKLAR                          → ⬛ formül

KV YÜKÜMLÜLÜKLER / UV YÜKÜMLÜLÜKLER      → 🔵 girdi alt kalemler + ⬛ SUM
TOPLAM YÜKÜMLÜLÜKLER                      → ⬛ formül

TOPLAM ÖZKAYNAKLAR                        → ⬛ formül (= Önceki + GelirTablosu Net Kâr)
TOPLAM KAYNAKLAR                          → ⬛ formül (= TY + ÖK)

DENGE KONTROLÜ = TV − TK                 → ⬛ formül (=0 olmalı)
  Conditional formatting: 🟢 yeşil = 0, 🔴 kırmızı ≠ 0

HESAPLANAN METRİKLER:
Net Finansal Borç                         → ⬛ = KV Borç + UV Borç − Nakit − FinYat
Cari Oran                                → ⬛ = TDV / TKV
```

### Sayfa 5: Senaryolar (Senaryolar)

Adım 6'daki varsayım setinin Excel versiyonu. **Tüm projeksiyon girdileri bu tablodan IF formülüyle çekilir.** [v1.7]

**Senaryo Seçici Mekanizması:**
- B4: Dropdown (Bear/Base/Bull) → B5: `=IF(B4="Bear",1,IF(B4="Bull",3,2))`
- Diğer sayfalardaki formül: `=IF($B$5=1,Senaryolar!B{row},IF($B$5=3,Senaryolar!D{row},Senaryolar!C{row}))`

**FM Senaryolar Satır Haritası (sabit — diğer sayfalar buraya referans verir):**

```
Row  | Parametre                    | Ayı 🔵 | Temel 🔵 | Boğa 🔵
-----|------------------------------|--------|---------|--------
7    | YoY Büyüme FY2026T           |        |         |
8    | YoY Büyüme FY2027T           |        |         |
9    | Terminal Büyüme (g)           |        |         |
10   | FAVÖK Marjı (hedef)           |        |         |
11   | ETR (Terminal)                |        |         |
12   | SMM/Hasılat FY26 (%)          |        |         |
13   | PAZ/Hasılat FY26 (%)          |        |         |
14   | GYG/Hasılat FY26 (%)          |        |         |
15   | CapEx/Hasılat FY26 (%)        |        |         |
16   | İS Değişimi FY26 (M)          |        |         |
17   | İS Değişimi FY27 (M)          |        |         |
18   | Senaryo Olasılığı             | %25    | %50     | %25
19-20| Amortisman FY26/FY27          |        |         |
21-22| Finansman Gideri FY26/FY27    |        |         |
23-24| Banka Faizi FY26/FY27         |        |         |
25-26| Parasal K/K FY26/FY27         |        |         |
27-28| Diğer Faal. FY26/FY27         |        |         |
29-30| Yat.Faal. FY26/FY27           |        |         |
31   | SMM/Hasılat FY27 (%)          |        |         |
32   | PAZ/Hasılat FY27 (%)          |        |         |
33   | GYG/Hasılat FY27 (%)          |        |         |
34   | CapEx/Hasılat FY27 (%)        |        |         |
```

> **Yıl bazlı marj ayrımı:** Row 12-15 (FY26 marjları) ve Row 31-34 (FY27 marjları) **ayrı değerlerdir**. GelirTablosu'nun FY2026 sütunu Row 12-15'e, FY2027 sütunu Row 31-34'e referans verir. Bu sayede marjların yıldan yıla gelişimi (ölçek etkisi, maliyet optimizasyonu vb.) modellenebilir. [v1.7]

**Diğer sayfalar bu sayfadan değer çeker.** Aktif senaryo seçimi (dropdown) ile model tek tıkla değişir.

### Sayfa 6: İNA Girdileri (INAGirdileri)

bbb-dcf Faz 1.5'e handoff sayfası. Bu sayfa T2 sınırıdır — hesaplama bbb-dcf'te yapılır.

> **🔴 FORMAT KURALI (NVO v4.3 dersi):**
> INAGirdileri `setup_tab()` ile değil ayrı yazıldığı için format ATLANIR.
> **Her hücreye number_format ZORUNLU ata:**
> - Parasal/adet değerler (Hasılat, Borç, Pay Sayısı): `#,##0`
> - Yüzde değerler (Büyüme, ETR, Marj, Halka Açıklık, β, Rf, ERP, CRP): `0.0%`
> - Oran değerler (D/E, S/C, ICR): `0.00`
> - Tüm B sütunu: `Alignment(horizontal='right')`
> - Formül hücreleri: yeşil font (`008000`), girdi hücreleri: mavi font (`0000FF`)

```
AOSM (WACC) Girdileri:
  Risksiz Getiri (Rf)                    → 🔵 girdi + kaynak
  Olgunlaşmış Pazar ERP                  → 🔵 girdi (Damodaran)
  Ülke Risk Primi (CRP)                  → 🟢 = Coğrafi kırılımdan ağırlıklı
  Kaldıraçsız Beta (β_U)                → 🔵 girdi + kaynak (Damodaran sektör)
  Vergi Oranı (t)                        → 🟢 = ETR link
  D/E Oranı                              → 🟢 = Bilanço link
  Borçlanma Maliyeti (Kd)                → 🔵 girdi + kredi notu
  Kaldıraçlı Beta (β_L)                 → ⬛ = β_U × (1 + (1−t) × D/E)
  Özsermaye Maliyeti (Ke)                → ⬛ formül

Büyüme Girdileri:
  Gelir büyüme oranları (Faz 1-2-Terminal) → 🟢 = Senaryolar link
  Terminal marj                           → 🟢 = Senaryolar link

Yatırım Girdileri:
  S/C                                    → 🟢 = GelirTablosu link
  CapEx/Hasılat                          → 🟢 = Senaryolar link

Pay Bilgileri:
  Toplam Pay Sayısı                      → 🔵 girdi (KAP'tan)
  Hisse Başı Değer                       → ⬛ (bbb-dcf hesaplar)
```

### openpyxl Uygulama Kuralları [v2.0 — NVO dersleri]

> **🔴 7 ZORUNLU BİÇİMLENDİRME KURALI (atlanan her biri açılış hatası üretir):**
> 1. `DataValidation(type="list", formula1='"Bear,Base,Bull"')` → Senaryolar B4'e eklenmeli. Bu OLMADAN dropdown çalışmaz, senaryo seçici kırılır.
> 2. `ws.sheet_view.showGridLines = False` → TÜM sayfalarda kılavuz çizgileri kapalı.
> 3. `ws.merge_cells('A1:{SON_SÜTUN}1')` → Her sayfada Row 1 merge.
> 4. Row 1 font: `Font(color="2C3E50", bold=True, size=14)`. Subtitle: `Font(color="888888", size=9)`.
> 5. Header (Row 5/6): `Font(color="FFFFFF", bold=True, size=11)` + `PatternFill("solid", fgColor="2C3E50")`.
> 6. Tab renkleri: veri tab'ları `F7931A` (turuncu), Senaryolar `3498DB` (mavi).
> 7. `Conditional formatting` Bilanço denge satırına: `CellIsRule(operator='equal', formula=['0'], fill=yeşil)` + `CellIsRule(operator='notEqual', formula=['0'], fill=kırmızı)`.

> **🔴 PLUG FORMÜLÜ KURALI (Bilanço Nakit satırı):**
> PLUG formülü EBEBK'ten kopyalanırken satır numaraları DEĞİŞİR. Her şirkette bilanço satır sayısı farklıdır.
> **Formül:** `Nakit = Toplam_Kaynaklar_SATIRI - Toplam_Duran_SATIRI - (FinYat + TicAlac + Stok + Diger)`
> **Doğrulama:** Script bittikten sonra PLUG satır referanslarını yazdır ve kontrol et:
> ```python
> print(f"PLUG: Nakit(R{nakit_row}) = TK(R{tk_row}) - TDur(R{tdur_row}) - ...")
> ```

> **🔴 SENARYO SEÇİCİ KURALI:**
> Senaryo IF formülleri **HER ZAMAN** `Senaryolar!$B$5` referans alır.
> GelirModeli veya başka tab'da AYRI bir B4/B5 kopyası OLUŞTURMA.
> `=IF(Senaryolar!$B$5=1,Senaryolar!B{row},IF(Senaryolar!$B$5=3,Senaryolar!D{row},Senaryolar!C{row}))`

> **🔧 xlsx skill openpyxl_helpers.py KULLAN (v2.1):**
> Tüm tuzak çözümleri, renk sabitleri, RowTracker ve setup fonksiyonları hazır modülde:
> ```python
> import sys; sys.path.insert(0, str(Path.home() / '.openclaw/workspace/skills/xlsx/scripts'))
> from openpyxl_helpers import (
>     formula_embeddable, scenario_if, safe_ratio,
>     RowTracker, setup_standard_sheet, write_section_header, write_hist_values, write_proj_formula,
>     FONT_INPUT, FONT_FORMULA, FONT_LINK, FONT_WARNING, FONT_FORMULA_BOLD, FONT_ITALIC,
>     FILL_HISTORICAL, FILL_TOTAL, FILL_SECTION, FILL_INPUT, FILL_HEADER,
>     FMT_PERCENT, FMT_NUMBER, FMT_RATIO, THIN_BORDER,
> )
> ```
> Bu modül SKILL.md'deki 8 tuzağı çözer. Sıfırdan stil tanımlamak YASAK — bu modülü import et.

```python
# === EBEBK REFERANS STİL SETİ (birebir kopyala) ===
# NOT: Yukarıdaki openpyxl_helpers.py tercih edilir. Aşağıdaki blok eski referans olarak korunmuştur.
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

# Renk kodları (2C3E50 şeması)
TITLE = Font(color="2C3E50", bold=True, size=14)     # Row 1
SUBTITLE = Font(color="888888", bold=False, size=9)    # Row 2-3
HDR_FONT = Font(color="FFFFFF", bold=True, size=11)    # Row 5 header
HDR_FILL = PatternFill("solid", fgColor="2C3E50")     # Row 5 header fill
MAVI_FONT = Font(color="0000FF", size=10)              # Kullanıcı girdisi
SIYAH_FONT = Font(color="000000", size=10)             # Formül
SIYAH_BOLD = Font(color="000000", bold=True, size=10)  # Toplam satırları
YESIL_FONT = Font(color="008000", size=10)             # Çapraz sayfa link
WARN_FONT = Font(color="FF0000", bold=True, size=10)   # Senaryo uyarı
WARN_FONT_BIG = Font(color="FF0000", bold=True, size=12) # AKTIF SENARYO
GRI_FONT = Font(color="888888", size=9)                # Senaryo kodu

GRI_FILL = PatternFill("solid", fgColor="E8E8E8")     # Tarihsel arka plan
BOLUM_FILL = PatternFill("solid", fgColor="D5E8D4")   # Bölüm başlığı (yeşilimsi)
TOPLAM_FILL = PatternFill("solid", fgColor="D6E4F0")  # Toplam/hesaplanan (mavimsi)
SENARYO_FILL = PatternFill("solid", fgColor="FFFFCC")  # Senaryo B4 + input hücreleri

# Tab renkleri
TAB_ORANGE = "F7931A"  # Veri tab'ları (5 adet)
TAB_BLUE = "3498DB"    # Senaryolar tab'ı (1 adet)

# Format kuralları
YUZDE_FORMAT = '0.0%'
SAYI_FORMAT = '#,##0'
DEC2_FORMAT = '#,##0.00'

# Sayfa genişlikleri
# A sütunu: 38 (kalem adı), B-G sütunları: 16 (veri), Senaryolar E: 35 (not)

# === HER SAYFA BAŞLANGICI (zorunlu) ===
def setup_tab(ws, title, sub1, sub2, headers, ncol, tab_color=TAB_ORANGE, freeze='B6'):
    ws.column_dimensions['A'].width = 38
    for i in range(2, ncol+1):
        ws.column_dimensions[get_column_letter(i)].width = 16
    ws.freeze_panes = freeze
    ws.sheet_properties.tabColor = tab_color
    ws.sheet_view.showGridLines = False  # ZORUNLU
    ws.row_dimensions[1].height = 19
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncol)
    ws.cell(row=1, column=1, value=title).font = TITLE
    ws.cell(row=2, column=1, value=sub1).font = SUBTITLE
    ws.cell(row=3, column=1, value=sub2).font = SUBTITLE
    for i, h in enumerate(headers):
        c = ws.cell(row=5, column=i+1, value=h)
        c.font = HDR_FONT; c.fill = HDR_FILL
        c.alignment = Alignment(horizontal='center'); c.border = THIN

# === SENARYO DROPDOWN (Senaryolar tab'ına zorunlu) ===
dv = DataValidation(type="list", formula1='"Bear,Base,Bull"', allow_blank=False)
dv.error = "Sadece Bear, Base veya Bull secebilirsiniz"
ws_senaryolar.add_data_validation(dv)
dv.add(ws_senaryolar['B4'])

# === BİLANÇO CONDITIONAL FORMATTING (zorunlu) ===
from openpyxl.formatting.rule import CellIsRule
green_fill = PatternFill("solid", fgColor="C6EFCE")
green_font = Font(color="006100")
red_fill = PatternFill("solid", fgColor="FFC7CE")
red_font = Font(color="9C0006")
ws_bilanco.conditional_formatting.add(f'B{denge_row}:G{denge_row}',
    CellIsRule(operator='equal', formula=['0'], fill=green_fill, font=green_font))
ws_bilanco.conditional_formatting.add(f'B{denge_row}:G{denge_row}',
    CellIsRule(operator='notEqual', formula=['0'], fill=red_fill, font=red_font))
```

> **Projeksiyon hücre stili:** EBEBK'te projeksiyon sütunları arka plan BEYAZ (fill yok), font MAVI (girdi) veya SİYAH (formül). Gri arka plan SADECE tarihsel sütunlarda.

### BBB Finans 147 Kalem Entegrasyonu

```python
import json, subprocess

# Veri çek
result = subprocess.run(
    ['python3', 'bbb_financials.py', ticker, '--dcf', '--json'],
    capture_output=True, text=True,
    cwd='~/.openclaw/workspace/skills/bbb-finans/scripts'
)
data = json.loads(result.stdout)

# Dönem sütunlarını oluştur
for period in data['periods']:
    # Her kalem ilgili satıra yerleşir
    # Tarihsel dönemler → GRI_FILL + SIYAH_FONT
    # Her hücrede kaynak: BBB Finans / KAP
```

### Doğrulama (Model Bittikten Sonra)

| Kontrol | Yöntem | Kabul |
|---------|--------|-------|
| Bilanço dengesi | Her dönem TV = TY + ÖK | Fark = 0 |
| Nakit tutarlılığı | NakitAkış dönem sonu = Bilanço nakit | Fark < 1 mn TL |
| **Nakit PLUG sanity** | Projeksiyon nakit ≈ önceki dönem nakit ± %30 | 3x artış → temettü/buyback unutulmuş |
| **Temettü/Buyback** | ÖK formülünde temettü+buyback düşülmüş mü? | Yoksa ÖK ve nakit şişer |
| Gelir tutarlılığı | GelirModeli toplamı = GelirTablosu hasılat | Fark = 0 |
| Negatif kontrol | Stok, PP&E, pay sayısı > 0 | Negatif yok |
| Formül kontrolü | Excel'de FORMULATEXT ile spot-check | Formül ≠ hardcoded sayı |
| Cross-check | BBB Finans toplam gelir = Model toplam gelir | <%1 fark |

---

---

## Adım 9: Döngüsel Şirket Uyarlamaları

Döngüsel sektörler: çimento, çelik, petrokimya, enerji (upstream), havacılık (kısmen), otomotiv, tarım ürünleri.
Bu sektörlerde standart T2 akışı uygulandığında **sistematik hatalar** oluşur. Bu bölüm o hataları ve düzeltmelerini tanımlar.

> Kural: Döngüsel şirket analizi başlamadan önce "Bu şirket döngüsel mi?" testi yap. Cevap evetse bu bölümdeki 5 uyarlama zorunludur.

### Döngüsellik Testi

Şu üç koşuldan ikisi gerçekleşiyorsa şirket döngüseldir:
1. Hasılat veya EBIT marjı 10 yılda >%40 dalgalanma gösteriyor
2. Emtia fiyatı (çelik, petrol, çimento, buğday) geliri direkt etkiliyor
3. Kapasite kullanım oranı %60-%95 arasında gidip geliyor

---

### Uyarlama 1: Normalized Earnings (Döngüsel Kârı Normalleştir)

**Sorun:** Peak veya trough döneminde analiz yapıyorsan F/K ve EV/FAVÖK yanıltıcı olur. Peak'te ucuz görünür (düşük F/K), trough'ta pahalı görünür (yüksek F/K).

**Çözüm:** Mid-cycle (orta döngü) kârı hesapla.

```
# Yöntem 1 — Tarihsel ortalama marj
Normalized EBIT Marjı = Son tam döngü (7-10Y) EBIT marjı ortalaması
Normalized EBIT = Güncel Gelir × Normalized EBIT Marjı

# Yöntem 2 — Emtia fiyatı normalizasyonu (daha doğru)
Normalized Gelir = Güncel Hacim × Mid-cycle Emtia Fiyatı
Normalized EBIT = Normalized Gelir × Mid-cycle Marj

# BIST çimento örneği:
Gerçek FY2024 EBIT: 4.2 milyar TL (yüksek dönem)
Tarihsel 7Y ortalama EBIT marjı: %22 (vs güncel %31)
Normalized EBIT: Gelir × 0.22 = 2.98 milyar TL
→ Gerçek EV/EBIT: 4x (ucuz görünür) | Normalized EV/EBIT: 5.6x (daha gerçekçi)
```

**Ne zaman uygula:** Comps tablosunda, DCF terminal marjı belirlerken, F/K bazlı değerlemede.

---

### Uyarlama 2: Through-the-Cycle Değerleme Metrikleri

Peak EV/FAVÖK veya F/K üzerinden comps yapmak yanıltıcı. Döngüsel şirketler için ek metrikler:

| Metrik | Tanım | Ne Zaman Güçlü |
|--------|-------|----------------|
| **EV/Kapasite** | EV / ton (çimento, çelik) veya EV / varil (petrol) | Her döngü noktasında karşılaştırılabilir |
| **PD/Yenileme Değeri** | Piyasa değeri / benzer kapasitenin inşa maliyeti | Varlık-bazlı değerleme için |
| **EV/EBITDA (normalized)** | Normalized EBITDA üzerinden | Peak/trough farkını kaldırır |
| **Temettü Verimi (normalized)** | Sürdürülebilir temettü / hisse fiyatı | Peak temettüden kaçın |

**BIST'e özgü referans değerler:**

| Sektör | Metrik | Tarihsel Medyan |
|--------|--------|-----------------|
| Çimento | PD/Klinker kapasitesi | 7.5x (14 peer medyanı) |
| Çelik | EV/Ton | Sektöre göre değişir — Damodaran baz al |
| Petrokimya | EV/EBITDA normalized | Global peer ile karşılaştır |

---

### Uyarlama 3: Terminal Marj Belirleme

**Hata:** Döngüsel zirvede analiz yapılırken güncel marj terminal marj alınır → DCF şişer.

**Kural:** Terminal marj = Tarihsel 10Y ortalama EBIT marjı, değil son yıl marjı.

```
# Çimento şirketi örneği:
Son yıl EBIT marjı: %31 (yüksek dönem)
Tarihsel 10Y ortalama: %22
Damodaran sektör ortalaması: %19

Terminal marj: MAX(%19 sektör, %22 tarihsel ort.) = %22
→ "Güçlü moat olduğu için tarihsel ortalamanın üzerinde kalacak" argümanı
  ancak spesifik ve ölçülebilir gerekçeyle kabul edilir.
```

---

### Uyarlama 4: Senaryo Çerçevesi — Emtia Fiyatı Eklemleme

Standart Bull/Base/Bear senaryo çerçevesine emtia fiyatı varsayımı eklenir:

```
| Varsayım | Ayı | Temel | Boğa |
|----------|-----|-------|------|
| Emtia Fiyatı ($/ton veya $/bbl) | [Trough] | [Mid-cycle] | [Peak-1] |
| KKO (Kapasite Kullanım Oranı) | %60-65 | %72-78 | %83-88 |
| Gelir CAGR (5Y) | %X | %X | %X |
| EBIT Marjı (Terminal) | [Trough marjı] | [Mid-cycle] | [Peak marjı] |
| Emtia Volatilitesi | Yüksek | Orta | Düşük |
```

**Emtia fiyatı kaynakları:**
- Uluslararası emtia: web_search → LME (çelik, alüminyum), ICE (petrol), CBOT (tarım)
- Türkiye iç pazar: OSD (otomotiv), TÇD (çimento), TÇÜD (çelik)
- Damodaran commodity beta tablosu: sektör betası emtia döngüsünü reflekte eder

---

### Uyarlama 5: EV/Kapasite ile Sanity Check

DCF sonucunu EV/Kapasite metrikiyle cross-check et.

```
DCF → Hisse başı değer hesapla
     → Equity değeri × (1 + Net Borç/Equity) = EV
     → EV / Kapasite (ton, varil, vb.) = İmplied EV/Kapasite

Karşılaştır: BIST peer medyanı veya Damodaran sektör ortalaması
Kabul aralığı: İmplied değer peer medyanının ±%30 içinde
Dışında kalıyorsa: DCF varsayımlarını sorgula
```

---

### Döngüsel Şirket Checklist (T2 sonu, döngüsel sektörler için ek)

- [ ] Döngüsellik testi yapıldı (3 koşul kontrol edildi)
- [ ] Normalized earnings hesaplandı (tarihsel 7-10Y marj ortalaması)
- [ ] Terminal marj: son yıl değil, mid-cycle ortalama
- [ ] EV/Kapasite metrigi comps tablosuna eklendi
- [ ] Senaryo çerçevesine emtia fiyatı varsayımı eklendi
- [ ] DCF çıktısı EV/Kapasite ile cross-check yapıldı

---

## §10. T2 → T3 Handoff — Excel Cell Map

T3 (hedef-fiyat-derivasyonu + bbb-dcf) T2 Excel modelinden şu verileri çeker. Cell adresleri standart satır numarası değil, **named range** veya **satır etiketine göre arama** ile erişilir (agent `_hucre_deger_ara` fonksiyonunu kullanır).

### Zorunlu Handoff Noktaları (T3 Başlamadan Hazır Olmalı)

> **Birim Kuralı:** IAS 29 şirketlerinde Excel modeli IAS 29 düzeltmeli (reel, her dönem kendi Dec bazı) verileri içerir.
> T3 (bbb-dcf) reel DCF yapıyorsa → baz yıl verisi Dec {SON_FY} bazında olur.
> Senaryo varsayımları (handoff #16) §6A'daki Guidance Rekonsilasyonu ile tutarlı olmalıdır.

| # | Veri | Kaynak Sheet | Satır Etiketi | Birim | Kullanıldığı Yer |
|---|------|-------------|---------------|-------|-----------------|
| 1 | Son FY + TTM Hasılat | GelirModeli | `TOPLAM HASILAT` | IAS 29 Dec {SON_FY} | İNA büyüme varsayımı baz |
| 2 | Son FY + TTM EBIT | GelirTablosu | `FAALİYET KÂRI` | IAS 29 Dec {SON_FY} | İNA marj varsayımı baz |
| 3 | Son FY + TTM FAVÖK | GelirTablosu | `FAVÖK` | IAS 29 Dec {SON_FY} | Comps: EV/FAVÖK |
| 4 | Son FY + TTM Net Kâr | GelirTablosu | `NET KÂR` | IAS 29 Dec {SON_FY} | Comps: F/K |
| 5 | Son FY + TTM HBK | GelirTablosu | `HBK` | TL/hisse | Forward F/K hesabı |
| 6 | ROIC (son FY + TTM) | GelirTablosu | `ROIC` | Oran (%) | Moat barometresi, sanity check |
| 7 | S/C (son FY + TTM) | GelirTablosu | `S/C` | Oran (x) | Damodaran reinvestment |
| 8 | ICR | GelirTablosu | `ICR` | Oran (x) | Sentetik rating cross-check |
| 9 | ETR | GelirTablosu | `ETR` | Oran (%) | İNA vergi varsayımı |
| 10 | Toplam Pay Sayısı | INAGirdileri | `Pay Sayısı` | Adet | Hisse başı değer |
| 11 | Net Borç | Bilanco | `Net Borç` | IAS 29 Dec {SON_FY} | EV → Equity bridge |
| 12 | Yatırılmış Sermaye (IC) | Bilanco | `Yatırılmış Sermaye` | IAS 29 Dec {SON_FY} | Reinvestment hesabı |
| 13 | CapEx/Hasılat % | NakitAkis | `CapEx/Hasılat` | Oran (%) | Reinvestment varsayımı |
| 14 | SNA (FCF) | NakitAkis | `SNA` | IAS 29 Dec {SON_FY} | FCF yield, comps |
| 15 | Gelir segmenti payları (coğrafi) | GelirModeli | `CRP Ağırlıkları` | Oran (%) | Revenue-weighted CRP |
| 16 | Senaryo varsayımları (3 set) | Senaryolar | Tüm sayfa | §6A birimiyle AYNI | İNA 3 senaryo |
| 17 | Rf, ERP, CRP, β_U, Kd | INAGirdileri | İlgili satırlar | Oran (%) | WACC hesabı (bbb-dcf) |

> **IAS 29 olmayan şirketlerde:** Birim sütunundaki "IAS 29 Dec {SON_FY}" → "Nominal TL" olarak değişir.

### Named Range Standartı

Excel modelinde aşağıdaki named range'ler tanımlanır (opsiyonel ama T3 otomasyonunu kolaylaştırır):

```
HASILAT_TTM       → GelirModeli!{son TTM sütunu}{Toplam Hasılat satırı}
EBIT_TTM          → GelirTablosu!{son TTM sütunu}{EBIT satırı}
FAVOK_TTM         → GelirTablosu!{son TTM sütunu}{FAVÖK satırı}
NET_KAR_TTM       → GelirTablosu!{son TTM sütunu}{Net Kâr satırı}
HBK_TTM           → GelirTablosu!{son TTM sütunu}{HBK satırı}
ROIC_TTM          → GelirTablosu!{son TTM sütunu}{ROIC satırı}
NET_BORC           → Bilanco!{son dönem sütunu}{Net Borç satırı}
IC                 → Bilanco!{son dönem sütunu}{IC satırı}
PAY_SAYISI         → INAGirdileri!{Pay Sayısı hücresi}
WACC_TL            → INAGirdileri!{WACC hücresi} (bbb-dcf hesapladıktan sonra geri yazılır)
WACC_USD           → INAGirdileri!{WACC USD hücresi}
```

### T3 → T2 Geri Yazma (bbb-dcf Faz 2 Sonrası)

bbb-dcf Faz 2 tamamlandığında şu değerler Excel'e geri yazılır:

| Veri | Hedef Sheet | Satır |
|------|-------------|-------|
| WACC (TL) | INAGirdileri | AOSM satırı |
| WACC (USD) | INAGirdileri | AOSM USD satırı |
| Kaldıraçlı Beta | INAGirdileri | β_L satırı |
| Ke (Özsermaye maliyeti) | INAGirdileri | Ke satırı |
| Firma Değeri | INAGirdileri | Firma Değeri (yeni satır) |
| Hisse Başı Değer (3 senaryo) | INAGirdileri | Hisse Değeri satırları |

### Doğrulama (Handoff Sonrası)

```
- [ ] T2'deki 17 handoff noktasının tamamı dolu mu?
- [ ] GelirModeli toplamı = GelirTablosu hasılat (cross-check)?
- [ ] Net Borç: Bilanço'daki ve comps'taki aynı mı?
- [ ] Pay sayısı: BBB Finans'tan doğrulandı mı?
- [ ] Senaryo sayfasında 3 set varsayım gerekçeli mi?
- [ ] CRP ağırlıkları coğrafi gelir kırılımıyla tutarlı mı?
- [ ] T1'den gelen Yapısal Analiz Tetikleyicileri işlendi mi? (segment breakeven, M&A şerefiye, kapasite ROI vb.) [v1.8]
- [ ] Forward bilanço projeksiyonu hazır mı? (en az FY+1T sütunu: varlıklar, borçlar, özkaynak) [v1.8]
- [ ] Forward nakit akış projeksiyonu hazır mı? (en az FY+1T: CFO, CapEx, FCF) [v1.8]
- [ ] §6A Guidance Rekonsilasyonu yapıldı mı? (Reel↔Nominal çevirisi, sapma yönü ve gerekçesi) [v1.9]
- [ ] Handoff noktalarındaki birimler (IAS 29 / Nominal / Reel) DCF yaklaşımıyla tutarlı mı? [v1.9]
```

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-17 | v1.0 oluşturuldu — bbb-dcf handoff kuralı, BIST/KAP kalem sıralama, TTM/IC/S/C/ICR/ETR hesaplamalar, senaryo varsayım çerçevesi, IAS 29 kontrol |
| 2026-03-17 | v1.1 — T2 Excel 6-tab spec (openpyxl), renk kodlama, BBB Finans 147 kalem entegrasyonu, doğrulama kontrolleri |
| 2026-03-18 | v1.2 — §9 Döngüsel Şirket Uyarlamaları: normalized earnings, through-the-cycle metrikler, terminal marj kuralı, emtia senaryo çerçevesi, EV/Kapasite sanity check |
| 2026-03-18 | v1.3 — §10 T2→T3 Handoff Excel Cell Map: 17 zorunlu handoff noktası, named range standardı, T3→T2 geri yazma, handoff doğrulama checklist |
| 2026-03-18 | v1.4 — KAP Finansal Tablolar PDF: On Kosullara eklendi. Adim 3G (Dipnot Dogrulama) eklendi: efektif faiz (Kd), ETR normalizasyonu (vergi tesvik), tek seferlik kalem ayristirma, doviz pozisyon kirimi. T2 Checklist'e dipnot maddesi eklendi. Is Yatirim 147 kalem + dipnot PDF = tam resim. |
| 2026-03-19 | v1.5 — 6-tab standardinda satir hedefleri guncellendi: BIST gerceklerine uygun aralıklar (GelirTablosu 30-40, NakitAkis 20-30, Bilanco 25-35, Senaryolar 10-15, INAGirdileri 15-20). GelirModeli segment sayisi 5-15 satir, cografya 2-10 satir olarak netlesti. |
| 2026-03-22 | v1.6 — Bolum 0 eklendi: Temel Metodolojik Referanslar tablosu (reel/nominal, WACC, temettü, kazanç kalitesi, EV FX harmonizasyonu) — senaryo-metodoloji.md v3.0 ve karsilastirmali-degerleme.md §6A ile cross-reference |
| 2026-03-23 | v1.8 — T1 Yapısal Analiz Tetikleyicileri handoff eklendi: T1'den gelen tetikleyiciler T2'de zorunlu analiz kalemlerine dönüşür. Forward BS/CF projeksiyonu zorunluluğu checklist'e eklendi (en az FY+1T sütunu). "İş Yatırım API" → "İş Yatırım" düzeltmesi |
| 2026-03-22 | v1.7 — Excel model iyileştirmeleri skill dosyasına yansıtıldı: (1) NakitAkış CFO 5-bileşen formülü belgelendi (FAVÖK+Vergi+Faiz+Parasal+İS), (2) Bilanço 3-tablo entegrasyonu belgelendi (Özkaynaklar=Prior+NetKâr, Nakit=plug), (3) Senaryolar satır haritası eklendi (Row 7-34, 28 parametre), (4) Yıl bazlı marj ayrımı belgelendi (FY26→Row12-15, FY27→Row31-34), (5) Conditional formatting kuralı (denge kontrolü yeşil/kırmızı), (6) T2 Doğrulama Checklist'e 4 yeni madde |
| 2026-03-25 | v1.9 — EBEBK REG: §6A Guidance tablosuna Birim sütunu + Reel↔Nominal Rekonsilasyon şablonu (IAS 29 zorunlu). §10 Handoff 17 noktaya Birim sütunu. Çıkış Gate'e guidance rekonsilasyon + birim tutarlılık kontrolü. |
