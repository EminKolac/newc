"""
Generate Bloomberg BDH formulas for all 11 BIST portfolio tickers.

Usage:
    python generate_bdh_formulas.py [output_file]
"""

import sys

TICKERS = {
    "TURSG": {"bbg": "TURSG TI Equity", "sector": "Insurance"},
    "TCELL": {"bbg": "TCELL TI Equity", "sector": "Telecom"},
    "TTKOM": {"bbg": "TTKOM TI Equity", "sector": "Telecom"},
    "HALKB": {"bbg": "HALKB TI Equity", "sector": "Banking"},
    "TRENJ": {"bbg": "TRENJ TI Equity", "sector": "Mining"},
    "TRMET": {"bbg": "TRMET TI Equity", "sector": "Mining"},
    "TRALT": {"bbg": "TRALT TI Equity", "sector": "Mining"},
    "THYAO": {"bbg": "THYAO TI Equity", "sector": "Airlines"},
    "VAKBN": {"bbg": "VAKBN TI Equity", "sector": "Banking"},
    "KRDMD": {"bbg": "KRDMD TI Equity", "sector": "Steel"},
    "KAYSE": {"bbg": "KAYSE TI Equity", "sector": "Food"},
}

START_DATE = "01/01/2015"
END_DATE = "12/31/2025"

PRICE_FIELDS = ["PX_LAST", "TOT_RETURN_INDEX_GROSS_DVDS", "MARKET_CAP", "CUR_MKT_CAP", "SHARES_OUT", "EQY_DVD_YLD_IND"]
FUNDAMENTAL_FIELDS = ["SALES_REV_TURN", "EBITDA", "NET_INCOME", "CF_FREE_CASH_FLOW", "TRAIL_12M_EPS", "BEST_EPS", "PE_RATIO", "PX_TO_BOOK_RATIO", "RETURN_COM_EQY"]


def main():
    output = sys.argv[1] if len(sys.argv) > 1 else "bloomberg_bdh_formulas.txt"
    with open(output, "w") as f:
        f.write(f"# Bloomberg BDH Formulas for BIST Portfolio\n")
        f.write(f"# {len(TICKERS)} tickers x {len(PRICE_FIELDS) + len(FUNDAMENTAL_FIELDS)} fields\n")
        f.write(f"# Date range: {START_DATE} to {END_DATE}\n\n")
        for ticker, info in TICKERS.items():
            bbg = info["bbg"]
            f.write(f"\n## {ticker} ({info['sector']})\n")
            for field in PRICE_FIELDS + FUNDAMENTAL_FIELDS:
                formula = f'=BDH("{bbg}","{field}","{START_DATE}","{END_DATE}","per=Q","Days=A","Fill=P")'
                f.write(f"  {field}: {formula}\n")
    count = len(TICKERS) * (len(PRICE_FIELDS) + len(FUNDAMENTAL_FIELDS))
    print(f"Generated {count} formulas for {len(TICKERS)} tickers -> {output}")


if __name__ == "__main__":
    main()
