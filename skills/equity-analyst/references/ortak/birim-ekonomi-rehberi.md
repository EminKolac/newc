# Unit Economics — Dijital/Platform Şirketleri İçin Birim Ekonomi Analizi

## Ne Zaman Kullanılır?

Subscription, platform, marketplace veya SaaS benzeri iş modeline sahip şirketlerde — birim ekonomi metrikleri geleneksel EBITDA/FCF'den daha iyi hikaye anlatır. BIST'te: MACKO (Bilyoner/dijital eğlence), Pop Mart (IP/koleksiyon platformu), DOCO (platform), Getir-benzeri startuplar.

---

## 1. Temel Metrikler

### Müşteri Ekonomisi

| Metrik | Formül | Neden Önemli |
|--------|--------|-------------|
| **CAC** (Customer Acquisition Cost) | Satış+Pazarlama Gideri / Yeni Müşteri Sayısı | Müşteri kazanma maliyeti |
| **LTV** (Lifetime Value) | ARPU × Brüt Marj × Ortalama Müşteri Ömrü | Müşterinin toplam değeri |
| **LTV/CAC** | LTV / CAC | >3x sağlıklı, <1x para yakıyor |
| **Payback Period** | CAC / (ARPU × Brüt Marj / ay) | CAC'yi kaç ayda geri alırsın |
| **ARPU** (Kullanıcı Başına Ortalama Gelir) | Toplam Gelir / Aktif Kullanıcı Sayısı | Monetizasyon gücü |
| **Churn Rate** | Kaybedilen Müşteri / Dönem Başı Müşteri | Müşteri tutma başarısı |

### Büyüme Kalitesi

| Metrik | Formül | Neden Önemli |
|--------|--------|-------------|
| **NDR** (Net Dollar Retention) | (Başlangıç MRR + Expansion - Churn - Contraction) / Başlangıç MRR | >100% = mevcut müşteriler büyüyor |
| **GDR** (Gross Dollar Retention) | (Başlangıç MRR - Churn - Contraction) / Başlangıç MRR | >90% sağlıklı |
| **Rule of 40** | Gelir Büyümesi (%) + EBITDA Marjı (%) | >40 = kaliteli SaaS |
| **Organik vs Paid Growth** | Organik müşteri / toplam yeni müşteri | Yüksek organik = sürdürülebilir |

---

## 2. Cohort Analizi

Cohort analizi "Ocak'ta kazandığım müşteriler 12 ay sonra ne yapıyor?" sorusuna cevap verir. Aggregate metriklerin maskelediği trend bozulmalarını ortaya çıkarır.

### Cohort Retention Tablosu

```
| Cohort | Ay 0 | Ay 1 | Ay 3 | Ay 6 | Ay 12 | Ay 24 |
|--------|------|------|------|------|-------|-------|
| Oca-25 | 100% | X%   | X%   | X%   | X%    | X%    |
| Şub-25 | 100% | X%   | X%   | X%   | X%    | —     |
| Mar-25 | 100% | X%   | X%   | X%   | —     | —     |
```

### Ne Aramalı?
- **Improving cohorts:** Yeni cohort'lar eskilerden daha iyi tutunuyor → ürün iyileşiyor
- **Degrading cohorts:** Yeni cohort'lar eskilerden daha kötü → büyüme kalitesi düşüyor
- **Cohort revenue expansion:** Aynı cohort zamanla DAHA FAZLA harcıyor → NDR > 100%
- **Plateau noktası:** Churn nerede duruyor? (ör. Ay 6'da %30 kaybedip sonra stabil)

---

## 3. BIST Dijital/Platform Şirketleri İçin Adaptasyon

### Veri Erişim Sorunu

BIST şirketleri genellikle unit economics detayını KAP'ta PAYLAŞMAZ. Çözümler:
1. **Faaliyet raporundaki operasyonel metrikler** — aktif kullanıcı, işlem hacmi, mağaza sayısı
2. **IR sunumlarındaki KPI slide'ları** — genellikle en zengin kaynak
3. **App store/web traffic verileri** — cross-check için (SimilarWeb, Sensor Tower)
4. **Sektör kuruluşu verileri** — oyun pazarı (Gaming Turkey), e-ticaret (TÜBİSAD)

### MACKO (Bilyoner) Örneği
- Aktif kullanıcı = bahis hesabı olan + son 30 günde işlem yapan
- ARPU = toplam bahis geliri / aktif kullanıcı
- Churn = rekabetçi piyasada yüksek (Nesine, Misli, Birebin)
- Brüt marj = komisyon oranı - vergi/fon kesintileri

### Pop Mart Örneği
- ARPU = gelir / aktif müşteri (satın alma yapan)
- Repurchase rate = tekrar satın alan müşteri oranı
- IP diversifikasyonu = tek IP bağımlılığı riski (THE MONSTERS %35)
- Coğrafya mix = yurt dışı payı artışı (H1 2025: ~%50)
- Brüt marj = %70+ (IP lisans değil, kendi IP = düşük royalty)

---

## 4. Değerleme İmplikasyonu

### LTV/CAC → Terminal ROIC Köprüsü

LTV/CAC doğrudan sermaye getirisi ile ilişkilidir:
- LTV/CAC > 5x → Yüksek ROIC, güçlü moat (Switching cost veya network effect)
- LTV/CAC 3-5x → Sağlıklı ama rekabetçi baskı altında
- LTV/CAC < 3x → Dikkatli — organik büyüme zayıf olabilir
- LTV/CAC < 1x → Para yakıyor, VC desteksiz sürdürülemez

### Rule of 40 ve Değerleme Çarpanı

```
40 Kuralı skoru > 60 → Prim FD/Hasılat (>10x)
40 Kuralı skoru 40-60 → Orta FD/Hasılat (5-10x)
40 Kuralı skoru < 40 → İskonto FD/Hasılat (<5x)
```

---

## 5. Sık Yapılan Hatalar

| Hata | Sonuç | Çözüm |
|------|-------|-------|
| Blended churn kullanmak | Segment farkları maskeleniyor | Cohort bazlı churn |
| Paid vs organic ayrımı yapmamak | CAC gerçekten düşük sanıyorsun | Marketing harcamasız büyümeyi izole et |
| Gross margin yerine net margin kullanmak | LTV şişiyor | LTV = ARPU × GROSS margin × ömür |
| 100% retention varsaymak | LTV → sonsuz | Gerçekçi churn oranı kullan |
| Tek cohort'tan genelleme | Yanıltıcı trend | Min 6-12 cohort karşılaştır |
