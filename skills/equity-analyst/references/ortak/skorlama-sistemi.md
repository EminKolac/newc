# Quality Value Skorlama Sistemi v2.0

> Bu sistem hisse kalitesini ve değerleme cazibesini **tek bir sayısal çerçevede** sentezler.
> Teknik analiz yoktur. Zamanlama kararları bu sistemin kapsamı dışındadır.
> Kaynak: İlker'in Quality Value metodolojisi + Damodaran sermaye verimliliği çerçevesi.

---

## Felsefe

> "Ucuz + Hendekli = İdeal Yatırım. Ucuz + Hendeksiz = Value trap (en tehlikeli)."

Bir hissenin çekiciliği iki soruya indirgenebilir:

1. **Kalite:** Bu şirket gerçekten iyi bir iş mi? (ROIC, moat, büyüme kalitesi)
2. **Fiyat:** Bu iş bugün makul bir fiyattan satılıyor mu? (İNA ve comps'a göre)

Bu iki sorunun cevabı ayrı ayrı değerlendirilir. Kalitesiz şirket ucuz olsa da değer tuzağıdır.

---

## Skor Yapısı

```
Toplam Skor = Kalite Skoru (%60) + Değerleme Skoru (%40)
```

**Ağırlık gerekçesi:** Kalite daha ağır çünkü değer tuzağı — iyi fiyat, kötü iş — en sık kayıp nedenidir. Aynı zamanda kaliteyi değerlendirmek daha zordur; daha fazla dikkat hak eder.

---

## Bölüm A: Kalite Skoru (%60 ağırlık)

Kalite skoru 4 alt bileşenden oluşur.

### A1. Sermaye Verimliliği — %25 ağırlık (KALİTE'nin içinde)

**Birincil metrik:** ROIC (Yatırılan Sermaye Getirisi)

| ROIC | Skor | Yorum |
|------|------|-------|
| >%25 | 90-100 | Güçlü moat kanıtı — sermaye için nadir getiri |
| %18-25 | 75-89 | Kaliteli iş, sürdürülebilir rekabet avantajı |
| %12-18 | 55-74 | İyi, WACC üzerinde — ancak moat sorgulanabilir |
| %8-12 | 30-54 | Zayıf — WACC civarında, değer yaratımı belirsiz |
| <%8 | 0-29 | 🔴 **VETO** — Sermaye maliyetini karşılamıyor |

> Veto kuralı: ROIC <%8 → bu kategoride skor ne olursa olsun, Toplam Skor maksimum 40'tır.

**İkincil metrik:** S/C (Sales/Capital — sektör ortalamasıyla karşılaştır)
- S/C > sektör ortalaması → +5 bonus
- S/C < sektör ortalamasının yarısı → -5 ceza

---

### A2. Nakit Akışı Kalitesi — %15 ağırlık

**Birincil metrik:** SNA (Serbest Nakit Akışı) Marjı

| SNA Marjı | Skor | Yorum |
|-----------|------|-------|
| >%20 | 90-100 | Güçlü nakit üreticisi — kârı nakde dönüyor |
| %12-20 | 75-89 | İyi SNA kalitesi |
| %6-12 | 50-74 | Orta — CapEx yoğunluğuna dikkat |
| %0-6 | 20-49 | Zayıf |
| Negatif | 0-19 | 🔴 **VETO** — Para yakıyor |

> Veto kuralı: SNA negatif → Toplam Skor maksimum 40'tır.

**SNA kalite testi:** FCF / Net Kâr oranı kontrol et.
- >0.85 → Kâr nakde dönüyor (yüksek kalite)
- 0.50-0.85 → Orta kalite
- <0.50 → Kâr kalitesi düşük (ör: çalışma sermayesi tuzağı, gerçek dışı kâr)

---

### A3. Büyüme Kalitesi — %12 ağırlık

Büyüme kalitesi, büyüme hızından önemlidir. Kârsız büyüme değer yıkar.

**Değerlendirme:**

| Koşul | Skor |
|-------|------|
| ROIC>WACC + %15+ reel büyüme | 90-100 |
| ROIC>WACC + %8-15 reel büyüme | 70-89 |
| ROIC>WACC + %0-8 reel büyüme | 50-69 |
| ROIC<WACC + herhangi bir büyüme | 0-30 (büyüme değer yıkıyor) |
| Negatif büyüme (3Y+) | 0-20 |

**Büyüme tutarlılığı:** 5Y büyüme volatilitesi yüksekse (çeyrekten çeyreğe %30+ dalgalanma) → -10 ceza.

---

### A4. Moat Gücü — %8 ağırlık

SKILL.md'deki moat değerlendirmesinden türetilir (0-10 skor).

| Moat Skoru (0-10) | Skor |
|-------------------|------|
| 8-10 | 90-100 |
| 6-7 | 65-89 |
| 4-5 | 40-64 |
| 2-3 | 15-39 |
| 0-1 | 0-14 |

**Moat Barometresi entegrasyonu:** Terminal ROIC >> WACC → moat skoru bir kademe yükselt.

---

### Kalite Skoru Hesaplama

```
KaliteSkoru = (A1_skor × 0.25 + A2_skor × 0.15 + A3_skor × 0.12 + A4_skor × 0.08) / 0.60
```

**Özel Kural — Çift Veto:**
A1 veto (ROIC <%8) **veya** A2 veto (SNA negatif) tetiklenirse:
- Kalite Skoru 40/100'ü geçemez
- Toplam Final Skor 40/100'ü geçemez
- Bu durum açıkça raporlanır

---

## Bölüm B: Değerleme Skoru (%40 ağırlık)

Değerleme skoru üç yöntemden gelir. Mevcut tüm yöntemler kullanılır; ağırlıklar aşağıda.

### B1. İNA (İçsel Değer) İskontosu — %20 ağırlık

bbb-dcf Faz 2 çıktısından türetilir.

| İNA / Mevcut Fiyat | Skor | Yorum |
|-------------------|------|-------|
| >1.40 (%40+ ucuz) | 90-100 | Olağanüstü margin of safety |
| 1.20-1.40 (%20-40 ucuz) | 70-89 | Cazip |
| 1.05-1.20 (%5-20 ucuz) | 50-69 | Makul |
| 0.90-1.05 (±%10) | 30-49 | Nötr |
| <0.90 (%10+ pahalı) | 0-29 | Pahalı |

**Duyarlılık notu:** İNA hesaplaması varsayım-bağımlıdır. Bu skoru yorumlarken duyarlılık aralığını da belirt. "İNA iskontosu %28, duyarlılık aralığı %10-%45."

---

### B2. Göreceli Değerleme (Comps) İskontosu — %12 ağırlık

`karsilastirmali-degerleme.md`'deki comps tablosundan türetilir.

| Hedef EV/FAVÖK / Peer Medyanı | Skor | Yorum |
|-------------------------------|------|-------|
| <0.70 (%30+ ucuz) | 90-100 | Peer'lara derin iskonto |
| 0.70-0.85 (%15-30 ucuz) | 70-89 | Cazip görece değerleme |
| 0.85-1.00 (≤%15 ucuz) | 50-69 | Hafif iskonto |
| 1.00-1.15 (hafif prim) | 30-49 | Nötr/hafif pahalı |
| >1.15 (%15+ prim) | 0-29 | Peer'lara prim — gerekçe gerekli |

**Prim istisnası:** Şirket peer'larından yapısal olarak üstünse (ROIC %50 daha yüksek), prim haklıdır. Bu durumu açıkça yaz.

---

### B3. Forward F/K vs Tarihsel Ortalama — %8 ağırlık

`task3-hedef-fiyat.md` §1C'den türetilir.

| Forward F/K / 5Y Ort. F/K | Skor | Yorum |
|--------------------------|------|-------|
| <0.70 (%30+ iskonto) | 90-100 | Tarihsel iskontosu yüksek |
| 0.70-0.85 | 70-89 | Tarihsel iskonto |
| 0.85-1.00 | 50-69 | Hafif iskonto veya paralel |
| 1.00-1.20 | 30-49 | Tarihsel prime yakın |
| >1.20 | 0-29 | Tarihsel prime göre pahalı |

---

### Değerleme Skoru Hesaplama

```
DeğerlemeSkoru = (B1_skor × 0.20 + B2_skor × 0.12 + B3_skor × 0.08) / 0.40
```

---

## Final Skor ve Karar

```
FinalSkor = KaliteSkoru × 0.60 + DeğerlemeSkoru × 0.40
```

### Karar Matrisi

| Final Skor | Kalite Skoru | Karar | Conviction | Açıklama |
|-----------|-------------|-------|------------|---------|
| 80-100 | >70 | **EKLE** | Yüksek | Hem kaliteli hem ucuz |
| 70-79 | >60 | **EKLE** | Orta | Cazip, bazı soru işaretleri var |
| 60-69 | >55 | **İZLE** | Düşük | Makul, daha iyi giriş veya veri bekle |
| 45-59 | Herhangi | **TUT** | — | Mevcut pozisyon için koru |
| <45 | Herhangi | **KAÇIN** | — | Kalite veya değerleme yetersiz |

**Özel durum — Quality Trap:**
- Final Skor >70 ama Kalite Skoru <50 → **KAÇIN** (pahalı ve düşük kalite)

**Özel durum — Value Trap Uyarısı:**
- Değerleme Skoru >80 ama Kalite Skoru <40 → **DEĞER TUZAĞI RISKI ⚠️**
- Tezde "Neden value trap değil?" sorusu cevaplanmalı

---

## Çıktı Formatı

```
## Quality Value Skoru — [ŞİRKET] ([TICKER])
**Tarih:** [YYYY-MM-DD] | **Hisse Fiyatı:** X TL

### Kalite Skoru (%60 ağırlık)
| Bileşen | Alt Skor | Ağırlık | Katkı | Notlar |
|---------|----------|---------|-------|--------|
| A1 Sermaye Verimliliği (ROIC: %X) | XX | 25% | XX | [Veto var mı?] |
| A2 SNA Kalitesi (%X marj) | XX | 15% | XX | FCF/Net Kâr: Xx |
| A3 Büyüme Kalitesi (%X reel) | XX | 12% | XX | ROIC>WACC? |
| A4 Moat Gücü (X/10) | XX | 8% | XX | Terminal ROIC vs WACC |
| **Kalite Toplamı** | | 60% | **XX** | |

### Değerleme Skoru (%40 ağırlık)
| Bileşen | Alt Skor | Ağırlık | Katkı | Notlar |
|---------|----------|---------|-------|--------|
| B1 İNA İskontosu (%X ucuz/pahalı) | XX | 20% | XX | Duyarlılık aralığı |
| B2 Comps İskontosu (EV/FAVÖK Xx vs Xx peer) | XX | 12% | XX | |
| B3 Forward F/K vs Tarihsel (Xx vs Xx) | XX | 8% | XX | |
| **Değerleme Toplamı** | | 40% | **XX** | |

### Final Skor: XX/100 → [EKLE / İZLE / TUT / KAÇIN]
**Conviction:** [Yüksek / Orta / Düşük]
**Quality Value Matrisi:** [Ucuz+Hendekli ✅ / Pahalı+Hendekli / Ucuz+Hendeksiz ⚠️ / Pahalı+Hendeksiz ❌]

**Uyarılar:**
- [ ] Veto tetiklendi mi? (ROIC <%8 veya SNA negatif)
- [ ] Value trap riski var mı?
- [ ] Skor mevcut analizden mi türetildi? (T2 + T3 tamamlanmış olmalı)
```

---

## Sınırlar ve Uyarılar

1. **Bu skor nihai karar değildir.** "ÖNCE KARAR" süreci (SKILL.md) bu skorun üzerine kurulur — İlker'in onayı zorunludur.
2. **Döngüsel şirketler:** A3 büyüme kalitesi için normalized earnings kullan (`task2-finansal-modelleme.md §9`).
3. **Erken aşama / zarar eden şirketler:** B1 İNA uygulanamaz, B3 Forward F/K anlamsız olabilir. Bu durumda değerleme ağırlığı düşer, kalite daha ağır tartılır.
4. **Bankalar:** ROIC yerinde ROE kullan. SNA yerinde temettü kapasitesi değerlendir.
5. **Bu skor teknik analizi içermez.** Zamanlama için ayrı değerlendirme yapılır — ancak bu sistemde yeri yoktur.

---

| Tarih | Değişiklik |
|-------|-----------|
| Orijinal | v1.0 — F/K + PD/DD + Teknik üçlü ağırlık sistemi |
| 2026-03-18 | v2.0 — **TAM REFACTOR.** Teknik analiz kaldırıldı. Quality Value felsefesiyle yeniden inşa edildi: Kalite %60 (ROIC, SNA, büyüme kalitesi, moat), Değerleme %40 (İNA, comps, forward F/K). Çift veto kuralı, value trap uyarısı, quality trap özel durumu. |
