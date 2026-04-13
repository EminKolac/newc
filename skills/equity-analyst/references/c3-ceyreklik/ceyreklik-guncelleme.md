# Çeyreklik Güncelleme Rehberi — Çeyreklik Analiz Çerçevesi

> **Bu dosyanın rolü:** Ç3 ve Ç4 için metodoloji (5-fazlı workflow, §14 veri tazeliği, §15 ön bakış, §16 yazım standardı).
> **Ç3 Çıktı Şablonu (DOCX, sayfa yapısı, QC):** `references/c3-ceyreklik/c3-sablon.md`
> **Ç4 Çıktı Şablonu (DOCX, sayfa yapısı, QC):** `references/c4-on-bakis/c4-sablon.md`

## Felsefe

Çeyreklik güncelleme, ilk kez kapsama raporundan farklıdır. İlk kez kapsama "şirket nedir?" sorusuna cevap verir; çeyreklik güncelleme "ne DEĞİŞTİ?" sorusuna. Okuyucu şirketi zaten tanıyor — ona yeni bilgiyi, beklentiyle gerçekleşmenin farkını ve tezine etkisini söyle.

> İlker'in çeyreklik yazım kalıbı: "Beklenti → Gerçekleşme → Neden?"

---

## 1. Beat/Miss Analizi (ZORUNLU Tablo)

Her çeyreklik analizin başında bu tablo yer almalı:

```
## Q[X] 20XX Sonuçları: [BEAT / INLINE / MISS]

| Metrik | Beklenti | Gerçekleşme | Fark | Not |
|--------|----------|-------------|------|-----|
| Gelir | X mn TL | X mn TL | +X% / -X% | [Kısa açıklama] |
| FAVÖK | X mn TL | X mn TL | +X% / -X% | [Marj etkisi] |
| FAVÖK Marjı | %X | %X | +Xbp / -Xbp | |
| Net Kâr | X mn TL | X mn TL | +X% / -X% | |
| [Sektörel KPI] | X | X | +/- | [Pazar payı, hacim vb.] |
```

### Beklenti Kaynakları
BIST'te Bloomberg konsensüsü genellikle mevcut değil. Alternatifler:
- İlker'in kendi önceki çeyrekteki guidance/beklentisi (öncelikli)
- Kurum raporları hedef/tahminleri (İş Yatırım, Ak Yatırım, Garanti BBVA)
- Sektör ortalaması veya tarihsel trend

Beklenti kaynağı parantez içinde belirtilir: `(İlker Q3 yazısı)`, `(İş Yatırım tahmin)`, `(sektör ort.)`

### Sonuç Sonrası Yönetim Kaynakları (Ç3 için ZORUNLU)

Bilanço açıklandıktan sonra yönetimin ne söylediği rakamlar kadar önemlidir:

```bash
# ── Konferans Çağrısı / Analist Toplantısı (sonuç sonrası) ──
web_search "{şirket} analist toplantısı {çeyrek} {yıl} site:youtube.com"
summarize "https://youtu.be/{video_id}" --youtube auto --extract-only > /tmp/{TICKER}_conf_call.txt

# ── Yatırımcı Sunumu (çeyreklik güncelleme) ──
# Şirket IR sayfasından en son sunumu bul
summarize "https://ir.{şirket}.com/{dönem}_sunum.pdf" --extract-only > /tmp/{TICKER}_sunum.txt
```

**Çıkarılacak bilgiler:**
- Yönetim tonu (güvenli / temkinli / savunmacı)
- Guidance güncellemesi (yukarı / aşağı / sabit)
- Forward-looking ipuçları (yeni yatırım, M&A, maliyet baskısı)
- Kaçınılan sorular (analistlerin sorduğu ama geçiştirilen konular)

**⚠️ Kaynak Güncelliği:** Çeyreklik güncelleme en güncel veriyle yapılır. >6 ay eski kaynak birincil olarak KULLANILAMAZ. Detay → `task1-arastirma.md §Kaynak Güncelliği Protokolü`

---

## 2. What's NEW — Sadece Yeni Bilgi

Bu bölüm sadece çeyrekle birlikte ortaya çıkan yeni bilgilere odaklanır. Şirket tanıtımı, sektör arka planı gibi bilgiler tekrarlanmaz.

### Yapı

```
## Bu Çeyrekte Ne Değişti?

### 1. [En önemli gelişme — headline]
[2-3 cümle açıklama]

### 2. [İkinci önemli gelişme]
[2-3 cümle açıklama]

### 3. [Üçüncü gelişme]
[2-3 cümle açıklama]
```

---

## 3. Tahmin Revizyonu

Yeni veri sonrası forward tahminlerin nasıl değiştiğini göster:

```
## Tahmin Revizyonu

| Metrik | Eski Tahmin (FY) | Yeni Tahmin (FY) | Değişim | Neden |
|--------|-----------------|-----------------|---------|-------|
| Gelir | X mn TL | X mn TL | +X% | [Kısa gerekçe] |
| FAVÖK Marjı | %X | %X | +Xbp | [Gerekçe] |
| Net Kâr | X mn TL | X mn TL | +X% | [Gerekçe] |
| Hedef Fiyat | X TL | X TL | +X% | [Gerekçe] |
```

### Signal vs Noise Ayrımı

Her tahmin revizyonunda sor: "Bu çeyrekte gördüğüm değişiklik yapısal mı (sinyal) yoksa geçici mi (gürültü)?"

| Değişiklik Türü | Sinyal (Yapısal) | Gürültü (Geçici) |
|----------------|-----------------|----------------|
| Pazar payı artışı/kaybı | ✅ Trend 3+ çeyrek sürüyorsa | ❌ Tek çeyreklik dalgalanma |
| Marj değişimi | ✅ Maliyet yapısı değiştiyse | ❌ Hammadde geçici spike |
| Gelir büyümesi | ✅ Yeni ürün/pazar etkisi | ❌ Kur etkisi, tatil takvimi farkı |
| Net kâr sapma | ✅ Operasyonel iyileşme | ❌ Karşılık çözümü, vergi avantajı |

**Kural:** Sinyal → tahminleri revize et. Gürültü → normalizasyon yap, tahminleri değiştirme.

---

## 4. Teze Etkisi

Çeyreklik sonuç teze ne yaptı?

```
## Teze Etkisi

**Tez Takip Kartı Güncellemesi:**
| Tez Ayağı | Önceki Durum | Yeni Durum | Değişim |
|-----------|-------------|-----------|---------|
| Büyüme | Yolunda | [Durum] | ↑/→/↓ |
| Marj | Yolunda | [Durum] | ↑/→/↓ |

**Conviction:** [Değişmedi / Yüksek→Orta / vs.]
**Karar:** [Korunuyor / Değişti: TUT→EKLE vs.]
```

---

## 5. Önceki Yazılara Referans (ZORUNLU — İlker'in Kalıbı)

İlker her çeyreklik yazıda önceki yazılarından doğrudan alıntı yapar. Bu tutarlılık ve dürüstlük göstergesidir.

```
> Geçen çeyrek şöyle yazmıştık: "[İtalik alıntı, İlker'in kendi sözleri]"
>
> Gerçekleşme: [Beklentiyle gerçekleşme karşılaştırması]
```

---

## 6. Veri Doğrulama Kuralları (TBORG Q4 Dersi)

1. **Her rakama kaynak etiketi** — `(KAP Q4 2025, BBB Finans)`, `(Şirket IR sunumu, s.12)`
2. **"Tahmin ediyorum" = kırmızı bayrak** — Veri dosyada varken tahmin yapma
3. **Excel her sayfa, her satır** — En güncel veriyi bul, son satırı oku
4. **Önceki Q yazılarından alıntı zorunlu** — Tutarlılık kanıtı
5. **Son kontrol: "Bu rakamı hangi dosyada gördüm?"** — Doğrulanamayan kaldırılır

---

## 7. Çeyreklik Ön Bakış (Sonuç Öncesi Hazırlık)

> **Tam 5-adım workflow → §15'e bak.** Drive kurum raporlarından konsensüs çıkarma, sektör bazlı kritik metrik listesi, piyasa tepkisi senaryoları ve çıktı formatı §15'te.

Hızlı başvuru — senaryo tablosu yapısı:

```
### Boğa / Temel / Ayı Senaryoları
| Senaryo | Olasılık | Koşul | Beklenen Tepki |
|---------|----------|-------|----------------|
| Boğa | %25 | Konsensüs >+%5 beat, kilit metrik güçlü | Kısa vadede olumlu |
| Temel | %50 | Konsensüse paralel (±%3) | Nötr |
| Ayı | %25 | Konsensüs miss, guidance düşürme | Olumsuz tepki |
```

**Dosya isimlendirme:** `4C_2025_on_bakis.md` (sonuç öncesi) / `4C_2025_guncelleme.md` (sonuç sonrası)

---

## 8. Dosya Yapısı

```
research/companies/{TICKER}/
├── tez_takip_karti.md
├── ceyreklik/
│   ├── 4C_2025_on_bakis.md    ← Sonuç öncesi
│   ├── 4C_2025_guncelleme.md  ← Sonuç sonrası
│   ├── 1C_2026_on_bakis.md
│   └── 1C_2026_guncelleme.md
└── analiz.md
```

---

## 9. 5 Fazlı Çeyreklik Güncelleme Workflow'u

### ÖNEMLİ: EĞİTİM VERİSİ ESKİDİR

Agent'ın eğitim verisi tarihidir. Her çeyreklik güncelleme başında aşağıdaki adımlar ZORUNLU:

```
Adım 1: Bugünün tarihini kontrol et → session_status
Adım 2: Web araması yap → "{TICKER} {ÇEYREKLİK DÖNEM} sonuçları"
Adım 3: Sonuçların son 3 ay içinde olduğunu doğrula
Adım 4: BBB Finans araçlarıyla (KAP ve İş Yatırım) güncel finansal dönem verilerini çek
Adım 5: Çeyreklik güncellemeye ancak ŞİMDİ başla
```

### Faz 1: Veri Toplama (~15 dk)

```bash
cd ~/.openclaw/workspace/skills/bbb-finans/scripts

# 1. Güncel finansal tablo çek
python3 bbb_financials.py {TICKER} --start-year 2023 --end-year 2026 --section all --full

# 2. KAP özet (son 4 dönem)
python3 bbb_kap.py {TICKER} --kap-summary

# 3. İlker'in önceki çeyrek yazısını oku
# → research/companies/{TICKER}/ceyreklik/ veya İlker'in makale arşivi

# 4. Varsa kurum raporlarını oku
# → research/sources/{kurum}/{TICKER}_*.md

# 5. Sektörel KPI güncelle (TAPDK, OSD, BTK vb.)
```

**Faz 1 çıktısı:** Ham veri seti + önceki çeyrek referansları hazır.

### Faz 2: Analiz (~20 dk)

**2A. Beklenti/Gerçekleşme Karşılaştırması**

İlker'in önceki yazısından beklentileri çıkar, KAP gerçekleşmeleriyle karşılaştır.

| Kaynak Önceliği | Beklenti |
|----------------|----------|
| 1. İlker'in önceki Q yazısı | "FAVÖK marjının %15 civarında kalmasını bekliyoruz" |
| 2. İlker'in tez takip kartı | Büyüme hedefi: %10-15 |
| 3. Kurum konsensüsü | İş Yatırım: X mn TL gelir |
| 4. Tarihsel trend | 3Y ortalama büyüme: %8 |

**2B. Çeyreklik ve Yıllık Performans Ayrıştırma**

```
                Q4 2025    Q4 2024    QoQ     YoY
Hasılat         X mn TL    X mn TL    +X%     +X%
EBIT           X mn TL    X mn TL    +X%     +X%
Net Kâr         X mn TL    X mn TL    +X%     +X%

                FY2025     FY2024     YoY
Hasılat         X mn TL    X mn TL    +X%
EBIT           X mn TL    X mn TL    +X%
Net Kâr         X mn TL    X mn TL    +X%
```

⚠️ **Kümülatif raporlama notu:** BIST şirketleri kümülatif raporlar. Q4 tek başına = FY − 9M.

**2C. Marj Evrimi**

```
| Marj      | Q1   | Q2   | Q3   | Q4   | FY2025 | FY2024 | Δ     |
|-----------|------|------|------|------|--------|--------|-------|
| Brüt      | %X   | %X   | %X   | %X   | %X     | %X     | +Xbp  |
| EBIT     | %X   | %X   | %X   | %X   | %X     | %X     | +Xbp  |
| Net       | %X   | %X   | %X   | %X   | %X     | %X     | +Xbp  |
```

**Sorulacak soru:** Marj değişiminin kaynağı ne?
- Hammadde maliyeti? (maliyet tarafı)
- Fiyat artışı? (gelir tarafı)
- Faaliyet kaldıracı? (ölçek)
- IAS 29 etkisi? (muhasebe)
- Bir defalık kalem? (gürültü)

**2D. Sektörel KPI Analizi**

Her sektörün kendine özgü metrikleri var:

| Sektör | KPI'lar |
|--------|---------|
| Bira | Pazar payı %, kişi başı tüketim (lt), TAPDK hacim |
| Havacılık | Doluluk oranı (load factor), RPK, birim gelir (yield) |
| Bankacılık | NIM (net faiz marjı), TGA oranı, sermaye yeterliliği |
| Perakende | LFL (mağaza bazında) büyüme, m² başı satış, mağaza sayısı |
| Otomotiv | KKO, ihracat adet, birim FAVÖK |
| Çimento | Kapasite kullanımı, ton başı FAVÖK |

**2E. Sinyal/Gürültü Ayrıştırma**

Her büyük sapma için karar ver:

```
| Sapma | Büyüklük | Karar | Gerekçe |
|-------|----------|-------|---------|
| Brüt marj +300bp | Büyük | SİNYAL | 3 çeyrektir artıyor, fiyatlama gücü |
| Net kâr −%20 | Büyük | GÜRÜLTÜ | Kur farkı zararı, operasyonel değil |
| Gelir +%5 | Küçük | SİNYAL | Hacim artışı, trend devam ediyor |
```

### Faz 3: Rapor Yazımı (~30 dk)

**3A. Rapor Yapısı (8-12 sayfa, DOCX)**

```
SAYFA 1: Kapak + Özet Kutusu
  ┌─────────────────────────────────────┐
  │ [ŞİRKET] — [X]Ç 20XX Güncelleme    │
  │                                      │
  │ Karar: [ÜSTÜNDE / PARALEL / ALTINDA]│
  │ Conviction: [Yüksek / Orta / Düşük] │
  │ Hedef Fiyat: [X] TL → [Y] TL       │
  │ Mevcut Fiyat: [Z] TL               │
  │ Potansiyel Getiri: %XX              │
  └─────────────────────────────────────┘
  
  Beklenti/Gerçekleşme tablosu (Bölüm 1)
  Önceki yazıdan alıntı + kısa yorum

SAYFA 2-3: Detaylı Sonuçlar
  Çeyreklik ve yıllık performans tabloları (Faz 2B)
  Marj evrimi tablosu ve yorum (Faz 2C)
  Sektörel KPI analizi (Faz 2D)

SAYFA 4-5: Metrik Dashboard + Rehberlik
  İlker'in 6 metriği tablosu (güncel + tarihsel)
  Yönetim rehberliği (varsa) + BBB değerlendirmesi
  Peer karşılaştırma tablosu (güncelleme gerekiyorsa)

SAYFA 6: Tahmin Revizyonu + Değerleme
  Eski → Yeni tahmin tablosu (Bölüm 3)
  Hedef fiyat derivasyonu (Forward F/K + İNA)
  Duyarlılık tablosu (mini versiyon)

SAYFA 7: Risk + Tez Güncellemesi
  Tez takip kartı güncellemesi
  Yeni riskler / ortadan kalkan riskler
  Çıkış kriterleri kontrolü

SAYFA 8+: Grafikler (Minimum 8, bkz. Bölüm 13)
```

**3B. Başlık Kuralları**

| ❌ Yanlış | ✅ Doğru |
|----------|---------|
| "Q4 2025 Sonuçları" | "Brüt marj rekor seviyede, net kâr muhasebe etkisiyle düştü" |
| "Finansal Analiz" | "Hacim artışı %7 — pazar payı farkı kapanıyor" |
| "Değerleme Tablosu" | "Forward F/K 12x — sektör ortalaması 15x'e karşı iskontolu" |

**3C. Grafik Referansları**

`[GRAFİK: ...]` direktifleri YASAK. Grafiklere metin içinde organik referans:

> "FAVÖK marjı son 4 çeyrekte istikrarlı biçimde genişledi (bkz. Şekil 3). Bu trend..."

### Faz 4: Kalite Kontrol (~10 dk)

| Kontrol | Durum | Açıklama |
|---------|-------|----------|
| Her rakamda kaynak etiketi var mı? | ☐ | `(KAP 4Ç 2025)`, `(BBB Finans)` |
| `[DOĞRULANMADI]` etiketi var mı? | ☐ | Varsa → doğrula veya kaldır |
| Önceki Q yazısından alıntı var mı? | ☐ | ZORUNLU — yoksa ekle |
| Sinyal/gürültü ayrımı yapıldı mı? | ☐ | Her büyük sapma etiketli |
| Beklenti/gerçekleşme tablosu var mı? | ☐ | SAYFA 1'de |
| İlker'in 6 metriği güncel mi? | ☐ | Veto kontrolü yapıldı mı? |
| 8+ grafik var mı? | ☐ | Gömülü, placeholder değil |
| Tez takip kartı güncellendi mi? | ☐ | Conviction değişimi var mı? |
| Hedef fiyat revize edildi mi? | ☐ | Hayırsa → neden değişmedi? |
| TBORG Q4 dersi uygulandı mı? | ☐ | 5 kural kontrol |

### Faz 5: Teslim ve Arşiv

```bash
# 1. DOCX üret
python3 rapor-uret.py --type ceyreklik --ticker {TICKER} --period Q4_2025

# 2. Dosyala
mv output/{TICKER}_4C_2025_Guncelleme.docx research/companies/{TICKER}/ceyreklik/

# 3. Tez takip kartını güncelle
# research/companies/{TICKER}/tez_takip_karti.md

# 4. MEMORY.md'ye not
# "TBORG Q4 2025 çeyreklik güncelleme tamamlandı. Conviction: Yüksek. Hedef: 221 TL."
```

---

## 10. Kurumsal Türkçe Terminoloji

| İngilizce | Türkçe (Kurumsal) |
|-----------|-------------------|
| Earnings Update | Çeyreklik Güncelleme |
| Beat / Miss / Inline | Beklenti Üstünde / Altında / Paralel |
| Earnings Preview | Çeyreklik Ön Bakış |
| Estimate Revision | Tahmin Revizyonu |
| Signal vs Noise | Sinyal vs Gürültü |
| Bull / Base / Bear | İyimser / Baz / Kötümser |
| Thesis Impact | Tez Etkisi |
| Kill Criteria | Çıkış Kriterleri |
| Thesis Scorecard | Tez Takip Kartı |
| Pillar | Tez Ayağı |
| On-track | Yolunda |
| Conviction | Conviction (Türkçe karşılığı yaygın değil) |
| Guidance | Şirket Rehberliği |
| Forward P/E | İleriye Dönük F/K |
| LFL (Like-for-Like) | Mağaza Bazında Büyüme |
| QoQ / YoY | QoQ / YoY |

---

## 11. En İyi Uygulama Örnekleri (TBORG ve Kurum Raporlarından)

### İyi Başlık Örnekleri
- "Rekor brüt marj, muhasebe etkisiyle düşen net kâr" — TBORG Q4
- "Hacim artışına rağmen pazar payı farkı daralmadı" — rekabet odaklı
- "Guidance üstü gelir, marj baskısı devam ediyor" — İş Yatırım tarzı

### İyi Beklenti/Gerçekleşme Yazımı
> "Geçen çeyrek 'brüt marjın %52-54 bandında kalmasını bekliyoruz' demiştik. Gerçekleşme %55.3 ile bandın üzerinde geldi. Bu sürprizin ana kaynağı fiyat artışlarının SMM artışının önünde gitmesi."

### İyi Sinyal/Gürültü Ayrıştırma
> "Net kârdaki -%34.8'lik düşüş ilk bakışta endişe verici. Ancak bunun iki ana sürücüsü var: (1) IAS 29 parasal kazanç/kayıp etkisi (gürültü — nakit etkisi yok), (2) 1.58 milyar TL'lik satın alma (sinyal — büyüme yatırımı). Operasyonel kârlılık aslında rekor seviyede."

### Kötü Örnek (KAÇIN)
> "TBORG Q4 sonuçları geldi. Gelir X, FAVÖK Y, net kâr Z oldu." — Analiz yok, sadece veri tekrarı.

---

## 12. Zamanlama Kuralı

| Durum | Beklenen Süre | Hedef Yayın |
|-------|--------------|-------------|
| Sonuçlar açıklandı | 24 saat | Ertesi gün |
| Telekonferans/IR sunumu da geldi | +12 saat | 36 saat sonra |
| Karmaşık çeyrek (IAS 29, M&A, restatement) | +24 saat | 48 saat sonra |

**Hız > Mükemmellik kuralı:** Çeyreklik güncelleme 48 saatten geç yayınlanırsa değerini kaybeder. "İyi güncelleme geç" < "iyi güncelleme zamanında."

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-17 | v1.0 oluşturuldu — Beat/miss, estimate revision, thesis impact, preview, veri doğrulama |
| 2026-03-17 | v2.0 — 5 fazlı workflow, rapor yapısı (8-12 sayfa), sinyal/gürültü ayrıştırma, kurumsal terminoloji, en iyi uygulama örnekleri, zamanlama kuralı |
| 2026-03-17 | v2.1 — 8 zorunlu grafik listesi (Bölüm 13), veri tazeliği protokolü (Bölüm 14) |

---

## 13. Zorunlu 8 Grafik Listesi (Çeyreklik Güncelleme)

Her çeyreklik güncelleme raporunda aşağıdaki 8 grafik **zorunludur.** Ek grafikler opsiyonel.

| # | Grafik | Tip | Veri Kaynağı | Not |
|---|--------|-----|-------------|-----|
| Ç1 | **Çeyreklik hasılat progresyonu** | Bar (4-8 çeyrek) | BBB Finans | YoY büyüme çizgisi overlay |
| Ç2 | **Beklenti vs gerçekleşme waterfall** | Waterfall / grouped bar | İlker'in önceki Q yazısı + KAP | ⭐ BBB'ye özel: İlker beklentisi vs gerçekleşme |
| Ç3 | **Marj evrimi** | Çizgi (brüt + FAVÖK + net) | BBB Finans | 8 çeyreklik trend, bp değişim etiketli |
| Ç4 | **Segment/coğrafi kırılım** | Stacked bar veya area | BBB Finans / KAP FR | Çeyreklik mix değişimi |
| Ç5 | **Sektörel KPI trendi** | Bar + çizgi | TAPDK, OSD, BTK vb. | Sektöre özgü (bira: pazar payı + hacim) |
| Ç6 | **Peer karşılaştırma** | Scatter veya grouped bar | BBB Finans + Yahoo Finance | EV/FAVÖK vs FAVÖK marjı veya büyüme |
| Ç7 | **Hisse fiyatı + hedef fiyat** | Çizgi + yatay çizgi | BBB Finans / Yahoo | 1Y fiyat, hedef fiyat çizgisi, %potansiyel |
| Ç8 | **Değerleme çarpan bandı** | Band/area | BBB Finans | Tarihsel F/K veya FD/FAVÖK, mevcut konum işaretli |

### Ç2 Detay — Beklenti vs Gerçekleşme Grafiği (BBB'ye Özel)

BIST'te Bloomberg konsensüsü genellikle yetersiz. Bu grafik İlker'in kendi beklentileri üzerine kurulur:

```
Beklenti vs Gerçekleşme — Gelir & EBIT

           Beklenti    Gerçekleşme    Fark
Gelir     ████████░░   ██████████    +8%  ← Beat
EBIT     ████████     ████████░     -3%  ← Inline (miss <5%)
Net Kâr   ████████░░   █████░░░░░   -22% ← Miss (IAS 29)
```

**Beklenti kaynağı sırası:**
1. İlker'in önceki Q yazısındaki açık tahmin (varsa, verbatim)
2. İlker'in tez takip kartındaki hedef
3. Kurum konsensüsü (≥3 kurum gerekli)
4. Son 4 çeyrek trendi (en son başvuru)

**Kaynak notu zorunlu:** "Beklenti: İlker Başaran, TBORG Q3 2025 Güncelleme (Ekim 2025). Gerçekleşme: KAP."

### Opsiyonel Ek Grafikler

| # | Grafik | Ne Zaman Ekle? |
|---|--------|---------------|
| Ç9 | Tahmin revizyonu (eski vs yeni) | Tahminler materyal değiştiyse (>%5) |
| Ç10 | Operasyonel dashboard (İlker'in 6 metriği) | Veto metriği tetiklendiyse |
| Ç11 | Çeyreklik SNA (FCF) trendi | Nakit akışında materyal değişim varsa |
| Ç12 | Yönetim rehberliği vs gerçekleşme | Şirket guidance veriyorsa |

---

## 14. Veri Tazeliği Protokolü — Tüm Veri Sürecine Zorunlu

> **Her analiz başlangıcında — sadece çeyreklik değil, tüm rapor türlerinde — bu protokol uygulanır.**
> Kök neden: Agent eğitim verisi tarihidir. Web araması bile güncelliğini yitirebilir.

### ZORUNLU 5 ADIM (Atlanamazlar)

```
┌─────────────────────────────────────────────────────────────────────┐
│ ADIM 1: TARİH KONTROLÜ                                            │
│                                                                     │
│ → session_status ile bugünün tarihini yaz: ___/___/______          │
│ → Analiz edilen dönem: ___Ç ______                                 │
│ → Bu dönem sonuçları açıklandı mı?                                 │
│   □ EVET → Adım 2'ye geç                                          │
│   □ BİLMİYORUM → Web araması yap                                  │
│   □ HAYIR → Çeyreklik ön bakış modunda çalış                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ ADIM 2: BİRİNCİL KAYNAK DOĞRULAMA                                 │
│                                                                     │
│ → BBB Finans araçlarını çalıştır (KAP API):                       │
│   bbb_financials.py {TICKER} --section all --full                  │
│ → Son dönem: ___Ç _____ → Bu beklenen dönem mi?                   │
│   □ EVET → Adım 3'e geç                                           │
│   □ HAYIR → KAP'a henüz yüklenmemiş olabilir, web_search ile     │
│     teyit et ve BBB aracını --end-year parametresiyle yeniden dene │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ ADIM 3: İKİNCİL KAYNAK CROSS-CHECK                                │
│                                                                     │
│ Web araması yap: "{TICKER} {dönem} finansal sonuçlar"              │
│ → Bulunan kaynaklar (tarih + URL):                                 │
│   1. _____________________________ (tarih: ___)                    │
│   2. _____________________________ (tarih: ___)                    │
│                                                                     │
│ → Kaynaklar 90 günden eski mi?                                     │
│   □ HAYIR → Devam                                                  │
│   □ EVET → ⚠️ KIRMIZI BAYRAK: "Güncel veri bulunamadı"            │
│     → İlker'e bildir, analize devam ETME                          │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ ADIM 4: ÇİFT KAYNAK DOĞRULAMA (P0 KURAL)                         │
│                                                                     │
│ Web'den gelen HER rakam iki bağımsız kaynakla doğrulanmalı.       │
│ BBB Finans (KAP API) zaten birincil kaynak sayılır.               │
│                                                                     │
│ → Web aramasından gelen veri: _______________                      │
│ → Kaynak 1 (birincil): BBB Finans / KAP □                         │
│ → Kaynak 2 (ikincil): ________________________ □                  │
│ → İki kaynak uyuşuyor mu?                                          │
│   □ EVET → Veriyi kullan                                           │
│   □ HAYIR → Birincil kaynağı (KAP) doğru kabul et, farkı belirt  │
│   □ TEK KAYNAK → [DOĞRULANMADI] etiketi ekle                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ ADIM 5: "BU RAKAMI NEREDE GÖRDÜM?" SON KONTROL                    │
│                                                                     │
│ Rapor tamamlandıktan sonra, rapordaki HER rakam için:             │
│ → Dosya/kaynak yolu yazılabilir mi?                                │
│   □ EVET → Kaynak etiketi ekle                                     │
│   □ HAYIR → Rakamı KALDIR veya [DOĞRULANMADI] etiketle            │
│                                                                     │
│ → "Tahmin ediyorum" / "yaklaşık" / "~" içeren cümleler:           │
│   □ Gerçek veri ara — bulursan kesin rakamla değiştir              │
│   □ Bulamıyorsan → silme, ama [DOĞRULANMADI] etiketle              │
└─────────────────────────────────────────────────────────────────────┘
```

### Kırmızı Bayraklar (Analize Devam ETME)

| Durum | Aksiyon |
|-------|---------|
| BBB Finans dönem verisi eksik | İlker'e bildir — KAP güncellenmemiş olabilir |
| Web'de sonuç 90 günden eski | "Sonuçlar henüz açıklanmamış olabilir" — İlker'e sor |
| Birincil-ikincil kaynak uyuşmuyor (>%5 fark) | Her iki kaynağı göster, İlker karar versin |
| Excel/PDF'ten okunan rakam mantıksal tutarsız | Cross-check: farklı kalemle doğrula (gelir − maliyet = brüt kâr) |

### Bu Protokolün Geçerli Olduğu Tüm İş Akışları

- ✅ Çeyreklik güncelleme (Faz 1)
- ✅ İlk kez kapsama raporu (T1 veri toplama)
- ✅ Sektör raporu (veri bölümü)
- ✅ DCF çalışması (Faz 1: DATA_PACK)
- ✅ Hızlı analiz (kısaltılmış versiyon: Adım 1 + 2 yeterli)
- ✅ Bülten / makale yazımı (web verisi kullanılıyorsa Adım 3-4 zorunlu)

---

## §15. Sonuç Öncesi Ön Bakış

Sonuçlar açıklanmadan önce hazırlanan analiz. §14 Adım 1'de "Sonuçlar henüz açıklanmamış" durumuysa bu mod devreye girer.

### Ön Bakış ile Sonraki Güncellemenin Farkı

| | Ön Bakış | Çeyreklik Güncelleme |
|---|---------|---------------------|
| **Amacı** | "Ne bekliyoruz?" | "Ne değişti?" |
| **Birincil veri** | Kurum raporları + beklentiler | BBB Finans (KAP) — gerçekleşme |
| **Beat/miss tablosu** | HAYIR (henüz yok) | EVET (zorunlu) |
| **Kurum beklenti tablosu** | EVET (zorunlu) | Opsiyonel (karşılaştırma için) |
| **Tahmin revizyonu** | HAYIR | Varsa EVET |

### Adım Akışı — Ön Bakış

**Adım 1: Kurum Raporları Taraması**

Drive klasöründen ilgili kurumların beklenti raporlarını çek:
```
/Users/ilkerbasaran/Library/CloudStorage/GoogleDrive-ilker@borsadabibasina.com/
Drive'ım/Drive'ım/borsadabibasina.com/#5 - Kurum Raporları/
```

Arama önceliği:
- `{TICKER} {dönem}` içeren PDF'ler (örn. "THYAO 4Ç25")
- "4Ç25 Kar Beklenti Raporu" gibi multi-hisse raporlar (ticker bazlı bölüm ara)
- Kurum analisti toplantı notları (Analist Toplantı Notu)

```bash
DRIVE_KURUM="/Users/ilkerbasaran/Library/CloudStorage/GoogleDrive-ilker@borsadabibasina.com/Drive'ım/Drive'ım/borsadabibasina.com/#5 - Kurum Raporları"
find "$DRIVE_KURUM" -iname "*{TICKER}*" 2>/dev/null
```

**PDF Okuma (bulunan her rapor için):**
```bash
# GDrive warm cache (ilk erişimde timeout alırsa NORMAL):
cat "$DRIVE_KURUM/{Dosya}.pdf" > /dev/null 2>&1; sleep 30

# Metin çıkarma:
summarize "$DRIVE_KURUM/{Kurum} - {TICKER} {Dönem}.pdf" --extract-only > /tmp/{TICKER}_{kurum}.txt

# Çok uzun PDF'ler için özetleme:
summarize "$DRIVE_KURUM/{Dosya}.pdf" --model anthropic/claude-sonnet-4-6 > /tmp/{TICKER}_{kurum}_ozet.txt
```
⚠️ **GDrive warm cache:** Google Drive dosyaları ilk `cat`'te timeout alabilir — dosya henüz yerel cache'e indirilmemiştir. `cat > /dev/null` + `sleep 30` + tekrar dene. Hâlâ başarısız ise İlker'den sync kontrolü iste.

**Adım 2: Beklenti Tablosu Oluştur**

En az 3 kurum raporundan beklentileri topla:

```
## {ŞİRKET} {Dönem} Sonuç Beklentileri

| Metrik | Kurum A | Kurum B | Kurum C | BBB Tahmini |
|--------|---------|---------|---------|-------------|
| Gelir (mn TL/USD) | X | X | X | X |
| FAVÖK (mn TL/USD) | X | X | X | X |
| FAVÖK Marjı (%) | X% | X% | X% | X% |
| Net Kâr (mn TL/USD) | X | X | X | X |
| [Sektörel KPI] | X | X | X | X |
```

BBB Tahmini sütunu: BBB'nin kendi görüşünü yansıtır. Önceki çeyrekteki analizden türetilir.

**Adım 3: "İzlenecek 3-5 Kritik Metrik" Seç**

Her sektörde sonuçları en çok hareket ettirecek metrikler farklıdır:

| Sektör | Öncelikli Metrikler |
|--------|-------------------|
| Perakende | Mağaza başına ciro, trafik, e-ticaret payı |
| Havacılık | Yolcu sayısı, doluluk oranı, birim gelir (USD) |
| Telekomünikasyon | Abone büyümesi, ARPU, FAVÖK marjı |
| Sağlık | Yatak kapasitesi, hasta başına gelir, marj |
| İnşaat-GYO | Konut teslimi, ön satış, net nakit |
| Enerji/Baz Yük | Kapasite faktörü, satış fiyatı |
| Banka | Net faiz marjı, kredi büyümesi, TGA oranı |

**Adım 4: Olası Piyasa Tepkisi Çerçevesi**

```
## Sonuç Senaryoları

| Senaryo | Koşul | Beklenen Piyasa Tepkisi |
|---------|-------|------------------------|
| Güçlü Pozitif | Konsensüs >+%5 beat, kilit metrik güçlü | Kısa vadede olumlu |
| Hafif Pozitif | Konsensüs <%5 beat, mix gelir/marj | Sınırlı tepki |
| Baz | Konsensüse paralel (±%3) | Nötr |
| Negatif | Konsensüs miss, guidance düşürme | Olumsuz tepki |
```

**⚠️ BIST'e özgü not:** Önceki dönem piyasa tepkisine bak (tez scorecard'ından). Kurumların bu hisseye özel hassasiyet katsayısı var.

**Adım 5: Çıktı Formatı**

Ön bakış yazısının yapısı:

```
## [ŞİRKET] [Dönem] Sonuç Beklentileri

[1-2 cümle: Bu dönemde neye odaklanacağız?]

**Beklenti Tablosu** (Kurum konsensüsü)
[§15 Adım 2 tablosu]

**İzlenecek Kritik Metrikler**
■ **[Metrik 1]** — [Neden önemli? 1-2 cümle]
■ **[Metrik 2]** — [Neden önemli? 1-2 cümle]
■ **[Metrik 3]** — [Neden önemli? 1-2 cümle]

**Senaryo Çerçevesi**
[§15 Adım 4 tablosu]

**Tez Etkisi** — Sonuçtan bağımsız, izlenecek uzun vadeli sinyal:
[1 paragraf: Bu çeyrekte tezin hangi pillar'ı test edilecek?]
```

---

## §16. Rapor Sayfa 1 — Özet Kutu ve Yazım Standardı

Çeyreklik güncelleme raporunun ilk sayfası net, hızlı okunabilir olmalı. Yapı:

### Sayfa 1 — Zorunlu Bileşenler

```
[ŞİRKET ADI] ([TICKER])
[Dönem] Bilanço Değerlendirmesi

Tarih: [GG.AA.YYYY]  Fiyat: [XX.XX TL]  Hedef: [XX TL]
Potansiyel: [+/-X%]  Tavsiye: [AL / TUT / AZALT / ÇIK]  PD: [X mn TL]  FD: [X mn TL]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Değerlendirme: [GÜÇLÜ POZİTİF / SINIRLI POZİTİF / NÖTR / OLUMSUZ]

[Şirket adı], [dönem]'te [gelir/FAVÖK/net kâr] [konsensüs beklentisi X]'nin
[üstünde/paralel/altında] [Y] açıkladı.

■ **[Başlık 1 — en önemli bulgu, kalın]**

[2-3 cümle: sayıyla başla, gerçekleşmeyi beklentiyle karşılaştır, neden önemli?
Örnek: "4Ç25 geliri 6.276 mn USD ile Deniz Yatırım beklentisi olan
6.152 mn USD'nin %2 üzerinde gerçekleşti. Yolcu gelirleri %12,7
büyürken kargo birim gelirlerindeki düşüş (-3,4%) dengeleyici etki yarattı."]

■ **[Başlık 2 — ikinci önemli bulgu]**

[2-3 cümle: yukarıdaki formata uygun]

■ **[Başlık 3 — tez etkisi veya forward bakış]**

[2-3 cümle: Bu sonuç tezi güçlendirdi mi, zayıflattı mı?]

[Hedef fiyat ve tavsiye kararı: "Hedef fiyatımızı [X→Y] TL'ye revize ediyoruz /
koruyoruz. [AL/TUT/AZALT/ÇIK] tavsiyemizi sürdürüyoruz."]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Beat/Miss Özeti:

| Metrik | Beklenti | Gerçekleşme | Fark |
|--------|----------|-------------|------|
| Gelir | X mn | X mn | +X% |
| FAVÖK | X mn | X mn | +X% |
| Net Kâr | X mn | X mn | +X% |
```

### Yazım Kuralları

| Kural | Doğru | Yanlış |
|-------|-------|--------|
| Bullet yapısı | `■ **Başlık** — açıklama` | `- Başlık: ...` veya `* ...` |
| Sayıyla başla | "4Ç25 geliri 6.276 mn USD..." | "Gelir beklentilerin üzerinde..." |
| Beklenti vs gerçek | Her bullet'ta fark belirtilmeli | Sadece gerçekleşmeyi yaz |
| Tez bağlantısı | Son bullet teze bağlanmalı | Sadece rakam özeti yapma |
| Tavsiye kararı | Her raporda açıkça belirt | "Değerlendirmemiz devam ediyor" |
| Değerlendirme notu | "Güçlü Pozitif / Sınırlı Pozitif / Nötr / Olumsuz" | Yıldız sistemi veya puan |
