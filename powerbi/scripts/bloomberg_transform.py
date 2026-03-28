"""
Bloomberg FA Export -> Power BI Ready (Wide to Long)
Transforms Bloomberg Financial Analysis screen exports into fact tables.

Usage:
    python bloomberg_transform.py <ticker> <input_excel> <output_csv>

Example:
    python bloomberg_transform.py THYAO THYAO_FA.xlsx fact_financials_THYAO.csv
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path

FIELD_MAP = {
    "Revenue": "Revenue",
    "Sales/Revenue": "Revenue",
    "SALES_REV_TURN": "Revenue",
    "Net Premium Earned": "Net_Premium_Earned",
    "IS_TOT_NET_PREM_EARN": "Net_Premium_Earned",
    "Investment Income": "Investment_Income",
    "Operating Income": "Operating_Income",
    "Operating Income (Loss)": "Operating_Income",
    "Pretax Income": "Pretax_Income",
    "Pretax Income (Loss), GAAP": "Pretax_Income",
    "Net Income": "Net_Income",
    "Net Income, GAAP": "Net_Income",
    "EBITDA": "EBITDA",
    "Basic EPS": "EPS_Basic",
    "Basic EPS, GAAP": "EPS_Basic",
    "Diluted EPS": "EPS_Diluted",
    "Profit Margin": "Profit_Margin",
    "Loss Ratio (Non-Life)": "Loss_Ratio_NL",
}

CF_FIELD_MAP = {
    "Net Income": "Net_Income_CF",
    "Depreciation & Amortization": "Depreciation_Amort",
    "Cash From Operating Activities": "CF_Operating",
    "Cash From Investing Activities": "CF_Investing",
    "Cash from Financing Activities": "CF_Financing",
    "Capital Expenditures": "CapEx",
    "Free Cash Flow": "FCF",
    "Free Cash Flow to Firm": "FCF_to_Firm",
    "Free Cash Flow to Equity": "FCF_to_Equity",
    "Free Cash Flow Per Share": "FCF_per_Share",
    "Cash Flow Per Share": "CF_per_Share",
}


def parse_bbg_sheet(df, field_map):
    items = df.iloc[:, 0].values
    dates = df.iloc[0, 1:].values
    records = []
    for i, item in enumerate(items):
        if i == 0:
            continue
        item_str = str(item).strip()
        mapped = field_map.get(item_str)
        if not mapped:
            continue
        for j, date in enumerate(dates):
            val = df.iloc[i, j + 1]
            if pd.isna(val) or str(val).strip() in ('\u2014', '', 'nan'):
                val = None
            else:
                try:
                    val = float(val)
                except (ValueError, TypeError):
                    val = None
            if val is not None:
                records.append({"Q_Date": pd.to_datetime(date), "Field": mapped, "Value": val})
    return pd.DataFrame(records)


def wide_to_long(ticker, input_file):
    xls = pd.ExcelFile(input_file)
    results = []
    for sheet_name, currency in [("Cash Flow - Standardized", "TRY"), ("BBG Adjusted", "USD")]:
        if sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            parsed = parse_bbg_sheet(df, FIELD_MAP)
            parsed["Currency"] = currency
            parsed["Ticker"] = ticker
            results.append(parsed)
    for sheet_name, currency in [("Cash Flow - Standardized (2)", "TRY"), ("Cash Flow - Standardized (2 (3))", "USD")]:
        if sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            parsed = parse_bbg_sheet(df, CF_FIELD_MAP)
            parsed["Currency"] = currency
            parsed["Ticker"] = ticker
            results.append(parsed)
    if not results:
        print(f"No data found in {input_file}")
        return None
    combined = pd.concat(results, ignore_index=True)
    pivoted = combined.pivot_table(index=["Ticker", "Q_Date", "Currency"], columns="Field", values="Value", aggfunc="first").reset_index()
    pivoted["Q_Label"] = pivoted["Q_Date"].apply(lambda d: f"{d.year}-Q{(d.month - 1) // 3 + 1}")
    pivoted["Sort_Order"] = pivoted["Q_Date"].apply(lambda d: d.year * 10 + (d.month - 1) // 3 + 1)
    if "Revenue" in pivoted.columns and "EBITDA" in pivoted.columns:
        pivoted["EBITDA_Margin"] = pivoted["EBITDA"] / pivoted["Revenue"]
    if "Revenue" in pivoted.columns and "Net_Income" in pivoted.columns:
        pivoted["Net_Margin"] = pivoted["Net_Income"] / pivoted["Revenue"]
    return pivoted


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    ticker = sys.argv[1].upper()
    input_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else f"fact_financials_{ticker}.csv"
    result = wide_to_long(ticker, input_file)
    if result is not None:
        result.to_csv(output_file, index=False)
        print(f"Exported {len(result)} rows to {output_file}")


if __name__ == "__main__":
    main()
