# BIST Portfolio Performance Tracker

Financial analysis toolkit for an 11-stock BIST (Borsa Istanbul) portfolio.

## What's Included

### Power BI Build Package
- `powerbi/themes/` — McKinsey-style Power BI theme (JSON)
- `powerbi/dax/` — 90+ DAX measures (What-If parameters, real value deflation, returns, portfolio metrics)
- `powerbi/power_query/` — Power Query M scripts for data transformation
- `powerbi/scripts/` — Python utilities (Bloomberg transform, BDH formula generator, data validator)
- `powerbi/sample_data/` — Sample CSVs for all dim/fact tables
- `powerbi/page_layouts.json` — Pixel-precise visual positions for 6 report pages
- `powerbi/BUILD_GUIDE.md` — Step-by-step build guide

### Reports
- `reports/bist_portfolio_v3.html` — Goldman Sachs-style HTML equity research report with live Fintables data

### MCP Server Configuration
- Fintables (BIST financial data)
- Yahoo Finance (global market data)
- Apify (Twitter/X, news, Google Trends scrapers)

## Portfolio Holdings

| Ticker | Company | Sector | Ownership |
|--------|---------|--------|----------|
| HALKB | Halk Bankasi | Banking | 91.49% |
| TURSG | Turkiye Sigorta | Insurance | 81.00% |
| VAKBN | Vakiflar Bankasi | Banking | 73.26% |
| TRENJ | Turkerler Enerji | Mining | 62.12% |
| TTKOM | Turk Telekomunikasyon | Telecom | 55.00% |
| TRMET | Turk Metal | Mining | 52.25% |
| THYAO | Turk Hava Yollari | Airlines | 49.12% |
| TRALT | Turk Altin | Mining | 48.01% |
| TCELL | Turkcell Iletisim | Telecom | 26.20% |
| KAYSE | Kayseri Seker | Food | 9.41% |
| KRDMD | Kardemir | Steel | 4.41% |

## Data Sources
- **Fintables MCP** — BIST financials, prices, balance sheets
- **Bloomberg Terminal** — FA exports, BDH price data
- **Yahoo Finance** — Global market context
