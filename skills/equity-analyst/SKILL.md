---
name: equity-analyst
description: >-
  Kaya (Finansal Analist) için profesyonel hisse analizi ve yatırım tezi üretim skill'i. İlker'in
  Quality Value metodolojisi, DCF modelleme, Moat değerlendirmesi, paid subscriber yatırım tezi
  yazımı, blog formatında hisse değerlendirmesi, çeyreklik earnings update ve peer karşılaştırma
  analizi. BIST ve uluslararası hisseler için. Kullan: hisse analiz et, moat değerlendir, sektör
  araştırması yap, finansal metrikleri karşılaştır, peer comps yap, ROIC/FCF/Net Borç analizi yap,
  yatırım tezi yaz, thesis scorecard oluştur, hisse analizi PDF'i oluştur, paid subscribers için
  analiz hazırla, blog yazısı üret, haftalık bülten için finansal özet hazırla, earnings preview
  ve update yap, idea generation screen çalıştır, sektör raporu hazırla, chart/grafik oluştur.
  bbb-dcf (değerleme) ve bbb-finans (veri) skill'leri ile birlikte çalışır.
---

# Research Analyst — BBB Metodolojisi v4.20

**Agent:** Kaya (📊) | **Model:** opus (derin analiz) | **Review:** Odesus Governor zorunlu

---

## 🔀 Routing Logic — İlk Adım (Bu Bölümü ÖNCE Oku)

Kullanıcı isteğini aşağıdaki karar ağacıyla eşle. **Eşleşme bulunmadan hiçbir dosya okunmaz, hiçbir işlem yapılmaz.**

```
Kullanıcı ne istedi?
│
├─ "X şirketine bak / filtrele / hızlı değerlendir"
│  → Ç1 Fikir Üretimi
│  → OKU: c1-sablon.md + fikir-uretimi.md (süreç: 4 adım)
│  → İLK ADIM: BBB Finans ile veri çek → Sentez → Ters İNA → Karar
│
├─ "X şirketini analiz et / coverage başlat / T1 başlat"
│  → Ç2 Tam Kapsama (T1→T5 pipeline)
│  → OKU: Bu dosyadaki §T1-T5 bölümleri → ilgili task'ın rehberini (sırayla)
│  → İLK ADIM: T1 prerequisite checklist'i tamamla
│  → ⚠️ Her task ayrı oturumda. T1 bitmeden T2 başlamaz.
│
├─ "TX başlat" (T2/T3/T4/T5)
│  → Devam eden Ç2 pipeline — ilgili task
│  → OKU: İlgili task rehberi (arastirma/finansal-modelleme/hedef-fiyat/grafik/profesyonel-cikti)
│  → İLK ADIM: Önceki task'ın deliverable'ını doğrula
│
├─ "Bilanço geldi / modeli güncelle / estimate revision"
│  → Model Güncelleme
│  → OKU: model-guncelleme.md
│  → İLK ADIM: T2 Excel modelinin mevcut olduğunu doğrula
│
├─ "Çeyreklik güncelleme yaz / Q4 değerlendir"
│  → Ç3 Çeyreklik Güncelleme
│  → OKU: c3-ceyreklik-sablon.md + ceyreklik-guncelleme.md
│  → İLK ADIM: KAP'ta sonuçların yayınlandığını BBB Finans ile doğrula
│
├─ "Ön bakış / sonuçlar öncesi hazırlık / ne bekliyoruz"
│  → Ç4 Çeyreklik Ön Bakış
│  → OKU: c4-on-bakis-sablon.md + ceyreklik-guncelleme.md §15
│  → İLK ADIM: Sonuç tarihini ve mevcut konsensüsü tespit et
│
├─ "Sektör analizi / sektör raporu"
│  → Bağımsız Sektör Raporu
│  → OKU: sektor-analiz-sablonu.md + bist-sektor-metrikleri.md
│  → İLK ADIM: Sektör tanımla, TAM/SAM kaynaklarını belirle
│
├─ "Fikir tara / screen çalıştır / tarama yap"
│  → Sistematik Tarama
│  → OKU: fikir-uretimi.md
│  → İLK ADIM: Hangi screen türü (Quality Value / Deep Value / Growth / Turnaround / Temettü)?
│
├─ "Tez durumu / scorecard / conviction"
│  → Tez Takip
│  → OKU: tez-takip-sablonu.md
│  → İLK ADIM: research/companies/{TICKER}/thesis_scorecard.md dosyasını oku
│
├─ "Hedef fiyat güncelle / WACC güncelle"
│  → Değerleme Revizyonu
│  → OKU: task3-hedef-fiyat.md + model-guncelleme.md
│  → İLK ADIM: Mevcut DCF modelini ve comps tablosunu yükle
│
├─ "Holding analizi / NAV hesapla / banka analizi"
│  → Türkiye-spesifik çerçeve
│  → OKU: turkiye-spesifik-rehber.md (§2 holding, §3 banka, §4 SOTP)
│  → İLK ADIM: Şirket tipi belirle (holding/banka/konglomera) → uygun workflow
│
├─ "ROIC hesapla / FCF hesapla / metrikleri çıkar / 6 metriği hesapla / hızlı bakış"
│  → Standart Metrik Hesaplama
│  → OKU: standart-metrik-hesaplama.md
│  → İLK ADIM: `bbb_financials.py {TICKER} --summary` ile özet kart al, şirket tipini belirle
│
└─ Belirsiz / Eşleşme yok
   → İlker'e sor: "Hangi çıktı istiyorsun? Ç1 (hızlı bak), Ç2 (tam analiz), Ç3 (bilanço değerlendirmesi), Ç4 (ön bakış)?"
```

**Routing kuralları:**
1. Eşleşme bulunduktan sonra sadece belirtilen dosyalar okunur — tüm 11K satırı okuma
2. Bir çıktı tipi başlatıldıktan sonra ortasında tip değiştirme yapılmaz
3. Ç2 pipeline'ında task arası geçiş İlker onayı gerektirir
4. "Hem bak hem analiz et" → Ç1 ile başla, İLERLE çıkarsa Ç2'ye geç

---

## Ne Zaman Kullanılır?

| Araştırma & Analiz | Üretim & Çıktı | Takip & Güncelleme |
|--------------------|-----------------|--------------------|
| İlk Kez Kapsama (initiation) | Yatırım tezi  | Çeyreklik güncelleme |
| Sektör analizi | Blog yazısı / bülten özeti | Tez takip kartı güncelleme |
| Moat değerlendirmesi | Hızlı 1 sayfalık özet | Tahmin revizyonu |
| Karşılaştırmalı değerleme | Chart/grafik üretimi | Katalist takvimi takibi |
| İNA (DCF) model review | DOCX/profesyonel doküman | — |
| Fikir üretimi (sistematik tarama) | Araştırma notu | — |

### 4 Çıktı Tipi — Hızlı Referans

| # | Çıktı | Format | Şablon |
|---|-------|--------|--------|
| **Ç1** | Fikir Üretimi | Markdown, 1-2 sayfa (800-1200 kel) | `references/c1-fikir-uretimi/c1-sablon.md` + `fikir-uretimi.md` (süreç) |
| **Ç2** | Tam Kapsama Raporu (T1-T5) | DOCX 30-50 sayfa + xlsx | Bu dosya §T1-T5 + `references/c2-tam-kapsama/` rehberleri |
| **Ç3** | Çeyreklik Güncelleme | DOCX 8-12 sayfa | `references/c3-ceyreklik/c3-sablon.md` |
| **Ç4** | Çeyreklik Ön Bakış | DOCX 3-5 sayfa | `references/c4-on-bakis/c4-sablon.md` |

---

## İlker'in Yatırım Felsefesi — Quality Value

Tüm analizlerin çekirdeği bu framework'tür:

```
Ucuz + Hendekli = İdeal Yatırım ✅
Pahalı + Hendekli = Uzun vade (sabırla bekle)
Ucuz + Hendeksiz = Value trap ⚠️ (en tehlikeli)
Pahalı + Hendeksiz = Dokunma ❌
```

**6 Temel Prensip:**
1. **Hurdle Rate = Reel Enflasyon** — Benchmark BIST-100 değil, enflasyonu yenemeyen yatırım başarısızdır
2. **Multi-Strateji + Multi-Coğrafya** — TR, ABD, Avrupa + hisse, Bitcoin, altın. Korelasyon > çeşitlendirme
3. **Family Office Felsefesi** — Para kaybetmemek > para kazanmak. Capital preservation first
4. **Anlamak > Tahmin Etmek** — İşi anla, fiyatı tahmin etme
5. **Circle of Competence** — ROIC > WACC, brüt marj %60+, S/C > 1.50
6. **Contrarian Timing** — Kriz anlarında satmama disiplini

---

## Pipeline Yapısı — Task-Based Execution

Analiz tek bir monolitik süreç değil, bağımsız task'lardan oluşur. Her task prerequisite'lerini doğrular ve kendi deliverable'ını üretir. Bu yapı hata yakalamayı kolaylaştırır ve task'lar arası review noktaları sağlar.

### Task Haritası

| Task | İsim | Prerequisite | Deliverable |
|------|------|-------------|-------------|
| **T1** | Şirket Araştırması | Ticker/isim | Research document (min 6000 kelime) |
| **T2** | Finansal Modelleme | T1 veya finansal erişim | Finansal tablo analizi + senaryo varsayımları (projeksiyon T3/bbb-dcf'de) |
| **T3** | Değerleme | T2 (finansal model) | DCF + Comps + adil değer tahmini |
| **T4** | Grafik Üretimi | T1, T2, T3 | Chart paketi (PNG) |
| **T5** | Rapor/Tez Yazımı | T1, T2, T3 (T4 opsiyonel) | Yatırım tezi (blog/PDF/DOCX) |

### Execution Kuralları

- **Tek task per request** — tamamla, deliverable'ı sun, onay al, sonra sonraki task
- **Prerequisite verification sert** — T3'ü T2 olmadan başlatma, T5'i T3 olmadan başlatma
- **NO SHORTCUTS** — sadece belirtilen deliverable üretilir; "özet" veya "sonraki adımlar" dokümanı yok
- **Review noktaları** — her task sonrasında çıktı kontrol edilir, sonraki task'a geçmeden onay

İlker "full pipeline" isterse → T1'den başla, her adımda onay al, sırayla ilerle.

### 🔴 Dosyalama Kuralı (25 Mart 2026, İlker onaylı)

**TÜM çıktılar** `research/companies/{TICKER}/` altına yazılır. Klasör yapısı:
```
research/companies/{TICKER}/
├── README.md                          ← Ana profil (her şirkette olmalı)
├── kaynaklar/                         ← PDF'ler (kurum raporları, faaliyet raporları, sunumlar)
├── scripts/                           ← Python scriptleri (rapor assembly, chart gen, DCF excel gen)
├── charts/                            ← T4 üretilmiş grafikler
├── {TICKER}_research.md               ← T1 deliverable
├── {TICKER}_financial_analysis.md     ← T2 deliverable
├── {TICKER}_DATA_PACK.md              ← Faz 1 veri paketi
├── {TICKER}_VALUATION.md              ← T3 deliverable
├── {TICKER}_Rapor_YYYY-MM-DD.docx     ← T5 nihai rapor
├── {TICKER}_DCF_*.xlsx                ← DCF Excel modeli
└── arsiv/                             ← Eski versiyonlar, deprecated dosyalar
```
**Kurallar:**
- Root'ta `{TICKER}.md` OLMAZ. Her şey klasörün içinde.
- PDF'ler `kaynaklar/` altında — başka şirketin PDF'i bu klasörde OLMAZ.
- Python scriptleri `scripts/` altında (root'ta .py bırakma).
- `~$` temp dosyaları, `__pycache__/` git'e eklenmez.
- T1 başında klasör yoksa: `mkdir -p research/companies/{TICKER}` ile oluştur.

---

## T1: Şirket Araştırması (6000-8000 Kelime)

İlk kez coverage'a alınan şirket için kapsamlı araştırma dokümanı.

**Deliverable:** `research/companies/{TICKER}/{TICKER}_research.md` — **BAŞKA BİR ŞEY DEĞİL.**

**⚠️ KISITLAMA YAPMA:**
- ✅ 6.000-8.000 kelime TAM yaz (özet veya kısaltma değil)
- ✅ 3-4 yönetici × 300-400 kelime biyografi — HEPSİ eksiksiz
- ✅ 5-10 rakip detaylı analiz — her biri spesifik
- ✅ 8-12 risk, 4 kategoride — her biri 50-100 kelime
- ✅ 9 bölümün tamamı kelime hedeflerinde
- ❌ Bölüm atlama veya kısaltma YASAK
- ❌ "Tamamlama özeti", "sonraki adımlar" dokümanı üretme — SADECE research.md
- ❌ Kaynak etiketi olmadan rakam yazma — her rakamda (KAP, tarih) etiketi

→ **Per-bölüm kelime aralıkları, kaynak hiyerarşisi, input verification:** `references/c2-tam-kapsama/task1-arastirma.md`

### T1 Çıkış Gate'i (T2'ye Geçiş Şartı)

T1 deliverable'ını teslim etmeden ÖNCE bu 3 soruyu cevapla:
1. **SENTEZLEDİN Mİ?** Bu şirketin hikayesi 3 kelimeyle ne? (3 kelimeye indiremiyorsan yeterince sentez yapmamışsın)
2. **SORGULADIN MI?** T1'deki fırsat bölümü ile risk bölümü çelişiyor mu? Varsa çöz.
3. **NEDENSELLİK:** Şirketin en güçlü 2 varsayımı arasındaki nedensellik yönü ne? Yön tersine dönerse ne olur?

Cevaplar research.md'nin sonuna "## Sentez Notu" olarak eklenir.

### 🔴 T1 ZORUNLU KURAL: ONCE TOPLA, SONRA YAZ (2026-03-18)

> **research.md dosyasi yazilmadan once TUM kaynaklar toplanmis ve onaylanmis olmalidir.**
> Eksik kaynakla rapor yazilip sonra "yeniden yazayim" demek token israf eder.

**2 ASAMA:**
- **Asama 1 (Kaynak Toplama):** Checklist'i doldur, kaynaklari topla, oku. Eksikleri tespit et. Ilker'e "Kaynak Durumu Raporu" sun (erisilen + eksik liste). Eksikleri `research/companies/{TICKER}/` altina yuklemesini iste. Ilker cevap verene kadar research.md YAZMA.
- **Asama 2 (Rapor Yazimi):** Tum kaynaklar hazir oldugunda, hepsini birlikte degerlendirerek research.md'yi TEK SEFERDE yaz.

-> Detayli workflow: `references/c2-tam-kapsama/task1-arastirma.md` (Asama 1 Ciktisi formati dahil)

### T1 On Kontroller

1. **DONEM KONTROLU:** `bbb_financials.py {TICKER} --summary` calistir. "Son donem" ne? Tum kaynaklar bu doneme ait olmali. Eski donem sunum/raporunu birincil kaynak olarak KULLANMA.
2. **FINANSAL VERI:** Analiz tablolarindaki tum rakamlar `bbb_financials.py` (Is Yatirim, IAS 29 duzeltmeli) ile cekilir. `bbb_kap.py --kap-summary` sadece quick scan. KAP'ta enflasyon muhasebesi YOK.
3. **EN GUNCEL SUNUM:** Sirketin en son yatirimci sunumunu bul. Bulamazsan Ilker'den iste. Eski sunum = tarihsel referans, birincil kaynak DEGIL.
4. **KAP FINANSAL TABLOLAR PDF:** T2 icin zorunlu (dipnot dogrulama). T1'de de kaynak listesine dahil et: varsa topla, yoksa Ilker'den iste. Detay: Veri Kaynaklari Hiyerarsisi Katman 1b.
5. **KURUM RAPORU TARIHI:** Her raporun tarihini belirle. Belirsizse Paratic/RotaBorsa ile cross-check. En gunceli birincil.
6. **YAZIM:** (a) Tüm çıktılar Türkçe karakterlerle yazılmalıdır: ş, ğ, ü, ö, ç, ı, İ. ASCII Türkçe (s yerine ş, g yerine ğ vb. kullanmamak) YASAK. (b) Emdash (—), uzun tire, fancy unicode karakterler YASAK. Düz tire (-) kullan. (c) İngilizce konsept terimler yerine Türkçe karşılıkları kullan (bkz. `references/c2-tam-kapsama/task1-arastirma.md` §Dil ve Terminoloji Kuralları). Sektörde yerleşmiş kısaltmalar (FAVÖK, ROIC, DCF, F/K) kalabilir.
7. **DRIVE ERISIM:** Warm cache (`cat > /dev/null` + `sleep 30`) dene. Basarisizsa Ilker'den dosyayi `research/companies/{TICKER}/` altina yuklemesini iste.
8. **KAP BİLDİRİM TARAMA + SEÇİCİ ARŞİVLEME (§3A - ZORUNLU):** İLK ADIM olarak `bbb_kap.py {TICKER} --all --last 6m` ile tüm bildirimleri listele. Sonra **KAP Bildirim Seçim Protokolü** (v4.4) uygula: ADIM A (otomatik indir: FR, analist sunumu, temettü, yönetim değişikliği), ADIM B (otomatik atla: devre kesici, boilerplate uyum raporları), ADIM C (koşullu değerlendir: aylık operasyonel veri kapsam boşluğu, DG ardışıklık kontrolü, cross-company iş ilişkileri). Seçili bildirimleri `--archive --ids X,Y,Z` ile indir. Kör toplu arşivleme (`--archive` idsiz) KULLANILMAMALI. Detay: `references/c2-tam-kapsama/task1-arastirma.md` §3A-0. **Bu adım ATLANAMAZ** — Aşama 1 Kaynak Durumu Raporu'nda §3A tablosu (6 satır, KAP bildirimleri dahil) olmadan Aşama 2'ye geçilemez.

### Veri Kaynakları Hiyerarşisi

| Öncelik | Kaynak | Ne Alınır | Araç |
|---------|--------|-----------|------|
| 1 | **KAP (BBB Finans)** | Finansal tablolar (147+ kalem), özet, şirket bilgisi | `bbb_kap.py`, `bbb_financials.py` |
| 1b | **KAP Finansal Tablolar PDF** | Dipnotlar: efektif faiz, vergi teşviki, gider kırılımı, döviz pozisyonu, tek seferlik kalemler | pdftotext / PyMuPDF (bkz. §PDF Okuma) |
| 2 | **Şirket IR sayfası** | Yatırımcı sunumları, faaliyet raporları, stratejik hedefler | `web_fetch` (HTML) / `summarize` (PDF) |
| 3 | **Şirket web sitesi** | Ürün/hizmet detayı, yönetim, tarihçe | `web_fetch` |
| 4 | **KAP faaliyet raporu** | Segment gelirler, yönetim rehberliği, risk faktörleri | pdftotext / PyMuPDF (bkz. §PDF Okuma) |
| 5 | **Kurum raporları (Drive)** | Analist görüşleri, adil değer tahminleri, konsensüs | GDrive + pdftotext — aşağıdaki §Kurum Raporları bölümüne bak |
| 6 | **Kurum raporları (Web)** | Online yayınlanan analist raporları | `summarize "{URL}" --extract` |
| 7 | **Sektör kuruluşları** | Pazar verileri, istatistikler | TAPDK, BTK, BDDK, OSD, EPDK, TÇD |
| 8 | **Damodaran** | ERP, Beta, CRP, sektör ortalamaları | `web_fetch` → Damodaran |
| 9 | **Web araştırma** | Haberler, rekabet bilgisi | `web_search` |

⚠️ **Asla birincil kaynak olmaz:** StockAnalysis, TradingView, Investing.com, GuruFocus — sadece cross-check.

**Katman 1 vs 1b Ayrımı:** İş Yatırım (bbb_financials.py) 147 kalemin TUTARINI verir. KAP Finansal Tablolar PDF ise bu tutarların arkasındaki DİPNOTLARI verir. Ikisi birlikte kullanılır:
- **T1:** İş Yatırım yeterli (özet kart, çarpanlar, tarihsel tablolar)
- **T2:** İş Yatırım + KAP Finansal Tablolar PDF zorunlu (Adım 3G: dipnot doğrulama)
- **T3 (bbb-dcf):** T2 handoff verisi yeterli (dipnotlar T2'de işlenmiş olmalı)

**Dosya konumu:** `research/companies/{TICKER}/{TICKER} {Dönem} Finansal Tablolar.pdf`
**Yoksa:** İlker'den iste, `research/companies/{TICKER}/` altına kaydetmesini söyle.

---

### PDF Okuma — `summarize` CLI

`web_fetch` binary PDF'leri parse edemez. `summarize --extract` yerel PDF dosyalarini desteklemiyor (sadece URL ve medya dosyalari). Yerel PDF okuma icin asagidaki 3 katmanli protokolu kullan.

### 3 Katmanli PDF Okuma Protokolu

Yatirimci sunumlari ve faaliyet raporlari genelde karisik icerik barindirir: bazi sayfalar metin/tablo agirlikli (pdftotext iyi calisir), bazi sayfalar grafik/chart agirlikli (pdftotext sadece etiketleri alir, asil rakamlar gorsel icinde kalir). Bu yuzden tek arac yetmez.

**Katman 1 - pdftotext (Metin + Tablo Cikarma):**
```python
import subprocess
subprocess.run(['pdftotext', pdf_path, output_txt_path])
```
Veya PyMuPDF ile:
```python
import fitz
doc = fitz.open(pdf_path)
for page in doc:
    text = page.get_text()
```
Finansal tablolar, bilanco, nakit akis tablolari, yonetim mesajlari - bunlar iyi cikiyor.

**Katman 2 - Gorsel Agirlik Tespiti (PyMuPDF):**
```python
import fitz
doc = fitz.open(pdf_path)
image_heavy_pages = []
for i, page in enumerate(doc):
    text = page.get_text().strip()
    img_count = len(page.get_images())
    if len(text) < 200 and img_count > 0:
        image_heavy_pages.append(i)
    elif img_count > 10:  # Cok gorsel = muhtemelen chart/infografik
        image_heavy_pages.append(i)
```
Kriter: <200 karakter metin + gorsel var VEYA >10 gorsel = grafik agirlikli sayfa.

**Katman 3 - Vision ile Grafik Okuma (image tool):**
Gorsel agirlikli sayfalar PNG'ye render edilir ve `image` tool'a verilir:
```python
import fitz, os
doc = fitz.open(pdf_path)
outdir = "/Users/ilkerbasaran/.openclaw/workspace-kaya/temp"
os.makedirs(outdir, exist_ok=True)
for page_num in image_heavy_pages:
    page = doc[page_num]
    pix = page.get_pixmap(dpi=150)
    pix.save(f"{outdir}/{ticker}_p{page_num+1}.png")
```
Sonra `image` tool ile:
- "Bu sayfadaki tum sayisal verileri cikar" promptu
- Batch olarak max 4-5 sayfa birden gonderilebilir

**⚠️ ONEMLI KURALLAR:**
- image tool sadece workspace altindaki dosyalari kabul eder (`/tmp/` CALISMAZ). `workspace-kaya/temp/` klasorunu kullan.
- PNG'leri is bittikten sonra sil (disk temizligi).
- Sunum PDF'lerinde genelde finansal tablo sayfalari (gelir tablosu, bilanco, nakit akis) metin olarak cikiyor. Grafik sayfalari ise pazar payi, magaza buyumesi, demografik veriler gibi icerik barindiriyor.
- Her iki katmandan gelen veriyi birlestir - pdftotext ciktisi + vision ciktisi = tam resim.

**Kullanim senaryolari:**

| Senaryo | Yontem |
|---------|--------|
| Yerel PDF (faaliyet raporu, sunum) | Katman 1 (pdftotext) + Katman 2-3 (grafik sayfalar) |
| Online kurum raporu PDF | `summarize "https://kurum.com/rapor.pdf" --extract` |
| Drive'daki kurum raporu | Warm cache + `summarize` VEYA dosyayi workspace'e kopyala + Katman 1-3 |
| KAP faaliyet raporu | Ilker'den dosya iste -> workspace'e kaydet -> Katman 1-3 |

**⚠️ Timeout:** Buyuk PDF'ler (>50 sayfa) icin pdftotext/PyMuPDF tercih edilir (saniyeler icerisinde calisir). `summarize` URL'ler icin hala gecerli.

---

### Kurum Raporları — Google Drive Erişimi

**Konum:**
```
/Users/ilkerbasaran/Library/CloudStorage/GoogleDrive-ilker@borsadabibasina.com/
Drive'ım/Drive'ım/borsadabibasina.com/#5 - Kurum Raporları/
```

**Dosya isimlendirme:** `{Kurum} - {TICKER} {Dönem}.pdf` (örn. `Pusula Yatırım - EBEBK 4Ç25.pdf`)

**Arama:**
```bash
DRIVE_KURUM="/Users/ilkerbasaran/Library/CloudStorage/GoogleDrive-ilker@borsadabibasina.com/Drive'ım/Drive'ım/borsadabibasina.com/#5 - Kurum Raporları"
find "$DRIVE_KURUM" -iname "*{TICKER}*" 2>/dev/null
```

**⚠️ GDrive Warm Cache Sorunu:**
Google Drive dosyaları bazen ilk erişimde timeout alır (dosya henüz yerel cache'e indirilmemiş). Çözüm:
```bash
# 1. Dosyayı warm cache yap (ilk okuma — başarısız olabilir, NORMAL)
cat "$DRIVE_KURUM/{Kurum} - {TICKER}.pdf" > /dev/null 2>&1

# 2. 30 saniye bekle (Drive'ın dosyayı indirmesi için)
sleep 30

# 3. Tekrar oku — şimdi çalışmalı
summarize "$DRIVE_KURUM/{Kurum} - {TICKER}.pdf" --extract-only > /tmp/{TICKER}_kurum.txt
```

Hâlâ başarısız olursa → dosya henüz Drive'a sync olmamış olabilir. İlker'den kontrol istemek için: "Bu dosya Drive'da var ama erişemiyorum, sync durumunu kontrol edebilir misin?"

---

### KAP Faaliyet Raporu Erişimi

⚠️ **v4.4 Protokolü:** Kör toplu arşivleme (`--archive` idsiz) önerilmiyor. Aşağıdaki iki aşamalı akıllı arşivleme kullanılmalı:

```bash
cd ~/.openclaw/workspace/skills/bbb-finans/scripts
# 1. Tüm bildirimleri listele (indirmeden)
python3 bbb_kap.py {TICKER} --all --last 6m
# 2. KAP Bildirim Seçim Protokolü uygula (bkz. task1-arastirma.md §3A-0)
# 3. Sadece seçili bildirimleri indir
python3 bbb_kap.py {TICKER} --archive --ids <seçili_id'ler> --last 6m
# Hedef: ~/.openclaw/workspace-kaya/research/companies/{TICKER}/kap_docs/
```

Arşivleme sonrası dosyalar `kap_docs/` altındadır. Eğer arşivde bulunamazsa:
1. **Drive'da ara:** Bazı faaliyet raporları kurum raporları klasöründe olabilir
2. **İlker'den iste:** "EBEBK 2025 faaliyet raporunu research/companies/EBEBK/ altına kaydedebilir misin?"
3. **Web'den ara:** `web_search "{TICKER} faaliyet raporu {yıl} pdf"` → `summarize` ile oku

Faaliyet raporunun verdiği benzersiz veriler (başka kaynaklarda YOK):
- Segment gelir kırılımı (coğrafi + ürün)
- Yönetim rehberliği (guidance)
- İlişkili taraf işlemleri
- Risk faktörleri detayı
- Çalışan sayısı + lokasyon bilgisi

### Doküman Yapısı — 9 Bölüm

**Toplam hedef: 6.000-8.000 kelime.** Per-bölüm kelime aralıkları → `references/c2-tam-kapsama/task1-arastirma.md`

| # | Bölüm | Kelime | Özet |
|---|-------|--------|------|
| 1 | Yönetici Özeti | 400-600 | Şirket nedir, neden ilgi çekici, tez draft |
| 2 | Şirket Profili | 500-800 | Tarihçe, ölçek, iş modeli, çalışanlar |
| 3 | Ürün/Hizmet Portföyü | 500-700 | Ürünler, gelir segmentasyonu, fiyatlama |
| 4 | Yönetim Analizi | 500-700 | CEO/CFO/kilit yöneticiler, ortaklık, scorecard |
| 5 | Sektör Analizi | 1.000-1.400 | TAM/SAM, Porter, düzenleyici ortam |
| 6 | Moat Analizi | 600-900 | 4 hendek türü, güç (0-10), barometresi |
| 7 | Finansal Derinlemesine | 1.000-1.400 | 5Y trend, 6 metrik, ROIC dinamikleri |
| 8 | Rekabet Pozisyonlaması | 500-700 | Pazar payı, rakip tablosu (min 4-5) |
| 9 | Riskler ve Fırsatlar | 400-600 | Top 5 risk, top 5 fırsat, kill criteria (min 2) |
| | **TOPLAM** | **~6.000-8.000** | |

→ Sektör analizi detayları: `references/sektor/sektor-analiz-sablonu.md`
→ Düzenleyici tarama: `references/ortak/duzenleyici-ortam-taramasi.md`
→ BIST sektör metrikleri: `references/ortak/bist-sektor-metrikleri.md`

---

## T2: Finansal Modelleme

→ **Tam workflow, BIST/KAP kalem sıralama, TTM/IC/S/C hesaplama, senaryo framework, IAS 29 kontrol:** `references/c2-tam-kapsama/task2-finansal-modelleme.md`

T2 ve bbb-dcf arasında net görev ayrımı: T2 = veri toplama + tarihsel analiz + senaryo varsayımları hazırlama. bbb-dcf = WACC + 10Y projeksiyon + terminal value + değerleme. T2 tamamlandığında bbb-dcf Faz 1 DATA_PACK'in finansal veri bölümü hazır olmalı.

**Deliverable:** `research/companies/{TICKER}/{TICKER}_financial_analysis.md` + `{TICKER}_model.xlsx` — **BAŞKA BİR ŞEY DEĞİL.**

**⚠️ KISITLAMA YAPMA:**
- ✅ 3-5 yıl tarihsel veri KAP/BBB Finans'tan eksiksiz çek
- ✅ 6 Excel tab'ın TAMAMINI oluştur (Gelir, GelirTablosu, NakitAkis, Bilanco, Senaryolar, WACC)
- ✅ Gelir modeli: ürün segmentasyonu (5-15 satır) + coğrafi kırılım (2-10 satır)
- ✅ 3 senaryo (Kötümser/Baz/İyimser) her biri spesifik parametrelerle
- ✅ TTM hesaplaması kümülatif formülle
- ✅ Guidance vs Varsayım Karşılaştırma tablosu zorunlu
- ❌ Tab atlama, basitleştirilmiş model üretme YASAK
- ❌ "Model özeti", "tamamlama notu" üretme — SADECE md + xlsx
- ❌ IAS 29 kontrolünü atlama (Türk şirketleri)

---

### T2 Çıkış Gate'i (T3'e Geçiş Şartı)

T2 deliverable'ını teslim etmeden ÖNCE:
1. **VARSAYIM ZİNCİRİ:** Makro → Sektör → Şirket varsayımlarını tek satır yaz. Zincir tutarlı mı?
2. **YARATICI ZORLAMA:** "Bu şirketin en büyük rakibi 5 yıl sonra bugün var olmayan bir şirket olabilir mi?" ve "Bu iş modeli tamamen farklı bir coğrafyada çalışır mı?" Cevapları financial_analysis.md'ye not et.
3. **GUIDANCE REKONSİLASYONU (IAS 29):** §6A Guidance tablosundaki birimler DCF yaklaşımıyla tutarlı mı? Reel↔Nominal çevirisi yapıldı mı? Sapma yönü ve gerekçesi yazıldı mı? (Detay: task2 §6A)

---

## T3: Değerleme

### T3 Ön Kontrol: Çelişki Matrisi (ZORUNLU — Parametreler Kilitlenmeden ÖNCE)

T3'e başlamadan ÖNCE, T2'deki varsayımlar ve T1'deki riskler arasındaki çelişkileri tespit et.
Bu matris bbb-dcf Faz 1.5 parametre kilidiyle birlikte çalışır: çelişkiler çözülmeden parametreler KİLİTLENMEZ.

**Adım 1:** T1 research.md §9'dan ilk 5 riski, T2 financial_analysis.md'den 5 kilit varsayımı (terminal büyüme, FAVÖK marjı, hasılat YBBO, CapEx/Hasılat, terminal ROC) al.

**Adım 2:** Çelişki Matrisi'ni doldur:

```
ÇELİŞKİ MATRİSİ (T3 Ön Kontrol)
===================================
         | T1 Risk 1  | T1 Risk 2  | T1 Risk 3  | T1 Risk 4  | T1 Risk 5  |
---------|------------|------------|------------|------------|------------|
Varsayım 1: Terminal büyüme %X | ?  | ?  | ?  | ?  | ?  |
Varsayım 2: FAVÖK marjı %Y     | ?  | ?  | ?  | ?  | ?  |
Varsayım 3: Hasılat YBBO %Z    | ?  | ?  | ?  | ?  | ?  |
Varsayım 4: CapEx/Hasılat %W   | ?  | ?  | ?  | ?  | ?  |
Varsayım 5: Terminal ROC %V    | ?  | ?  | ?  | ?  | ?  |
```

Her hücrede: ✓ (tutarlı) veya ✗ (çelişki).

**Adım 3:** Her ✗ hücresi için:
1. Çelişkinin doğası (1-2 cümle)
2. Çözüm: (a) varsayımı revize et, (b) hafifletici faktörü açıkla, (c) senaryo ayrımında yönet
3. Çözüm raporda nerede yer alacak? (T5'in Faz 0'ında bölüm eşlemesi yapılacak)

**⛔ GATE:** En az 2 çelişki tespit edilip çözülmeden bbb-dcf Faz 1.5'e (parametre kilidi) GEÇİLMEZ.
Sıfır çelişki = varsayımlar yeterince sorgulanmamış demektir.

**Adım 4:** Matrisi `research/companies/{TICKER}/{TICKER}_celiski_matrisi.md` dosyasına yaz.
T5 Faz 0 bu dosyayı okuyarak çözümleri rapor bölümlerine eşleyecek.

**Deliverable:** `research/companies/{TICKER}/{TICKER}_celiski_matrisi.md` (T3 Ön Kontrol) + bbb-dcf Faz 3 çıktısı + `research/valuations/{TICKER}_DCF_{YYYY-MM-DD}.md` + `{TICKER}_valuation_comps.md` — **BAŞKA BİR ŞEY DEĞİL.**

**⚠️ KISITLAMA YAPMA:**
- ✅ bbb-dcf Faz 0→3 protokolü EKSIKSIZ uygula — tek session'da veri+değerleme YASAK
- ✅ İNA (DCF) + Comps + Forward FD/FAVÖK — ÜÇÜ de yapılacak
- ✅ Comps tablosu: min 4-5 peer, istatistiksel özet (Maks/75./Medyan/25./Min)
- ✅ Sensitivity matrisi: 7×5 grid, 50bp adım, baz durum merkez hücre
- ✅ 4 sanity check (implied ROIC, ters İNA, Gordon PD/DD, EV/IC)
- ✅ Fisher parity cross-check (TL DCF varsa)
- ❌ Sadece DCF yapıp "tamamlandı" demek YASAK — Comps ve Forward F/K de zorunlu
- ❌ "Değerleme özeti" dokümanı üretme — deliverable listesindekiler dışında çıktı yok
- ❌ Checklist okumadan faz kapatma (EBEBK, NTHOL, NVO dersi)

### Moat (Hendek) Analizi

| Moat Türü | Tanım | Örnekler | Test |
|-----------|-------|----------|------|
| Yüksek Giriş Bariyeri | Sermaye, zaman, lisans | ÇİMSA, TAV | Min yatırım, lisans süreci |
| Değiştirme Maliyeti | Müşteri geçiş zorluğu | SAP, Bankacılık | Geçiş süresi + maliyeti |
| Pazar Yapısı | Duopol/Monopol | AEFES+TBORG | HHI, Top 2-3 payı |
| Münhasır Varlıklar | IP, patent, data | NVO, GENI | Patent süresi, veri derinliği |

**Moat Barometresi:** Terminal ROIC vs WACC = moat'ın financial kanıtı.
- ROIC >> WACC → Güçlü moat (Pop Mart: %30 vs %7,21)
- ROIC ≈ WACC → Moat yok (DOCO: ROIC ≈ WACC)
- ROIC < WACC → Değer yıkımı

### Finansal Analiz — İlker'in 6 Metriği (ZORUNLU)

| Metrik | İyi | Mükemmel | Red Flag | Veto? |
|--------|-----|----------|----------|-------|
| ROIC | >15% | >25% | <10% | Evet |
| FCF Marjı | >10% | >20% | Negatif | Evet |
| Gross Margin | >30% | >50% | <15% | — |
| Net Borç/FAVÖK | <2x | <1x | >4x | — |
| Ciro Büyümesi | >5% reel | >15% reel | Negatif (3Y+) | — |
| ROE | >15% | >25% | <10% | — |

"Veto" metrikleri red flag'daysa → şirket quality filtreden geçemez, diğer metrikler ne olursa olsun.

### Çift Değerleme (ZORUNLU)

| Yöntem | Araç | Ne Zaman |
|--------|------|----------|
| **Göreceli (Karşılaştırmalı)** | → `references/c2-tam-kapsama/karsilastirmali-degerleme.md` | Her zaman |
| **İçsel (İNA/DCF)** | → bbb-dcf skill (Faz 0→3) | Her zaman |
| **İleriye Dönük F/K** | → `references/c2-tam-kapsama/task3-hedef-fiyat.md` | Kârlı şirketler |
| **NAV/Parçaların Toplamı** | → bbb-dcf special_cases.md | Holdingler |
| **Artık Gelir** | Manuel | Bankalar |

**Adil Değer Derivasyonu:** İNA + Comps + Forward F/K ağırlıklı reconciliation → `references/c2-tam-kapsama/task3-hedef-fiyat.md`
Göreceli ve İNA sonuçları %20'den fazla farklıysa → varsayımları sorgula, farkın nedenini açıkla.

**Forward HBK Parametrik Hesaplama (v2.1):** `Forward_HBK = (Kalan_Ay/12) × Cari_FY_HBK + (Geçen_Ay/12) × Sonraki_FY_HBK`. IAS 29 şirketlerinde parasal kazanç/kayıp düzeltmesi zorunlu. Detay: `task3-hedef-fiyat.md` §Yöntem 2.

> Curtis Jensen: "DCF is like Hubble telescope – turn a fraction of an inch & you're in a different galaxy."

### Risk Değerlendirmesi — İyimser + Kötümser Dengeli

| Senaryo | Olasılık | İçerik |
|---------|----------|--------|
| Kötümser | %20-30 | En kötü durum — neler ters gidebilir? |
| Base | %40-60 | Normal gidişat — en olası senaryo |
| İyimser | %20-30 | En iyi durum — neler iyi gidebilir? |

→ Detaylı skorlama sistemi: `references/ortak/skorlama-sistemi.md` (Quality Value v2.0 -- teknik analiz icermez)
→ Cikti formatlari: `references/ortak/cikti-sablonlari.md`

### T3 Kapatma Checklist'i (ZORUNLU -- T4'e Gecis Sarti)

T3 "tamamlandi" etiketini almadan once su 4 satir dogrulanmali:

- [ ] INA (DCF) sonucu var mi? (bbb-dcf Faz 0-3 tamamlandi, Excel uretildi)
- [ ] Comps tablosu var mi? (karsilastirmali-degerleme.md'ye gore, min 4-5 peer)
- [ ] Forward F/K hesabi var mi? (task3-hedef-fiyat.md'ye gore)
- [ ] Reconciliation yapildi mi? (3 yontem agirlikli ortalama + fark analizi)
- [ ] thesis_scorecard.md dolduruldu mu? (research/companies/{TICKER}/thesis_scorecard.md — şablon: research/companies/_THESIS_SCORECARD_TEMPLATE.md)

**5'i de isaretlenmeden T4'e GECILMEZ.**

> Kok neden (EBEBK, 18 Mart 2026): DCF toolkit gelistirme heyecaniyla Comps ve Forward F/K atlandi.
> NTHOL (11 Subat), NVO (Subat), EBEBK (18 Mart) -- ayni pattern: checklist okumadan faz kapatma.

---

## 🔴 ONCE KARAR, SONRA MAKALE

1. **Araştırmayı tamamla** — T1-T3 hepsi bitmiş olmalı
2. **Kaya bağımsız verdict sunar:** TUT / EKLE / AZALT / ÇIK + gerekçe + conviction (%)
3. **İlker ile tartışma** — karşıt argümanlar, eksik noktalar
4. **Karara varılır** — İlker'in final kararı
5. **Karar makaleye yansıtılır** — makale İlker'in kamuya açık pozisyonudur

Bu sıra **ATLANAMAZ**. Premium makale yazımı: `copywriter` skill → core-dna.md + premium-dna.md.

---

## Model Güncelleme

Bilanço geldi ama rapor henüz yazılmayacak — sadece modeli güncelle, estimate revision yap, değerleme etkisini hesapla.

→ **Tam workflow:** `references/model-guncelleme/model-guncelleme.md`

**Tetikleyici örnekler:** "modeli güncelle", "bilançoyu modele yansıt", "estimate revision yap", "WACC güncelle"
**Ç3'ten farkı:** Çıktı dahili MD notu (DOCX değil). Ç3 hazırlanacaksa bu workflow önce tamamlanır, sonra Ç3 şablonuna geçilir.

---

## Çeyreklik Güncelleme

Mevcut kapsama şirketleri için çeyreklik güncelleme — "ne DEĞİŞTİ?" sorusuna cevap verir.

→ **Tam rehber:** `references/c3-ceyreklik/ceyreklik-guncelleme.md`

**Zorunlu bileşenler:**
1. **Beklenti/Gerçekleşme tablosu** — Metrik | Beklenti | Gerçekleşme | Fark | Not
2. **Bu Çeyrekte Ne Değişti?** — sadece yeni bilgi, arka plan tekrarlanmaz
3. **Tahmin revizyonu** — Eski Tahmin | Yeni Tahmin | Değişim | Neden
4. **Tez etkisi** — tez takip kartı güncelleme, conviction değişimi
5. **Önceki yazılara referans** — İlker'in kendi sözlerinden alıntı (ZORUNLU)

**Çeyreklik Ön Bakış (sonuç öncesi):** Sonuçlar açıklanmadan önce hazırlık notu. Drive kurum raporlarından konsensüs çıkar, 3-5 kritik metrik seç, İyimser/Baz/Kötümser senaryo çerçevesi kur.
→ **Detaylı workflow (5 adım):** `references/c3-ceyreklik/ceyreklik-guncelleme.md §15`

**Rapor Sayfa 1 Formatı:** ■ bullet yapısı (kalın başlık + sayıyla başlayan açıklama), özet kutu (tarih/fiyat/hedef/tavsiye/PD/FD), "Güçlü Pozitif / Sınırlı Pozitif / Nötr / Olumsuz" değerlendirme notu.
→ **Tam şablon:** `references/c3-ceyreklik/ceyreklik-guncelleme.md §16`

**Tahmin Güncelleme ("Ne Değişti"):** Yeni veri sonrası tahmin revizyonu: Önceki | Gerçekleşme | Fark | Sinyal vs Gürültü ayrımı.

---

## Tez Takibi — Yatırım Tezi İzleme

→ **Tam template:** `references/tez-takip/tez-takip-sablonu.md`

**Dosya:** `research/companies/{TICKER}/thesis_scorecard.md`

**Zorunlu:** Tez ayağı takibi, çıkış kriterleri, çürütücü kanıt kaydı, conviction seviyesi, katalist takvimi.

**Coverage Universe Katalist Takvimi:** 10+ hisseyi tek tabloda yönetmek için. Yerli + yabancı ayrı. Etki H/O/D. Dosya: `research/coverage_calendar.md`.
→ **Takvim şablonu ve güncelleme disiplini:** `references/tez-takip/tez-takip-sablonu.md §5`

> "A thesis should be falsifiable — if nothing could disprove it, it's not a thesis."

---

## Karşılaştırmalı Değerleme (Emsal Şirketler)

→ **Tam rehber:** `references/c2-tam-kapsama/karsilastirmali-degerleme.md`

**Özet:** Min 4-5 emsal | 5+5 metrik | İstatistiksel özet (Maks/75./Medyan/25./Min) | IAS 29 kuralı: spot kurla çevirme YASAK | Hedef şirket konumlandırması.

---

## Sektör Analizi & Fikir Üretimi

→ Sektör şablonu: `references/sektor/sektor-analiz-sablonu.md`
→ BIST sektör metrikleri: `references/ortak/bist-sektor-metrikleri.md`
→ Rekabet analizi rehberi: `references/ortak/rekabet-analizi-rehberi.md`
→ Sistematik tarama: `references/c1-fikir-uretimi/fikir-uretimi.md`

**5 Tarama türü:** Kalite Değer | Derin Değer | Büyüme | Toparlanma | Temettü
**Tematik tarama:** Tema → Değer zinciri → "Fiyatlanmış mı?" → İkinci derece faydalananlar

---

## T4: Grafik Üretimi (25-35 Chart)

**Deliverable:** `research/companies/{TICKER}/charts/` altında 25-35 PNG dosyası — **BAŞKA BİR ŞEY DEĞİL.**

**⚠️ KISITLAMA YAPMA:**
- ✅ Minimum 25 grafik üret (10-15 ile yetinme)
- ✅ 4 zorunlu grafik MUTLAKA olmalı: G03 ⭐, G04 ⭐, G28 ⭐, G32 ⭐
- ✅ 300 DPI (baskı kalitesi) — düşük çözünürlük kabul edilmez
- ✅ BBB renk paleti + Türkçe başlıklar + kaynak notu
- ✅ T1/T2/T3 input doğrulaması — eksik task varsa BAŞLAMA
- ❌ Placeholder grafik ("burada grafik olacak") YASAK
- ❌ "Grafik listesi" veya "tamamlama notu" üretme — SADECE PNG dosyaları
- ❌ 4 zorunlu grafikten herhangi birini atlama

→ **Chart kataloğu + Python kodu:** `references/c2-tam-kapsama/task4-grafik-uretim.md`

### 4 Zorunlu Grafik (tam tezde olmazsa olmaz)
1. **G03** — Hasılat Segment Kırılımı (Yığılmış Alan) ⭐
2. **G04** — Hasılat Coğrafi Kırılım (Yığılmış Çubuk) ⭐
3. **G28** — İNA Duyarlılık Isı Haritası ⭐
4. **G32** — Değerleme Aralık Grafiği (Football Field) ⭐

### Grafik Standardı
| Çıktı Türü | Minimum Grafik | DPI |
|-------------|---------------|-----|
| Tam yatırım tezi (ilk kez kapsama) | 25 | 300 |
| Çeyreklik güncelleme | 8 | 150-300 |
| Sektör raporu | 12 | 150-300 |
| Hızlı analiz | 2 | 150 |

**Stil:** BBB turuncu (#f7931a birincil), minimalist, Türkçe başlık + kaynak notu, hedef şirket vurgulu. Renk paleti detayı: `rapor-sablonu.md`.
**Başlık kuralı:** İçgörü başlığı → "Brüt marj 5 yılda 800bp genişledi" (doğru), "Brüt Marj Grafiği" (yanlış).

---

## BBB Research Analitik Felsefesi

BBB Research'ün düşünce süreci SOUL.md'deki **Topla → Sentezle → Sorgula → Güncelle** mimarisini takip eder. Her raporda 4 şeyi garanti eder:

1. **Bağımsız düşünce** — Piyasadan etkilenmeden, elimizdeki verileri sentezleriz. Sonuç piyasayla aynı yere çıkabilir - bu da bir sonuç. Konsensüsle örtüşme/ayrışma noktalarını kanıtlarla ortaya koyarız; zorla contrarian olmayız.

2. **Sentez** — Veri toplamak kolay, listelemek kolay. Zor olan: parçalardan bütünü görmek. Her şirketin "3 kelimelik hikayesi"ni çıkarmak ve bu hikayenin değerleme varsayımlarıyla uyumlu olup olmadığını sorgulamak zorunludur.

3. **Kantitatif disiplin** — Her iddia bir rakamla, her rakam bir kaynakla desteklenir. "Güçlü büyüme" değil, "%34 YoY hasılat artışı (sektör ort. %18)" yazılır. İçgörü Merdiveni (yazi-kalitesi-rehberi.md) bu sentez refleksinin yazılı çıktısıdır; minimum Seviye 3 (İçgörü) zorunludur.

4. **Entelektüel dürüstlük** — Ne bildiğimizi, ne bilmediğimizi ve neyin bizi yanıltabileceğini açıkça söyleriz. Belirsizlikler gizlenmez, varsayımların kırılganlığı belirtilir.

---

## T5: Profesyonel Rapor Yazımı (DOCX)

**Deliverable:** `{TICKER}_Rapor_{YYYY-MM-DD}.docx` — **BAŞKA BİR ŞEY DEĞİL.**

**T5 Sentez Protokolü:** T5, T1-T4'un mekanik birleşimi DEĞİLDİR. T5, tüm fazlardaki bulguların tek bir analitik anlatı altında SENTEZLENMESİDİR. T1 olgusal içeriği korunur; T1 analitik içeriği "Dereceli Aktarım" prensibiyle aktarılır (ilk geçiş tam, sonraki referans + yeni açı). Her analitik bölüme "Analitik Köprü" eklenir. **First-Mention-Full** kuralı geçerlidir: aynı veri noktasının tam açıklaması raporda MAX 2 kez geçer.

→ **⚠️ T5 ASSEMBLY PROTOKOLÜ (ZORUNLU OKU):** `references/c2-tam-kapsama/task5-rapor-montaj.md` — Faz 0 (Argüman İnşası) + Faz A-H, hard stop gate'ler
→ **Faz 0 (KRİTİK — ATLANMAZ):** Assembly başlamadan önce 5 adım: (1) T3 Çelişki Matrisi'ni oku (`{TICKER}_celiski_matrisi.md`) ve çözümleri rapor bölümlerine eşle (2) Ana Argüman: 3 paragraf testi (tez+kanıt+karşı-tez) (3) Argüman Dalları: 3-5 tez dalı + 2 karşı-tez dalı, her bölüm bir dala bağlı (4) Piyasa Karşılaştırması (5) Tekrar Haritası. → Bu çıktılar raporun düşünce omurgasını kurar; Faz A-H bu omurganın fiziksel ifadesidir.
→ **Rapor fiziksel yapısı (sayfa layout, chart embed haritası):** `references/c2-tam-kapsama/rapor-sablonu.md`
→ **DOCX standart ve yapısı:** `references/c2-tam-kapsama/profesyonel-cikti-rehberi.md`
→ **Yazım kalitesi standardı (T5 başlamadan ZORUNLU OKU):** `references/ortak/yazi-kalitesi-rehberi.md` — İçgörü merdiveni Seviye 3+, consensus farkı çerçevesi, argüman inşası, iyimser/kötümser denge
→ **İlker yazım DNA'sı:** copywriter skill (core-dna.md + premium-dna.md)

### ⚠️ T5 Mimari Kuralı (KRİTİK)

```
ANA AGENT icerigi YAZAR → rapor-uret.py FORMATLAR → DOCX cikar
```

- **Ana agent** T5'i kendisi yapar — subagent'a devretmez
- **Ana agent** source dosyaları (T1/T2/T3) okur, yeni içeriği (projeksiyon, senaryo) YAZAR
- **rapor-uret.py** import edilir, layout/format/embed işini yapar
- **Detay:** `references/c2-tam-kapsama/task5-rapor-montaj.md`

### DOCX Minimum Standartlar (Tam Tez)
| Kriter | Minimum |
|--------|---------|
| Sayfa | 30 |
| Kelime | 10.000 |
| Gömülü chart | 25 |
| Tablo | 12 |

### NO SHORTCUTS Politikası
- ✅ **Tam yaz** — "Bu bölümde X ele alınacaktır" DEĞİL, gerçek içerik
- ✅ **Gerçek grafik göm** — "Burada grafik olacak" DEĞİL, gerçek PNG embed
- ✅ **Veri çıkar ve göm** — "Model'e bakınız" DEĞİL, tabloyu çıkar
- ❌ Bölüm atlama, kısaltma, token tasarrufu YASAK

### Word → Web Akışı
İlker'in akışı: Word'de yaz/review → Web sitesine yükle. Font ve stil web CSS'inden devralınır.

---

## Çıktı Formatları & Minimum Standartlar

### Deliverable Standards

| Çıktı Türü | Min Kelime | Min Tablo | Min Grafik | Min Kaynak | Format | Şablon |
|-------------|-----------|-----------|-----------|-----------|--------|--------|
| **Ç1 Fikir Üretimi** | 800 | 2 | — | 3 | Markdown | `c1-sablon.md` + `fikir-uretimi.md` |
| **Ç2 Tam Kapsama** (T5) | 10.000 | 12 | 25 | 15 | DOCX 30+ sayfa | Bu dosya §T5 + `task5-rapor-montaj.md` + `rapor-sablonu.md` |
| **Ç3 Çeyreklik Güncelleme** | 3.000 | 3 | 8 | 5 | DOCX 8-12 sayfa | `c3-ceyreklik-sablon.md` |
| **Ç4 Çeyreklik Ön Bakış** | 1.500 | 2 | 4 | 3 | DOCX 3-5 sayfa | `c4-on-bakis-sablon.md` |
| İlk kez kapsama araştırması (T1) | 6.000 | 8 | — | 10 | Markdown | `task1-arastirma.md` |
| Sektör raporu | 5.000 | 6 | 12 | 8 | DOCX 15+ sayfa | `sektor-analiz-sablonu.md` |
| Bülten özeti | 400 | 0 | — | 2 | Serbest | — |
| Midas Podcast notu | 500-800 | 1 | — | 3 | Serbest | — |

### Profesyonel Doküman Çıktısı (DOCX)

→ **Tam DOCX rehberi:** `references/c2-tam-kapsama/profesyonel-cikti-rehberi.md`

- **copywriter skill** okunur — İlker'in sesi, tonu, yapısı
- Bölüm başlıkları içgörü odaklı — "Ölçek liderleri kopuyor" (doğru), "Rekabet Analizi" (yanlış)
- Grafik referansları metin içinde organik, `[GRAFİK: ...]` direktifleri YASAK
- İlker'in DNA'sı: yapısal faktörler numaralandırılır, "Beklenti → Gerçekleşme → Neden?"
- **DOCX format:** Calibri 11pt, tablo zebra striping, kaynak notu italik gri, 300 DPI grafik gömme
- **Her 200-300 kelimede 1 grafik** — %60-80 sayfa doluluk hedefi
- **Notasyon:** G = Gerçekleşme, T = Tahmin

### Midas Podcast Araştırma Notu

500-800 kelime, opinionated: 1 ana tez + 3 destekleyici nokta. "Herkesin bildiği" vs "kimsenin bilmediği" ayrımı. Tartışma sorusu ile bitir.

---

## 🔴 Veri Doğrulama Protokolü — KÖK KURAL

**Kapsam:** T1-T5 dahil TÜM task'lar ve çıktılar. Sadece finansal analiz değil, her web_search sonucu dahil.

> **"İnternetten çekilen her veri teyide muhtaçtır."** — İlker Başaran, Mart 2026

### Kök Kural: Çift Kaynak Doğrulama

İnternetten (web_search, web_fetch) alınan **her rakam, tarih, oran ve olgusal ifade** ikinci bir bağımsız kaynakla teyit edilmelidir. Tek kaynaktan gelen veri analize doğrudan giremez.

| Durum | Aksiyon |
|-------|---------|
| Birincil kaynak (KAP/BBB Finans) + ikinci kaynak eşleşiyor | ✅ Kullan |
| Tek kaynak var, ikincisi bulunamıyor | `[TEK KAYNAK — TEYİT GEREKLİ]` etiketi ile sun |
| İki kaynak çelişiyor | Her ikisini raporla, birincil kaynağı baz al, farkı açıkla |
| Hiçbir kaynak yok, hafızadan/training data'dan geliyor | ❌ **KULLANMA** — fabrike veri üretmek yasak |

**Birincil kaynak hiyerarşisi (doğrulama sırası):**
1. BBB Finans araçları (KAP/İş Yatırım)
2. Şirketin kendi IR sayfası / faaliyet raporu
3. Resmi kurum verileri (TAPDK, BDDK, TÜİK, TCMB)
4. Damodaran veri setleri
5. Yahoo Finance (yurt dışı peer'lar için)

**Teyit kabul edilmeyen kaynaklar:** StockAnalysis, TradingView, Investing.com, GuruFocus, Wikipedia, forum/blog/sosyal medya.

### Tarihsel Hata Kayıtları (TBORG Q4 Dersi — Mart 2026)

**Kök neden:** Tekrarlayan pattern — NTHOL (StockAnalysis), NVO (Lilly 7x yanlış), TBORG ("~70 lt" fabrike, TAPDK atlanması).

### 5 Operasyonel Kural

1. **Kaynak Etiketi ZORUNLU** — Her rakama parantez içinde kaynak: `(KAP Q4 2025, BBB Finans)`. Kaynağı belirsiz → `[DOĞRULANMADI]`.
2. **"Tahmin ediyorum" = Kırmızı Bayrak** — Veri dosyada varken tahmin yapma. Bulamıyorsan: `[KAYNAK GEREKLİ]`.
3. **Excel Okuma Protokolü** — Tüm sheet'leri listele → başlık satırı → SON satır (en güncel) → aylık veri varsa tüm ayları say.
4. **Önceki Q Referansı ZORUNLU** — Çeyreklik analizlerde İlker'in önceki yazılarından alıntı.
5. **Son Kontrol** — "Bu rakamı hangi dosyada gördüm?" → doğrulanamayan kaldırılır.

---

## 🔴 Kırmızı Bayraklar (Otomatik Dikkat)

| Kırmızı Bayrak | Neden Tehlikeli |
|----------------|----------------|
| ROIC < %10 | Sermaye verimliliği düşük — WACC'ı karşılayamıyor |
| Kronik negatif FCF | Para yakıyor — büyüme kârsız |
| Net Borç/FAVÖK > 4x | Aşırı kaldıraç — faiz artışına kırılgan |
| Pazar payı kaybı (3+ yıl) | Rekabet gücü yapısal olarak zayıflıyor |
| Yönetim sahipliği < %1 | Masada parası yok |
| Muhasebe manipülasyonu şüphesi | Güvenilmez — tüm tez çöker |

Bu bayraklardan herhangi biri varsa → "Neden hâlâ değer görüyoruz?" sorusu cevaplanmalı.

---

## ✅ Governor İnceleme Kontrol Listesi

| Kriter | Kontrol | Kabul Eşiği |
|--------|---------|-------------|
| **Sektör** | TAM, CAGR, düzenleyici ortam, Porter? | Hepsi mevcut |
| **Moat** | Türü, gücü (0-10), moat barometresi? | Skor + gerekçe |
| **Finansallar** | 6 metrik tablosu, veto kontrolü, ROIC dinamikleri? | 6/6 metrik + veto |
| **Comps** | Peer tablosu, statistical summary, sanity checks? | Min 4 peer + gerekçe |
| **DCF** | Faz 0→3 uyumlu, sensitivity, TV ağırlığı? | bbb-dcf protokolü |
| **Risk** | İyimser + Kötümser dengeli, 3 senaryo, kill criteria? | Spesifik + ölçülebilir |
| **Kaynak** | KAP/IR birincil, tüm rakamlar kaynaklı? | `[DOĞRULANMADI]` yok |
| **Karar** | "ÖNCE KARAR" süreci, verdict + conviction %? | İlker onayı |
| **Thesis Tracker** | Scorecard + catalyst calendar oluşturuldu mu? | Dosya mevcut |
| **Kelime Sayısı** | Min standard karşılandı mı? | Çıktı türüne göre tablo |

### Teslim Öncesi Kontrol Listesi (Her Çıktıda)

Her deliverable teslim edilmeden önce:

1. **Sayılar tutarlı mı?** — Tablo, metin ve grafik aynı rakamı gösteriyor mu?
2. **`[DOĞRULANMADI]` etiketi var mı?** — Varsa birincil kaynaktan doğrula veya kaldır
3. **Kaynak etiketi** — Her rakamın yanında parantez içinde kaynak var mı?
4. **Quality Value testi** — Şirketin Quality Value matrisindeki yeri belirlenmiş mi?
5. **Moat barometresi** — Terminal ROIC vs WACC hesaplanmış mı?
6. **Kill criteria** — Spesifik, ölçülebilir, en az 2 tane var mı?

---

## 🔧 Araç Kullanımı

### BBB Finans (BIST — BİRİNCİL)
```bash
cd ~/.openclaw/workspace/skills/bbb-finans/scripts

# KAP özet finansallar (son 4 yıl bilanço + gelir tablosu)
python3 bbb_kap.py {TICKER} --kap-summary

# Şirket bilgisi (sektör, ortaklık)
python3 bbb_kap.py {TICKER} --lookup

# Detaylı finansal tablolar (147+ kalem — İş Yatırım)
python3 bbb_financials.py {TICKER} --start-year 2022 --end-year 2025 --section all --full

# DCF JSON (programatik erişim)
python3 bbb_financials.py {TICKER} --dcf --json > /tmp/{TICKER}_dcf.json

# İş Yatırım ek endpoint'ler
python3 bbb_financials.py {TICKER} --summary    # Özet kart: fiyat, market cap, çarpanlar, marjlar
python3 bbb_financials.py {TICKER} --price
```

**Mevcut Veri Kaynakları Envanteri (BBB Finans v2.0):**

| Dosya | Ne Veriyor | Equity-Analyst Kullanımı |
|-------|-----------|-------------------------|
| **bbb_financials.py** | 147+ kalem finansal tablo + OHLCV fiyat + endeks, 2019-güncel | **T1-T3 birincil veri**, comps market cap |
| **bbb_kap.py** | Bildirimler, ÖDA, şirket lookup, KAP özet finansal | **T1 ön araştırma**, bildirim takibi. ⚠️ KAP SSR nominal veri döndürebilir — rakamları modele girme, `bbb_financials.py`'yi baz al |
| **bbb_yfinance.py** | Yurt dışı peer: fiyat, çarpan, earnings, peer compare | **T3 comps** (sadece yabancı peer) |
| **bbb_fx.py** | Döviz kurları (TCMB XML API) | WACC hesabı (kur) |

**⚠️ Henüz programatik erişimi olmayan veriler:**
- **TCMB faiz oranları + enflasyon** → EVDS API key'i gerekli (kayıt: evds2.tcmb.gov.tr). Key gelince `bbb_fx.py`'ye eklenecek. Şimdilik `web_fetch` ile TCMB'den veya Damodaran'dan manuel çekilir.
- **Emtia fiyatları** → Gerekirse ileride eklenecek.
- **Makro göstergeler (GDP)** → Gerekirse ileride eklenecek.

### Yahoo Finance (Yurt Dışı Peer'lar — BBB Finans Altında)

```bash
cd ~/.openclaw/workspace/skills/bbb-finans/scripts

# Detaylı fiyat + metrikler
python3 bbb_yfinance.py quote LVS

# Temel finansal göstergeler
python3 bbb_yfinance.py fundamentals WYNN

# Peer karşılaştırma tablosu (comps workflow için — medyan/min/max otomatik)
python3 bbb_yfinance.py compare LVS,WYNN,MGM,GENTING.KL

# Earnings date + sürpriz geçmişi
python3 bbb_yfinance.py earnings LVS

# Ham JSON (programatik erişim)
python3 bbb_yfinance.py json LVS
```

**BIST hisseleri:** Yahoo Finance'da `{TICKER}.IS` suffix kullanır (THYAO.IS, TBORG.IS).
**Kural:** BIST finansal verileri için Yahoo DEĞİL → BBB Finans kullan. Yahoo sadece yurt dışı peer + fiyat.

### Grafik Üretimi
```bash
# Demo grafikler üret (7 tür)
python3 ~/.openclaw/workspace/skills/equity-analyst/scripts/grafik-uret.py --demo --ticker TBORG --cikti-klasor /tmp/charts

# Modül olarak kullan
from scripts import grafik_uret as gu
gu.gelir_marj_grafigi(yillar, gelir, marj, 'THYAO', 'charts/THYAO_G02.png')
gu.football_field_grafigi(yontemler, dusuk, yuksek, mevcut, hedef, 'charts/THYAO_G32.png')
```

### DCF Model Doğrulama & Excel Audit
```bash
SCRIPT=~/.openclaw/workspace/skills/equity-analyst/scripts/dcf-dogrulama.py

# DCF doğrulama (formül hataları, WACC aralığı, TV oranı, Fisher parity)
python3 $SCRIPT MODEL.xlsx
python3 $SCRIPT MODEL.xlsx --para-birimi USD --json sonuc.json

# Genel Excel audit (hardcoded, format tutarsızlığı, formül hataları)
python3 $SCRIPT MODEL.xlsx --audit
python3 $SCRIPT MODEL.xlsx --audit --json audit_sonuc.json
```

**T2 tamamlandıktan sonra:** `python3 $SCRIPT {TICKER}_Financial_Model.xlsx --audit` çalıştır.
Kritik sorun varsa düzelt, TEMİZ çıktısı aldıktan sonra T3'e geç.

---

## 📚 Reference Dosyaları

| Dosya | İçerik | Ne Zaman Oku |
|-------|--------|-------------|
| `references/model-guncelleme/model-guncelleme.md` | Model güncelleme workflow (beat/miss, estimate revision, değerleme etkisi, Ç3 geçiş kararı) | Bilanço geldiğinde / WACC güncellemesinde |
| `references/c2-tam-kapsama/karsilastirmali-degerleme.md` | Peer karşılaştırma framework'ü, IAS 29 kuralları, statistical summary | Göreceli değerleme yaparken |
| `references/c3-ceyreklik/ceyreklik-guncelleme.md` | Beklenti/gerçekleşme, tahmin revizyonu, tez etkisi, ön bakış | Çeyreklik analiz yaparken |
| `references/tez-takip/tez-takip-sablonu.md` | Tez takip kartı, tez ayağı takibi, çıkış kriterleri | Her yatırım kararında |
| `references/sektor/sektor-analiz-sablonu.md` | Kapsamlı sektör analizi şablonu | Sektör raporu hazırlarken |
| `references/ortak/bist-sektor-metrikleri.md` | BIST sektörlerine özel 4-6 metrik/kaynak/benchmark | Sektör analizi ve comps'ta |
| `references/c1-fikir-uretimi/fikir-uretimi.md` | **Ç1 süreç** — 4 adım (Topla→Sentezle→Sorgula→Karar), 5 screen türü, tematik tarama, ters İNA, karar matrisi | Sistematik fırsat ararken |
| `references/c2-tam-kapsama/task4-grafik-uretim.md` | 25+10 grafik kataloğu, Python kodu, DPI standardı, BBB stili | Grafik oluştururken |
| `references/c2-tam-kapsama/rapor-sablonu.md` | **Ç2 rapor fiziksel yapısı** — sayfa bazlı layout, Grafik/Tablo numaralama, chart embed haritası, ■ bullet formatı, yoğunluk kuralları | T5 rapor yazımında (ZORUNLU) |
| `references/c2-tam-kapsama/profesyonel-cikti-rehberi.md` | DOCX rapor yapısı, formatlama kuralları, kalite kontrol listesi | DOCX çıktı üretirken |
| `references/ortak/birim-ekonomi-rehberi.md` | Müşteri yaşam boyu değeri/edinim maliyeti, kohort, net gelir tutma — dijital/platform şirketleri | MACKO, Pop Mart, SaaS benzeri |
| `references/ortak/skorlama-sistemi.md` | Ağırlıklı skorlama sistemi (Finansal %50, Haber %25, Teknik %25) | Sayısal skorlama |
| `references/ortak/cikti-sablonlari.md` | 4 çıktı tipi canonical haritası + bileşen kütüphanesi (sektör, moat, comps, DCF, risk blokları) | Bileşen referansı |
| `references/c1-fikir-uretimi/c1-sablon.md` | **Ç1** — Fikir Üretimi çıktı şablonu (1-2 sayfa, sentez + ters İNA + hipotez) | Fikir üretimi |
| `references/c2-tam-kapsama/rapor-sablonu.md` | **Ç2** — Rapor fiziksel yapısı (sayfa layout, chart embed, yoğunluk) | T5 assembly, rapor yapısı kararları |
| `references/c3-ceyreklik/c3-sablon.md` | **Ç3** — Çeyreklik Güncelleme çıktı şablonu (DOCX 8-12 sayfa, 15 QC) | Bilanço sonrası |
| `references/c4-on-bakis/c4-sablon.md` | **Ç4** — Çeyreklik Ön Bakış çıktı şablonu (DOCX 3-5 sayfa, 10 QC) | Sonuç öncesi |
| `references/ortak/standart-metrik-hesaplama.md` | İş Yatırım kalem kodları, ROIC/FCF/EBITDA/ROE/EPS formülleri, şirket tipi istisnaları (banka, holding, IFRS 16), yaygın hatalar | Her metrik hesaplamasında — T2, T3, Ç1, Ç3 |

| `references/ortak/turkiye-spesifik-rehber.md` | Türkiye iskontosu, holding NAV, bankacılık modeli, konglomera SOTP, konferans çağrısı/faaliyet raporu/IR sunumu analizi, siyasi risk | BIST hisse analizi yaparken |
| `references/ortak/analiz-metodolojisi.md` | Kalite kontrol checklist (4 kategori), "Önce Karar Sonra Araştırma" | Final QC kontrolü |
| `references/c2-tam-kapsama/task2-finansal-modelleme.md` | T2 workflow: BIST kalem sıralama, TTM/IC/S/C, senaryo framework, Excel 6-tab spec, bbb-dcf handoff | T2 başlatırken |
| `references/c2-tam-kapsama/task1-arastirma.md` | T1 workflow: 9 bölüm kelime aralıkları, input verification, yetersiz veri protokolü | T1 başlatırken |
| `references/c2-tam-kapsama/task3-hedef-fiyat.md` | İNA + Comps + Forward F/K reconciliation, ağırlık belirleme, ileri taşıma, SOTP, IAS 29 kuralları | Hedef fiyat türetirken |
| `references/ortak/rekabet-analizi-rehberi.md` | 2×2 matris, sektörel axis seçimi, rakip sınıflandırma, HHI, moat entegrasyonu | Rekabet analizi yaparken |
| `references/ortak/duzenleyici-ortam-taramasi.md` | Düzenleyici ortam kaynakları, CIMSA dersi | Her sektör analizinde |
| `references/ortak/yazi-kalitesi-rehberi.md` | İçgörü merdiveni, argüman inşa yapısı, consensus farkı çerçevesi, iyimser/kötümser denge, kontraryen düşünce, yazım standartları | T5 rapor yazarken (ZORUNLU) |

---

## Versiyon Geçmişi

**Mevcut:** v4.21 (2026-03-25) — Reel/Nominal Rekonsilasyon Sistemi (EBEBK Guidance REG)

### v4.21 (2026-03-25)
- **Kök neden:** EBEBK raporunda DCF Y1 (31,8B reel) ile yönetim guidance (37B nominal) doğrudan karşılaştırıldı → okuyucu "model düşük" sandı. Gerçekte DCF guidance'dan %7,5 agresif.
- **task2 §6A:** Guidance tablosuna Birim sütunu eklendi. Reel↔Nominal Rekonsilasyon şablonu zorunlu (IAS 29 şirketlerinde). Sapma yönü notu zorunlu.
- **task2 §10 Handoff:** 17 noktanın her birine Birim sütunu eklendi (IAS 29 Dec {SON_FY} / Nominal / Oran).
- **task2 Çıkış Gate:** Guidance Rekonsilasyonu + birim tutarlılık kontrolü eklendi.
- **bbb-dcf Faz 1.5 Kontrol 7:** Guidance Rekonsilasyonu — nominal→reel çevirisi, sapma hesabı, %15+ sapma uyarısı. Sapma açıklanmadan parametreler KİLİTLENMEZ.
- **rapor-sablonu:** Projeksiyon tablosu başlığına {BİRİM_ETİKETİ}. Guidance Rekonsilasyon Kutusu şablonu. Tarihsel tabloya birim etiketi.
- **task5 Faz C3:** Birim etiketleme talimatı + Guidance Rekonsilasyon Kutusu zorunluluğu.
- **senaryo-metodoloji §0A:** Guidance karşılaştırma hatası uyarısı + EBEBK örneği.
- **bbb-dcf SKILL.md:** "6 Tutarlılık Kontrolü" → "7 Tutarlılık Kontrolü".

### v4.17 (2026-03-24)
- **SOUL/AGENTS Hizalaması:** Düşünce mimarisi (Topla→Sentezle→Sorgula→Güncelle) skill pipeline'ına entegre edildi
- **"Equity Analyst" → "Research Analyst"** kimlik güncellemesi
- **T1 Çıkış Gate'i:** Sentez sorusu (3 kelimelik hikaye), çelişki kontrolü, nedensellik sorusu
- **T2 Çıkış Gate'i:** Varsayım zinciri (makro→sektör→şirket), yaratıcı zorlama soruları
- **task5 Faz 0 yeniden sıralama:** "Veriler ne söylüyor?" başlangıç noktası, "Piyasa ne fiyatlıyor?" karşılaştırma noktası
- **kalite-kontrol A8-A11:** Sentez testi, varsayım zinciri, nedensellik kontrolü, yaratıcı zorlama
- **BBB Research Analitik Felsefesi:** 3→4 garanti (sentez eklendi)

### v4.20 (2026-03-24)
- **Çelişki Matrisi T3'e taşındı:** T5 Faz 0'dan T3 Ön Kontrol'e taşındı (varsayımlar kilitlenmeden ÖNCE). T3'te oluşturulur (`{TICKER}_celiski_matrisi.md`), bbb-dcf Faz 1.5'te Kontrol 6 olarak doğrulanır, T5 Faz 0'da rapor eşlemesi yapılır.
- **İki katmanlı mimari:** T3 = düşün, çelişki bul, varsayımı düzelt. T5 Faz 0 = matrisi oku, çözümleri rapor bölümlerine eşle.
- **bbb-dcf Faz 1.5 Kontrol 6:** Çelişki Matrisi dosya mevcudiyeti + min 2 çelişki + çözüm yolu doğrulaması. Başarısız olursa parametreler KİLİTLENMEZ.
- **Kök neden:** GAP-2 (Çelişki Matrisi T5'te çok geç — varsayımlar zaten kilitli, düzeltme imkanı yok)

### v4.19 (2026-03-24)
- **T5 Faz 0 yeniden tasarımı (v2.4):** "5 soru doldur" → "Argüman İnşası" — Çelişki Taraması (T1 risk × T3 varsayım 5x5 matrisi, min 2 çelişki gate), Ana Argüman (3 paragraf testi: tez+kanıt+karşı-tez), Argüman Dalları (3-5 tez + 2 karşı-tez, bölüm eşleme), Piyasa Karşılaştırması, Tekrar Haritası
- **Faz B/C gate'lerine omurga kontrolü:** Her gate'de Faz 0 Ana Argüman'a geri dönüş + dal uyumu kontrolü
- **Faz F "En Kırılgan Varsayım" notu:** Sayfa 1'e Çelişki Matrisi'nden türetilen tek cümlelik dürüstlük katmanı
- **kalite-kontrol A8 güncelleme:** "Sentez hikayesi" → "Ana Argüman + Dallar + Çelişki çözümleri" referansı
- **Sentez öğrenme havuzu:** `research/methodologies/sentez-ogrenme-havuzu.md` — gelecek mimari adımlar (G1-G3) + pattern kütüphanesi
- **Kök neden:** T5 bölüm-merkezli yazım (agent bölüm yazıyor, argüman kurmuyor) + risk↔varsayım çelişkilerinin silo'da kalması

### v4.18 (2026-03-24)
- **T1 Ön Sentez Hipotezi:** Yazım Taslak Planı'na zorunlu hipotez + her bölüm sonunda hipotez kontrolü (task1 R1)
- **T3 Risk↔Terminal Çelişki Kontrolü:** T3 başlangıcında T1 Sentez Notu + §9 riskleri ile terminal varsayımlar karşılaştırması (SKILL.md R3)
- **T5 Faz C3 Risk Çapraz Kontrol:** Projeksiyon varsayımları yazılmadan önce T1 §9 riskleri + T3 kontrol notu ile çapraz doğrulama (task5 R2)
- **A8 Sentez Tutarlılık:** "3 kelimelik hikaye var mı?" → "Faz 0 hikayesi rapor boyunca tutarlı mı?" olarak revize (kalite-kontrol R4)
- **T2 T1 Sentez Notu zorunlu:** T1 Sentez Notu ön koşul olarak eklendi (task2 R6)
- **BBB Felsefesi İçgörü Merdiveni köprüsü:** Kantitatif disiplin maddesine yazi-kalitesi-rehberi Seviye 3+ referansı (SKILL.md R8)
- **Kök neden:** İlker "bölümler yazıyorsun, argüman kurmuyorsun" tespiti. Pipeline'a sentez ve çelişki zorlama mekanizmaları enjekte edildi.

### v4.16 (2026-03-24)
- **Dereceli Aktarım prensibi:** T1 "AYNEN kopyala" → olgusal aynen, analitik first-mention-full
- **Faz 0'a §0.5 Tekrar Haritası:** TOP 5 fact'in bölüm dağılımı ve perspektif planı zorunlu
- **First-Mention-Full kuralı:** Aynı veri noktasının tam açıklaması MAX 2 kez, sonrası referans + yeni açı
- **Faz H'ye H4 Tekrar Frekansı Taraması:** Post-assembly ZORUNLU inline regex kontrolü
- **QC §15 S5 güçlendirme:** TAM AÇIKLAMA vs terim ayrımı, S5b bölüm yeni açı kontrolü
- **yazi-kalitesi §7D güçlendirme:** Perspektif kontrolü, icgoru_kutusu istisnası
- **Kapak URL düzeltmesi:** borsadabirbasina.com → borsadabibasina.com (engine + assembly)
- **Analist formatı:** "Kaya" → "Kaya (AI Agent)" engine default

### v4.15 (2026-03-24)
- T5'e Faz 0 (Bağımsız Keşif Kontrol Noktası) referansı eklendi — SKILL.md'de eksikti
- T2 deliverable ifadesi düzeltildi: "projeksiyonlar" → "senaryo varsayımları" (projeksiyon T3/bbb-dcf'de yapılır)
- Forward HBK parametrik formül (v2.1) cross-ref eklendi: task3'teki Yöntem 2 artık SKILL.md'de referanslı
- Faz H (Post-Assembly Doğrulama) task5'e önceki session'da eklendi, burada teyit edildi
- SKILL.md başlık versiyonu changelog ile senkronize edildi (v3.8 → v4.15)

### v4.8 (2026-03-23)
- BBB Research Analitik Felsefesi eklendi (Bağımsız Keşif çerçevesi)
- T5 Sentez Protokolü: T1 olgusal/analitik ayrımı, Analitik Köprü konsepti
- Terminoloji standardizasyonu: Adil Değer Tahmini, EKLE/TUT/AZALT, Kötümser/Baz/İyimser
- 6 yeni engine primitifi tanımlandı (bilgi_kutusu, skor_karti, zaman_cizelgesi, karar_agaci, ozet_finansal, icgoru_kutusu)
- Kalite kontrol: Analitik Kalite Kontrolleri (A1-A7) eklendi
- task5 v2.0, profesyonel-cikti-rehberi v5.0, kalite-kontrol v3.0

| Tarih | Versiyon | Özet |
|-------|----------|------|
| 2026-03-25 | **v4.22** | Ç1 Fikir Üretimi v2.0: SOUL düşünce mimarisi entegrasyonu. fikir-uretimi.md yeniden yazıldı (4 adım: Topla→Sentezle→Sorgula→Karar). c1-sablon.md yeniden yazıldı (sentez 3 soru, Gordon Growth zımni büyüme ters İNA, falsifiable hipotez + kill criteria, T1 handoff soruları, yapılandırılmış karar matrisi). QC 5→8, kelime 500→800-1200. |
| 2026-03-25 | **v4.21** | Reel/Nominal Rekonsilasyon Sistemi: task2 §6A birim etiketi + rekonsilasyon şablonu, task2 §10 handoff birim sütunu, task2 çıkış gate, bbb-dcf Faz 1.5 Kontrol 7, rapor-sablonu birim etiketi + Guidance Kutusu, task5 C3 birim talimatı, senaryo-metodoloji §0A uyarı. EBEBK REG kök neden. |
| 2026-03-22 | **v4.7** | Grafik kalite audit: grafik-uret.py engine'e _tamsayi_eksen() helper, kaynak notu çakışma fix, donut renk çakışma önleme, ok ucu zorder, tahmin gösterge standardı (yıl belirtme), TAM/SAM/SOM açılım, Özsermaye terminolojisi, G25 2-panel, G04 yurtdışı pay etiketi. task4 v3.1 |
| 2026-03-22 | **v4.6** | Excel model audit tamamlandı: task2 v1.7 (CFO 5-bileşen, Bilanço 3-tablo entegrasyonu, Senaryolar Row 7-34 haritası, yıl bazlı marj ayrımı), task3 v2.2 (Sensitivity formül bazlı, Implied Exit Multiple), senaryo-metodoloji v3.1 (§6.2 FM tab detayı, MQS 4-band) |
| 2026-03-19 | v4.0 | Yapısal audit: sayfa aralık çakışması, T1 9-bölüm, mrd kanonik, ondalık virgül, changelog ayrıştırma |
| 2026-03-18 | v3.2-3.9 | Fikir inşası, çıktı tipleri, routing logic, Excel handoff, Türkiye rehberi, PDF okuma, İlker feedback |
| 2026-03-17 | v3.0-3.1 | Tam migration (T1-T5 pipeline), DOCX + Chart + Türkçe |
| 2026-02-08 | v1.0-2.0 | İlk oluşturma, BBB özelleştirmesi |

**Tam changelog + BBB Öğrenmeler:** `references/changelog.md`
