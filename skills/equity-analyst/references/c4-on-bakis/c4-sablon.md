# Ç4 — Çeyreklik Ön Bakış Çıktı Şablonu v1.0

> **Çıktı Tipi:** Ç4 — Çeyreklik Ön Bakış (Sonuç Öncesi)
> **Format:** DOCX (+ PDF isteğe bağlı)
> **Kullanım:** Sonuçlar açıklanmadan önce. Sonuçlar gelince → Ç3'e geçiş.
> **Metodoloji (§15 Tam Workflow):** `references/c3-ceyreklik/ceyreklik-guncelleme.md §15`
> **Grafik Kataloğu:** `references/c2-tam-kapsama/task4-grafik-uretim.md §3` (E01, E07, E08)

---

## Ç4 ile Ç3 Arasındaki Fark

| | **Ç4 — Ön Bakış** | **Ç3 — Çeyreklik Güncelleme** |
|---|------------------|-------------------------------|
| **Zamanlama** | Sonuç öncesi | Sonuç sonrası (24-48 saat) |
| **Soru** | "Ne bekliyoruz?" | "Ne değişti?" |
| **Birincil veri** | Kurum raporları + beklentiler | BBB Finans / KAP — gerçekleşme |
| **Beat/miss tablosu** | YOK (henüz gerçekleşme yok) | ZORUNLU |
| **Kurum konsensüs tablosu** | ZORUNLU | Opsiyonel |
| **Tahmin revizyonu** | YOK | Varsa EVET |
| **Trigger** | §14 Adım 1: "Sonuçlar açıklanmamış" | Sonuçlar KAP'ta yayınlandı |

**Ön Bakış tamamlandıktan sonra:** Sonuçlar gelince Ç3 şablonunu (`c3-ceyreklik-sablon.md`) başlat.

---

## Minimum Standartlar

| Kriter | Minimum | İdeal |
|--------|---------|-------|
| **Sayfa** | 3 | 4-5 |
| **Kelime** | 1.500 | 2.000-2.500 |
| **Grafik (gömülü)** | 4 | 5-6 |
| **Tablo** | 2 | 3-4 |
| **Format** | DOCX | DOCX + PDF |

---

## Önkoşul Doğrulaması (Başlamadan Önce)

```
□ §14 Adım 1 tamamlandı: Bugünün tarihi yazıldı, sonuçlar henüz açıklanmamış onaylandı
□ Mevcut tez takip kartı okundu → research/companies/{TICKER}/tez_takip_karti.md
□ Şirketin önceki çeyrek güncelleme yazısı okundu (beklenti referansı için)
□ Drive'daki kurum raporları tarandı (§15 Adım 1)
□ En az 2 kurum beklentisi bulundu (3 idealdir)
```

---

## Adım 1: Kurum Raporları Taraması

Drive klasöründen ilgili kurumların beklenti raporlarını çek:

```bash
# Ticker bazlı arama
find "/Users/ilkerbasaran/Library/CloudStorage/GoogleDrive-ilker@borsadabibasina.com/Drive'ım/Drive'ım/borsadabibasina.com/#5 - Kurum Raporları" \
  -name "*{TICKER}*" 2>/dev/null

# Çeyreklik dönem araması (tüm hisseler)
find "/Users/ilkerbasaran/Library/CloudStorage/GoogleDrive-ilker@borsadabibasina.com/Drive'ım/Drive'ım/borsadabibasina.com/#5 - Kurum Raporları" \
  -name "*{DÖNEM}*" 2>/dev/null
# Örnek: "*4Ç25*" veya "*Q4_2025*"
```

**Dosya isimlendirme konvansiyonu:** `{Kurum} - {TICKER} {Dönem}.pdf`
- Örn: `İş Yatırım - THYAO 4Ç25 Kar Beklenti.pdf`

**Arama önceliği:**
1. `{TICKER} {dönem}` içeren PDF — şirkete özel
2. "4Ç25 Kar Beklenti Raporu" gibi multi-hisse raporlar — ticker bazlı bölüm ara
3. Kurum analist toplantı notları

**En az 2 kurum, ideal 3 kurum** beklentisi topla. Daha azsa → `[DOĞRULANMADI]` etiketle.

---

## Adım 2: Beklenti Tablosu

```markdown
## {ŞİRKET} ({TICKER}) — {Dönem} Sonuç Beklentileri

| Metrik | {Kurum A} | {Kurum B} | {Kurum C} | BBB Tahmini |
|--------|-----------|-----------|-----------|-------------|
| Hasılat (mn TL/USD) | | | | |
| FAVÖK (mn TL/USD) | | | | |
| FAVÖK Marjı (%) | | | | |
| Net Kâr (mn TL/USD) | | | | |
| [Sektörel KPI 1] | | | | |
| [Sektörel KPI 2] | | | | |

Kaynaklar: [{Kurum A}, tarih], [{Kurum B}, tarih], [{Kurum C}, tarih]
BBB Tahmini: Önceki çeyrek analizinden türetildi ([dosya referansı]).
```

**BBB Tahmini sütunu:**
- Önceki çeyrekteki analizden türetilir (tez takip kartı + son güncelleme yazısı)
- Eğer önceki analiz yoksa → `[Önceki Analiz Yok]` yaz, sütunu boş bırakma

---

## Adım 3: "İzlenecek 3-5 Kritik Metrik" Seçimi

Sektöre göre doğru metriği seç:

| Sektör | Öncelikli Metrikler |
|--------|-------------------|
| **Bira** | Pazar payı %, hacim (hl), kişi başı tüketim, TAPDK verisi |
| **Havacılık** | Yolcu sayısı, doluluk oranı (load factor), birim gelir (yield, USD) |
| **Bankacılık** | Net faiz marjı (NIM), TGA oranı, kredi büyümesi |
| **Perakende** | LFL büyüme, m² başı satış, mağaza sayısı, e-ticaret payı |
| **Otomotiv** | KKO (kapasite kullanım oranı), ihracat adet, birim FAVÖK |
| **Çimento** | Kapasite kullanımı, ton başı FAVÖK, ihracat |
| **Sağlık** | Yatak kapasitesi, hasta başı gelir, FAVÖK marjı |
| **İnşaat/GYO** | Konut teslimi, ön satış, net nakit pozisyonu |
| **Enerji** | Kapasite faktörü, satış fiyatı (TL/MWh), kurulu güç |
| **Telekomünikasyon** | Abone büyümesi, ARPU, FAVÖK marjı |

---

## Adım 4: Senaryo Çerçevesi

```markdown
## Sonuç Senaryoları

| Senaryo | Koşul | Beklenen Piyasa Tepkisi |
|---------|-------|------------------------|
| **Güçlü Pozitif** | Konsensüs >+%5 beat, kilit metrik güçlü | Kısa vadede belirgin olumlu |
| **Hafif Pozitif** | Konsensüs <%5 beat, mix görünüm | Sınırlı olumlu |
| **Baz / Paralel** | Konsensüse ±%3 | Nötr tepki |
| **Negatif** | Konsensüs miss veya guidance düşürme | Olumsuz tepki |
```

**BIST özelliği:** Önceki dönem piyasa tepkisine bak (tez takip kartından). Her hissenin sürpriz katsayısı farklıdır.

---

## Rapor Yapısı — Sayfa Bazlı

### SAYFA 1: Kapak + Özet

```
[ŞİRKET ADI] ([TICKER])
[X]Ç 20XX Sonuç Beklentileri

Tarih: [GG.AA.YYYY]
Sonuç Açıklanma Tahmini: [YYYY-MM-DD civarı veya "henüz açıklanmadı"]
Mevcut Fiyat: [XX.XX TL]  Hedef: [XX TL]  Potansiyel: [+/-X%]
Tavsiye: [AL / TUT / AZALT / ÇIK]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Bu rapor, [dönem] sonuçları açıklanmadan önce hazırlanmıştır.
Sonuçlar geldiğinde → Ç3 Çeyreklik Güncelleme'ye geçilecektir.

■ **[Bu çeyrekten en önemli beklenti — 1 cümle]**
■ **[Tezi test edecek kilit metrik]**
■ **[Risklerin odak noktası]**
```

---

### SAYFA 2: Beklenti Tablosu + Kritik Metrikler (~800-1.000 kelime)

**Kurum Konsensüs Tablosu:** (Adım 2'den)

Tablo altı yorum zorunlu — 3-5 cümle:
- Beklentiler arasındaki spread ne anlama geliyor?
- BBB tahmini konsensüsün nerede ve neden ayrışıyor?

**İzlenecek 3-5 Kritik Metrik:**

```
■ **[Metrik 1 — Kalın Başlık]**
[Neden bu metrik bu çeyrek kritik? 2-3 cümle. Beklenti nedir, ne olursa tezi etkiler?]
Kaynak: [Beklenti kaynağı]

■ **[Metrik 2]**
[2-3 cümle]

■ **[Metrik 3]**
[2-3 cümle]
```

---

### SAYFA 3: Senaryo Çerçevesi + Tez Etkisi (~500-700 kelime)

**Senaryo Tablosu:** (Adım 4'ten)

**Tez Etkisi Analizi:**

```markdown
## Bu Çeyrekte Tezin Neyi Test Edilecek?

[Tez takip kartından]: Bu çeyrekte hangi pillar doğrulanacak/çürütülecek?

**Pillar [X] — [İsim]:**
[Bu çeyrek bu pillar için nasıl bir test? Güçlü sonuç neyi kanıtlar, zayıf sonuç neyi?)
Beklenti: [Mevcut durum / İzleme kriteri]

**Önceki Çeyrekten Taşınan Soru:**
> "[Önceki güncellemeden alıntı — ne izlemeye aldık?]"
[Bu çeyrekte cevap gelecek mi?]

**Conviction Değişim Riski:**
[Hangi senaryo conviction'ı değiştirir? Ölçülebilir ifade et.]
```

---

### SAYFA 4: Değerleme Hatırlatıcı + Sonraki Adımlar (~300-400 kelime)

**Mevcut Değerleme Durumu:**

| Metrik | Mevcut | Peer Medyan | Yorumu |
|--------|--------|-------------|--------|
| Forward F/K | Xx | Xx | İskonto/prim |
| FD/FAVÖK | Xx | Xx | İskonto/prim |
| P/FCF | Xx | Xx | İskonto/prim |

**Sonuç Sonrası Aksiyon Planı:**

```
□ Sonuçlar açıklandığında → §14 Veri Tazeliği Protokolü başlat
□ Beat/miss analizi: Bu ön bakıştaki 3-5 kritik metriği kontrol et
□ Tez takip kartını güncelle
□ Ç3 Çeyreklik Güncelleme DOCX hazırla (48 saat)
```

---

### SAYFA 5: Grafikler (4 Zorunlu)

Grafikler metin akışı içinde dağıtılır. Her grafik üstünde içgörü başlığı.

| # | Grafik | Sayfa | Not |
|---|--------|-------|-----|
| **E01** | Çeyreklik hasılat progresyonu (son 8 çeyrek) | S.2 | Konsensüs beklentisi noktalı çizgi olarak ekle |
| **E03** | Marj evrimi (son 8 çeyrek) | S.2 | Beklenen marj aralığı gölgeli alan olarak göster |
| **E07** | Hisse fiyatı + hedef fiyat | S.4 | 12-24 ay, hedef fiyat yatay çizgi |
| **E08** | Değerleme çarpan bandı | S.4 | Tarihsel bant, mevcut konum işaretli |

**Opsiyonel:**
- E06 Peer karşılaştırma (Sayfa 3) — konsensüs scatter'ı olarak
- E05 Sektörel KPI trendi (Sayfa 2) — son dönem veriyle

**Grafik başlık örnekleri:**
- ✅ "Gelir büyümesi 4 çeyrektir yavaşlıyor — konsensüs %8 büyüme bekliyor"
- ✅ "Forward F/K 10x — tarihsel 5Y bandının altında"
- ❌ "Çeyreklik Gelir Trendi", "Değerleme Grafiği"

---

## DOCX Üretimi

```bash
# Ön bakış DOCX
python3 ~/.openclaw/workspace/skills/equity-analyst/scripts/rapor-uret.py \
  --sablon preview \
  --ticker {TICKER} \
  --cikti {TICKER}_{DONEM}_OnBakis.docx
```

**⚠️ Not:** `rapor-uret.py`'de `--sablon preview` henüz implement edilmemişse `--sablon earnings` kullanılabilir — içerik kısa tutulur.

**Dosyalama:**
```
research/companies/{TICKER}/ceyreklik/
├── {X}C_{YYYY}_on_bakis.docx   ← Bu Ç4 çıktısı
└── {X}C_{YYYY}_on_bakis.md     ← Markdown draft
```

---

## QC Checklist — 10 Kritik Kontrol

- [ ] Her kurum beklentisinde kaynak + tarih var
- [ ] BBB Tahmini sütunu dolduruldu (veya `[Önceki Analiz Yok]`)
- [ ] En az 2 kurum beklentisi toplandı (1 ise `[DOĞRULANMADI]`)
- [ ] 3-5 kritik metrik seçildi ve neden kritik olduğu açıklandı
- [ ] Senaryo tablosu BIST özelliğiyle (tepki katsayısı) değerlendirildi
- [ ] Tez takip kartı okundu, hangi pillar test edileceği yazıldı
- [ ] Önceki güncelleme yazısından alıntı var
- [ ] 4 zorunlu grafik gömülü — placeholder yok
- [ ] Sonuç geldiğinde Ç3'e geçiş aksiyon planı yazıldı
- [ ] `[GRAFİK: ...]` direktifleri yok — organik metin referansı

---

## Ç4 → Ç3 Geçiş Trigger'ı

Sonuçlar KAP'ta yayınlandığında:

1. `§14 Adım 1`'i tekrar çalıştır → "Sonuçlar açıklandı" → Ç3 moduna geç
2. Bu Ç4 dosyasını arşivle (silme)
3. `c3-ceyreklik-sablon.md`'yi aç, önkoşullar kısmında bu dosyaya referans ver
4. Ç3 raporunda "Ön Bakışta beklentilerimiz şöyleydi..." bölümü yaz

---

## İlgili Dosyalar

| Dosya | Rolü |
|-------|------|
| `references/c3-ceyreklik/ceyreklik-guncelleme.md §15` | Ön bakış 5-adım metodolojisi (tam detay) |
| `references/c3-ceyreklik/ceyreklik-guncelleme.md §14` | Veri tazeliği protokolü (zorunlu) |
| `references/tez-takip/tez-takip-sablonu.md` | Tez takip kartı — pillar durumu |
| `references/c2-tam-kapsama/task4-grafik-uretim.md §3` | E01, E03, E07, E08 grafik fonksiyonları |
| `c3-ceyreklik-sablon.md` | Sonuçlar gelince geçilecek çıktı şablonu |
| `scripts/rapor-uret.py` | DOCX motor |

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-18 | v1.0 — `ceyreklik-guncelleme.md §15`'teki 5-adım workflow bağımsız çıktı şablonuna dönüştürüldü. Ç4 / Ç3 farkı netleştirildi, geçiş trigger'ı eklendi, 4 sayfa yapısı, 10 kontrol QC, 4 zorunlu grafik eşleme. |
