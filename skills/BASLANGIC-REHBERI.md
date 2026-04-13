# BBB Finans Skills — Claude Desktop Kurulum ve Kullanım Rehberi

**Tarih:** 2026-04-01 | **Versiyon:** 1.0
**Hazırlayan:** Borsada bi' Başına Araştırma Ekibi

---

## Bu Rehber Ne İçin?

Bu rehber, BBB Finans skill setini (equity-analyst, bbb-finans, bbb-dcf) Claude Desktop uygulamasında **tam kapasite** kullanabilmeniz için gereken kurulum adımlarını ve kullanım talimatlarını içerir.

**Yaygın yanlış anlaşılma:** "Bu skill'lerdeki Python scriptleri Claude Desktop'ta çalışmaz." Bu **yanlıştır.** Claude Desktop'un Cowork (yerel agent) modu aktif edildiğinde, tüm Python scriptleri doğrudan bilgisayarınızda çalışır. Hiçbir ek platforma ihtiyaç yoktur.

---

## Skill Seti Nedir? Ne Yapabilirsiniz?

Bu 3 skill birlikte çalışan entegre bir BIST hisse analiz ekosistemidir:

### 1. equity-analyst (Kaya — Finansal Analist)
Profesyonel hisse analizi ve yatırım tezi üretim skill'i. Quality Value metodolojisiyle çalışır.

**Yapabilecekleriniz:**
- Hisse hakkında hızlı fikir üretimi (Ç1 — 1-2 sayfa sentez + ters İNA)
- Tam kapsama raporu (Ç2 — 30-50 sayfa DOCX, T1-T5 pipeline)
- Çeyreklik güncelleme (Ç3 — bilanço sonrası "ne değişti?" analizi)
- Çeyreklik ön bakış (Ç4 — sonuçlar öncesi hazırlık notu)
- Sektör analizi, sistematik tarama, peer karşılaştırma
- Moat değerlendirmesi, 6 metrik (ROIC, FCF, Brüt Marj, Net Borç/FAVÖK, Büyüme, ROE)
- Grafik üretimi (25-35 profesyonel chart, BBB stili)
- Profesyonel DOCX rapor çıktısı

**Örnek komutlar:**
- "THYAO için hızlı fikir üretimi yap"
- "EBEBK'i analiz et, T1 başlat"
- "Çeyreklik güncelleme yaz — TBORG Q4 2025"
- "Sektör analizi yap — havacılık"

### 2. bbb-finans (Veri Toplama Araç Seti)
BIST şirketleri için veri toplama motoru. Diğer iki skill'in veri katmanını sağlar.

**Yapabilecekleriniz:**
- 147+ kalem finansal tablo çekme (İş Yatırım API — IAS 29 düzeltmeli)
- KAP bildirimlerini listeleme, filtreleme, arşivleme, PDF indirme
- Şirket profili, ortaklık yapısı, sektör bilgisi çekme
- Hisse fiyatı, endeks verileri (OHLCV)
- Yabancı peer verileri (Yahoo Finance — fiyat, çarpan, earnings)
- Döviz kurları (TCMB)
- Tüm verileri cache'leyerek hızlı erişim

**Örnek komutlar (Claude'a söyleyin, o çalıştıracak):**
```
"THYAO'nun son 3 yıl finansal tablolarını çek"
"KAP'ta bugünün önemli bildirimlerini göster"
"WYNN ve MGM'yi karşılaştır" (yabancı peer)
"Güncel dolar kuru nedir?"
```

### 3. bbb-dcf (DCF Değerleme Modeli)
Aswath Damodaran metodolojisiyle İndirgenmiş Nakit Akışı değerlemesi. IAS 29 uyumlu.

**Yapabilecekleriniz:**
- Tam DCF değerleme (FCFF modeli — 10 yıl projeksiyon + terminal value)
- WACC hesaplama (Beta, ERP, CRP, Kd, Ke)
- Monte Carlo simülasyonu
- Sensitivity analizi (7x5 grid)
- Fisher cross-check (TL vs USD tutarlılık)
- Holding NAV analizi
- 17 Damodaran diagnostik sorusu

**Örnek komutlar:**
- "THYAO'yu değerle — DCF modeli kur"
- "WACC hesapla — EBEBK"
- "Hedef fiyat nedir? Ucuz mu pahalı mı?"

---

## Kurulum (4 Adım)

### Adım 1: Skill Dosyalarını Yükleyin

Claude Desktop'ta yeni bir **Proje** oluşturun (veya mevcut projenize ekleyin):

1. Claude Desktop'u açın
2. Sol menüden **Projects** > **New Project** (veya mevcut projeniz)
3. Proje ayarlarında **Project Knowledge** bölümüne gidin
4. Her bir skill klasörünü (equity-analyst, bbb-finans, bbb-dcf) zip olarak yükleyin:
   - `equity-analyst.zip`
   - `bbb-finans.zip`
   - `bbb-dcf.zip`

> **Not:** Zip dosyalarını doğrudan sürükleyip bırakabilirsiniz.

### Adım 2: Cowork Modunu Aktif Edin

Cowork modu, Claude'un bilgisayarınızda dosya okuması, yazması ve **script çalıştırması** için gereklidir. Bu mod olmadan Claude sadece sohbet yapabilir, script çalıştıramaz.

1. Claude Desktop'ta **sol alt köşedeki** profil ikonunuza tıklayın
2. **Settings** > **Features** bölümüne gidin
3. **Cowork** seçeneğini aktif edin (toggle'ı açın)
4. Cowork aktifken Claude sizden izin isteyecektir — ilk kullanımda onaylayın

> **Güvenlik notu:** Cowork modu Claude'a bilgisayarınızda komut çalıştırma yetkisi verir. Her işlemde size onay sorar. Güvendiğiniz klasörleri "Trusted Folders" olarak ekleyebilirsiniz.

### Adım 3: Skill Dosyalarını Bilgisayarınıza Yerleştirin

Skill'lerdeki Python scriptlerinin çalışabilmesi için dosyaların bilgisayarınızda erişilebilir bir yerde olması gerekir.

**Önerilen konum:**
```
~/Documents/bbb-skills/
├── equity-analyst/
├── bbb-finans/
└── bbb-dcf/
```

Zip dosyalarını bu konuma çıkartın. Ardından Cowork ayarlarında bu klasörü **Trusted Folder** olarak ekleyin:
- Settings > Features > Cowork > Trusted Folders > `~/Documents/bbb-skills` ekleyin

### Adım 4: Python Bağımlılıklarını Kurun

Bilgisayarınızda Python 3.10+ kurulu olmalıdır. Terminal'i açın ve şu komutu çalıştırın:

```bash
# Python kurulu mu kontrol edin
python3 --version

# Bağımlılıkları kurun
pip3 install requests yfinance
```

Bu kadar. Artık hazırsınız.

---

## CLAUDE.md'ye Eklemeniz Gereken Talimatlar

Claude'un skill'leri doğru kullanabilmesi için projenizin **Custom Instructions** (veya CLAUDE.md) bölümüne aşağıdaki talimatları ekleyin. Bu talimatlar Claude'a:
- Script'lerin nerede olduğunu
- Hangi sırayla çalıştırması gerektiğini
- Veri hiyerarşisini

öğretir. Aşağıdaki metni olduğu gibi kopyalayıp yapıştırın:

---

```markdown
# BBB Finans Skills — Çalışma Talimatları

## Skill Dosyaları
Bu projede 3 skill yüklüdür: equity-analyst, bbb-finans, bbb-dcf. Bunlar birbirine bağımlı, entegre çalışan bir BIST hisse analiz ekosistemidir.

## Script Konumu
Python scriptleri şu konumdadır (kendi path'inize göre güncelleyin):
```
~/Documents/bbb-skills/bbb-finans/scripts/
```

Script çalıştırırken bu path'i kullan:
```bash
cd ~/Documents/bbb-skills/bbb-finans/scripts
python3 bbb_financials.py {TICKER} --section all --full
```

## Veri Hiyerarşisi (ÖNEMLİ)
1. **BİRİNCİL:** bbb_financials.py (İş Yatırım API, IAS 29 düzeltmeli) — TÜM modelleme ve metrik hesaplamaları buradan
2. **İKİNCİL:** bbb_kap.py (KAP API) — bildirim takibi, şirket bilgisi, quick scan
3. **YABANCI PEER:** bbb_yfinance.py (Yahoo Finance) — SADECE yurt dışı şirketler için
4. **DÖVİZ:** bbb_fx.py (TCMB) — güncel kurlar

## IAS 29 Kuralı
- BIST şirketleri: İş Yatırım (bbb_financials.py) IAS 29 düzeltmeli veri döndürür. KAP SSR nominal veri döndürebilir.
- İki kaynak farklı rakam verirse: HER ZAMAN bbb_financials.py'yi baz al
- Yahoo Finance BIST çarpanları GÜVENİLMEZ (IAS 29 düzeltmeli finansallar + nominal fiyat = absürt çarpanlar)

## Çıktı Dosyalama
Tüm analiz çıktılarını şu yapıda kaydet:
```
research/companies/{TICKER}/
├── {TICKER}_research.md         (T1)
├── {TICKER}_financial_analysis.md (T2)
├── {TICKER}_VALUATION.md        (T3)
├── charts/                      (T4 grafikleri)
└── {TICKER}_Rapor_YYYY-MM-DD.docx (T5)
```

## Kaynak Etiketi Zorunluluğu
Her rakama parantez içinde kaynak yaz: (KAP Q4 2025, BBB Finans). Kaynağı belirsiz = [DOĞRULANMADI].

## DCF Kuralları
- Tek session'da tamamlanmaya çalışılmaz. Faz 0 > 1 > 1.5 > 2 > 3 sırasıyla
- Faz 1.5'te parametreler kilitlenir, Faz 2'de değiştirilmez
- Fisher cross-check zorunlu: TL hedef ≈ USD hedef x kur (sapma <%15)
- Terminal growth >= WACC ise ENGELLE
```

---

## Kullanıma Başlama — İlk Test

Kurulumunuzu doğrulamak için Claude Desktop'ta şu komutu deneyin:

### Test 1 — Veri Çekme (bbb-finans)
Claude'a şunu söyleyin:
> "THYAO'nun özet finansal kartını çek. Script konumu: ~/Documents/bbb-skills/bbb-finans/scripts/"

Claude, `bbb_financials.py THYAO --summary` komutunu çalıştırarak fiyat, piyasa değeri, çarpanlar ve marjları getirecektir.

### Test 2 — Fikir Üretimi (equity-analyst)
Claude'a şunu söyleyin:
> "THYAO için hızlı fikir üretimi yap (Ç1 formatında)"

Claude, equity-analyst skill'ini kullanarak veri toplayacak, sentezleyecek ve 1-2 sayfalık bir değerlendirme sunacaktır.

### Test 3 — KAP Bildirimleri (bbb-finans)
Claude'a şunu söyleyin:
> "THYAO'nun son 3 aydaki KAP bildirimlerini listele"

Claude, `bbb_kap.py THYAO --last 3m` komutunu çalıştıracaktır.

**Eğer Test 1 çalışıyorsa** — tebrikler, tüm skill'ler tam kapasite kullanıma hazır.

**Eğer çalışmıyorsa** — muhtemel nedenler:
| Sorun | Çözüm |
|-------|-------|
| "Permission denied" | Cowork modunu aktif edin, klasörü Trusted Folders'a ekleyin |
| "python3: command not found" | Python 3 kurun: `brew install python3` (macOS) |
| "No module named requests" | `pip3 install requests yfinance` çalıştırın |
| "File not found" | Script path'ini kontrol edin, CLAUDE.md'deki path'i güncelleyin |

---

## Sık Sorulan Sorular

**S: Fintables MCP kurulu, bu skill'lere gerek var mı?**
Fintables temel finansal verileri sağlar. Bu skill'ler ise:
- 147+ kalemlik detaylı IAS 29 düzeltmeli veri (İş Yatırım)
- KAP bildirim takibi ve akıllı arşivleme
- Profesyonel rapor şablonları ve workflow (Ç1-Ç4)
- DCF değerleme modeli (Damodaran metodolojisi)
- Moat analizi, peer karşılaştırma, grafik üretimi
Fintables veri sağlar, bu skill'ler **analiz metodolojisi + veri + rapor üretimi** sağlar. İkisi birbirini tamamlar.

**S: Scriptler internet bağlantısı gerektiriyor mu?**
Evet. bbb_financials.py İş Yatırım API'sine, bbb_kap.py KAP API'sine, bbb_fx.py TCMB'ye bağlanır. Cache mekanizması var (7 gün), o yüzden aynı veriyi tekrar çekmez.

**S: DCF modeli tek seferde tamamlanır mı?**
Hayır. DCF protokolü 4+1 fazdan oluşur (Faz 0, 1, 1.5, 2, 3). Her faz ayrı oturumda yapılmalı. Bu bir kısıtlama değil, kalite kontrolü.

**S: Hangi hisseler destekleniyor?**
BIST'te işlem gören tüm hisseler (725+ şirket). Yabancı peer'lar Yahoo Finance üzerinden.

**S: Skill'ler Türkçe mi çalışıyor?**
Evet. Tüm çıktılar, tablolar, raporlar Türkçe. Sektörde yerleşmiş kısaltmalar (FAVÖK, ROIC, DCF, F/K) korunur.

---

## Hızlı Komut Referansı

| Ne İstiyorsunuz? | Claude'a Ne Söyleyin |
|-------------------|---------------------|
| Hızlı şirket değerlendirmesi | "{TICKER} için hızlı fikir üretimi yap" |
| Detaylı finansal tablo | "{TICKER}'ın 3 yıllık finansallarını çek" |
| KAP bildirimleri | "{TICKER}'ın son bildirimleri ne?" |
| DCF değerleme başlat | "{TICKER}'ı değerle, DCF modelini başlat" |
| Peer karşılaştırma (yabancı) | "LVS, WYNN, MGM'yi karşılaştır" |
| Çeyreklik güncelleme | "{TICKER} Q4 sonuçlarını değerlendir" |
| Döviz kuru | "Güncel USD/TRY kuru nedir?" |
| Sektör analizi | "Havacılık sektörü analizi yap" |
| Moat değerlendirmesi | "{TICKER}'ın hendek gücü nedir?" |

---

## Skill Dosya Yapısı (Referans)

```
bbb-skills/
├── equity-analyst/              ← Analist skill'i (Kaya)
│   ├── SKILL.md                 ← Ana workflow + routing logic
│   └── references/              ← 29 referans dosyası
│       ├── c1-fikir-uretimi/    ← Hızlı analiz şablonları
│       ├── c2-tam-kapsama/      ← T1-T5 tam rapor rehberleri
│       ├── c3-ceyreklik/        ← Çeyreklik güncelleme
│       ├── c4-on-bakis/         ← Sonuç öncesi hazırlık
│       ├── ortak/               ← Metrik hesaplama, skorlama, stil
│       ├── sektor/              ← Sektör analiz şablonu
│       ├── model-guncelleme/    ← Bilanço sonrası model güncelleme
│       └── tez-takip/           ← Yatırım tezi izleme kartı
│
├── bbb-finans/                  ← Veri toplama araç seti
│   ├── SKILL.md                 ← Komut referansı + IAS 29 uyarıları
│   ├── requirements.txt         ← Python bağımlılıkları
│   └── scripts/                 ← Python scriptleri
│       ├── bbb_financials.py    ← 147+ kalem finansal (İş Yatırım)
│       ├── bbb_kap.py           ← KAP bildirimleri + arşivleme
│       ├── bbb_yfinance.py      ← Yabancı peer (Yahoo Finance)
│       ├── bbb_fx.py            ← Döviz kurları (TCMB)
│       ├── bbb                  ← CLI router
│       ├── kap/                 ← Modüler KAP paketi (7 dosya)
│       └── dcf_tools/           ← DCF yardımcı modüller
│
├── bbb-dcf/                     ← DCF Değerleme skill'i
│   ├── SKILL.md                 ← Değerleme workflow + checklist
│   ├── methodology/             ← 6 teorik rehber (WACC, büyüme, risk...)
│   ├── templates/               ← DCF şablonları
│   ├── examples/                ← THYAO örnek DCF
│   ├── references/              ← 10 referans (formüller, sektör, CRP...)
│   └── scripts/                 ← DCF hesaplama scriptleri
│       ├── dcf_engine.py        ← Ana DCF motoru
│       ├── wacc_calculator.py   ← WACC hesaplama
│       ├── monte_carlo_dcf.py   ← Monte Carlo simülasyonu
│       └── dcf_excel_generator.py ← Excel model üretici
│
└── BBB-SKILLS-KURULUM-REHBERI.md ← Bu dosya
```

**Toplam:** 3 skill, 33 Python script, 45+ referans dokümanı, 1 örnek DCF modeli.

---

*Borsada bi' Başına — Quality Value Araştırma*
