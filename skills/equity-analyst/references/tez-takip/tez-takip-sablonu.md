# Thesis Tracker — Yatırım Tezi Takip Sistemi

## Felsefe

Tez yazmak işin yarısı; takip etmek diğer yarısı. Çoğu yatırımcı tez yazar, verdikleri kararı gerekçelendirir, ama sonra tezi izlemeyi bırakır. Sonuç: confirmation bias — sadece tezi destekleyen veriyi görürsün, çürüten veriyi kaçırırsın.

> "A thesis should be falsifiable — if nothing could disprove it, it's not a thesis."

---

## 1. Thesis Scorecard (Her Tez İçin Zorunlu)

Tez yayınlandığında veya karar verildiğinde bu tablo oluşturulur ve `research/companies/{TICKER}/thesis_scorecard.md` dosyasına kaydedilir.

### Scorecard Template

```
# [ŞİRKET] Thesis Scorecard

**Tez Tarihi:** [YYYY-MM-DD]
**Pozisyon:** [Long / Short / Watch]
**Verdict:** [AL / TUT / AZALT / ÇIK]
**Conviction:** [Yüksek / Orta / Düşük] — [%X güven]

## Core Thesis (1-2 cümle)
[Temel yatırım argümanı]

## Pillar Tracking

| # | Pillar | Orijinal Beklenti | Güncel Durum | Trend | Son Güncelleme |
|---|--------|-------------------|-------------|-------|----------------|
| 1 | [Büyüme] | [Beklenti] | [Durum] | ↑/→/↓ | [Tarih] |
| 2 | [Marj] | [Beklenti] | [Durum] | ↑/→/↓ | [Tarih] |
| 3 | [Moat] | [Beklenti] | [Durum] | ↑/→/↓ | [Tarih] |
| 4 | [Değerleme] | [Beklenti] | [Durum] | ↑/→/↓ | [Tarih] |
| 5 | [Katalizör] | [Beklenti] | [Durum] | ↑/→/↓ | [Tarih] |

## Kill Criteria (Tez Ne Zaman Çöker?)
- [ ] [Spesifik, ölçülebilir kriter 1]
- [ ] [Spesifik, ölçülebilir kriter 2]
- [ ] [Spesifik, ölçülebilir kriter 3]

## Update Log

| Tarih | Veri Noktası | Etkilenen Pillar | Etki | Aksiyon |
|-------|-------------|-----------------|------|---------|
| [Tarih] | [Ne değişti] | [#X] | Güçlendirdi/Zayıflattı/Nötr | Değişiklik yok / Conviction ↓ |
```

---

## 2. Update Süreci

### Ne Zaman Güncellenir?
- Çeyreklik sonuçlar açıklandığında (ZORUNLU)
- Önemli haber/gelişme olduğunda
- Sektörel değişim olduğunda (regülasyon, rakip hamlesi)
- Makro ortam değiştiğinde (faiz, kur, enflasyon)
- Minimum: Her çeyrekte 1 kez

### Güncelleme Formatı

Her güncelleme Update Log'a eklenir:

```
| 2026-03-15 | Q4 EBITDA marjı %18→%16 | #2 (Marj) | Zayıflattı | Conviction: Yüksek→Orta |
```

### Disconfirming Evidence Kuralı

Tezi ÇÜRÜTEN kanıtları tezi DESTEKLEYEN kanıtlarla aynı titizlikle kaydet. Her güncelleme girişinde kendine sor:

1. Bu veri tezimi güçlendiriyor mu, zayıflatıyor mu?
2. Bu veriyi görmezden gelme eğilimim var mı? (confirmation bias check)
3. Kill criteria'dan herhangi biri tetiklendi mi?

---

## 3. Conviction Seviyeleri

| Seviye | Tanım | Aksiyon |
|--------|-------|---------|
| **Yüksek** (80-100%) | Pillar'ların çoğu on-track, kill criteria uzak | Tam pozisyon |
| **Orta** (50-79%) | Bazı pillar'lar sorgulanıyor, risk artmış | Pozisyon küçült veya koru |
| **Düşük** (20-49%) | Birden fazla pillar zayıflamış | Ciddi olarak çıkışı değerlendir |
| **Çökmüş** (<20%) | Kill criteria tetiklendi | ÇIK |

---

## 4. Catalyst Calendar Entegrasyonu

Thesis scorecard'ın altına yaklaşan katalizörleri ekle:

```
## Yaklaşan Katalizörler

| Tarih | Olay | Beklenen Etki | İlgili Pillar |
|-------|------|--------------|---------------|
| [Tarih] | Q1 2026 sonuçları | Büyüme teyidi | #1 |
| [Tarih] | Regülasyon kararı | Moat etkisi | #3 |
```

Her katalizör gerçekleştikten sonra "Gerçekleşen" sütunu eklenir ve Update Log'a yansıtılır.

### Geçmiş Kataliz Arşivi

Gerçekleşen katalizörleri sonuçlarıyla birlikte arşivle — pattern recognition oluşturur:

```
## Geçmiş Katalizörler (Arşiv)

| Tarih | Olay | Beklenen Etki | Gerçekleşen | Öğrenim |
|-------|------|--------------|-------------|---------|
| 2025-Q4 | Yeni fabrika devreye alma | Kapasite +%20 | Gecikti → Q1 2026 | Yönetim timeline'ına %20 buffer ekle |
| 2026-Q1 | Q4 sonuçları | Marj genişlemesi | Beat, marj +120bp | Pricing power teyit |
```

**Neden arşivle?** Yönetimin taahhüt → gerçekleşme oranını ölçer. "Bu yönetim söylediğini yapıyor mu?" sorusuna veri sağlar.

---

## 5. Coverage Universe Katalist Takvimi

Tek bir hisseye değil, tüm takip listesine ait olayları yönetmek için. 10+ hisse takip ediliyorken hangi haftada ne var sorusunu hızlı yanıtlar.

**Dosya konumu:** `research/coverage_calendar.md`

### Coverage Universe Takvim Şablonu

```
# Coverage Universe Katalist Takvimi
**Son güncelleme:** [YYYY-MM-DD]

## Yerli Hisseler (BIST)

| Dönem | Olay | Hisse | Tür | Etki | Pozisyon Etkisi | Durum |
|-------|------|-------|-----|------|-----------------|-------|
| 2026-Q1 sonuçları | Bilanço | THYAO | Çeyreklik | Y | AL tezi test | Bekleniyor |
| 2026-Q1 sonuçları | Bilanço | TBORG | Çeyreklik | O | Marj takibi | Bekleniyor |
| 2026-05 | KAP bildirimi | DOCO | Kurumsal | Y | Genişleme planı | Bekleniyor |

## Yabancı Hisseler

| Dönem | Olay | Hisse | Tür | Etki | Pozisyon Etkisi | Durum |
|-------|------|-------|-----|------|-----------------|-------|
| 2026-Q1 sonuçları | Earnings | PMRTY | Çeyreklik | Y | Yurt dışı büyüme | Bekleniyor |
| 2026-Q1 sonuçları | Earnings | NOVO | Çeyreklik | Y | GLP-1 pazar payı | Bekleniyor |

## Makro / Sektörel Olaylar

| Tarih | Olay | İlgili Hisseler | Etki |
|-------|------|----------------|------|
| Her ay 1. iş günü | OSD verisi | TOASO, FROTO, DOAS | Orta |
| Her ay ~10 | TCMB kararı | Tüm | Yüksek |
| Şubat-Mart | TAPDK verileri | TBORG, AEFES | Orta |
```

**Etki skalası:** Y = Yüksek, O = Orta, D = Düşük

### Veri Kaynakları (Takvim Doldurmak İçin)

**Yerli:**
- KAP.org.tr → "Finansal Raporlar" → dönem takvimi
- BBB Finans araçları → son raporlanan dönem, bir sonraki tahmini çıkar
- Drive kurum raporları → beklenti raporları (4Ç25 el kitapçığı vb.)

**Yabancı:**
- Yahoo Finance `{TICKER} earnings date` araması
- SEC EDGAR 10-Q dosyalama tarihi

### Güncelleme Disiplini

| Ne Zaman | Aksiyon |
|----------|---------|
| Her çeyreklik sonuç açıklandığında | Durum → "Gerçekleşti", Update Log'a ekle |
| Yeni hisse kapsama alındığında | Kapsama tarihi + yaklaşan olaylar ekle |
| Kurum raporu yeni olay duyurursa | Takvime ekle |
| Hisse kapsamadan çıktığında | Satır sil veya "Çıkıldı" not düş |

### Arşivleme

Geçmiş dönemleri silme — `research/coverage_calendar_archive.md`'ye taşı. Her gerçekleşen olayın yanına kısa sonuç notu ekle:

```
| 2026-Q4 | THYAO 4Ç25 bilanço | Beat (+%4 FAVÖK) | Tez pillar #1 güçlendi |
```

---

## 6. Katalizör Tipolojisi ve Etki Matrisi

Katalizörler eşit değildir. Türü, kalıcılığı ve zamanlama etkisi farklıdır. Yanlış tipoloji → yanlış conviction değişimi.

### 8 Katalizör Tipi

| Tip | Tanım | Ortalama Hisse Etkisi | Kalıcılık | BIST Kaynakları |
|-----|-------|----------------------|-----------|-----------------|
| **T1 — Çeyreklik Sonuç** | Beklenti üstü/altı bilanço | %3-8 (beat), -%5-12 (miss) | Kalıcı (revizyon) | KAP bilanço açıklaması |
| **T2 — Guidance Revizyonu** | Yönetim beklenti güncelleme | %5-15 | Kalıcı | KAP özel durum bildirimi, basın toplantısı |
| **T3 — M&A / Kurumsal Eylem** | Satın alma, satış, birleşme, ayrışma | %8-20 | Kalıcı (yapısal) | KAP özel durum bildirimi |
| **T4 — Regülasyon Kararı** | TAPDK, BDDK, EPDK, SPK kararı | %5-20 | Kalıcı (yapısal) | Resmi gazete, regülatör duyurusu |
| **T5 — Sektörel Yeniden Fiyatlama** | Sektörün tamamı yeniden değerleniyor | %5-15 (sektör geneli) | Orta (3-9 ay) | Sektör endeksleri, global peer tepkisi |
| **T6 — Yönetim Değişikliği** | CEO, CFO, kilit yönetici değişimi | %3-10 | Belirsiz (bekle-gör) | KAP özel durum bildirimi |
| **T7 — Makro İnfleksiyon** | Faiz kararı, kur hareketi, enflasyon verisi | %2-8 | Geçici (gürültü) | TCMB, TÜİK, BIST tepkisi |
| **T8 — Pozisyon Değişimi** | Kurumsal alım/satım, short kapanışı | %3-8 | Geçici | MKK pay bildirim, KAP hisse geri alım |

### Kalıcılık Kuralı

**Conviction değişimi sadece kalıcı katalizörlerde (T1-T4, T6) yapılır.**

T7 (makro) veya T8 (pozisyon) sonrası fiyat hareketi tek başına conviction'ı değiştirmez.

```
Örnek:
TCMB faiz kararı → hisse %5 düştü → T7 (makro, geçici)
→ Tez pillar'larında değişiklik yok → Conviction DEĞİŞMEZ
→ Fiyat daha cazip hale geldi → "Değerleme" pillar'ı iyileşti → not al

TAPDK yeni lisans izni → hisse %8 düştü → T4 (regülasyon, kalıcı)
→ Moat pillar'ı zayıfladı → Kill criteria'ya yaklaştı → Conviction ↓
```

### Etki Skalası

Coverage calendar'da kullanılan H/O/D skalasını katalizör tipine göre default ata:

| Katalizör Tipi | Default Etki | Override Koşulu |
|---------------|--------------|-----------------|
| T1 çeyreklik | O (orta) | Büyük miss/beat → Y |
| T2 guidance | Y (yüksek) | Her zaman |
| T3 M&A | Y (yüksek) | Küçük boyutsa O |
| T4 regülasyon | Y (yüksek) | Sektörün küçük parçasıysa O |
| T5 sektör | O (orta) | Sektör odak hisseyse Y |
| T6 yönetim | O (orta) | Kilit kurucu/stratejistyse Y |
| T7 makro | D (düşük) | Yüksek kur bağımlılığıysa O |
| T8 pozisyon | D (düşük) | Büyük blok işlemse O |

---

## 7. Tahmin Post-Mortem Protokolü

> "Hataları kaydetmemek, onları tekrar yapmaya davet etmektir." — Bridgewater

Her kapatılan pozisyon veya önemli ölçüde yanılan tahmin için post-mortem zorunludur. Bu, hesap verebilirlik değil, kalibrasyon aracıdır.

### Ne Zaman Tetiklenir?

Post-mortem şu iki durumda yazılır:
1. Pozisyon kapatıldığında (kâr veya zarar)
2. Bir tahmin gerçekleşenden >%20 sapmayla sonuçlandığında (hedef fiyat, gelir tahmini, marj tahmini)

### Post-Mortem Şablonu

```
# [ŞİRKET] Tahmin Post-Mortem
**Tarih:** [YYYY-MM-DD]
**Olay:** [Neydi? Pozisyon kapanışı / Büyük tahmin miss]

## Ne Bekliyorduk?
| Metrik | Tahminimiz | Gerçekleşen | Sapma |
|--------|-----------|-------------|-------|
| [Gelir] | X | Y | ±% |
| [EBIT Marjı] | %X | %X | ±pp |
| [Hedef Fiyat] | X TL | [Gerçekleşen fiyat] | ±% |

## Neden Yanıldık? (Kök Neden)
Aşağıdaki kategorilerden birini seç ve gerekçelendir:

- [ ] **Veri hatası** — Yanlış veri kullandık (kaynak, dönem, para birimi)
- [ ] **Varsayım hatası** — Doğru veri, yanlış projeksiyon (büyüme, marj, kur)
- [ ] **Model hatası** — Metodoloji sorunu (WACC, terminal değer, döngüsellik)
- [ ] **Niteliksel hata** — Moat, yönetim, regülasyon yanlış değerlendi
- [ ] **Zamanlama hatası** — Tez doğru ama katalizör beklediğimizden geç/erken
- [ ] **Bilinmeyene bağlı** — Öngörülemeyen dışsal şok (siyasi, doğal afet, pandemi)

## Ne Öğrendik?

[1-3 spesifik öğrenim — sonraki analizde nasıl uygulayacağız?]

## Bir Sonraki Analiz İçin Kural

[Bu hatadan çıkan 1 somut kural — mümkünse SKILL.md veya ilgili reference dosyasına da ekle]
```

### Post-Mortem Arşivi

Tüm post-mortemler `research/companies/{TICKER}/post_mortem/` altına kaydedilir. Her 6 ayda bir tüm post-mortemler gözden geçirilir, tekrarlayan pattern'ler MEMORY.md'ye taşınır.

```
research/
└── companies/{TICKER}/
    └── post_mortem/
        ├── 2026-Q1_gelir_miss.md
        └── 2026_pozisyon_kapanisi.md
```

### Hata Kategorisi Dağılımı (Takip Et)

```
# Her yıl sonunda kendi hata dağılımını çıkar:
Veri hatası: X%
Varsayım hatası: X%
Model hatası: X%
Niteliksel hata: X%
Zamanlama hatası: X%
Bilinmeyene bağlı: X%
```

Bu dağılım hangi kategoride sistematik zayıflık olduğunu gösterir.

---

## 8. Dosya Konumu

```
research/
├── coverage_calendar.md       ← Coverage universe takvimi (§5)
├── coverage_calendar_archive.md ← Geçmiş dönem arşiv
└── companies/{TICKER}/
    ├── thesis_scorecard.md    ← Bu template ile oluştur
    ├── analysis.md            ← Tam analiz
    ├── earnings_updates/      ← Çeyreklik güncellemeler
    │   ├── Q4_2025.md
    │   └── Q1_2026.md
    └── post_mortem/           ← Tahmin post-mortemleri (§7)
        └── YYYY_olay.md
```
