# Yaygın Hatalar ve Tuzaklar — Detaylı Açıklamalar

> **Kaynak:** THYAO, TBORG, NTHOL, CIMSA DCF süreçlerinde yapılan gerçek hatalar.
> **Her DCF'te bu listeyi gözden geçir.**

## 1. IAS 29 Tuzağı
TRY IAS 29 düzeltmeli rakamları spot kurla USD'ye çevirme → **YANLIŞ.** Hiperenflasyon muhasebesi parasal olmayan kalemleri şişirir; spot kurla bölünce sahte USD rakamlar çıkar. **Çözüm:** Şirketin kendi USD raporlamasını (investor relations / fact sheet) kullan.

## 2. Sentetik Kd Tuzağı
ICR hesabında KAP'taki brüt finansman giderine kur farkı zararları dahil → ICR düşer → sentetik rating çöker → Kd şişer. **Çözüm:** ICR'da sadece gerçek faiz giderini kullan. Sentetik rating yalnızca cross-check; birincil olarak şirketin gerçek S&P/Moody's/Fitch notunu baz al.

## 3. Kaynak Olmadan Rakam Kullanma
Borç, gelir, pay sayısı → **HER ZAMAN** BBB Finans veya KAP'tan doğrulanmış veri. Tahmin, hafızadan rakam, veya kaynaksız sayı YASAK.

## 4. S/C'yi Tahmin Etme, Hesapla
Sales/Capital = Gelir / Yatırılan Sermaye. Sezgisel tahmin yapma. Yanlış S/C, yeniden yatırım miktarını %30+ saptırabilir.

## 5. Rf'yi ABD Default Spread ile Düzelt
Damodaran yaklaşımı: ABD Aa1'e düşürüldü → Rf = ABD 10Y - ABD default spread (Aa1 → ~0.23%). Ham 10Y getirisi kullanma.

## 6. Baz Yıl Veri Karmaşası (IAS 29 Ülkeler) *(2026-02-11 — NTHOL kazanımı)*
İş Yatırım API ve KAP Özet **farklı IAS 29 bazları** kullanır:
- **İş Yatırım:** FY2024 yıllık raporundan → Q4-2024 fiyat endeksine restated
- **KAP Özet:** Q3-2025 interim raporundan → Q3-2025 fiyat endeksine restated
- 9M-2025 gibi aynı dönem verileri **aynı** (aynı GPI bazı)
- FY2024 gibi geçmiş dönem verileri **farklı** (~%25 fark)

**AMA:** USD'ye çevrildiğinde (her TL bazı kendi dönem kuruyla) **Currency Invariance** çalışır → USD sonuçlar ~aynı.

**ÇÖZÜM (Baz Yıl Seçim Kuralı):**
1. **USD DCF birincil → İş Yatırım TTM** kullan (tutarlı tek kaynak, en güncel)
2. **TTM hesabı:** 9M-son + (FY-önceki - 9M-önceki) → İş Yatırım'dan
3. **USD çevrim:** TTM TL / dönem sonu spot kur
4. **Cross-check:** KAP FY / FY ortalama kur → USD sonuç ~aynı olmalı
5. **Şirketin USD raporlaması varsa** → birincil kaynak o olur

## 7. Currency-Consistent Valuation *(2026-02-12 — NTHOL+CIMSA kazanımı)*

> **WACC, büyüme oranları ve terminal growth AYNI para birimi enflasyonunu yansıtmalı.**
> Fisher dönüşümü: (1+r_TL) = (1+r_USD) × (1+π_TL)/(1+π_US)
> Bu kural WACC, gelir büyümesi VE terminal growth için geçerlidir.
>
> **TL DCF yapıyorsan:**
> - Baz yıl: IAS 29 düzeltmeli son veriler (KAP'tan)
> - Büyüme: Nominal TL (%30-35 gibi, enflasyon + reel büyüme)
> - WACC: TL bazlı (%30+ — TL risksiz oran zaten ~%28-30)
> - Terminal g: Nominal TL (%15-20 — uzun vadeli enflasyon + reel)
> - CRP: TL Rf zaten ülke riskini içerir → CRP eklenmez
> - WACC-g spread: %8-15 arası makul
>
> **USD DCF yapıyorsan:**
> - Baz yıl: NOMİNAL (IAS 29 düzeltmeSİZ) TRY veriler ÷ dönem ortalaması kur
> - VEYA şirketin kendi USD raporlaması (investor relations)
> - NOMİNAL veri kaynağı: `bbb_kap.py --source isyatirim` (İş Yatırım API)
> - IAS 29 düzeltmeli TRY ÷ spot kur = YANLIŞ (distorted USD)
> - Büyüme: USD reel + USD enflasyonu (%3-8)
> - WACC: USD bazlı (%10-13)
> - Terminal g: %2-3 USD
>
> **Her DCF sonunda Fisher cross-check ZORUNLU:**
> TL hedef ≈ USD hedef olmalı. >%15 sapma varsa parametreleri gözden geçir.
>
> **NTHOL+CIMSA hatası:** TL WACC %36.8, TL büyüme %8-20 → spread %17-29 → TL DCF çöktü.
> Eğer büyüme Fisher-consistent %31.7 olsaydı spread %5.1 olurdu → makul sonuç.

## 8. Peer Ticker Bulunamazsa → ARAŞTIR *(2026-02-12 — CIMSA kazanımı)*

> Peer şirketin tickerı KAP'ta bulunamazsa "bulunamadı" deyip GEÇME.
> **Sorgula:** Birleşme mi yapıldı? İsim mi değişti? Delist mi oldu?
> Web araması yap: "{şirket adı} birleşme" veya "{ticker} delisted"
> **CIMSA örneği:** BOLU, ADANA, MRDIN "bulunamadı" → aslında hepsi OYAKC ile birleşti.
> Bu bilgi peer comparison'ı tamamen değiştirir.

## 9. CRP'de Tek Yaklaşıma Güvenme *(2026-02-11 — NTHOL kazanımı)*
CRP hesaplamada **her zaman iki yaklaşım** hesapla:
- **Rating bazlı:** Konservatif, stabil, rating güncellemelerini bekler
- **CDS bazlı:** Güncel piyasa algısı, volatil ama forward-looking
- **Blended önerilen:** %60 CDS + %40 Rating (piyasa ağırlıklı ama rating tabanıyla)
- Fark >100 bps ise her ikisini raporla ve seçimi gerekçelendir
- **NTHOL örneği:** Rating CRP %5.41, CDS CRP %4.04 → Blended %4.70 (WACC %11.73)

## 10. Fazlar Arası Tutarsızlık
Bir DCF'in farklı bölümlerinde aynı parametreler (WACC, Kd, β, Rf) kullanılmalı. Faz 2'de bir WACC, Faz 3'te başka bir WACC → kabul edilemez. Her parametre değişikliği açıkça gerekçelendirilmeli.

## 11. Piyasa Fiyatı Altında DCF → Red Flag
Model piyasa fiyatının altında değer üretiyorsa → muhafazakâr varsayımları sorgula. Ya model doğru (gerçekten overvalued) ya da varsayımlar aşırı sıkı.

## 12. β_U Seçimi: Nakit Düzeltmeli Kullan
Damodaran'da iki versiyon var: düzeltmeli ve düzeltmesiz. DCF'te nakit equity bridge'de ayrıca ekleniyor → β_U'da da nakit çıkarılmalı, yoksa çift sayım. **Nakit düzeltmeli (cash-corrected) β_U kullan.**

## 13. Capex Normalizasyonu *(2026-02-11 — MEMORY kazanımı)*
Gerçek capex/revenue oranı %25-50 olabilir, model %15 kullanıyorsa → FCFF şişer → değer şişer. **Çözüm:** Son 5 yıl capex/revenue oranını hesapla. Model'deki S/C'den implied reinvestment rate'i gerçek CapEx trendi ile karşılaştır. Ciddi fark varsa S/C'yi gradual normalization ile ayarla.

## 14. Terminal WACC Override Unutma *(2026-02-10 — TBORG kazanımı)*
Damodaran'ın default terminal WACC hesabı `Rf + Mature_ERP`'dir — bu Country Risk Premium'u sıfırlar. Türk firmaları için Türkiye'nin 10 yılda tamamen gelişmiş piyasa olma olasılığı düşük → terminal WACC override ZORUNLU. **Çözüm:** `Terminal_WACC = Rf + Mature_ERP + α × CRP` (α = 0.3-0.7, baz 0.5).
