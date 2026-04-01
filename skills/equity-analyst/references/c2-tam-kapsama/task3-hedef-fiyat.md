# Hedef Fiyat Derivasyonu — Üç Yöntem Reconciliation Rehberi

> Hedef fiyat tek bir modelin çıktısı değil, birden fazla yöntemin sentezlenir.
> Curtis Jensen: "DCF is like Hubble telescope – turn a fraction of an inch & you're in a different galaxy."
> Bu dosya: İNA + Karşılaştırmalı Değerleme + İleriye Dönük F/K → Tek Hedef Fiyat

---

## Bölüm 0: Temel Metodolojik Referanslar [v2.1]

> Hedef fiyat derivasyonu öncesi aşağıdaki temel kurallar kontrol edilmelidir.
> Bu referanslar ihlal edildiğinde hedef fiyat **yapısal olarak hatalı** olur.

| Konu | Referans Dosya | Bölüm | T3'te Ne Zaman Geçerli |
|------|---------------|-------|----------------------|
| **Reel vs Nominal baz** | senaryo-metodoloji.md | §0A | İNA hedef fiyat ile Forward F/K hedef fiyat AYNI bazda mı? Reel İNA + nominal F/K → **UYUMSUZ** |
| **WACC bileşenleri** | senaryo-metodoloji.md | §0B | İNA WACC'ın Ke/Kd bileşenleri doğru kaynaklardan mı? MQS primi uygulandı mı? |
| **Temettü/Payout** | senaryo-metodoloji.md | §0C | Terminal value formülünde payout = 1-g/ROC mi? Hardcoded payout → **HATA** |
| **Kazanç kalitesi** | senaryo-metodoloji.md | §0D | Forward HBK'da parasal kazanç/kayıp çıkarıldı mı? DSO trendi anormal mi? |
| **EV FX harmonizasyonu** | karsilastirmali-degerleme.md | §6A | Comps hedef fiyat FX karışıklığı var mı? Peer EV/EBITDA yerel para biriminde mi? |
| **Forward HBK parametrik** | bu dosya | §1 Yöntem 2 | Forward HBK ağırlıkları rapor ayına göre parametrik mi? Hardcoded 9/12 → **HATA** |

> **Sanity check:** 3 yöntemin hedef fiyatları arasında >%30 fark varsa, Bölüm 0 ihlali araştır (en yaygın neden: baz uyumsuzluğu).

---

## Felsefe

Hedef fiyat üretmek, değerlemenin en kritik ve en tartışmalı adımıdır. Üç temel ilke:

1. **Tekil model tehlikelidir.** İNA tek başına varsayım hassasiyetine aşırı bağımlıdır. Comps tek başına piyasanın bugünkü duyarlılığını yansıtır. İkisi birlikte kullanılmalı.
2. **Reconciliation zorunludur.** İNA ve Comps farklı değerler verdiğinde, farkın nedenini açıklamak hedef fiyattan daha değerlidir.
3. **Hedef fiyat bir aralıktır, nokta değildir.** Nokta tahmini senaryo ağırlıklı beklenen değerden türetilir; ancak aralık her zaman raporlanır.

---

## 1. Üç Değerleme Yöntemi

### 1A. İNA (İndirgenmiş Nakit Akışı) — Mutlak Değer

**Kaynak:** bbb-dcf skill (Faz 2 çıktısı)
**Ne verir:** Şirketin iç değerine dayalı hisse başı değer

```
İNA Hedef Fiyat = (Firma Değeri − Net Borç + Nakit) / Pay Sayısı
```

**Senaryo bazlı İNA:**

| Senaryo | Olasılık | Hisse Başı Değer |
|---------|----------|------------------|
| Kötümser| %25      | X TL             |
| Baz     | %50      | Y TL             |
| İyimser | %25      | Z TL             |
| **Ağırlıklı Beklenen Değer** | | **(0.25×X + 0.50×Y + 0.25×Z)** |

**İNA'nın güçlü olduğu durumlar:**
- Öngörülebilir nakit akışı olan şirketler
- Büyüme profili net olan şirketler
- Karşılaştırılabilir peer'ı az olan şirketler (niş iş modeli)

**İNA'nın zayıf olduğu durumlar:**
- Erken aşama / zarar eden şirketler (negatif FCF)
- Döngüsel sektörler (terminal varsayım riskli)
- IAS 29 etkisiyle nakit akışları bozuk görünen Türk şirketleri

### 1B. Karşılaştırmalı Değerleme (Comps) — Göreceli Değer

**Kaynak:** karsilastirmali-degerleme.md
**Ne verir:** Piyasanın benzer şirketlere biçtiği değere dayalı hedef

```
Comps Hedef Fiyat = Seçilen Çarpan × Şirketin Metriği / Pay Sayısı
```

**Birincil Çarpanlar (Sektöre Göre):**

| Sektör | Birincil Çarpan | İkincil Çarpan |
|--------|----------------|----------------|
| Sanayi / Üretim | FD/FAVÖK | F/K |
| Bankacılık | F/DD | F/K |
| Teknoloji (kârlı) | FD/FAVÖK | FD/Hasılat |
| Teknoloji (zararda) | FD/Hasılat | PS/FCF (ileriye dönük) |
| Perakende | FD/FAVÖK | FD/FVÖK |
| Gayrimenkul | F/NAV | F/FFO |
| Holding | NAV İskontosu | SOTP |

**Comps Hedef Fiyat Hesaplama Adımları:**

1. Peer grubu medyanını hesapla (karsilastirmali-degerleme.md'deki 5-10 kuralına göre)
2. Şirketin hak ettiği primi/iskontoyu belirle:
   - ROIC > peer medyanı → prim hak eder
   - Büyüme < peer medyanı → iskonto uygulanır
   - Ülke riski (Türkiye) → sistematik iskonto
3. Düzeltilmiş çarpanı şirketin forward metriğine uygula

```
Örnek:
Peer FD/FAVÖK medyanı = 14.8x
TBORG ROIC (%26) > Peer medyanı (%15) → prim: +1.5x
Türkiye iskontosu → -%2.0x
Düzeltilmiş çarpan = 14.8 + 1.5 − 2.0 = 14.3x
TBORG Forward FAVÖK = 8.500 mn TL
Comps Firma Değeri = 14.3 × 8.500 = 121.550 mn TL
Comps Hisse Değeri = (121.550 − Net Borç + Nakit) / Pay Sayısı
```

### 1C. İleriye Dönük F/K — Piyasa Duyarlılığı Yansıması

**Bu BBB'ye özel ek yöntemdir.** Kurum raporlarında (İş Yatırım, Ak Yatırım) sıkça kullanılan yaklaşım.

**Forward F/K nedir?**
Mevcut hisse fiyatının, gelecek 12 ay beklenen hisse başı kazanca (HBK) bölümü. BBB'de bunu tersten kullanıyoruz: hedef F/K × forward HBK = hedef fiyat.

```
Forward F/K Hedef Fiyat = Hedef F/K Çarpanı × Forward HBK
```

**Hedef F/K nasıl belirlenir?**

| Yöntem | Açıklama | Kullanım |
|--------|----------|----------|
| Tarihsel F/K bandı | Şirketin son 5Y F/K medyanı | En sık kullanılan |
| Peer F/K medyanı | Emsal şirketlerin forward F/K'sı | Cross-check |
| PEG oranı türetmesi | F/K = PEG × Beklenen büyüme | Büyüme odaklı |
| Sektör ortalaması | BIST sektör F/K'sı | Yeni kapsanan şirketler |

**Forward HBK nasıl hesaplanır?**

```
# Yöntem 1: TTM + büyüme (basit)
Forward HBK = TTM HBK × (1 + beklenen büyüme %)

# Yöntem 2: Kümülatif ağırlıklı (kurum standardı) [v2.1 — parametrik]
# Yılın kalan kısmı (current FY) + gelecek yılın tamamlanmış kısmı
# M = raporun yazıldığı ay (1-12), FY_END = şirketin mali yıl sonu ayı
#
# GENEL FORMÜL:
#   Kalan_Ay = (FY_END - M) mod 12   (mali yıl sonuna kalan ay)
#   Gecen_Ay = 12 - Kalan_Ay
#   Forward HBK = (Kalan_Ay/12 × Current_FY_HBK) + (Gecen_Ay/12 × Next_FY_HBK)
#
# Örnek 1: Mart 2026 raporu, Aralık mali yıl sonu (M=3, FY_END=12)
#   Kalan_Ay = 9, Gecen_Ay = 3
#   Forward HBK = (9/12 × FY2026T HBK) + (3/12 × FY2027T HBK)
#
# Örnek 2: Temmuz 2026 raporu, Aralık mali yıl sonu (M=7, FY_END=12)
#   Kalan_Ay = 5, Gecen_Ay = 7
#   Forward HBK = (5/12 × FY2026T HBK) + (7/12 × FY2027T HBK)
#
# Örnek 3: Ekim 2026 raporu, Mart mali yıl sonu (M=10, FY_END=3)
#   Kalan_Ay = (3-10) mod 12 = 5, Gecen_Ay = 7
#   Forward HBK = (5/12 × FY2027T HBK) + (7/12 × FY2028T HBK)
#
# NOT: M ve FY_END değerleri her raporda güncellenir — hardcode YASAK.

# Yöntem 3: İş Yatırım tarzı "ileriye taşıma" (forward roll)
# İNA modelinden türetilen HBK, 3 aylık ileriye taşınır
Forward HBK = İNA Hisse Değeri × Ke × (3/12) + İNA Hisse Değeri
# → Bu aslında "zaman değeri" taşıması — bugünkü İNA değerini 3 ay ileriye getirme
```

**⚠️ IAS 29 Uyarısı — BIST Forward F/K Güvenilirliği**

IAS 29 muhasebesi net kârı çarpıtır (parasal kazanç/kayıp). Forward F/K hesaplanırken:
1. Parasal kazanç/kayıp çıkarılmış (düzeltilmiş) net kâr kullanılmalı
2. Düzeltilmemiş F/K yanıltıcıdır — "ucuz" görünen hisse aslında parasal kazanç şişirmesinden dolayı düşük F/K'da olabilir
3. Peer karşılaştırmada: IAS 29 olmayan ülke peer'larıyla direkt F/K karşılaştırması → **YASAK** (düzeltme farkı açıklanmadan)

**Forward F/K'nın güçlü olduğu durumlar:**
- Kârlı, istikrarlı şirketler (F/K anlamlı)
- BIST'te yaygın kullanılması → piyasa F/K bazında fiyatlıyor
- Kurum raporlarıyla doğrudan karşılaştırma imkânı

**Forward F/K'nın zayıf olduğu durumlar:**
- Zararda olan şirketler (F/K negatif veya anlamsız)
- IAS 29 etkisi güçlü şirketler (düzeltme yapılmazsa)
- Döngüsel sektörler (peak earnings'te düşük F/K → value trap)

---

## 2. Reconciliation (Uzlaştırma) Süreci

### Adım 1: Üç Yöntemin Sonuçlarını Yan Yana Koy

```
Tablo: Değerleme Özeti

| Yöntem | Hisse Başı Değer | Ağırlık | Ağırlıklı Katkı |
|--------|------------------|---------|------------------|
| İNA (Temel Senaryo) | X TL | %W₁ | X × W₁ |
| Comps (FD/FAVÖK medyan) | Y TL | %W₂ | Y × W₂ |
| İleriye Dönük F/K | Z TL | %W₃ | Z × W₃ |
| **Hedef Fiyat** | | **%100** | **Σ** |
```

### Adım 2: Ağırlık Belirleme

Ağırlıklar sabit değildir — şirket ve durum bağımlıdır.

**Standart Ağırlıklar (Başlangıç Noktası):**

| Durum | İNA | Comps | Forward F/K |
|-------|-----|-------|-------------|
| Stabil, kârlı, iyi peer grubu | %40 | %35 | %25 |
| Stabil, az peer | %55 | %20 | %25 |
| Yüksek büyüme, belirsiz profil | %50 | %30 | %20 |
| Döngüsel sektör | %35 | %35 | %30 |
| Zararda / erken aşama | %60 | %30 | %10 |
| Holding / SOTP | %20 | %10 | %10 (+ SOTP %60) |

**Ağırlık Ayarlama Kuralları:**

| Durum | Ayarlama |
|-------|----------|
| İNA projeksiyonlarına yüksek güven | İNA ağırlığı ↑ |
| Peer grubu çok uyumlu (5+ benzer şirket) | Comps ağırlığı ↑ |
| Şirketin tarihsel F/K bandı istikrarlı | Forward F/K ağırlığı ↑ |
| IAS 29 etkisi güçlü | Forward F/K ağırlığı ↓, İNA ağırlığı ↑ |
| M&A olasılığı yüksek | Emsal işlem ağırlığı ↑ (varsa 4. yöntem) |

### Adım 3: Fark Analizi (Reconciliation'ın Kalbi)

**İNA ve Comps arasındaki fark %20'den büyükse → ZORUNLU açıklama.**

Olası fark nedenleri:

| Fark Yönü | Olası Neden | Aksiyon |
|-----------|-------------|---------|
| İNA >> Comps | İNA varsayımları çok iyimser | Büyüme/marj varsayımlarını sorgula |
| İNA >> Comps | Piyasa şirketi değersizliyor | Tez bu: katalizör ne? |
| İNA << Comps | İNA AOSM çok yüksek | CRP/Beta girdilerini kontrol et |
| İNA << Comps | Peer grubu şişirilmiş çarpanlarda | Peer'ları döngüsellik için kontrol et |
| F/K >> İNA | Kâr geri dönmezse F/K yanıltıcı | Kâr kalitesini kontrol et (one-off'lar) |
| F/K << İNA | IAS 29 kâr düşürücü etki | Düzeltilmiş HBK kullan |

**Fark büyüklüğüne göre zorunlu aksiyonlar:**

| Fark (|İNA − Comps| / Comps) | Seviye | Zorunlu Aksiyon |
|------------------------------|--------|-----------------|
| <%10 | Normal | Kısa açıklama yeterli |
| %10-20 | Dikkat | 1-2 paragraf fark analizi |
| %20-30 | Uyarı | Yapısal açıklama zorunlu — aşağıdaki şablonu doldur |
| >%30 | 🔴 Kritik | Detaylı 5-maddeli açıklama + varsayım revizyonu değerlendirmesi |

**>%30 Fark İçin Zorunlu Şablon:**

```
## İNA-Comps Fark Analizi (Fark: %X)

1. WACC Etkisi: İNA'nın WACC'ı (%Y) peer ortalamasından Z pp [yüksek/düşük].
   → WACC'ı peer ortalamasıyla eşleştirsek İNA değeri: [W TL] olurdu.

2. Büyüme Etkisi: İNA'nın 5Y CAGR'ı (%A), peer büyümesinden [yüksek/düşük].
   → Peer büyümesini kullansak İNA değeri: [B TL] olurdu.

3. Marj Etkisi: İNA'nın terminal marjı (%C), peer medyanından [yüksek/düşük].
   → Peer marjını kullansak İNA değeri: [D TL] olurdu.

4. Çarpan Seçimi: Comps'ta kullanılan çarpan ([FD/FAVÖK]) peer grubu
   için [uygun/tartışmalı] çünkü [gerekçe].

5. Sonuç: Farkın %X'i [WACC/büyüme/marj] farklılığından kaynaklanıyor.
   → Varsayım revizyonu [gerekli/gereksiz] çünkü [gerekçe].
```

**Reconciliation paragraf şablonu:**

> "İNA modelimiz hisse başı [X] TL, karşılaştırmalı değerleme [Y] TL, ileriye dönük F/K ise [Z] TL ima etmektedir. İNA ile Comps arasındaki %[N] farkın temel nedeni [açıklama]. İNA ağırlığını %[W₁] olarak belirlememizin gerekçesi [varsayımlara güven seviyesi]. Sonuç olarak, ağırlıklı hedef fiyatımız [HF] TL'dir."

### Adım 4: Duyarlılık Kontrolü

Hedef fiyat, anahtar varsayımlara ne kadar duyarlı?

```
Tablo: Hedef Fiyat Duyarlılık Matrisi

               | AOSM %11 | AOSM %12 | AOSM %13 | AOSM %14 |
|--------------|----------|----------|----------|----------|
| Büyüme %2    | A TL     | B TL     | C TL     | D TL     |
| Büyüme %3    | E TL     | F TL     | **G TL** | H TL     |
| Büyüme %4    | I TL     | J TL     | K TL     | L TL     |
| Büyüme %5    | M TL     | N TL     | O TL     | P TL     |

** = Temel senaryo
```

### Adım 5: Değerleme Aralık Grafiği (Football Field)

Zorunlu görselleştirme. `grafik-uret.py: football_field_grafigi()` kullanılır.

```
[AYIRIK GRAFİĞİ: Yatay çubuklar]

İNA (Ayı-Boğa)          |████████████████████|  180 ——— 275 TL
FD/FAVÖK Comps           |████████████|          190 ——— 245 TL
İleriye Dönük F/K        |██████████████|        170 ——— 255 TL
52 Hafta Fiyat Aralığı   |████████|              120 ——— 185 TL
                         ─────────────────────────────────────
                         100  120  140  160  180  200  220  240  260  280
                                              ▲
                                         Mevcut: 155 TL
                                                   ▲
                                              Hedef: 221 TL
```

**Aralık grafiği kuralları:**
- Minimum 4 çubuk: İNA aralığı, Comps aralığı, Forward F/K aralığı, 52 hafta fiyat aralığı
- Varsa: Emsal işlem aralığı, kurum konsensüsü aralığı
- Mevcut fiyat ve hedef fiyat işaretleri zorunlu
- Çubuklar Ayı→Boğa aralığını gösterir

---

## 3. İleri Taşıma (Forward Roll) Kuralı

Kurum raporlarının standart pratiği: İNA modelini analiz tarihinden ileriye taşıma.

**Ne zaman uygulanır?**
- Rapor tarihi ile hedef fiyat ufku arasında 3+ ay varsa
- İNA modeli geçmiş bir tarih baz alıyorsa (örn: FY sonu modeli, Mart'ta yayınlama)

**Nasıl uygulanır?**

```
İleri Taşınmış Değer = İNA Hisse Değeri × (1 + Ke)^(ay/12)

# Örnek: İNA değeri 210 TL, Ke = %18 (TL bazlı), 3 ay ileri taşıma
İleri Taşınmış = 210 × (1.18)^(3/12) = 210 × 1.042 ≈ 219 TL
```

**⚠️ Dikkat:** İleri taşıma sadece zaman değeri taşımasıdır — yeni bilgi içermez. Raporda açıkça belirtilmeli: "3 aylık ileriye taşıma uygulanmıştır."

---

## 4. BBB'ye Özgü Kurallar

### 4A. IAS 29 Şirketleri

| Kural | Uygulama |
|-------|----------|
| Comps'ta spot kurla çevirme | YASAK — yıllık ort. kur veya şirketin kendi USD raporlaması |
| Forward F/K'da düzeltilmemiş HBK | YASAK — parasal kazanç/kayıp çıkarılmış HBK |
| İNA TL ve İNA USD cross-check | ZORUNLU — Fisher parity kontrolü |

### 4B. Emsal İşlemler (Precedent Transactions)

**Genel ilke:** BIST'te M&A verisi sınırlıdır, ancak mevcut olduğunda değerli bir kontrol noktasıdır. Trading comps'un üzerine kontrol primi ekleyerek "bu şirketi satın almak isteseydiniz ne öderdiniz?" sorusunu cevaplar.

**Ne zaman uygulanır:**
- Son 5 yıl içinde AYNI SEKTÖRDE en az 2-3 kapanmış M&A işlemi varsa
- Şirketin kendisi M&A hedefi olma potansiyeli taşıyorsa
- Konsolidasyon trendi olan sektörlerde (perakende, bankacılık, enerji)

**Ne zaman uygulanmaz:**
- Sektörde 5 yıl içinde anlamlı M&A yoksa → bu yöntemi ATLAMA, 1 cümleyle geçiştir
- Ağırlık hiçbir zaman birincil olamaz — maks %10-15

**Veri kaynakları (BIST için):**
1. KAP önemli işlem bildirimleri
2. Rekabet Kurumu kararları (rekabet.gov.tr)
3. Basın açıklamaları ve haberler
4. SPK izahnameleri (halka arz öncesi satışlar)

**Emsal İşlem Tablosu Formatı:**
```
Tarih    Hedef         Alıcı         İşlem         FD/Has   FD/FAVÖK  Prim   Gerekçe
                                     Değeri(mn TL)
[AA/YY]  [Şirket A]   [Alıcı A]    X              X,Xx     XX,Xx     %X     [Konsolidasyon]
[AA/YY]  [Şirket B]   [Alıcı B]    X              X,Xx     XX,Xx     %X     [Stratejik]
[AA/YY]  [Şirket C]   [Alıcı C]    X              X,Xx     XX,Xx     %X     [PE çıkışı]

Medyan                                              X,Xx     XX,Xx     %X

Kaynak: KAP, Rekabet Kurumu, basın açıklamaları.
```

**Kontrol primi analizi:**
- Kontrol primi = (İşlem fiyatı - etkilenmemiş fiyat) / etkilenmemiş fiyat
- Etkilenmemiş fiyat = Açıklamadan 1-2 gün önceki kapanış
- BIST'te tipik kontrol primi: %20-40
- Stratejik alıcı genellikle finansal alıcıdan daha yüksek prim öder

**Uygulanışı:**
```
Hedef Şirket TTM FAVÖK = X mn TL
Emsal Medyan FD/FAVÖK (TTM) = XX,Xx

İma Edilen FD (Emsal) = X mn TL × XX,Xx = Y mn TL

Not: Emsal çarpanlar trading comps'tan genellikle %15-30 yüksektir
(kontrol primi + sinerji beklentisi nedeniyle).
```

**Reconciliation'da ağırlık:**
- Emsal işlem verisi yeterliyse (5+ işlem): %10-15
- Sınırlı veri (2-3 işlem): %5-10
- Veri yoksa: %0 (uygulanmaz, açıkla)
- Şirket aktif M&A hedefiyse: %15-20'ye kadar çıkabilir

### 4C. Holding / SOTP Şirketleri

Holdinglere (NTHOL, SAHOL, KCHOL) standart İNA uygulanmaz. Bunun yerine:

```
SOTP Hedef Fiyat:
1. Her iştirak ayrı değerlenir (İNA veya Comps)
2. İştirak değerleri toplanır
3. Holding iskontosu uygulanır (genellikle %15-30)
4. Holding düzeyinde net borç çıkarılır
5. Pay sayısına bölünür

Holding İskontosu Nedenleri:
- Yönetişim riski → -%5 ila -%15
- Likidite iskontosu (iştirakler borsada değilse) → -%10 ila -%20
- Karmaşıklık iskontosu → -%5 ila -%10
```

### 4D. Kurum Konsensüsü Cross-Check

Varsa (İş Yatırım, Ak Yatırım, Garanti BBVA, Ziraat Yatırım hedef fiyatları):
- Konsensüs medyanı ile BBB hedef fiyatı karşılaştırılır
- %30+ fark varsa → nedenini açıkla (farklı büyüme varsayımı, farklı AOSM, farklı marj)
- Kurumların tavsiye dağılımı raporlanır: X/Y AL, Z TUT

---

## 5. Çıktı Formatı

### 5A. Değerleme Özet Tablosu (Her Raporda Zorunlu)

```
Tablo: Hedef Fiyat Derivasyonu

| Yöntem | Aralık | Temel Değer | Ağırlık | Katkı |
|--------|--------|-------------|---------|-------|
| İNA (Ayı/Temel/Boğa) | 180-275 TL | 221 TL | %45 | 99.5 TL |
| FD/FAVÖK Comps | 190-245 TL | 215 TL | %30 | 64.5 TL |
| İleriye Dönük F/K | 170-255 TL | 210 TL | %25 | 52.5 TL |
| **Ağırlıklı Hedef Fiyat** | | | **%100** | **216.5 TL** |
| 3 Ay İleri Taşıma (+%4.2) | | | | **225.5 TL** |
| → Yuvarlanmış Hedef Fiyat | | | | **225 TL** |

Mevcut Fiyat: 155 TL | Potansiyel Getiri: %45 | Tavsiye: EKLE
```

### 5B. Reconciliation Paragrafı (Her Raporda Zorunlu)

Yukarıdaki şablona ek olarak:
- Neden bu ağırlıkları seçtiğini açıkla (1-2 cümle)
- En büyük fark kaynağını belirt
- "Bu hedef fiyat X TL bandına oturduğu sürece tez geçerlidir" diye aralık ver

### 5C. Değerleme Aralık Grafiği (Her Raporda Zorunlu)

`grafik-uret.py: football_field_grafigi()` ile üretilir.

### 5D. Duyarlılık Matrisi (İNA içeren her raporda zorunlu)

`grafik-uret.py: dcf_sensitivity_grafigi()` ile üretilir.

**Sensitivity Matrisi Formül Bazlıdır (hardcoded değil):** [v2.2]
DCF Excel'deki Sensitivity tabı, `DCFProjeksiyon` sayfasındaki PV(10Y FCFF), Terminal NOPAT, CDF ve Equity Bridge referanslarıyla **dinamik formüllerle** hesaplanır. Inputs değiştiğinde matris otomatik güncellenir. Formül yapısı:
```
Hisse Değeri = ((PV_10Y + TermNOPAT × (1-g/ROC) / (WACC-g) × CDF_Y10) × (1-İflas) - Borç + Nakit) / Pay
```

### 5D_bis. Implied Exit Multiple Sanity Check (ZORUNLU) [v2.2]

DCF'in terminal value varsayımlarının makul olup olmadığını test eder. DCFProjeksiyon sayfasında otomatik hesaplanır:

| Metrik | Formül | Makul Aralık | Alarm |
|--------|--------|-------------|-------|
| **Implied Exit EV/EBIT** | TV / Terminal EBIT | 8-15x (gelişen piyasa perakende) | >20x ise terminal varsayım agresif |
| **Implied Exit EV/NOPAT** | TV / Terminal NOPAT | 10-20x | >25x ise kontrol et |
| **TV Ağırlığı** | PV(TV) / (PV(TV) + PV(10Y)) | %50-75 | >%80 ise model terminale aşırı bağımlı |

> **Kural:** TV Ağırlığı %80'i aşarsa, 10Y projeksiyon güvenilirliğini sorgula. Büyüme hızlı konverje ediyor mu? WACC makul mu? Terminal g GDP üstü mü?

### 5E_bis. Ters İNA Cross-Check (Her Raporda Zorunlu)

> **Amaç:** Hedef fiyatın "makullüğünü" bağımsız olarak test etmek. §9 Test 2'deki detaylı hesaplamayı burada **özet tablo** olarak raporla.

```
## Ters İNA Cross-Check

| Parametre | Mevcut Fiyat İma Ediyor | Hedef Fiyat İma Ediyor | BBB Projeksiyonu |
|-----------|------------------------|------------------------|------------------|
| 5Y Gelir CAGR | %X | %Y | %Z |
| Terminal EBIT marjı | %A | %B | %C |
| Terminal büyüme | %D | %E | %F |

Yorum: Hedef fiyatımız [piyasanın fiyatladığından %N daha yüksek/düşük] büyüme
ima ediyor. Bu fark [makul/agresif/muhafazakâr] çünkü [1-2 cümle gerekçe].
```

**Kritik kural:** Hedef fiyatın ima ettiği 5Y CAGR, tarihsel 5Y CAGR'ın 2x'ini aşıyorsa → gerekçe zorunlu (yeni pazar, M&A, yapısal değişim gibi).

---

## 5E. T2→T3 Tutarlılık Kontrolü (ZORUNLU — T3 Başlamadan Önce)

> **Neden zorunlu?** T2 finansal modelleme ile T3 değerleme arasında veri uyumsuzluğu, hedef fiyatı temelden geçersiz kılar. En yaygın hatalar: T2'de farklı gelir, T3'te farklı gelir; T2'de farklı EBIT tanımı, T3'te farklı EBIT tanımı.

### Checklist: T2 → T3 Veri Köprüsü

| # | Kontrol | T2 Kaynağı | T3 Kaynağı | Kabul Edilebilir Sapma |
|---|---------|-----------|-----------|----------------------|
| 1 | **Gelir (Y1-Y5)** | T2 finansal model | DCF projeksiyonları | <%1 (yuvarlama farkı) |
| 2 | **EBIT Tanımı** | T2 FAVÖK/FVÖK | DCF EBIT | **Tam eşleşme** — aşağıya bkz. |
| 3 | **EBIT Marjı (Y1)** | T2 model | DCF projeksiyonu | <%0.5pp fark |
| 4 | **Capex / Gelir** | T2 model | DCF yatırım harcaması | <%1pp fark |
| 5 | **Net Borç** | T2 bilanço projeksiyonu | Köprü hesabı (EV→Equity) | <%5 fark |
| 6 | **Nakit ve Nakit Benzerleri** | T2 bilanço | Köprü hesabı | <%5 fark |
| 7 | **Pay Sayısı** | T2 HBK hesabı | DCF hisse değeri böleni | **Tam eşleşme** |
| 8 | **Efektif Vergi Oranı** | T2 model | DCF FCFF hesabı | <%2pp fark |

### EBIT Tanımı Eşleştirmesi — IAS 29 İçin KRİTİK

IAS 29 uygulayan BIST şirketlerinde en az 3 farklı EBIT tanımı olabilir:

```
1. GAAP EBIT = Brüt Kâr − Faaliyet Giderleri − Diğer Faaliyet Giderleri (net)
   → Parasal pozisyon kaybını İÇERİR → genellikle düşük marj (%1-3)

2. Operasyonel EBIT = GAAP EBIT + Parasal Pozisyon Kaybı (Diğer Faal. Gid. içinde)
   → Parasal pozisyon kaybını HARIC TUTAR → gerçek operasyonel performansı yansıtır

3. API/KAP FAVÖK = Platformun kendi hesaplaması
   → Genellikle GAAP bazlı, ama amortisman geri ekleme yöntemi farklı olabilir
```

**ZORUNLU:** DCF'de hangi EBIT tanımı kullanıldığı açıkça belirtilmeli:

```
## EBIT Köprüsü (IAS 29 Şirketleri İçin ZORUNLU)

| Kalem | Tutar (mn TL) | Marj |
|-------|--------------|------|
| GAAP EBIT (gelir tablosu) | X | %Y |
| (−) Parasal pozisyon kaybı | (Z) | |
| Operasyonel EBIT (DCF'de kullanılan) | W | %V |

DCF'de kullanılan: [Operasyonel EBIT / GAAP EBIT] — Gerekçe: [...]
```

**Hata senaryosu:** T2'de GAAP EBIT (%2 marj) ile model kurup, T3'te operasyonel EBIT (%9 marj) ile DCF yaparsanız → gelecek yıl marj projeksiyonları 7pp sapacak ve hedef fiyat %40-60 şişecektir.

### Sapma Bulunursa Ne Yapılır?

1. **Sapma <%5:** Yuvarlama farkı — kabul et, not düş
2. **Sapma %5-15:** T2 veya T3'ten birini düzelt, hangisinin doğru olduğunu belirle
3. **Sapma >%15:** 🔴 T2'ye geri dön, modeli kontrol et, T3'ü askıya al

---

## 6. Dogrulama Checklist

### 6A. T3 Kapatma Sarti (T4'e gecis icin ZORUNLU)

T3 "tamamlandi" etiketini almadan once:

- [ ] INA (DCF) sonucu var mi? (bbb-dcf Faz 0-3, Excel uretildi)
- [ ] Comps tablosu var mi? (min 4-5 peer, karsilastirmali-degerleme.md'ye gore)
- [ ] Forward F/K hesabi var mi? (task3-hedef-fiyat.md 1C bolumune gore)
- [ ] Reconciliation yapildi mi? (3 yontem agirlikli ortalama + fark analizi)

**4'u de isaretlenmeden T4'e GECILMEZ.**

### 6B. Hedef Fiyat Teslim Checklist

Hedef fiyat teslim edilmeden once:

- [ ] Uc yontem de hesaplandi ve tablosu var
- [ ] Ağırlıklar gerekçeli (neden bu ağırlıklar?)
- [ ] İNA-Comps farkı %20'den büyükse açıklanmış
- [ ] Değerleme aralık grafiği mevcut
- [ ] Duyarlılık matrisi mevcut
- [ ] IAS 29 şirketse: düzeltilmiş HBK kullanılmış
- [ ] IAS 29 şirketse: Fisher parity kontrolü yapılmış
- [ ] İleri taşıma uygulandıysa açıkça belirtilmiş
- [ ] Kurum konsensüsü (varsa) cross-check yapılmış
- [ ] Hedef fiyat hem nokta (yuvarlanmış) hem aralık olarak raporlanmış
- [ ] Potansiyel getiri ve tavsiye açıkça belirtilmiş

---

## 7. Sık Yapılan Hatalar

| Hata | Sonuç | Çözüm |
|------|-------|-------|
| Sadece İNA ile hedef fiyat türetme | Piyasa duyarlılığı yok | Comps + Forward F/K ekle |
| Comps'ta peer grubu 2-3 şirket | İstatistiksel anlamsız | Min 4-5 peer, ideal 6-8 |
| Forward F/K'da IAS 29 düzeltmesiz HBK | F/K yanıltıcı düşük/yüksek | Parasal kazanç/kayıp çıkar |
| Ağırlık gerekçesi yok | Keyfi görünür | Her ağırlık 1-2 cümle gerekçeli |
| İleri taşıma açıklanmamış | Şeffaflık sorunu | "3 ay ileri taşıma" notu |
| Reconciliation paragrafı yok | Fark açıklanmamış | Zorunlu — fark nedenini yaz |
| Değerleme aralık grafiği yok | Görselleştirme eksik | football_field_grafigi() |
| Duyarlılık matrisi yok | Hassasiyet bilinmiyor | AOSM × büyüme matrisi |

---

## 8. Duyarlılık Matrisi — Standart Spec

Her İNA bazlı hedef fiyat için 2-boyutlu duyarlılık tablosu zorunludur.

### Grid Boyutu ve Parametreler

**Standart grid: 7 satır × 5 sütun**

| Eksen | Parametre | Aralık | Adım |
|-------|-----------|--------|------|
| Satır (dikey) | AOSM (%) | Baz ±200bp | 50bp adımlar → 7 değer |
| Sütun (yatay) | Terminal büyüme / Çıkış çarpanı | Baz ±100bp veya ±0.5x | 2 adım her yönde → 5 değer |

**Örnek grid (AOSM × Terminal Büyüme):**
```
Hisse Başına Değer (TL)    Terminal Büyüme Oranı (%)
AOSM (%)     2.0%    2.5%    3.0%    3.5%    4.0%
─────────────────────────────────────────────────
   9.0%       165     175     187     201     218
   9.5%       153     162     172     184     198
  10.0%       143     151     160     171     183   ← BAZI (merkez)
  10.5%       133     141     149     158     169
  11.0%       125     131     139     147     156
  11.5%       117     123     130     137     146
  12.0%       110     116     122     128     136
```

**Kural:** Baz durum değeri MERKEZ hücrede yer almalı (4. satır, 3. sütun = hücre[4,3]).

### Renk Skalası

| Renk | Koşul |
|------|-------|
| 🟢 Koyu yeşil | Hedef fiyat > Mevcut fiyat × 1.30 (>%30 artış potansiyeli) |
| 🟡 Açık yeşil | Hedef > Mevcut × 1.15 (%15-30 potansiyel) |
| ⬜ Nötr | ±%15 aralığında |
| 🟠 Açık kırmızı | Hedef < Mevcut × 0.85 (%15-30 kayıp riski) |
| 🔴 Koyu kırmızı | Hedef < Mevcut × 0.70 (>%30 kayıp riski) |

**Script:** `grafik-uret.py` → `duyarlilik_matrisi()` fonksiyonu.

Fonksiyon parametreleri:
```python
duyarlilik_matrisi(
    baz_aosm=0.10,          # Baz AOSM (örn. 10.0%)
    baz_terminal_g=0.03,    # Baz terminal büyüme
    aosm_adim=0.005,        # 50bp adım
    terminal_adim=0.005,    # 50bp adım
    satirlar=7,             # Satır sayısı (baz ±3)
    sutunlar=5,             # Sütun sayısı (baz ±2)
    mevcut_fiyat=...,       # Renk skalası referansı
)
```

### TL vs USD Duyarlılık

- **TL İNA:** AOSM × terminal büyüme grid
- **USD İNA:** WACC × terminal büyüme grid
- İkisi aynı raporda varsa: Fisher cross-check sütunu ekle (TL hedef ÷ kur ≈ USD hedef)

---

---

## 9. Bağımsız Değerleme Sanity Check

DCF ve comps tamamlandıktan sonra, hedef fiyatı açıklamadan önce 4 bağımsız test uygulanır. Bu testler modeli değil, **sonucun makullüğünü** sorgular.

> Amaç: "Model doğru çalıştı" ile "Sonuç mantıklı" farklı sorulardır. Her ikisi de onaylanmalı.

---

### Test 1: İmplied ROIC Testi

Hedef fiyatın ima ettiği terminal ROIC'ı hesapla. Bu ROIC makul mu?

```
Adım 1: Hedef hisse fiyatı → Equity değeri
Adım 2: EV = Equity + Net Borç
Adım 3: IC = Son dönem Yatırılmış Sermaye × (1 + terminal büyüme)^n
         (basitleştirilmiş: son IC'nin terminal büyüme oranıyla büyütülmüş hali)
Adım 4: İmplied ROIC = Terminal NOPAT / Terminal IC

Kontrol: İmplied ROIC mantıklı mı?
- ROIC >> WACC ve güçlü moat varsa → kabul edilebilir
- ROIC ≈ WACC ama "güçlü moat" diyoruz → çelişki, varsayımı sorgula
- ROIC < WACC → hedef fiyat değer yıkımını fiyatlıyor, bunu açıkla
```

**Kural:** İmplied ROIC, Damodaran sektör ortalamasından >2x yukarıdaysa güçlü moat gerekçesi zorunlu.

---

### Test 2: Ters İNA Testi

Mevcut hisse fiyatının fiyatladığı büyümeyi hesapla.

```
# Hedef fiyat yerine MEVCUT fiyatı kullan
# WACC ve terminal marjı sabit tut
# Gelir büyümesini (solve) olarak çöz

Mevcut fiyat = X TL
WACC = %Y, terminal marj = %Z
İmplied büyüme = ?

Karşılaştır:
- Tarihsel 5Y büyüme neydi?
- Sektör büyümesi ne?
- İmplied büyüme bunlara göre makul mu?
```

**Ters İNA iki soruyu yanıtlar:**
1. Mevcut fiyat ucuz mu pahalı mı? (İmplied büyüme düşükse ucuz, yüksekse pahalı)
2. Tezimizin fiyatlanıp fiyatlanmadığı: Eğer consensus ile aynı büyümeyi görüyorsak, neden hisse almalıyız?

---

### Test 3: Gordon Growth ile Teorik PD/DD

Şirketin ROIC'ı ve büyüme oranı verildiğinde, teorik PD/DD nedir?

```
# Gordon Growth Model derivasyonu:
Teorik PD/DD = (ROIC − g) / (Ke − g)
              veya
            = (ROE − g) / (Ke − g)

Burada:
  ROIC = Terminal ROIC (tarihsel ortalama veya projected)
  g = Terminal büyüme oranı
  Ke = Özsermaye maliyeti

Örnek:
  ROE = %20, g = %4, Ke = %14
  Teorik PD/DD = (0.20 − 0.04) / (0.14 − 0.04) = 0.16 / 0.10 = 1.6x

Kontrol: Hedef fiyatımızın ima ettiği PD/DD ile karşılaştır.
- İmplied PD/DD teorik değere yakınsa → tutarlı
- İmplied PD/DD çok yüksekse → büyüme veya ROIC artış beklentisi var, açıkla
- İmplied PD/DD çok düşükse → değer tuzağı riski var, moat'ı sorgula
```

---

### Test 4: EV/IC vs ROIC/WACC Skalası

Yüksek ROIC şirketler yüksek EV/IC hak eder. Bu ilişki grafik veya tablo olarak kontrol edilir.

```
Temel ilişki:
  EV/IC = (ROIC − g) / (WACC − g)    [sürdürülebilir ROIC varsayımıyla]

Pratik kontrol tablosu (WACC = %12, g = %4):

| ROIC | Teorik EV/IC |
|------|-------------|
| %10  | 0.75x (değer yıkımı → <1x normal) |
| %12  | 1.0x |
| %16  | 1.5x |
| %20  | 2.0x |
| %25  | 2.63x |
| %30  | 3.25x |

Hedef fiyatın ima ettiği EV/IC bu tabloya göre makul mu?
```

---

### Sanity Check Çıktı Formatı

Her değerleme sonunda bu 4 testin özeti raporlanır:

```
## Değerleme Sanity Check

| Test | Sonuç | Değerlendirme |
|------|-------|---------------|
| İmplied ROIC | %X | Sektör ort. %Y → [Makul/Yüksek/Düşük] |
| Ters İNA (mevcut fiyat) | %X büyüme fiyalanıyor | Tarihsel %Y → [Ucuz/Pahalı/Makul] |
| Teorik PD/DD | X.Xx | İmplied PD/DD X.Xx → [Tutarlı/Çelişki] |
| EV/IC vs ROIC | X.Xx EV/IC | ROIC %X için teorik Xx → [Makul/Yüksek] |

**Sonuç:** Tüm testler tutarlı → hedef fiyat [X TL] savunulabilir.
```

Bir testte çelişki varsa → önceki bölümlere dön, kaynağını bul, ya gerekçelendir ya düzelt.

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-17 | v1.0 oluşturuldu — 3 yöntem (İNA + Comps + Forward F/K), reconciliation süreci, BBB kuralları, SOTP, ileri taşıma, IAS 29 dikkat noktaları |
| 2026-03-18 | §8 Duyarlılık Matrisi Spec eklendi — 7×5 grid standardı, renk skalası, grafik-uret.py parametre tablosu |
| 2026-03-18 | §9 Bağımsız Değerleme Sanity Check — 4 test: İmplied ROIC, Ters İNA, Gordon Growth PD/DD, EV/IC vs ROIC skalası |
| 2026-03-22 | §5E T2→T3 Tutarlılık Kontrolü — EBIT köprüsü, 8 maddelik cross-check, sapma aksiyon rehberi |
| 2026-03-22 | Adım 3 genişletildi — >%30 İNA-Comps fark için zorunlu 5-maddeli yapısal açıklama şablonu |
| 2026-03-22 | §5E_bis Ters İNA Cross-Check — hedef fiyat çıktı formatına zorunlu özet tablo eklendi |
| 2026-03-22 | §10 Monte Carlo Simülasyonu — 10.000 iterasyon, 6 parametre dağılımı, VaR/CVaR, olasılık dağılımı |
| 2026-03-22 | §11 Senaryo Tutarlılık Kontrolü ve Adaptif Ağırlıklar — üç yöntem tolerans kuralları, adaptif senaryo ağırlıkları, DCF-FM çakışma kontrolü, güncelleme zamanlama |
| 2026-03-22 | **v2.1** — Forward HBK parametrik formul (hardcoded 9/12 → `(FY_END-M) mod 12` genel formul, 3 ornek). Bolum 0 eklendi: Temel Metodolojik Referanslar tablosu — senaryo-metodoloji.md v3.0 cross-reference (reel/nominal, WACC, temettü, kazanç kalitesi, EV FX, Forward HBK parametrik) |
| 2026-03-22 | **v2.2** — §5D: Sensitivity matrisi formül bazlı olduğu belgelendi (DCFProjeksiyon referanslı, hardcoded değil). §5D_bis: Implied Exit Multiple sanity check eklendi (EV/EBIT, EV/NOPAT, TV Ağırlığı — makul aralıklar ve alarm eşikleri) |

---

## §10. Monte Carlo DCF Simülasyonu (T3 Son Adım — ZORUNLU)

### Felsefe

3 ayrık senaryo (Bear/Base/Bull) değerleme pratiğinde yaygın ama yetersizdir:
- Sadece 3 nokta tahmini verir — aradaki sürekliliği kaçırır
- Parametreler arasındaki korelasyonları yakalamaz
- "Hedef fiyatın %70 olasılıkla X-Y TL arasında olduğu" gibi olasılıksal ifadeler üretemez

MS/JPM/Goldman DCF çalışmalarında Monte Carlo "supplementary analysis" olarak sunulur. Deterministic DCF (ana model) + Monte Carlo (risk dağılımı) birlikte verilir.

### BBB Monte Carlo Yaklaşımı

**Girdiler:** T2'deki baz senaryo parametreleri + Bear/Bull sınırlarından türetilen dağılımlar

6 anahtar parametreye sürekli olasılık dağılımı atanır:

| # | Parametre | Dağılım Tipi | Baz | Min (Bear) | Max (Bull) | Gerekçe |
|---|-----------|-------------|-----|------------|------------|---------|
| 1 | Gelir büyümesi Y1 | PERT | T2 baz | Bear Y1 | Bull Y1 | PERT: uçlar düşük olasılıklı, merkez ağırlıklı |
| 2 | Gelir büyümesi Y2-5 CAGR | PERT | T2 baz | Bear CAGR | Bull CAGR | |
| 3 | Hedef EBIT marjı | PERT | T2 baz | Bear marj | Bull marj | |
| 4 | Terminal büyüme (g) | Üçgen | T2 baz | -50bp | +50bp | Dar aralık — terminal hassasiyeti yüksek |
| 5 | WACC (terminal) | Normal | T2 baz | sigma=100bp | | Normal dağılım — simetrik belirsizlik |
| 6 | Terminal ROC | PERT | T2 baz | Bear ROC | Bull ROC | |

**Neden PERT dağılımı?**
- Üçgen dağılımdan daha gerçekçi — uçlara daha düşük olasılık atar
- Goldman ve Damodaran'ın tercih ettiği DCF dağılımı
- 3 parametre: min, mode (en olası), max — Bear/Base/Bull ile doğal uyum

**Korelasyon matrisi (opsiyonel ama önerilen):**

| | Büyüme Y1 | CAGR Y2-5 | EBIT Marjı | Terminal g | WACC | Terminal ROC |
|---|-----------|-----------|-----------|-----------|------|-------------|
| Büyüme Y1 | 1.0 | 0.6 | 0.3 | 0.2 | 0.0 | 0.2 |
| CAGR Y2-5 | | 1.0 | 0.4 | 0.3 | 0.0 | 0.3 |
| EBIT Marjı | | | 1.0 | 0.2 | 0.0 | 0.5 |
| Terminal g | | | | 1.0 | 0.0 | 0.0 |
| WACC | | | | | 1.0 | 0.0 |
| Terminal ROC | | | | | | 1.0 |

Gerekçe: Yüksek büyüme genellikle daha iyi marjlarla koreledir (ölçek etkisi). WACC büyük ölçüde makro faktörlere bağlı — şirket spesifik değil.

### Çalıştırma

```bash
# Evrensel Monte Carlo script'i
python3 ~/.openclaw/workspace/skills/bbb-dcf/scripts/monte_carlo_dcf.py \
  --config research/companies/{TICKER}/{TICKER}_mc_config.json \
  --iterations 10000 \
  --output research/companies/{TICKER}/{TICKER}_monte_carlo.md
```

### Monte Carlo Yapılandırma Dosyası

T2 ve T3 tamamlandıktan sonra, baz/bear/bull parametrelerinden otomatik oluşturulur:

```json
{
  "ticker": "{TICKER}",
  "pay_sayisi": 160,
  "net_borc": -921,
  "iflas_olasiligi": 0.01,
  "baz_gelir": 27675,
  "projeksiyon_yili": 10,
  "parametreler": {
    "gelir_buyume_y1": {"dagilim": "pert", "min": 0.08, "mode": 0.15, "max": 0.22},
    "gelir_buyume_cagr_y2_5": {"dagilim": "pert", "min": 0.08, "mode": 0.12, "max": 0.16},
    "hedef_ebit_marji": {"dagilim": "pert", "min": 0.08, "mode": 0.10, "max": 0.12},
    "terminal_buyume": {"dagilim": "triangle", "min": 0.025, "mode": 0.035, "max": 0.045},
    "wacc_terminal": {"dagilim": "normal", "mean": 0.1208, "std": 0.01},
    "terminal_roc": {"dagilim": "pert", "min": 0.121, "mode": 0.125, "max": 0.15}
  },
  "vergi_orani": 0.23,
  "sales_capital_y1_5": 5.0,
  "sales_capital_y6_10": 4.5,
  "sfp_explicit": 0.025,
  "sfp_terminal": 0.015
}
```

### Zorunlu Monte Carlo Çıktıları

```markdown
## Monte Carlo Simülasyon Sonuçları — {TICKER}
### İterasyon: 10.000 | Tarih: YYYY-MM-DD

### Dağılım İstatistikleri
| Metrik | Değer |
|--------|-------|
| Ortalama (Beklenen Değer) | X TL |
| Medyan (P50) | X TL |
| Standart Sapma | X TL |
| 10. Yüzdelik (P10) | X TL |
| 25. Yüzdelik (P25) | X TL |
| 75. Yüzdelik (P75) | X TL |
| 90. Yüzdelik (P90) | X TL |
| Minimum | X TL |
| Maximum | X TL |
| VaR %95 (aşağı yön riski) | X TL |
| CVaR %95 (koşullu VaR) | X TL |

### Olasılık Değerlendirmesi
| Eşik | Olasılık |
|------|----------|
| > Mevcut fiyat (X TL) | %Y |
| > Hedef fiyat (X TL) | %Y |
| > Bull senaryo (X TL) | %Y |
| < Bear senaryo (X TL) | %Y |

### Deterministic vs Monte Carlo Karşılaştırma
| Yöntem | Değer | Fark |
|--------|-------|------|
| Deterministic Base (T3) | X TL | — |
| MC Ortalama | X TL | %Y sapma |
| MC Medyan | X TL | %Y sapma |

### Hassasiyet Sıralaması (Tornado Analizi)
| Parametre | Baz → Baz+1σ Etkisi | Rank |
|-----------|---------------------|------|
| [En etkili parametre] | ±X TL | 1 |
| [2. parametre] | ±X TL | 2 |
| ... | | |

> Deterministic ve MC ortalaması arasında >%10 fark varsa → parametrelerin dağılım şeklini gözden geçir (asimetri kontrol).
```

### T3 VALUATION.md'ye Entegrasyon

Monte Carlo sonuçları VALUATION.md'nin §12 (Sonuç) bölümüne ek paragraf olarak eklenir:

```
Monte Carlo Doğrulaması (10.000 iterasyon):
- MC ortalama X TL (deterministic baz: Y TL, sapma: %Z)
- P(hisse > mevcut fiyat) = %W → [güçlü/orta/zayıf] güven
- VaR(%95): X TL — en kötü %5 senaryoda bile [X] TL üzeri
- En hassas parametre: [parametre adı] → bu varsayıma özellikle dikkat
```

### Grafik Gereksinimleri (T4)

Monte Carlo çalıştırıldığında 2 grafik üretilir:
1. **Olasılık dağılımı histogramı** (G_MC01): 50 bin, mevcut fiyat + hedef fiyat çizgileri
2. **Tornado grafiği** (G_MC02): Parametre hassasiyeti sıralaması

---

## §11. Senaryo Tutarlilik Kontrolu ve Adaptif Agirliklar

> **Referans**: Detayli metodoloji icin bkz. `senaryo-metodoloji.md`

### 11.1 Uc Yontem Senaryo Tutarlilik Kontrolu (ZORUNLU)

Her senaryo (Bear/Base/Bull) icin INA, Comps ve Forward F/K hedef fiyatlari hesaplandiktan sonra:

```
Tolerans Kurallari:
- Bull INA vs Bull Comps: Fark <= %15 (aksi halde dominant yontemi sec, sapma notu yaz)
- Bull INA vs Bull F/K: Fark <= %20
- Bear senaryolarda tolerans %25'e kadar kabul edilir (dusuk guven)

Dogrulama:
[ ] Bull INA ≈ Bull Comps (±%15)
[ ] Bear INA ≈ Bear Comps (±%25)
[ ] Agirlikli hedef >= konsensus fiyatin %90'i (sanity check)
[ ] TV agirligi < %70 (model frajilik kontrolu)
[ ] Terminal ROC > Terminal WACC (tum senaryolarda)
```

### 11.2 Adaptif Senaryo Agirliklari

Sabit %25/%50/%25 KULLANMAYIN. T1 ciktilarindan adaptif agirliklar hesaplayin:

```
Adim 1: Temel = Bear %25 | Base %50 | Bull %25
Adim 2: MQS duzeltmesi (bkz. senaryo-metodoloji.md Bolum 3.2)
Adim 3: Risk matrisi duzeltmesi (bkz. senaryo-metodoloji.md Bolum 3.3)
Adim 4: Nihai = Bear_final | Base_final | Bull_final

Kisit: Her senaryo agirligi >= %10

Ornek:
  MQS = 22 (orta) → duzeltme yok
  En yuksek risk olasiligi = %35 → duzeltme yok
  Nihai: %25 / %50 / %25 (standart)

Ornek:
  MQS = 26 (yuksek kalite) → Bear -5pp, Bull +5pp
  En yuksek risk olasiligi = %15 → Bear -5pp, Bull +5pp
  Nihai: %15 / %50 / %35 (yuksek kaliteli, dusuk riskli sirket)
```

### 11.3 DCF-FM Cakisma Kontrolu

T3 hedef fiyat hesaplanmadan ONCE, DCF ve FM senaryolarinin tutarliligini dogrulayin:

```
[ ] FM terminal buyume = DCF terminal g (birebir)
[ ] FM Base CAGR ≈ DCF Base Y1-5 ortalama (±2pp)
[ ] FM ETR = DCF vergi orani (birebir)
[ ] Senaryo agirliklari her iki dosyada ayni
[ ] Bear hisse degeri FM ≈ DCF Bear (±%15)
```

Uyumsuzluk cikarsa: DCF master kabul edilir, FM uyumlu hale getirilir.

### 11.4 Senaryo Guncelleme Zamanlama

```
Senaryolar su durumlarda GUNCELLENMELI:
1. T2 tamamlandiginda (ilk olusturma)
2. T3 INA sonucu ciktiginda (TV agirligi kontrolu → gerekirse terminal varsayimlari revize)
3. Monte Carlo sonucu ciktiginda (MC ortalama vs agirlikli ortalama ±%10 kontrolu)
4. T5 rapor oncesi (son kalite kontrolu)
5. 6 aylik geri test sirasinda (backtest sonucuna gore kalibrasyon)
```
