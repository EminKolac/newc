# Bloomberg Data Extraction Guide for TVF Portfolio

## Overview
While Fintables provides comprehensive Turkish financial data, Bloomberg offers additional depth for institutional-grade analysis. This guide covers how to extract and format Bloomberg data to complement the Fintables dataset.

## When to Use Bloomberg vs Fintables

| Data Type | Fintables | Bloomberg | Recommendation |
|-----------|-----------|-----------|----------------|
| Quarterly financials (TRY) | ✅ Full | ✅ Full | Fintables (already loaded) |
| Quarterly financials (USD) | ✅ Full | ✅ Full | Fintables (already loaded) |
| FCF / Cash Flow | ✅ Full | ✅ Full | Fintables (already loaded) |
| Revenue segments | ❌ | ✅ | Bloomberg |
| Consensus estimates | Partial | ✅ Full | Bloomberg |
| EV/EBITDA multiples | ❌ | ✅ | Bloomberg |
| Peer comparison | ❌ | ✅ | Bloomberg |
| CPI / Inflation data | ❌ | ✅ | Bloomberg |

## Bloomberg Terminal Formulas

### 1. Historical Financial Data (BDH)

```excel
=BDH("THYAO TI Equity","SALES_REV_TURN","2017-01-01","2025-12-31","Period","Q","Currency","USD")
```

Key fields:
- `SALES_REV_TURN` = Revenue
- `EBITDA` = EBITDA
- `NET_INCOME` = Net Income
- `CF_FREE_CASH_FLOW` = Free Cash Flow
- `IS_OPER_INC` = Operating Income
- `TOT_DEBT_TO_TOT_EQY` = D/E Ratio

### 2. For Banks (HALKB, VAKBN)

```excel
=BDH("HALKB TI Equity","NET_INT_INC","2017-01-01","2025-12-31","Period","Q","Currency","USD")
```

Key fields:
- `NET_INT_INC` = Net Interest Income
- `NET_FEE_COMMISSION_INC` = Net Fee & Commission Income
- `PROVISION_FOR_LOAN_LOSS` = Provision for Loan Losses
- `NET_INCOME` = Net Income
- `RETURN_COM_EQY` = ROE

### 3. For Insurance (TURSG)

```excel
=BDH("TURSG TI Equity","GROSS_WRITTEN_PREMIUM","2024-06-01","2025-12-31","Period","Q","Currency","USD")
```

Key fields:
- `GROSS_WRITTEN_PREMIUM` = Gross Written Premiums
- `NET_EARNED_PREMIUM` = Net Earned Premiums
- `CLAIMS_INCURRED` = Claims Incurred
- `COMBINED_RATIO` = Combined Ratio
- `NET_INCOME` = Net Income

### 4. Price & FX Data

```excel
=BDH("USDTRY Curncy","PX_LAST","2017-01-01","2025-12-31","Period","Q")
```

### 5. Inflation Data (for Real Returns)

```excel
=BDH("TUCPIY Index","PX_LAST","2017-01-01","2025-12-31","Period","M")  ; Turkey CPI YoY
=BDH("CPI YOY Index","PX_LAST","2017-01-01","2025-12-31","Period","M")  ; US CPI YoY
```

## Data Format for Power BI Import

### Excel Template Structure
Each Bloomberg export should match the CSV templates in `/data/`:

**Format Rules:**
1. Date column: `Q_Date` as YYYY-MM-DD (last day of quarter)
2. Currency: All monetary values in original units (no thousands/millions scaling)
3. Ticker: Use BIST codes (THYAO, TCELL, etc.)
4. Separate columns for TRY and USD values

### Step-by-Step Bloomberg Export Process

1. **Open Bloomberg Terminal** → BDH function in Excel
2. **Set parameters:**
   - Securities: `THYAO TI Equity` (repeat for each ticker)
   - Start: `2017-01-01` (or ticker acquisition date)
   - End: `2025-12-31`
   - Period: `Q` (quarterly)
   - Currency: Run twice - once `TRY`, once `USD`
3. **Copy results** to the appropriate CSV template
4. **Validate** against Fintables data (they should match within rounding)

### Handling Bloomberg Data Quirks

- **Restatements**: Bloomberg may show restated values; Fintables shows as-reported. Use as-reported for consistency.
- **Currency conversion**: Bloomberg uses period-average FX for income statement, period-end for balance sheet. Fintables does the same.
- **Bank financials**: Bloomberg uses GICS classification which maps NII/Fee Income differently. Cross-check with Fintables `NET FAİZ GELİRİ VEYA GİDERİ`.
- **Null quarters**: Both sources may show null for Q4 when annual report hasn't been filed yet. This is normal - IFRS allows 3-month filing window.

## Inflation Table for Real Returns

Create a `dim_Inflation.csv` with:

```csv
Date,Turkey_CPI_YoY,Turkey_Cumul_CPI,US_CPI_YoY,US_Cumul_CPI
2017-03-31,11.29%,2.82%,2.38%,0.60%
2017-06-30,10.90%,5.68%,1.63%,1.01%
...
```

Source: TUIK for Turkey CPI, BLS for US CPI. Bloomberg tickers: `TUCPIY Index`, `CPI YOY Index`.

The `Real_Return_TRY` and `Real_Return_USD` DAX measures in `DAX_Measures.csv` reference this table.
