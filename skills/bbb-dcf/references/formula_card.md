# Formül Referans Kartı

## 1. Temel DCF

```
Firma Değeri = Σ [FCFF_t / (1+WACC)^t] + TV / (1+WACC)^n
Özsermaye = Firma Değeri + Nakit - Borç - Opsiyonlar + İştirakler - Azınlık
```

## 2. Nakit Akışları

```
FCFF = EBIT(1-t) - Reinvestment
Reinvestment = ΔRevenue / Sales_to_Capital           [Damodaran yöntemi]
Reinvestment = Net CapEx + ΔWC                        [Geleneksel]
Net CapEx = CapEx - Depreciation
RR = Reinvestment / EBIT(1-t)
```

## 3. Terminal Value

```
TV = FCFF_{n+1} / (WACC - g)
TV = EBIT_{n+1}(1-t) × (1 - g/ROC) / (WACC - g)
RR_terminal = g / ROC
```

**KRİTİK:** ROC = WACC → büyüme değer yaratmaz. ROC > WACC = moat.

## 4. Cost of Equity (CAPM)

```
Ke = Rf + β × ERP                                     [Basit]
Ke = Rf + β × Mature_ERP + λ × Country_ERP            [Lambda]
```

## 5. Beta

```
β_L = β_U × [1 + (1-t) × (D/E)]
β_U = β_L / [1 + (1-t) × (D/E)]
Total β = Market β / Correlation                       [Özel firmalar]
```

## 6. WACC

```
WACC = Ke × (E/V) + Kd × (1-t) × (D/V)
V = E + D   [piyasa değerleri]
```

## 7. Cost of Debt

```
Kd = Rf + Country_Default_Spread + Company_Spread
ICR = EBIT / Interest_Expense → Synthetic Rating → Spread
MV_Debt = Interest × PV_annuity(n, Kd) + BV / (1+Kd)^n
```

## 8. Country Risk

```
Country_Default_Spread = TR_Bond - US_Bond (eşdeğer vade)
Country_ERP = Default_Spread × (σ_equity / σ_bond)
λ = Firma_yurtiçi_gelir% / Ortalama_yurtiçi%
```

## 9. Büyüme

```
g = RR × ROC                                          [Stabil ROC]
g = ROC_{t+1} × RR + (ROC_{t+1} - ROC_t) / ROC_t     [Değişen ROC]
ROC = EBIT(1-t) / Invested_Capital
IC = BV_Equity + BV_Debt - Cash
Revenue_Growth($) = Reinvestment × Sales/Capital       [Negatif kazançlı]
```

## 10. R&D Kapitalizasyonu

```
R&D_Asset = Σ (amortize_edilmemiş_geçmiş_R&D)
Adjusted_EBIT = EBIT + R&D_Expense - R&D_Amortization
FCFF değişmez! (EBIT↑ ve CapEx↑ birbirini dengeler)
```

## 11. Operating Lease (Pre-IFRS 16)

```
Lease_Debt = PV(gelecek_taahhütler, Kd_pretax)
Adjusted_EBIT ≈ EBIT + Kd_pretax × PV(Leases)
```

## 12. İflas Düzeltmesi

```
Adjusted_Value = DCF × P(hayatta) + Tasfiye × P(iflas)
```

## 13. Fisher Denklemi

```
(1 + nominal) = (1 + reel) × (1 + π)
reel = (1 + nominal) / (1 + π) - 1
```

## 13B. Reel WACC Dönüşümü (IAS 29 DCF)

```
Reel Kd = (1 + Nominal Kd) / (1 + π) − 1
Reel Ke = Reel Rf + β_L × Mature_ERP + λ × Country_ERP
Reel WACC = Reel Ke × (E/V) + Reel Kd × (1−t) × (D/V)

Cross-check: (1 + Nominal WACC) ≈ (1 + Reel WACC) × (1 + π)   sapma <%5
```

## 14. IAS 29 Reel FCFF

```
FCFF_reel = (EBIT_düzeltilmiş - Parasal_K/K) × (1-t)
          - Reel_Net_CapEx - ΔWC_düzeltilmiş
```

## 15. Holding NAV

```
NAV = Σ(İştirak_MV × pay%) + Net_Nakit - Holding_Borç
Holding_İndirimi = (NAV - Market_Cap) / NAV
```

## 16. Bankacılık FCFE

```
FCFE = Net_Gelir - ΔRegulatory_Equity
Equity_Value = Σ FCFE_t/(1+Ke)^t + FCFE_{n+1}/(Ke-g)
```

## 17. Relative Valuation

```
P/E = Payout × (1+g) / (r-g)
P/BV = ROE × Payout × (1+g) / (r-g)
EV/EBITDA = f(tax, reinvestment, growth, risk)
P/S = Net_Margin × Payout × (1+g) / (r-g)
```

## 18. Black-Scholes (Opsiyonlar)

```
Call = S×N(d₁) - K×e^(-rt)×N(d₂)
d₁ = [ln(S/K) + (r + σ²/2)t] / (σ√t)
d₂ = d₁ - σ√t
```

## 19. Dual-Track Kur

```
Forward = Spot × (1 + TR_π) / (1 + US_π)    [PPP-bazlı]
Sapma = |TL_Value_USD - USD_Value| / Average
  < %10 → Tutarlı ✅
  %10-25 → Uyar ⚠️
  > %25 → Debug 🔴
```

## 20. Sensitivity (2D Matrix)

```
Satır: Terminal WACC (±2%, 5 adım)
Sütun: Terminal growth (±1.5%, 5 adım)
Hücre: Value per share
→ 25 senaryo, değer aralığı
```
