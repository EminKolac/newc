"""
Data validation script for BIST Portfolio Power BI data.

Usage:
    python validate_data.py <excel_file>
"""

import sys
import pandas as pd
import numpy as np


def validate_dim_tickers(df):
    issues = []
    required_cols = ["Ticker", "Company_Name", "Sector", "Ownership_Pct"]
    for col in required_cols:
        if col not in df.columns:
            issues.append(f"Missing column: {col}")
    if "Ticker" in df.columns:
        if df["Ticker"].duplicated().any():
            dupes = df[df["Ticker"].duplicated()]["Ticker"].tolist()
            issues.append(f"Duplicate tickers: {dupes}")
        expected = {"TURSG", "TCELL", "TTKOM", "HALKB", "TRENJ", "TRMET", "TRALT", "THYAO", "VAKBN", "KRDMD", "KAYSE"}
        missing = expected - set(df["Ticker"].values)
        if missing:
            issues.append(f"Missing tickers: {missing}")
    if "Ownership_Pct" in df.columns:
        invalid = df[(df["Ownership_Pct"] <= 0) | (df["Ownership_Pct"] > 1)]
        if len(invalid) > 0:
            issues.append(f"Ownership_Pct outside 0-1 range for: {invalid['Ticker'].tolist()}")
    return issues


def validate_fact_returns(df):
    issues = []
    if "Q_Date" in df.columns and not pd.api.types.is_datetime64_any_dtype(df["Q_Date"]):
        issues.append("Q_Date is not datetime type")
    if "Q_Label" in df.columns:
        invalid = df[~df["Q_Label"].str.match(r"^\d{4}-Q[1-4]$", na=False)]
        if len(invalid) > 0:
            issues.append(f"Invalid Q_Label format: {invalid['Q_Label'].unique()[:5]}")
    return issues


def validate_fact_financials(df):
    issues = []
    if "Revenue_USD" in df.columns:
        negatives = df[df["Revenue_USD"] < 0]
        if len(negatives) > 0:
            issues.append(f"Negative Revenue_USD: {len(negatives)} rows")
    return issues


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    file_path = sys.argv[1]
    xls = pd.ExcelFile(file_path)
    print(f"Validating: {file_path}")
    print(f"Sheets found: {xls.sheet_names}\n")
    total_issues = 0
    for sheet, validator in [("dim_Tickers", validate_dim_tickers), ("fact_Returns", validate_fact_returns), ("fact_Financials", validate_fact_financials)]:
        if sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)
            issues = validator(df)
            status = "PASS" if not issues else "FAIL"
            print(f"[{status}] {sheet} ({len(df)} rows)")
            for issue in issues:
                print(f"  - {issue}")
            total_issues += len(issues)
        else:
            print(f"[SKIP] {sheet} -- not found")
    print(f"\nTotal issues: {total_issues}")
    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
