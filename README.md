# BIST Portfolio Performance Tracker

## Overview
11-stock BIST (Borsa Istanbul) portfolio tracker with:
- Acquisition-date returns (USD & TRY)
- Ownership-weighted metrics
- McKinsey design language
- Power BI integration guide

## Portfolio Holdings

| Ticker | Company | Sector | Ownership % |
|--------|---------|--------|-------------|
| TURSG | Turkiye Sigorta | Insurance | 81.00% |
| TCELL | Turkcell | Telecom | 26.20% |
| TTKOM | Turk Telekomunikasyon | Telecom | 55.00% |
| HALKB | Halk Bankasi | Banking | 91.49% |
| TRENJ | Turkerler Enerji | Energy | 62.12% |
| TRMET | Turk Metal | Metals | 52.25% |
| TRALT | Turk Altin | Metals | 48.01% |
| THYAO | Turk Hava Yollari | Airlines | 49.12% |
| VAKBN | Vakiflar Bankasi | Banking | 73.26% |
| KRDMD | Kardemir Demir Celik | Steel | 4.41% |
| KAYSE | Kayseri Seker Fabrikasi | Food | 9.41% |

## Key Metrics
- **Portfolio NAV:** $23.47B
- **Portfolio CAGR USD:** +1.26%
- **Weighted Return USD:** +43.3%
- **Best Performer:** THYAO +320% USD (17.5% CAGR)
- **Worst Performer:** HALKB -72% USD (-13.3% CAGR)

## Installed Tools

### Claude Code Plugins
- `financial-analysis` (core) — shared modeling tools, data connectors
- `investment-banking` — CIMs, teasers, buyer lists, merger models
- `equity-research` — earnings reports, coverage initiations, thesis tracking
- `private-equity` — deal sourcing, diligence, IC memos, portfolio KPIs
- `wealth-management` — client meeting prep, financial planning, rebalancing

### MCP Servers
- **Fintables** — Turkish financial data (`https://evo.fintables.com/mcp`)
- **Yahoo Finance** — Global market data via `mcp-yahoo-finance`
- **Apify** — Twitter scraping, Google News, Google Trends, web scraping

### Python Packages
- **TradingAgents v0.2.2** — Multi-agent LLM trading framework
- **TradingAgents-BIST** — BIST-customized fork

## Files
- `reports/bist_portfolio_v2.html` — Interactive 6-page portfolio dashboard
- `scripts/build_portfolio_v3.py` — Excel workbook builder (V3 with FCF & IRR)
- `.claude/settings.local.json` — MCP server configuration

## Setup
```bash
# Install dependencies
pip install openpyxl yfinance

# Build the Excel workbook
python scripts/build_portfolio_v3.py

# Run TradingAgents analysis
tradingagents
```
