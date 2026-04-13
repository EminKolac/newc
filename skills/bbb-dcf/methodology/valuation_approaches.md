# Üç Değerleme Yaklaşımı

## 1. DCF (İndirgenmiş Nakit Akışı)

**Temel Fikir:** Varlığın değeri = gelecekteki beklenen nakit akışlarının bugünkü değeri.

```
Value = Σ CFₜ / (1+r)ᵗ   (t = 1 → n)
```

**Ne zaman kullan:**
- Firma kararlı nakit akışı üretiyor veya üretecek
- Uzun vadeli bakış açısı
- İçsel değer (intrinsic value) aranıyor

**Güçlü yönler:** Piyasa hatasından bağımsız, temellere dayalı  
**Zayıf yönler:** Varsayımlara çok hassas, terminal value dominant olabilir

### Üç Yanılgı (Damodaran)
1. **"Değerleme objektiftir"** → Hayır. Tüm değerlemeler önyargılıdır.
2. **"İyi değerleme kesin sonuç verir"** → En az kesin olduğu durumda en değerlidir.
3. **"Ne kadar kantitatif o kadar iyi"** → Basit modeller daha iyi performans gösterir.

---

## 2. Göreceli (Relative) Değerleme

**Temel Fikir:** Benzer varlıkların piyasa fiyatlarına göre değerleme.

### Çarpanlar ve Ne Belirler

| Çarpan | Formül | Temel Sürücü |
|--------|--------|-------------|
| P/E | `Payout × (1+g) / (r-g)` | Büyüme, risk, ödeme oranı |
| P/BV | `ROE × Payout × (1+g) / (r-g)` | **ROE** kritik |
| EV/EBITDA | f(vergi, CapEx, büyüme, risk) | CapEx yoğunluğu |
| P/S | `Net Margin × Payout × (1+g) / (r-g)` | **Marj** kritik |

### Sektöre Göre Çarpan

| Sektör | Çarpan | Neden |
|--------|--------|-------|
| Döngüsel | PE (normalize) | Kazançlar döngüsel |
| Yüksek Büyüme/Kârsız | PS, EV/Sales | Gelecek marjlara bahis |
| Ağır Altyapı | EV/EBITDA | Yüksek amortisman |
| Finansal | PBV | BV piyasaya yakın |

### Uyarılar
- Sadece peers'a göre ucuz/pahalı dersiniz — grubun kendisi aşırı değerli olabilir
- "Benzer varlık" yoktur — farklılıkları kontrol et
- Regresyon ile temellere dayandır: `PE = a + b₁(Growth) + b₂(Risk) + b₃(Payout)`

---

## 3. Contingent Claim (Opsiyon Bazlı)

**Temel Fikir:** Opsiyon özellikleri taşıyan varlıkları opsiyon fiyatlama modelleriyle değerle.

### Ne Zaman Var?
1. Açıkça tanımlanmış dayanak varlık
2. Değeri öngörülemeyen şekilde değişiyor
3. Getiri sonlu sürede belirli olaya bağlı
4. **Münhasırlık (exclusivity) gerekli** — tam rekabette opsiyon değersiz

### Uygulamalar
- **Patent:** Biogen/Avonex örneği → BS modeli
- **Doğal kaynak:** Geliştirilmemiş petrol rezervi
- **Genişleme opsiyonu:** İlk yatırım NPV negatif ama genişleme opsiyonu pozitif
- **Özsermaye = Tasfiye Opsiyonu:** Firm value < borç olsa bile equity > 0

### Black-Scholes
```
Call = S×N(d₁) - K×e^(-rt)×N(d₂)
d₁ = [ln(S/K) + (r + σ²/2)t] / (σ√t)
d₂ = d₁ - σ√t
```

---

## Hangi Yaklaşımı Kullan?

| Durum | Birincil | İkincil |
|-------|---------|---------|
| Normal BIST şirketi | DCF | Relative (sanity check) |
| Karşılaştırılabilir çok | Relative | DCF (anchor) |
| Madencilik/Patent | DCF + Real Options | — |
| Holding | NAV (relative) | DCF (iştiraklerde) |
| Banka | FCFE DCF | P/BV relative |

**Kaya'nın varsayılan yaklaşımı:** DCF birincil, relative ikincil (sanity check).
