# TVF Portfolio Performance Tracker - Power BI Project

## Overview
Portfolio performance tracker for 11 Türkiye Varlık Fonu (TVF) holdings across 6 sectors.

## Holdings
| Ticker | Company | Sector | Ownership | Acquisition |
|--------|---------|--------|-----------|-------------|
| THYAO | Türk Hava Yolları | Airlines | 49.12% | 2017-02-03 (Devir) |
| HALKB | Halkbank | Banking | 91.49% | 2017-02-06 (Devir) |
| VAKBN | VakıfBank | Banking | 73.26% | 2020-05-29 (Satın Alma) |
| TCELL | Turkcell | Telecom | 26.20% | 2024-03-10 (Satın Alma) |
| TTKOM | Türk Telekom | Telecom | 55.00% | 2024-09-20 (Satın Alma) |
| TURSG | Türkiye Sigorta | Insurance | 81.00% | 2024-06-15 (Satın Alma) |
| TRENJ | TR Doğal Enerji | Energy | 62.12% | 2024-08-19 (Devir) |
| TRMET | TR Anadolu Metal | Mining | 52.25% | 2024-08-19 (Devir) |
| TRALT | Türk Altın İşletmeleri | Mining | 48.01% | 2024-08-19 (Devir) |
| KRDMD | Kardemir | Steel | 4.41% | 2022-12-05 (Satın Alma) |
| KAYSE | Kayseri Şeker | Food | 9.41% | 2017-02-03 (Devir) |

## Project Structure
```
powerbi-project/
├── data/
│   ├── dim_Tickers.csv          # Company master data + returns
│   ├── dim_FX_Rates.csv         # Quarterly USDTRY rates
│   ├── fact_Financials.csv      # Revenue, EBITDA, Net Profit, FCF
│   ├── fact_Returns.csv         # Quarterly price returns (TRY + USD)
│   ├── fact_Dividends.csv       # Dividend payments
│   ├── DAX_Measures.csv         # All DAX formulas for Power BI
│   └── Portfolio_CAGR.csv       # Weighted portfolio metrics
├── docs/
│   ├── BLOOMBERG_DATA_GUIDE.md  # How to extract Bloomberg data
│   └── POWERBI_DESIGN_SPEC.md   # 5-page dashboard design spec
└── README.md
```

## Power BI Pages
1. **Portfolio Overview** - NAV, weighted returns, treemap allocation, sector donut
2. **Performance Metrics** - Cumulative returns, heatmap, quarterly waterfall
3. **Financial Analysis** - Revenue/EBITDA/FCF with margin trends
4. **Dividends & IRR** - XIRR with dividends, payment timeline
5. **Company Profiles** - Card grid with deep-dive panel

## Data Sources
- **Fintables MCP**: Quarterly financials (TRY/USD), OHLCV prices, corporate info
- **Bloomberg**: Revenue segments, consensus estimates, EV/EBITDA, inflation data

## Filters (Pages 2-4)
- Currency: TRY Nominal | USD Nominal | TRY Real | USD Real
- Date range slicer
- Ticker multi-select
- Interest rate what-if parameter (yearly, inputable)

## Figma Designs
- [Data Model Diagram](https://www.figma.com/online-whiteboard/create-diagram/c884b986-ed05-4cbb-83e2-6ece7e7081f3)
- [Page 1 Overview Layout](https://www.figma.com/online-whiteboard/create-diagram/89c558ae-48ae-4a4c-b6ba-13dc2eedec05)
- [Pages 2-3 Performance & Financials](https://www.figma.com/online-whiteboard/create-diagram/b4a366a8-012d-44e1-a7dc-7bb15b286367)
- [Pages 4-5 Dividends & Company Info](https://www.figma.com/online-whiteboard/create-diagram/b1f2552b-b558-4807-a514-90197849ce8c)
