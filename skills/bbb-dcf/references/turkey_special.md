# Türkiye Özel Konular — Detaylı Referans

## IAS 29 Hiperenflasyon (2022+)
- BIST tabloları enflasyon düzeltmeli (Yİ-ÜFE ile)
- **Parasal Kazanç/Kayıp → EBIT'ten ÇIKAR** (operasyonel değil!)
- İki yaklaşım: Reel TL DCF veya Nominal TL DCF
- **ASLA nominal Rf + reel büyüme karıştırma!**
- Detay: `methodology/turkey_adjustments.md`

## Country Risk Premium (CRP — Ülke Risk Primi) — FORMÜLDEN HESAPLA

**⚠️ CRP Damodaran'dan hazır alınmaz, formülle hesaplanır.** Damodaran sadece cross-check.

### CRP Hesaplama Formülü
```
CRP = Default_Spread × (σ_Equity / σ_Bond)
```
- **σ_Equity / σ_Bond** = Damodaran'ın Ocak 2026 verisinden: **1.5234** (ctryprem.xlsx)
- Bu çarpan yılda 1 kez güncellenir (Ocak)

### Default Spread Kaynağı — İKİ Yaklaşım (İkisini de hesapla)

**Yaklaşım A — Rating Bazlı (Konservatif):**
1. Ülkenin Moody's/S&P notunu **güncel online kaynaktan** doğrula (Damodaran stale olabilir!)
2. Damodaran "Default Spreads for Ratings" tablosundan ilgili spread'i al
3. CRP = Spread × 1.5234

**Yaklaşım B — CDS Bazlı (Piyasa, Daha Güncel):**
1. Ülkenin 5Y sovereign CDS'ini çek (MacroMicro, CBONDS, Trading Economics)
2. CRP = CDS × 1.5234
3. CDS olmayan ülkeler → Rating yaklaşımına geri dön

**Karar:** İki sonucu karşılaştır:
- CDS < Rating spread → Piyasa daha iyimser (reform/upgrade beklentisi)
- CDS > Rating spread → Piyasa daha kötümser (downgrade riski)
- **Fark >100 bps ise her ikisini de raporla ve seçimi gerekçelendir**

### Çok Ülkeli Şirketler — Revenue-Weighted CRP
```
CRP_weighted = Σ (Ülke_i CRP × Ülke_i Gelir Payı)
```
**Gelir payı bilinmiyorsa:** Asset-weighted proxy kullan (oda sayısı, tesis m², çalışan sayısı)

### Segment Kırılımı Yoksa → Asset-Weighted Proxy
Şirket segment gelir dağılımı vermemişse, şu sırayla dene:
1. **Dipnot 5 (TFRS 8):** "Bölümlere Göre Raporlama" — en güvenilir
2. **Asset-weighted:** Ülke bazında tesis sayısı/kapasitesi/m² oranları
3. **Çalışan-weighted:** Ülke bazında çalışan sayıları
4. **Yönetim beyanları:** Faaliyet raporundaki coğrafi referanslar
5. **Son çare:** Sektör normlarından tahmin + [TAHMİNİ] etiketi

### KKTC Gibi Tanınmamış Bölgeler — Sentetik CRP
```
CRP_sentetik = Bağlı_Ülke_CRP × Amplifier
```
- **Amplifier faktörleri:** Uluslararası tanınmama (+10-20%), ambargo/izolasyon (+10-20%), siyasi bağımlılık (+5-10%)
- **KKTC amplifier:** ×1.30 (tanınmama + Türkiye bağımlılığı + ambargo)
- **Terminal WACC:** Override ŞART! Aksi halde CRP sıfırlanır

## Model Seçimi (FX bazlı)

| FX Gelir | Model |
|----------|-------|
| >%70 USD/EUR | USD DCF birincil |
| <%30 | Reel TL birincil |
| %30-70 | Dual-track zorunlu |

## Holding İndirimi (Konglomera İskontosu) — FORMÜLDEN HESAPLA

**Baz indirim + ek faktörler yaklaşımı:**

| Faktör | Aralık | Açıklama |
|--------|--------|----------|
| **BIST holding baz indirimi** | %20-25 | Türk holdinglerin tarihsel ortalama iskontosu (SAHOL, KCHOL, TKFEN referans) |
| **Düşük HAO (Halka Açıklık Oranı)** | +%3-8 | HAO <%30 → likidite riski, çıkış zorluğu |
| **Aile/tek kişi kontrolü** | +%3-5 | >%50 kontrol → azınlık haklarına potansiyel risk |
| **Zayıf IR (Yatırımcı İlişkileri)** | +%2-3 | IR sayfası yok/güncellenmemiş, sunum yok |
| **Ülke/bölge riski** | +%2-5 | KKTC tanınmama, siyasi bağımlılık |
| **Sektör riski** | +%2-3 | ESG riski (kumar, tütün vb.), regülasyon belirsizliği |
| **A grubu imtiyaz** | +%2-3 | Küçük pay ile tam kontrol → azınlık dezavantajı |

**Hesaplama:** Baz + ilgili ek faktörlerin toplamı
**SOTP cross-check:** NAV × (1 - İndirim %) = SOTP Değer

## Time-Varying WACC (Dezenflasyon Ortamı) *(2026-02-10 — TBORG kazanımı)*

**Ne zaman kullan:** Beklenen enflasyon yıllar içinde >10pp değişecekse veya sabit WACC ile terminal ROC < WACC çıkıyorsa.

**Prosedür:**
```
Her yıl t için ayrı WACC hesapla:
  1. TCMB enflasyon beklenti anketinden yıllık enflasyon yolu oluştur
  2. Rf_t = Reel Rf (~%5) + Beklenen Enflasyon_t
  3. Ke_t = Rf_t + β × ERP + CRP
  4. WACC_t = Ke_t × (E/V) + Kd_t × (1-t_tax) × (D/V)
  5. Terminal WACC: Normalize enflasyon (%5) + Reel Rf (%5) + β×ERP

Kümülatif iskonto faktörü:
  DF_t = DF_{t-1} / (1 + WACC_t)
```

**Dezenflasyon şablonu:**

| Dönem | Enflasyon | Rf (DİBS) | Örnek WACC |
|-------|-----------|-----------|------------|
| Y1 | %25 | %28 | ~%30 |
| Y2-3 | %14-18 | %19-23 | ~%21-25 |
| Y4-5 | %10 | %15 | ~%17 |
| Y8-10 | %6 | %11 | ~%13 |
| Terminal | %5 | %10 | ~%12 |

**Fisher tutarlılık:** Her yılda `Nominal Büyüme ≈ Reel Büyüme + Enflasyon`. Terminal'de `g < Rf` (ZORUNLU).

## HAO / Likidite İndirimi *(2026-02-10 — TBORG kazanımı)*

> *"The discount for illiquidity should be applied to the estimated value, not built into the discount rate."* — Damodaran

**Uygulama:** Equity bridge'de **ayrı satır**. WACC'a EKLENMİYOR.

**Kalite matrisi:**

| Ortak Kalitesi | İndirim |
|---------------|---------|
| Güçlü ortak (Carlsberg, Coca-Cola) | %5-10 |
| Zayıf/dağınık ortaklık | %15-25 |
| Sorunlu şirket | %25-35 |

**Kurallar:**
- Düşük HAO → sektör beta tercih et (regression beta şişer — thin trading bias)
- Squeeze-out riski (ana ortak %95+ → zorunlu çağrı olasılığı)
- Endeks dışı → kurumsal yatırımcı erişimi yok

## Management Guidance Filtresi *(2026-02-10 — TBORG kazanımı)*

> **İlker talimatı:** Şirketlerin kendi beklentilerine çok ciddi güvenmemek.

**3 seviyeli filtre:**
1. **Ham Input** → Şirketin söylediği (doğrudan kullanma)
2. **Çapraz Kontrol** → Track record, sektör benchmark, makro tutarlılık, CapEx-büyüme uyumu
3. **Kalibre Edilmiş Input** → Güven skoruna göre ağırlıklandırılmış

**Güven skoru** (5 kriter): Track record, spesifiklik, teşvik uyumu, denetim kalitesi, sektör dinamiği

**Ağırlıklandırma:**
- Yüksek güven → %50 guidance / %50 bağımsız
- Orta güven → %40 / %60
- Düşük güven → %20 / %80

## IAS 29 + Nominal DCF Tutarlılık Kuralı *(2026-02-10 — TBORG kazanımı)*
```
KURAL: Son çeyrekte IAS 29 düzeltme katsayısı ≈ 1.0 → nominal baz olarak kullanılabilir.
D&A farkına DİKKAT: IAS 29 EBIT < Nominal EBIT (şişmiş amortisman nedeniyle).
Nominal DCF yapıyorsan → nominal marjları baz al, IAS 29'u cross-check olarak kullan.
```

## ERP ve CRP Hesaplama Adımları

### ERP Hesaplama (Doğrulama)
```
Adım 1: S&P 500 Implied ERP → Damodaran Ocak güncellemesi (substack/blog)
Adım 2: ABD Default Spread → Moody's ABD notu (Aa1 ise 0.23%)
Adım 3: Olgun Piyasa ERP = Implied ERP - ABD Default Spread
Örnek (Ocak 2026): 4.46% - 0.23% = 4.23%
```
**Doğrulama:** Damodaran'ın son blog postunu (`aswathdamodaran.substack.com`) kontrol et

### CRP Hesaplama (Elle)
```
Adım 1: Default Spread belirle (İKİ yaklaşım):
  A) Rating-based: Moody's nota → Damodaran spread tablosu
  B) CDS-based: 5Y sovereign CDS (MacroMicro, CBONDS)

Adım 2: σ_E/σ_B çarpanını al
  - Damodaran ctryprem.xlsx → Ocak 2026: 1.5234
  - VEYA: CRP_mevcut / Default_Spread_mevcut oranından hesapla

Adım 3: CRP = Default_Spread × σ_E/σ_B

Adım 4: Çok ülkeliyse → Revenue-weighted CRP
```

### Kroll (Duff & Phelps) Cross-Check
- Kroll ERP önerisi: `kroll.com/en/reports/cost-of-capital/`
- Genelde Damodaran'dan farklı (Kroll daha muhafazakâr)
- Fark >1 puan ise raporla

> **⚠️ Güncel ERP/CRP değerleri → `references/country_erp.md` (kanonik kaynak).**
> Bu dosyadaki sayılar formül gösterimi ve hesaplama adımları içindir.
