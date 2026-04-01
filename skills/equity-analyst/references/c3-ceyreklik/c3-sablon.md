# Ç3 — Çeyreklik Güncelleme Çıktı Şablonu v1.0

> **Çıktı Tipi:** Ç3 — Çeyreklik Güncelleme
> **Format:** DOCX (+ PDF isteğe bağlı)
> **Kullanım:** Sonuçlar açıklandıktan sonra, 24-48 saat içinde.
> **Metodoloji (5 Fazlı Workflow):** `references/c3-ceyreklik/ceyreklik-guncelleme.md`
> **DOCX Motor:** `scripts/rapor-uret.py --sablon earnings`
> **Grafik Kataloğu:** `references/c2-tam-kapsama/task4-grafik-uretim.md §3` (E01-E12)
> **Model güncelleme önce yapıldıysa:** `references/model-guncelleme/model-guncelleme.md` çıktısı burada input olarak kullanılır — beat/miss tablosu ve estimate revision zaten hazır.

---

## Minimum Standartlar

| Kriter | Minimum | İdeal |
|--------|---------|-------|
| **Sayfa** | 8 | 10-12 |
| **Kelime** | 3.000 | 4.000-5.000 |
| **Grafik (gömülü)** | 8 | 10-12 |
| **Tablo** | 3 | 5-8 |
| **Format** | DOCX | DOCX + PDF |
| **Yayın süresi** | 48 saat | 24 saat |

**Hız > Mükemmellik:** 48 saatten geç yayınlanan güncelleme değer kaybeder.

---

## Önkoşul Doğrulaması (Başlamadan Önce)

```
□ Sonuçlar KAP'ta yayınlandı mı? → BBB Finans ile teyit et
□ Önceki çeyrek yazısı/güncelleme okundu mu? (ZORUNLU alıntı için)
□ Mevcut tez takip kartı okundu mu? → research/companies/{TICKER}/tez_takip_karti.md
□ §14 Veri Tazeliği Protokolü (5 adım) tamamlandı mı?
```

Herhangi biri eksikse → DURMA. Önce tamamla.

---

## Veri Toplama (Faz 1 — Kısaltılmış)

```bash
cd ~/.openclaw/workspace/skills/bbb-finans/scripts

# 1. Güncel finansal tablo
python3 bbb_financials.py {TICKER} --start-year 2023 --end-year 2026 --section all --full

# 2. KAP özet (son 4 dönem)
python3 bbb_kap.py {TICKER} --kap-summary

# 3. Önceki Q yazısını oku → research/companies/{TICKER}/ceyreklik/
```

---

## Rapor Yapısı — Sayfa Bazlı

### SAYFA 1: Kapak + Özet Kutusu (§16 Şablonu)

```
[ŞİRKET ADI] ([TICKER])
[X]Ç 20XX Bilanço Değerlendirmesi

Tarih: [GG.AA.YYYY]  Fiyat: [XX.XX TL]  Hedef: [XX TL]
Potansiyel: [+/-X%]  Tavsiye: [AL / TUT / AZALT / ÇIK]  PD: [X mn TL]  FD: [X mn TL]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Değerlendirme: [GÜÇLÜ POZİTİF / SINIRLI POZİTİF / NÖTR / OLUMSUZ]

[Şirket adı], [dönem]'te [gelir/FAVÖK/net kâr] konsensüs beklentisi [X]'nin
[üstünde/paralel/altında] [Y] açıkladı.

■ **[Başlık 1 — en önemli bulgu]**
[2-3 cümle: sayıyla başla, gerçekleşme vs beklenti, neden önemli]

■ **[Başlık 2 — ikinci önemli bulgu]**
[2-3 cümle]

■ **[Başlık 3 — tez etkisi veya forward bakış]**
[2-3 cümle: Bu sonuç tezi güçlendirdi mi, zayıflattı mı?]

[Hedef fiyat kararı: "Hedef fiyatımızı [X→Y] TL'ye revize ediyoruz /
koruyoruz. [AL/TUT/AZALT/ÇIK] tavsiyemizi sürdürüyoruz."]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Beat/Miss Özeti:

| Metrik | Beklenti | Gerçekleşme | Fark |
|--------|----------|-------------|------|
| Gelir | X mn | X mn | +X% |
| FAVÖK | X mn | X mn | +X% |
| FAVÖK Marjı | %X | %X | +Xbp |
| Net Kâr | X mn | X mn | +X% |
| [Sektörel KPI] | X | X | +/- |
```

**Bullet Yazım Kuralları (§16'dan):**
- `■ **Kalın Başlık**` formatı — tire değil, yıldız değil
- Her bullet sayıyla başlar: "4Ç25 geliri 6.276 mn USD..."
- Her bullet'ta beklenti vs gerçekleşme farkı belirtilir
- Son bullet teze bağlanır

---

### SAYFA 2-3: Detaylı Sonuçlar (~1.000-1.500 kelime)

**Çeyreklik ve Yıllık Performans Tablosu:**

| Metrik | Q[X] 20XX | Q[X] 20XY | QoQ | YoY |
|--------|-----------|-----------|-----|-----|
| Hasılat (mn TL) | | | | |
| Brüt Kâr | | | | |
| FAVÖK | | | | |
| EBIT | | | | |
| Net Kâr | | | | |

| Metrik | FY 20XX | FY 20XY | YoY |
|--------|---------|---------|-----|
| Hasılat | | | |
| FAVÖK | | | |
| Net Kâr | | | |

**⚠️ Kümülatif Raporlama Notu:** Q4 tek başına = FY − 9M. Formülle hesapla, API'den doğrudan alma.

**Marj Evrimi Tablosu:**

| Marj | Q1 | Q2 | Q3 | Q4 | FY | YoY Δ |
|------|----|----|----|----|-----|-------|
| Brüt | | | | | | |
| FAVÖK | | | | | | |
| Net | | | | | | |

Marj değişiminin kaynağı analizi (zorunlu — seç birini):
- [ ] Fiyat artışı (gelir tarafı)
- [ ] Hammadde maliyeti (maliyet tarafı)
- [ ] Faaliyet kaldıracı (ölçek)
- [ ] IAS 29 etkisi (muhasebe — gürültü)
- [ ] Bir defalık kalem (gürültü)

**Sektörel KPI Analizi:**

| KPI | Q[X] 20XX | Q[X] 20XY | YoY | Kaynak |
|----|-----------|-----------|-----|--------|
| [Sektöre özgü] | | | | |

*Sektör → KPI eşlemesi: `ceyreklik-guncelleme.md §2D` tablosundan.*

---

### SAYFA 4-5: Metrik Dashboard + Rehberlik (~800-1.200 kelime)

**İlker'in 6 Metriği — Güncel Durum:**

| Metrik | TTM | FY Önceki | Trend | Değerlendirme |
|--------|-----|-----------|-------|---------------|
| ROIC | %X | %X | ↑/→/↓ | |
| FCF Marjı | %X | %X | ↑/→/↓ | |
| Brüt Kâr Marjı | %X | %X | ↑/→/↓ | |
| Net Borç/FAVÖK | Xx | Xx | ↑/→/↓ | |
| Ciro Büyümesi | %X | %X | ↑/→/↓ | |
| ROE | %X | %X | ↑/→/↓ | |

**Veto Kontrolü:**
- [ ] ROIC > %10 → GEÇER / ❌ RED FLAG
- [ ] FCF Marjı pozitif → GEÇER / ❌ RED FLAG

**Yönetim Rehberliği (varsa):**

| Metrik | Önceki Guidance | Yeni Guidance | Değişim |
|--------|----------------|---------------|---------|
| | | | |

BBB Değerlendirmesi: [Guidance'a inanıyor musunuz? Tarihsel doğruluk nedir?]

**Önceki Yazıdan Alıntı (ZORUNLU):**

> "[İlker'in önceki Q yazısından birebir alıntı]"
>
> Gerçekleşme: [Beklentiyle karşılaştırma — 2-3 cümle]

---

### SAYFA 6: Tahmin Revizyonu + Değerleme (~600-800 kelime)

**Tahmin Revizyonu:**

| Metrik | Eski Tahmin (FY) | Yeni Tahmin (FY) | Değişim | Neden |
|--------|-----------------|-----------------|---------|-------|
| Hasılat (mn TL) | | | | |
| FAVÖK Marjı (%) | | | | |
| Net Kâr (mn TL) | | | | |
| **Hedef Fiyat (TL)** | | | | |

**Sinyal/Gürültü Ayrımı:**

| Değişiklik | Sinyal mi? | Gerekçe |
|------------|-----------|---------|
| [Sapma 1] | ✅ / ❌ | |
| [Sapma 2] | ✅ / ❌ | |

**Hedef Fiyat Derivasyonu (Güncelleme):**

| Yöntem | Eski Hedef | Yeni Hedef | Ağırlık |
|--------|-----------|-----------|---------|
| DCF | X TL | X TL | %X |
| Comps | X TL | X TL | %X |
| **Ağırlıklı Ortalama** | **X TL** | **X TL** | — |

Upside/Downside: [Mevcut fiyata göre %X]

---

### SAYFA 7: Risk + Tez Güncellemesi (~600-800 kelime)

**Tez Takip Kartı Güncellemesi:**

| Tez Ayağı | Önceki | Yeni | Değişim | Kanıt |
|-----------|--------|------|---------|-------|
| [Pillar 1] | | | ↑/→/↓ | |
| [Pillar 2] | | | ↑/→/↓ | |
| [Pillar 3] | | | ↑/→/↓ | |

**Conviction:** [Önceki] → [Yeni] | **Karar:** [Korunuyor / Değişti]

**Çıkış Kriterleri Kontrolü:**

| Kriter | Durum | Not |
|--------|-------|-----|
| [Kill criteria 1] | ✅ Güvende / ⚠️ Yaklaşıyor / ❌ Tetiklendi | |
| [Kill criteria 2] | | |

**Bu Çeyrekte Ne Değişti? (Yeni riskler / ortadan kalkan riskler)**

| Değişim | Önceki Durum | Yeni Durum |
|---------|-------------|-----------|
| [Risk 1] | | |

**Sonraki Katalist:**

| Tarih | Olay | Tez Etkisi |
|-------|------|-----------|
| [YYYY-MM] | | |

---

### SAYFA 8-12: Grafikler (8 Zorunlu)

Grafikler metin akışı içinde dağıtılır, sonunda toplanmaz. Her grafik üstünde **içgörü başlığı** (konu değil, bulgu).

**8 Zorunlu Grafik (E01-E08):**

| # | Grafik | Tip | Sayfa |
|---|--------|-----|-------|
| **E01** | Çeyreklik hasılat progresyonu (8-12 çeyrek, YoY büyüme overlay) | Bar + çizgi | S.2 |
| **E02** | Beklenti vs gerçekleşme waterfall | Waterfall / grouped bar | S.1 veya S.2 |
| **E03** | Marj evrimi (brüt + FAVÖK + net, 8 çeyrek) | Çok çizgili | S.3 |
| **E04** | Segment / coğrafi kırılım (çeyreklik mix değişimi) | Stacked bar veya area | S.3 |
| **E05** | Sektörel KPI trendi (sektöre özgü) | Bar + çizgi | S.4 |
| **E06** | Peer karşılaştırma (EV/FAVÖK vs FAVÖK marjı) | Scatter veya grouped bar | S.5 |
| **E07** | Hisse fiyatı + hedef fiyat (12-24 ay) | Çizgi + yatay çizgi | S.6 |
| **E08** | Değerleme çarpan bandı (tarihsel F/K veya FD/FAVÖK) | Band/area | S.6 |

**Opsiyonel (E09-E12):**

| # | Ne Zaman Ekle |
|---|---------------|
| E09 | Tahmin revizyonu — tahminler >%5 değiştiyse |
| E10 | 6 metrik dashboard — veto tetiklendiyse |
| E11 | FCF trendi — nakit akışında materyal değişim |
| E12 | Yönetim rehberliği vs gerçekleşme — guidance varsa |

**Grafik başlık örnekleri:**
- ✅ "Brüt marj 3. çeyrek üst üste genişledi — fiyatlama gücü korunuyor"
- ✅ "Beklenti %8 beat — hacim artışı ana sürücü"
- ❌ "Marj Grafiği", "Q4 2025 Sonuçları"

**Python kodu:** `references/c2-tam-kapsama/task4-grafik-uretim.md §3` (E01-E12 fonksiyonları)

---

## DOCX Üretimi

```bash
# Çeyreklik güncelleme DOCX
python3 ~/.openclaw/workspace/skills/equity-analyst/scripts/rapor-uret.py \
  --sablon earnings \
  --ticker {TICKER} \
  --cikti {TICKER}_{DONEM}_Guncelleme.docx

# Grafik paketi üret
python3 ~/.openclaw/workspace/skills/equity-analyst/scripts/grafik-uret.py \
  --tip ceyreklik \
  --ticker {TICKER} \
  --cikti-klasor research/companies/{TICKER}/charts/
```

**Dosyalama:**
```
research/companies/{TICKER}/ceyreklik/
├── {X}C_{YYYY}_on_bakis.md      ← Ç4 çıktısı (varsa)
├── {X}C_{YYYY}_guncelleme.docx  ← Bu Ç3 çıktısı
└── {X}C_{YYYY}_guncelleme.md    ← Markdown draft
```

---

## QC Checklist — 15 Kritik Kontrol

Teslim öncesi bu 15 kontrol tamamlanmadan DOCX gönderilmez.

**Veri Doğrulama**
- [ ] Her rakamda kaynak etiketi var (`KAP Q4 2025`, `BBB Finans`)
- [ ] `[DOĞRULANMADI]` etiketi yok (varsa doğrula veya kaldır)
- [ ] Kaynak & referans kontrolü: hyperlink + son sayfa (`profesyonel-cikti-rehberi.md §8K`)
- [ ] Q4 tek başına = FY − 9M formülüyle hesaplandı (kümülatif)
- [ ] §14 Veri Tazeliği Protokolü (5 adım) tamamlandı

**İçerik**
- [ ] Önceki Q yazısından birebir alıntı var (ZORUNLU)
- [ ] Beat/miss tablosu Sayfa 1'de
- [ ] Sinyal/gürültü ayrımı her büyük sapma için yapıldı
- [ ] Çıkış kriterleri kontrol edildi ve sonucu yazıldı
- [ ] Tahmin revizyonu tablosu var (değişmese bile → "neden değişmedi?" yaz)

**Format**
- [ ] Sayfa 1: ■ bullet yapısı, sayıyla başlayan açıklamalar
- [ ] Değerlendirme notu: "Güçlü Pozitif / Sınırlı Pozitif / Nötr / Olumsuz"
- [ ] 8 zorunlu grafik gömülü (E01-E08) — placeholder yok
- [ ] Grafik başlıkları içgörü formatında
- [ ] `[GRAFİK: ...]` direktifleri yok — organik metin referansı
- [ ] İçindekiler mevcut (8+ sayfa için)

**Minimum Standart**
- [ ] Sayfa ≥ 8 | Kelime ≥ 3.000 | Grafik ≥ 8 | Tablo ≥ 3

---

## İlgili Dosyalar

| Dosya | Rolü |
|-------|------|
| `references/c3-ceyreklik/ceyreklik-guncelleme.md` | 5 fazlı metodoloji + §14 veri tazeliği + §16 yazım kuralları |
| `references/c2-tam-kapsama/task4-grafik-uretim.md §3` | E01-E12 grafik fonksiyonları |
| `references/c2-tam-kapsama/task3-hedef-fiyat.md` | Hedef fiyat güncelleme formülleri |
| `references/tez-takip/tez-takip-sablonu.md` | Tez takip kartı ve çıkış kriterleri |
| `references/ortak/yazi-kalitesi-rehberi.md` | Yazım standardı — içgörü merdiveni |
| `scripts/rapor-uret.py` | DOCX motor (`--sablon earnings`) |
| `scripts/grafik-uret.py` | Grafik üretimi (`--tip ceyreklik`) |
| `c4-on-bakis-sablon.md` | Sonuç öncesi Ç4 → Ç3 geçiş trigger'ı |

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-18 | v1.0 — `ceyreklik-guncelleme.md` metodolojisinden ayrılarak bağımsız çıktı şablonu oluşturuldu. 8 sayfa yapısı, 15 kontrol QC, 8 zorunlu grafik eşleme, DOCX üretim komutları. |
