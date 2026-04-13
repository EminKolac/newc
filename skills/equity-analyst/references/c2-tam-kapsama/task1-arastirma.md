# Şirket Araştırması Rehberi — T1 Detaylı Workflow v1.0

> T1 (Şirket Araştırması) task'ının detaylı yürütme rehberi.
> Her bölümün kelime aralığı, zorunlu içeriği ve kaynak hiyerarşisi tanımlanmıştır.
> SKILL.md'deki T1 bölümüne ek detay sağlar.

---

## Dil ve Terminoloji Kuralları

### Türkçe Karakter Zorunluluğu

Tüm çıktılar (research.md ve diğer deliverable'lar) doğru Türkçe karakterlerle yazılmalıdır:
- ş (s DEĞİL), ğ (g DEĞİL), ü (u DEĞİL), ö (o DEĞİL), ç (c DEĞİL), ı (i DEĞİL), İ (I DEĞİL)
- ASCII Türkçe (Türkçe karakterleri kullanmadan yazmak) **YASAK**
- Emdash (—), uzun tire, fancy unicode karakterler YASAK. Düz tire (-) kullan.

### Kurumsal Dil Referansı

Yazım tonu ve ifade kalıpları için kurumsal dil rehberine başvur:
**Dosya:** `research/methodologies/kurumsal-dil-ogrenme.md`

Bu dosya Türkiye'deki kurum raporlarından öğrenilen 150+ profesyonel finansal ifade kalıbı, kurum tonu karşılaştırmaları ve sektörel jargon içerir. Özellikle:
- Değerleme ve tavsiye dili (İş Yatırım, AK Yatırım, Deniz Yatırım tonu)
- Sektörel terimler (perakende, çelik, otomotiv, sigorta vb.)
- Olumsuz sonuçları zarif ifade etme kalıpları
- İlker'in makro/strateji dili ve portföy felsefesi

### Terim Karşılıkları Tablosu

Raporda İngilizce konsept terimler yerine Türkçe karşılıkları kullanılmalıdır. Sektörde yerleşmiş kısaltmalar (FAVÖK, ROIC, DCF, F/K, FD, TAM/SAM) İngilizce kalabilir.

| İngilizce Terim | Türkçe Karşılık | Kullanım Kuralı |
|-----------------|-----------------|-----------------|
| Moat | Hendek (rekabet avantajı) | Türkçe kullan |
| Moat Analysis | Hendek Analizi | Türkçe kullan |
| Porter's Five Forces | Porter Beş Güç Analizi | Türkçe kullan |
| Kill criteria | Tez çöküş kriterleri | Türkçe kullan |
| Skin in the game | Yönetim hisse sahipliği | Türkçe kullan |
| Guidance | Yönetim beklentisi / yönetim hedefi | Türkçe kullan |
| Management Quality Scorecard | Yönetim Kalitesi Karnesi | Türkçe kullan |
| Quality Value | Kalite-Değer (özel çerçeve adı) | İlk kullanımda açıklamalı İngilizce kalabilir |
| Track record | Geçmiş performans / sicil | Türkçe kullan |
| Beat (guidance beat) | Aşma (hedefi aştı) | Türkçe kullan |
| Miss (guidance miss) | Kaçırma (hedefi kaçırdı) | Türkçe kullan |
| Cross-check | Çapraz doğrulama | Türkçe kullan |
| Tailwind / Headwind | Olumlu rüzgâr / olumsuz rüzgâr | Türkçe kullan |
| Value trap | Değer tuzağı | Türkçe kullan |
| Insider ownership | Yönetim/içeriden hisse sahipliği | Türkçe kullan |
| YBBO (CAGR) | Yıllık Bileşik Büyüme Oranı | Zaten Türkçe |
| TAM / SAM / SOM | Toplam/Hizmetlenebilir/Ulaşılabilir Pazar | İlk kullanımda Türkçe açıklama |
| FCF yield | Serbest nakit akışı getirisi | Türkçe kullan |
| DuPont decomposition | DuPont ayrıştırması | Türkçe fiil kullan |
| Omni-channel | Çok kanallı (omni-channel) | İlk kullanımda parantezle |
| Click-to-brick | Dijitalden fiziksele geçiş | Türkçe kullan |
| ROPO / BORIS | İlk kullanımda Türkçe açıklama zorunlu | Kısaltma + açıklama |

**İlk kullanım kuralı:** Bir terimin İngilizce kısaltması veya çerçeve adı korunacaksa, ilk kullanımda parantez içinde Türkçe açıklama zorunludur. Sonraki kullanımlarda kısaltma tek başına kullanılabilir.

**Örnek:**
- ✅ "Hendek (rekabet avantajı) analizi sonucunda şirketin marka gücü 7/10 olarak değerlendirilmiştir."
- ✅ "FD/FAVÖK 2,86x seviyesinde işlem görmektedir."
- ❌ "Moat analysis shows strong brand power."
- ❌ "Sirketin guidance'i beat edilmistir."

---

## T1 ZORUNLU 2 ASAMA: ONCE TOPLA, SONRA YAZ

> **Ilker'in feedback kurali (2026-03-18):** "Bence soyle yapmalisin; once T1 baslarken sen 'EBEBK_research.md' yazmaya baslamadan once kaynaklari toplarken, bulamadigin ya da erisemedigi kaynaklari bana sormalisin ve ilgili klasor yoluna yuklememi istemelisin. Elindeki senin eristigin kaynaklarla birlikte bunlari sonra hepsini toplu bir sekilde degerlendirmeye alarak research yazmaya baslamalisin yoksa bu sekilde surekli olarak yeniden yeniden rapor yazmakla token yakariz."

### KURAL: research.md DOSYASI YAZILMADAN ONCE TUM KAYNAKLAR TOPLANMIS VE ONAYLANMIS OLMALIDIR.

T1 iki zorunlu asamadan olusur:

```
ASAMA 1: KAYNAK TOPLAMA (research.md YAZILMAZ)
  1. Input Verification Checklist'i doldur
  2. Tum kaynaklari topla (BBB Finans, Drive, IR, web)
  3. Eksik kaynaklari tespit et
  4. Ilker'e eksik listesi sun ve dosyalari research/companies/{TICKER}/ altina yuklemesini iste
  5. Ilker eksikleri tamamlayana kadar BEKLE
  6. Tum kaynaklar hazir -> Ilker'e "Kaynaklar tamam, yazmaya basliyorum" de

ASAMA 2: RAPOR YAZIMI (tek seferde, yeniden yazma YOK)
  7. Yazım Taslak Planı hazırla (bkz. aşağıda)
  8. Toplanan TUM kaynaklari birlikte degerlendirerek research.md'yi yaz
     - HER BOLUM YAZILDIKTAN SONRA o bolumun kelime sayisini kontrol et
     - Hedefin altindaysa HEMEN genislet — sonraki bolume GECMEDEN once
  9. T1 Dogrulama Checklist ile kontrol et
  10. Ilker'e sun
```

**YASAK:** Asama 1 tamamlanmadan Asama 2'ye gecmek. Eksik kaynakla rapor yazip sonra "yeniden yazayim" demek token israf eder.

### Aşama 2 Öncesi: Yazım Taslak Planı (ZORUNLU)

Research.md yazmaya başlamadan ÖNCE, her bölüm için kısa bir yazım planı hazırla. Bu plan token israfını önler ve ilk seferde hedef kelime sayılarını tutturmayı sağlar.

```
## Yazım Taslak Planı — {TICKER}

### Ön Sentez Hipotezi (ZORUNLU)
**Ç1 varsa:** `research/companies/{TICKER}/fikirler/{TICKER}_fikir_*.md` dosyasını oku. Ç1'deki "Ön Tez" hipotezini, kill criteria'yı ve "T1'in cevaplaması gereken 3 soru"yu başlangıç noktası olarak al. Hipotez aşağıda genişletilecek; T1 sorularını Aşama 2'deki bölüm planlarına eşle.

**Ç1 yoksa (doğrudan T1 başlıyorsa):**
**Bu şirketin hikayesi 3 kelimeyle ne?** + **Neden yatırım yapılır veya yapılmaz? (1 cümle)**
> [Aşama 1'de okunan kaynaklar ışığında ilk hipotez. Değişebilir — amaç doğru olmak değil, düşünmeye başlamak. T1 sonundaki Çıkış Gate'inde bu hipotez nihai haliyle Sentez Notu'na yazılacak.]

Bu hipotez 9 bölüm boyunca test edilecek. Her bölüm sonunda 1 cümleyle geri dön:
"Bu bölüm hipotezimi destekliyor / zayıflatıyor, çünkü [neden]."

| Bölüm | Kelime Hedefi | Ana Kaynaklar | Anahtar Veri Noktaları |
|-------|--------------|---------------|----------------------|
| 1. Yönetici Özeti | 400-500 | Tüm bölümlerin özeti | QV matrisi, tez taslağı, 5 metrik |
| 2. Şirket Profili | 700-1.000 | Faaliyet raporu, IR | Tarihçe, iş modeli, ölçek |
| 3. Ürün Portfolyosu | 700-1.000 | Faaliyet raporu, sunum | Kategoriler, kanal kırılımı |
| 4. Yönetim Analizi | 700-1.000 | §3A kaynakları | CEO, CFO, ortaklık, karneö |
| 5. Sektör Analizi | 1.000-1.200 | Sektör raporları, kurum raporları | TAM/SAM, Porter, büyüme |
| 6. Hendek Analizi | 600-800 | T1 diğer bölümler | 4 hendek türü, skor |
| 7. Finansal Derinlemesine | 1.000-1.200 | İş Yatırım, kurum raporları | 5Y trend, bilanço, nakit |
| 8. Rekabet Pozisyonlaması | 500-700 | Kurum raporları, sektör | Pazar payı, rakipler |
| 9. Riskler ve Fırsatlar | 500-800 | Tüm bölümler | 5R, 5F, 2 çöküş kriteri |
```

Bu tabloyu Aşama 1 sonunda (kaynak durumu raporu ile birlikte veya hemen sonrasında) hazırla. İlker'e sunmak zorunlu değil — kendi yazım rehberin olarak kullan.

### Bölüm Bazlı Ara Kontrol (ZORUNLU)

Research.md yazarken her bölümü tamamladıktan sonra:
1. O bölümün kelime sayısını hesapla
2. Kelime hedefinin altındaysa → hemen genişlet, sonraki bölüme geçme
3. Kelime hedefinin üstündeyse → içerik yoğun ve gerekliyse kabul et, gereksiz tekrar varsa kısalt
4. **Hipotez kontrolü:** Bu bölüm Ön Sentez Hipotezi'ni destekliyor mu, zayıflatıyor mu? (1 cümle, bölüm sonuna yaz. Zayıflatıyorsa hipotezi revize et veya çelişkiyi not al.)
5. Tüm bölümler yazıldıktan sonra toplam kontrolü yap (6.000-8.000)

**ASLA "sonra düzeltirim" deme.** Her bölüm yazıldığı anda hedefi karşılamalı.

### Asama 1: Kaynak Toplama Checklist

T1'e baslamadan once bu kontrolleri yap:

- [ ] Ticker/sirket adi belirlenmis
- [ ] BBB Finans erisimi test edilmis (`bbb_kap.py {TICKER} --lookup`)
- [ ] **KAP Bildirimleri taranmış** — `bbb_kap.py {TICKER} --all --last 6m` ile tam liste çekilmiş, KAP Bildirim Seçim Protokolü (§3A-0, ADIM A/B/C) uygulanmış, seçili bildirimler `--archive --ids` ile indirilmiş
- [ ] `research/companies/{TICKER}/` klasoru olusturulmus
- [ ] Sirketin BIST mi yoksa yurt disi mi oldugu belirlenmis
- [ ] **DONEM KONTROLU:** Hangi ceyreklik donemde oldugumuzu belirle. En son aciklanan bilanco donemi hangisi? Tum kaynaklar bu doneme gore mi? (bkz. Donem Guncellik Kurali asagida)
- [ ] KAP faaliyet raporu erisilebilir mi? (segment verisi icin kritik)
- [ ] **KAP Finansal Tablolar PDF** erisilebilir mi? (dipnot dogrulama icin: efektif faiz, vergi tesviki, tek seferlik kalemler, doviz pozisyonu)
- [ ] **En guncel yatirimci sunumu** erisilebildi mi? Eger bulunamazsa veya eski donemse, Ilker'den dosya iste.
- [ ] Sirket IR sayfasi URL'si biliniyor mu?
- [ ] Drive'da kurum raporlari var mi? (`find "$DRIVE_KURUM" -iname "*{TICKER}*"`)
- [ ] PDF'ler okunabilir mi? (pdftotext + gorsel agirlik tespiti + gerekirse image tool ile grafik okuma)
- [ ] **EKSIK KAYNAK LISTESI** hazirlandi mi? (asagidaki formata bak)

### Asama 1 Ciktisi: Ilker'e Sunulacak Kaynak Durumu Raporu

Tum kaynaklar tarandi, okunabilenler okundu. Asama 2'ye gecmeden once Ilker'e su formatta rapor sun:

```
## EBEBK T1 - Kaynak Durumu

### Erisilen Kaynaklar (hazir)
1. Is Yatirim finansal verileri (FY2023-2025, IAS 29) - OK
2. Marbas Menkul sirket raporu (13.03.2026) - OK, okundu
3. Deniz Yatirim 4C25 raporu (20.02.2026) - OK, okundu
4. BBB Finans --summary - OK

### Erisilemedi / Eksik (Ilker'den bekleniyor)
5. FY2025 faaliyet raporu - KAP'tan indiremedim, Drive'da yok
   -> Lutfen research/companies/EBEBK/ altina yukle
6. 4C25 yatirimci sunumu - IR sayfasinda bulamadim
   -> Varsa research/companies/EBEBK/ altina yukle
7. Pusula 4C25 raporu - Drive cloud-only, indiremedim
8. KAP Finansal Tablolar PDF (FY2025 bagimsiz denetim raporu dahil)
   -> T2'de dipnot dogrulama icin gerekli (efektif faiz, vergi tesviki, gider kirilimi)
   -> Lutfen research/companies/EBEBK/ altina yukle veya Drive sync et

### Senin Eklemek Istedigin Kaynak Var Mi?
Yukaridaki liste disinda bildigin veya paylasmaak istedigin ek kaynak
(kurum raporu, haber, roportaj, internal not, sektor raporu vb.) varsa
research/companies/{TICKER}/ altina yukleyebilirsin.

### Karar
Eksik kaynaklar tamamlaninca rapor yazimina baslarim.
Yoksa eksiklerle devam edeyim mi?
```

**Ilker'in cevabina gore:**
- "Yukledim" -> Dosyalari oku, Asama 2'ye gec
- "Bulamadim / atlayalim" -> Eksikleri `[KAYNAK EKSIK]` olarak isaretle, Asama 2'ye gec
- "Bekle" -> Bekle

### DONEM GUNCELLIK KURALI (ZORUNLU)

> **Ilker'in geribildirim kurali (2026-03-18):** "Su anda biz 4C25 donemindeyiz, sen neden 1C25 sunum dosyasini ana kaynak gibi kullandin? Neden hangi donemde oldugumizi daha duzgun bicimde kontrol ederek en guncel doneme ait sunum dosyalarina erismiye calismiyorsun?"

**Kural:** T1 baslarken ilk is olarak su soruyu cevapla: "Su an hangi ceyreklik doneme ait finansallar aciklanmis durumda?"

| Kontrol | Nasil |
|---------|-------|
| Son aciklanan bilanço donemi | `bbb_financials.py {TICKER} --summary` calistir, "Son donem" satirini oku |
| En guncel yatirimci sunumu | Sirket IR sayfasinda ara, Fintables'ta ara, `web_search "{sirket} investor presentation {yil}"` |
| KAP Finansal Tablolar PDF | KAP bildirimler veya Ilker'den iste. `research/companies/{TICKER}/` altina kaydet |
| En guncel kurum raporlari | Drive'da dosya tarihlerini kontrol et, Paratic/RotaBorsa'da son hedef fiyat haberlerini ara |

**Eger en guncel donem sunumu/raporu bulunamazsa:** Ilker'den ISTE. Eski donem kaynagiyla rapor yazmaktansa eksigi belirt ve Ilker'den dosya talep et.

**ASLA eski donem sunumunu birincil kaynak olarak kullanma.** Eski sunumlar sadece tarihsel referans ve guidance karsilastirmasi icin gecerlidir.

### FINANSAL VERI KAYNAK KURALI (ZORUNLU)

> **Ilker'in geribildirim kurali (2026-03-18):** "Finansal verilerde neden KAP kullandin orada enflasyon muhasebesi bulunmuyor. Analiz tablolarimizda mutlaka Is Yatirim ile sirketin finansal verilerini almaliyiz."

**Kural:** Analiz icindeki tum finansal rakamlar **bbb_financials.py** (Is Yatirim, IAS 29 duzeltmeli) uzerinden cekilir. `bbb_kap.py --kap-summary` SADECE hizli tarama (quick scan) ve donem kontrolu icindir, analiz tablolarinda birincil kaynak DEGILDIR.

| Arac | Kullanim | Birincil mi? |
|------|----------|-------------|
| `bbb_financials.py --summary` | Ozet kart, carpanlar, marjlar | EVET -- analiz tablosu |
| `bbb_financials.py --section all --full` | 147+ kalem detayli finansal | EVET -- analiz tablosu |
| `bbb_kap.py --kap-summary` | Hizli tarama, donem kontrolu | HAYIR -- sadece quick scan |
| KAP web sitesi (web_fetch) | KULLANMA (Cloudflare engeli) | HAYIR |

### KURUM RAPORU GUNCELLIK KURALI

> **Ilker'in geribildirim kurali (2026-03-18):** "Rapor hangi tarihli? Neden eger guncel degilse daha guncel raporlar zorlamadik?"

**Kural:** Her kurum raporunun tarihini belirle. Birden fazla rapor varsa en gunceli birincil kaynak olur. Eski raporlar tarihsel referans olarak kullanilir.

- Rapor tarihini belirlemek icin: Drive dosya tarihi + rapor ici tarih + Paratic/RotaBorsa haberleri
- `web_search "{sirket} {TICKER} hedef fiyat {yil}" site:paratic.com OR site:rotaborsa.com` ile en guncel kurum goruslerini tara
- Eger Drive'daki rapor tarihi belirsizse, raporu acip icerideki tarihi kontrol et

**Herhangi biri basarisizsa:** Asama 1 Ciktisi formatinda Ilker'e sun, eksik kaynaklari `research/companies/{TICKER}/` altina yuklemesini iste, cevabini bekle. research.md YAZMA.

### KURUM RAPORU KULLANIM CERCEVESI

> **Ilker'in geribildirim kurali (2026-03-21):** "Kurum raporlarini kesinlikle dogru ya da yol gosterici olarak kabul etmemeliyiz. Sadece gozumuzden kacan bilgiler, farkli bakis acisi, ileriye yonelik beklentiler icin kontrol mekanizmasi."

**Temel Ilke:** Kurum raporlari **birincil kaynak degil, kontrol mekanizmasidir.** Bizim ozgun arastirmamiz icin girdi degil, dogrulama aracidir.

**Gecerli Kullanim Alanlari (3 sinirli alan):**

| Alan | Ornek | Nasil Kullanilir |
|------|-------|-----------------|
| 1. Gozden kacan veri tespiti | Bizim okumedigimiz dipnot, farketmedigimiz operasyonel detay | "Deniz Yatirim raporunda belirtilen X verisini birincil kaynaktan dogruladik" |
| 2. Farkli bakis acisi | Ayni veriye farkli yorumlama, bizim dusunmedigimiz risk/firsat | "Bu risk faktorunu bagimsiz olarak degerlendirdik, katiliyoruz/katilmiyoruz cunku..." |
| 3. Piyasa beklentisi referansi | Konsensus tahminler, hedef fiyat araligi | "Piyasa X fiyatliyor, bizim gorusumuz Y cunku..." -- fark analizi olarak |

**YASAK Kullanimlar:**

- Hedef fiyatlarini benimsemek veya "referans almak"
- Varsayimlarini kopyalamak (buyume orani, marj tahmini vb.)
- "X kurumu da boyle diyor" seklinde otorite olarak gostermek
- Kurum raporundaki degerleme modelini temel almak
- Tavsiye yonunu (AL/TUT/SAT) etkilenmek icin okumak

**Rapor Yaziminda Kural:** Kurum raporlarindan alinan herhangi bir bilgi mutlaka birincil kaynaktan (faaliyet raporu, finansal tablolar, KAP bildirimi, yatirimci sunumu) dogrulanmalidir. Dogrulanamayan veri rapora GIREMEZ. Kurum raporu tek basina kaynak gosterilemez.

### Veri Toplama Araçları — Hızlı Referans

```bash
# ── BBB Finans (KAP/İş Yatırım) — MUTLAK ──
cd ~/.openclaw/workspace/skills/bbb-finans/scripts
python3 bbb_financials.py {TICKER} --summary                               # Özet kart
python3 bbb_kap.py {TICKER} --kap-summary                                  # KAP özet
python3 bbb_kap.py {TICKER} --lookup                                        # Şirket bilgisi

# ── Drive Kurum Raporları (PDF) ──
DRIVE_KURUM="/Users/ilkerbasaran/Library/CloudStorage/GoogleDrive-ilker@borsadabibasina.com/Drive'ım/Drive'ım/borsadabibasina.com/#5 - Kurum Raporları"
find "$DRIVE_KURUM" -iname "*{TICKER}*" 2>/dev/null

# ── Yerel PDF Okuma (3 Katmanli Protokol) ──
# Katman 1: pdftotext ile metin/tablo cikarma
pdftotext "research/companies/{TICKER}/{dosya}.pdf" /tmp/{TICKER}_rapor.txt
# Veya PyMuPDF: import fitz; doc = fitz.open(path); page.get_text()

# Katman 2: Gorsel agirlikli sayfa tespiti (PyMuPDF)
# <200 karakter + gorsel var VEYA >10 gorsel = grafik sayfasi
# python3 -c "import fitz; ..." (detay SKILL.md'de)

# Katman 3: Grafik sayfalari PNG'ye render + image tool ile okuma
# PyMuPDF page.get_pixmap(dpi=150) -> workspace-kaya/temp/ altina kaydet
# image tool ile "tum sayisal verileri cikar" promptu

# ── Online PDF (kurum raporu / IR sunumu) ──
summarize "https://example.com/rapor.pdf" --extract > /tmp/{TICKER}_online.txt
# Ozetleme gerekirse: summarize URL --model google/gemini-2.5-flash

# ⚠️ GDrive Warm Cache: Ilk erisimde timeout alirsa:
# cat "$DRIVE_KURUM/{Dosya}.pdf" > /dev/null 2>&1; sleep 30; sonra tekrar dene

# ⚠️ summarize --extract yerel PDF desteklemiyor! Yerel dosyalar icin pdftotext/PyMuPDF kullan.
```

### Erişilemeyen Kaynaklar İçin Protokol

| Sorun | Çözüm |
|-------|-------|
| IR sayfası Cloudflare engelliyor | `web_search` ile alternatif kaynak + İlker'den dosya iste |
| KAP faaliyet raporu PDF'i yok | İlker'den `research/companies/{TICKER}/` altına kaydetmesini iste |
| Drive PDF timeout | Warm cache yap (`cat > /dev/null` + `sleep 30`) + tekrar dene |
| Drive dosya sync olmamış | İlker'den Drive sync kontrolü iste |
| Kurum raporu online ama binary PDF | `summarize "{URL}" --extract` kullan (`web_fetch` PDF parse edemez) |
| Yerel PDF gorsel agirlikli (grafik/chart) | pdftotext + PyMuPDF gorsel tespit + image tool ile grafik okuma (3 katmanli protokol, detay SKILL.md'de) |

---

## 9 Bölüm — Kelime Aralıkları ve Zorunlu İçerik

### Toplam Hedef: 6.000-8.000 kelime

| # | Bölüm | Kelime | Zorunlu İçerik |
|---|-------|--------|----------------|
| 1 | Yönetici Özeti | 400-500 | Şirket ne yapar, neden ilgi çekici, tez taslağı, Kalite-Değer matrisi |
| 2 | Şirket Profili | 700-1.000 | Tarihçe, iş modeli, operasyonel ölçek, çalışanlar, coğrafi varlık |
| 3 | Ürün/Hizmet Portföyü | 700-1.000 | Ürün kategorileri, öz marka stratejisi, kanal kırılımı, yıllık seyir |
| 4 | Yönetim Analizi | 700-1.000 | CEO (150-200 kel), CFO (100-150 kel), 1-2 kilit yönetici (her biri 75-100 kel), ortaklık yapısı, Yönetim Kalitesi Karnesi |
| 5 | Sektör Analizi | 1.000-1.200 | TAM/SAM, Porter Beş Güç Analizi, düzenleyici ortam, büyüme sürücüleri |
| 6 | Hendek Analizi | 600-800 | 4 hendek türü değerlendirmesi, gücü (0-10), barometresi |
| 7 | Finansal Derinlemesine | 1.000-1.200 | 5Y trend, 6 metrik tablosu, ROIC dinamikleri, bilanço sağlığı |
| 8 | Rekabet Pozisyonlaması | 500-700 | Pazar payı, rakip tablosu (min 4-5), stratejik avantajlar |
| 9 | Riskler ve Fırsatlar | 500-800 | 5 risk, 5 fırsat, tez çöküş kriterleri (min 2) |
| | **TOPLAM** | **6.700-9.200** | Alt sınır toplamı ~6.700, hedef band: 6.000-8.000 |

**Not:** Bölüm kelime aralıkları EBEBK T1 deneyimine göre güncellenmiştir (v4.2, 2026-03-20). Yönetim analizi, şirket profili ve ürün portfolyosu bölümleri pratikte daha fazla alan gerektirmektedir.

---

## Bölüm Detayları

### 1. Yönetici Özeti (400-500 kelime)

**Amaç:** Okuyucu 2 dakikada şirketin ne olduğunu ve neden analiz ettiğimizi anlamalı.

**Zorunlu içerik:**
- Şirket tek cümle tanımı (ne yapıyor, hangi sektör, nerede)
- Ölçek göstergeleri (gelir, çalışan, pazar payı)
- Quality Value matrisi pozisyonu: Ucuz+Hendekli / Pahalı+Hendekli / Ucuz+Hendeksiz / Pahalı+Hendeksiz
- İlk tez taslağı (2-3 cümle — neden bu şirketi analiz ediyoruz?)
- 3-5 temel metrik (gelir, FAVÖK marjı, ROIC, EV/FAVÖK, net borç)
- **Ters İNA Özeti (zorunlu):** "Piyasa ne fiyatlıyor?" — 2-3 cümle (detay Bölüm 1B'de)

**Yazma:** İlker'in DNA'sında metafor veya çarpıcı veri noktasıyla açılış. "X dünyada Y yapan Z şirketi" formülü.

**Kaynak:** KAP, BBB Finans, şirket web sitesi

**Yazma / yazmama:**
- ✅ Net, özlü, sayısal → "Yıllık 8.5 milyar TL gelir, %18 FAVÖK marjı"
- ❌ Genel övgü → "Türkiye'nin lider şirketlerinden biri"

---

### 1B. Ters İNA ve Varyant Algısı Çerçevesi (ZORUNLU)

> **Amaç:** T1'in en başında "piyasa ne fiyatlıyor?" sorusunu somut olarak cevapla. Bu, tüm analizin çerçevesini belirler. Ters İNA olmadan yazılan analiz "havada uçan değerleme" riski taşır.
> **Not:** Bu analiz T3'te detaylı yapılacak — T1'de kaba hesaplama yeterli. Amaç kesin değerleme değil, yönlendirme.

**ADIM 1: Piyasa Ne Fiyatlıyor? (Ters İNA — Kaba Hesaplama)**

```
Mevcut Fiyat → Piyasa Değeri → Firma Değeri (FD)
FD = Piyasa Değeri + Net Borç

Zımni FAVÖK Büyüme = (FD / Mevcut FAVÖK) çarpanı → peer çarpanıyla karşılaştır
Zımni FCF Getirisi = Mevcut FCF / Piyasa Değeri
```

Daha detaylı hesaplama gerekiyorsa (T3 girdisi):
```
Mevcut fiyattan geriye çalış:
  FD → TV → Zımni terminal büyüme + zımni FAVÖK marjı
  "Piyasa %X büyüme ve %Y FAVÖK marjı fiyatlıyor"
```

**Kaynak:** BBB Finans (`bbb_financials.py --summary`), mevcut hisse fiyatı

**ADIM 2: Bu Varsayımlar Makul mü? (Varyant Algısı)**

Ters İNA'dan çıkan zımni varsayımları karşılaştır:

```markdown
### Varyant Algısı Tablosu — {TICKER}

| Zımni Varsayım | Piyasa Fiyatlıyor | Tarihsel Gerçekleşme | Sektör Ort. | Yönetim Guidance | Bizim İlk Görüş |
|----------------|-------------------|---------------------|-------------|-----------------|-----------------|
| Gelir CAGR     | %X (zımni)        | %Y (son 3Y)         | %Z          | %W              | ✅/⚠️/❌ + 1 cümle |
| FAVÖK Marjı    | %X (zımni)        | %Y (son 3Y ort.)    | %Z          | %W              | ✅/⚠️/❌ + 1 cümle |
| Terminal Büyüme | %X (zımni)       | Reel GDP: %A        | —           | —               | ✅/⚠️/❌ + 1 cümle |
```

**3 olası sonuç:**

| Sonuç | Anlam | Raporlama |
|-------|-------|-----------|
| **(a) Katılıyoruz** | Piyasa fiyatlaması makul | "Adil değerlenmiş; şu 2-3 katalizör/risk izlenmeli" |
| **(b) Spesifik bir noktada farklıyız** | Belirli bir varsayımda ayrışma | "Piyasa X fiyatlıyor ama biz Y görüyoruz çünkü [kanıt]" |
| **(c) Belirsizlik yüksek** | Geniş aralık, koşullu | "Değerleme aralığı çok geniş, koşullu pozisyon" |

**⚠️ Contrarian Bias Uyarısı:** Bu çerçeve analizin her zaman piyasadan farklı düşünmesini ZORLAMAZ. Piyasa haklıysa "haklı" demek de geçerli bir sonuçtur. Önemli olan hangi spesifik varsayımda ayrıştığını veya ayrışmadığını netleştirmektir. "Her şeyde farklı düşünüyoruz" tuzağına düşme.

**ADIM 3: Bizi Ne Yanıltabilir?**

Bu adım her 3 sonuç için de ZORUNLU:
- **(a) Katılıyorsak:** "Bu konsensüsü ne bozabilir?" → Downside katalizörler
- **(b) Farklıysak:** "Eğer X olursa tezimiz çöker" → Kill criteria ile bağlantılı (Bölüm 9)
- **(c) Belirsizse:** "Hangi veri noktası belirsizliği çözecek?" → Takip listesi

**Çıktı:** Yönetici Özeti'nin son paragrafında 2-3 cümle + Bölüm 9'da detaylı kill criteria bağlantısı.

---

### 2. Şirket Profili (700-1.000 kelime)

**Amaç:** Şirketi bilmeyen biri okuyunca temel resmi görmeli — ne yapar, nasıl para kazanır, ne kadar büyük.

**Zorunlu içerik:**
- **Tarihçe (200-300 kel):** Kuruluş, milestones, M&A geçmişi, stratejik pivotlar
- **İş modeli ve gelir yapısı (100-200 kel):** Nasıl para kazanıyor, B2C/B2B, abonelik/tek seferlik
- **Operasyonel ölçek (100-200 kel):** Çalışan sayısı, fabrika/mağaza/şube, kapasite, coğrafi varlık
- **Temel finansal ölçek (50-100 kel):** Gelir, çalışan, pazar payı — "büyüklüğü hisset" verileri

**Kaynak hiyerarşisi:**
1. KAP faaliyet raporu (birincil)
2. Şirket IR sayfası / yatırımcı sunumu
3. Şirket web sitesi (About sayfası)
4. Web araştırma (cross-check)

---

### 3. Ürün/Hizmet Portföyü (700-1.000 kelime)

**Amaç:** Şirketin ne sattığını, kime sattığını ve gelirin nereden geldiğini detaylıca anla.

**Zorunlu içerik:**
- **Ana ürün/hizmet kategorileri (200-300 kel):** Her kategori ne yapar, fiyatlama modeli
- **Gelir segmentasyonu (150-200 kel):** Segment × coğrafya kırılımı (faaliyet raporundan)
- **Kanal kırılımı (100-150 kel):** Fiziksel/online, perakende/toptan, yurtiçi/ihracat
- **Ürün yaşam döngüsü (50-100 kel):** Olgunlaşan vs büyüyen segmentler

**Kaynak hiyerarşisi:**
1. KAP faaliyet raporu — segment gelir kırılımı (birincil)
2. Şirket IR sayfası / yatırımcı sunumu — ürün portföyü detayı
3. Şirket web sitesi (Products sayfaları)
4. Web araştırma (cross-check)

**Segment verisi bulunamazsa:** `[SEGMENT KAP FAAlİYET RAPORUNDAN ALINACAK]` etiketi ile devam et. Tahmini segment kırılımı YAPMA.

---

### 4. Yönetim Analizi (700-1.000 kelime)

**Amaç:** "Bu şirketi kim yönetiyor ve güvenebilir miyiz?" — sadece profil değil, kalite değerlendirmesi.

**Zorunlu içerik (per-exec minimum kelime aralığı):**
- **CEO profili (150-200 kel):** Görev süresi, önceki pozisyonlar, track record, sermaye tahsisi karnesi
- **CFO profili (100-150 kel):** Finansal disiplin geçmişi, sermaye tahsisi kalitesi, yatırımcı ilişkileri
- **1-2 kilit yönetici (her biri 75-100 kel):** Sektör deneyimi, katkıları
- **Ortaklık yapısı (75-100 kel):** Ana ortak (%), halka açıklık, insider ownership
- **Management Quality Scorecard (aşağıda):** 6 kriter, her biri 0-5, toplam skor

**T5 (Rapor Assembly) İçin Biyografi Standardı:**

| Standart | Hedef | Veri Kısıtlı ise |
|----------|-------|------------------|
| CEO | 300-400 kelime | 150-200 kelime (minimum) |
| CFO | 200-300 kelime | 100-150 kelime (minimum) |
| Kilit yönetici (1-2) | 150-200 kelime (her biri) | 75-100 kelime (her biri) |
| **Toplam** | **800-1.200 kelime** | **400-600 kelime** |

**Türkiye-Spesifik Kaynak Listesi (biyografi için):**

| Öncelik | Kaynak | Ne İçerir | Erişim |
|---------|--------|-----------|--------|
| 1 | KAP faaliyet raporu | Yönetim bölümü, ortaklık yapısı, yönetim kurulu listesi | KAP bildirimi |
| 2 | Şirket IR sayfası | Yönetim profilleri, fotoğraflar, görev tanımları | Web |
| 3 | KAP özel durum açıklamaları | Atama/görevden ayrılma bildirimleri | KAP |
| 4 | LinkedIn | Kariyer geçmişi, eğitim, önceki pozisyonlar | Web |
| 5 | Basın/röportajlar | CEO/CFO'nun stratejik görüşleri, kriz yönetimi | web_search |
| 6 | Konferans çağrısı | Yönetim tonu, guidance dili, soru-cevap | Transkript |
| 7 | YouTube | CEO röportajları, panel katılımları | web_search |

**"Veri kısıtlı" durumlar:**
- Türkiye'de birçok şirketin IR sayfasında detaylı yönetim biyografisi YOKTUR
- KAP faaliyet raporunda genellikle isim + görev süresi + kısa özet bulunur
- LinkedIn profilleri Türkçe olabilir ve kısıtlı olabilir
- **Veri bulunamadığında:** Mevcut bilgilerle yazılır + "Detaylı biyografi kamuya açık değil" notu eklenir
- **CEO değişikliği varsa:** Ayrılan CEO'nun notu + yeni atama durumu/beklentisi yazılır

**Yönetim hisse sahipliği kontrolü:** Yönetim sahiplik oranı <%1 → UYAR.

**Kaynak hiyerarşisi (genel):**
1. **KAP faaliyet raporu** — yönetim bölümü, ortaklık yapısı, sermaye tahsisi tablosu
2. **Şirket IR sayfası** — yönetim kurulu profilleri, yatırımcı sunumları
3. **KAP bağımsız denetim raporu** — ilişkili taraf işlemleri bölümü (kritik)
4. **Konferans çağrısı / analist toplantısı** — yönetim tonu, guidance dili, soru-cevap dinamikleri (bkz. `turkiye-spesifik-rehber.md §5`)
5. **YouTube / basın röportajları** — CEO/CFO'nun kendi ağzından strateji, öncelikler, kriz yönetimi
6. **Haber arşivi** (web_search: "{CEO adı} röportaj", "{şirket} yönetim kararı") — M&A, kriz, değişim haberleri
7. **LinkedIn** (cross-check: kariyer geçmişi)

#### 3A. Zorunlu Yönetim Kaynak Tarama Adımı

> **⚠️ KAYNAK ONCELIK KURALI:** Yonetim bilgisi (ortaklik yapisi, yonetim kurulu, CEO/CFO biyografileri) icin ONCE eldeki dosyalari kullan:
> 1. **Faaliyet raporu** (ortaklik yapisi, yonetim mektubu, biyografiler, strateji bolumu)
> 2. **Yatirimci sunumu** (ust yonetim, KPI'lar, guidance)
> 3. **bbb_kap.py --profile** (KAP sirket bilgisi)
> 4. **Kurum raporlari** (analist toplanti notlari, yonetim degerlendirmesi)
>
> Web aramasini (YouTube, basin, haber siteleri) SADECE yukaridaki kaynaklarda bulunamayan bilgiler icin kullan (CEO roportajlari, basin aciklamalari, kriz yonetimi ornekleri vb.).
> KAP verisi icin web_fetch/web_search DEGIL, bbb_kap.py kullan. KAP web sitesine dogrudan erisim Cloudflare engeli nedeniyle calismaz.

T1 Bölüm 4 (Yönetim Analizi) yazılmadan önce aşağıdaki kaynakların **tamamı** taranmalıdır. Bulunamayan kaynaklar "Eksik" olarak işaretlenir — ama arama YAPILMIŞ olmalıdır.

**Adım 3A-0: KAP Bildirimleri Tarama (ZORUNLU — İLK ADIM)**

KAP bildirimleri en güncel bilgi kaynağıdır. CEO/CFO ataması, görevden ayrılma, ortaklık değişiklikleri, temettü kararları gibi kritik gelişmeler burada anlık olarak yayınlanır. Faaliyet raporu aylar gecikmeli çıkar — KAP bildirimleri aynı gün çıkar.

```bash
cd ~/.openclaw/workspace/skills/bbb-finans/scripts

# ═══════════════════════════════════════════════════════════════
# İKİ AŞAMALI AKILLI ARŞİVLEME (ÖNERİLEN YÖNTEM)
# ═══════════════════════════════════════════════════════════════
# Adım 1: Tüm bildirimleri listele — sadece başlıkları gör, hiçbir şey indirme
python3 bbb_kap.py {TICKER} --all --last 6m

# Adım 2: Listeyi oku, araştırma bağlamına göre ilgili bildirimleri SEÇ
#   - Faaliyet raporu, finansal tablolar (FR)
#   - Önemli ÖDA'lar: M&A, strateji değişikliği, önemli sözleşme (ODA)
#   - Yönetim değişiklikleri (YON)
#   - Temettü kararları (TEM)
#   → Rutin/tekrarlayan bildirimleri ATLA (şirket genel bilgi formu güncellemeleri,
#     sürdürülebilirlik uyum raporları, standart defter tutma vb.)

# Adım 3: Sadece seçili bildirimleri indir
python3 bbb_kap.py {TICKER} --archive --ids 1560680,1561522,1564039 --last 6m
# Bu komut:
# - Yalnızca belirtilen ID'lerin PDF/metin dosyalarını indirir
# - Kategori filtresi uygulamaz (AI zaten seçim yapmıştır)
# - companies/{TICKER}/kap_docs/ altında index.md oluşturur

# ═══════════════════════════════════════════════════════════════
# ALTERNATİF: Kör toplu arşivleme (tüm ilgili kategoriler)
# ═══════════════════════════════════════════════════════════════
python3 bbb_kap.py {TICKER} --archive --last 6m
# Tüm ODA, FR, GK, TEM, SA, YON, DG kategorilerini indirir.
# Çok fazla gereksiz dosya üretebilir — akıllı mod tercih edilmeli.

# TEK TEK TARAMA:
python3 bbb_kap.py {TICKER} --last 6m                    # Son 6 ay tüm bildirimler
python3 bbb_kap.py {TICKER} --all                         # Tüm bildirimler (150+)
python3 bbb_kap.py {TICKER} --last 6m --category ODA      # Sadece ÖDA'lar
python3 bbb_kap.py {TICKER} --last 6m --category YON      # Yönetim değişiklikleri
python3 bbb_kap.py {TICKER} --last 6m --category ORT      # Ortaklık değişiklikleri
python3 bbb_kap.py {TICKER} --last 6m --category TEM      # Temettü kararları
python3 bbb_kap.py {TICKER} --id {bildirim_id}            # Bildirim detayı + ek dosyalar
```

**ARŞİV KLASÖR YAPISI:** `--archive` komutu sonrası `workspace-kaya/research/companies/{TICKER}/kap_docs/` altında:
- Metin bildirimleri: `2026-03-02_oda_ozel-durum-aciklamasi_1564039.txt`
- Ek dosyalı bildirimler: `2026-02-23_fr_faaliyet-raporu_1560680/` alt klasörü (bildirim.txt + PDF'ler)
- `index.md`: Tüm bildirimlerin tarih/kategori/başlık/dosya tablosu

**KAP BİLDİRİM SEÇİM PROTOKOLÜ (ZORUNLU)**

Bu protokol `--all` çıktısını değerlendirirken uygulanmalıdır. Kör toplu arşivleme (`--archive` idsiz) KULLANILMAMALIDIR.

**ADIM A — Otomatik İNDİR (sorgusuz, her zaman):**
- Faaliyet Raporu (FR) — her dönem
- Finansal Rapor / Finansal Tablo (FR) — her dönem
- Analist Toplantısı Sunumu — her dönem
- Bilgilendirme Notu (finansallara ilişkin) — her dönem
- Kar Payı Dağıtım Bildirimi
- Genel Kurul İşlemleri
- Üst Yönetim Değişikliği / YK Üyesi Değişikliği
- Bağlı Ortaklık Pay Devri / stratejik ortaklık kararı
- Uluslararası genişleme (yeni pazar, yeni mağaza anlaşması)
- Bağımsız Denetim Kuruluşu Belirlenmesi
- İhraç tavanı (şirketin KENDİ ihracı — borçlanma kapasitesi)
- Sermaye artırımı kararları (SA)

**ADIM B — Otomatik ATLA (sorgusuz, her zaman):**
- Devre Kesici / Pay Bazında Devre Kesici Bildirimi (Borsa İstanbul teknik)
- Pay Alım Satım Bildirimi (MKK/KAP platformu bildirimi)
- Hak Kullanımı / BISTECH Duyurusu (Borsa İstanbul teknik)
- Endeks Şirketlerinde Değişiklik (Borsa İstanbul teknik)
- Sürdürülebilirlik Uyum Raporu (boilerplate)
- Kurumsal Yönetim Uyum Raporu (boilerplate)
- Katılım Finansı İlkeleri Bilgi Formu (standart düzenleyici)
- Finansal Takvim (sadece tarih bilgisi)
- Bağlı ortaklık rutin kira sertifikası itfa/ihraç işlemleri (Değer Varlık Kiralama vb.)

**ADIM C — Koşullu Değerlendir (AI judgment gerektirir):**

1. **Aylık operasyonel veri** (mağaza sayısı, satış adedi, ziyaretçi sayısı):
   - Son analist sunumunun kapsadığı dönemden SONRAKİ aylar → İNDİR (henüz başka kaynakta yok)
   - Önceki aylar → ATLA (analist sunumunda zaten mevcut)
   - Örnek: 4Ç analist sunumu Şubat'ta yayınlandıysa Ekim-Aralık verileri sunumda var, ama Ocak-Şubat verileri yeni → indir

2. **Şirket Genel Bilgi Formu (DG):**
   - YK/yönetim değişikliği bildirimi ARDINDAN gelen güncelleme → İNDİR (değişikliğin yansıması)
   - Tarihsel olarak tek başına gelen rutin güncelleme → ATLA

3. **Yeni İş İlişkisi (başka şirketin bildirimi olsa bile):**
   - Araştırılan şirketle ilgili müşteri/tedarikçi/partner ilişkisi → İNDİR
   - Tamamen ilgisiz → ATLA

4. **İhraç Tavanı:**
   - Şirketin kendi ihracı → İNDİR (borçlanma kapasitesi bilgisi)
   - Bağlı ortaklığın rutin kira sertifikası → ATLA

5. **Diğer ODA bildirimleri:**
   - Başlık/özetinde stratejik karar, M&A, dava, soruşturma varsa → İNDİR
   - Rutin düzenleyici uyum bildirimi → ATLA

**ÖNEMLİ UYARILAR:**
- KAP'ta yönetim değişiklikleri her zaman ayrı YON kategorisinde yayınlanmaz — çoğu zaman "Şirket Genel Bilgi Formu" güncellemesi olarak gelir
- Başka şirketlerin bildirimleri listede görünebilir (bağlı ortaklıklar, iş ortakları) — bunları başlığa göre değerlendir, otomatik atlama
- Emin olamadığında `--id` ile detayını oku, sonra `--ids` ile seçici indir

**Adım 3A-1: Faaliyet Raporu (ZORUNLU)**
```bash
# KAP faaliyet raporu — segment, yönetim mektubu, strateji, ilişkili taraf
# Drive'da varsa:
DRIVE_KURUM="/Users/ilkerbasaran/Library/CloudStorage/GoogleDrive-ilker@borsadabibasina.com/Drive'ım/Drive'ım/borsadabibasina.com/#5 - Kurum Raporları"
find "$DRIVE_KURUM" -iname "*{TICKER}*faaliyet*" 2>/dev/null

# KAP'tan doğrudan ulaşılamıyorsa (Cloudflare) → İlker'den iste
# Şirket IR sayfasında varsa → summarize ile oku
```

**Adım 3A-2: Yatırımcı Sunumu**
```bash
# Şirket IR sayfası → "Yatırımcı Sunumları" / "Investor Presentations"
# URL'yi web_search ile bul:
web_search "{şirket} yatırımcı sunumu investor presentation {yıl}"

# PDF varsa:
summarize "https://ir.{şirket}.com/sunum.pdf" --extract-only > /tmp/{TICKER}_ir_sunum.txt
```
- Yatırımcı sunumunda KPI'lar, guidance, stratejik yol haritası var
- Çeyreklik yayınlıyorsa → en son olanı oku
- Protokol detayı: `turkiye-spesifik-rehber.md §5 — Yatırımcı Sunumu Analiz Protokolü`

**Adım 3A-3: Konferans Çağrısı / Analist Toplantısı**
```bash
# Son bilanço açıklaması sonrası toplantı — en güncel yönetim görüşünü içerir
# Transkript varsa (şirket yayınlıyorsa):
summarize "https://ir.{şirket}.com/transcript.pdf" --extract-only > /tmp/{TICKER}_conf_call.txt

# YouTube'da webcast varsa:
web_search "{şirket} analist toplantısı {çeyrek} {yıl} site:youtube.com"
summarize "https://youtu.be/{video_id}" --youtube auto --extract-only > /tmp/{TICKER}_conf_call_yt.txt

# Drive'daki kurum notlarında analist toplantı notu varsa:
find "$DRIVE_KURUM" -iname "*{TICKER}*toplant*" -o -iname "*{TICKER}*analist*" 2>/dev/null
```
- Protokol detayı: `turkiye-spesifik-rehber.md §5 — Konferans Çağrısı Analiz Protokolü`
- **Özellikle bak:** Yönetim tonu, kaçınılan sorular, guidance dışı sözel ipuçları

**Adım 3A-4: CEO/CFO Röportajları ve YouTube Videoları**
```bash
# YouTube aramaları:
web_search "{CEO adı} röportaj site:youtube.com"
web_search "{şirket} CEO {yıl} site:youtube.com"
web_search "{CEO adı} {şirket} interview"

# Bulunan videolar için transkript:
summarize "https://youtu.be/{video_id}" --youtube auto --extract-only > /tmp/{TICKER}_ceo_interview.txt

# Basın röportajları:
web_search "{CEO adı} röportaj {yıl}"
web_search "{şirket} yönetim stratejisi {yıl}"
```
- CEO'nun kendi ağzından strateji, öncelikler, kriz yönetimi
- **Dikkat:** Röportaj pazarlama amaçlı olabilir — söylediklerini finansal verilerle cross-check et

**Adım 3A-5: Kaynak Tarama Sonuç Tablosu**

T1 Bölüm 4'ün (Yönetim Analizi) başına bu tablo eklenir:

```markdown
### Yönetim Kaynakları Tarama Sonucu

| Kaynak | Durum | Tarih | Not |
|--------|-------|-------|-----|
| KAP Bildirimleri (son 6 ay) | ✅ Tarandı / ❌ Taranmadı | YYYY-MM | [Kritik bildirimler: YON, ODA, ORT, TEM] |
| Faaliyet Raporu (Son) | ✅ Okundu / ❌ Bulunamadı | YYYY | [Kaynak URL/yol] |
| Yatırımcı Sunumu (Son) | ✅ / ❌ | YYYY-QX | [URL] |
| Konferans Çağrısı (Son) | ✅ / ❌ | YYYY-QX | [URL veya "yayınlanmıyor"] |
| CEO/CFO Röportajları | ✅ / ❌ | YYYY-MM | [URL veya "bulunamadı"] |
| Kurum Analist Toplantı Notu | ✅ / ❌ | YYYY-QX | [Drive dosya adı] |
```

**Tüm satırlar doldurulmalı.** Bulunamayanlar "❌ Bulunamadı" + neden (yayınlanmıyor, silinmiş, erişim engeli).

> **⚠️ KAYNAK GÜNCELLİĞİ KURALI:** Bkz. bu dosyanın sonundaki **§ Kaynak Güncelliği Protokolü** — her kaynağın tarihi belirtilmeli, eski kaynaklar uyarı ile işaretlenmeli.

---

### Yönetim Kalitesi Karnesi — 6 Kriter

Her kriter 0-5 arasında puanlanır. **Toplam 30 üzerinden:**
- 24-30 → Olağanüstü (Buffett portföy yöneticisi seviyesi)
- 18-23 → İyi (ortalamanın üzeri)
- 12-17 → Orta (yakından izle)
- <12 → Zayıf (tez için ciddi risk faktörü)

**Kriter 1: Sermaye Tahsisi Geçmişi (0-5)**

Son 5 yıldaki kararları değerlendir: temettü, yatırım, M&A, geri alım, sermaye artırımı.

| Skor | Tanım |
|------|-------|
| 5 | ROIC>WACC yatırımlar, değer yaratan M&A, geri alım zamanlaması doğru |
| 3 | Karışık: 1-2 iyi karar, 1 sorgulanabilir |
| 1 | Değer yıkıcı M&A, tepe noktasında sermaye artırımı, aşırı temettü |
| 0 | Holding veya ana şirket lehine kaynak transferi şüphesi |

**Kaynak:** KAP faaliyet raporu (yatırım harcamaları, M&A açıklamaları), temettü tarihi.

**Kriter 1 Derinleştirme: Sermaye Tahsisi Kantifikasyonu (MS/JPM seviyesi)**

Basit skorun ötesinde, her büyük sermaye kararını kantitatif olarak değerlendir:

```markdown
### Sermaye Tahsisi Geçmişi — Kantitatif Değerlendirme

| Karar | Yıl | Tutar | Sonuç | ROIC | Değerlendirme |
|-------|-----|-------|-------|------|---------------|
| [M&A: Hedef şirket] | YYYY | X M TL | [Başarılı/Başarısız/Erken] | %X | [1 cümle] |
| [Organik yatırım: fabrika/mağaza] | YYYY | X M TL | [Doluluk/kapasite kullanımı] | %X | [1 cümle] |
| [Temettü politikası] | Son 3Y | Toplam X M TL, Dağıtım oranı %Y | [Sürdürülebilir mi?] | — | [1 cümle] |
| [Geri alım] | YYYY | X M TL @ ortalama Y TL/hisse | [Mevcut fiyat vs alım fiyatı] | — | [1 cümle] |
```

**Tazminat Yapısı Analizi (veri mevcutsa):**

| Bileşen | Oran | KPI Bağlantısı | Değerlendirme |
|---------|------|----------------|---------------|
| Sabit maaş | %X | — | |
| Değişken/performans | %X | [Hangi KPI'lara bağlı?] | Hissedar çıkarıyla uyumlu mu? |
| Hisse bazlı | %X | [Uzun vadeli mi, kısa vadeli mi?] | |

**⚠️ Veri kısıtlılığı notu:** Türkiye'de çoğu BIST şirketinde detaylı tazminat yapısı kamuya açık değildir. Faaliyet raporundaki "Üst düzey yönetici ücretleri" toplam rakamı genellikle tek mevcut veridir. Bu durumda toplam tutarı ve YoY değişimini raporla, yapısal kırılım yapılamadığını belirt.

**Governance Kama Analizi (kontrol eden ortak varsa):**

```
Kontrol Hakları: %X (oy hakkı)
Nakit Akış Hakları: %Y (temettü hakkı)
Kama = Kontrol - Nakit Akış = %Z

Kama > %10 → ⚠️ Governance riski (kontrol eden ortağın çıkarı ile küçük yatırımcının çıkarı ayrışabilir)
Kama = 0 → ✅ Tek sınıf hisse, çıkarlar uyumlu
```

---

**Kriter 2: Guidance Doğruluğu (0-5)**

Son 3-4 yılda yönetimin açıkladığı beklentiler ne kadar tuttu?

| Skor | Tanım |
|------|-------|
| 5 | Açıklanan guidance'a ±%5 içinde, tutarlı |
| 3 | Ortalama ±%10-15 sapma — muhafazakâr veya iyimser |
| 1 | Büyük miss'ler, sürekli aşağı revizyon |
| 0 | Guidance vermekten kaçınma veya gerçekçilikten uzak iyimserlik |

**Kaynak:** KAP bilanço açıklama sunumları, önceki yıl bülten veya basın açıklamaları, faaliyet raporu hedefler bölümü. Web araştırma: "{şirket} yönetim beklenti {yıl}".

---

**Kriter 3: İlişkili Taraf İşlemleri Riski (0-5)**

Özellikle aile şirketlerinde holding/ana şirket lehine kaynak transferi riski.

| Skor | Tanım |
|------|-------|
| 5 | Olağan ticari koşullarda, küçük hacimde, tam açıklama |
| 3 | İlişkili taraf işlemi var ama piyasa koşullarına yakın, tam açıklama |
| 1 | Şüpheli fiyatlandırma veya açıklama eksikliği |
| 0 | Holding lehine sistematik kaynak transferi kanıtı |

**Kaynak:** KAP faaliyet raporu dipnotları — "İlişkili Taraf İşlemleri" bölümü (ZORUNLU OKU). Bağımsız denetim raporu.

---

**Kriter 4: Kriz Yönetimi Geçmişi (0-5)**

Şirket geçmişte kriz yaşadıysa (kur şoku, sektörel kriz, COVID, regülasyon) yönetim nasıl tepki verdi?

| Skor | Tanım |
|------|-------|
| 5 | Proaktif, şeffaf, uzun vadeyi koruyan kararlar |
| 3 | Reaktif ama yönetilebilir, kalıcı zarar yok |
| 1 | Geç tepki, iletişim eksikliği, kalıcı değer kaybı |
| 0 | Kriz geçmişi yok — bu durumda "Değerlendirilemez (DE)" yaz |

**Kaynak:** Haber arşivi (web_search: "{şirket} {kriz yılı}"), basın açıklamaları, faaliyet raporları.

---

**Kriter 5: Stratejik Tutarlılık (0-5)**

Açıklanan strateji ile gerçekleşen yatırım kararları uyumlu mu?

| Skor | Tanım |
|------|-------|
| 5 | 3+ yıl boyunca strateji tutarlı, yatırımlar stratejiyi destekliyor |
| 3 | Strateji var, bazı sapmalar açıklanmış |
| 1 | Strateji sık değişiyor veya söylem ile eylem arasında ciddi fark |
| 0 | Belirsiz strateji, reaktif kararlar |

**Kaynak:** Son 3-5 yıl faaliyet raporları (strateji bölümü), yatırımcı günü sunumları, röportajlar.

---

**Kriter 6: Yönetim İletişim Kalitesi (0-5)**

Yönetim kötü haberleri de iyi haberler kadar açıkça paylaşıyor mu?

| Skor | Tanım |
|------|-------|
| 5 | Miss'leri kabul eder, açıklar, düzeltici plan paylaşır |
| 3 | İyi haberlerde iletişim güçlü, kötü haberlerde çekingen |
| 1 | Sorunları örtbas etme eğilimi, yatırımcı ilişkileri minimal |
| 0 | Güvenilirlik sorunu, önemli gelişmeleri geç/eksik açıklama |

**Kaynak:** KAP özel durum açıklamaları, analist konferansları (varsa), basın açıklamaları, şirket IR toplantı notları.

---

**Scorecard Çıktı Formatı:**

```
## Yönetim Kalitesi Karnesi — [ŞİRKET]

| Kriter | Skor (/5) | Gerekçe (1-2 cümle) |
|--------|-----------|---------------------|
| 1. Sermaye Tahsisi | X | [Gerekçe] |
| 2. Guidance Doğruluğu | X | [Gerekçe] |
| 3. İlişkili Taraf Riski | X | [Gerekçe] |
| 4. Kriz Yönetimi | X/DE | [Gerekçe veya "Kriz geçmişi yok"] |
| 5. Stratejik Tutarlılık | X | [Gerekçe] |
| 6. İletişim Kalitesi | X | [Gerekçe] |
| **TOPLAM** | **XX/30** | **[İyi/Orta/Zayıf]** |

**Öne Çıkan Güçler:** [1-2 madde]
**Öne Çıkan Riskler:** [1-2 madde]
**Yönetim Hisse Sahipliği:** Yönetim sahiplik oranı %X → [Normal/Düşük ⚠️]
```

**Not:** Kamuya açık olmayan bilgiler (dedikodu, anonim iddialar) scorecard'a girmez. Yalnızca doğrulanabilir kaynaklar: KAP, faaliyet raporu, basın, röportaj, IR toplantısı.

**MQS → WACC Etkisi (T2/T3 entegrasyonu):**

MQS skoru, DCF'te WACC'a eklenen (veya çıkarılan) bir governance primi olarak yansır:

| MQS Skoru | Band | WACC Etkisi | Gerekçe |
|-----------|------|-------------|---------|
| 24-30 | Olağanüstü | -50bp | Üstün sermaye tahsisi, güçlü governance → daha düşük risk |
| 18-23 | İyi | 0bp (nötr) | Ortalamanın üzeri, ek risk/ödül yok |
| 12-17 | Orta | +50bp | Governance riski var, sermaye tahsisi sorgulanabilir |
| <12 | Zayıf | +100bp | Ciddi governance sorunu, WACC artırımı zorunlu |

**T3 aktarım mekanizması:**
1. T1'de MQS skoru hesaplanır ve research.md'ye yazılır
2. T2'de DCF parametreleri belirlenirken, data_pack'teki "ERP" veya "firma spesifik prim" satırına MQS etkisi eklenir
3. T3'te VALUATION.md'de MQS WACC etkisi ayrı satır olarak gösterilir
4. Excel modelinde "MQS primi" ayrı bir input hücresi olur (formül bazlı modelde Ke hesabına eklenir)

**Zorunlu çıktı:** MQS skoru T1 research.md'de raporlandıktan sonra, T2 data_pack'ine "MQS WACC Etkisi: +X bp" olarak aktarılır.

#### 4A. Yönetim Rehberliği Kantitatif Yakalama (ZORUNLU — T2 Senaryo Girdisi) [v2.3]

> **Neden var?** MQS Kriter 2 guidance doğruluğunu 0-5 skalada skorlar ama senaryo-metodoloji.md §2A.1, formülde **gerçek sayısal değerleri** kullanır:
> `Ağırlıklı_Değer = G × Yönetim_Rehberliği + (1-G) × Formül_Sonucu`
> Bu formül için 3 girdi gerekir: (1) güncel rehberlik değerleri, (2) tarihsel isabet oranı, (3) hesaplanmış G skoru.
> MQS tek başına bunu sağlamaz — bu bölüm o boşluğu kapatır.

**ADIM 1: Güncel Dönem Rehberlik Değerlerini Kaydet**

Şirketin açıkladığı forward-looking guidance'ı aşağıdaki tabloya kaydet. Kaynaklar: yatırımcı sunumu, faaliyet raporu "beklentiler" bölümü, KAP özel durum açıklaması, analist konferansı transkripti.

```
## Yönetim Rehberliği — [ŞİRKET] (Açıklama Tarihi: [TARİH])

| Metrik | Yönetim Rehberliği | Birim | Kaynak |
|--------|-------------------|-------|--------|
| Hasılat büyümesi | [%X veya X mn TL] | % veya TL | [Sunum/KAP/Konferans] |
| FAVÖK marjı | [%X] | % | [Kaynak] |
| CapEx | [X mn TL veya hasılatın %Y'si] | TL veya % | [Kaynak] |
| Mağaza/şube sayısı | [X adet / net açılış] | adet | [Kaynak] |
| Temettü politikası | [%X payout / X TL/hisse] | % veya TL | [Kaynak] |
| Diğer: [metrik adı] | [değer] | [birim] | [Kaynak] |

Rehberlik Türü: ☐ Kesin rakam  ☐ Aralık (alt-üst)  ☐ Nitel ("büyüme sürecek")  ☐ Yok
Rehberlik Kapsamı: ☐ 1 yıl  ☐ Orta vade (3-5 yıl)  ☐ Uzun vade vizyonu
```

**Rehberlik YOKSA:** Tabloyu boş bırakma — "Yönetim kamuya açık kantitatif guidance vermemektedir" yaz ve G = 0.5 (nötr) olarak not et.

**Rehberlik NİTEL ise** ("güçlü büyüme bekliyoruz" gibi): Nitel ifadeyi tahmini aralığa çevir ve kaydet:
- "Güçlü büyüme" → %15-25 (sektör ortalamasının üzeri)
- "Istikrarlı seyir" → %0-5
- "Marj iyileşmesi" → +100-300bp
- Not: Nitel çeviri → G skoru otomatik olarak 0.1 düşürülür (belirsizlik cezası)

**ADIM 2: Tarihsel Rehberlik İsabet Tablosu**

Son 2-3 dönemin guidance vs gerçekleşen karşılaştırmasını yap. Bu tablo G skoru hesabının ana girdisidir.

```
## Rehberlik İsabet Tablosu — [ŞİRKET]

| Dönem | Metrik | Rehberlik | Gerçekleşen | Sapma (%) | Yön |
|-------|--------|-----------|-------------|-----------|-----|
| FY2024 | Hasılat büyümesi | %X | %Y | |Y-X|/X | ↑aşırı / ↓eksik |
| FY2024 | FAVÖK marjı | %X | %Y | |Y-X|/X | ↑ / ↓ |
| FY2023 | Hasılat büyümesi | %X | %Y | |Y-X|/X | ↑ / ↓ |
| FY2023 | FAVÖK marjı | %X | %Y | |Y-X|/X | ↑ / ↓ |
| ... | ... | ... | ... | ... | ... |

Ortalama Sapma: %Z
Eğrilim (Bias): ☐ Sistematik iyimser  ☐ Sistematik muhafazakâr  ☐ Karışık/nötr
```

**Kaynak hiyerarşisi (tarihsel guidance bulmak için):**
1. Önceki yıl yatırımcı sunumları (Drive veya IR sayfası arşivi)
2. Önceki yıl faaliyet raporu "beklentiler" bölümü
3. KAP bülten/basın açıklamaları arşivi
4. Kurum raporlarındaki "yönetim hedefi" referansları
5. Web araştırma: `"{şirket} yönetim beklenti {yıl}"`, `"{şirket} guidance {yıl}"`

**ADIM 3: G Skoru Hesapla ve Kaydet**

Tarihsel isabet tablosundaki ortalama sapma oranını kullanarak G skorunu belirle:

```
G SKORU HESAPLAMA:

Ortalama Sapma = %Z (Adım 2'den)

  Z < %5   → G = 1.0 (mükemmel isabet)
  Z = %5-15  → G = 0.8 (güçlü isabet)
  Z = %15-30 → G = 0.6 (orta isabet)
  Z = %30-50 → G = 0.4 (zayıf isabet)
  Z > %50   → G = 0.2 (güvenilmez)

Düzeltmeler:
  Sistematik iyimser eğrilim → G'yi 0.1 düşür
  Sistematik muhafazakâr eğrilim → G'yi 0.1 artır (max 1.0)
  Nitel rehberlik (sayısal değil) → G'yi 0.1 düşür
  Rehberlik yok veya ilk defa → G = 0.5 (nötr)

Hesaplanan G skoru: [X.X]
```

**T2 AKTARIM FORMATI (ZORUNLU):**

T1 research.md'nin sonuna aşağıdaki bloğu ekle — T2 senaryo parametreleri bu veriyi doğrudan kullanacak:

```
## T1→T2 Guidance Aktarım Paketi

G_SKORU: [0.X]
G_GEREKCE: "[1 cümle — isabet oranı ve eğrilim]"

GÜNCEL_REHBERLIK:
  hasilat_buyume: [%X veya null]
  favok_marji: [%X veya null]
  capex: [X mn TL veya null]
  magaza_sayisi: [X adet veya null]
  diger: {metrik: deger}

MQS_KRITER2_SKOR: [0-5]
REHBERLIK_TURU: [kesin/aralik/nitel/yok]
EGRILIM: [iyimser/muhafazakar/notr]
```

> **Cross-reference:** Bu aktarım paketi, senaryo-metodoloji.md §2A.1'deki harmanlama formülünde kullanılır.
> `Ağırlıklı_Değer = G × Yönetim_Rehberliği + (1-G) × Formül_Sonucu`

---

### 5. Sektör Analizi (1.000-1.200 kelime)

**Amaç:** Şirketin oynadığı sahayı tam olarak anlamak.

**Zorunlu içerik:**
- **Pazar büyüklüğü ve büyüme (250-350 kel):** Global TAM, Türkiye TAM, CAGR, segment kırılımı
- **Porter Beş Güç Analizi (250-350 kel):** Her güç 1-5 skorlu + düzenleyici boyut entegre
- **Düzenleyici ortam (200-300 kel):** İlgili regülatör (TAPDK, BDDK, EPDK...), risk seviyesi, aktif soruşturma/düzenleme
- **Büyüme sürücüleri ve engeller (200-300 kel):** Tailwinds, headwinds, sekülyer trendler
- **Endüstri yapısı (100-200 kel):** Konsolide/parçalı, yoğunlaşma trendi, değer zinciri

**Kaynak hiyerarşisi:**
1. Sektör kuruluşları (TAPDK, TÇD, OSD, BTK, BDDK, EPDK)
2. KAP faaliyet raporu — sektör bölümü
3. Araştırma firmaları (Euromonitor, IATA, WHO)
4. Kurum raporları (İş Yatırım, Ak Yatırım sektör notları) — Drive'dan `summarize` ile oku (bkz. T1 başlangıç §Veri Toplama)
5. Web araştırma

**Düzenleyici tarama ZORUNLU:** → `references/ortak/duzenleyici-ortam-taramasi.md` okunmadan sektör analizi tamamlanmış SAYILMAZ.
**BIST sektör metrikleri:** → `references/ortak/bist-sektor-metrikleri.md` — her sektörün kendine özgü 4-6 metriği.

**TAM hype uyarısı:** Araştırma firmalarının TAM tahminleri genellikle şişirilmiştir. TAM → SAM → SOM daralma zincirini göster.

**5B. Makro-Mikro Aktarım Zinciri (Zorunlu — MS/JPM seviyesi)**

Sektör analizini şirket gelir projeksiyonuna bağlayan sayısal zincir. "GDP artıyor → sektör büyüyecek → şirket büyüyecek" yetmez. Elastikiyetlerle desteklenen somut aktarım mekanizması kur:

```markdown
### Makro-Mikro Aktarım Zinciri — {TICKER}

GDP Büyümesi (reel) → %X
  × Tüketim Elastikiyeti → ~Y (sektöre bağlı, tipik 0.8-1.2)
= Özel Tüketim Büyümesi → %Z

  × Sektör/Tüketim Elastikiyeti → ~W
= Sektör Büyümesi → %V
  (Cross-check: sektör kuruluşu tahmini ile karşılaştır)

  × Şirket Pazar Payı Trendi → kazanıyor/kaybediyor?
  + Yeni kanal/coğrafya katkısı → %U ek büyüme
= Şirket Organik Büyüme Tahmini → %T

Sonuç: Reel GDP %X → Şirket büyümesi %T
Çarpan: T/X = [kaç x GDP büyümesi]
```

**Elastikiyet kaynakları:**
- TCMB / TUIK: Tüketim-GDP elastikiyeti
- Sektör raporları: sektör-tüketim elastikiyeti
- Yoksa: proxy olarak son 5Y sektör büyümesi / GDP büyümesi oranı

**⚠️ Bu zincir T2 gelir projeksiyonunu gerekçelendirir.** "Şirket %15 büyüyecek" dediğimizde, bu zincirdeki hangi varsayıma dayandığı açık olmalı.

---

### 6. Hendek (Rekabet Avantajı) Analizi (600-800 kelime)

**Amaç:** "Bu şirketi takliden aynısını yapsam ne kadar zaman ve para harcamam lazım?"

**Zorunlu içerik:**
- **4 hendek türü değerlendirmesi (her biri 100-150 kel):**
  1. Yüksek Giriş Bariyeri — sermaye, lisans, zaman
  2. Değiştirme Maliyeti — müşteri geçiş zorluğu
  3. Pazar Yapısı — duopol, monopol, HHI
  4. Münhasır Varlıklar — patent, IP, veri, marka
- **Hendek gücü skoru:** 0-10, gerekçeli
- **Hendek dayanıklılığı:** Kaç yıl sürdürülebilir?
- **Hendek barometresi:** Terminal ROIC vs WACC ilişkisi
  - ROIC >> WACC → güçlü moat
  - ROIC ≈ WACC → moat yok
  - ROIC < WACC → değer yıkımı

**Kaynak:** T1'in diğer bölümleri + sektör analizi + peer ROIC karşılaştırması

**BBB örnekleri (referans):**
- Data moat: Genius Sports → veri tekeli
- Brand moat: Ferrari → Veblen etkisi
- Cultural moat: Vakko → 90 yıllık miras, kırılgan
- Duopoly: TBORG+AEFES → %95+ pazar payı
- Terminal ROIC barometresi: Pop Mart %30 vs WACC %7.21 → güçlü; DOCO ≈ WACC → yok

---

### 7. Finansal Derinlemesine (1.000-1.200 kelime)

**Amaç:** "Rakamlar hikayeyi doğruluyor mu?" — T2'nin özet anlatımı.

**Zorunlu içerik:**
- **İlker'in 6 metriği tablosu (zorunlu):** ROIC, SNA Marjı, Brüt Kâr Marjı, Net Borç/FAVÖK, Ciro Büyümesi, ÖK
- **Veto kontrolü:** ROIC < %10 veya FCF negatif → RED FLAG
- **5Y trend analizi (300-400 kel):** Gelir büyümesi trendi, marj evrimi, hikaye nedir?
- **ROIC dinamikleri (200-300 kel):** ROIC = Marj × Devir. Hangi bileşen değişiyor? DuPont decomposition.
- **Nakit akış kalitesi (200-300 kel):** FCF/Net Kâr oranı, CapEx yoğunluğu, çalışma sermayesi trendi
- **Bilanço sağlığı (150-200 kel):** Net borç, kaldıraç, vade profili, kur riski

**Yazma kuralı:** "Brüt marj 5 yılda 800bp genişledi" (doğru) — "Brüt marj artmıştır" (yanlış). Sayısal, spesifik, trend odaklı.

**Kaynak:** T2 finansal modelleme çıktısı veya BBB Finans araçları. Her rakama kaynak etiketi zorunlu.

---

### 8. Rekabet Pozisyonlaması (500-700 kelime)

**Amaç:** "Bu şirket rakiplerine göre nerede duruyor?"

**Zorunlu içerik:**
- **Pazar payı ve trend (150-200 kel):** Son 3-5 yılda pay artıyor mu düşüyor mu?
- **Rakip tablosu (min 4-5 rakip):**

```
| Şirket | Gelir | Büyüme | Brüt Marj | FAVÖK Marjı | ROIC | Konum |
|--------|-------|--------|-----------|-------------|------|-------|
| [Target] ★ | | | | | | Lider/Takipçi |
| [Peer 1] | | | | | | |
```

- **Stratejik avantajlar ve zayıflıklar (150-200 kel):** Nerede daha iyi, nerede daha kötü
- **Konsolidasyon/rekabet dinamikleri (100-150 kel):** Pazar yoğunlaşıyor mu parçalanıyor mu?

**Kaynak hiyerarşisi:**
1. KAP/BBB Finans (yerli peer'lar)
2. Yahoo Finance (yurt dışı peer'lar)
3. Damodaran Industry Data (sektör ortalamaları)
4. Faaliyet raporları (rakip referansları)

---

### 9. Riskler ve Fırsatlar (500-800 kelime)

**Amaç:** Dürüst risk değerlendirmesi — İlker'in kuralı: "her tezde Bulls + Bears dengeli."

**Zorunlu içerik:**
- **Top 5 fırsat (her biri 30-50 kel):** Spesifik, veriyle destekli
- **Top 5 risk (her biri 30-50 kel):** Spesifik, ölçülebilir etki
- **Tez çöküş kriterleri (min 2):** Tez ne zaman çöker? → "Pazar payı %40'ın altına düşerse", "ROIC 2 yıl üst üste <%10 kalırsa"
- **Quality Value matris sonucu (50-100 kel):** Final değerlendirme

**Tez çöküş kriterleri kuralı:** Spesifik + ölçülebilir + izlenebilir. "Rekabet artarsa" yanlış. "Lisans sayısı 2x artarsa pazar payı ≤%35'e düşebilir" doğru.

**9B. Olasılıksal Risk Çerçevesi (ZORUNLU)**

Her risk için niteliksel etiketin ötesinde olasılık × etki matrisi doldur:

```markdown
### Risk Etki Matrisi — {TICKER}

| # | Risk | Olasılık | FAVÖK Etkisi | Zımni Senaryo | İzleme Göstergesi |
|---|------|----------|-------------|---------------|-------------------|
| 1 | [Risk tanımı] | %X | -%Y | Bear senaryoda dahil mi? | [Hangi veri izlenecek] |
| 2 | [Risk tanımı] | %X | -%Y | | |
```

**Olasılık × Etki skoru:** Yüksek olasılık + yüksek etki → Bölüm 1B Varyant Algısı'na otomatik geri bildirim.

**9C. Pre-Mortem Egzersizi (ZORUNLU)**

> "12 ay sonra hisse %50 düştü. Ne oldu?"

Bu soruyu ZORLA cevapla — 3-5 senaryo:
1. [Senaryo: Ne oldu? Neden göremedik?]
2. [Senaryo: ...]
3. [Senaryo: ...]

**Amaç:** Teyit yanlılığını kırmak. Analist kendi tezine aşık olduğunda pre-mortem "ama ya yanılıyorsam?" sorusunu disiplinli bir formata sokar.

**9D. Kırmızı Takım Kontrolü (ZORUNLU)**

Tezin karşısındaki en güçlü 3 argümanı yaz. Bu argümanları çürütebiliyorsan tez güçlüdür; çürütemiyorsan tez zayıftır.

```markdown
### Kırmızı Takım — Teze Karşı En Güçlü 3 Argüman

| # | Argüman | Kanıt/Veri | Çürütme Girişimi | Sonuç |
|---|---------|-----------|------------------|-------|
| 1 | [En güçlü karşı argüman] | [Veri] | [Neden yanlış/eksik?] | Çürütüldü/Geçerli risk |
| 2 | | | | |
| 3 | | | | |
```

**Kural:** "Çürütülemedi → Geçerli risk" sonucu kabul edilebilir. Zorla çürütme — bu dürüst değildir. Çürütülemeyen risk → Bölüm 9 risk listesinde ÜST SIRALARA çıkar + senaryo ağırlıklandırmasını etkiler.

---

### 10. Katalizör Takvimi (ZORUNLU)

**Amaç:** Hisseyi hareket ettirecek olayların tarih, olasılık ve potansiyel etki bazında sistematik takibi. MS/JPM/Goldman analistleri her raporun sonunda "Key Catalysts" bölümü koyar — biz bunu daha kantitatif yapıyoruz.

**Kaynak hiyerarşisi:**
1. KAP bilanço açıklama takvimi (en güvenilir — zorunlu tarihler)
2. Faaliyet raporu — yönetim hedefleri, proje tamamlanma tarihleri
3. Yatırımcı sunumları — büyüme planları, açılış tarihleri
4. Kurum raporları — analist beklentileri
5. Sektör kuruluşları — regülasyon takvimi, ÖTV/vergi düzenlemesi
6. TCMB PPK takvimi, BDDK düzenlemeleri (makro katalizörler)

**Katalizör Takvimi Formatı:**

```markdown
### Katalizör Takvimi — {TICKER}
#### Değerleme Tarihi: YYYY-MM-DD

| # | Katalizör | Tahmini Tarih | Olasılık | Yön | Etki (Hisse %) | Kaynak |
|---|-----------|--------------|----------|-----|----------------|--------|
| C1 | 1C26 bilanço açıklaması | Mayıs 2026 | %95 | Yukarı | +5-10% | KAP takvim |
| C2 | Yeni mağaza açılışları (X adet) | 2026 H2 | %80 | Yukarı | +3-5% | Yatırımcı sunumu |
| C3 | ÖTV düzenlemesi riski | 2026 Q3 | %30 | Aşağı | -10-15% | TAPDK takvim |
| C4 | M&A duyurusu (pazar söylentisi) | Belirsiz | %20 | Yukarı | +15-25% | Basın |
| C5 | MSCI EM endeks incelemesi | Kasım 2026 | %15 | Yukarı | +10-20% | MSCI takvim |

#### Katalizör Özeti
- **Net pozitif katalizör sayısı:** X
- **En yüksek etkili katalizör:** CX — [1 cümle]
- **En yakın tarihli katalizör:** CX — [tarih, kalan gün]
- **Beklenen Değer (olasılık × etki):** Toplam +/-%X → Senaryo ağırlıklandırmasına geri bildirim
```

**Katalizör sınıflandırması:**
| Tür | Örnekler | Tipik Etki |
|-----|----------|-----------|
| Bilanço/Kazanç | Çeyreklik sonuçlar, yıllık bilanço | %5-15 |
| Kurumsal Aksiyon | M&A, sermaye artırımı, geri alım, halka arz | %10-30 |
| Regülasyon | ÖTV, lisans, çevre mevzuatı | %5-20 |
| Makro | PPK faiz kararı, kur şoku, seçim | %5-15 |
| Sektörel | Rakip iflası, pazar konsolidasyonu | %5-20 |
| Endeks | MSCI, BIST-30 dahil/hariç | %10-20 |

**T3 entegrasyonu:** Katalizör takvimi T3'te hedef fiyatın "forward roll" (ileri taşıma) hesaplamasına girdi sağlar. Pozitif katalizörlerin ağırlıklı beklenen değeri, 12 aylık hedefin hesaplanmasında potansiyel upside olarak değerlendirilir.

**Backtest bağlantısı:** 6 ay sonra bu tablo geri açılır ve gerçekleşen/gerçekleşmeyen katalizörler işaretlenir → Bkz. "Sistematik Geri Test Çerçevesi" bölümü.

---

### 11. Sistematik Geri Test Çerçevesi (T1 Sonunda Kurulur, +6 Ay Sonra Çalıştırılır)

**Amaç:** Her değerleme çalışmasını 6 ay sonra geriye dönük inceleme — ne doğru gitti, ne yanlış gitti, neden? MS/JPM seviyesinde kurumsal disiplin.

**Kurulum (T1 sırasında):**

T1 tamamlandığında, geri test dosyası oluşturulur ve 6 ay sonra inceleme için hatırlatma kurulur.

```markdown
### Geri Test Kayıt Dosyası — {TICKER}
#### Analiz Tarihi: YYYY-MM-DD
#### İnceleme Tarihi: [+6 ay, YYYY-MM-DD]

## Başlangıç Değerleri (kilitli — değiştirilemez)
| Parametre | Değer |
|-----------|-------|
| Analiz tarihi hisse fiyatı | X TL |
| Hedef fiyat | X TL |
| Tavsiye | [AL/TUT/SAT] |
| Potansiyel getiri | %X |
| Bull senaryo | X TL |
| Bear senaryo | X TL |
| Katalizör takvimindeki C1-C5 | [özet] |
| MQS skoru | X/30 |
| WACC | %X |
| Baz EBIT marjı Y1 | %X |

## +6 Ay İnceleme (analiz tarihinde BOŞ bırakılır)
| Kontrol | Başlangıç | Gerçekleşen | Sapma | Not |
|---------|-----------|-------------|-------|-----|
| Hisse fiyatı | X TL | | | |
| Hedef fiyat isabeti | ±%30 içinde mi? | | | |
| Gelir büyümesi Y1 | %X beklenti | | | |
| EBIT marjı Y1 | %X beklenti | | | |
| Katalizör C1 | [beklenen] | [gerçekleşti mi?] | | |
| Katalizör C2 | [beklenen] | [gerçekleşti mi?] | | |
| MQS güncelleme | X/30 | [yeni skor?] | | |

## Öğrenilen Dersler
1. [Doğru tahmin — neden?]
2. [Yanlış tahmin — neden? Model hatasından mı, dış şok mu?]
3. [Skill/metodoloji iyileştirme önerisi]
```

**Operasyonel süreç:**
1. T1 tamamlandığında → `{TICKER}_backtest.md` dosyası `research/companies/{TICKER}/` altına oluşturulur
2. Dosya adının içinde inceleme tarihi: `{TICKER}_backtest_review_YYYY-MM-DD.md`
3. İlker'e hatırlatma: "6 ay sonra ({tarih}) bu dosyayı açıp geri test yapılması gerekiyor"
4. +6 ay sonra: İlker `/backtest {TICKER}` dediğinde, bu dosya açılır, güncel veriler çekilir, karşılaştırma yapılır

**Başarı kriteri:** 1 yıl içinde 5+ şirket geri test edildiğinde:
- Hedef fiyat isabeti: ±%30 içinde %60+ ise → model çalışıyor
- Sistematik sapma varsa (hep yukarı/hep aşağı) → varsayım bias'ı düzelt
- Katalizör tahmin isabeti → kaynakların güvenilirliğini ölç

---

### 12. Birincil Araştırma Kontrol Listesi (Mümkünse Uygulanır)

**Amaç:** Kurum analistlerinin avantajı "birincil araştırma" erişimidir — müşteri anketleri, yönetim toplantıları, saha ziyaretleri. Biz bunların çoğuna erişemeyiz ama bazılarını yapay zekâ araçlarıyla simüle edebiliriz.

**Yapılabilir Birincil Araştırma (AI destekli):**

| # | Araştırma Türü | Nasıl | Araç | Öncelik |
|---|---------------|-------|------|---------|
| PR1 | Google Trends analizi | Marka arama hacmi trendi, sezonalite | web_search + web_fetch | Yüksek |
| PR2 | App Store / Google Play sıralaması | Uygulama puanı, inceleme trendi, rakip sıralaması | web_fetch | Yüksek (dijital kanalı olan şirketler) |
| PR3 | Glassdoor / Indeed çalışan yorumları | Yönetim kalitesi, çalışan memnuniyeti, maaş trendi | web_search | Orta |
| PR4 | Sosyal medya duyarlılığı | Twitter/X, Ekşi Sözlük, şikayetvar.com | web_search | Orta |
| PR5 | E-ticaret fiyat karşılaştırması | Hepsiburada, Trendyol, n11 fiyat konumlandırması | web_fetch | Orta (perakende şirketleri) |
| PR6 | Bayii / franchise ağı analizi | Mağaza sayısı trendi, coğrafi kapsam | web_search + IR sunumu | Yüksek (perakende/franchise) |
| PR7 | Patent / marka tescili | Türk Patent Enstitüsü, WIPO | web_search | Düşük |
| PR8 | Mahkeme / soruşturma taraması | UYAP (sınırlı), basın, KAP özel durum | web_search | Orta |
| PR9 | İhracat verileri | TÜİK, gümrük istatistikleri | web_fetch | Orta (ihracatçılar) |
| PR10 | Endüstri konferans / fuar katılımları | Şirket hangi fuarlara katılıyor? | web_search | Düşük |

**Yapılamayan Birincil Araştırma (farkındalık notu):**
- Yönetimle birebir toplantı (NDR)
- Müşteri anketi (channel check)
- Tedarikçi/bayii telefon görüşmeleri
- Fabrika/tesis ziyareti

Bu kısıtlılık raporun sonunda "Analiz Kısıtlılıkları" bölümünde belirtilir. "Bu analiz kamuya açık veriler ve ikincil kaynaklara dayanmaktadır. Birincil araştırma (yönetim toplantısı, saha ziyareti) yapılmamıştır."

**Sektöre Göre Birincil Araştırma Önceliklendirmesi:**

| Sektör | Öncelikli PR Adımları | Açıklama |
|--------|----------------------|----------|
| Perakende | PR1, PR2, PR5, PR6 | Marka arama, uygulama, fiyat, mağaza ağı |
| Teknoloji | PR1, PR2, PR3, PR7 | Arama trendi, uygulama, çalışan, patent |
| Sanayi | PR6, PR8, PR9 | Üretim ağı, hukuki risk, ihracat |
| Bankacılık | PR1, PR3, PR4 | Marka, çalışan, sosyal medya |
| Gıda/İçecek | PR1, PR5, PR6 | Marka, fiyat, dağıtım ağı |

---

## T1 Çıktı Formatı

**Dosya:** `research/companies/{TICKER}/{TICKER}_research.md`

```markdown
# [ŞİRKET ADI] ([TICKER]) — Şirket Araştırması

**Tarih:** [YYYY-MM-DD] | **Analist:** Kaya | **Kelime Sayısı:** ~X.XXX

---

## 1. Yönetici Özeti
[...]

## 2. Şirket Profili
[...]

[... 9 bölüm ...]

---

## Kaynaklar
- [Kaynak 1 — tarih]
- [Kaynak 2 — tarih]
```

---

## T4 Grafik Ön Planı (T1 Sonunda ZORUNLU)

T1 tamamlandığında, T4 (Grafik Üretimi) için gerekli grafiklerin listesini hazırla. Bu liste T4'ün verimliliğini artırır ve rapor kalitesini yükseltir.

```markdown
### T4 Grafik Ön Planı — {TICKER}

| # | Grafik Adı | Bölüm | Veri Kaynağı | Grafik Tipi | Öncelik |
|---|-----------|-------|-------------|-------------|---------|
| G01 | Gelir Büyümesi (5Y) | Bölüm 7 | BBB Finans | Çubuk + çizgi (marj overlay) | Yüksek |
| G02 | FAVÖK Marjı Evrimi | Bölüm 7 | BBB Finans | Çizgi | Yüksek |
| G03 | Ürün Segmentasyonu | Bölüm 3 | Faaliyet raporu | Pasta/treemap | Orta |
| G04 | Coğrafi Kırılım | Bölüm 3 | Faaliyet raporu | Harita/pasta | Orta |
| ... | [Sektöre özgü] | | | | |
```

**Kural:** Her bölümde en az 1 grafik planlanmalı. Grafik yoksa "metin ağırlıklı bölüm" notu düş. T5 Assembly'de grafik olmayan sayfa = zayıf sayfa.

---

## T1 Doğrulama Checklist

- [ ] Kelime sayısı 6.000-8.000 aralığında
- [ ] 9 bölümün tamamı yazılmış (hiçbiri atlanmamış)
- [ ] Quality Value matris pozisyonu belirlenmiş
- [ ] İlker'in 6 metriği tablosu mevcut (Bölüm 6'da)
- [ ] Hendek gücü skorlanmış (0-10) ve barometresi hesaplanmış
- [ ] Düzenleyici ortam taranmış (Bölüm 4'te)
- [ ] Tez çöküş kriterleri min 2 tane, spesifik ve ölçülebilir
- [ ] Peer tablosu min 4-5 rakip içeriyor
- [ ] Her rakamda kaynak etiketi var
- [ ] `[DOĞRULANMADI]` veya `[KAYNAK GEREKLİ]` etiketi yok (varsa önce çöz)
- [ ] Veto kontrolü yapılmış (ROIC, FCF)
- [ ] **Yönetim kaynakları tarama tablosu (§3A-5)** doldurulmuş — 5 satırın tamamı
- [ ] **Kaynak güncelliği kontrolü** yapılmış — eski kaynaklar (>6 ay) uyarı ile işaretli
- [ ] **Türkçe karakter kontrolü** — tüm metin Türkçe karakterlerle yazılmış (ş, ğ, ü, ö, ç, ı, İ). ASCII Türkçe yok.
- [ ] **Terminoloji kontrolü** — İngilizce konsept terimler Türkçe karşılıklarıyla kullanılmış (bkz. §Dil ve Terminoloji Kuralları)
- [ ] **Her bölüm kelime aralığını karşılıyor** — bölüm bazlı kelime sayısı kontrol edilmiş
- [ ] **Ters İNA + Varyant Algısı tablosu (§1B)** doldurulmuş — zımni varsayımlar çıkarılmış, 3 sonuçtan biri seçilmiş
- [ ] **Risk Etki Matrisi (§9B)** doldurulmuş — her risk için olasılık × etki
- [ ] **Pre-Mortem egzersizi (§9C)** yapılmış — en az 3 senaryo
- [ ] **Kırmızı Takım (§9D)** doldurulmuş — 3 karşı argüman + çürütme girişimi
- [ ] **Makro-Mikro Aktarım Zinciri (§5B)** kurulmuş — GDP → şirket büyümesi bağlantısı
- [ ] **T4 Grafik Ön Planı** hazırlanmış — her bölüm için grafik listesi
- [ ] **Sermaye Tahsisi Kantifikasyonu** (Bölüm 4, Kriter 1 derinleştirme) — en az M&A ve organik yatırım değerlendirilmiş

---

## Yetersiz Veri Durumu

Bazı BIST şirketlerinde veri sınırlı olabilir. Protokol:

| Durum | Aksiyon |
|-------|---------|
| Segment gelir kırılımı yok | `[FAAlİYET RAPORU GEREKLİ]` etiketi, devam et |
| Yönetim biyografisi bulunamıyor | KAP + LinkedIn ile minimum bilgi, eksik kısmı belirt |
| TAM verisi güvenilir kaynak yok | "Bağımsız TAM tahmini mevcut değil" yaz, proxy kullan |
| Peer'lar çok farklı (ölçek/iş modeli) | Neden farklı olduğunu açıkla, en yakın olanları seç |
| Sektör kuruluşu verisi güncel değil | Son mevcut tarihi belirt, güncel olmadığını not et |

**Kural:** Bilmediğini yaz, biliyormuş gibi davranma. `[DOĞRULANMADI]` etiketi kullan.

---

## 📅 Kaynak Güncelliği Protokolü

### Neden Gerekli

2 yıl önce yayınlanmış bir CEO röportajı veya eski bir sektör raporu okunabilir — ama aradan geçen sürede şirket stratejisi, sektör yapısı, yönetim kadrosu veya makro koşullar tamamen değişmiş olabilir. **Eski kaynak = yanlış bilgi riski.**

### Güncellik Kategorileri

| Kategori | Eşik | Kurallar |
|----------|-------|---------|
| 🟢 **Güncel** | ≤6 ay | Herhangi bir uyarı olmadan kullanılabilir |
| 🟡 **Yaşlanmış** | 6-12 ay | Kullanılabilir **ama** `[Kaynak: YYYY-MM — X ay öncesi]` etiketi zorunlu |
| 🔴 **Eski** | >12 ay | **Birincil kaynak olarak KULLANILAMAZ.** Sadece tarihsel referans veya trend karşılaştırması için. `[TARİHSEL KAYNAK: YYYY-MM — X ay öncesi, güncel doğrulama gerekli]` etiketi zorunlu |

### Kaynak Tipine Göre Kurallar

| Kaynak Tipi | Beklenen Yenilenme Sıklığı | "Eski" Ne Zaman Başlar | Özel Kural |
|-------------|---------------------------|----------------------|------------|
| **KAP finansal tablo** | Çeyreklik | Son açıklanan dönem yoksa eski | BBB Finans otomatik güncel veri çeker — sorun yok |
| **Faaliyet raporu** | Yıllık | >15 ay (yeni yıl raporunun yayınlanması gerekir) | Yıllık rapor genellikle Mart-Nisan'da çıkar |
| **Yatırımcı sunumu** | Çeyreklik (varsa) | >6 ay | Guidance ve KPI'lar hızlı değişebilir |
| **Konferans çağrısı / toplantı** | Çeyreklik (varsa) | >6 ay | Yönetim tonu ve guidance en hızlı değişen veri |
| **CEO/CFO röportajı** | Düzensiz | >12 ay | Vizyon/strateji röportajı daha uzun ömürlü olabilir |
| **YouTube videosu** | Düzensiz | >12 ay | Yayın tarihi videoda yazar — kontrol et |
| **Sektör raporu** (Euromonitor vb.) | Yıllık | >18 ay | Sektör yapısı daha yavaş değişir ama enflasyonlu pazarlarda rakamlar hızlı eskir |
| **Kurum analisti raporu** | Çeyreklik/bilanço sonrası | >6 ay | Hedef fiyat ve beklentiler çok hızlı eskir |
| **Haber / basın** | Anlık | >6 ay | Haber bağlamı önemli — "kriz haberi" 2 yıl sonra da referans olabilir |

### Uygulama Kuralları

**Kural 1 — Her kaynağın tarihi belirtilir:**
```markdown
# ✅ Doğru
Faaliyet raporu (2025): Yönetim mektubu temkinli bir dil kullanıyor...
Pusula Yatırım raporu (Mart 2026): Hedef fiyat 63 TL...
CEO röportajı (Bloomberg HT, Eylül 2025): "2026'da 330 mağazayı hedefliyoruz"

# ❌ Yanlış
Faaliyet raporunda yönetim mektubu temkinli...
Hedef fiyat 63 TL olarak belirlendi...
CEO "330 mağazayı hedefliyoruz" dedi.
```

**Kural 2 — Eski kaynak kullanırken "o zamandan bu yana ne değişti?" sorusu sorulur:**
```markdown
# Doğru kullanım (tarihsel referans):
CEO, Mart 2024 röportajında (24 ay önce) "2025'te 250 mağazayı hedefliyoruz" demişti.
Gerçekleşme: 300 mağaza (hedefin %20 üzeri) — yönetim beklentisini aştı.
[TARİHSEL KAYNAK: 2024-03 — 24 ay öncesi, güncel doğrulama yapıldı]
```

**Kural 3 — Guidance karşılaştırmasında tarih zinciri zorunlu:**
Yönetimin verdiği guidance → gerçekleşme → fark → yeni guidance. Bu zincir kırık olmamalı.

**Kural 4 — YouTube videolarında tarih kontrolü:**
- Video yayın tarihi başlıkta veya açıklamada yazar
- `web_search` sonucunda tarih görünür
- Tarih bulunamazsa `[TARİH BELİRLENEMEDİ — güncelliği doğrulanamıyor]` etiketi

**Kural 5 — Sektör/pazar büyüklüğü verilerinde enflasyon uyarısı:**
Türkiye'de 3 yıl önceki "7B TL pazar" bugün 20B+ TL olabilir. Eski TL rakamları → `[TARİHSEL NOMİNAL DEĞER: YYYY — enflasyonla güncelliğini yitirmiş]`

### T1 Çıktısında Kaynak Listesi Formatı

Dosyanın sonundaki "Kaynaklar" bölümünde her kaynak şu formatta listelenir:

```markdown
## Kaynaklar

| # | Kaynak | Tarih | Güncellik | Kullanım |
|---|--------|-------|-----------|----------|
| 1 | KAP Faaliyet Raporu 2024 | 2025-04 | 🟢 | Birincil — segment, yönetim, strateji |
| 2 | Pusula Yatırım 4Ç25 Raporu | 2026-03 | 🟢 | Birincil — beklenti, hedef fiyat |
| 3 | CEO Röportajı (Bloomberg HT) | 2024-09 | 🟡 18 ay | İkincil — strateji vizyonu, güncel doğrulama gerekli |
| 4 | Euromonitor Sektör Raporu | 2023-06 | 🔴 33 ay | Tarihsel — pazar yapısı referansı, rakamlar eski |
| 5 | YouTube Analist Toplantısı | 2026-02 | 🟢 | Birincil — yönetim tonu, guidance |
```

---

## Bolum 13: T1 → T2 Senaryo Koprusu (Zorunlu Cikti)

> **Referans**: Turetim formulleri icin bkz. `senaryo-metodoloji.md`

T1 arastirma tamamlandiginda, asagidaki ciktilarin T2'ye aktarilmasi **zorunludur**.
Bu ciktilar T2'deki senaryo parametrelerinin turetiminde kullanilir.

### 13.1 T1 → T2 Aktarim Tablosu

| T1 Ciktisi | T2'de Kullanim Alani | Etki Mekanizmasi |
|------------|---------------------|------------------|
| Risk Etki Matrisi (en yuksek risk olasiligi) | Senaryo agirliklari | Risk >= %40 → Bear +5pp, Bull -5pp |
| MQS Skoru (0-30 arasi) | Senaryo agirliklari + WACC | MQS 24-30 → Bear -5pp; MQS 12-17 → Bear +5pp; MQS < 12 → Bear +10pp (bkz. senaryo-metodoloji.md §3.2) |
| Katalizor Takvimi (pozitif/negatif dagilim) | Senaryo narratifi | Bull tetikleyicileri = pozitif katalizorler |
| Peer buyume/marj verileri | Buyume + marj parametreleri | Q25/medyan/Q75 benchmark |
| Makro varsayimlar (GDP, FX, enflasyon) | Terminal buyume tavani | Terminal g <= reel GDP + sektor primi |
| Birincil arastirma bulgulari | Buyume validasyonu | Google Trends, App Store vb. teyit |
| **Yonetim rehberligi — kantitatif paket** [v2.3] | **Parametre harmanlama** | **§4A: G skoru + gercek degerler → senaryo-metodoloji.md 2A.1 formulu** |
| **Yatirim dongusu tespiti** [v2.2] | **CapEx + buyume parametreleri** | **senaryo-metodoloji.md 2A.2: rejim bazli ayarlama** |
| **Katalist takvimi (tarihli)** [v2.2] | **Senaryo tetikleyicileri** | **senaryo-metodoloji.md 2A.3: olay-senaryo esleme** |
| **Sirket rejimi** [v2.2] | **Aralik genisligi + agirlik egilimi** | **senaryo-metodoloji.md 2B: buyume/olgun/toparlanma** |
| **Bottom-up segment kirilimi** [v2.2] | **Buyume dogrulamasi** | **senaryo-metodoloji.md 2A.4: segment × buyume** |

### 13.2 Senaryo Narratif Sablonu (T1'de Doldurulur)

T1 sonunda asagidaki narratif hazirlanir ve T2-T5 boyunca kullanilir:

```
BEAR SENARYO TETIKLEYICILERI:
- [T1 Risk Matrisindeki en yuksek 2-3 risk]
- "Bu senaryo gerceklesir eger: (i) ..., (ii) ..., VE (iii) ..."
- Olasilik: [MQS + Risk bazli hesaplanan Bear agirligi]%

BASE SENARYO MERKEZI VARSAYIMLAR:
- [Konsensus + T1 bulgusuyla kalibre edilmis]
- "Sektorde mevcut trendler devam eder, yonetim guidance'a yakin performans gosterir"

BULL SENARYO KATALIZORLERI:
- [T1 Katalizor Takvimindeki pozitif katalizorler]
- "Bu senaryo gerceklesir eger: (i) ..., (ii) ..., VEYA (iii) ..."
- Olasilik: [MQS + Risk bazli hesaplanan Bull agirligi]%
```

### 13.3 Kontrol Listesi

```
[ ] Risk Etki Matrisi tamamlandi — en yuksek risk olasiligi not edildi
[ ] MQS skoru hesaplandi — T2 senaryo agirliklarina aktarilacak
[ ] Makro varsayimlar belirlendi — terminal buyume tavani icin
[ ] Peer benchmark tablosu olusturuldu — buyume/marj Q25/med/Q75
[ ] Senaryo narratif sablonu dolduruldu (Bear/Base/Bull hikayeleri)
[ ] Tum T1 ciktilari T2 handoff formatinda hazir
[ ] Yonetim rehberligi KANTITATIF yakalandi — guncel deger tablosu + tarihsel isabet tablosu + G skoru hesaplandi (bkz. §4A) [v2.3]
[ ] T1→T2 Guidance Aktarim Paketi research.md'ye eklendi (G_SKORU, GUNCEL_REHBERLIK, EGRILIM) [v2.3]
[ ] Yatirim dongusu tespiti yapildi — buyume/olgun/toparlanma rejimi belirlendi [v2.2]
[ ] Katalist takvimi dolduruldu — en az 3 Bull + 3 Bear katalist, tarihli [v2.2]
[ ] Bottom-up segment buyume kirilimi hazir — top-down formul ile karsilastirilacak [v2.2]
[ ] Yapisal Analiz Tetikleyicileri tamamlandi — tespit edilen tetikleyiciler T2'ye aktarildi [v2.4]
[ ] Broker rapor konsensus tablosu hazirlandi — en az 3 kurum raporu ozetlendi [v2.4]
[ ] Kuresel peer listesi olusturuldu — en az 2-3 uluslararasi peer belirlendi [v2.4]
```

### 13.4 Yapisal Analiz Tetikleyicileri [v2.4]

**Amac:** T1 arastirmasi sirasinda sirketin yapisal ozelliklerini tespit ederek, T2'de ZORUNLU ek analiz kalemleri olusturmak. Her tetikleyici, T2'de spesifik bir analiz uretir.

**KURAL:** Asagidaki kosullardan herhangi biri gecerliyse, ilgili analiz T2'de ZORUNLU hale gelir ve T5'te rapora eklenir.

| Tetikleyici Kosul | T2'de Zorunlu Analiz | T5'te Rapor Bolumu | Ornek |
|---|---|---|---|
| Zarar eden cografi segment var | Segment Breakeven Analizi: kac yil, kac lokasyon, hangi hasilat seviyesinde kara gecer | Sirket Profili altinda ayri baslik | EBEBK UK operasyonu |
| Yeni is kolu / urun hatti lansmani | Unit Economics / Payback Analizi: birim bazinda gelir-maliyet, geri odeme suresi | Buyume Suruculeri altinda | Yeni urun kategorisi |
| Son 3 yilda M&A gerceklestirmis | Serefiye Risk Analizi + Entegrasyon Degerlendirmesi: serefiye/toplam varlik orani, deger dusukluğu riski | Finansal Analiz altinda | EBEBK Tuna Cocuk |
| Buyuk kapasite yatirimi devam ediyor | Kapasite Utilizasyon ve ROI Analizi: mevcut vs planlanan kapasite, yatirim getirisi | Projeksiyon Varsayimlari altinda | Fabrika / depo yatirimi |
| Yurtdisi hasilat payi >%5 veya hizla artiyor | Cografi Segment Detay Analizi: FX riski, transfer fiyatlama, yerel regulasyon | Risk Degerlendirmesi altinda | Ihracat agirlikli sirket |
| Tek musteri/tedarikci payi >%20 | Yogunlasma Riski Analizi: top-5 musteri/tedarikci, alternatif kaynak | Risk Degerlendirmesi altinda | B2B sirketler |
| Duzenlemeye tabi sektor (EPDK, BDDK, TAPDK vb.) | Regulasyon Etki Analizi: fiyat tavanlari, lisans gereksinimleri, uyum maliyeti | Sektor & Rekabet altinda | Enerji, banka, tutun |
| Halka arz sonrasi ilk 2 yil | Lock-up ve Sulanma Analizi: kilit donem bitisleri, potansiyel ikincil arzlar | Ortaklik Yapisi altinda | Yeni halka arz |

**T1→T2 Aktarim Formati:**

```
YAPISAL ANALIZ TETIKLEYICILERI:
[ ] Zarar eden cografi segment: [Evet/Hayir] → Detay: [segment adi, zarar tutari]
[ ] Yeni is kolu/urun: [Evet/Hayir] → Detay: [urun/kanal adi, lansman tarihi]
[ ] M&A gecmisi: [Evet/Hayir] → Detay: [edinim adi, yil, serefiye tutari]
[ ] Kapasite yatirimi: [Evet/Hayir] → Detay: [yatirim turu, tutar, tamamlanma]
[ ] Yurtdisi hasilat >%5: [Evet/Hayir] → Detay: [ulkeler, hasilat payi, trend]
[ ] Musteri/tedarikci yogunlasmasi: [Evet/Hayir] → Detay: [top musteri payi]
[ ] Regulasyona tabi: [Evet/Hayir] → Detay: [duzenleme kurumu, etki alani]
[ ] Yeni halka arz: [Evet/Hayir] → Detay: [halka arz tarihi, lock-up bitisi]
```

### 13.5 Broker Rapor Konsensus Cikarimi [v2.4]

**Amac:** T1'de okunan kurum raporlarindan (Marbas, Deniz, KT, Pusula vb.) hedef fiyat ve tahminleri cikartarak bir konsensus tablosu olusturmak.

**KURAL:** T1 arastirmasi sirasinda en az 3 farkli kurum raporu okunmusssa, asagidaki tablo doldurulur ve T5'e aktarilir.

```
KONSENSUS KARSILASTIRMA TABLOSU:

| Kurum | Tarih | Tavsiye | Hedef Fiyat | FY+1 Hasilat | FY+1 FAVÖK | FY+1 Net Kar |
|-------|-------|---------|-------------|-------------|-----------|-------------|
| [Kurum 1] | [tarih] | [AL/TUT/SAT] | [X TL] | [Y mn] | [Z mn] | [W mn] |
| [Kurum 2] | [tarih] | [AL/TUT/SAT] | [X TL] | [Y mn] | [Z mn] | [W mn] |
| [Kurum 3] | [tarih] | [AL/TUT/SAT] | [X TL] | [Y mn] | [Z mn] | [W mn] |
| Konsensus Medyan | — | — | [medyan] | [medyan] | [medyan] | [medyan] |
| **BBB Research** | [tarih] | [tavsiye] | [hedef] | [tahmin] | [tahmin] | [tahmin] |
| BBB vs Konsensus | — | — | [+/-%X] | [+/-%X] | [+/-%X] | [+/-%X] |
```

**NOT:** Eger kurum raporlari IAS 29 duzeltmeli vs nominal farkli bazda raporluyorsa, baz farki dipnot olarak belirtilir.

### 13.6 Kuresel Peer Secimi [v2.4]

**Amac:** Yerli BIST peer'larin yanina en az 2-3 uluslararasi esenik sirket ekleyerek degerleme karsilastirmasini derinlestirmek.

**KURAL:** T1 sirasinda yahoo-finance skill'i veya web arastirmasi ile kuresel peer'lar belirlenir.

**Secim Kriterleri:**

| Kriter | Yerli Peer | Kuresel Peer |
|--------|-----------|-------------|
| Sayi | 3-5 BIST sirketi | 2-3 uluslararasi |
| Kaynak | Is Yatirim | Yahoo Finance / web |
| Carpan hesabi | TL bazinda | Yerel para birimi bazinda (birimsiz carpan) |
| Buyukluk filtresi | Ayni BIST segmenti | PD ±200% kabul edilebilir |

**Kuresel Peer Secim Sureci:**

1. Alt-sektor tanimini belirle (ornek: "baby & children specialty retail")
2. Yahoo Finance'de sector screening yap veya web arastir
3. En az 2, ideal 3 kuresel peer sec
4. Her peer icin: PD, FD/FAVÖK, F/K, Buyume, Brut Marj kaydet
5. T3'te comps tablosuna "Kuresel Peer" basligı altinda ekle

**Ornek Kuresel Peer Haritasi:**

| Sektor | Potansiyel Kuresel Peer'lar |
|--------|---------------------------|
| Bebek perakende | Carter's (US), Mothercare (UK), Smyths Toys (UK/EU) |
| Gida perakende | Walmart (US), Tesco (UK), Carrefour (FR) |
| Moda perakende | H&M (SE), Inditex (ES), Fast Retailing (JP) |
| Tutun/icecek | BAT (UK), PMI (US), AB InBev (BE) |
| Cimento | LafargeHolcim (CH), HeidelbergCement (DE) |

---

## Versiyon Geçmişi

**Mevcut:** v2.4 (2026-03-23)

| Tarih | Versiyon | Özet |
|-------|----------|------|
| 2026-03-23 | **v2.4** | §13.4 Yapisal Analiz Tetikleyicileri eklendi (8 tetikleyici + T2 handoff), §13.5 Broker Rapor Konsensus Cikarimi eklendi, §13.6 Kuresel Peer Secimi eklendi (min 2-3 uluslararasi peer), §13.3 checklist guncellendi |
| 2026-03-22 | **v2.3** | §4A eklendi: Yonetim Rehberligi Kantitatif Yakalama — guncel guidance degerleri tablosu, tarihsel isabet tablosu, G skoru hesaplama, T1→T2 Guidance Aktarim Paketi. senaryo-metodoloji.md §2A.1 formulunun ham veri ihtiyacini karsilar. §13.1 aktarim tablosu ve §13.3 checklist guncellendi |
| 2026-03-22 | **v2.2** | Bolum 13 genisletildi: Sirkete ozgu girdi katmani (yonetim rehberligi, yatirim dongusu, katalist takvimi, bottom-up segment dogrulamasi, sirket rejimi) — senaryo-metodoloji.md v2.0 ile uyumlu |
| 2026-03-22 | **v2.1** | Bolum 13 eklendi: T1→T2 Senaryo Koprusu — Risk Etki Matrisi, MQS, Katalizor Takvimi ciktilarini T2 senaryo parametrelerine baglayan aktarim tablosu, narratif sablonu ve kontrol listesi |
| 2026-03-19 | v2.0 | 8→9 bölüm (Şirket Profili + Ürün Portföyü ikiye bölündü), kelime harmonizasyonu |
| 2026-03-18 | v1.1-1.5 | Yönetim kaynakları, Kaynak Güncelliği, 2-Aşama Kuralı, PDF okuma, İlker feedback |
| 2026-03-17 | v1.0 | İlk oluşturma |

**Tam changelog:** `references/changelog.md`
