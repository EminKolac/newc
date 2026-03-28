# BIST Portfolio Performance Tracker — V3 Build Guide

## McKinsey Design · Acquisition-Date Returns · Dual Currency

### Prerequisites
- Power BI Desktop (latest)
- BIST_Portfolio_V3.xlsx with all fact/dim sheets
- Bloomberg Terminal (for additional data exports)

---

## Phase 1: Import Data

1. **Get Data → Excel** → Select `BIST_Portfolio_V3.xlsx`
2. Load these sheets: `dim_Tickers`, `fact_Returns`, `fact_Financials`, `fact_Dividends`
3. Also import `BIST_CAGR_IRR.xlsx → OwnWeighted_Revenue_Stacked` for Page 6
4. Skip: `PowerBI_Setup`, `fact_Transactions`

## Phase 2: Data Model

### Relationships (Star Schema)
```
dim_Tickers[Ticker] → 1:N → fact_Returns[Ticker]
dim_Tickers[Ticker] → 1:N → fact_Financials[Ticker]
dim_Tickers[Ticker] → 1:N → fact_Dividends[Ticker]
```

### CRITICAL: Sort Q_Label
- Data view → `fact_Returns` → click `Q_Label` → Column tools → **Sort by Column → Sort_Order**
- Repeat for `fact_Financials`

### Create Disconnected Tables
```
NominalReal = DATATABLE("Value", STRING, {{"Nominal"}, {"Real"}})
```

## Phase 3: What-If Parameters

1. Modeling → New Parameter → `TRY Discount Rate`
   - Min: 0, Max: 1, Increment: 0.005, Default: 0.45
2. Modeling → New Parameter → `USD Discount Rate`
   - Min: 0, Max: 0.5, Increment: 0.005, Default: 0.055

## Phase 4: DAX Measures

Import all measures from `powerbi/dax/all_measures.dax`

## Phase 5: Apply Theme

1. View → Themes → Browse for themes
2. Select `powerbi/themes/bist_mckinsey_theme.json`

## Phase 6: Build Pages

See `powerbi/page_layouts.json` for exact visual positions.

## Phase 7: Sync Slicers

View → Sync Slicers → Enable across all 6 pages

## Phase 8: Conditional Formatting

- Return columns: green (#2D8C3C) for positive, red (#E4002B) for negative
- CAGR columns: same green/red
- Data bars on weight columns

---

## Color Palette (McKinsey)

| Element | Hex | Usage |
|---------|-----|-------|
| Navy | #051C2C | Headers, primary bars |
| Electric Blue | #2251FF | Secondary accent |
| Teal | #009CDC | Tertiary accent |
| Green | #2D8C3C | Positive values |
| Red | #E4002B | Negative values |
| Yellow | #FFD100 | Warnings, rate inputs |
| Dark Gray | #333333 | Body text |
| Mid Gray | #58595B | Muted labels |
| Light Gray | #F2F2F2 | Backgrounds |
