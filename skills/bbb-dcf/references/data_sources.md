# Veri Kaynakları — Detaylı Referans

## Veri Hiyerarşisi

### Katman 1: KAP (BİRİNCİL — TÜM FİNANSAL VERİLER BURADAN)
- **Finansal Tablolar:** `bbb_kap.py {TICKER} --kap-summary` → Bilanço + Gelir Tablosu (4 dönem)
- **Detaylı Tablolar (147 kalem):** `bbb_financials.py {TICKER} --full` → İş Yatırım API (KAP kaynaklı)
- **DCF Verileri (JSON):** `bbb_financials.py {TICKER} --dcf --json` → Tüm dönemler, hesap kalemleri
- **XBRL Ham Veri:** `bbb_mkk.py` → MKK KAP VYK API (API key gerekli, .env'de tanımlı)
- **Faaliyet Raporları:** KAP bildirimleri → PDF indirilip okunacak
- **Son Çeyrek + Son Yıllık Faaliyet Raporu:** İKİSİ DE ZORUNLU

### Katman 1B: KAP Erişim Kuralı *(2026-02-11 — İlker talimatı)*
> **KAP'a HER ZAMAN bizim KAP API anahtarımız ile erişilir** (`bbb_mkk.py`).
> Web scraping veya Cloudflare ile uğraşma — API kullan.
> Segment verileri, ortaklık yapısı, faaliyet raporları → KAP API üzerinden.

### Katman 1C: Güncellik Kuralı — CDS, Kredi Notu, Spread *(2026-02-11 — İlker talimatı)*
> **Damodaran Excel/HTML tabloları HER ZAMAN ESKİ olabilir** — tek başına güvenme.
> Öncelik sırası:
> 1. **BBB Finans kaynağı** (varsa)
> 2. **İnternetteki en güncel VE güvenilir kaynak** (Moody's, S&P, CBONDS, Trading Economics vb.)
> 3. Damodaran tablosu sadece **cross-check** olarak kullanılır
>
> Özellikle: Ülke kredi notu, CDS spread, default spread, ERP → mutlaka online güncel kaynak.

### Katman 2: Şirket Yatırımcı İlişkileri
- Şirket web sitesi → Yatırımcı İlişkileri bölümü
- **Yatırımcı Sunumları** (varsa) — en güncel olanlar
- **USD/EUR bazlı raporlama** (IAS 29 ülkeleri için şirketin kendi dönüşümü)
- Ortaklık yapısı, yönetim bilgileri
- **Şirketin kendi sitesindeki ek raporlar** (KAP'ta bulunmayan investor sunumları, fact sheet'ler)

### Katman 3: Sektör & Rekabet Verileri *(güncellenme: 2026-02-11)*
- **Yerli rakipler/peer'lar:** KAP API (`bbb_kap.py`, `bbb_financials.py`) + rakip şirketlerin Yatırımcı İlişkileri sayfaları
- **Yurt dışı eşlenikler:** Yahoo Finance skill (`yf fundamentals {TICKER}`, `yf quote {TICKER}`) + BBB Finans (varsa)
- **Sektör raporları:** Güvenilir dış kaynaklar (sektör dernekleri, düzenleyiciler)
- **Ortaklık yapısı doğrulama:** En güncel faaliyet raporu VEYA finansal rapor VEYA KAP API

### Katman 4: Makro & Piyasa Verileri
- **BBB Finans araçları:**
  - Hisse fiyatı, piyasa değeri → `bbb_kap.py` veya Yahoo Finance
  - Döviz kurları → TCMB (web_fetch)
  - Faiz oranları, enflasyon → TCMB
- **Damodaran verileri:** Beta, ERP, CRP → `dcf_tools/erp_updater.py` veya web

### Katman 5: ASLA KULLANILMAYACAKLAR (Finansal Veri İçin)
- ❌ StockAnalysis.com
- ❌ TradingView
- ❌ Investing.com
- ❌ GuruFocus
- ❌ Hafızadan veya tahminden rakam
- Bu siteler SADECE cross-check için kullanılabilir, BİRİNCİL KAYNAK OLAMAZ

---

## Çalışan Komutlar (Copy-Paste Hazır)

```bash
# Çalışma dizini
cd ~/.openclaw/workspace-can/skills/bbb-finans/scripts

# 1. KAP Özet Finansallar (BİRİNCİL — her DCF'in ilk adımı)
python3 bbb_kap.py {TICKER} --kap-summary

# 2. Detaylı Finansal Tablolar (147 kalem, İş Yatırım kaynaklı)
python3 bbb_financials.py {TICKER} --start-year 2022 --end-year 2025 --section all --full

# 3. DCF İçin JSON Veri (tüm dönemler, programatik erişim)
python3 bbb_financials.py {TICKER} --dcf --json > /tmp/{TICKER}_dcf.json

# 4. Şirket Bilgisi (KAP MKK API)
python3 bbb_kap.py {TICKER} --lookup

# 5. Yahoo Finance (yurt dışı peer'lar)
# yahoo-finance skill: yf fundamentals LVS / yf fundamentals WYNN

# 6. Damodaran Verileri
# web_fetch: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html
# web_fetch: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html

```

---

## BBB Finans Zorunlu Kullanım

| Veri | Araç | Fonksiyon |
|------|------|-----------|
| **Hisse fiyatı** | `bbb_isyatirim` | `get_stock_data('THYAO')` → HGDG_KAPANIS |
| **Piyasa değeri** | `bbb_isyatirim` | `get_stock_data()` → PD, PD_USD |
| **Pay sayısı** | `bbb_isyatirim` | `get_stock_data()` → SERMAYE (cross-check: ödenmiş sermaye KAP'tan) |
| **USD/TRY kuru** | `bbb_fx` | `get_rate('USD')` → buying, selling |
| **Finansal tablolar** | `bbb_isyatirim` | `get_financials('THYAO', start_year, end_year)` |
| **KAP verileri** | `bbb_kap_financials` | Detaylı XBRL verileri |

---

## Faaliyet Raporu & Yatırımcı Sunumları Analizi

### Zorunlu Dokümanlar
Her DCF öncesinde şirketin aşağıdaki dokümanları indirilip okunmalı:
1. **Son yıllık faaliyet raporu** — KAP'tan çekilir (birincil kaynak)
2. **Son çeyrek faaliyet raporu** — KAP'tan çekilir, yıllık ile karşılaştırılır
3. **Yatırımcı sunumları** — Şirketin kendi web sitesi → Yatırımcı İlişkileri bölümünde "sunum" adıyla paylaşılan ek dokümanlar (varsa)

### Kaynak Hiyerarşisi
- **Birincil:** KAP üzerinden çekilir (hem faaliyet raporları hem finansal tablolar)
- **İkincil:** Şirketin kendi sitesi → Yatırımcı İlişkileri (özellikle USD bazlı raporlar varsa — THY örneğindeki gibi)
- KAP dışı kaynak kullanılırsa → **tarih ve güncellik ekstra doğrulanmalı**

### Faaliyet Raporu Okuma Stratejisi
Türk şirketlerinde faaliyet raporları iki uçta olabilir:
- **Şablon/Boş:** Bazı şirketler asgari şablon doldurur, gerçek bilgi yok → Bu durumda yatırımcı sunumları ve KAP bildirimleri daha değerli
- **Çok Büyük/Zengin:** Yüzlerce sayfa olabilir → Tamamını okumak token israfı

**Ne aranmalı (odak alanları):**

| Bölüm | Neden Önemli | DCF'te Nereye Gider |
|-------|-------------|---------------------|
| Yönetim değerlendirmesi / CEO mektubu | Stratejik yön, beklentiler | Büyüme varsayımları |
| Sektör analizi | Pazar büyüklüğü, rekabet | 17 Diagnostics soruları |
| Yatırım/CapEx planları | Gelecek yatırımlar | Reinvestment rate |
| Segment bazlı gelirler | Gelir çeşitliliği | FX gelir payı, dual-track kararı |
| Risk faktörleri | Şirkete özgü riskler | Beta, failure probability |
| Borç profili / vade yapısı | Refinancing riski | Kd, D/E yapısı |
| İlişkili taraf işlemleri | Holding yapısı riskleri | Holding indirimi |
| Kapasite kullanımı | Büyüme potansiyeli | Sales/Capital, Soru 11 |

**⚠️ KRİTİK:** Odaklı oku ama **önemli bir şeyi kaçırma/atlama**. Şüphe varsa, ilgili bölümü oku ve özetle.

### KAP'tan Faaliyet Raporu Çekme
- KAP bildirim türü: "Faaliyet Raporu" veya "Yıllık Rapor"
- Çeyrek: "Ara Dönem Faaliyet Raporu"
- Eğer Kaya KAP'tan nasıl çekeceğini bilmiyorsa → Can'dan destek alınır

### PDF Okunamadığında Alternatif Strateji *(2026-02-11 — TBORG kazanımı)*
> **"PDF okunamadı" mazeret değil, çözülmesi gereken bir engel.**
> KAP'tan çekilen PDF binary olarak gelebilir. Sırasıyla dene:
> 1. Web'de HTML/metin versiyonu ara (şirket adı + "faaliyet raporu" + yıl)
> 2. Şirket sitesi → Yatırımcı İlişkileri sayfası
> 3. KAP'ta alternatif dosya formatı (aynı bildirimde birden fazla ek olabilir)
> 4. Tarayıcı ile PDF'i aç ve snapshot al
> 5. OCR aracı kullan
>
> **TBORG dersi:** Faaliyet raporu okunamadığı için ortaklık yapısı doğrulanamadı → ciddi hata.

---

## Can'ın API Çağrıları

```python
# KAP'tan veri çekme (birincil)
from bbb_mkk import get_disclosure_data, extract_flat_items
data = get_disclosure_data('{disclosureId}')
items = extract_flat_items(data)

# İş Yatırım (fallback)
from bbb_financials import get_financials
financials = get_financials('THYAO', period='annual')
```

### Temel KAP XBRL Field'ları (19 Zorunlu)

| Field | Açıklama | Damodaran |
|-------|----------|-----------|
| `Revenue` | Hasılat | B11 |
| `ProfitLossFromOperatingActivities` | EBIT | B12 |
| `FinanceCosts` | Finansman Giderleri | B13 |
| `Equity` | Toplam Özkaynaklar | B14 |
| `CurrentBorowings` + `LongtermBorrowings` | Toplam Borç | B15 |
| `CashAndCashEquivalents` | Nakit | B18 |
| `InvestmentAccountedForUsingEquityMethod` | İştirakler | B19 |
| `NoncontrollingInterests` | Azınlık Payları | B20 |
| `IssuedCapital` | Ödenmiş Sermaye (÷1 = pay sayısı) | B21 |
| `ProfitLossBeforeTax` | EBT | B23 payda |
| `IncomeTaxExpenseContinuingOperations` | Vergi | B23 pay |

---

## Veri Kaynakları Özet Tablosu

| Sıra | Kaynak | Veri | Erişim |
|------|--------|------|--------|
| 1 | **KAP (MKK XBRL)** | Finansal tablolar (237 field) | `bbb_mkk.py` → `get_disclosure_data()` |
| 2 | **İş Yatırım API** | Finansal tablolar (fallback) | `bbb_financials.py` |
| 3 | **Yahoo Finance** | Hisse fiyatı, piyasa değeri | Web fetch |
| 4 | **TCMB** | Risksiz oran (10Y DİBS), enflasyon | Web fetch |
| 5 | **Damodaran** | ERP, sektör betaları, spread'ler | `erp_updater.py` + web |

---

## MKK VYK API Durumu

> **⚠️ MKK VYK API Durumu (Mart 2026 — hâlâ DEV):**
> `bbb_mkk.py` şu anda DEV ortamını kullanıyor (`apigwdev.mkk.com.tr`) — veriler 2023 Q3'te donmuş.
> Production erişimi İlker'in MKK Portal'dan (`apiportal.mkk.com.tr`) talep etmesini bekliyor.
> **Geçici çözüm:** `bbb_kap.py --kap-summary` (KAP direkt, IAS 29) + `--source isyatirim` (detaylı nominal).
> MKK production gelince `MKK_XBRL_MAPPING.md` ile 237 field'lık tam XBRL erişimi açılacak.

---

## Borçlanma Maliyeti Doğrulaması

- Sentetik rating'den hesaplanan Kd ile **şirketin gerçek borçlanma maliyetini** karşılaştır
- Gerçek Kd = Finansman Giderleri / Ortalama Borç (son 2-3 yıl)
- Fark varsa nedenini açıkla (TL vs FX borç kompozisyonu, lease faizi vb.)
