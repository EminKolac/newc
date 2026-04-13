# Equity Analyst Skill — Kullanım Rehberi

Bu skill, BBB (Borsada Bir Başına) için hisse senedi analizi yapan Kaya agent'ını yönlendirir. Araştırmadan DOCX raporuna kadar tüm süreci kapsar.

---

## Ne Yapılır?

4 tip çıktı üretilebilir:

| # | Çıktı | Ne Zaman | Format | Süre |
|---|-------|----------|--------|------|
| **Ç1** | Fikir Üretimi | "Bu şirkete bakalım mı?" | Markdown, 1 sayfa | ~30 dk |
| **Ç2** | Tam Kapsama Raporu | Şirket ilk kez coverage'a alınıyor | DOCX 30-50 sayfa + Excel | 5 oturum (T1→T5) |
| **Ç3** | Çeyreklik Güncelleme | Sonuçlar açıklandıktan sonra | DOCX 8-12 sayfa | 1 oturum |
| **Ç4** | Çeyreklik Ön Bakış | Sonuçlar açıklanmadan önce | DOCX 3-5 sayfa | 1 oturum |

---

## Nasıl Kullanılır?

### Ç1 — Fikir Üretimi

**Komut örnekleri:**
- "THYAO'ya hızlı bak"
- "Bu şirkete bakmamız lazım mı?"
- "CIMSA'yı filtrele"

**Ne olur:** Kaya 5 dakikada KAP verisini çeker, 6 metriği kontrol eder, moat hızlı değerlendirmesi yapar. Sonuç: İLERLE / BEKLE / ATLA.

**İLERLE derse:** T1 başlatma kararı senden beklenir. "Tamam, T1 başlat" demen yeterli.

**Şablon:** `references/c1-fikir-uretimi/c1-sablon.md`

---

### Ç2 — Tam Kapsama Raporu

**Komut örnekleri:**
- "THYAO'ya coverage başlat"
- "TBORG tam analizi yap"
- "T1 başlat" (zaten Ç1'den İLERLE aldıysa)

**5 ayrı oturumda yapılır (birleştirilemez):**

| Task | Ne Yapılır | Deliverable | Onay Gerekli? |
|------|-----------|-------------|---------------|
| **T1** | Şirket araştırması — sektör, moat, yönetim, rekabet | `{TICKER}_research.md` (6.000+ kel.) | ✅ |
| **T2** | Finansal modelleme — 6 tab Excel, tarihsel + projeksiyon | `{TICKER}_model.xlsx` | ✅ |
| **T3** | Değerleme — DCF (Faz 0→3) + Comps + hedef fiyat | `{TICKER}_DCF_{tarih}.md` | ✅ |
| **Karar** | Kaya verdict sunar → tartışma → İlker karar verir | — | ✅ |
| **T4** | 25-35 grafik üretimi | `charts/` klasörü (PNG) | ✅ |
| **T5** | Rapor yazımı + DOCX birleştirme | `{TICKER}_Rapor_{tarih}.docx` | ✅ |

**Her task sonunda İlker onayı beklenir.** "Devam et" veya "T2 başlat" demen yeterli.

**Giriş noktası:** `SKILL.md` §T1-T5 bölümleri + `references/c2-tam-kapsama/` rehberleri

---

### Ç3 — Çeyreklik Güncelleme

**Komut örnekleri:**
- "THYAO Q4 sonuçlarını değerlendir"
- "TBORG bilanço geldi, güncelleme yaz"
- "Çeyreklik güncelleme hazırla"

**Ön koşul:** Sonuçlar KAP'ta yayınlanmış olmalı. Kaya BBB Finans ile kontrol eder.

**Ne olur:** Veri çekilir, beat/miss tablosu hazırlanır, tez etkisi değerlendirilir, hedef fiyat revize edilir (gerekiyorsa), 8+ grafik üretilir, DOCX rapor yazılır.

**Zorunlu:** Önceki çeyrek yazısından birebir alıntı yapılır. Yoksa Kaya uyarır.

**Şablon:** `references/c3-ceyreklik/c3-sablon.md`

---

### Ç4 — Çeyreklik Ön Bakış

**Komut örnekleri:**
- "THYAO Q1 sonuçları öncesi hazırlık yap"
- "Ön bakış hazırla"
- "Ne bekliyoruz bu çeyrekte?"

**Ne olur:** Drive'daki kurum raporları taranır, konsensüs beklentileri toplanır, 3-5 kritik metrik seçilir, senaryo analizi yapılır.

**Sonuçlar geldiğinde:** Kaya otomatik olarak Ç3'e geçiş önerir.

**Şablon:** `references/c4-on-bakis/c4-sablon.md`

---

## Dosya Yapısı

```
equity-analyst/
│
├── README.md                    ← Bu dosya (nasıl kullanılır)
├── SKILL.md                     ← Agent talimatları (Kaya bunu okur)
│
├── references/                  ← Rehberler ve şablonlar
│   │
│   │  ── 4 Çıktı Şablonu ──
│   ├── c1-fikir-uretimi-sablon.md      Ç1 çıktısı nasıl üretilir
│   ├── (c2-sablon.md kaldırıldı — giriş noktası artık SKILL.md §T1-T5)
│   ├── c3-ceyreklik-sablon.md          Ç3 çıktısı nasıl üretilir
│   ├── c4-on-bakis-sablon.md           Ç4 çıktısı nasıl üretilir
│   │
│   │  ── Metodoloji Rehberleri ──
│   ├── task1-arastirma.md            T1: araştırma nasıl yapılır (detay)
│   ├── task2-finansal-modelleme.md   T2: Excel modeli nasıl kurulur (detay)
│   ├── task3-hedef-fiyat.md      T3: hedef fiyat nasıl türetilir
│   ├── ceyreklik-guncelleme.md         Ç3+Ç4: 5 fazlı metodoloji
│   ├── profesyonel-cikti-rehberi.md    T5: DOCX format spec + assembly
│   ├── task4-grafik-uretim.md        T4: 25+10 grafik kataloğu
│   ├── yazi-kalitesi-rehberi.md        Yazım standardı (içgörü merdiveni)
│   ├── karsilastirmali-degerleme.md    Peer comps framework
│   ├── skorlama-sistemi.md            Quality Value puanlama sistemi
│   │
│   │  ── Konu-Spesifik Araçlar ──
│   ├── turkiye-spesifik-rehber.md      Holding NAV, bankacılık, Türkiye iskontosu, IR analizi
│   ├── fikir-uretimi.md               Sistematik fikir tarama süreci
│   ├── rekabet-analizi-rehberi.md      Rekabet analizi framework
│   ├── tez-takip-sablonu.md           Yatırım tezi izleme kartı
│   ├── sektor-analiz-sablonu.md        Bağımsız sektör raporu şablonu
│   ├── birim-ekonomi-rehberi.md        Dijital/platform şirketleri
│   ├── bist-sektor-metrikleri.md       BIST sektör KPI'ları
│   ├── duzenleyici-ortam-taramasi.md   Regülatör risk kontrol
│   │
│   │  ── Hub / Index ──
│   ├── cikti-sablonlari.md            4 çıktı haritası + bileşen blokları
│   └── analiz-metodolojisi.md          Çapraz referans merkezi + kalite kontrol
│
└── scripts/                     ← Python araçları
    ├── rapor-uret.py                   DOCX üretim motoru
    ├── grafik-uret.py                  Grafik üretim motoru
    └── dcf-dogrulama.py                DCF doğrulama kontrolleri
```

---

## Sık Kullanılan Komutlar

| Senaryo | Diyeceğin | Kaya Ne Yapar |
|---------|-----------|---------------|
| Yeni hisse keşfi | "ASELS'e bak" | Ç1 üretir |
| Coverage başlat | "T1 başlat" | Ç2 T1 başlatır |
| Sonuçlar geldi | "THYAO Q4 değerlendir" | Ç3 üretir |
| Sonuçlar yakın | "TBORG Q1 ön bakış" | Ç4 üretir |
| Devam et | "T2 başlat" / "Devam" | Sonraki task'a geçer |
| Mevcut tezi sor | "THYAO tez durumu ne?" | Tez takip kartı okur |
| Hedef fiyat güncelle | "THYAO hedef fiyatını revize et" | DCF/Comps günceller |

---

## Kurallar (Kaya'nın Uyduğu İlkeler)

1. **Her rakamda kaynak etiketi zorunlu.** Kaynaksız → `[DOĞRULANMADI]`.
2. **KAP verisi BBB Finans araçlarından gelir.** Web scraping veya 3. parti site yasak.
3. **Ç2'de task'lar birleştirilemez.** T1 bitmeden T2 başlamaz.
4. **Moat analizi olmadan tez olmaz.** Quality Value: Kalite %60, Değerleme %40.
5. **Beat/miss her çeyrekte sinyal/gürültü ayrımıyla değerlendirilir.**
6. **Fisher parity her TL DCF'te kontrol edilir.** TL hedef ÷ kur ≈ USD hedef.
7. **Kill criteria ölçülebilir ve spesifik olmalı.** "Kötüye giderse" kabul edilmez.
8. **Önceki çeyrek yazısından alıntı zorunlu** (Ç3'te).

---

## Bağımlılıklar

Bu skill tek başına çalışmaz, şu skill'lerle birlikte kullanılır:

| Skill | Ne İçin |
|-------|---------|
| `bbb-dcf` | DCF değerleme motoru (T3) |
| `bbb-finans` | KAP/İş Yatırım üzerinden finansal veri |
| `yahoo-finance` | Yurt dışı peer şirket verileri |
| `copywriter` | İlker'in yazım sesi (core-dna.md + premium-dna.md) |

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-18 | v1.0 — İnsan kullanıcı için kullanım rehberi oluşturuldu. 4 çıktı tipi, komut örnekleri, dosya yapısı, kurallar. |
