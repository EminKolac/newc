# Senaryo Metodolojisi ve Tutarlilik Cercevesi
# v3.0 | 2026-03-22

> **Amac**: Tum senaryo parametrelerinin (Bear/Base/Bull) turetim formulleri, makro kisitlari,
> **sirkete ozgu girdi katmani**, tutarlilik kontrolleri ve T1-T5 akisindaki senaryo yonetimi
> icin **tek kaynak belge**. Bu dosya task2 (FM) ve task3 (DCF) tarafindan referans alinir.
>
> **v3.0 Yenilik**: Reel/nominal projeksiyon kurali (Bolum 0), WACC metodolojisi (Bolum 0B),
> temettu politikasi (Bolum 0C), kazanc kalitesi kontrolleri (Bolum 0D) eklendi.
> **v2.0 Yenilik**: Sirkete ozgu girdi katmani (Bolum 2A), rejim tespiti (Bolum 2B),
> senaryo tutarlilik matrisi (Bolum 2C), ve Goldman/MS seviyesi ek iyilestirmeler eklendi.

---

## Bolum 0: Temel Cerceve Kurallari (TUMU OKUMADAN DEVAM ETME) ⚠️

> Bu bolum tum senaryo ve degerleme calismasinin ALTINDA yatan cerceve kurallarini icerir.
> Hatali uygulanirsa hedef fiyat %30-60 sapabilir.

### 0A. Reel vs Nominal Projeksiyon Kurali 🔴 KRITIK

```
MUTLAK KURAL: Projeksiyon para birimi ve iskonto orani AYNI BAZDA olmali.
  - Reel buyume + Reel WACC → DOGRU ✅
  - Nominal buyume + Nominal WACC → DOGRU ✅
  - Reel buyume + Nominal WACC → YANLIS ❌ (hedef fiyat %40-60 DUSUK cikar)
  - Nominal buyume + Reel WACC → YANLIS ❌ (hedef fiyat %40-60 YUKSEK cikar)
```

**BBB Standart Yaklasimi (Turk Sirketleri):**

```
IAS 29 uygulaniyorsa → REEL TL DCF birincil
  - Tarihsel veri: IAS 29 duzeltmeli (bbb_financials.py --dcf --json)
  - Projeksiyon buyume: REEL (enflasyon haric)
  - WACC: REEL bazda hesaplanir
  - Terminal buyume: Reel GDP (%3-4 Turkiye)

Dogrulama — Fisher Cross-Check (ZORUNLU):
  (1 + Nominal WACC) = (1 + Reel WACC) × (1 + Beklenen Enflasyon)
  Sapma < %5  → Tutarli ✅
  Sapma %5-10 → Kontrol et ⚠️
  Sapma > %10 → Hata var 🔴

Ikincil Yaklasim (FX Gelir > %70 olan sirketler):
  USD DCF birincil → USD Rf + ERP + CRP, buyume USD bazli
```

**UYARI — En Sik Yapilan Hata:**
IAS 29 duzeltmeli verileri (reel) alip, nominal Turk devlet tahvili faiziyle (%28-31)
iskonto etmek → HATALI. Bu durumda buyume %14 ama WACC %35 → yapay 21pp spread.

**UYARI — Guidance Karsilastirma Hatasi (EBEBK REG):**
Yonetim guidance'i genellikle NOMİNAL'dir. DCF REEL ise, 31,8B reel ile 37B nominal'i
dogrudan karsilastirmak HATALI — okuyucu "model dusuk" sanir.
Ceviri zorunlu: Guidance_Reel = Guidance_Nominal / (1 + π_beklenen)
Ornek: 37B / 1,25 = 29,6B reel → DCF 31,8B aslinda guidance'in %7,5 ustunde.
Bu rekonsilasyon T2 §6A'da yapilir, T5 raporda Guidance Rekonsilasyon Kutusu ile sunulur.

> **Detayli Referans:** `bbb-dcf/methodology/risk_discount.md` §5B,
> `bbb-dcf/methodology/turkey_adjustments.md` §3-4

### 0B. WACC Hesaplama Metodolojisi 🔴 KRITIK

WACC hedef fiyatin en hassas parametresidir (±1pp WACC → ±%10-15 hedef fiyat).
Her bileseni acikca tanimlanmalidir:

```
WACC = Ke × We + Kd × (1-t) × Wd

Ke = Rf + Beta × ERP + CRP + SFP + MQS_etkisi

BILESEN DETAYLARI:
═══════════════════════════════════════════════════════════
Rf (Risksiz Faiz):
  - REEL DCF: ABD 10Y T-bond (%4.2-4.5) + TR CDS spread'i haric
    VEYA TL DİBS nominal faizi Fisher'la reele cevrilir
    Reel_Rf = (1 + Nominal_DİBS) / (1 + Beklenen_Enflasyon) - 1
  - NOMINAL DCF: TL DİBS 10Y (KAP, TCMB EVDS)
  - Kaynak: TCMB EVDS, Bloomberg, Damodaran country data

ERP (Ozsermaye Risk Primi):
  - Damodaran implied ERP (guncellenmis, yillik)
  - Kaynak: pages.stern.nyu.edu/~adamodar/ → implied ERP
  - Tipik deger: %5.5-6.5 (global), %7-9 (gelisen piyasalar)

CRP (Ulke Risk Primi):
  - Damodaran CRP = Ulke temerrut spread × (Ozsermaye vol / Tahvil vol)
  - Kaynak: Damodaran country risk premium tablosu
  - Turkiye: tipik %3-5 (donem bagimli)
  - ALTERNATIF: 5Y CDS spread bazli hesaplama

Beta:
  - Adjusted Beta = 0.33 + 0.67 × Raw Beta (Bloomberg/Blume duzeltmesi)
  - Pencere: 2Y haftalik getiriler (BIST-100 benchmark)
  - Kaynak: Bloomberg, Yahoo Finance, veya bbb_financials.py
  - Senaryo etkisi: Bear +0.1, Base +0, Bull -0.1

SFP (Small Firm Premium / Kucuk Firma Primi):
  - MCap < $250M: +%2.5
  - MCap $250M-$1B: +%1.5
  - MCap > $1B: +%0.5
  - Terminal donemde azaltilir (buyume varsayimi): SFP_term = SFP_explicit × 0.6
  - Kaynak: Duff & Phelps SBBI Yearbook, Damodaran kucuk firma analizi

MQS Etkisi:
  - MQS 24-30: -50bp (yuksek kalite yonetim indirimi)
  - MQS 18-23: 0bp (notr)
  - MQS 12-17: +50bp (dusuk kalite primi)
  - MQS < 12: +100bp (ciddi governance riski primi)

Kd (Borc Maliyeti):
  - Birincil: KAP PDF NOT 13 — agirlikli ortalama faiz orani
  - Alternatif: Sentetik kredi notu → Damodaran default spread tablosu
  - REEL DCF icin: Reel_Kd = (1 + Nominal_Kd) / (1 + π) - 1
  - Vergi sonrasi: Kd × (1 - ETR)

Sermaye Yapisi (We, Wd):
  - Hedef sermaye yapisi (sirketin optimize ettigi)
  - VEYA piyasa degerleri (MCap / (MCap + Net Borc))
  - Senaryo etkisi: Sabit tutulur (ayni sermaye yapisi)
═══════════════════════════════════════════════════════════
```

**DOGRULAMA — WACC Sanity Check:**
```
Reel TL WACC: %10-18 arasi beklenir (Turkiye)
  <%10: Cok dusuk — risk primlerini kontrol et
  >%18: Cok yuksek — SFP veya CRP asiri mi?

Nominal TL WACC: %30-50 arasi beklenir
  <%30: Cok dusuk — Rf veya enflasyon beklentisi kontrol et
  >%50: Cok yuksek — firma spesifik risk asiri mi?
```

> **Detayli Referans:** `bbb-dcf/methodology/risk_discount.md` §1-5

### 0C. Temettu ve Payout Politikasi 🔴 KRITIK

Terminal deger hesabinda payout orani DOGRUDAN hedef fiyati etkiler:

```
Terminal Value = NOPAT × (1 - g/ROC) / (WACC - g)

Burada (1 - g/ROC) = yeniden yatirim orani
  g/ROC YUKSEK → daha cok yeniden yatirim → daha dusuk FCF → daha dusuk TV
  g/ROC DUSUK → daha az yeniden yatirim → daha yuksek FCF → daha yuksek TV

BIST OZEL KURALI:
  - SPK zorunlu temettu dagitimi: Net karin %5'i (minimum)
  - Cogu sirket %20-50 dagitir
  - Temettu politikasi DEGİSKENDİR — yonetimin kararina bagli

SENARYO ETKİSİ:
  Bear: Temettu azaltilir/kesilir → yeniden yatirima yonelir → g/ROC artar
  Base: Mevcut politika devam eder
  Bull: Temettu arttirilir → payout artar → g/ROC azalir
```

**Forward F/K Etkisi:**
```
Forward HBK hesaplanirken:
  - Seyreltilmis (diluted) pay sayisi kullanilmali (opsiyonlar, convertible)
  - Olagan disi kalemler cikarilmali (one-off)
  - IAS 29 parasal kazanc/kayip cikarilmali

Pay Sayisi Kontrolu:
  [ ] Basic vs Diluted farki >%3 mu? → Diluted ZORUNLU
  [ ] Son 2 yil pay sayisi degisti mi? → Seyrelme trendi notu ekle
  [ ] Potansiyel seyrelme kaynaklari? (opsiyon, convertible, bedelli)
```

### 0D. Kazanc Kalitesi Kontrolleri (Earnings Quality) 🟠 ONEMLI

Goldman/MS standart "forensic accounting" kontrolleri — T2'de ZORUNLU uygulanir:

```
KAZANC KALİTESİ KONTROL LİSTESİ (T2 sirasinda doldurulur):

1. Nakit Donusum Kalitesi:
   CFO / Net Kar orani (son 3Y):
   [ ] > 1.0 → Yuksek kalite ✅
   [ ] 0.7-1.0 → Kabul edilir ⚠️
   [ ] < 0.7 → Dusuk kalite — accrual bazli kazanc 🔴
   [ ] Negatif → Ciddi uyari — nakit yakmaya ragmen kar raporluyor 🔴

2. Ticari Alacak Gunleri (DSO) Trendi:
   Son 3Y DSO degisimi:
   [ ] Azaliyor/Sabit → Saglıklı ✅
   [ ] Artiyor (>5 gun/yil) → Agresif gelir tanima riski ⚠️
   [ ] Hasılattan hızlı artıyor → Kırmızı bayrak 🔴

3. Stok Gunleri (DIO) Trendi:
   [ ] Azaliyor/Sabit → Saglıklı ✅
   [ ] Artiyor (>10 gun/yil) → Talep zayiflamasi veya obsolescence ⚠️

4. Iliskili Taraf Islemleri:
   [ ] Hasilatin <%5'i → Duşuk risk ✅
   [ ] %5-15 → Orta risk — detay incele ⚠️
   [ ] >%15 → Yuksek risk — bagimsizlik sorgulanir 🔴
   Kaynak: KAP PDF dipnot "Iliskili Taraflarla Islemler"

5. Bagimsiz Denetim Gorusu:
   [ ] Olumlu (unqualified) → Normal ✅
   [ ] Sartli (qualified) → Risk notu ekle ⚠️
   [ ] Olumsuz/Gorus bildirmeme → Analize devam etme 🔴

6. Olagandisi Kalem Orani:
   Olagandisi Kalemler / Brut Kar:
   [ ] <%10 → Normal ✅
   [ ] %10-25 → Acıklama gerekli ⚠️
   [ ] >%25 → Normalize edilmis kar ZORUNLU kullanilir 🔴

7. Tahakkuk Orani (Sloan Ratio):
   Accruals = (Net Kar - CFO) / Toplam Varlik
   [ ] <%5 → Saglıklı ✅
   [ ] %5-10 → Dikkat ⚠️
   [ ] >%10 → Kazanc manipulasyonu riski 🔴

SONUC:
  7 kontrolden 5+ ✅ → Kaliteli kazanc — FM parametreleri guvenilir
  3-4 ✅ → Orta kalite — normalize edilmis kar kullan, risk notu ekle
  ≤2 ✅ → Dusuk kalite — FM'de konservatif varsayim kullan, Bear agirligini artir (+5pp)
```

> **Bu kontroller T1 §7 "Finansal Derinlemesine" ile birlesitirilir.**
> T2'de FM olusturulurken normalize edilmis kar kullanip kullanmama karari buradan cikar.

---

## Bolum 1: Temel Prensipler

### 1.1 Senaryo Turetim Hiyerarsisi (Oncelik Sirasi)

```
Seviye 1: Makro Kisitlar — TAVAN/TABAN (GDP, enflasyon, FX)
  └─ Terminal buyume ASLA nominal GDP + sektor priminin ustune cikamaz
  └─ Makro koridoru belirler, icerisini sirkete ozgu veriler doldurur

Seviye 2: Sirkete Ozgu Girdi Katmani — CEKIRDEK ⭐ [YENI v2.0]
  └─ Yonetim rehberligi (guidance) → guvenilirlik iskontolu
  └─ Mevcut yatirim donguleri (yeni magaza, yeni ulke, fabrika vb.)
  └─ Pipeline/katalist takvimi (zaman sinirli buyume sureculeri)
  └─ Sirket rejimi (buyume / olgun / toparlanma / donusum)
  └─ Bottom-up gelir dekompoze dogrulamasi

Seviye 3: Tarihsel Veri (sirketin gecmis performansi)
  └─ Base case = normalize edilmis tarihsel ortanca +/- yapisal degisim

Seviye 4: Peer Kasilastirma (sektorel benchmark)
  └─ Marj hedefleri peer 25th-75th yuzdelik araligi icinde olmali

Seviye 5: Konsensus Kalibrasyonu (analist beklentileri)
  └─ Base case konsensusten >5pp sapiyorsa yazili gerekce zorunlu
  └─ Rehberlik vs konsensus farki → asimetrik bilgi gostergesi
```

**KRITIK**: Seviye 1 tavan/taban belirler, ama parametrelerin GERCEK degerini Seviye 2 (sirkete ozgu) ve Seviye 3 (tarihsel) belirler. Sadece dissal kisitlarla senaryo kurmak **sirket analizi degil, makro tahmindir**.

### 1.2 Altin Kurallar

1. **Tek Olcu Birimi**: DCF ve FM ayni marj metrigini kullanmali. Tercih: EBIT marji. FAVOK kullanilirsa, FAVOK→EBIT koprusu (amortisman normalize) zorunlu.
2. **Terminal Buyume Tavani**: Terminal buyume <= Nominal GDP + sektor primi (maks +2pp)
3. **Terminal ROIC Tabani**: Terminal ROIC >= Terminal WACC (negatif spread = deger yok)
4. **Senaryo Aralik Kontrolu**: Bull/Bear hisse degeri araliginin Base'e orani %30-60 olmali (cok dar = anlamsiz, cok genis = belirsizlik)
5. **Formul Bazli Turetim**: Her parametre icin acik turetim formulu, "hissi" deger yok

---

## Bolum 2: Senaryo Parametre Turetim Formulleri

### 2.1 Hasilat Buyumesi (5Y CAGR)

```
Girdi A: Tarihsel 5Y reel CAGR (son 5 yil, IAS 29 duzeltmeli)
Girdi B: Peer medyan 5Y CAGR (Comps tablosu)
Girdi C: Makro buyume beklentisi (reel GDP + sektor primi)

Bear = MIN(Girdi_A - 2pp, Peer Q25, Girdi_C - 1pp)
Base = Konsensus VEYA (Girdi_A + Girdi_B + Girdi_C) / 3
Bull = MAX(Girdi_A + 2pp, Peer Q75, Girdi_C + 2pp)

Kisit: Bear >= 0% (negatif buyume ancak ozel senaryoda)
Kisit: Bull <= Girdi_C + 5pp (surdurulebilirlik siniri)
```

**Not**: Yil bazli buyume profili icin kademeli azalis kullanilir:
- Y1-Y3: Baslangic CAGR (yuksek buyume donemi)
- Y4-Y7: Lineer azalis (olgunlasma)
- Y8-Y10: Terminal buyumeye yaklasim

### 2.2 Terminal Buyume (g)

```
Girdi: Nominal GDP tahmini (T+5), sektor buyume farklilasmasi

Terminal_g_bear = Reel GDP - 0.5pp (pazar payini kaybediyor)
Terminal_g_base = Reel GDP (pazar payini koruyor)
Terminal_g_bull = Reel GDP + 0.5pp (pazar payini artiriyor)

Turkiye icin (2026+):
  Reel GDP konsensus: %3.0 - %4.0
  Terminal g aralik: %2.5 - %4.5

MUTLAK TAVAN: %5.0 (hicbir sektor GDP'nin %1pp ustunde surdurulebilir buyuyemez)
```

**UYARI**: Nominal buyume (enflasyon dahil) kullaniliyorsa, reel-nominal ayrimi acikca belirtilmeli. IAS 29 uygulaniyorsa tum proyeksiyonlar REEL olmali.

### 2.3 EBIT Marji (Hedef / Terminal)

```
Girdi A: Mevcut EBIT marji (normalize - one-off haric)
Girdi B: Peer medyan EBIT marji
Girdi C: Sirketin tarihsel peak EBIT marji (son 7Y)
Girdi D: Yapisal avantaj/dezavantaj degerlendirmesi (-2pp ile +2pp)

Bear = MAX(Girdi_B - 2pp, Girdi_A - 1pp)          [marj baskisi]
Base = (Girdi_B + Girdi_A) / 2 + Girdi_D / 2      [normalize]
Bull = MIN(Girdi_C, Girdi_B + 2pp + Girdi_D)       [tarihsel peak'e yakin]

Kisit: Terminal marj <= Peer Q75 + 1pp (moat primi dahil)
Kisit: Terminal marj >= Peer Q25 (kalici dezavantaj yoksa)
```

### 2.4 WACC

```
WACC = Ke * We + Kd*(1-t) * Wd

Ke = Rf + Beta * ERP + CRP + SFP + MQS_etkisi

Senaryo farkliligi WACC'ta su kaynaklardan gelir:
  - Beta farkliligi: Bear +0.1, Base +0, Bull -0.1
  - SFP farkliligi: Sabit (MCap bazli)
  - MQS etkisi: T1'den gelen MQS skoruna gore (-50bp ile +100bp)

Terminal WACC = Explicit Y1-5 WACC - SFP farklilasmasi - olgunlasma indirimi
```

### 2.5 Terminal ROC (Return on Capital)

```
Terminal ROC = Terminal EBIT marji * (1 - terminal vergi) * S/C

Kisit: Terminal ROC > Terminal WACC (tum senaryolarda)
Kisit: Terminal ROC < %20 (surdurulebilir ust sinir, ozel sektorler haric)

Dogrulama: ROC = Marj * (1-t) * S/C
  Ornek: %10 * 0.75 * 5.0 = %37.5 → UYARI: cok yuksek, S/C veya marj gozden gecir
```

### 2.6 CapEx/Hasilat

```
Girdi A: Tarihsel 3Y ortalama CapEx/Hasilat
Girdi B: Peer medyan CapEx/Hasilat

Bear = Girdi_A + 1pp (daha fazla yatirim gerekiyor)
Base = (Girdi_A + Girdi_B) / 2
Bull = MAX(Girdi_A - 1pp, Girdi_B - 0.5pp)

Kisit: CapEx/Hasilat >= %2 (minimum bakim capex)
```

### 2.7 Efektif Vergi Orani (ETR)

```
Terminal ETR = Yasal vergi orani - tesvik avantaji + IAS 29 duzeltmesi

Bear = Yasal oran (tum tesvikler kalkar)
Base = Yasal oran - 2pp (mevcut tesvik devam eder)
Bull = Yasal oran - 4pp (ek tesvik kazanilir)

Turkiye: Yasal KV %25, tipik ETR %20-23
```

---

## Bolum 2A: Sirkete Ozgu Girdi Katmani ⭐ [v2.0 — YENI]

> **NEDEN GEREKLI**: Bolum 2'deki formüller (tarihsel CAGR, peer medyan, makro kisit) **sektörel ortalama** verir. Ama her sirketin kendine ozgu buyume sureculeri, yatirim dongusu, yonetim beklentileri vardir. Bu bolum, parametreleri sirketin gercek durumuyla harmanlayarak **bottom-up dogrulama** saglar.

### 2A.1 Yonetim Rehberligi (Guidance) Entegrasyonu

Yonetim rehberligi — varsa — senaryo parametrelerine **guvenilirlik iskontolu** olarak dahil edilir.

```
REHBERLIK GUVENIRLILIGI HESAPLAMA:

Girdi: Yonetimin son 2-3 donem rehberlik isabet orani
  Gerceklesen_vs_Rehberlik = ortalama(|Gercek - Rehberlik| / Rehberlik)

Guvenilirlik Skoru (G):
  G = 1.0 — isabet orani %95+ (neredeyse her zaman tutturur)
  G = 0.8 — isabet orani %85-94 (cogunlukla tutar)
  G = 0.6 — isabet orani %70-84 (bazen sapma olur)
  G = 0.4 — isabet orani %50-69 (sik sapma)
  G = 0.2 — isabet orani <%50 (guvensiz — dikkate alinmaz)

Rehberlik yoksa veya ilk defa veriliyorsa: G = 0.5 (notr)

PARAMETRE HARMANLAMA:
  Agirlikli_Deger = G × Yonetim_Rehberligi + (1-G) × Formul_Sonucu

Ornek (EBEBK):
  Yonetim buyume rehberligi: %15
  Formul_Sonucu (Bolum 2.1): %14.4
  G = 0.6 (orta guvenilirlik)
  Base buyume = 0.6 × 0.15 + 0.4 × 0.144 = 0.1476 → %14.8
```

**KISIT**: Rehberlik ne kadar guclu olursa olsun, Bolum 2 kisitlari gecerli. Yonetim "%30 buyume" dese bile terminal buyume tavani asılamaz.

**UYARI**: Rehberlik iyimser mi kotu mu? Egrilim (bias) tespiti yap:
- Surekli iyimser rehberlik → G'yi 0.1 dusur
- Surekli muhafazakar rehberlik → G'yi 0.1 artir + Bull senaryoda yukarı potansiyel not et

### 2A.2 Yatirim Dongusu ve Stratejik Girdi

Sirketin mevcut yatirim/buyume dongusu senaryo parametrelerini dogrudan etkiler:

```
YATIRIM DONGUSU TESPITI (T1 ciktisi olmali):

Soru 1: Sirket son 12-18 ayda buyuk yatirim karari acikladi mi?
  ☐ Yeni pazara giris (ulke/bolge genislemesi)
  ☐ Yeni urun kategorisi lansmani
  ☐ Kapasite artisi (fabrika, depo, magaza)
  ☐ M&A veya stratejik ortaklik
  ☐ Dijital donusum / teknoloji yatirimi
  ☐ Hayir — normal isleyis

Soru 2: Bu yatirim(lar) gelire ne zaman yansir?
  ☐ Zaten yansimaya basladi (FY+0)
  ☐ Gelecek yil baslar (FY+1)
  ☐ 2-3 yil icinde (FY+2-3)
  ☐ Belirsiz

Soru 3: Yatirim buyuklugu (CapEx/Hasilat vs tarihsel ortalama)
  ☐ Normalin %50+ uzerinde → agresif buyume donemi
  ☐ Normalin %20-50 uzerinde → olculü buyume
  ☐ Normal aralıkta → bakim capex
  ☐ Normalin altında → kuculme / tasarruf donemi
```

**SENARYO ETKISI**:

```
Agresif buyume donemi (yeni ulke/magaza acilisi gibi):
  Bear: Yatirim basarisiz — CapEx harcanir ama gelir gelmez
    → CapEx/Hasilat: Tarihsel + 2pp (yüksek yatirim devam eder)
    → Buyume: Formul sonucu - 3pp (yatirim getiri saglamaz)
    → EBIT marji: Formul - 2pp (amortismani yukarı, gelir gelmez)

  Base: Yatirim plan dahilinde sonuc verir
    → CapEx/Hasilat: Yonetim rehberligi (G ile agirlikli)
    → Buyume: Formul + yatirim etkisi (segment bazli ekle)
    → EBIT marji: Kısa vadede baski, orta vadede toparlanma

  Bull: Yatirim beklenenden hizli/buyuk sonuc verir
    → CapEx/Hasilat: Tarihsel - 1pp (verimli yatirim)
    → Buyume: Formul + yatirim upsurge
    → EBIT marji: Olcek ekonomisi hizla devreye girer
```

### 2A.3 Katalist Takvimi (Zaman Sinirli Olaylar)

Her senaryoyu tetikleyecek **spesifik, tarihli olaylar** belirle. Bu Goldman/MS'in "upside/downside catalyst" yaklasimidir:

```
KATALIST TAKVIM SABLONU (T1'de doldurulur, T5'te rapora yazilir):

| # | Katalist | Senaryo | Zamanlama | Olasilik | Etki |
|---|----------|---------|-----------|----------|------|
| 1 | [Ornek: UK ikinci magaza acilisi] | Bull | Q3 FY26 | %60 | Buyume +2pp |
| 2 | [Ornek: Minimum ucret artisi %30+] | Bear | Q1 FY26 | %40 | EBIT marj -1.5pp |
| 3 | [Ornek: Online penetrasyon %25'e] | Bull | FY27 | %50 | Buyume +1pp |
| 4 | [Ornek: Kur krizi (USD/TRY +%30)] | Bear | any | %25 | FX marj baskisi |
| 5 | [Ornek: M&A — kucuk rakip satinalma] | Bull | FY26-27 | %30 | Pazar payi +2pp |

KURALLAR:
- Her senaryo icin EN AZ 3 katalist tanimlanmali
- Her katalistin tahmini zamani olmali (ceyrek/yil)
- Olasilik + etki = senaryoya kantitatif destek
- Geriye dönük doğrulama: 6 ay sonra katalistler gerceklesti mi? → backtest girdisi
```

### 2A.4 Bottom-Up Gelir Dogrulamasi

Formul bazli buyume tahminini (Bolum 2.1) sirketin segment/urun yapisina gore dogrula:

```
BOTTOM-UP DOGRULAMA SABLONU:

Konsolide Hasilat Buyumesi = Σ(Segment_Payi × Segment_Buyumesi)

| Segment | FY25 Payi | Bear Buyume | Base Buyume | Bull Buyume | Kaynak |
|---------|-----------|-------------|-------------|-------------|--------|
| TR Magaza | %X | %Y | %Z | %W | Magaza sayisi × sepet buyuklugu |
| TR Online | %X | %Y | %Z | %W | Online penetrasyon trendi |
| UK | %X | %Y | %Z | %W | Magaza açilma takvimi |
| Diger | %X | %Y | %Z | %W | |
| TOPLAM | %100 | %calc | %calc | %calc | |

KONTROL: Bottom-up CAGR vs Top-down formul (Bolum 2.1) farki:
  ±2pp → Kabul edilir (yapisal tutarli)
  >2pp → Gerekce yaz: "Bottom-up %X, top-down %Y — fark nedeni: Z"
  >5pp → Red: Biri yanlis — hangisi oldugunu belirle ve duzelt
```

### 2A.5 Rehberlik vs Konsensus Fark Analizi

Yonetimin beklentileri piyasa konsensusunden onemli olcude farklilasiliyorsa, bu **asimetrik bilgi** gostergesidir:

```
REHBERLIK vs KONSENSUS KARSILASTIRMASI:

| Metrik | Yonetim | Konsensus | Fark | Yorum |
|--------|---------|-----------|------|-------|
| FY26 Buyume | %X | %Y | +/-Zpp | Yonetim daha iyimser/karamsar |
| FY26 EBIT Marji | %X | %Y | +/-Zpp | |
| CapEx | X M TL | Y M TL | | Yatirim plani farki |

YORUM KURALLARI:
- Yonetim > Konsensus + 3pp: Bull senaryoya yukari potansiyel notu ekle
  "Yonetim piyasanin gormedigi buyume sureculeri biliyor olabilir"
- Yonetim < Konsensus - 3pp: Bear senaryoya risk notu ekle
  "Yonetim muhafazakar veya icsel sorunlari onceden fiyatliyor"
- Tarihsel trend kontrol: Son 3 donemde kim daha isabetliydi?
```

---

## Bolum 2B: Sirket Rejimi Tespiti ⭐ [v2.0 — YENI]

Sirketin icinde bulundugu yasam dongusu evresi, senaryo parametrelerinin nasil calistigini koktenden degistirir.

### 2B.1 Rejim Tespit Matrisi

```
REJIM TESPITI (T1 sirasinda yapilir):

Soru 1: Son 3 yil hasilat CAGR nedir?
  >%15 → Hizli Buyume | %5-15 → Olculü Buyume | %0-5 → Olgun | <%0 → Kuculme

Soru 2: CapEx/Hasilat son 3Y trendi?
  Artıyor → Yatirim donemi | Sabit → Olgun | Azaliyor → Hasat/tasarruf

Soru 3: Yeni pazar/urun lansmanı var mi?
  Evet → Buyume donemi unsuru | Hayir → Mevcut

Soru 4: EBIT marj trendi?
  Artıyor → Olcek kazanimi | Sabit → Olgun | Azaliyor → Rekabet baskisi / yatirim

REJIMLER:
┌─────────────────────────────────────────────────────────────────┐
│ HIZLI BUYUME         │ OLCULÜ BUYUME         │ OLGUN            │
│ Hasilat CAGR >%15    │ Hasilat CAGR %5-15    │ CAGR <%5         │
│ CapEx artıyor        │ CapEx sabit/artan     │ CapEx azaliyor   │
│ Marj baskisi normal  │ Marj iyilesme         │ Marj optimize    │
│                      │                       │                  │
│ SENARYO ETKİSİ:      │ SENARYO ETKİSİ:       │ SENARYO ETKİSİ:  │
│ Bull-Base farki genis│ Dengeli aralik        │ Dar aralik       │
│ (%8-12pp)            │ (%5-8pp)              │ (%3-5pp)         │
│ Bear risk: yatirim   │ Bear risk: pazar      │ Bear risk: marj  │
│ basarısızlığı        │ yavaslama             │ erimesi          │
├─────────────────────────────────────────────────────────────────┤
│ TOPARLANMA           │ DONUSUM                                  │
│ Onceki donem kayip   │ Yeni yonetim/strateji                   │
│ EBIT negatif→pozitif │ Radikal degisim                         │
│                      │                                         │
│ SENARYO ETKİSİ:      │ SENARYO ETKİSİ:                         │
│ En genis aralik      │ Bimodal dagilim                         │
│ Bear: toparlanma     │ (ya cok iyi ya cok kotu)                │
│ basarisiz            │ Base agirlik: %40 (vs normal %50)       │
└─────────────────────────────────────────────────────────────────┘
```

### 2B.2 Rejim → Parametre Ayarlama

```
HIZLI BUYUME rejiminde:
  Buyume aralik genisligi:  Bear-Bull farki %10-15pp (genis)
  Marj aralik genisligi:    Bear-Bull farki %4-6pp
  Agirlik egilimi:          Bull'a +3pp kaydir (momentum etkisi)
  CapEx/Hasilat:            Tarihsel yerine yonetim plani agirlikli

OLGUN rejiminde:
  Buyume aralik genisligi:  Bear-Bull farki %3-5pp (dar)
  Marj aralik genisligi:    Bear-Bull farki %2-3pp
  Agirlik egilimi:          Notr (standart 25/50/25)
  CapEx/Hasilat:            Tarihsel ortalama agirlikli

TOPARLANMA rejiminde:
  Buyume aralik genisligi:  Bear-Bull farki %12-20pp (en genis)
  Marj aralik genisligi:    Bear-Bull farki %5-8pp
  Agirlik egilimi:          Bear'a +5pp kaydir (risk primi)
  CapEx/Hasilat:            Yatirim planina gore, guvenilirlik dusuk
```

---

## Bolum 2C: Senaryo Ic Tutarlilik Matrisi ⭐ [v2.0 — YENI]

> **SORUN**: Parametreleri bagimsiz turetmek "Frankenstein senaryosu" yaratabilir — mesela
> Bear senaryoda buyume dusuk ama EBIT marji artıyor (mantıksiz). Her senaryonun kendi icinde
> **tutarli bir hikayesi** olmali.

### 2C.1 Parametre Korelasyon Matrisi

```
Bear senaryoda TUTARLI bir tablo:
  ↓ Buyume → ↓ Olcek etkisi → ↓ EBIT marji (veya en iyi sabit)
  ↓ Buyume → ↓ Magaza acma → ↓ CapEx/Hasilat (veya ↑ eger magaza kapanmaz)
  ↑ Risk → ↑ WACC → ↑ SFP
  ↑ Makro belirsizlik → ↑ IS degisimi (nakit dongusu yavaslar)

Bull senaryoda TUTARLI bir tablo:
  ↑ Buyume → ↑ Olcek etkisi → ↑ EBIT marji (kaldırac)
  ↑ Buyume → ↑ Magaza acma → ↑ CapEx/Hasilat (yatirim gerekiyor)
  ↓ Risk → ↓ WACC
  ↑ Talep → ↓ IS degisimi (daha hizli tahsilat)

TUTARSIZLIK ORNEKLERI (KIRMIZI BAYRAK):
  ❌ Bear: Buyume %5 ama EBIT marji %15 (marj olcege bagli, buyume dusunce marj artamaz)
  ❌ Bull: Buyume %20 ama CapEx %3 (yuksek buyume yatirim gerektirir)
  ❌ Bear: IS -600M ama buyume %3 (dusuk buyume IS baskisi azaltir)
  ❌ Bull: Buyume %18 ama WACC Base ile ayni (yuksek buyume risk primini arttirir mi?)
```

### 2C.2 Ic Tutarlilik Kontrol Listesi

```
HER SENARYO ICIN SOR:
[ ] Buyume ile CapEx tutarli mi? (yuksek buyume → yuksek yatirim)
[ ] Buyume ile marj iliskisi mantikli mi? (olcek etkisi var mi yok mu?)
[ ] Buyume ile IS degisimi yonu dogru mu?
[ ] Makro varsayim tum parametrelere yansidi mi?
    (resesyon senaryosu → buyume ↓ VE marj ↓ VE IS ↑ VE risk ↑)
[ ] Katalist listesi parametrelerle eslesli mi?
    (Bull'da UK genisleme katalist ise, UK buyumeye segment etkisi var mi?)
[ ] Senaryo "tek cumle hikayesi" tum parametreleri kapsiyor mu?
```

---

## Bolum 3: Senaryo Agirliklari (Olasilik) — Adaptif Model

### 3.1 Temel Agirliklar

```
Varsayilan: Bear %25 | Base %50 | Bull %25
```

### 3.2 MQS (Yonetim Kalitesi) Duzeltmesi

```
MQS >= 24 (Yuksek Kalite):  Bear -5pp | Base +0 | Bull +5pp → 20/50/30
MQS 18-23 (Orta):           Standart                        → 25/50/25
MQS 12-17 (Dusuk):          Bear +5pp | Base +0 | Bull -5pp → 30/50/20
MQS < 12 (Cok Dusuk):       Bear +10pp | Base +0 | Bull -10pp → 35/50/15
```

### 3.3 Risk Matrisi Duzeltmesi (T1 Risk Etki Matrisinden)

```
En yuksek risk olasiligi >= %40:  Bear +5pp, Bull -5pp
En yuksek risk olasiligi <= %20:  Bear -5pp, Bull +5pp
```

### 3.4 Nihai Hesaplama

```
Bear_final = 25% + MQS_duzeltme + Risk_duzeltme
Bull_final = 25% - MQS_duzeltme - Risk_duzeltme
Base_final = 100% - Bear_final - Bull_final

Kisit: Bear_final >= %10, Bull_final >= %10 (minimum temsiliyet)
```

---

## Bolum 4: DCF-FM Senaryo Tutarlilik Kontrolleri

### 4.1 Ortak Parametreler (AYNI olmali)

| Parametre | FM Kaynagi | DCF Kaynagi | Uyum Kurali |
|-----------|-----------|-------------|-------------|
| Base Y1 Buyume | GelirModeli projeksiyonu | Inputs Y1 | BIREBIR esit olmali |
| Terminal g | FM terminal varsayimi | DCF Terminal Buyume | BIREBIR esit olmali |
| EBIT marji yonu | GelirTablosu marj trendi | DCF hedef EBIT | Ayni yonde olmali |
| CapEx/Hasilat | NakitAkis CapEx/Hasilat | DCF S/C'den turetilmis | %2pp icinde olmali |
| ETR | GelirTablosu vergi | DCF vergi orani | BIREBIR esit olmali |

### 4.2 Cakisma Kontrol Listesi (T3 zorunlu)

```
[ ] FM Base buyume CAGR ≈ DCF Base Y1-5 ortalama buyume (±2pp)
[ ] FM terminal buyume = DCF terminal g (birebir)
[ ] FM FAVOK marji ≈ DCF EBIT marji + D&A/Hasilat (±1pp)
[ ] FM CapEx/Hasilat ≈ 1/DCF_SC (±%1pp)
[ ] FM ETR = DCF vergi orani (birebir)
[ ] Senaryo agirliklari her iki dosyada ayni
[ ] Bear hisse degeri FM ≈ DCF Bear (±%15)
[ ] Bull hisse degeri FM ≈ DCF Bull (±%15)
```

### 4.3 Uyumsuzluk Cikarsa

1. DCF **master** kabul edilir (daha uzun ufuk, daha detayli)
2. FM parametreleri DCF'e uyumlu hale getirilir
3. Sapma notu yazilir: "FM terminal buyume X, DCF terminal buyume Y — fark nedeni: Z"

---

## Bolum 5: T1-T5 Senaryo Akisi (Cascade)

### 5.1 T1 Arastirma → Senaryo Girdileri

```
T1 Ciktilari → Senaryo Etki Alanlari:
├─ Risk Etki Matrisi → Senaryo agirliklari (Bolum 3.3)
├─ MQS Skoru → Senaryo agirliklari (Bolum 3.2) + WACC etkisi
├─ Katalizor Takvimi → Senaryo tetikleyicileri (Bull/Bear narratif)
├─ Makro Varsayimlar → Terminal buyume tavani (Bolum 2.2)
├─ Peer Analizi → Marj/buyume benchmark'lari (Bolum 2.1, 2.3)
└─ Birincil Arastirma → Buyume validasyonu (Google Trends vb.)
```

### 5.2 T2 Finansal Modelleme → Senaryo Uretimi

```
T2 Adimlari:
1. T1 ciktilarindan makro kisitlari al (Bolum 2 formulleri uygula)
2. Tarihsel veriyi normalize et (IAS 29 duzeltme, one-off cikarma)
3. Peer benchmark tablolarini olustur
4. Formul bazli Bear/Base/Bull parametreleri turet
5. FM Senaryolar tab'ina yaz (dinamik — dropdown ile aktif)
6. DCF Senaryolar tab'ina yaz (FM ile tutarli — Bolum 4 kontrolleri)
7. Tutarlilik kontrol listesini isle (Bolum 4.2)
```

### 5.3 T3 Hedef Fiyat → Senaryo Kullanimi

```
T3 Adimlari:
1. DCF'te senaryo seciciyi calistir (Bear/Base/Bull)
2. Her senaryo icin INA hedef fiyat hesapla
3. Comps ve Forward F/K ile cakistir
4. Senaryo tutarlilik kontrolu (Bolum 4.2)
5. Adaptif agirliklar uygula (Bolum 3)
6. Monte Carlo ile dogrula (agirlikli ortalama ≈ MC ortalama ±%10)
```

### 5.4 T4 Grafik → Senaryo Gorsellestirme

```
Zorunlu senaryo grafikleri:
- G_S01: Senaryo Yolculugu (Revenue path x3 senaryo + peer araligi)
- G_S02: Hedef Fiyat Aralik (Bull/Base/Bear bar chart + mevcut fiyat cizgisi)
- G_MC01: Monte Carlo histogram (zaten mevcut)
```

### 5.5 T5 Rapor → Senaryo Narratifi

```
Rapor zorunlu bolumleri:
- "Senaryo Ozeti" tablosu (1 sayfa — tum parametreler, agirliklar, hedef fiyatlar)
- "Bear Tetikleyicileri" (2-3 cumle: "Bu senaryo gerceklesir eger...")
- "Bull Katalizoru" (2-3 cumle: "Bu senaryo gerceklesir eger...")
- "Senaryo Kaynaklari" (her parametrenin turetim kaynagi referansi)
```

---

## Bolum 6: Excel Dosya Mimarisi

### 6.1 DCF Excel (Master Senaryo Deposu)

```
Inputs tab:
├─ B4: Aktif Senaryo (dropdown: Bear/Base/Bull)
├─ B5: Senaryo Kodu (IF formulu: 1/2/3)
├─ Sirket Bilgileri: Sabit (tum senaryolarda ayni)
├─ Buyume Y1-Y10: =IF(senaryo, Senaryolar!BearCol, ...)
├─ Marj: =IF(senaryo, ...)
├─ WACC: =IF(senaryo, ...)
└─ Terminal: =IF(senaryo, ...)

Senaryolar tab:
├─ BOLUM A: Senaryo Suruculer (yil bazli — 15-20 parametre)
│   └─ Kullanici bu degerleri degistirebilir
├─ BOLUM B: Senaryo Ciktilari (hesaplanan — referans)
│   └─ PV, TV, Equity Value, Hisse Basi Deger
└─ BOLUM C: Reconciliation (uc yontem uzlasma)
```

### 6.2 Finansal Model Excel [v3.1]

```
Senaryolar tab:
├─ B4: Aktif Senaryo (dropdown: Bear/Base/Bull)
├─ B5: Senaryo Kodu =IF(B4="Bear",1,IF(B4="Bull",3,2))
│
├─ SENARYO PARAMETRELERİ (Row 7-34, toplam 28 parametre):
│   ├─ Row 7-8:   YoY Buyume FY2026T / FY2027T
│   ├─ Row 9:     Terminal Buyume (g)
│   ├─ Row 10:    FAVOK Marji (hedef)
│   ├─ Row 11:    ETR (Terminal)
│   ├─ Row 12-15: Marj/CapEx FY26 (SMM, PAZ, GYG, CapEx/Hasilat)
│   ├─ Row 16-17: IS Degisimi FY26/FY27
│   ├─ Row 18:    Senaryo Olasiligi
│   ├─ Row 19-30: P&L parametreleri FY26/FY27 ciftleri
│   │   └─ Amortisman, Finansman Gid., Banka Faizi,
│   │      Parasal K/K, Diger Faal., Yat.Faal.
│   └─ Row 31-34: Marj/CapEx FY27 (SMM, PAZ, GYG, CapEx/Hasilat)
│
├─ DCF TUTARLILIK KONTROLU:
│   └─ Terminal g, ETR, CAGR, senaryo agirliklari
│
└─ Projeksiyon sayfalari IF formulleriyle senaryo seciciye bagli
```

> **Yil Bazli Marj Ayrimi:** FY26 marjlari Row 12-15, FY27 marjlari Row 31-34.
> GelirTablosu E sutunu (FY26) Row 12-15'e, F sutunu (FY27) Row 31-34'e referans verir.
> Bu yapi marjlarin yildan yila gelisimini (olcek etkisi, maliyet optimizasyonu vb.) modelleyebilmek icindir.

### 6.3 Dosyalar Arasi Tutarlilik

```
FM terminal buyume = DCF terminal g (birebir)
FM Base CAGR ≈ DCF Base Y1-5 ortalama (±2pp)
FM ETR = DCF vergi (birebir)
FM senaryo agirliklari = DCF senaryo agirliklari (birebir)
```

---

## Bolum 7: Goldman/MS Seviyesi Karsilastirma

### 7.1 Goldman Sachs Scenario Framework (Benchmark)

| Unsur | Goldman/MS Standarti | BBB v1.0 | BBB v2.0 (mevcut) |
|-------|---------------------|----------|-------------------|
| Senaryo turetimi | Makro + bottom-up + sirket | Sadece makro | Makro + sirket ozgu (2A) ✅ |
| Yonetim rehberlik entegrasyonu | Guvenilirlik iskontoyla | Yok | G skoru (2A.1) ✅ |
| Yatirim dongusu etkisi | Her parametre icin ayarlanir | Yok | Rejim tespiti (2B) ✅ |
| Katalist takvimi | Tarihli, olasılıklı | Yok | Sablonlu (2A.3) ✅ |
| Bottom-up dogrulama | Segment bazli gelir reconcile | Yok | Segment matrisi (2A.4) ✅ |
| Senaryo ic tutarliligi | Korelasyon kontrollu | Yok | Tutarlılık matrisi (2C) ✅ |
| Senaryo sayisi | 3-5 | 3 | 3 (yeterli) |
| Agirliklama | Risk-adjusted, adaptif | Sabit 25/50/25 | Adaptif (Bolum 3) ✅ |
| Audit trail | Her parametre kaynak gosterir | Yok | Formul + kaynak ✅ |
| Cross-method check | INA vs Comps vs DDM tutarlilik | Yok | Bolum 4 kontrolleri ✅ |
| Narratif | Her senaryonun "hikayesi" var | Yok | T5 sablon ✅ |
| Rehberlik vs konsensus | Fark analizi + implikasyon | Yok | 2A.5 ✅ |
| Rejim bazli aralik | Buyume/olgun/donusum farki | Yok | 2B ✅ |

### 7.2 Kalite Puanlama

```
v1.0 (onceki): ~40/100 (ad-hoc senaryolar, tutarsiz, formulsuz)
v2.0 (mevcut): ~85/100 ✅
  +15pp: Sirkete ozgu girdi katmani (guidance, yatirim dongusu)
  +10pp: Rejim tespiti ve aralik ayarlama
  +10pp: Ic tutarlilik matrisi
  +10pp: Katalist takvimi ve bottom-up dogrulama

Kalan ~%15 icin gerekli (ileri seviye):
  - Otomatik consensus API entegrasyonu (Bloomberg/FactSet)
  - Multi-factor Monte Carlo (tek parametreli degil, korelasyonlu)
  - Ceyreklik otomatik backtest pipeline'ı
  - Regime-switching modeli (Markov) ile dinamik olasilik
```

### 7.3 Kurumsal Raporlarda Senaryo Yazim Standartlari

Goldman/MS raporlarinda senaryo bolumu su unsurları icerir (v2.0 ile tumu karsilanir):

```
1. ✅ Tek cumle senaryo basligi (olculebilir sonuc icerir)
     Ornek: "Bull: UK genisleme FY27'de %8 gelir payi → %18 konsolide buyume"
     Yanlis: "Bull: Isler iyi gider"

2. ✅ Kantitatif parametre tablosu (tum parametreler sayisal)

3. ✅ Turetim gerekce paragraf (her parametre NEDEN bu deger)
     - Tarihsel veri referansi
     - Peer karsilastirma
     - Sirket rehberligi (guvenilirlik notu ile)
     - Makro kisit

4. ✅ Katalist listesi (tarihli, olasilikli)

5. ✅ Degerlenme implikasyonu (her senaryoda INA + Comps degeri)

6. ✅ Risk/getiri asimetrisi degerlendirmesi
     "Mevcut fiyattan: upside %X (Bull), downside %Y (Bear) → asimetri Bull lehine"
```

---

## Bolum 8: Senaryo Hassasiyet Siralamasi [v2.0 — YENI]

### 8.1 Tornado Analizi Mantigi

Her parametre icin "bu parametre ±1pp degisirse hedef fiyat ne kadar degisir?" sorusunu sor:

```
HASSASIYET SIRALAMASI (en etkili → en az etkili):

Tipik siralama (sirketler arasi degisir):
1. WACC (±1pp → hedef fiyat %10-15 degisir) ← en hassas
2. Terminal buyume (±0.5pp → hedef fiyat %8-12 degisir)
3. EBIT marji (±1pp → hedef fiyat %5-8 degisir)
4. Hasilat CAGR (±1pp → hedef fiyat %3-5 degisir)
5. CapEx/Hasilat (±1pp → hedef fiyat %1-3 degisir)
6. ETR (±1pp → hedef fiyat %1-2 degisir)

UYGULAMA:
- En hassas 2-3 parametreyi "kilit varsayim" olarak raporun on sayfasinda goster
- Bu parametrelerin turetim gerekcesini EN DETAYLI yaz (1.5x daha uzun)
- Sensitivity tablosunun eksenleri bu parametreler olmali
```

### 8.2 Senaryo Degeri Farki Kontrolu

```
Hedef Fiyat Aralik Kontrolu:
  Bull_Hedef / Bear_Hedef orani: ideal 1.5x - 2.5x

  <1.3x → Cok dar: Senaryolar anlamsiz, parametre farki artir
  1.3-1.5x → Dar: Olgun sirket mi? Degilse farki artir
  1.5-2.5x → Ideal: Yeterli ayrisma
  2.5-3.5x → Genis ama kabul edilir: Buyume/donusum sirketleri icin normal
  >3.5x → Cok genis: Belirsizlik cok yuksek, varsayimlari gozden gecir

FORMUL:
  Aralik_Orani = Bull_Hedef / Bear_Hedef
  Asimetri = (Bull_Hedef - Base_Hedef) / (Base_Hedef - Bear_Hedef)
    >1.2: Bull lehine asimetri → AL tavsiyesi destekler
    0.8-1.2: Simetrik → notr
    <0.8: Bear lehine asimetri → dikkatli ol
```

---

## Changelog
- v3.1 (2026-03-22): §6.2 FM Senaryolar tab detayli satir haritasi (Row 7-34, 28 parametre), yil bazli marj ayrimi dokumantasyonu (FY26 Row 12-15, FY27 Row 31-34), §0B MQS 4-band duzeltmesi (24-30/-50bp, 18-23/0, 12-17/+50bp, <12/+100bp)
- v2.0 (2026-03-22): Sirkete ozgu girdi katmani (2A — guidance, yatirim dongusu, katalist, bottom-up), rejim tespiti (2B), ic tutarlilik matrisi (2C), hassasiyet siralamasi (Bolum 8), Goldman benchmark v2
- v1.0 (2026-03-22): Ilk surum — 7 bolum, turetim formulleri, tutarlilik kontrolleri, T1-T5 akisi
