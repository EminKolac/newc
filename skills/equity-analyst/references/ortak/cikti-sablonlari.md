# Equity Analyst — Çıktı Formatları & Şablonlar v3.2

---

## 4 Çıktı Tipi — Canonical Harita

| # | Çıktı | Format | Uzunluk | Canonical Şablon |
|---|-------|--------|---------|-----------------|
| **Ç1** | Fikir Üretimi | Markdown | 1-2 sayfa (800-1200 kel) | → `c1-sablon.md` + `fikir-uretimi.md` (süreç) |
| **Ç2** | Tam Kapsama Raporu | DOCX + xlsx | 30-50 sayfa | → `SKILL.md` §T1-T5 + `references/c2-tam-kapsama/` |
| **Ç3** | Çeyreklik Güncelleme | DOCX | 8-12 sayfa | → `c3-ceyreklik-sablon.md` |
| **Ç4** | Çeyreklik Ön Bakış | DOCX | 3-5 sayfa | → `c4-on-bakis-sablon.md` |

**Sürpriz varsa:** Ç2 DOCX formatı detayı → `profesyonel-cikti-rehberi.md`
**Metodoloji:** Ç3/Ç4 workflow → `ceyreklik-guncelleme.md`

---

## Yazım Kuralları

Tüm çıktılar için geçerli yazım standardı → `SKILL.md` T5 bölümü + `yazi-kalitesi-rehberi.md`
Kaynak & referans protokolü → `profesyonel-cikti-rehberi.md §8K`

---

## Bileşen Kütüphanesi (Tüm Çıktılarda Yeniden Kullanılabilir Bloklar)

> Aşağıdaki bölümler tek başına kullanılacak çıktı şablonları değildir.
> Bunlar Ç1-Ç4 çıktılarına entegre edilen standart **bileşenlerdir**.
> Her bileşenin hangi çıktıda kullanıldığı belirtilmiştir.

---

## 1. Sektör Analizi Çıktısı
> *Kullanım: Ç2 T1 bölümü (Sektör Analizi), bağımsız sektör raporu*

```
## Sektör Analizi: [SEKTÖR ADI]

**TAM:** $X milyar (kaynak) | **CAGR:** %X (dönem, kaynak)
**Döngü:** [Döngüsel/Defansif/Karma]

**Düzenleyici Ortam:** Risk Seviyesi: [Düşük/Orta/Yüksek]
→ Detay: references/ortak/duzenleyici-ortam-taramasi.md

**Porter Özeti:**
- Rekabet: [X/5] — [düzenleyici bulgular dahil]
- Giriş bariyeri: [X/5]
- Genel çekicilik: [X/10]
```

**Kapsamlı sektör raporu için → `references/sektor/sektor-analiz-sablonu.md`**

---

## 2. Moat Analizi Çıktısı
> *Kullanım: Ç2 T1 bölümü (Moat Analizi), Ç1 Moat kısası*

```
## Moat Analizi: [ŞİRKET]

**Ana Moat:** [Türü — Giriş Bariyeri / Değiştirme Maliyeti / Pazar Yapısı / Münhasır Varlık]
**Moat Gücü:** X/10
**Dayanıklılık:** [Yıl tahmini]
**Moat Barometresi:** Terminal ROIC (%X) vs WACC (%X) → [Güçlü / Zayıf / Yok]

**Detay:** [Açıklama, rakip karşılaştırması, tehditler]
```

---

## 3. Finansal Highlights Çıktısı
> *Kullanım: Ç1 (kısaltılmış), Ç2 T2 bölümü, Ç3 Sayfa 4-5*

```
## Finansal Highlights: [ŞİRKET]

### İlker'in 6 Metriği
| Metrik | Son FY | TTM | 5Y Trend | Değerlendirme |
|--------|--------|-----|----------|---------------|
| ROIC | %X | %X | ↑/↓/→ | İyi/Kötü/Mükemmel |
| FCF Marjı | %X | %X | ↑/↓/→ | İyi/Kötü/Mükemmel |
| Brüt Kâr Marjı | %X | %X | ↑/↓/→ | İyi/Kötü/Mükemmel |
| Net Borç/FAVÖK | Xx | Xx | ↑/↓/→ | İyi/Kötü/Mükemmel |
| Ciro Büyümesi | %X | %X | ↑/↓/→ | İyi/Kötü/Mükemmel |
| ROE | %X | %X | ↑/↓/→ | İyi/Kötü/Mükemmel |

### Veto Kontrolü
- [ ] ROIC > %10 → GEÇER / RED FLAG
- [ ] FCF Marjı pozitif → GEÇER / RED FLAG

**Özet:** [2-3 cümle finansal sağlık değerlendirmesi]
```

---

## 4. Peer Karşılaştırma (Comps) Çıktısı
> *Kullanım: Ç2 T3 değerleme bölümü, Ç3 Sayfa 4-5 peer tablosu*

```
## Karşılaştırmalı Değerleme: [ŞİRKET]
**Tarih:** [YYYY-MM-DD] | **Para birimi:** [TL/USD] | **Kur:** [X.XX TL/USD, kaynak]

### Faaliyet Metrikleri
| Şirket | Gelir (mn) | Büyüme % | Brüt Marj | FAVÖK Marjı | ROIC |
|--------|------------|----------|-----------|-------------|------|
| [Target] ★ | X | X% | X% | X% | X% |
| [Peer 1] | X | X% | X% | X% | X% |
| | | | | | |
| **Median** | - | X% | X% | X% | X% |
| **75th** | - | X% | X% | X% | X% |
| **25th** | - | X% | X% | X% | X% |

### Değerleme Çarpanları
| Şirket | PD (mn) | EV (mn) | EV/Gelir | EV/FAVÖK | F/K |
|--------|---------|---------|----------|----------|-----|
| [Target] ★ | X | X | Xx | Xx | Xx |
| | | | | | |
| **Median** | - | - | Xx | Xx | Xx |

### Pozisyonlama
- **EV/EBITDA:** Xx vs medyan Xx → [%] [iskonto/prim] — [haklı mı?]
```

**Tam comps framework → `references/c2-tam-kapsama/karsilastirmali-degerleme.md`**

---

## 5. Değerleme Çıktısı
> *Kullanım: Ç2 T3 (tam değerleme), Ç3 Sayfa 6 (güncelleme), Ç4 Sayfa 4 (hatırlatıcı)*

```
## Değerleme: [ŞİRKET]

### Göreceli (Comps Summary)
| Çarpan | [Şirket] | Peer Medyan | Premium/İskonto |
|--------|----------|-------------|-----------------|
| EV/EBITDA | Xx | Xx | +/-Z% |
| F/K | Xx | Xx | +/-Z% |
| P/FCF | Xx | Xx | +/-Z% |

### İNA (Temel Senaryo)
- Hasılat CAGR: %X | Nihai Büyüme: %X | AOSM: %X
- Nihai Değer Ağırlığı: %X [>%90 ise KIRMIZI BAYRAK]
- **Hedef Fiyat:** X TL | **Potansiyel Getiri:** %Z

### Çift Değerleme Karşılaştırma
| Yöntem | Hedef Fiyat | Fark |
|--------|-------------|------|
| DCF (Base) | X TL | — |
| Comps (Medyan) | X TL | ±Y% |
→ [%20'den fazla fark varsa varsayımları sorgula]

### Sensitivity (ZORUNLU)
| WACC↓ / Terminal g→ | 2% | 2.5% | 3% | 3.5% | 4% |
|----------------------|-----|------|-----|------|-----|
| 8% | $X | $X | $X | $X | $X |
| 9% | $X | $X | $X | $X | $X |
| **10%** | $X | **$X** | $X | $X | $X |
| 11% | $X | $X | $X | $X | $X |
| 12% | $X | $X | $X | $X | $X |
```

---

## 6. Risk Matrisi Çıktısı
> *Kullanım: Ç2 T5 Sayfa 5-7, Ç3 Sayfa 7*

```
## Risk Matrisi

### ✅ Bulls (Olumlu Yönler)
1. [Güçlü yön 1 — veriyle destekle]
2. [Güçlü yön 2]
3. [Güçlü yön 3]

### ❌ Bears (Riskler)
1. [Risk 1 — ölçülebilir: "Pazar payı %5 düşerse → FAVÖK -%15"]
2. [Risk 2]
3. [Risk 3]

### Kill Criteria (Tez Ne Zaman Çöker?)
- [ ] [Spesifik, ölçülebilir kriter]
- [ ] [Spesifik, ölçülebilir kriter]

### Senaryo Analizi
| Senaryo | Olasılık | Hedef | Tetikleyici |
|---------|----------|-------|-------------|
| Bear | %25 | X TL | [Tetikleyici] |
| **Base** | **%50** | **Y TL** | [Normal gidişat] |
| Bull | %25 | Z TL | [Tetikleyici] |
```

---

## 7. Çeyreklik Güncelleme Çıktısı (Kısa Blok)
> *Kullanım: Hızlı inline referans. Tam çıktı → `c3-ceyreklik-sablon.md`*

```
## [ŞİRKET] [X]Ç 20XX Güncelleme: [ÜSTÜNDE / PARALEL / ALTINDA]

### Sonuç Özeti
| Metrik | Beklenti | Gerçekleşme | Fark | Not |
|--------|----------|-------------|------|-----|
| Gelir | X mn TL | X mn TL | +X% | (Kaynak) |

### Bu Çeyrekte Ne Değişti?
[Sadece yeni bilgi — arka plan tekrarlanmaz]

### Tahmin Revizyonu
| Metrik | Eski | Yeni | Değişim | Neden |
|--------|------|------|---------|-------|

### Tez Etkisi
- Conviction: [Önceki] → [Yeni]
- Karar: [Korunuyor / Değişti]
```

**Tam framework → `references/c3-ceyreklik/ceyreklik-guncelleme.md`**

---

## 8. Ç1 — Fikir Üretimi

**Süreç (4 adım: Topla→Sentezle→Sorgula→Karar) → `references/c1-fikir-uretimi/fikir-uretimi.md`**
**Çıktı şablonu → `references/c1-fikir-uretimi/c1-sablon.md`**
*v2.0: SOUL düşünce mimarisi entegrasyonu, sentez + ters İNA + falsifiable hipotez*

## 9. Ç2 — Tam Kapsama Raporu

**Giriş noktası (T1-T5 akışı) → `SKILL.md` §T1-T5 bölümleri**
**DOCX format spesifikasyonu → `references/c2-tam-kapsama/profesyonel-cikti-rehberi.md`**
*Önceki isim: `yatirim-tezi-sablonu.md` (silinmiş — içerik c2'ye taşındı)*

## 10. Ç3 — Çeyreklik Güncelleme

**Canonical şablon → `references/c3-ceyreklik/c3-sablon.md`**
**5-fazlı metodoloji → `references/c3-ceyreklik/ceyreklik-guncelleme.md`**

## 11. Ç4 — Çeyreklik Ön Bakış

**Canonical şablon → `references/c4-on-bakis/c4-sablon.md`**
**§15 metodoloji → `references/c3-ceyreklik/ceyreklik-guncelleme.md §15`**

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-02-10 | v1.0 oluşturuldu |
| 2026-03-17 | v3.0 — Comps çıktısı, earnings update, moat barometresi, veto kontrolü, kill criteria eklendi. Yeni reference dosyalarına cross-link'ler. |
| 2026-03-18 | v3.2 — 4 çıktı tipi canonical haritası eklendi (Ç1-Ç4). Bölümler "Bileşen Kütüphanesi" olarak etiketlendi. §8-11 canonical şablon pointer'larına güncellendi. |
