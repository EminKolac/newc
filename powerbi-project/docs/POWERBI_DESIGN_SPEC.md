# Power BI Dashboard Design Specification
## TVF Portfolio Performance Tracker

---

## Data Model (Star Schema)

```
                    ┌──────────────┐
                    │ dim_Tickers  │
                    │──────────────│
                    │ Ticker (PK)  │
                    │ Company_Name │
                    │ Sector       │
                    │ Template_Type│
                    │ Acq_Date     │
                    │ Ownership_Pct│
                    │ CAGR_USD     │
                    │ IRR_USD      │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
     ┌────────▼───┐ ┌──────▼──────┐ ┌──▼──────────┐
     │fact_Returns│ │fact_Finance │ │fact_Dividend│
     │────────────│ │─────────────│ │─────────────│
     │Ticker (FK) │ │Ticker (FK)  │ │Ticker (FK)  │
     │Q_Date      │ │Q_Date       │ │Payment_Date │
     │Price_TRY   │ │Revenue_TRY  │ │Net_DPS_TRY  │
     │Price_USD   │ │Revenue_USD  │ │Net_DPS_USD  │
     │Cumul_Nom_* │ │EBITDA_*     │ │Post_Acq     │
     └────────────┘ │Net_Profit_* │ └─────────────┘
                    │FCF_*        │
                    └─────────────┘
```

**Relationships:**
- dim_Tickers[Ticker] → fact_Returns[Ticker] (1:M)
- dim_Tickers[Ticker] → fact_Financials[Ticker] (1:M)
- dim_Tickers[Ticker] → fact_Dividends[Ticker] (1:M)

---

## Page 1: PORTFOLIO OVERVIEW (Executive Dashboard)

### Layout
```
┌─────────────────────────────────────────────────────────┐
│  TVF PORTFOLIO TRACKER                    [Date] [FX]   │
├─────────┬─────────┬─────────┬─────────┬─────────────────┤
│ NAV     │ Wtd     │ Wtd     │ Wtd     │ # Holdings     │
│ $XXB    │ Return  │ CAGR    │ IRR     │ 11              │
│ KPI Card│ KPI Card│ KPI Card│ KPI Card│ KPI Card        │
├─────────┴─────────┴─────────┴─────────┴─────────────────┤
│                                                          │
│  [Treemap: Portfolio Allocation by Value]                │
│  Size = Your_Value_USD, Color = Total_Return_USD         │
│  Labels: Ticker + Return %                               │
│                                                          │
├──────────────────────────┬───────────────────────────────┤
│                          │                               │
│  [Bar Chart: Total       │  [Donut: Sector Allocation]   │
│   Return by Ticker]      │  Banking / Telecom / Airlines │
│  Sorted desc by return   │  Mining / Steel / Food / Ins  │
│  Color: green/red        │                               │
│                          │                               │
└──────────────────────────┴───────────────────────────────┘
```

### Filters (Page-level)
- Currency toggle: TRY Nominal | USD Nominal | TRY Real | USD Real
- Date range slicer
- Interest rate what-if parameter

---

## Page 2: PERFORMANCE METRICS (Quarterly Returns)

### Layout
```
┌─────────────────────────────────────────────────────────┐
│  QUARTERLY PERFORMANCE          [Ticker▼] [Currency▼]   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [Line Chart: Cumulative Return Over Time]               │
│  X = Q_Date, Y = Cumul_Nom_USD (or selected currency)   │
│  Multiple lines: one per ticker (or selected ticker)     │
│  Reference line at 0%                                    │
│                                                          │
├──────────────────────────┬───────────────────────────────┤
│                          │                               │
│  [Heatmap Table:         │  [Waterfall: Quarterly        │
│   Q Return by Ticker     │   Return Decomposition]       │
│   x Quarter]             │  Shows QoQ contribution       │
│  Color scale: red-green  │  by ticker to portfolio       │
│                          │                               │
├──────────────────────────┴───────────────────────────────┤
│                                                          │
│  [Table: Detailed quarterly data]                        │
│  Ticker | Q_Date | Price_TRY | Price_USD | Q_Return |    │
│  Cumul_Return | Sortable, filterable                     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Filters
- Ticker slicer (multi-select)
- Currency: TRY Nominal | USD Nominal | TRY Real | USD Real
- Date range
- Interest rate input (what-if parameter, yearly basis)

---

## Page 3: FINANCIAL ANALYSIS (Revenue / EBITDA / FCF)

### Layout
```
┌─────────────────────────────────────────────────────────┐
│  FINANCIAL METRICS              [Ticker▼] [Currency▼]   │
├─────────┬─────────┬─────────┬───────────────────────────┤
│ Revenue │ EBITDA  │ FCF     │ EBITDA Margin | Net Margin│
│ Latest Q│ Latest Q│ Latest Q│ Latest Q      | Latest Q  │
├─────────┴─────────┴─────────┴───────────────────────────┤
│                                                          │
│  [Combo Chart: Revenue (bars) + EBITDA Margin (line)]    │
│  X = Q_Date, Primary Y = Revenue, Secondary Y = Margin  │
│                                                          │
├──────────────────────────┬───────────────────────────────┤
│                          │                               │
│  [Stacked Bar:           │  [Line: FCF Over Time]        │
│   Revenue by Ticker      │  OpCF + Capex breakdown       │
│   per Quarter]           │  Net FCF line                 │
│                          │                               │
├──────────────────────────┴───────────────────────────────┤
│                                                          │
│  NOTE: Banks (HALKB, VAKBN) show NII + Fee Income        │
│  instead of Revenue. Insurance (TURSG) shows Earned      │
│  Premiums. These are NOT directly comparable to           │
│  standard Revenue.                                       │
│                                                          │
│  [Table: Full financial detail - all metrics, sortable]  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Template-Specific Handling
| Template | "Revenue" Column | "EBITDA" Column | "FCF" |
|----------|-----------------|-----------------|-------|
| Standard | Satış Gelirleri | FAVÖK | OpCF + Capex |
| Bank | NII + Fee Income | N/A (use Net Op Profit) | N/A |
| Insurance | Earned Premiums | N/A (use Net Profit) | N/A |

### Filters
- Ticker slicer
- Currency: TRY | USD
- Date range
- Template type filter (to separate bank/insurance views)

---

## Page 4: DIVIDENDS & IRR

### Layout
```
┌─────────────────────────────────────────────────────────┐
│  DIVIDENDS & IRR                          [Currency▼]   │
├─────────┬─────────┬─────────┬───────────────────────────┤
│ Total   │ Wtd IRR │ Div     │ Div Paying Tickers        │
│ Divs    │ (XIRR)  │ Yield   │ 5 of 11                   │
│ Received│         │ Avg     │                            │
├─────────┴─────────┴─────────┴───────────────────────────┤
│                                                          │
│  [Timeline: Dividend payments with amounts]              │
│  X = Payment_Date, Y = Net_DPS_USD, Color = Ticker      │
│                                                          │
├──────────────────────────┬───────────────────────────────┤
│                          │                               │
│  [Bar: IRR by Ticker]    │  [Table: XIRR Cashflows]     │
│  XIRR including divs     │  Date | Cashflow | Type      │
│  vs CAGR without divs    │  (Buy, Dividend, Current Val)│
│  Side-by-side comparison │                               │
│                          │                               │
└──────────────────────────┴───────────────────────────────┘
```

---

## Page 5: GENERAL INFORMATION

### Layout
```
┌─────────────────────────────────────────────────────────┐
│  COMPANY PROFILES                        [Ticker▼]      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [Card Grid: All 11 holdings]                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │ THYAO    │ │ HALKB    │ │ VAKBN    │ │ TCELL    │   │
│  │ Airlines │ │ Banking  │ │ Banking  │ │ Telecom  │   │
│  │ 49.12%   │ │ 91.49%   │ │ 73.26%   │ │ 26.20%   │   │
│  │ +209%    │ │ -67%     │ │ +20%     │ │ -6%      │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
│                                                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [Selected Ticker Detail Panel]                          │
│  Company name, sector, acq date, acq type, ownership    │
│  Acq price vs current price (TRY and USD)               │
│  Mini sparkline: price history                           │
│  Key financial snapshot: Latest Rev, EBITDA, Net Profit  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Global Filters (Applied to Pages 2-4)

| Filter | Type | Values |
|--------|------|--------|
| Ticker | Multi-select slicer | All 11 tickers |
| Currency | Radio button | TRY Nominal, USD Nominal, TRY Real, USD Real |
| Date Range | Date range slicer | Q1 2017 - Q4 2025 |
| Interest Rate | What-if parameter slider | 0% - 100% (yearly, step 0.5%) |

**Note on Real Returns:** Requires inflation data in `dim_Inflation` table. TRY Real uses Turkey CPI, USD Real uses US CPI. The DAX measures handle deflation automatically.

---

## Color Scheme

| Element | Color | Hex |
|---------|-------|-----|
| Positive return | Dark Green | #1B5E20 |
| Negative return | Dark Red | #B71C1C |
| THYAO (Airlines) | Blue | #1565C0 |
| Banks (HALKB, VAKBN) | Teal | #00695C |
| Telecom (TCELL, TTKOM) | Purple | #6A1B9A |
| Mining (TRALT, TRMET, TRENJ) | Amber | #E65100 |
| Steel (KRDMD) | Grey | #37474F |
| Food (KAYSE) | Green | #2E7D32 |
| Insurance (TURSG) | Indigo | #283593 |

---

## Data Refresh

- **Fintables data**: Quarterly (after Q results published, ~45 days post quarter-end)
- **Price data**: Can be refreshed daily if needed
- **Bloomberg data**: Update consensus estimates monthly
- **Inflation data**: Monthly from TUIK/BLS
