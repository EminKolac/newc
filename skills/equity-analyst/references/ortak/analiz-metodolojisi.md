# Equity Analyst — Analiz Metodolojisi & Kalite Kontrol Merkezi

> Bu dosyanın iki rolü var:
> 1. **Kalite Kontrol Checklist** — her analizin sonunda tamamlanması zorunlu 4 kategorili kontrol
> 2. **"Önce Karar Sonra Araştırma"** — BBB analiz felsefesinin temel ilkesi
>
> Tekrarlanan tablolar (moat türleri, 6 metrik, veri hiyerarşisi, çıktı formatları) kaldırıldı.
> Bu bilgiler için tek yetkili kaynaklar:
> - Moat türleri ve örnekler → `SKILL.md` T3 Moat bölümü
> - İlker'in 6 Metriği → `SKILL.md` T3 Finansal Analiz + `skorlama-sistemi.md`
> - Veri kaynakları hiyerarşisi → `SKILL.md` T1 Veri Kaynakları tablosu
> - BBB Finans komutları → `SKILL.md` Araç Kullanımı bölümü
> - 4 Çıktı tipi haritası → `SKILL.md` + `cikti-sablonlari.md`

---

## 5 Aşama Genel Bakış (Pointer Tablosu)

| Aşama | İçerik | Tek Yetkili Kaynak |
|-------|--------|-------------------|
| 1. Sektör Analizi | TAM/SAM, Porter's Five Forces, düzenleyici ortam | `task1-arastirma.md` Bölüm 4, `sektor-analiz-sablonu.md`, `duzenleyici-ortam-taramasi.md` |
| 2. Moat Analizi | 4 moat türü, gücü (0-10), barometresi | `SKILL.md` T3 Moat bölümü |
| 3. Finansal Analiz | 6 metrik, trend, ROIC, veto | `SKILL.md` T3 Finansal Analiz + `task2-finansal-modelleme.md` |
| 4. Çift Değerleme | İNA + Comps + Forward F/K | `task3-hedef-fiyat.md` + `karsilastirmali-degerleme.md` + bbb-dcf |
| 5. Risk & Tez Takip | 3 senaryo, kill criteria, scorecard | `tez-takip-sablonu.md` |

---

## Kalite Kontrol Checklist — Her Analizin Sonu

5 aşama tamamlandıktan sonra bu kontroller yapılır. **Tamamlanmadan rapor çıkmaz.**

### 1. Veri Doğrulama (Kök Kural — SKILL.md §Veri Doğrulama)

| Kontrol | Yöntem |
|---------|--------|
| Tüm BIST finansal verileri KAP/BBB Finans'tan mı? | `bbb_financials.py` çıktısıyla çapraz kontrol |
| Tek kaynaktan gelen rakamlar etiketli mi? | `[TEK KAYNAK — TEYİT GEREKLİ]` etiketi |
| Tahmin edilen / hafızadan alınan rakam var mı? | `[DOĞRULANMADI]` etiketi veya kaldır |
| İki bağımsız kaynak bulunamayan rakam kaldırıldı mı? | TBORG hatası: "~70 lt" fabrike rakam |
| Her rakamda kaynak etiketi var mı? | `(KAP, Q4 2025)` formatı — `profesyonel-cikti-rehberi.md §8K` |

### 2. Argüman Kalitesi (yazi-kalitesi-rehberi.md)

| Kontrol | Standart |
|---------|---------|
| Her bölüm İçgörü Merdiveni Seviye 3+ mi? | Veri aktarımı değil — "ne anlama geliyor?" |
| Consensus farkı sayısal olarak belirtildi mi? | "Piyasa %X, biz %Y görüyoruz" |
| Bear case bull case kadar güçlü yazılmış mı? | Eşit uzunluk + spesifik sayılar |
| Kill criteria ölçülebilir mi? | "Marj <%X" veya "Pazar payı >%Y" gibi |
| Başlıklar içgörü taşıyor mu? | "Rekabet Analizi" ❌ → "Duopol Yapı Giriş Bariyerini Koruyor" ✅ |

### 3. Değerleme Tutarlılığı

| Kontrol | Yöntem |
|---------|--------|
| İNA ve comps farkı <%20 mi? | Değilse açıkla veya ağırlıklandır |
| Sensitivity grid sonucu makul aralıkta mı? | Peer EV/FAVÖK ile çapraz kontrol |
| TL DCF varsa Fisher parity kontrol edildi mi? | TL hedef ÷ kur ≈ USD hedef |
| 4 sanity check yapıldı mı? | `task3-hedef-fiyat.md §9` |
| Hedef fiyat aralık olarak raporlandı mı? | Nokta tahmini + duyarlılık aralığı |

### 4. Sonuç Hazırlığı

| Kontrol | Yöntem |
|---------|--------|
| Quality Value skoru hesaplandı mı? | `skorlama-sistemi.md v2.0` |
| Katalizör tipi tanımlandı mı? | `tez-takip-sablonu.md §6` — T1-T8 hangisi? |
| Tez scorecard dolduruldu mu? | `tez-takip-sablonu.md §1` — conviction, kill criteria |
| Döngüsel şirketse uyarlamalar uygulandı mı? | `task2-finansal-modelleme.md §9` |
| DOCX kaynak & referans sayfası hazır mı? | `profesyonel-cikti-rehberi.md §8K` |
| Excel audit çalıştırıldı mı? | `dcf-dogrulama.py --audit` → TEMİZ |

---

## Önce Karar, Sonra Araştırma

> "Rakamlar hikayeyi değil, hikaye rakamları seçer." — Damodaran

**Yanlış akış:** Veri topla → model kur → ne çıkarsa tezi o yap.

**Doğru akış:**
1. **Şirketi tanı** — sektör, moat, iş modeli (T1'in ilk yarısı)
2. **Ön hipotez kur** — "Bu şirket değerinin altında/üstünde olabilir mi?"
3. **Kill criteria ÖNCE yaz** — hangi varsayımlar tezi çürütür?
4. **Veriyi topla, hipotezi test et** — T1 tamamla + T2 başla
5. **Sonuç veriyle uyuşmuyorsa:** tezi revize et, verideki hatayı bul, veya "geçiyorum" de

**BBB farkı:** Consensus makinesi olmamak. Veriyle desteklenmiş kontraryen görüş değerlidir.

**SKILL.md'deki süreç:**
```
Araştırma (T1-T3) → Kaya verdict sunar → İlker ile tartışma → Karar → Makale (T5)
```

Bu sıra **ATLANAMAZ.** "Önce makale yaz, sonra bakarız" kabul edilmez.

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-02-08 | v1.0 oluşturuldu |
| 2026-03-17 | v3.0 — Cross-reference hub'a dönüştürüldü |
| 2026-03-18 | v3.1 — Kalite kontrol checklist + "Önce Karar Sonra Araştırma" eklendi |
| 2026-03-18 | v4.0 — **Tekrar temizliği.** Moat, 6 metrik, veri hiyerarşisi, BBB Finans komutları, çıktı formatları tabloları kaldırıldı — tek yetkili kaynak pointer'ları eklendi. Dosya artık saf QC + felsefe hub'ı. |
