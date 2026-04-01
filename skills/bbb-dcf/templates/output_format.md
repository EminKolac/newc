# DCF Rapor Çıktı Formatı — v2.0

**Güncelleme:** 2026-02-10 — İlker'in THYAO geri bildirimi sonrası kapsamlı revizyon
**Kaynak:** Damodaran "Valuation as Picture" sayfası + İlker feedback

---

## 🎯 ZORUNLU ÇIKTILAR

Her DCF değerleme için **3 çıktı** üretilmelidir:

| # | Çıktı | Format | İçerik |
|---|-------|--------|--------|
| 1 | **Valuation as Picture** | Excel (.xlsx) | Damodaran formatında özet tablo + story alanları |
| 2 | **Değerleme Raporu** | PDF | Sayfa 1: Özet + kısa story, Sayfa 2+: Detaylı açıklamalar |
| 3 | **Markdown Raporu** | .md | Tam teknik rapor (mevcut format + iyileştirmeler) |

**Çıktı lokasyonu:** `/Users/ilkerbasaran/Documents/Odesus/valuations/[TICKER]_[TARIH]/`

---

## 📊 ÇIKTI 1: Valuation as Picture (Excel)

Damodaran'ın Excel dosyasındaki "Valuation as Picture" sayfasının **birebir reprodüksiyonu**.

### Tablo Yapısı

```
┌─────────────────────────────────────────────────────────┐
│           [ŞİRKET] — VALUATION AS PICTURE               │
│           Tarih: [TARİH] | Para Birimi: [USD/TL]        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  GROWTH STORY          │  PROFITABILITY STORY           │
│  ────────────          │  ────────────────────          │
│  [Kısa açıklama]       │  [Kısa açıklama]              │
│  Rev Growth: X%→Y%     │  EBIT Margin: X%→Y%           │
│  Terminal g: Z%        │  Terminal Margin: W%           │
│                        │                                │
├────────────────────────┼────────────────────────────────┤
│                        │                                │
│  GROWTH EFFICIENCY     │  RISK STORY                    │
│  STORY                 │  ──────────                    │
│  ──────────────────    │  [Kısa açıklama]               │
│  [Kısa açıklama]       │  WACC: X%→Y%                  │
│  Sales/Capital: X→Y    │  Beta: Z                       │
│  Reinvestment Rate: Z% │  P(failure): W%                │
│                        │                                │
├────────────────────────┼────────────────────────────────┤
│                                                         │
│  COMPETITIVE ADVANTAGES                                 │
│  ──────────────────────                                 │
│  [Moat açıklaması — hub avantajı, filo, rota ağı vb.]  │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  SUMMARY                                                │
│  Value/Share: [XX] TL  │  Current Price: [YY] TL       │
│  Upside/Downside: [Z%] │  Confidence: [Low/Med/High]   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Excel Sayfaları

| Sayfa | İçerik |
|-------|--------|
| **Valuation as Picture** | Yukarıdaki tablo + story alanları |
| **Assumptions** | Tüm varsayımlar + kaynakları + gerekçeleri |
| **Projections** | 10 yıllık projeksiyon tablosu |
| **WACC** | WACC bileşenleri detay |
| **Sensitivity** | 2D sensitivity matrix (5×5) |
| **Diagnostics** | Damodaran 6 soru + cevaplar |
| **Historicals** | Tarihsel veriler (gelir, marj, büyüme) |
| **Peers** | Eşlenik karşılaştırma tablosu |

---

## 📄 ÇIKTI 2: PDF Raporu

### Sayfa 1: Özet (Valuation as Picture)
- Yukarıdaki tablo formatı
- 5 Story alanı **kısa** olarak doldurulmuş (her biri 2-3 cümle)
- Final değer + piyasa karşılaştırması

### Sayfa 2+: Detaylı Açıklamalar

Her story alanı detaylıca açılmalı:

#### Growth Story (Detaylı)
- Tarihsel gelir büyüme trendi (5-10Y tablo)
- CAGR hesaplamaları (3Y, 5Y, 10Y)
- Büyüme kaynakları (kapasite, fiyatlama, pazar genişlemesi)
- Toplam pazar büyüklüğü ve şirketin pazar payı projeksiyonu
- Neden bu büyüme oranını seçtim?

#### Profitability Story (Detaylı)
- Tarihsel EBIT marjı trendi (5-10Y tablo)
- Son yıllardaki trend ve nedenleri
- Eşlenik karşılaştırma (yerli + yabancı peer'lar)
- Sektör marj ortalamaları
- Marj yakınsama gerekçesi (neden X yıl?)
- Birim ekonomisi analizi

#### Growth Efficiency Story (Detaylı)
- Tarihsel Sales/Capital trendi
- Sektör ortalaması karşılaştırması
- Yeniden yatırım verimliliği
- Fazla kapasite analizi
- Büyüme → yeniden yatırım tutarlılığı

#### Risk Story (Detaylı)
- WACC hesabı adım adım (tüm kaynaklar belirtilmiş)
- Sektör WACC ortalaması karşılaştırması
- WACC'in zamanla değişim gerekçesi
- Başarısızlık olasılığı gerekçesi
- Makro riskler (kur, jeopolitik, regülasyon)

#### Competitive Advantages (Detaylı)
- Moat analizi (4 kategori: giriş bariyeri, switching cost, pazar yapısı, münhasır varlıklar)
- Rekabet analizi
- Sürdürülebilirlik değerlendirmesi
- Terminal ROC vs WACC yorumu

### Son Bölüm: "Neden Bu Değeri Biçtim?"
- Tüm hikayeyi bir araya getiren 1-2 sayfa açıklama
- Ana tez
- En kritik varsayımlar ve hassasiyetleri
- Piyasa fiyatıyla farkın nedeni
- Yatırım kararı önerisi (al/tut/sat/izle)

---

## 📝 ÇIKTI 3: Markdown Raporu (Teknik Detay)

### Rapor Yapısı (Genişletilmiş)

#### 1. Özet (Executive Summary)
```
[ŞİRKET] (#TICKER) — DCF Değerleme Özeti
Tarih: [TARİH] | Para Birimi: [TL/USD] | Yaklaşım: [Nominal/Reel/USD]
Döviz Kuru: [KURU ve TARİHİ belirt]

Tahmini Değer: [XX.XX] TL/hisse
Güncel Fiyat:  [XX.XX] TL
Upside/Downside: [+/- XX%]

Değer Aralığı (sensitivity): [XX - YY] TL/hisse
Güven Seviyesi: [Düşük/Orta/Yüksek]
```

#### 2. Valuation as Picture (5 Story)
Her biri 2-3 cümle:
- Growth Story
- Profitability Story
- Growth Efficiency Story
- Risk Story
- Competitive Advantages

#### 3. Temel Varsayımlar Tablosu

**ZORUNLU FORMAT — Her varsayım self-documenting olmalı:**

| Değişken | Tam İsim | Değer | Kaynak | Gerekçe | Tarihsel Ref. |
|----------|----------|-------|--------|---------|---------------|
| Rf | Risksiz Faiz Oranı (Risk-free Rate) | %4.50 | US 10Y Treasury, [tarih] | USD DCF → USD risksiz oran | — |
| β_U | Kaldıraçsız Beta (Unlevered Beta) | 0.82 | Damodaran Air Transport Global, [tarih] | Bottom-up sektör betası | Regression β: [X] |
| β_L | Kaldıraçlı Beta (Levered Beta) | 1.435 | Hesaplanan: β_U × (1+(1-t)×D/E) | — | — |
| D/E | Borç/Özsermaye Oranı (Debt-to-Equity) | 1.0 | KAP bilanço [tarih] + MCap [tarih] | Lease borcu dahil (IFRS 16) | — |
| ERP_M | Olgun Piyasa Risk Primi (Mature ERP) | %4.60 | Damodaran S&P 500 Implied ERP, [tarih] | S&P 500 bazlı | — |
| ERP_C | Ülke Risk Primi (Country ERP) | %10.87 | Damodaran Turkey, [tarih] | [Kendi hesap: X%, Fark: Y%] | — |
| λ | Lambda (Ülke Riski Maruziyeti) | 0.35 | Hesaplanan: Gelir FX %75, Gider FX %60 | Operasyon TR ağırlıklı | — |
| ... | ... | ... | ... | ... | ... |

**⚠️ KURAL:** β_U, λ, Rf gibi kodların yanında **mutlaka** tam Türkçe/İngilizce isim yazılmalı.

#### 4. Tarihsel Analiz (YENİ — ZORUNLU)

##### 4a. Gelir Büyümesi Tarihsel

| Yıl | Gelir (USD M) | YoY Büyüme | Not |
|-----|---------------|------------|-----|
| 2019 | X | — | Pandemi öncesi |
| 2020 | X | -X% | COVID |
| 2021 | X | +X% | Toparlanma |
| ... | ... | ... | ... |
| 2024 | X | +X% | Son yıl |

**CAGR:** 3Y: X%, 5Y: Y%, 10Y: Z%
**Projeksiyon vs Tarihsel:** [Karşılaştırma ve gerekçe]

##### 4b. EBIT Marjı Tarihsel

| Yıl | EBIT Marjı | Trend | Not |
|-----|------------|-------|-----|
| 2019 | X% | — | Normal yıl |
| ... | ... | ... | ... |

**Ortalama (5Y):** X% | **Ortalama (10Y):** Y%
**Son trend:** Yükseliyor/Düşüyor — Neden?

##### 4c. Eşlenik Karşılaştırma (Peer Comparison)

| Şirket | Ülke | Gelir (USD B) | EBIT Marjı | EV/EBITDA | Sales/Cap | ROIC |
|--------|------|---------------|------------|-----------|-----------|------|
| THYAO | TR | X | X% | X | X | X% |
| Pegasus | TR | X | X% | X | X | X% |
| Lufthansa | DE | X | X% | X | X | X% |
| IAG | UK | X | X% | X | X | X% |
| Delta | US | X | X% | X | X | X% |
| Sektör Ort. | — | — | X% | X | X | X% |

#### 5. WACC Hesabı (Detaylı)
Tüm bileşenler + kaynaklar + tarihler

**⚠️ YENİ ZORUNLU:** 
- Ülke ERP → Hem Damodaran verisi hem kendi hesaplama göster
- Kredi notu → KAP'tan gerçek rating varsa onu kullan
- E/V, D/V → KAP bilanço tarihi ve MCap tarihi belirt
- Regression beta → Cross-check olarak göster

#### 6. Projeksiyon Tablosu (10 yıl)
(Mevcut format yeterli)

#### 7. Terminal Value
(Mevcut format yeterli)

#### 8. Equity Bridge
(Mevcut format yeterli)
**⚠️ YENİ:** Döviz kuru ve tarihini explicit belirt

#### 9. Sensitivity Analizi
2D tablo: WACC × Terminal Growth (5×5 = 25 senaryo)
+ Lambda sensitivity
+ Lease muamelesi sensitivity (varsa)

#### 10. Sanity Check'ler
- TV Ağırlığı: <%70 ✅ | %70-80 normal 📊 | %80-90 hassas ⚠️ | >%90 kritik 🔴
- Terminal g < WACC (her zaman)
- Terminal g ≤ Rf (uyarı eşiği)
- ROC terminal ≥ WACC (moat kontrolü)
- Fisher cross-check: TL hedef ≈ USD hedef × kur (sapma <%15)

#### 11. Damodaran Diagnostics (ZORUNLU)

17 sorunun tamamı → `references/diagnostics_17q.md`
Her soru TEK TEK cevaplanır. Cevaplar varsayımlarla çelişiyorsa → revizyon.

#### 12. "Neden Bu Değeri Biçtim?" (YENİ — ZORUNLU)
1-2 paragraf: Tüm hikayeyi birleştiren gerekçe
- Ana tez
- Piyasa fiyatıyla farkın nedeni
- En kritik 3 varsayım
- Yatırım kararı önerisi

#### 13. Riskler ve Disclaimer
(Mevcut format yeterli)

---

## ⚙️ Varsayım İsimlendirme Standardı

**KURAL:** Her kısaltma/sembol ilk kullanımda açıklanmalı. Tam sözlük → `references/term_glossary.md`

---

*Bu format İlker'in 2026-02-10 geri bildirimi sonrası oluşturulmuştur. Tüm DCF çalışmaları bu standarda uymalıdır.*
