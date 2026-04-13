# DCF Değerleme Şablonu

## Şirket: [ŞİRKET ADI]
**Tarih:** [TARİH]  
**Para Birimi:** [TL / USD]  
**Yaklaşım:** [Nominal TL / Reel TL / USD]

---

## A. Temel Finansal Veriler

| Kalem | LTM | Önceki Yıl |
|-------|-----|------------|
| Hasılat | | |
| EBIT | | |
| Faiz Gideri | | |
| EBT | | |
| Vergi | | |
| BV Equity | | |
| BV Debt (ST+LT) | | |
| Nakit | | |
| İştirakler | | |
| Azınlık Payları | | |
| Pay Sayısı (M) | | |
| Güncel Fiyat | | |

## B. Türetilmiş Veriler

| Kalem | Değer |
|-------|-------|
| Invested Capital | |
| Sales/Capital | |
| Efektif Vergi Oranı | |
| EBIT Marjı | |
| ROC | |
| ICR | |
| D/E (piyasa) | |
| Market Cap | |

## C. WACC Bileşenleri

| Bileşen | Değer | Kaynak |
|---------|-------|--------|
| Rf | | TCMB 10Y DİBS |
| β (unlevered) | | Damodaran Global |
| β (levered) | | Hesaplama |
| Mature ERP | | Damodaran |
| Country ERP | | Damodaran |
| Lambda (λ) | | Gelir dağılımı |
| **Cost of Equity (Ke)** | | |
| Sentetik Rating | | ICR tablosu |
| Default Spread | | |
| **Cost of Debt (Kd pre-tax)** | | |
| E/V | | |
| D/V | | |
| **WACC** | | |

## D. Değer Sürücüleri (7 Input)

| # | Parametre | Değer | Referans |
|---|-----------|-------|----------|
| 1 | Gelir büyümesi (yıl 1) | | Tarihsel: __ |
| 2 | Gelir büyümesi (yıl 2-5) | | Sektör: __ |
| 3 | Hedef EBIT marjı | | Mevcut: __ |
| 4 | Marj yakınsama yılı | | |
| 5 | Sales/Capital (1-5) | | Mevcut: __ |
| 6 | Sales/Capital (6-10) | | |
| 7 | Terminal growth | | Rf: __ |

## E. 10 Yıllık Projeksiyon

| Yıl | g | Gelir | Marj | EBIT | Vergi | NOPAT | Reinv. | FCFF | WACC | PV(FCFF) |
|-----|---|-------|------|------|-------|-------|--------|------|------|----------|
| 0 | | | | | | | | | | |
| 1 | | | | | | | | | | |
| 2 | | | | | | | | | | |
| 3 | | | | | | | | | | |
| 4 | | | | | | | | | | |
| 5 | | | | | | | | | | |
| 6 | | | | | | | | | | |
| 7 | | | | | | | | | | |
| 8 | | | | | | | | | | |
| 9 | | | | | | | | | | |
| 10 | | | | | | | | | | |
| Term | | | | | | | | | | |

## F. Terminal Value

| Kalem | Değer |
|-------|-------|
| Terminal FCFF | |
| Terminal WACC | |
| Terminal Growth | |
| Terminal ROC | |
| Terminal Reinvestment Rate | |
| **Terminal Value** | |
| **PV(Terminal Value)** | |
| TV / Total Value (%) | |

## G. Equity Bridge

| Kalem | Değer |
|-------|-------|
| PV(10yr FCFF) | |
| PV(Terminal Value) | |
| **Operating Asset Value** | |
| × (1 - P_failure) | |
| - Debt | |
| - Minority Interests | |
| + Cash | |
| + Cross Holdings | |
| - Employee Options | |
| **= Equity Value** | |
| ÷ Shares | |
| **= Value per Share** | |
| Güncel Fiyat | |
| **Upside/Downside** | |

## H. Sensitivity Analizi

### WACC vs Terminal Growth

|  | g=__ | g=__ | g=__ | g=__ | g=__ |
|--|------|------|------|------|------|
| WACC=__ | | | | | |
| WACC=__ | | | | | |
| WACC=__ | | | | | |
| WACC=__ | | | | | |
| WACC=__ | | | | | |

## I. Sanity Check'ler

- [ ] TV Ağırlığı < %90
- [ ] Terminal g < WACC
- [ ] Terminal g ≤ Rf
- [ ] ROC terminal makul
- [ ] Implied market share yıl 10 makul
- [ ] Implied ROIC yıl 10 makul
- [ ] FCFF pozitif (en azından sonraki yıllarda)
