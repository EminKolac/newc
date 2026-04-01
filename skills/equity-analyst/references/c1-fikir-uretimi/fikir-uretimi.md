# Fikir Üretimi — Sistematik Yatırım Fırsatı Keşfi v2.0

> **Bu dosyanın rolü:** Ç1 için SÜREÇ dokümanı — yatırım fikirleri nasıl bulunur, nasıl düşünülür, nasıl değerlendirilir.
> **Ç1 Çıktı Şablonu (ne üretilir):** `references/c1-fikir-uretimi/c1-sablon.md`
> **Düşünce mimarisi:** SOUL.md — Topla → Sentezle → Sorgula → Güncelle

---

## Felsefe

En iyi fikirler kesişim noktalarından çıkar: kaliteli bir şirket, geçici bir sorun nedeniyle ucuzlamıştır. Ama "ucuz" tek başına yetmez — verilerin söylediği hikaye ile piyasanın fiyatladığı hikaye arasında anlamlı bir fark olması gerekir. Fark yoksa "adil fiyatlanmış" da bir sonuçtur; zorla fark aramak kadar tehlikeli bir şey yoktur.

> İlker'in Quality Value yaklaşımı: "Ucuz + Hendekli = İdeal yatırım. Ucuz + Hendeksiz = Value trap."

Sistematik tarama fırsatları sezgiden daha tutarlı yakalar — ancak tarama başlangıçtır, sonuç değil. Ekrandan geçen her aday düşünce gerektirir: "Rakamlar ne söylüyor? Birbirleriyle tutarlı mı? Tuhaf olan ne?"

---

## Ç1 Süreci: 4 Adım

```
Adım 1: TOPLA  — Screen çalıştır, veri çek (5 dk)
Adım 2: SENTEZLE — Verileri yorumla, hikayeyi bul (10 dk)
Adım 3: SORGULA — Hikayeyi yıkmaya çalış (5 dk)
Adım 4: KARAR VER — İLERLE / BEKLE / ATLA (5 dk)
```

**Toplam hedef: 20-25 dakika.** Daha kısa olabilir (veto tetiklenirse Adım 1'de biter), daha uzun olmamalı (bu Ç1, T1 değil).

---

### Adım 1: TOPLA (Screen + Veri)

#### 1A. Screen Türünü Belirle

5 screen türünden hangisi uygun? Birden fazla da geçerli olabilir.

| Screen | Ana Sorusu | Tetikleyici |
|--------|-----------|------------|
| **A. Quality Value** | Kaliteli ve ucuz mu? | İlker'in ana filtresi — default screen |
| **B. Deep Value** | Tarihsel olarak ucuz mu? | Çarpanlar sıkışmış, tez bozulmamış |
| **C. Growth** | Büyüme kaliteli mi? | Hızlı büyüyen ama pahalı görünen |
| **D. Turnaround** | Dönüş mü, value trap mı? | Düşmüş ama yapısal sorun mu geçici mi belirsiz |
| **E. Temettü** | Nakit getirisi sürdürülebilir mi? | Yüksek temettü verimi, soru: sürer mi? |

#### 1B. Veri Çek

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
- Son FY ve TTM büyüme oranları (reel)
- Sektör ve en yakın 2-3 peer'in EV/FAVÖK medyanı

#### 1C. Veto Kontrolü (Mekanik — ROIC veya FCF Negatif → DUR)

| Metrik | Veto Eşiği | Sonuç |
|--------|-----------|-------|
| ROIC | <%8 | ❌ ATLA (istisnai gerekçe yoksa) |
| FCF Marjı | Negatif (2Y+) | ❌ ATLA (turnaround screen hariç) |

Veto tetiklendiyse Adım 2'ye geçme. Çıktıda "Veto: [metrik] [değer]" yaz, dosyala, bitir.

**⚠️ Şirket Tipi İstisnaları:**
- **Banka/Finans:** ROIC ve S/C anlamsız. Veto metrikleri yerine: ROE >%12, Sermaye Yeterlilik Rasyosu >%14, Takipteki Kredi Oranı <%5. → `references/ortak/turkiye-spesifik-rehber.md` §3
- **Holding/Konglomera:** FCF ve EV/FAVÖK konsolide bazda yanıltıcı. NAV iskontosu birincil değerleme metriği. → `references/ortak/turkiye-spesifik-rehber.md` §2
- **Turnaround:** ROIC<%8 veya FCF negatif beklenen. Veto DEĞİL — ama Adım 2 sentezinde "neden turnaround?" sorusu cevaplanmalı.

---

### Adım 2: SENTEZLE (Verileri Yorumla)

> SOUL Adım 2: "10 veri noktası topladığımda durur ve sorarım: bunların hepsini birleştiren tek cümle ne?"

Veri toplamak kolay. Metrikleri renk kodlamak kolay. Zor olan: parçalardan bütünü görmek. Bu adımda 3 zorunlu soru cevaplanır:

#### Soru 1: "Bu şirketin 3 kelimelik hikayesi ne?"

Tüm metrikleri bir kenara koy. Tek cümleye indir. Örnekler:
- "Büyüdükçe nakit üretiyor" (negatif CCC + sıfır borç + pazar payı artışı)
- "Fiyatlama gücü var ama kullanmıyor" (yüksek brüt marj + düşük FAVÖK marjı)
- "Ucuz ama neden ucuz belli" (düşük çarpan + düşen ROIC + artan borç)

Tek cümleye indiremiyorsan, yeterince düşünmemişsin. Bu cümle çıktının "Sentez" bölümüne yazılacak.

#### Soru 2: "Bu sektör sermaye döngüsünün neresinde?"

> SOUL Lens: "Yüksek getiri sermaye çeker → rekabet getirileri düşürür → zayıflar ölür → hayatta kalanlar konsolide eder."

Bu sektörde:
- Sermaye akını fazında mıyız? (Yeni oyuncular geliyor, kapasite artıyor, rekabet sertleşiyor)
- Konsolidasyon fazında mıyız? (Zayıflar tasfiye olmuş, hayatta kalanlar güçlenmiş)
- Olgunluk fazında mıyız? (Büyüme yavaşlamış, nakit akışı güçlü ama yeniden yatırım fırsatı sınırlı)

Bu cevap önemli çünkü aynı şirket farklı döngü fazlarında çok farklı fiyatlanır.

#### Soru 3: "Rakamlar birbiriyle tutarlı mı? Tuhaf olan ne?"

> SOUL Adım 3a: "Parçalar arası çelişki ararım."

Metrikleri birlikte oku. Dört sinyal: marj, hacim, verimlilik, nakit akışı. Üçü aynı yönü gösteriyorsa sinyal güçlü. Tek metrik bozulurken diğerleri sağlamsa muhtemelen geçici. Dörtü birden bozuluyorsa yapısal sorun.

Anomali örnekleri:
- ROIC yüksek ama FCF düşük → yüksek capex, yatırım döneminde mi?
- Brüt marj yükseliyor ama FAVÖK marjı düşüyor → SGA şişiyor, neden?
- Gelir büyüyor ama S/C düşüyor → sermaye verimliliği kötüleşiyor, büyüme kalitesiz mi?
- F/K düşük ama EV/FAVÖK yüksek → bilanço sorunu (borç), düşük F/K yanıltıcı

**Her anomali bir hipotez tohumu.** "Neden tuhaf?" sorusu T1'in araştıracağı ilk şey olabilir.

---

### Adım 3: SORGULA (Hikayeyi Yıkmaya Çalış)

> SOUL Adım 3: "Sentez, bir hikaye inşa etmektir. Sorgulama, inşa ettiğin hikayeyi yıkmaya çalışmaktır."

Adım 2'de bir hikaye kurdun. Şimdi onu yıkmaya çalış:

#### 3A. Hızlı Ters İNA (Piyasa Ne Fiyatlıyor?)

> SOUL: "Ters İNA benim aracım. Piyasanın zımni varsayımlarını çözmek değerli bir egzersiz."

Ç1 düzeyinde tam ters İNA gerekmez. Ama piyasanın ne fiyatladığını anlamak gerekir:

**Gordon Growth Zımni Büyüme Hesabı:**
```
Zımni büyüme (g) = WACC - (NOPAT / EV)
                  = WACC - (1 / (EV/NOPAT))

Basitleştirilmiş (FAVÖK bazlı yaklaşık — D&A ≈ CapEx varsayar):
g ≈ WACC - (1 / (EV/FAVÖK × (1 - t)))

Burada:
- WACC: Sektör ortalama WACC (Damodaran sektör verisi veya genel tahmin)
- EV/FAVÖK: Mevcut çarpan
- t: Efektif vergi oranı
```

**Pratik uygulama:**
1. Mevcut EV/FAVÖK'ten zımni büyümeyi hesapla
2. Sektör medyan EV/FAVÖK'ten sektörün zımni büyümesini hesapla
3. Farkı yorumla: piyasa bu şirkete sektörden [daha yüksek/düşük] büyüme fiyatlıyor
4. Bu varsayım mantıklı mı? 1-2 cümle yorum

**⚠️ Sınırlama:** D&A ≈ CapEx varsayımı olgunlaşmış şirketlerde tutarlıdır; yüksek büyüme veya ağır yatırım döneminde (CapEx >> D&A) zımni büyüme düşük çıkar. Bu durumda sonucu "yatırım döneminde sapma beklenir" notuyla yorumla.

**Alternatif (veri yetersizse):** EV/FAVÖK karşılaştırması yeterli:
```
Şirket EV/FAVÖK: 12x | Sektör medyan: 8x | Fark: +%50 prim
→ Piyasa bu şirkete sektörden belirgin büyüme veya kalite primi veriyor.
→ Haklı mı? [Yorum]
```

**Kritik:** Sonuç "piyasa haklı" da olabilir. "Adil fiyatlanmış" da bir sonuç — zorla fark arama.

#### 3B. Yıkım Testi

> SOUL Adım 3c: "Bu hikayeyi yıkan en güçlü argüman ne?"

Tek soru sor: "6 ay sonra bu hisse %30 düştü. En muhtemel neden ne?"

Bu sorunun cevabı çıktının "Kill Risk" bölümüne yazılacak.

#### 3C. İkinci Derece Etki Kontrolü (İsteğe Bağlı — Tematik Taramada Zorunlu)

> SOUL Lens: "Birinci seviye düşünce: faiz düştü, bu şirket için iyi. İkinci seviye: herkes bunu biliyor, fiyatlanmış mı?"

Tematik taramada zorunlu: tema → birinci derece faydalanan → ikinci derece faydalanan → "priced in" kontrolü.

---

### Adım 4: KARAR VER

Adım 1-3 tamamlandı. Şimdi yapılandırılmış karar:

#### Karar Matrisi

**İLERLE 🟢 (EN AZ 3/4 SAĞLANMALI):**
- [ ] Ön tez hipotezi falsifiable ve spesifik (Adım 2'den)
- [ ] Quality Value matrisi: Ucuz+Hendekli VEYA Pahalı+Hendekli (izle listesine al)
- [ ] Sentez tutarlı: 3 soru cevapları birbiriyle çelişmiyor
- [ ] Ters İNA: piyasa varsayımında sorgulanabilir bir nokta var VEYA piyasa haklı ama kalite yeterince güçlü

**ATLA 🔴 (HERHANGİ BİRİ YETERLİ):**
- [ ] Veto metriği kırmızı (ROIC<%8 veya FCF negatif 2Y+)
- [ ] Sentez: "3 kelimelik hikaye yok" — şirketin ne yaptığını tanımlayamıyorum
- [ ] Ters İNA: piyasa haklı fiyatlamış VE kalite yetersiz (hendeksiz)
- [ ] Yıkım testi: yıkım senaryosu çok yakın ve muhtemel

**BEKLE 🟡:**
- [ ] Hipotez var ama katalizör yakın değil
- [ ] Veri yetersiz — çeyreklik sonuçları veya sektör verisini bekle
- [ ] Sermaye döngüsü: sektör henüz doğru fazda değil ama izlenmeye değer

---

## Screen Filtre Detayları

### A. Quality Value Screen (İlker'in Ana Filtresi)

| Filtre | Eşik | Neden |
|--------|------|-------|
| ROIC | >%15 (minimum), >%25 ideal | Sermaye verimliliği — moat proxy |
| Brüt Marj | >%30, >%50 ideal | Fiyatlama gücü |
| FCF Marjı | >%10 | Nakit yaratma kapasitesi |
| P/FCF | <20x | Makul değerleme |
| Net Borç/FAVÖK | <2x | Sağlıklı bilanço |
| S/C (Sales/Capital) | >1.50x | Sermaye verimliliği |

### B. Deep Value Screen

| Filtre | Eşik | Neden |
|--------|------|-------|
| P/E | Sektör medyanının altında | Göreceli ucuzluk |
| EV/EBITDA | 5Y ortalamasının altında | Tarihsel iskonto |
| FCF Yield | >%5 | Nakit getirisi |
| P/BV | <1.5x | Varlık iskontosu |
| İçeriden alım (3 ay) | Var | Yönetim güveni |

### C. Growth Screen

| Filtre | Eşik | Neden |
|--------|------|-------|
| Gelir büyümesi (YoY) | >%15 reel | Güçlü büyüme |
| FAVÖK büyümesi (YoY) | >%20 reel | Kârlı büyüme |
| Büyüme ivmesi | Artan (acceleration) | Momentum |
| Marj genişleme | Expanding | Operating leverage |
| ROIC | >%15 | Kaliteli büyüme (büyüme + verimlilik) |

### D. Turnaround / Special Situation Screen

| Filtre | Eşik | Neden |
|--------|------|-------|
| Gelir düşüşü → toparlanma | Son 2 çeyrekte pozitife döndü | Dip noktası |
| Yönetim değişikliği | Son 12 ay | Yeni strateji |
| Spin-off / bölünme | Son 12 ay | Gizli değer açığa çıkma |
| Aktivist yatırımcı girişi | Son 12 ay | Değişim katalizörü |
| Sektör konsolidasyonu | Aktif M&A döngüsü | Satın alma primi |

### E. Temettü / Income Screen

| Filtre | Eşik | Neden |
|--------|------|-------|
| Temettü verimi | >%3, >%5 cazip | Nakit getirisi |
| Temettü/FCF | <%70 | Sürdürülebilirlik |
| Temettü büyümesi (3Y) | Artan | İyileşme trendi |
| Net Borç/FAVÖK | <3x | Temettü güvenliği |

---

## Tematik Tarama (Thematic Sweep)

Belirli bir tema etrafında yatırım fırsatı araştırma. Adım 3C (İkinci Derece Etki Kontrolü) tematik taramada ZORUNLU.

### Adımlar
1. **Tezi tanımla** — "AI altyapı harcamaları 2027'ye kadar hızlanacak"
2. **Değer zincirini haritala** — birincil, ikincil, üçüncü derecede faydalananlar
3. **Pure-play vs diversified** — saf tema maruziyeti mi, yoksa konglomera mı?
4. **"Priced in" kontrolü** — piyasa bu temayı çoktan fiyatladı mı? (İkinci derece etki zorunlu)
5. **İkinci derece faydalananları ara** — konsensüsün henüz bağlamadığı isimleri bul

### Tema Örnekleri (BBB Bağlamı)
- Türkiye dezenflasyonu → Bankalar, tüketim, inşaat
- Avrupa enerji dönüşümü → Yenilenebilir enerji üreticileri
- AI altyapısı → Veri merkezi, soğutma, enerji
- Obezite tedavisi (GLP-1) → NVO, LLY, medikal cihaz
- Premiumlaşma (EM tüketicisi) → Luxury, premium gıda

---

## Tarama Sıklığı ve Takip

- **Aylık:** Quality Value screen + Deep Value screen (BIST)
- **Çeyreklik:** Growth screen + Temettü screen
- **Tematik:** Yeni tema ortaya çıktığında
- **Hit rate takibi:** Hangi screen'ler en iyi fikirler üretir? Zaman içinde kalibrasyon

---

## BIST Veri Kaynakları

| Screen Adımı | Araç |
|-------------|------|
| Finansal filtreler (ROIC, marj, vs.) | BBB Finans: `bbb_financials.py {TICKER} --dcf --json` |
| Çarpan karşılaştırma | BBB Finans + Yahoo Finance |
| İçeriden alım/satım | KAP bildirimleri |
| Sektör listesi | BIST sektör sınıflandırması |
| Sektör WACC (ters İNA için) | Damodaran: `pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/wacc.html` veya `bbb-dcf/references/industry_data.md` |

---

## Uyarılar

- Tarama başlangıçtır, sonuç değil — her adayın düşünce süreci (Adım 2-3) atlanamaz
- Kalabalık pozisyonlardan kaçın — herkes aynı fikirdeyse, fırsat muhtemelen gitmiştir
- Contrarian fikirler katalizör gerektirir — erken olmak ama katalizörsüz olmak yanlış olmakla aynıdır
- "Adil fiyatlanmış" da bir sonuçtur — zorla fark arama, zorla contrarian olma
- Short fikirler daha yüksek conviction ister — zamanlama zor, risk asimetrik

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-18 | v1.0 — İlk sürüm. 5 screen türü, tematik tarama. |
| 2026-03-25 | v2.0 — SOUL.md düşünce mimarisi entegrasyonu. 4 adımlı süreç (Topla→Sentezle→Sorgula→Karar). Mini Sentez (3 soru + sermaye döngüsü lens'i). Hızlı Ters İNA (Gordon Growth zımni büyüme). Yıkım testi. Yapılandırılmış karar matrisi (İLERLE/BEKLE/ATLA). |
| 2026-03-25 | v2.1 — Batch screen altyapı referansı eklendi. bbb-terminal-next derived_metrics entegrasyonu. Screen metrik key haritası. Ç1 tracking zorunluluğu. |

---

## Batch Screen Altyapısı (bbb-terminal-next Entegrasyonu)

> Bu bölüm Adım 1A'daki screen'lerin TOPLU çalıştırılması için altyapı referansıdır.
> Tekil ticker analizi (mevcut bbb-finans) hâlâ çalışır — batch, ek katmandır.

### Veri Kaynağı
- **DB:** `~/Documents/Claude Code - Ortak Tema Çalışma Alanı/bbb-terminal-next/backend/bbb_cache/financials.db`
- **Kapsam:** 570 BIST ticker, İş Yatırım API cache
- **Metrik motoru:** `backend/core/derived_metrics.py` — 58 benzersiz türetilmiş metrik (TTM/yıllık/çeyreklik)
- **Scorecard:** `backend/bbb_scorecard.py` (5 boyut /25) + `backend/bbb_advanced_scorecard.py` (quantile)
- **Fiyat:** Çarpanlar canlı fiyat gerektirir → `bbb-finans bbb_financials.py --price` ile batch çekim

### Screen Türü → Kritik Metrik Haritası

**Quality Value (İlker'in ana filtresi):**
```
Birincil (6): bs_roic, is_brut_marj, bs_fcf_marj, bs_ev_ebitda, bs_net_borc_ebitda, bs_sc
İkincil (4): is_faal_marj, bs_pe, cf_quality_earnings, bs_ccc
Eşikler: ROIC > %30 (WACC), Brüt Marj > %30, S/C > 1.50, Net Borç/FAVÖK < 2x
```

**Growth Screen:**
```
Birincil (5): is_revenue_cagr_3y, is_ebitda_cagr_3y, is_faal_marj, bs_roic, cf_reinvestment_rate
İkincil (3): cf_implied_growth, bs_ev_ebitda, bs_sc
Eşikler: Gelir CAGR > %15 reel, FAVÖK CAGR > %20 reel, ROIC > %15
```

**Deep Value Screen:**
```
Birincil (5): bs_pe, bs_ev_ebitda, bs_pb, bs_fcf_marj, bs_net_borc_ebitda
İkincil (3): bs_altman_z, bs_roic, cf_quality_earnings
Eşikler: F/K < sektör medyanı, FD/FAVÖK < 5Y ort., FCF Yield > %5
```

### Batch Screen Prosedürü (Manuel Tetik)

İlker "screen çalıştır" dediğinde:
1. financials.db'den 570 ticker cache veri çek (API çağrısı yok, hızlı)
2. Güncel fiyat için bbb-finans'tan watchlist batch çekim (çarpanlar fiyat bağımlı)
3. Screen filtresi uygula → eşikleri geçenleri sırala
4. Top 15-20 şirket → Ç1 adayı olarak sun (ticker + skor + kritik metrikler)
5. İlker seçim yapar → seçilen ticker'lar için Ç1 Adım 1-4 çalıştırılır

### ⚠️ Bilinen Sınırlamalar
- Cache güncelliği: financials.db son refresh tarihi kontrol edilmeli (21 Mart 2026 itibariyle 570 ticker)
- Fiyat bağımlılık: FD/FAVÖK, F/K, PD/DD gibi çarpanlar cache'deki fiyatla hesaplanamaz, canlı fiyat gerekir
- IAS 29: Cache İş Yatırım (nominal) verisi tutuyor, IAS 29 düzeltmeli değil
- Banka/Sigorta: ROIC, S/C, FCF metrikleri uygulanamaz — sektör tespiti otomatik (`_sector_type`)
- financials.db refresh mekanizması: `backend/scripts/sync_bist.py` veya `daily-refresh.sh` ile yapılıyor olabilir, prosedür doğrulanmalı
