# T5: Rapor Montajı — Detaylı Workflow

> **Rapor fiziksel yapısı (sayfa layout, chart embed haritası):** `references/c2-tam-kapsama/rapor-sablonu.md`
> **DOCX formatlama kuralları:** `references/c2-tam-kapsama/profesyonel-cikti-rehberi.md`
> **Kalite kontrol:** `references/c2-tam-kapsama/kalite-kontrol-listesi.md`

Bu doküman equity-analyst skill'inin T5 (Rapor Montajı) görevini tek bir doğrusal workflow olarak tanımlar.
Tüm içerik yazımı ve DOCX birleştirmesi **Faz A-G** sırasıyla, tek akışta yapılır.

---

## 🔥 KRİTİK TALİMAT: TOKEN TASARRUFU YAPMA, KISALTMA YAPMA

**BU FİNAL ÇIKTIDIR. TÜM GÜCÜNLE YAZ. KISAYOL YOK.**

4 önceki task'ı tamamladıktan sonra bu final task her şeyi yayın kalitesinde kurumsal araştırmaya dönüştürür.

### Mutlak Gereksinimler

**YAP:**
- ✅ **Gereken tüm token bütçesini KULLAN** — Bunun için var
- ✅ **HER bölümü TAM yaz** — Özet değil, placeholder değil, TAM İÇERİK
- ✅ **TÜM 25-35 grafiği GÖM** — T4'ten her grafiği doküman boyunca yerleştir
- ✅ **TÜM 12-20 tabloyu OLUŞTUR** — T2/T3'ten her finansal tabloyu çıkar
- ✅ **T1 içeriğini DERECELİ AKTAR** — Olgusal içerik (tarih, isim, rakam) aynen kopyala. Analitik içerik (değerlendirme, pozisyonlama) ilk geçiş yerinde tam kullan, sonraki bölümlerde kısa referans + yeni açı. (raporun %35-45'i)
- ✅ **Projeksiyon Varsayımlarını 2.000-3.000 kelime yaz** — Ürün-ürün, bölge-bölge detay
- ✅ **Senaryo Analizini 1.500-2.000 kelime yaz** — Spesifik İyimser/Baz/Kötümser parametreleri
- ✅ **Toplam 10.000-16.000 kelimeye ULAŞ** — Bu MİNİMUM, öneri değil
- ✅ **Minimum 30-50 sayfa ÜRET** — Her 200-300 kelimede grafik ile yoğun metin

**YAPMA:**
- ❌ "Detaylar için modele bakınız..." — HER varsayımı, her parametreyi TAM yaz
- ❌ "Burada grafik yerleştirilecektir..." — GERÇEK GRAFİĞİ YERLEŞTİR
- ❌ "Finansal tablo eklenecektir..." — GERÇEK TABLOYU OLUŞTUR
- ❌ "Bu bölüm daha sonra tamamlanacaktır..." — ŞİMDİ TAMAMLA
- ❌ Bölümleri özetlemek veya kısaltmak — TAM İÇERİK yaz
- ❌ T1 olgusal içeriğini yeniden yazmak — tarihçe, veriler, biyografiler AYNEN kopyala. Analitik içerik ise first-mention-full prensibiyle aktarılır (aynı açıklamayı 2+ bölümde tekrarlama).

**Standart:**
- **Eksiksiz**: Her bölüm minimum kelime hedefini karşılamalı
- **Kantitatif**: Her iddia sayıyla desteklenmeli
- **Kapsamlı**: Tüm veriler çıkarılmış, tüm grafikler gömülmüş
- **Profesyonel**: Doğru formatlama, kaynaklar, tablolar, grafikler her yerde
- **Yoğun**: %60-80 sayfa doluluğu, her sayfada metin ve görsel

---

## Girdi Doğrulama

**⚠️ TASK 1-4'ÜN TAMAMI TAMAMLANMADAN BU TASK'I BAŞLATMA.**

Placeholder içerik oluşturmaya, eksik bölümleri ikame etmeye veya eksik bir rapor birleştirmeye TEŞEBBÜS ETME.

### Ön Koşul Kontrol Listesi

```
GİRDİ DOĞRULAMA
================
- [ ] Şirket araştırma dokümanı mevcut? ({TICKER}_research.md, 6-8K kelime)
- [ ] Yönetim biyografileri tamam? (150-400 kelime × 3-4 yönetici)
- [ ] Finansal model mevcut? ({TICKER}_DCF_Model.xlsx, 6 tab)
- [ ] Finansal analiz dokümanı mevcut? ({TICKER}_financial_analysis.md)
- [ ] Değerleme analizi mevcut? ({TICKER}_valuation_comps.md)
- [ ] DCF analizi sensitivity tablosuyla tamam?
- [ ] Comps tablosu istatistiksel özetle tamam? (maks/75./medyan/25./min)
- [ ] 25-35 grafik dosyası mevcut? (charts_v2/ veya charts/)
- [ ] 4 zorunlu grafik mevcut? G03 ☐  G04 ☐  G28 ☐  G32 ☐
- [ ] Grafik dizini (chart_index.txt) mevcut?
- [ ] T1 Yapısal Analiz Tetikleyicileri kontrol edildi? (varsa ilgili bölümler rapora eklendi) [v2.1]
- [ ] T1 Konsensüs Karşılaştırma tablosu mevcut? (en az 3 kurum raporu) [v2.1]
- [ ] T1 Küresel peer listesi mevcut? (en az 2-3 uluslararası peer) [v2.1]
- [ ] T2 Forward bilanço/nakit akış sütunu mevcut? (en az FY+1T) [v2.1]
```

**EĞER TASK 1, 2, 3 VEYA 4'TEN HERHANGİ BİRİ TAMAMLANMADIYSA:** Hemen dur ve kullanıcıya hangi task'ların önce tamamlanması gerektiğini bildir.

### Beklenen Klasör Yapısı

```
research/companies/{TICKER}/
├── {TICKER}_research.md                    (Task 1)
├── {TICKER}_financial_analysis.md          (Task 2)
├── {TICKER}_DCF_Model.xlsx                 (Task 2/3)
├── {TICKER}_valuation_comps.md             (Task 3)
├── charts_v2/                              (Task 4)
│   ├── {TICKER}_G01_fiyat_performansi.png
│   ├── ... (25-35 grafik)
│   ├── {TICKER}_G28_dcf_sensitivity.png    ⭐ ZORUNLU
│   ├── {TICKER}_G32_football_field.png     ⭐ ZORUNLU
│   ├── {TICKER}_EK01-EK07.png             (destek grafikler — ilgili bölümlere gömülür, Ekler'e DEĞİL)
│   └── chart_index.txt
└── {TICKER}_rapor_metin.md                 (varsa T5 taslak)
```

### İçerik Envanteri

Girdi doğrulaması geçtikten sonra aşağıdaki envanteri doldur:

```
İÇERİK ENVANTERİ
=================
T1 kelime sayısı: _____ (hedef: 6.000-8.000)
T1 bölüm sayısı: _____
T2 tablo sayısı: _____
T2 segment kırılımı: MEVCUT / KISITLI / YOK
T2 coğrafi kırılım: MEVCUT / KISITLI / YOK
T3 adil deger tahmini: _____ TL, tavsiye: _____
T3 comps istatistiksel özet: MEVCUT / YOK
T4 grafik sayısı: _____ (hedef: ≥25)
T4 zorunlu 4 grafik: G03 ☐  G04 ☐  G28 ☐  G32 ☐

YENİ YAZIM GEREKEN BÖLÜMLER:
- [ ] Yatırım tezi (800-1.200 kel)
- [ ] Büyüme sürücüleri (800-1.200 kel)
- [ ] Tarihsel finansal analiz yorumu (1.200-1.800 kel)
- [ ] Projeksiyon varsayımları narratif (2.000-3.000 kel) ⭐
- [ ] Senaryo analizi detaylı (1.500-2.000 kel) ⭐
- [ ] Değerleme metodolojisi (800-1.200 kel)
- [ ] Adil değer tahmini & değerleme görüşü (300-500 kel)
- [ ] Yatırım özeti / Sayfa 1 (500-700 kel — EN SON yazılacak)
```

---

## Rapor Spesifikasyonları

### Uzunluk Gereksinimleri
- **Sayfa**: 30-50 (MİNİMUM 30 sayfa)
- **Kelime sayısı**: 10.000-16.000 kelime (MİNİMUM 10.000)
- **Grafik**: 25-35 gömülü PNG görseli
- **Tablo**: 12-20 kapsamlı finansal tablo
- **Yoğunluk**: %60-80 sayfa doluluğu

### Bölüm Kelime Hedefleri

| Bölüm | Min | Hedef | Kaynak | Faz | Kritik? |
|-------|-----|-------|--------|-----|---------|
| Yatırım Özeti (Sayfa 1) | 500 | 700 | Yeni yazım | F | |
| Yatırım Görüşü | 800 | 1.200 | Yeni yazım | B | |
| Risk Değerlendirmesi | 600 | 900 | T1 + reorganize | B | |
| Şirket Profili | 500 | 800 | T1 §2 kopyala | B | |
| Ürün/Hizmet Portföyü | 500 | 700 | T1 §3 kopyala | B | |
| Yönetim Analizi | 500 | 700 | T1 §4 kopyala | B | |
| Büyüme Sürücüleri (S.13-14) | 800 | 1.200 | Yeni yazım | B | |
| Sektör & Rekabet | 1.000 | 1.400 | T1 §5+§8 kopyala | B | |
| Moat Analizi | 600 | 900 | T1 §6 kopyala | B | |
| Tarihsel Finansal Analiz | 1.200 | 1.800 | Yeni yazım | C | |
| **Projeksiyon Varsayımları** | **2.000** | **3.000** | **Yeni yazım** | **C** | ⭐ |
| **Senaryo Analizi** | **1.500** | **2.000** | **Yeni yazım** | **C** | ⭐ |
| Değerleme Metodolojisi | 800 | 1.200 | Yeni yazım | D | |
| Adil Değer Tahmini & Değerleme Görüşü | 300 | 500 | Yeni yazım | D | |
| **TOPLAM** | **~12.000** | **~17.000** | | | |
| └ Yeni yazım toplamı | ~8.300 | ~12.500 | | | |
| └ T1 kopyala toplamı | ~3.700 | ~5.500 | | | |

**Not:** T1 olgusal bölümleri olduğu gibi alınır. Analitik bölümler Faz 0 Tekrar Haritası'na göre aktarılır: ilk geçiş yerinde tam, sonraki geçişlerde referans + farklı perspektif. Yeniden yazma eforunu kantitatif bölümlere (projeksiyon, senaryo, değerleme) yönlendir. T1 bölüm numaraları (§2-§8): T1'deki 9-bölüm yapısına karşılık gelir.

---

## Rapor Montaj Felsefesi

### Mimari Kural

```
ANA AGENT içeriği YAZAR → rapor-uret.py FORMATLAR → DOCX çıkar

YANLIŞ: Subagent → assembly.py yaz → Python çalıştır
DOĞRU:  Ana agent → source oku → içerik yaz → rapor-uret.py import et → exec çalıştır
```

### İçerik Tekrar Kullanım Stratejisi

- **T1 içeriği (raporun %40-50'si)**: .md dosyasını oku → Word formatına dönüştür → grafik ekle
- **T2/T3 verileri (raporun %15-20'si)**: Dosyaları oku → tabloları çıkar → yorum yaz
- **Yeni yazım (raporun %30-40'si)**: Yatırım tezi, projeksiyon varsayımları, senaryo analizi, değerleme

### Yoğunluk Hedefi

%60-80 sayfa doluluğu:
- Her sayfada HEM metin HEM görsel olmalı
- Grafikler metin boyunca dağıtılmalı, gruplanmış DEĞİL
- Her 200-300 kelimede 1 grafik
- Tablolar büyük metin bloklarını bölümlemeli

```
İyi sayfa düzeni:                   KÖTÜ — Kaçınılacak:
┌─────────────────────────────┐     - Sadece tek grafik olan tam sayfa
│ Bölüm Başlığı               │     - Birden fazla saf metin sayfası
│ Metin paragrafı (200 kel)   │     - Bölümlerin sonunda gruplanmış
│ [Gömülü grafik]             │       grafikler
│ Metin paragrafı (200 kel)   │
│ [Gömülü tablo]              │
│ Metin paragrafı (200 kel)   │
│ [Gömülü grafik]             │
└─────────────────────────────┘
```

### rapor-uret.py Fonksiyonları

```python
import os, sys
from importlib.machinery import SourceFileLoader

mod = SourceFileLoader('rapor_uret',
    os.path.expanduser('~/.openclaw/workspace/skills/equity-analyst/scripts/rapor-uret.py')
).load_module()

# Doküman oluşturma
doc = mod._doc_olustur()                        # Yeni doküman
mod.header_footer_ekle(doc, '{ŞİRKET} Raporu')  # Header/footer

# İçerik ekleme
mod._baslik(doc, text, level=1|2|3, sayfa_sonu=None)  # Başlık (H1: sayfa_sonu=True default, False ile override)
mod._paragraf(doc, text, ...)                    # Paragraf
mod.tablo_ekle(doc, basliklar, satirlar, kaynak) # Tablo (keep_with_next aktif)
mod.grafik_ekle(doc, yol, boyut, baslik)         # Grafik (TAM|YARIM|GRID|KÜÇÜK, keep_with_next aktif)
mod.cift_grafik(doc, sol_yol, sag_yol, ...)      # Yan yana grafik (keep_with_next aktif)

# Özel sayfalar
mod.kapak_sayfasi(doc, ticker, ...)              # Sayfa 1
mod.finansal_tablo_grid(doc, ...)                # Dual-column tablo
mod.grafik_ozet_sayfasi(doc, grafikler)          # 2×3 grid
mod.add_hyperlink(p, display_text, url)          # Tıklanabilir link
mod.kaynaklar_sayfasi(doc, {...})                # Sources sayfası
mod.yasal_uyari(doc)                             # Son sayfa
mod.icindekiler_ekle(doc)                        # TOC field
mod._sayfa_sonu(doc)                             # Sayfa sonu
```

---

## FAZ 0: ARGÜMAN İNŞASI (Assembly Öncesi — RAPORUN EN KRİTİK ADIMI)

**Bu faz raporun düşünce omurgasını kurar.** Assembly (Faz A-H) bu omurganın fiziksel ifadesidir.
Faz 0'ı yüzeysel doldurmak = 30+ sayfalık raporu temelsiz yazmak. BURADA düşün, sonra yaz.

> **SOUL.md Hizalaması:** Düşünce sürecimiz "Topla, Sentezle, Sorgula, Güncelle" sırasını takip eder.
> Faz 0, "Sentezle" ve "Sorgula" adımlarının T5 öncesi son kontrol noktasıdır.

### Adım 1: Çelişki Matrisi'ni Oku ve Rapor Eşlemesi Yap

**T3'te Çelişki Matrisi zaten oluşturuldu.** Dosya: `research/companies/{TICKER}/{TICKER}_celiski_matrisi.md`

1. Matrisi oku. Her ✗ hücresinin çözüm yolunu gözden geçir.
2. Her çözümü raporun hangi bölümüne ve paragrafına yazacağını EŞLE:

```
ÇELİŞKİ → RAPOR EŞLEMESİ
===========================
Çelişki 1: [Risk adı] × [Varsayım adı]
  Çözüm: [matristeki çözüm]
  Raporda nerede: [Bölüm adı, paragraf numarası, nasıl ifade edilecek]

Çelişki 2: ...
```

3. Eşlenemeyen çelişki varsa → bu bölüm eksik demektir. Faz A'da yapıya ekle.

**⛔ GATE:** T3'teki matris en az 2 çelişki içermeli. Matris dosyası yoksa veya yetersizse → T3'e geri dön, matrisi tamamla.
T5 assembly sırasında YENİ matris oluşturmak YASAK — T3'teki kilitli matrisi kullan.

### Adım 2: Ana Argüman (3 Paragraf Testi)

Bu raporu 3 paragrafta yazacak olsan:

```
ANA ARGÜMAN
============
PARAGRAF 1 — TEZ (tek cümle):
[Bu şirket neden yatırım yapılabilir/yapılamaz?]

PARAGRAF 2 — KANIT (3 veri noktası, HER BİRİ T1+T2+T3'ten birer eleman birleştirerek):
Kanıt 1: [T1 bulgusu] + [T2 kanıtı] + [T3 değerleme etkisi]
Kanıt 2: [T1 bulgusu] + [T2 kanıtı] + [T3 değerleme etkisi]
Kanıt 3: [T1 bulgusu] + [T2 kanıtı] + [T3 değerleme etkisi]

PARAGRAF 3 — KARŞI-TEZ:
[Bu tez neden yanlış olabilir? En kırılgan varsayım hangisi?
Kırılırsa sonuç ne kadar değişir? (sayıyla)]
```

**3 Paragraf Testi:** Bu 3 paragrafı okuyan biri, raporu okumadan yatırım kararının
özünü anlayabilmeli. Anlayamıyorsa tez net değil; yeniden yaz.

### Adım 3: Argüman Dalları ve Bölüm Eşleme

Ana tezi destekleyen 3-5 dal ve en az 2 karşı-tez dalı tanımla.
Her rapor bölümünün en az 1 dala bağlı olması zorunlu.

```
ARGÜMAN DALLARI
================
TEZ DALLARI:
Dal 1: [İsim]
  Kanıt: [T1'den] + [T2'den] + [T3'ten]
  Karşı-argüman: [Bu dalı ne çürütür?]
  Rapor bölümleri: [Yatırım Görüşü pillar 1, Büyüme S.13, Projeksiyon C3 §X]

Dal 2: [İsim]
  Kanıt: [T1+T2+T3]
  Karşı-argüman: [...]
  Rapor bölümleri: [...]

Dal 3-5: ...

KARŞI-TEZ DALLARI (en az 2):
Karşı-dal 1: [İsim]
  Tetikleyici: [Hangi olay/veri bunu tetikler?]
  Etki: [Sayıyla — hedef fiyat ne olur?]
  Rapor bölümleri: [Risk B2, Kötümser senaryo C4]

Karşı-dal 2: ...

BÖLÜM-DAL EŞLEMESİ:
Hiçbir dala bağlanmayan bölüm = gereksiz bölüm. Kaldır veya dalına bağla.
```

### Adım 4: Piyasa Karşılaştırması

```
PİYASA KARŞILAŞTIRMASI
=======================
Mevcut fiyat: ___ TL  |  PD: ___ mrd TL  |  FD: ___ mrd TL
Consensus: EV/EBITDA ___x  |  F/K ___x  |  Büyüme beklentisi %___
Piyasanın ima ettiği varsayımlar (ters İNA): büyüme %___, marj %___

Analizimiz piyasayla:
  Örtüşme: [hangi varsayımlarda hemfikiriz — bunlar da değerli bulgu]
  Ayrışma: [varsa — her biri için NEDEN: hangi veri/varsayım farkı?]
  (Ayrışma zorunlu değil. "Adil fiyatlanmış" da bir sonuç.)

Olasılık ağırlıklı adil değer: ___ TL
En kırılgan 3 varsayım: (1)___ (2)___ (3)___
En önemli 3 katalizör + zamanlama: (1)___ (2)___ (3)___
```

### Adım 5: Tekrar Haritası — Kilit Fact'lerin Bölüm Dağılımı

T1 research.md'yi oku ve en çok tekrarlanan 5 veri noktasını belirle. Her biri için rapordaki İLK GEÇİŞ YERİNİ ve sonraki bölümlerde HANGİ FARKLI AÇIDAN işleneceğini planla.

| Veri Noktası | İlk Tam Geçiş (Bölüm) | Sonraki Geçişler (kısa ref + yeni açı) |
|---|---|---|
| Örn: Öz marka %54,3 | Yatırım Tezi (marj koruması) | Ürün: kategori dağılımı / Finansal: baz puan etkisi / Projeksiyon: %58-60 hedef |
| Örn: IAS 29 etkisi | Yatırım Tezi (opaklık) | Finansal: GAAP vs Op. EBIT farkı / Kazanç Kalitesi: F/K distorsiyonu / Değerleme: EBIT baz yılı seçimi |

Bu tablo yazılmadan Faz A'ya geçilmez.

**Faz 0 Çıktı Dosyası:** Tüm Faz 0 çıktısını `research/companies/{TICKER}/{TICKER}_faz0_arguman.md` dosyasına yaz.
Bu dosya rapor boyunca referans noktası olarak kullanılacak. DOCX'e GİRMEZ; assembly'nin düşünce haritasıdır.
Faz B/C/D gate'lerindeki omurga kontrolleri bu dosyayı referans alır.

**⛔ FAZ 0 MASTER GATE:** Aşağıdakilerin TAMAMI tamamlanmadan Faz A'ya geçilmez:
- [ ] T3 Çelişki Matrisi (`{TICKER}_celiski_matrisi.md`) okundu ve rapor eşlemesi yapıldı
- [ ] Ana Argüman 3 paragraf testi yazıldı ve geçti
- [ ] En az 3 tez dalı + 2 karşı-tez dalı tanımlandı
- [ ] Her rapor bölümü en az 1 dala eşlendi
- [ ] Piyasa karşılaştırması yazıldı
- [ ] Tekrar Haritası (5 kilit fact) dolduruldu

---

## T1 ICERIK AKTARIM PROTOKOLU

T1 icerigi 2 kategoriye ayrilir:

| Kategori | Icerik Tipi | T5'te Ne Olur |
|----------|------------|---------------|
| **Olgusal** | Sirket tanimi, tarihce, yonetim biyografileri, urun listesi, magaza sayilari, somut veriler | Buyuk olcude korunur (kucuk akis duzenlemeleriyle) |
| **Analitik** | Sektor degerlendirmesi, moat analizi, rekabet pozisyonlama, buyume gorunumu | T2/T3 perspektifiyle yeniden sentezlenir |

**Analitik Kopru:** Her T1 analitik bolumune 2-3 cumlelik "Analitik Kopru" eklenir. Bu kopru, T2/T3 modelleme surecinde ortaya cikan icgoruyu ilgili T1 bolumuyle baglar.

Ornek:
> [T1 olgusal: Ebebek 304 magazayla Turkiye'nin en buyuk bebek perakendecisi...]
> [Analitik Kopru: Finansal modelimiz, magaza aginin olcek avantajini FAVOK marji uzerinden kantitatif olarak dogruluyor. DCF modelimizde bu marj avantajinin terminal degerin %35'ini olusturdugunu hesapliyoruz.]

**KURAL:** T1 olgusal icerigi yeniden YAZILMAZ. Analitik kopruler EKLENIR.

### Tekrar Onleme Kurallari (First-Mention-Full Prensibi)

1. **Ilk bahsis tam:** Bir veri noktasi (oz marka %54, pazar payi %14,6, IAS 29 etkisi vb.) raporda ILK gectigi yerde 2-3 cumleyle tam aciklanir.

2. **Sonraki bahsis kisa + yeni aci:** Ayni veri noktasi baska bolumde gectiginde:
   - Kisa referans: "Guclu oz marka penetrasyonu (bkz. S.3)" VEYA tek cumle hatirlatma
   - YENI perspektif: O bolume ozgu farkli bir aci (farkli metrik, zaman dilimi, karsilastirma)
   - AYNI 2-3 cumlelik aciklamayi TEKRARLAMA

3. **icgoru_kutusu istisnasi:** TEMEL BULGU / DIKKAT / OLUMLU GOSTERGE kutulari bolum girisi summary niteliginde — buradaki tekrarlar tolere edilir.

4. **Terim vs Aciklama ayrimi:** "IAS 29" terimi gecebilir (sinirsiz). Ama "IAS 29 operasyonel gercekligi maskeliyor, parasal pozisyon kaybi 1.891M TL..." seklindeki TAM ACIKLAMA raporda MAX 2 kez gecer.

Ornek — DOGRU:
> Yatirim Tezi: "IAS 29 hiperenflasyon muhasebesi, GAAP EBIT (513M TL) ile operasyonel EBIT (2.404M TL) arasinda 4,7x fark yaratmaktadir. Yatirimcilarin nakit bazli metriklere odaklanmasini tavsiye ediyoruz." (TAM ACIKLAMA — ILK GECIS)

> Finansal Analiz: "IAS 29 etkisi nedeniyle operasyonel EBIT referans alinmistir (detay: Yatirim Tezi, S.3)." (KISA REFERANS)

> Kazanc Kalitesi: "IAS 29 distorsiyonu, F/K carpanini yaniltici kilmaktadir — duzeltilmis F/K 8,5x ile peer medyaninin cok altindadir." (YENI ACI — carpan etkisi)

---

## FAZ A: Yapı Oluştur + Sayfa 1 Şablonu

**Çıktı:** Boş DOCX iskeleti — Sayfa 1 yapısı hazır (içerik Faz F'de yazılacak)

```python
doc = mod._doc_olustur()
mod.header_footer_ekle(doc, 'Şirket Raporu — {ŞİRKET_ADI}')

# Sayfa 1: Kapak (yapısı ÖNCE oluşturulur, içerik EN SON yazılır — Faz F)
# ⚠️ KAPAK VERİ KAYNAĞI KURALI (v4.9 + v4.14):
#   Kapak sayfasındaki HİÇBİR rakam kafadan yazılamaz!
#   - Finansal özet tablosu → T2 Excel finansal modelden birebir
#   - Çarpanlar → T2 + T3 DCF modelinden hesaplanmış
#   - Tez pillar metni → T1 araştırma dokümanından sentez
#   - Net Kâr "—" YAZILMAZ eğer T2 modelinde projeksiyon varsa
#   - FCF negatifse '(42)' veya 'n.m.' yaz, "—" ile atla YASAK
#   - FAVÖK metodolojisi assembly'de yorum satırında belirtilmeli
# ⚠️ PİYASA BİLGİLERİ VERİ KAYNAĞI KURALI (v4.14):
#   Aşağıdaki 4 veri yfinance'tan otomatik çekilmelidir — elle girilmesi YASAKTIR:
#   - mevcut_fiyat → yf.Ticker('{TICKER}.IS').history(period='5d')['Close'].iloc[-1]
#   - hafta52 → yf.Ticker('{TICKER}.IS').history(period='1y') min/max
#   - gunluk_hacim → 3 aylık ortalama hacim × ortalama fiyat (TL cinsinden)
#   - pd → mevcut_fiyat × toplam pay sayısı (pay sayısı KAP'tan, T1'de mevcut)
#   Elle girilecek veriler: halka_aciklik (KAP), ev (PD + T2 net borç), hedef_fiyat (T3 DCF)
# ⚠️ KAPAK SAYFA DOLULUK KURALI:
#   Sol panel tüm sayfayı doldurmalıdır (min 5 pillar, her biri 4-6 cümle, toplam min 550 kel).
#   Sağ panel: Piyasa Bilgileri + Finansal Özet + Çarpanlar + Ortaklık Yapısı + Grafik.
#   Tablo başlıkları kısa: "2024", "2025", "2026T" (FY prefix KULLANMA).
# ⚠️ HEADER/FOOTER:
#   rapor_turu: 'ARAŞTIRMA RAPORU' (Kapsam Başlatma değil)
#   analist: '{Ad} (AI Agent)', analist_kurum: '{URL}' (tıklanabilir link)
#   Header sağ: '{Ay Yıl} | BBB Research AI'

# ── Piyasa Verisi Çekme (v4.14 — ZORUNLU) ──
import yfinance as yf
import pandas as pd

_yf = yf.Ticker('{TICKER}.IS')
_yf_bist = yf.Ticker('XU100.IS')  # BIST-100 benchmark (G01 grafiği için de kullanılır)
_yf_hist = _yf.history(period='1y')
_yf_3m = _yf.history(period='3mo')

_mevcut_fiyat = _yf_hist['Close'].iloc[-1]
_hafta52_low = _yf_hist['Low'].min()
_hafta52_high = _yf_hist['High'].max()
_avg_volume_tl = _yf_3m['Volume'].mean() * _yf_3m['Close'].mean()
_pay_sayisi = 160_000_000  # KAP'tan — T1'de doğrulanmış olmalı
_pd_tl = _mevcut_fiyat * _pay_sayisi

mod.kapak_sayfasi(doc, ticker='{TICKER}', sirket_adi='{ŞİRKET_ADI}',
    tarih='{TARİH}', rapor_turu='ARAŞTIRMA RAPORU',
    analist='{Ad} (AI Agent)', analist_kurum='{URL}',
    mevcut_fiyat=f'{_mevcut_fiyat:,.2f}'.replace(',', '.'),  # yfinance
    hedef_fiyat='...',         # T3 DCF çıktısından
    potansiyel='...',          # (hedef - mevcut) / mevcut
    pd=f'{_pd_tl/1e9:.1f} mrd TL',  # hesaplamalı
    ev='...',                  # PD + T2 net borç
    hafta52=f'{_hafta52_low:.0f} – {_hafta52_high:.0f} TL',  # yfinance
    halka_aciklik='...',       # KAP'tan (statik)
    gunluk_hacim=f'{_avg_volume_tl/1e6:.0f}M TL',  # yfinance 3M ortalama
    tez_pillars=[...],  # Faz 0 Argüman Dalları'ndan türetilir. Min 5 pillar, her biri {'baslik': '...', 'metin': '...'}
    finansal_ozet={...},  # T2 Excel modelden — başlıklar: ['', '2024', '2025', '2026T', '2027T']
    carpanlar={...},  # T2+T3 modelden hesaplanmış
    ortaklik_yapisi={...},  # T1 KAP verisi
    degerleme_ozeti='...',  # T3 DCF/Comps çıktısından
    risk_ozeti='...',  # T1 risk analizinden
    grafik_yolu=chart('G01_fiyat_performansi'),
    alt_notlar=[...])

# İçindekiler
mod.icindekiler_ekle(doc)
mod._sayfa_sonu(doc)
```

---

## FAZ B: Yatırım Görüşü, Riskler ve Şirket 101 (S.3-17)

**Çıktı:** ~14-17 sayfa, 10-14 grafik gömülü
**Bu Faz'da yapılan:** Yatırım görüşü (yeni) + risk (T1 + reorganize) + şirket 101 (T1 kopyala + grafik göm) + büyüme görünümü (yeni, S.13-14)

### B1. Yatırım Görüşü (800-1.200 kelime — YENİ YAZIM)

```python
mod._baslik(doc, 'Yatırım Görüşü ve Riskler', level=1)
mod._baslik(doc, 'Yatırım Görüşü', level=2)
```

Faz 0'daki Argüman Dalları'nı tez pillar'larına dönüştür. Her tez dalı = 1 pillar.
- Her pillar: 200-300 kelime
- Faz 0'daki 3 kanıt katmanını (T1 bulgusu + T2 kanıtı + T3 değerleme etkisi) birleştirerek yaz
- Kilit istatistikle başla, finansal etkiyi kantitatif göster
- Zaman çizelgesi dahil et
- Her pillar'ın Faz 0'daki karşı-argümanını 1 cümleyle belirt

### B2. Risk Değerlendirmesi (600-900 kelime — T1 + REORGANİZE)

```python
mod._baslik(doc, 'Risk Değerlendirmesi', level=2)
```

**Tek talimat:** T1'deki risk bölümünü çek, **4 kategoride yeniden organise et**, çıkış kriterleri ekle:

| Kategori | Adet |
|----------|------|
| Şirkete özel riskler | 4-6 |
| Sektör/pazar riskleri | 3-4 |
| Finansal riskler | 2-3 |
| Makroekonomik riskler | 2-3 |

- Her risk: 50-100 kelime açıklama
- Çıkış kriterleri: checkbox formatında, ölçülebilir (min 2 per risk)

### B3. Şirket 101 — T1 Kopyala + Grafik Göm (S.6-12)

**KRİTİK:** T1 araştırma dokümanını neredeyse aynen kullan. YENİDEN YAZMA.

T1'deki şirket araştırması (6-8K kelime) zaten profesyonel, öz içerikli analizdir. Amaç:
1. **Word'e formatla** — Markdown'ı DOCX formatına dönüştür
2. **Grafikleri gömülü yerleştir** — T4'ten ilgili grafikleri metin boyunca ekle
3. **Küçük stil uyarlamaları** — Raporun geri kalanıyla tutarlı formatlama

**T1'den şu OLGUSAL bölümleri çıkar ve aynen kullan (Dereceli Aktarım — olgusal katman):**
- §2 Şirket Profili (500-800 kel) — olgusal, aynen kopyala
- §3 Ürün/Hizmet Portföyü (500-700 kel) — olgusal, aynen kopyala
- §4 Yönetim Analizi (500-700 kel) — olgusal, aynen kopyala

**Grafik Entegrasyon Stratejisi:**
- Her 200-300 kelime metin → 1 grafik ekle
- Şirket 101 bölümü (S.6-12) 6-8 grafik içermeli
- Grafiği tartışan paragraftan hemen sonra yerleştir

**⚠️ Proximity Prensibi (v3.2):**
- **Her grafik, anlattığı hikayenin yanında olmalıdır.** EK grafikler (EK01-EK07) dahil TÜM grafikler ilgili bölüme gömülür.
- Ekler bölümüne grafik "park etme" YASAKTIR. Ekler yalnızca teknik detay tabloları içindir.
- Aynı chart dosyası raporda 2 kez kullanılmamalıdır (duplikasyon yasağı). Tekrar referans gerekiyorsa "(bkz. Grafik N)" metin referansı kullan.
- **Duplikasyon kontrolü:** Aynı konuyu hem grafik hem tablo olarak gösterme — birini seç. Örnek: DCF duyarlılık analizi ya grafik ya tablo olsun, ikisi birden gereksiz.

### Grafik-Bölüm Eşleme Haritası (B3 Şirket 101)

| Rapor Bölümü | T1 Bölüm | Gömülecek Grafik(ler) | Boyut |
|--------------|----------|----------------------|-------|
| Şirket Profili | §2 | G01 fiyat performansı, **EK01 mağaza sayısı** | KÜÇÜK, ORTA |
| Ürün Portföyü | §3 | G03 kategori kırılımı ⭐, G08 ürün portföyü, **EK03 öz marka penetrasyonu** | TAM, YARIM, YARIM |
| Yönetim | §4 | Ortaklık yapısı pasta (varsa) | YARIM |
| Coğrafi | §3 | G04 coğrafi kırılım ⭐ | TAM |

**Python örneği:**

```python
# Şirket Profili — sayfa_sonu=False: önceki bölümle aynı sayfada devam (seyrek sayfa önleme)
mod._baslik(doc, 'Şirket Profili', level=1, sayfa_sonu=False)
mod._paragraf(doc, '[T1 §2 İÇERİĞİNİN BİRİNCİ PARAGRAFI — AYNEN]')
mod.grafik_ekle(doc, 'charts_v2/{TICKER}_G01_fiyat_performansi.png',
    boyut='YARIM', baslik='Hisse fiyatı son 1 yılda %X performans gösterdi')
mod._paragraf(doc, '[T1 §2 İÇERİĞİNİN DEVAMI — AYNEN]')

# Ürün Portföyü
mod._baslik(doc, 'Ürün ve Hizmet Portföyü', level=1)
mod._paragraf(doc, '[T1 §3 İÇERİĞİ — AYNEN]')
mod.grafik_ekle(doc, 'charts_v2/{TICKER}_G03_kategori_kirilimi.png',
    boyut='TAM', baslik='FMCG %33 ile en büyük segment — 5 yılda karına stabil')

# ... Her bölüm için aynı pattern: T1 paragraf → grafik → T1 paragraf → grafik
```

**ÖNEMLİ:** T1'in .md dosyasını OKUYUP gerçek içeriği YAPIŞTIR. Placeholder DEĞİL.

**`sayfa_sonu` kullanım rehberi:**
- H1 başlıklarında default `page_break_before=True` — her ana bölüm yeni sayfada başlar.
- Kısa bölümden sonra gelen H1 için `sayfa_sonu=False` kullanarak seyrek sayfaları önle.
- H2/H3 başlıklarında `keep_with_next` otomatik aktif — sonraki paragrafla aynı sayfada kalır.

**Analitik Kopru Ekleme:** Bu bolum T1'den kopyalandiktan sonra, T2/T3 perspektifinden 2-3 cumlelik baglamsal kopru ekle. Ornegin: sektor analizi bolumune T2'deki pazar buyuklugu projeksiyonunun implikasyonunu, rekabet bolumune T3'teki comps analizi sonuclarini bagla.

### B4. Sektör, Rekabet ve Moat — T1 Kopyala + Grafik Göm (S.15-18)

**T1'den şu ANALİTİK bölümleri çıkar ve Dereceli Aktarım uygula (first-mention-full):**
- §5 Sektör Analizi (1.000-1.400 kel) — analitik, tekrar haritasına göre aktar
- §6 Moat Analizi (600-900 kel) — analitik, tekrar haritasına göre aktar
- §8 Rekabet Pozisyonlaması (500-700 kel) — analitik, tekrar haritasına göre aktar

| Rapor Bölümü | T1 Bölüm | Gömülecek Grafik(ler) | Boyut |
|--------------|----------|----------------------|-------|
| Sektör analizi | §5 | Sektör trendi (varsa), **EK02 pazar payı**, **EK07 büyüme karşılaştırma** | TAM, YARIM, YARIM |
| Moat analizi | §6 | G17 pazar payı dağılımı | YARIM |
| Rekabet | §8 | G16 pozisyonlama, G18 radar | TAM, TAM |

**Analitik Kopru Ekleme:** Bu bolum T1'den kopyalandiktan sonra, T2/T3 perspektifinden 2-3 cumlelik baglamsal kopru ekle. Ornegin: sektor analizi bolumune T2'deki pazar buyuklugu projeksiyonunun implikasyonunu, rekabet bolumune T3'teki comps analizi sonuclarini bagla.

### B5. Büyüme Görünümü (800-1.200 kelime — YENİ YAZIM, S.13-14)

```python
mod._baslik(doc, 'Büyüme Görünümü', level=1)
mod._baslik(doc, 'Büyüme Motorları', level=2)
```

**⚠️ NOT:** Bu bölüm raporda Şirket 101 (S.6-12) sonrasında, Sektör Analizi (S.15) öncesinde konumlanır (S.13-14). Ama assembly sıralamasında Faz B'nin son adımı olarak yazılır.

3-5 kilit sürücü, kantitatif fırsatlarla:
- Her sürücü: 150-250 kelime
- TAM (Toplam Adreslenebilir Pazar) veya pazar penetrasyonu verisiyle destekle
- Zaman çizelgesi ve kilometre taşları
- Modelden destekleyici veri

**Kısa Vadeli (1-2 yıl):** Yeni mağaza/kapasite, e-ticaret, mix değişimi
**Orta Vadeli (3-5 yıl):** Yurt dışı genişleme, M&A, konsolidasyon

```python
mod.grafik_ekle(doc, 'charts_v2/{TICKER}_G15_tam_buyume.png',
    boyut='TAM', baslik='TAM X mrd TL — şirket payı %Y ile genişleme alanı geniş')
mod.grafik_ekle(doc, 'charts_v2/{TICKER}_G19_gelir_koprusu.png',
    boyut='TAM', baslik='Gelir köprüsü: büyüme motorlarının FY2030T katkısı')
```

**⛔ HARD STOP GATE:** Faz B tamamlanmadan Faz C'ye geçme. Kontrol et:
- [ ] Yatırım tezi yazıldı mı? (800+ kelime)
- [ ] Risk bölümü reorganize edildi mi? (4 kategori)
- [ ] T1 §2-§4 kopyalandı mı? (Şirket 101, S.6-12)
- [ ] T1 §5+§6+§8 kopyalandı mı? (Sektör/Moat/Rekabet, S.15-18)
- [ ] Büyüme Sürücüleri yazıldı mı? (800+ kelime, S.13-14)
- [ ] 10-14 grafik gömüldü mü?
- [ ] **OMURGA KONTROLÜ:** Faz 0 Ana Argüman'ı tekrar oku. Bu fazda hangi dalları genişlettim? [Dal listesi]. Daldan sapma var mı? [Evet: neden / Hayır]

---

## FAZ C: Finansal Analiz (S.19-26)

**Çıktı:** ~8-11 sayfa, 5-7 grafik, 6-10 tablo
**Bu Faz'da yapılan:** Tablo çıkarımı + tarihsel analiz (yeni) + projeksiyon varsayımları (yeni ⭐) + senaryo analizi (yeni ⭐)

```python
mod._baslik(doc, 'Finansal Analiz', level=1)
```

### C1. Tablo Çıkarımı — T2/T3'ten

Her tabloyu kaynak dosyadan oku, `rapor-uret.py` ile DOCX'e formatla.

#### Sayfa 1 Finansal Özet Tablosu

Kaynak: `{TICKER}_financial_analysis.md` veya XLS
Çıkarılacak: Hasılat, Brüt Kâr, FAVÖK, Net Kâr, HBK, FCF
Yıllar: FY2022G, FY2023G, FY2024G, FY2025G, FY2026T, FY2027T

```python
mod.tablo_ekle(doc,
    basliklar=['', 'FY22G', 'FY23G', 'FY24G', 'FY25G', 'FY26T', 'FY27T'],
    satirlar=[
        ['Hasılat (mn TL)', '12.450', '18.720', '24.150', '27.675', '32.100', '37.200'],
        ['  YoY Büyüme', '%22', '%50', '%29', '%15', '%16', '%16'],
        ['Brüt Kâr (mn TL)', '...', '...', '...', '...', '...', '...'],
        # ... diğer satırlar
    ],
    kaynak='KAP, BBB Finans, BBB tahminleri. G=Gerçekleşme, T=Tahmin.'
)
```

#### Tam Gelir Tablosu (30-40 kalem)

Kaynak: `{TICKER}_financial_analysis.md` ve/veya BBB Finans
Yıllar: 5Y tarihsel (FY2020G-FY2025G) + 5Y tahmin (FY2026T-FY2030T)

**BIST/KAP gelir tablosu sıralaması:**
```
Hasılat
Satışların Maliyeti
BRÜT KÂR
  Brüt Kâr Marjı %
Genel Yönetim Giderleri
Pazarlama Giderleri
ArGe Giderleri (varsa)
Diğer Faaliyet Gelirleri
Diğer Faaliyet Giderleri
FAALİYET KÂRI / EBIT
  EBIT Marjı %
Amortisman & İtfa
FAVÖK / EBITDA
  FAVÖK Marjı %
Finansman Gelirleri
Finansman Giderleri
Parasal Kazanç/Kayıp (IAS 29)
VERGİ ÖNCESİ KÂR
Vergi Gideri
  ETR %
NET KÂR
  Net Kâr Marjı %
Ana Ortaklık Payı
HBK (TL)
```

#### Gelir Segmentasyonu — Ürün (5-15 satır)

Kaynak: `{TICKER}_financial_analysis.md` segment bölümü.
BIST notu: Segment sayısı genellikle 3-8 (ABD şirketlerinden az).

**Segment MEVCUT ise:** Her ürün kategorisi + yıllar + toplam içi pay (%) + YoY büyüme.

**Segment KISITLI ise:** "Detaylı segment kırılımı kamuya açık değildir" notu ile toplam satır + varsa kategori özetleri.

#### Gelir Segmentasyonu — Coğrafya (2-10 satır)

BIST notu: Çoğu BIST şirketi tek pazarlıdır (Türkiye %95+). Bu durumda 2-3 satırlık kısa tablo yeterlidir.

**Tek pazarlı şirket (EBEBK, TBORG):**
```python
mod.tablo_ekle(doc,
    basliklar=['Bölge', 'FY2025G', 'Pay %'],
    satirlar=[
        ['Türkiye', '27.288', '%98,6'],
        ['Yurtdışı (UK + Erbil)', '387', '%1,4'],
        ['TOPLAM', '27.675', '%100'],
    ],
    kaynak='KAP Faaliyet Raporu'
)
```

**Çok pazarlı şirket (THY, DOCO):** Her bölge ayrı satır, 6-8 bölge + CRP etkisi notu.

#### Diğer Destekleyici Tablolar

Aşağıdaki tablolardan mevcut ve anlamlı olanları çıkar (12-20 tablo hedefi):
- Nakit akış tablosu (20-30 kalem)
- Bilanço özeti (25-35 kalem)
- Operasyonel metrikler tablosu
- Çalışma sermayesi (DSO/DIO/DPO)
- Pazar payı tablosu
- Makroekonomik varsayımlar

### C2. Tarihsel Finansal Analiz (1.200-1.800 kelime — YENİ YAZIM)

```python
mod._baslik(doc, 'Tarihsel Performans', level=2)
```

T2 verisinden tarihsel performansı analiz et. Hasılat, marj, nakit akış trendlerini tartış. Spesifik grafik ve tablolara referans ver.

**Yazım kuralı:** Sayıyla başla, kantitatif ol.
- ✅ "Hasılat FY2022-FY2025 döneminde %30,4 YBBO ile büyüdü, FY2025'te 27.675 mn TL'ye ulaştı."
- ❌ "Şirketin gelirleri güçlü bir büyüme gösterdi."

```python
mod._paragraf(doc, '[1.200-1.800 KELİME YENİ ANALİZ — SAYIYLA BAŞLA]')
mod.grafik_ekle(doc, 'charts_v2/{TICKER}_G02_gelir_brut_marj.png',
    boyut='TAM', baslik='Hasılat 3 yılda 2x büyüdü — premiumlaşma ve mağaza açılışları sürücü')
mod.grafik_ekle(doc, 'charts_v2/{TICKER}_G10_brut_marj_evrimi.png', ...)
mod.grafik_ekle(doc, 'charts_v2/{TICKER}_G12_fcf.png', ...)
# EK grafikleri İLGİLİ bölüme göm (Ekler'e DEĞİL):
mod.grafik_ekle(doc, 'charts_v2/{TICKER}_EK06_stok_optimizasyonu.png',
    baslik='Stok devir hızı iyileşmesi — işletme sermayesi verimliliği')
```

### C3. Projeksiyon Varsayımları (2.000-3.000 kelime — YENİ YAZIM) ⭐ KRİTİK

**🔴 BİRİM ETİKETLEME (ZORUNLU):**
Projeksiyon tablosunda ve metin içinde tüm TL rakamların birimi açıkça belirtilmelidir:
- Tablo başlığı: "Finansal Projeksiyonlar (Reel TL, Aralık {BAZ_YIL} sabit satın alma gücü bazında)" veya "(Nominal TL)" veya "(USD)"
- Büyüme oranları: "(reel)" veya "(nominal)" etiketi ile
- **Guidance Rekonsilasyon Kutusu:** Projeksiyon tablosunun hemen altında veya Hasılat Varsayımları başlangıcında, T2 §6A'daki rekonsilasyonu rapor diline çevirerek sun. Okuyucu 31,8B reel ile 37B nominal arasındaki farkı görebilmeli.
  Şablon: rapor-sablonu.md → "Guidance Rekonsilasyon Kutusu" bölümü

**⛔ YAZMADAN ÖNCE — Çelişki Matrisi Kontrolü (ZORUNLU):**
T3'te oluşturulan Çelişki Matrisi'ni (`{TICKER}_celiski_matrisi.md`) ve Faz 0'daki rapor eşlemesini tekrar oku.
Bu bölümde yazdığın her projeksiyon varsayımının matristeki çözümlerle tutarlı olduğunu doğrula.
Matristeki çelişki çözümleri bu bölümde somut paragraf olarak yer almalı (hafifletici faktör açıklaması veya senaryo ayrımı şeklinde).

```python
mod._baslik(doc, 'Projeksiyon Varsayımları', level=2)
```

🔥 **Bu bölüm amatörü profesyonelden ayırır. TOKEN TASARRUFU YAPMA.**

#### Ürün Bazlı Varsayımlar (1.000-1.500 kelime)

Her ana segment/ürün kategorisi için AYRI alt başlık aç. Minimum 3 segment. Her segment için:

```markdown
#### [Segment Adı] Gelir Varsayımları

[Segment] gelirinin FY20XX'teki X mn TL seviyesinden FY20XX+5'te Y mn TL'ye
ulaşmasını (Z% YBBO) bekliyoruz. Bu büyümenin ana sürücüleri:

1. **[Sürücü 1 — spesifik metrik]:** [2-3 cümle. Tarihsel veri + ileriye dönük
   beklenti. Sayıyla başla.] (Kaynak: KAP, sektör kuruluşu vb.)

2. **[Sürücü 2 — spesifik metrik]:** [2-3 cümle.] (Kaynak: ...)

3. **[Sürücü 3]:** [2-3 cümle.] (Kaynak: ...)

Yıl bazlı varsayımlar:
- FY20XXT: %X büyüme — [spesifik faktörler: yeni ürün lansmanı, kapasite artışı vb.]
- FY20XX+1T: %X büyüme — [spesifik faktörler]
- FY20XX+2 – FY20XX+4T: %X YBBO — [yapısal/uzun vadeli faktörler]

Bu varsayımlara yönelik riskler: [2-3 madde — her risk spesifik ve ölçülebilir]
```

**Her segment için 8-12 madde detay. Toplam 3-5 segment = 1.000-1.500 kelime.**

#### Coğrafi Varsayımlar (200-800 kelime)

**Çok pazarlı şirketlerde** (THY, DOCO, Pop Mart) her bölge AYRI alt başlık:

```markdown
#### [Bölge] Gelir Varsayımları

[Bölge] gelirinin toplam içindeki payı FY20XX'te %X'ten FY20XX+5'te %Y'ye
[artmasını/azalmasını] bekliyoruz. YBBO: %Z.

1. [Pazar dinamiği — spesifik ve kantitatif]
2. [Dağıtım genişlemesi — spesifik]
3. [Rekabet pozisyonu — spesifik]

CRP notu: Bu bölgenin ülke risk primi: %X (Damodaran [tarih]).
Hasılat-ağırlıklı CRP hesabına katkısı: %X × [pay] = %X.
```

**Tek pazarlı BIST şirketleri için:** Coğrafi bölüm yerine kanal kırılımı (perakende vs online, yurtiçi vs ihracat) veya bölgesel kırılım (200-300 kelime).

#### Diğer Temel Varsayımlar (500-700 kelime)

```markdown
#### Marj Varsayımları

Brüt marjın FY20XX'teki %X'ten terminal %Y'ye [genişlemesini/daralmasını] bekliyoruz.

Köprü (margin bridge):
| Faktör | Etki (bp) | Açıklama |
|--------|----------|----------|
| Fiyat artışı > maliyet artışı | +Xbp | [Gerekçe] |
| Ürün karması iyileşmesi | +Xbp | [Premium paya kayma] |
| Hammadde baskısı | -Xbp | [Spesifik hammadde] |
| **Net etki** | **+Xbp** | |

#### Faaliyet Gideri Varsayımları
- GYG/Hasılat: %X → %Y (ölçek avantajı)
- Pazarlama/Hasılat: %X → %Y (marka yatırımı)

#### Yatırım Harcaması (CapEx) Varsayımları
- CapEx/Hasılat: %X (5Y ort: %Y) — [Gerekçe]

#### Çalışma Sermayesi Varsayımları
- DSO: X gün, DIO: X gün, DPO: X gün
- CCC net etki: [X gün iyileşme/bozulma → SNA etkisi]

#### Vergi Varsayımları
- ETR: %X (yasal %Y, teşvik etkisi -%Z)
```

### C4. Senaryo Analizi (1.500-2.000 kelime — YENİ YAZIM) ⭐ KRİTİK

```python
mod._baslik(doc, 'Senaryo Analizi', level=2)
```

🔥 **Her senaryo için SPESİFİK parametreler ZORUNLU. TOKEN TASARRUFU YAPMA.**

#### İyimser Senaryosu (500-700 kelime)

```markdown
### İyimser Senaryosu: "[Senaryoyu anlatan tek cümle]"

Olasılık: %XX

Temel Varsayımlar:
- Hasılat YBBO (FY2026-FY2030T): %X (vs baz %Y)
- FY2030T Hasılat: X mn TL (vs baz Y mn TL)
- FY2030T FAVÖK Marjı: %X (vs baz %Y)
- Kilit ürün büyümesi: %X YBBO (vs baz %Y)
- Coğrafi genişleme: [spesifik kilometre taşları ve zaman çizelgesi]
- Pazar payı: %X (FY2030T'de, vs baz %Y)

İyimser Senaryosu İçin Gerekli Katalistler:
1. [Spesifik katalist] — Beklenen zamanlama: [tarih/çeyrek]
2. [Spesifik katalist] — Beklenen zamanlama: [tarih/çeyrek]
3. [Spesifik katalist] — Beklenen zamanlama: [tarih/çeyrek]

Detaylı Gerekçe:
[200-300 kelime — boğa senaryosunun gerçekleşmesi için ne olması gerektiğini açıkla.
Ürün lansmanları, pazar koşulları, rekabet dinamikleri hakkında spesifik ol.]

Değerleme İmplikasyonları:
- İNA Değeri: X TL/hisse (mevcut fiyattan %Z yükseliş)
- Comps Değeri: X.Xx FD/FAVÖK → X TL/hisse
- İyimser Senaryo Adil Değer Tahmini: X TL/hisse
```

#### Baz Senaryo (300-500 kelime)

```markdown
### Baz Senaryo: "[Başlık]"

Olasılık: %XX

Temel Varsayımlar:
[İyimser senaryosuyla aynı yapı, baz varsayımlarla]

Gerekçe:
[Bunun neden en olası senaryo olduğunu açıkla]

Değerleme:
- İNA Değeri: X TL/hisse
- Comps Değeri: X TL/hisse
- Baz Senaryo Adil Değer Tahmini: X TL/hisse (ağırlıklı ortalama)
```

#### Kötümser Senaryosu (500-700 kelime)

```markdown
### Kötümser Senaryosu: "[Başlık]"

Olasılık: %XX

Temel Varsayımlar:
[Düşüş parametreleriyle aynı yapı]

Düşüş Tetikleyicileri:
1. [Spesifik risk olayı] — Olasılık: [%]
2. [Spesifik risk olayı] — Olasılık: [%]
3. [Spesifik risk olayı] — Olasılık: [%]

Gerekçe:
[200-300 kelime — kötümser senaryosuna ne neden olur]

Değerleme İmplikasyonları:
- İNA Değeri: X TL/hisse (mevcut fiyattan %Z düşüş)
- Comps Değeri: X TL/hisse
- Kötümser Senaryo Adil Değer Tahmini: X TL/hisse
```

#### Senaryo Karşılaştırması (200-300 kelime)
- Kilit metriklerle kapsamlı karşılaştırma tablosu
- Olasılık-ağırlıklı sonuç analizi
- Risk/getiri değerlendirmesi

```python
mod.grafik_ekle(doc, 'charts_v2/{TICKER}_G14_senaryo_karsilastirma.png',
    boyut='TAM', baslik='...')
mod.tablo_ekle(doc, ...) # Senaryo karşılaştırma tablosu
```

#### ⚠️ Senaryo Parametreleri DCF-FM Tutarlılık Kontrolü (ZORUNLU)

> **Referans:** `references/c2-tam-kapsama/senaryo-metodoloji.md` — tüm formüller ve kurallar

Senaryo bölümünü yazmadan ÖNCE aşağıdaki tutarlılık kontrollerini yap:

```
DCF-FM TUTARLILIK KONTROL LİSTESİ
===================================
- [ ] Terminal büyüme (g): DCF Senaryolar tabı = FM Senaryolar tabı? (birebir eşit olmalı)
- [ ] ETR (efektif vergi): DCF = FM? (birebir eşit olmalı)
- [ ] Senaryo ağırlıkları: DCF = FM? (birebir eşit olmalı)
- [ ] FM CAGR ≈ DCF Y1-Y2 büyüme? (±2pp tolerans)
- [ ] Kötümser/İyimser adil değer tahmini: DCF ↔ FM ±%15 içinde mi?
- [ ] CapEx/Hasılat: FM Senaryolar = raporda yazılan parametre?
- [ ] FAVÖK marjı: FM GelirTablosu → NakitAkış zincirleme tutarlı mı?
- [ ] Senaryo dropdown (Kötümser/Baz/İyimser) her iki dosyada da aktif mi?
```

**Raporda yazılan her senaryo parametresi Excel dosyalarındaki değerlerle BİREBİR eşleşmeli.**
Raporda "%14,4 hasılat büyümesi" yazıp Excel'de %12 bırakmak KESİNLİKLE KABUL EDİLEMEZ.

#### Senaryo Narratif Şablonu — Kurumsal Format

Her senaryo aşağıdaki yapıda yazılmalı. Bu şablon Goldman Sachs / Morgan Stanley araştırma raporlarındaki yapıyla uyumludur:

```markdown
### [İyimser/Baz/Kötümser] Senaryosu: "[Tek cümle başlık — spesifik ve ölçülebilir]"

**Olasılık:** %XX (kaynak: MQS + Risk Matrisi bazlı adaptif ağırlıklar, bkz. senaryo-metodoloji.md)

**Tetikleyici Olaylar (Katalistler):**
1. [Olay] — Zamanlama: [Çeyrek/Yıl] — Olasılık: %XX
2. [Olay] — Zamanlama: [Çeyrek/Yıl] — Olasılık: %XX
3. [Olay] — Zamanlama: [Çeyrek/Yıl] — Olasılık: %XX

**Kantitatif Varsayımlar (Excel Senaryolar tabından):**

| Parametre | Değer | vs Temel | Kaynak |
|-----------|-------|----------|--------|
| Hasılat YBBO (FY26-FY27) | %X | +/- Xpp | FM Senaryolar satır 7-8 |
| Terminal Büyüme (g) | %X | +/- Xpp | DCF+FM Senaryolar satır 9 |
| FAVÖK Marjı (hedef) | %X | +/- Xpp | FM Senaryolar satır 10 |
| SMM/Hasılat | %X | +/- Xpp | FM Senaryolar satır 12 |
| CapEx/Hasılat | %X | +/- Xpp | FM Senaryolar satır 15 |
| WACC | %X | +/- Xpp | DCF Senaryolar |

**Türetim Gerekçesi (her parametre NEDEN bu değerde):**
[300-400 kelime — tarihsel veri, peer karşılaştırma, makro kısıtlar]

**Değerleme İmplikasyonları:**
- İNA (DCF) Adil Değer Tahmini: X TL/hisse (Excel DCF Senaryolar tabından)
- Çarpan Değeri: X.Xx FD/FAVÖK → X TL/hisse
- Ağırlıklı Adil Değer Tahmini: X TL/hisse
```

**Adaptif Ağırlık Mekanizması:**
Senaryo olasılıkları sabit değildir. T3'te hesaplanan MQS (Management Quality Score) ve Risk Matrisi sonuçlarına göre ayarlanır:
- MQS ≥ 24: Kötümser –5pp → %20, İyimser +5pp → %30
- MQS < 15: Kötümser +5pp → %30, İyimser –5pp → %20
- Risk Skoru ≥ %40: Kötümser +5pp → %30, İyimser –5pp → %20
- Varsayılan: Kötümser %25, Baz %50, İyimser %25

Bu ağırlıklar raporda açıkça belirtilmeli ve gerekçelendirilmelidir.

#### Senaryo Güncelleme Zamanlaması

Senaryolar statik değildir. Aşağıdaki aşamalarda güncellenir:

| Aşama | Senaryo Aksiyonu |
|-------|-----------------|
| T1 tamamlandığında | Risk faktörleri → Kötümser tetikleyicileri belirlenir |
| T2 tamamlandığında | FM parametreleri → kantitatif türetim (formüller uygulanır) |
| T3 tamamlandığında | DCF-FM tutarlılık kontrolü → uyumsuzluk varsa düzelt |
| T4 tamamlandığında | Grafiklerde senaryo karşılaştırması doğrula |
| T5 yazılırken | Narratif ↔ Excel birebir eşleşme son kontrol |

**⛔ HARD STOP GATE:** Faz C tamamlanmadan Faz D'ye geçme. Kontrol et:
- [ ] Tarihsel analiz yazıldı mı? (1.200+ kelime)
- [ ] Projeksiyon varsayımları yazıldı mı? (2.000+ kelime, ürün-ürün detay)
- [ ] Senaryo analizi yazıldı mı? (1.500+ kelime, 3 senaryo + karşılaştırma)
- [ ] Tüm tablolar çıkarıldı mı? (gelir tablosu, segment, coğrafya vb.)
- [ ] 5-7 grafik gömüldü mü?
- [ ] **OMURGA KONTROLÜ:** Faz 0 Ana Argüman'ı tekrar oku. Projeksiyon varsayımları ve senaryolar Faz 0 Çelişki Matrisi'ndeki çözümlerle tutarlı mı? Çelişki çözümleri raporda belirtilen bölümlere yazıldı mı?
- [ ] **BİRİM KONTROLÜ:** Projeksiyon tablosu başlığında birim etiketi var mı? Guidance Rekonsilasyon Kutusu (guidance varsa) yazıldı mı? Büyüme oranları "(reel)" veya "(nominal)" etiketli mi?

---

## FAZ D: Değerleme Analizi (S.27-31)

**Çıktı:** ~5-8 sayfa, 4-5 grafik, 4-5 tablo
**Bu Faz'da yapılan:** Değerleme metodolojisi (yeni) + INA + Comps + Football Field + Adil Değer Tahmini (yeni)

```python
mod._baslik(doc, 'Değerleme Analizi', level=1)
```

### D1. İNA (DCF) Analizi

```python
mod._baslik(doc, 'İndirgenmiş Nakit Akışları (İNA) Analizi', level=2)
```

T3 değerleme dokümanından İNA bölümünü çıkar, formatla ve YORUM ekle.

**İNA Varsayımlar Tablosu:** Varsayım | Değer | Kaynak (15-20 satır)

**İNA Sensitivity Matrisi:** AÖSM (WACC) değerleri satır başlıkları × terminal büyüme oranları sütun başlıkları

```python
mod.grafik_ekle(doc, 'charts_v2/{TICKER}_G28_dcf_sensitivity.png',
    boyut='TAM', baslik='Adil değer tahmini AÖSM ve büyümeye duyarlılık: X-Y TL bandı') # ⭐ ZORUNLU
mod.grafik_ekle(doc, 'charts_v2/{TICKER}_G29_dcf_waterfall.png',
    boyut='TAM', baslik='...')
# EK grafiği İLGİLİ bölüme göm:
mod.grafik_ekle(doc, 'charts_v2/{TICKER}_EK05_wacc_bilesenleri.png',
    baslik='WACC bileşenleri: Ke, Kd, ağırlıklar')
```

> **⚠️ Duplikasyon Uyarısı (v3.2):** DCF duyarlılık analizi için SADECE BİR format seç: ya G28 grafiğini ya da hassasiyet matrisi tablosunu kullan, ASLA ikisini birden koyma. Grafik → hızlı görsel; Tablo → kesin rakamlar. Tercih: grafik (G28) ana bölümde, tablo opsiyonel olarak Ekler'de.

### D2. Peer Karşılaştırma (Comps)

```python
mod._baslik(doc, 'Peer Karşılaştırma Analizi', level=2)
```

**KRİTİK:** İstatistiksel özet satırlarının tablonun altında mevcut olması ZORUNLU:

```python
mod.tablo_ekle(doc,
    basliklar=['Şirket', 'Ticker', 'PD (mn$)', 'FD/FAVÖK', 'F/K', 'Büyüme', 'FAVÖK Marjı'],
    satirlar=[
        # ... 5-10 peer
        # ... Hedef şirket
        ['', '', '', '', '', '', ''],  # boş satır
        ['Maksimum', '', '...', '...', '...', '...', '...'],
        ['75. Persantil', '', '...', '...', '...', '...', '...'],
        ['Medyan', '', '...', '...', '...', '...', '...'],
        ['25. Persantil', '', '...', '...', '...', '...', '...'],
        ['Minimum', '', '...', '...', '...', '...', '...'],
    ],
    kaynak='Yahoo Finance, BBB tahminleri'
)
```

İstatistiksel özet YOKSA → **HATA RAPORLA**, devam etme.

```python
mod.grafik_ekle(doc, 'charts_v2/{TICKER}_G30_peer_scatter.png', boyut='TAM', baslik='...')
mod.grafik_ekle(doc, 'charts_v2/{TICKER}_G31_peer_carpan.png', boyut='YARIM', baslik='...')
```

### D3. Değerleme Metodolojisi (800-1.200 kelime — YENİ YAZIM)

- İNA (DCF) açıklaması + varsayımlar gerekçesi
- Peer karşılaştırma (comps) gerekçesi
- Uzlaştırma ve ağırlıklandırma mantığı

**Değerleme Özet Tablosu:**

```python
mod.tablo_ekle(doc,
    basliklar=['Yöntem', 'Kötümser', 'Baz', 'İyimser', 'Ağırlık', 'Ağırlıklı'],
    satirlar=[...])

mod.grafik_ekle(doc, 'charts_v2/{TICKER}_G32_football_field.png',
    boyut='TAM', baslik='...') # ⭐ ZORUNLU
```

### D4. Adil Değer & Değerleme Görüşü (300-500 kelime — YENİ YAZIM)

```python
mod._baslik(doc, 'Adil Değer Tahmini ve Değerleme Görüşü', level=2)
```

- Final tavsiye: EKLE / TUT / AZALT
- Adil değer tahmini: X TL (mevcut fiyattan %X yükseliş)
- Zaman ufku: 12 ay
- Kilit katalistler (3-5, spesifik zaman çizelgesiyle)
- Adil değer tahminine yönelik kilit riskler (3-5, etki büyüklüğü ile)

**⛔ HARD STOP GATE:** Faz D tamamlanmadan Faz E'ye geçme. Kontrol et:
- [ ] İNA varsayımlar tablosu ve sensitivity matrisi yazıldı mı?
- [ ] Peer karşılaştırma tablosu istatistiksel özetle yazıldı mı?
- [ ] Değerleme metodolojisi yazıldı mı? (800+ kelime)
- [ ] Adil değer tahmini ve tavsiye yazıldı mı?
- [ ] Football field grafiği (G32) gömüldü mü?
- [ ] **OMURGA KONTROLÜ:** Faz 0 Ana Argüman'ı tekrar oku. Değerleme sonucu Faz 0'daki tez ve karşı-tez ile tutarlı mı? Çelişki Matrisi'ndeki çözümler değerleme bölümünde yansıtıldı mı?

---

## FAZ E: Ekler & Sonlandırma

```python
# Kaynaklar & Referanslar
mod.kaynaklar_sayfasi(doc, {
    'Finansal Veriler': [
        ('KAP Q4 2025 Finansal Tablo', 'https://kap.org.tr/tr/Bildirim/{no}', '15 Şubat 2026'),
        ('BBB Finans API çıktısı (KAP kaynaklı)', None, '18 Mart 2026'),
    ],
    'Sektör & Piyasa Verileri': [
        # sektöre göre ilgili kuruluş
    ],
    'Değerleme Referansları': [
        ('Damodaran Country Risk Premium', 'https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html', 'Mart 2026'),
        ('Damodaran Industry Betas', 'https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html', 'Mart 2026'),
    ],
    'Şirket Kaynakları': [
        ('{ŞİRKET} Yatırımcı İlişkileri', 'https://...', 'Mart 2026'),
    ],
    'Emsal Şirketler': [
        # her peer için Yahoo Finance linki
    ],
})

# Ekler — SADECE teknik detay tabloları (v3.2)
# ⚠️ YASAK: Grafikleri Ekler'e "park etme". Tüm grafikler (EK01-EK07 dahil)
#    ilgili ana bölüme gömülmelidir (bkz. Proximity Prensibi).
# ✅ Ekler'de olabilecek içerikler:
#    - IAS 29 / muhasebe köprü tabloları (teknik detay)
#    - Detaylı peer karşılaştırma tablosu (10+ sütunlu, ana bölüme sığmaz)
#    - Çeyreklik tahmin modeli tablosu (forward-looking granüler detay)
#    - SOTP / alternatif değerleme tablosu
#    - Detaylı finansal tablolar (40+ satırlık P&L, bilanço, nakit akış)
# ❌ Ekler'de OLMAMASI gerekenler:
#    - Tekil grafikler (mağaza sayısı, pazar payı, stok optimizasyonu vb.)
#    - Ana bölümde zaten olan içeriğin tekrarı (duplikasyon)
mod._sayfa_sonu(doc)
mod._baslik(doc, 'Ekler', level=1)
# Teknik detay tabloları buraya

# Analist Sertifikasyonu — AI Beyanı (v4.14)
# Yapay zeka ile üretildiğini, lisans/sertifika bulunmadığını,
# halüsinasyon riskini ve bağımsız danışman önerisini açıkça belirt.
# Tavsiye Tanımları tablosu v4.14'te kaldırıldı.
mod._baslik(doc, 'Analist Sertifikasyonu', level=2)
mod._paragraf(doc, '[AI beyanı — engine yasal_uyari gibi sabit metin değil, assembly\'de yazılır]')

# Yasal uyarı — SPK uyumlu sabit metin (engine'de tanımlı)
mod.yasal_uyari(doc)
```

---

## FAZ F: Sayfa 1 Yatırım Özetini Yaz (500-700 kelime — EN SON)

**ŞİMDİ** Sayfa 1'i yaz — tüm analiz tamamlandıktan sonra. Bu, raporun kapsamlı sentezini gerektirir.

İçerik:
- "KAPSAM BAŞLATMA" başlığı
- Tavsiye kutusu (EKLE/TUT/AZALT, adil değer tahmini, yükseliş potansiyeli)
- 3-4 detaylı bullet (bold başlıklar + spesifik veriler)
- Finansal özet tablosu
- Hisse fiyat grafiği (G01)

**Bullet'lar genel ifade DEĞİL, raporun en önemli argümanlarının veri destekli sentezi olmalı.**

**Sayfa 1 ek unsur — "En Kırılgan Varsayım" notu (bullet'ların altında):**
T3 Çelişki Matrisi'nden (Faz 0'da okunan `{TICKER}_celiski_matrisi.md`) türetilir. Tek cümle formatında:
> **En kırılgan varsayım:** [Varsayım adı ve değeri]. Bu varsayım kırılırsa adil değer tahmini [X TL'den Y TL'ye] geriler. İzleme kriteri: [spesifik, ölçülebilir, tarihli].

Bu unsur raporun dürüstlük katmanıdır. "Neye en az güveniyoruz?" sorusunun cevabı Sayfa 1'de görünür olmalıdır.

---

## FAZ G: İçindekiler, Sayfa Numaraları & Kalite Kontrol

1. TOC field güncelle
2. Tüm sayfalarda sayfa numarası doğrula
3. Header/footer doğrula
4. **Kaydet:**

```python
doc.save(f'research/companies/{TICKER}/{TICKER}_Rapor_{TARIH}.docx')
```

5. **`kalite-kontrol-listesi.md`'nin TAMAMINI uygula** (§0-§14 + §15 Post-Assembly). (Ayrı dosya olarak oku.)

**HERHANGİ BİR MADDE BAŞARISIZSA, TESLİM ETME. Düzelt, sonra devam et.**

---

## FAZ H: Post-Assembly Doğrulama ve İçerik Zenginleştirme (v4.14)

Bu faz, assembly sonrası opsiyonel olarak çalışır. İki amacı vardır:

### H1. Kelime Sayısı Kontrolü ve Zenginleştirme

1. DOCX'teki gerçek kelime sayısını hesapla (paragraf + tablo)
2. Eğer 12.000 kelime altındaysa, T1 research.md'den zenginleştirme yap
3. **Zenginleştirme kuralları** (bkz. yazi-kalitesi-rehberi §7):
   - Her ek paragraf mevcut bağlamla tutarlılık kontrolünden geçmeli
   - İçgörü Merdiveni min Seviye 3
   - Duplikasyon taraması yapılmalı
   - Aynı bölümdeki yazım stiline uyum sağlanmalı

### H2. Sayfa Düzeni Doğrulama

1. DOCX'i PDF'e dönüştür veya Word'de aç
2. **Kısa taşma kontrolü:** Bir bölüm sonraki sayfaya sadece 1-5 satır taşıyorsa, o bölümdeki gereksiz tekrarları kısaltarak bölümün kendi sayfası içinde bitmesini sağla
3. **Boş sayfa kontrolü:** <%15 dolulukta sayfa varsa (kapak/İçindekiler hariç) düzelt
4. **İçindekiler sayfa numarası doğrulama:** PDF'teki gerçek sayfa numaralarıyla karşılaştır, uyumsuz olanları düzelt

### H3. Yazım Stili Doğrulama

1. Em dash (—) ve arrow (→) sayısını kontrol et; rapor gövde metninde 0 olmalı
2. Bold lead-in uygulanmış mı kontrol et
3. Tablo-paragraf spacing yeterli mi kontrol et

### H4. Tekrar Frekansı Taraması (ZORUNLU)

Assembly tamamlanıp DOCX üretildikten sonra, Faz 0'daki Tekrar Haritası'ndaki 5 kilit fact için frekans kontrolü yap:

1. DOCX'i aç, tüm paragraf metinlerini birleştir
2. Her kilit fact için regex ile TAM AÇIKLAMA sayısını tara (terim geçişi değil, 2+ cümlelik aynı bağlamda açıklama)
3. 3+ tam açıklama olan fact'leri raporla
4. Fazlalıkları kısalt: tam açıklamayı kısa referans + yeni açıya dönüştür
5. DOCX'i yeniden üret ve tekrar kontrol et

Bu adım tamamlanmadan rapor teslim edilmez.

---

## Yazım Stili ve Kalite Standartları

Aşağıdaki dosyalar T5'in yazım ve kalite standartlarını tanımlar. T5 başlamadan ÖNCE okunmuş olmalıdır (SKILL.md T5 bölümünde "ZORUNLU OKU" olarak belirtilmiştir):

| Standart | Kanonik Kaynak | Ne İçerir |
|----------|---------------|-----------|
| Yazım kalitesi | `references/ortak/yazi-kalitesi-rehberi.md` | İçgörü Merdiveni (min Seviye 3), Insight-First, consensus farkı çerçevesi, argüman inşası |
| DOCX format | `references/c2-tam-kapsama/profesyonel-cikti-rehberi.md` | Renk, font, tablo, grafik embed standartları |
| Sayfa düzeni | `references/c2-tam-kapsama/rapor-sablonu.md` | Fiziksel yapı, sayfa planı, chart embed haritası, sayısal format kuralları |
| Kalite kontrol | `references/c2-tam-kapsama/kalite-kontrol-listesi.md` | A1-A11 kontrol listesi (A8, A9 FAIL = rapor geri çevrilir) |

**Hızlı hatırlatma (kanonik kaynak yukarıdaki dosyalarda — burayı DEĞİL orayı güncelle):**
- Insight-First: Her paragrafın ilk cümlesi sonuç/bulgu, kanıt sonra
- Sayıyla Başla: "Güçlü büyüme" değil → "Hasılat YoY %15 artışla 27.675 mn TL'ye ulaştı"
- Her rakamda kaynak etiketi zorunlu: `(KAP, Q4 2025)` formatında. Yoksa `[DOĞRULANMADI]`
- Em dash (—) YASAK, düz tire (-) kullan
- Grafik başlıkları İçgörü formatında: rakam + karşılaştırma içermeli
- Binlik: nokta (12.450), ondalık: virgül (%12,5), çarpan: küçük x (12,5x)
- EKLE/TUT/AZALT (BUY/HOLD/SELL değil), İyimser/Baz/Kötümser (Bull/Base/Bear değil)
- FY2024G (gerçekleşme), FY2025T (tahmin), 9A2025 (9 aylık)
- IAS 29 TL'yi spot kurla USD'ye çevirme YASAK

---

## Sık Yapılan Hatalar (KAÇINILACAKLAR)

1. **T1 içeriğini yeniden yazmak**: T1'den 6-8K kelimeyi YENİDEN YAZMA. Neredeyse aynen kullan — sadece formatla ve grafik ekle.

2. **Seyrek sayfalar**: Her sayfa HEM metin HEM görsel içermeli. Her 200-300 kelimede grafik ekle.

3. **Grafikleri sona gruplamak**: Grafikler metin boyunca dağıtılmalı. Grafiği tartışan paragraftan hemen sonra yerleştir.

4. **Markdown syntax bırakmak**: DOCX formatı kullan. `##`, `**`, ` ``` ` görünmemeli.

5. **Sayfa 1 formatını atlamak**: Tam kurumsal formatı takip etmeli — "KAPSAM BAŞLATMA" başlığı, tavsiye kutusu, bullet'lar, tablo.

6. **Genel bullet'lar**: Sayfa 1 bullet'ları bold başlıklar + spesifik veriler içermeli, genel ifadeler DEĞİL.

7. **İnce varsayımlar**: Projeksiyon Varsayımları MUTLAKA 2.000-3.000 kelime olmalı, ürün-ürün ve bölge-bölge detayla.

8. **Belirsiz senaryolar**: İyimser/Baz/Kötümser için SPESİFİK parametreler olmalı — genel ifadeler yetmez.

9. **Düz metin URL'ler**: Tüm kaynaklar tıklanabilir hyperlink olmalı. `add_hyperlink()` fonksiyonunu kullan.

10. **Eksik istatistiksel özet**: Comps tablosunda maks/75./medyan/25./min ZORUNLU.

11. **Modelle uyumsuz rakamlar**: Tüm rakamları kaynak dosyalarla doğrula. DOCX ↔ kaynak tutarlı olmalı.

12. **IAS 29 tuzağı**: TL IAS 29 düzeltmeli rakamları spot kurla USD'ye çevirme. Fisher cross-check zorunlu.

13. **Kaynak etiketi eksikliği**: Her rakamda kaynak etiketi zorunlu. Fabrike rakam YASAK. "Sanki biliyormuş gibi davranma."

14. **Doğrulama atlamak**: `kalite-kontrol-listesi.md`'nin TAMAMINI uygula. Opsiyonel DEĞİL.

15. **Piyasa iliskisini tartismamak** — rapor piyasa fiyatlamasiyla ortusme/ayrisma noktalarini belirtmiyor

16. **Analitik kopru yok** — T1 analitik bolumleri T2/T3 perspektifi eklenmeden aynen kopyalanmis

---

## Başarı Kriterleri

Başarılı bir hisse senedi araştırma raporu:

| # | Kriter | Minimum | İdeal |
|---|--------|---------|-------|
| 1 | Sayfa sayısı | 30 | 40-50 |
| 2 | Kelime sayısı | 10.000 | 12.000-16.000 |
| 3 | Gömülü grafik | 25 | 30-35 |
| 4 | Kapsamlı tablo | 12 | 15-20 |
| 5 | Projeksiyon Varsayımları | 2.000 kel | 2.500-3.000 kel |
| 6 | Senaryo Analizi | 1.500 kel | 1.800-2.000 kel |
| 7 | 4 zorunlu grafik | G03, G04, G28, G32 | + G01, G14, G33 |
| 8 | Comps istatistiksel özet | maks/medyan/min | + 75./25. persantil |
| 9 | Yönetim biyografileri | 150 kel × 3 yönetici | 300-400 kel × 4 |
| 10 | Tıklanabilir hyperlink | Kaynaklar sayfası | + şekil kaynakları |
| 11 | Sayfa yoğunluğu | %60 | %70-80 |
| 12 | Rakam tutarlılığı | 15 spot-check | DOCX ↔ XLS ↔ kaynak |

**Final test:** Okuyucu şirketi, değerlemeyi, riskleri anlamalı. Ak Yatırım/İş Yatırım/JPMorgan raporlarından ayırt edilemez olmalı.

---

## 🔥 SON HATIRLATMA

Eksiksiz, profesyonel bir rapor teslim etmek için gereken tüm tokenleri kullan.
Bu taslak değil. Özet değil. Anahat değil. **FİNAL YAYIN KALİTESİNDE RAPOR.**

1.000.000+ TL yatırım kararına layık kurumsal kalitede araştırma teslim et.
Token yetersiz kalırsa — bu task için beklenen ve kabul edilebilir. **Yazmaya devam et.**

---

## Versiyon Geçmişi

**Mevcut:** v2.2 (2026-03-24)

| Tarih | Versiyon | Özet |
|-------|----------|------|
| 2026-03-24 | **v2.5** | Çelişki Matrisi T3'e taşındı (GAP-2 çözümü). Faz 0 Adım 1 artık T3 matrisini OKUR + rapor eşlemesi yapar. C3 kontrolü T3 matrisine referans verir. |
| 2026-03-24 | **v2.4** | Faz 0 yeniden tasarlandı: Argüman İnşası (rapor eşlemesi + 3 paragraf testi + Dallar + Piyasa). Faz B/C/D gate'lerine omurga kontrolü. Faz F'ye "En Kırılgan Varsayım" notu. |
| 2026-03-24 | **v2.3** | Yazım Stili Rehberi (93 satır inline tekrar) → referans bloğuna dönüştürüldü (SSoT: yazi-kalitesi, profesyonel-cikti, rapor-sablonu, kalite-kontrol). Faz C3 T1 Risk Çapraz Kontrol eklendi. |
| 2026-03-23 | **v2.1** | Girdi Doğrulama bölümüne 4 yeni ön-koşul eklendi: Yapısal Analiz Tetikleyicileri kontrolü, Konsensüs Karşılaştırma tablosu, Küresel peer listesi, Forward bilanço/nakit akış sütunu. task1-arastirma.md v2.4 ve task2-finansal-modelleme.md v1.8 ile uyumlu |
| 2026-03-19 | **v2.0** | İlk yayın — 7 fazlı montaj workflow, yazım stili rehberi, başarı kriterleri |
