# Model Güncelleme Workflow

> **Rol:** T2 finansal modelini yeni bilanço veya rehberlik verisiyle güncelle.
> **Çıktı:** Dahili güncelleme notu (DOCX raporu değil). Ç3 hazırlanacaksa bu dosya input olur.
> **Bağımlılık:** T2 finansal model (`{TICKER}_Financial_Model.xlsx`) mevcut olmalı.

---

## Ne Zaman Kullanılır?

| Tetikleyici | Örnek |
|-------------|-------|
| Çeyrek bilanço açıklandı, model güncellenmeli ama rapor henüz yazılmayacak | "THYAO Q4 geldi, modeli güncelle" |
| Çeyrek ortası şirket rehberlik revizyonu | "TBORG guidance revize etti, modeli düzeltelim" |
| Makro değişimi (kur, enflasyon, faiz) modele yansıtılacak | "TCMB politika değişikliği → WACC güncelle" |
| Rakip bilanço geldi, peer comps yenilenmeli | "Rakip sonuçları var, göreceli pozisyon güncellenmeli" |
| Çeyrek bilanço açıklandı VE Ç3 raporu yazılacak | Önce bu workflow → sonra Ç3 şablonuna geç |

**Ç3'ten farkı:**
- Model güncelleme = dahili güncelleme notu, DOCX rapor yok
- Ç3 = tam müşteri/subscriber çıktısı (8-12 sayfa DOCX)
- Ç3 hazırlanacaksa: bu workflow'u tamamla → deliverable'ı Ç3 girdi olarak kullan

---

## Önkoşul Doğrulama

Model güncellemeye başlamadan önce:

```
- [ ] T2 finansal model dosyası mevcut: research/companies/{TICKER}/{TICKER}_Financial_Model.xlsx
- [ ] Yeni dönem verileri KAP'ta yayınlanmış (ya da rehberlik metni hazır)
- [ ] BBB Finans araçlarına erişim var
- [ ] Önceki dönem tahminleri modelde kayıtlı
```

**Eksik varsa:** İlker'e bildir, tamamlanana kadar başlama.

---

## Workflow (5 Adım)

### Adım 1: Yeni Veri Toplama

**Yeni bilanço güncellemesi için:**

```bash
cd ~/.openclaw/workspace/skills/bbb-finans/scripts

# Özet finansallar (son 4 dönem)
python3 bbb_kap.py {TICKER} --kap-summary

# Detaylı tüm tablolar (güncel dönem dahil)
python3 bbb_financials.py {TICKER} --start-year 2022 --end-year 2025 --section all --full

# JSON formatında (programatik erişim)
python3 bbb_financials.py {TICKER} --dcf --json > /tmp/{TICKER}_latest.json
```

**Kaynak kontrolü:**
- Her rakam KAP/BBB Finans'tan — `(KAP, Q4 2025)` etiketi
- [DOĞRULANMADI] kalan rakam varsa birincil kaynakla teyit et
- TTM = `Son Kümülatif + (Önceki FY - Önceki Yılın Aynı Kümülatifi)`

---

### Adım 2: Beat/Miss Tablosu

Yeni gerçekleşme ile önceki tahminleri karşılaştır.

| Metrik | Önceki Tahmin | Gerçekleşme | Fark (%) | Kaynak |
|--------|--------------|-------------|----------|--------|
| Hasılat (TL mn) | | | | (KAP, dönem) |
| Brüt Kâr (TL mn) | | | | |
| FAVÖK (TL mn) | | | | |
| FVÖK (TL mn) | | | | |
| Net Kâr (TL mn) | | | | |
| HBK (TL) | | | | |
| FCF (TL mn) | | | | |
| Net Borç (TL mn) | | | | |
| [Sektöre özel KPI] | | | | |

**Sinyal/Gürültü Ayrımı:**

Her büyük sapma (±%5 ve üzeri) için:
- **Sinyal mi?** → Tez ayağıyla doğrudan bağlantılı, beklenti revizyonu gerektirir
- **Gürültü mü?** → Tek seferlik kalem, sezonsal etki, muhasebe kaydı — forward tahmini değiştirme
- **Belirsiz** → Yönetim yorumunu bekle (bilanço çağrısı / KAP açıklaması)

---

### Adım 3: Tarihsel Tabloyu Güncelle

Excel modeline yeni dönem aktüellerini gir:

**Gelir Tablosu:**
- Yeni çeyrek / yıllık rakamları ilgili sütuna yaz
- TTM sütununu yenile
- Marj hesaplamalarının güncellenmesini kontrol et (formül mü, hardcoded mu?)

**Bilanço:**
- Net Borç güncel değeri
- Pay sayısı (geri alım veya sermaye artışı olduysa)
- Özkaynak

**Nakit Akış:**
- Faaliyet, yatırım, finansman aktiviteleri
- Serbest Nakit Akışı yeniden hesapla

**Kontrol:** Excel audit çalıştır.
```bash
python3 ~/.openclaw/workspace/skills/equity-analyst/scripts/dcf-dogrulama.py \
    {TICKER}_Financial_Model.xlsx --audit
```

---

### Adım 4: Forward Tahmin Revizyonu

Yeni veriye göre forward projeksiyonları güncelle.

**Estimate Revision Tablosu:**

| Metrik | Eski FY (cari yıl) | Yeni FY | Değişim | Eski FY+1 | Yeni FY+1 | Değişim | Neden |
|--------|-------------------|---------|---------|-----------|-----------|---------|-------|
| Hasılat | | | | | | | |
| FAVÖK Marjı | | | | | | | |
| Net Kâr | | | | | | | |
| FCF | | | | | | | |

**Varsayım değişikliği gerekçesi (her satır için):**
- Değişen varsayım nedir? (büyüme oranı, marj, capex)
- Neden değişiyor? (bilanço verisi, rehberlik, sektör dinamiği, makro)
- Sinyal mı gürültü mü? (Adım 2'den devral)

**Senaryo güncellemesi:**
- Bear / Base / Bull senaryolarında varsayım değişikliği var mı?
- Olasılık dağılımı değişti mi?

---

### Adım 5: Değerleme Etkisi

Güncel model ile değerlemeyi yenile.

**Değerleme Özet Tablosu:**

| Yöntem | Önceki Hedef | Yeni Hedef | Değişim | Neden |
|--------|-------------|-----------|---------|-------|
| İNA (DCF) | | | | |
| EV/FAVÖK (comps) | | | | |
| Forward F/K | | | | |
| **Ağırlıklı Hedef** | | | | |

**Rating Değişikliği:**

| | Önceki | Yeni | Değişiklik |
|-|--------|------|-----------|
| Verdict | TUT/EKLE/AZALT/ÇIK | | Değişti / Aynı kaldı |
| Conviction | %X | %X | ↑ / ↓ / → |
| Upside | %X | %X | |

**Tez Etkisi:**
- Hangi tez ayağı etkilendi? (Thesis Pillars'dan hangisi — On-track / Behind / Ahead)
- Kill criteria tetiklendi mi? Hayırsa hangi eşiğe ne kadar yaklaşıldı?
- Thesis scorecard güncellenmeli mi?

---

## Deliverable: Model Güncelleme Notu

**Dosya:** `research/companies/{TICKER}/{TICKER}_model_update_{YYYY-MM-DD}.md`

**İçerik (bu 5 bölüm, başka bir şey ekleme):**

```markdown
# {TICKER} Model Güncelleme — {dönem}, {tarih}

## 1. Beat/Miss Tablosu
[Adım 2 tablosu]

## 2. Estimate Revision
[Adım 4 tablosu]

## 3. Değerleme Etkisi
[Adım 5 özet tablosu]

## 4. Rating/Hedef Fiyat
Verdict: [önceki] → [yeni] | Conviction: %X → %X | Upside: %X → %X

## 5. Tez Etkisi (1-2 paragraf)
[Hangi tez ayağı etkilendi, kill criteria durumu, sonraki gözlem noktası]
```

**ÖNEMLİ:**
- Bu dosya dahili güncelleme notudur — DOCX formatında değil, Markdown
- Rapor yazılacaksa (Ç3) bu dosya input olarak kullanılır
- 5 bölümden fazlası yazılmaz — özet ve "sonraki adımlar" belgesi oluşturma

---

## Ç3'e Geçiş Kararı

Model güncelleme tamamlandıktan sonra:

| Durum | Aksiyon |
|-------|---------|
| Beat/miss önemli, tez etkisi var, rating değişti | Ç3 raporu yaz — model güncelleme notu input |
| Beat/miss sınırlı, tez etkisi yok, rating aynı | Ç3 yazmaya gerek yok — sadece thesis_scorecard.md güncelle |
| Guidance çok önemli değişim | Ç3 yaz, Ön Bakış Güncellemesi (Ç4 yerine) da değerlendirilebilir |
| Sadece model güncellenmesi istendi | Bu workflow yeterli — "Ç3 hazırla" talimatsız Ç3'e geçme |

**Kural:** Ç3'e geçiş kararı İlker'e sorulur. Otomatik geçiş yapılmaz.

---

## Makro / WACC Güncelleme

Bilanço değil, makro değişimi (kur, enflasyon, faiz, Damodaran ERP güncellemesi) tetikleyiciyse:

| Değişen Parametre | Etki | Güncelleme |
|-------------------|------|-----------|
| TCMB politika faizi | WACC (TL) | bbb-dcf skill, WACC modülü |
| Damodaran ERP (ocak güncellemesi) | Tüm USD DCF'ler | `dcf_tools/erp_updater.py` |
| USD/TRY kuru beklentisi | Fisher parity cross-check | TL hedef ÷ kur ≈ USD hedef |
| Ülke riski (CRP) değişimi | WACC (her iki DCF) | Damodaran cross-check |

**Prosedür:** Parametreyi güncelle → DCF yeniden çalıştır → Fisher parity kontrol et → Adım 5 değerleme tablosu.

---

## Kaynak & Referans

Her rakam etiketli olmalı — `profesyonel-cikti-rehberi.md §8K` formatı (kısa format):

| Kaynak | Format |
|--------|--------|
| KAP finansal tablo | `(KAP, Q4 2025)` |
| BBB Finans API | `(BBB Finans, Q4 2025)` |
| TCMB | `(TCMB, Şubat 2026)` |
| Damodaran | `(Damodaran, Ocak 2026)` |
| Şirket IR | `(IR Sunumu, Q4 2025)` |

---

## QC Kontrol Listesi

```
- [ ] T2 Excel modeli güncel dönemle güncellendi
- [ ] Excel audit geçti (--audit modu) → TEMİZ
- [ ] Her rakamda kaynak etiketi var
- [ ] Beat/miss tablosu tamamlandı
- [ ] Estimate revision tablosu tamamlandı (değişmese bile → neden değişmedi yaz)
- [ ] Değerleme yenilendi
- [ ] Rating/Conviction/Upside güncellendi
- [ ] Tez etkisi yazıldı
- [ ] Kill criteria kontrol edildi
- [ ] Dosya: research/companies/{TICKER}/{TICKER}_model_update_{YYYY-MM-DD}.md
- [ ] Ç3 kararı İlker'e soruldu
```

---

## Çapraz Referanslar

| Konu | Dosya |
|------|-------|
| T2 finansal model workflow | `task2-finansal-modelleme.md` |
| Ç3 çeyreklik rapor şablonu | `c3-ceyreklik-sablon.md` |
| Tez takip kartı | `tez-takip-sablonu.md` |
| Hedef fiyat türetimi | `task3-hedef-fiyat.md` |
| Kaynak/referans formatı | `profesyonel-cikti-rehberi.md §8K` |
| Excel audit | `scripts/dcf-dogrulama.py --audit` |
| Fisher parity kontrolü | `bbb-dcf/SKILL.md` |

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-18 | v1.0 — Bağımsız model güncelleme workflow oluşturuldu. 5 adım (veri toplama, beat/miss, tarihsel güncelleme, estimate revision, değerleme etkisi), deliverable formatı, Ç3 geçiş karar tablosu, makro/WACC güncelleme rehberi, QC checklist. |
