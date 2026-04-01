# Ç1 — Fikir Üretimi Çıktı Şablonu v2.0

> **Çıktı Tipi:** Ç1 — Fikir Üretimi
> **Format:** Markdown (1-2 sayfa, 800-1200 kelime)
> **Kullanım:** "Bu şirkete bakalım mı?" sorusuna düşünülmüş cevap. Geçerse → T1 başlat.
> **Süreç:** `references/c1-fikir-uretimi/fikir-uretimi.md` (4 adım: Topla→Sentezle→Sorgula→Karar)

---

## Minimum Standartlar

| Kriter | Hedef |
|--------|-------|
| **Uzunluk** | 800-1200 kelime |
| **Format** | Markdown → `research/companies/{TICKER}/fikirler/{TICKER}_fikir_YYYY-MM-DD.md` |
| **Tablolar** | 2 (finansal bakış + ters İNA) |
| **Grafik** | Gerekmez |
| **Kaynak** | Her rakamda zorunlu |
| **Düşünce süreci** | Sentez + Sorgulama bölümleri ATLANAMAZ |

---

## Önkoşul

```
□ Ticker / şirket ismi belli
□ BBB Finans araçları erişimi var (BIST için) veya Yahoo Finance (yurt dışı)
```

---

## Veri Toplama (Adım 1)

```bash
cd ~/.openclaw/workspace/skills/bbb-finans/scripts

# BIST
python3 bbb_kap.py {TICKER} --kap-summary
python3 bbb_kap.py {TICKER} --lookup

# Yurt dışı
python3 bbb_yfinance.py quote {TICKER}
python3 bbb_yfinance.py fundamentals {TICKER}
```

**Minimum veri seti:**
- Piyasa değeri, F/K, EV/FAVÖK, P/FCF
- ROIC, FCF Marjı, Brüt Marj, Net Borç/FAVÖK, S/C
- Son FY ve TTM büyüme oranları
- Sektör ve en yakın 2-3 peer'in EV/FAVÖK medyanı (ters İNA için)

---

## Çıktı Şablonu

```markdown
# {TICKER} — {Tam İsim} | Fikir Üretimi

**Sektör:** {Sektör} | **Tarih:** {YYYY-MM-DD} | **Tarama Türü:** {Quality Value / Deep Value / Growth / Turnaround / Tematik}

---

## Finansal Bakış

| Metrik | Değer | Sektör/Peer Medyan | Değerlendirme |
|--------|-------|--------------------|---------------|
| **Piyasa Değeri** | X mn TL | — | Kaynak: BBB Finans / Yahoo |
| **F/K** | Xx | Yx | Ucuz / Pahalı / Makul |
| **EV/FAVÖK** | Xx | Yx | ±Z% fark |
| **P/FCF** | Xx | Yx | Ucuz / Pahalı / Makul |
| **ROIC** | %X | %Y | 🟢 >%25 / 🟡 %15-25 / 🔴 <%15 |
| **FCF Marjı** | %X | %Y | 🟢 >%15 / 🟡 %10-15 / 🔴 <%10 |
| **Brüt Marj** | %X | %Y | 🟢 >%50 / 🟡 %30-50 / 🔴 <%30 |
| **Net Borç/FAVÖK** | Xx | Yx | 🟢 <2x / 🟡 2-3x / 🔴 >3x |
| **S/C** | Xx | Yx | 🟢 >1.5x / 🟡 1.0-1.5x / 🔴 <1.0x |
| **Ciro Büyümesi (YoY)** | %X reel | %Y | 🟢 >%15 / 🟡 %5-15 / 🔴 Negatif |

**Kaynak:** [BBB Finans / Yahoo Finance, tarih]

### Veto Kontrolü
- [ ] ROIC > %8 → GEÇER / ❌ VETO
- [ ] FCF Marjı pozitif (veya turnaround gerekçesi) → GEÇER / ❌ VETO

⛔ Veto tetiklendiyse → ATLA. Aşağıdaki bölümleri yazma, dosyala ve bitir.
⚠️ Banka/Finans: ROIC yerine ROE >%12. Holding: NAV iskontosu birincil. Turnaround: veto yok, sentezde gerekçe zorunlu. → fikir-uretimi.md §1C

---

## Sentez

**Bu şirketin 3 kelimelik hikayesi:** [Tek cümle — tüm metriklerin toplamı ne söylüyor?]

**Sermaye döngüsü:** Sektör [sermaye akını / konsolidasyon / olgunluk] fazında.
[1-2 cümle: Bu, şirket için ne anlama geliyor? Döngünün bu fazında olmanın yatırım implikasyonu ne?]

**Tutarlılık kontrolü:**
[Marj, hacim, verimlilik, nakit akışı — birlikte mi hareket ediyor? Anomali var mı?]
[Anomali varsa: "Tuhaf olan: [X]. Olası açıklama: [Y]. T1'de araştırılmalı: [Z]"]
[Anomali yoksa: "Dört sinyal tutarlı: [yorumla]"]

**Quality Value Pozisyonu:**
[Ucuz+Hendekli ✅] / [Pahalı+Hendekli ⏳] / [Ucuz+Hendeksiz ⚠️] / [Pahalı+Hendeksiz ❌]

---

## Moat (İlk İzlenim)

**Moat Türü:** [Giriş Bariyeri / Değiştirme Maliyeti / Pazar Yapısı / Münhasır Varlık / YOK]
**Moat Gücü:** X/10 (ilk izlenim — T1'de doğrulanacak)
**Moat Barometresi:** ROIC (%X) vs tahmini WACC (%Y) → [ROIC >> WACC: güçlü moat kanıtı / ROIC ≈ WACC: moat yok / ROIC < WACC: değer yıkımı]

[1-2 cümle: Moat'ı ne oluşturuyor veya neden yok?]

---

## Piyasa Ne Fiyatlıyor? (Hızlı Ters İNA)

### Zımni Büyüme Hesabı

| Parametre | Değer | Kaynak |
|-----------|-------|--------|
| EV/FAVÖK (mevcut) | Xx | BBB Finans / Yahoo |
| EV/FAVÖK (sektör medyan) | Yx | Peer seti |
| Efektif vergi oranı (t) | %Z | Son FY |
| Sektör WACC (yaklaşık) | %W | Damodaran sektör verisi / genel tahmin |
| **Zımni büyüme (şirket)** | %g₁ | g ≈ WACC - 1/(EV/FAVÖK × (1-t)) * |
| **Zımni büyüme (sektör)** | %g₂ | Aynı formül, sektör medyan EV/FAVÖK ile |

*Yaklaşık formül: D&A ≈ CapEx varsayar. Ağır yatırım döneminde sapma olabilir — yorum ekle.

**Yorumlama:**
- Piyasa bu şirkete sektörden [daha yüksek/düşük/benzer] büyüme fiyatlıyor (g₁ vs g₂ farkı: ±X pp)
- Bu varsayım mantıklı mı? [1-2 cümle gerekçe]
- Piyasa haklı olabilir mi? [Evet/Hayır/Belirsiz — dürüst değerlendirme]

**Verilerin söylediği hikaye vs piyasanın fiyatladığı hikaye:**
[2-3 cümle: Adım 2 sentezinin ima ettiği büyüme/kalite ile piyasanın zımni varsayımlarını karşılaştır. Fark var mı? Fark yoksa "veriler piyasayla aynı yere çıkıyor — bu da bir sonuç" de.]

---

## Ön Tez

**Hipotez:** "[Şirket] [neden] [veriler X'i gösteriyor] çünkü [kanıt/gerekçe]."

**Bu hipotezi çürütecek 2 kriter:**
1. [Ölçülebilir, spesifik, izlenebilir — örn: "Same-store büyüme 2 ardışık Q negatif"]
2. [Ölçülebilir, spesifik, izlenebilir — örn: "Net Borç/FAVÖK 3x'i aşarsa"]

**Kill Risk (en kısa vadeli tehdit):** [6 ay sonra %30 düştü — en muhtemel neden ne? 1-2 cümle]

**T1'in cevaplaması gereken 3 soru:**
1. [Spesifik soru — sentezdeki anomaliden veya ters İNA farkından türetilmiş]
2. [Spesifik soru — moat'ın gerçekliğini test eden]
3. [Spesifik soru — kill risk'in olasılığını ölçen]

---

## Karar

**Sonuç:** İLERLE 🟢 / BEKLE 🟡 / ATLA 🔴

**Karar Gerekçesi (4 kriter):**
- [ ] Ön tez hipotezi falsifiable ve spesifik
- [ ] Quality Value pozisyonu: ✅ veya ⏳
- [ ] Sentez tutarlı, 3 soru cevapları birbiriyle çelişmiyor
- [ ] Ters İNA: piyasa varsayımında sorgulanabilir nokta var VEYA piyasa haklı ama kalite güçlü

**(İLERLE: min 3/4 sağlanmalı. ATLA: herhangi bir veto veya 1/4 altı.)**

**Sonraki Adım:** [T1 başlat / Bekle — katalizör: X, tarih: Y / ATLA]

---

## Kaynaklar
- BBB Finans: `bbb_kap.py {TICKER} --kap-summary` (KAP, tarih)
- Sektör WACC: [Damodaran / genel tahmin]
- Peer seti: [en yakın 2-3 peer tickers + EV/FAVÖK medyanı]
- Şirket IR: [link — varsa]
```

---

## Dosyalama Kuralı

```
research/companies/{TICKER}/
└── fikirler/
    └── {TICKER}_fikir_{YYYY-MM-DD}.md   ← Bu Ç1 çıktısı
```

İLERLE kararı → T1 pipeline başlat, aynı klasörde devam et.
ATLA kararı → Dosya arşivde kalır, "Karar: ATLA" kayıtlıdır.
BEKLE kararı → `research/coverage_calendar.md`'e katalizör + tarih ekle.

---

## QC — 8 Kontrol

**Veri:**
- [ ] Her rakamda kaynak var (BBB Finans, Yahoo vb.)
- [ ] Peer/sektör karşılaştırması var (en az 2-3 peer EV/FAVÖK)
- [ ] Veto kontrolü yapıldı

**Düşünce:**
- [ ] Sentez: "3 kelimelik hikaye" yazıldı — template dolgusu değil, gerçek sentez
- [ ] Sermaye döngüsü pozisyonu belirlendi
- [ ] Ters İNA: zımni büyüme hesaplandı ve yorumlandı
- [ ] Ön tez: falsifiable hipotez + 2 kill criteria + T1 soruları yazıldı

**Karar:**
- [ ] Karar matrisi (4 kriter) dolduruldu, İLERLE/BEKLE/ATLA gerekçeli

**Tracking (ZORUNLU — bu olmadan Ç1 tamamlanmış SAYILMAZ):**
- [ ] `research/c1-tracking.json`'a kayıt düşüldü (id, ticker, date, screen_type, source, decision, hypothesis, kill_criteria, entry_metrics, sector)

---

## İlgili Dosyalar

| Dosya | Rolü |
|-------|------|
| `references/c1-fikir-uretimi/fikir-uretimi.md` | Süreç dokümanı — 4 adım, 5 screen türü, tematik tarama |
| `references/ortak/skorlama-sistemi.md` | Quality Value v2.0 — Kalite %60 + Değerleme %40 |
| `references/ortak/standart-metrik-hesaplama.md` | ROIC, FCF, EBITDA hesaplama formülleri |
| `references/c2-tam-kapsama/task1-arastirma.md` | T1 başlatma koşulları (İLERLE sonrası) |
| `references/tez-takip/tez-takip-sablonu.md` | Tez takip kartı — İLERLE → T1 sonunda Ç1 kill criteria buraya taşınır |

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-18 | v1.0 — İlk sürüm. 500-800 kelime, 5 QC. |
| 2026-03-25 | v2.0 — SOUL.md düşünce mimarisi entegrasyonu. Sentez bölümü (3 soru + sermaye döngüsü + anomali). Hızlı Ters İNA (Gordon Growth zımni büyüme hesabı + yorumlama). Ön Tez (falsifiable hipotez + 2 kill criteria + T1 soruları). Yapılandırılmış karar matrisi (4 kriter). QC 5→8 madde. Peer/sektör karşılaştırma sütunu tabloya eklendi. |
