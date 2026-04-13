#!/usr/bin/env python3
"""
BBB Finans — Yahoo Finance CLI
Yurt dışı peer verileri için yfinance wrapper.
BIST verileri için bu script DEĞİL → bbb_financials.py / bbb_kap.py kullanın.

Kullanım:
    python3 bbb_yfinance.py quote LVS
    python3 bbb_yfinance.py fundamentals WYNN
    python3 bbb_yfinance.py compare LVS,WYNN,MGM,GENTING.KL
    python3 bbb_yfinance.py earnings LVS
    python3 bbb_yfinance.py comps LVS,WYNN,MGM --metrics ev_ebitda,pe,roe,gross_margin
"""

import sys
import argparse
import json
from typing import List, Dict, Any, Optional

try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False

# ── Helpers ──────────────────────────────────────────────────────────────────

def fmt_num(val, decimals=2, prefix="", suffix=""):
    """Sayıyı okunabilir formata çevir."""
    if val is None:
        return "N/A"
    if isinstance(val, str):
        return val
    if abs(val) >= 1e12:
        return f"{prefix}{val/1e12:.{decimals}f}T{suffix}"
    if abs(val) >= 1e9:
        return f"{prefix}{val/1e9:.{decimals}f}B{suffix}"
    if abs(val) >= 1e6:
        return f"{prefix}{val/1e6:.{decimals}f}M{suffix}"
    return f"{prefix}{val:,.{decimals}f}{suffix}"


def fmt_pct(val):
    """Yüzdeyi formatla."""
    if val is None:
        return "N/A"
    return f"{val*100:.1f}%"


def safe_get(info: dict, key: str, default=None):
    """info dict'ten güvenli değer al."""
    val = info.get(key, default)
    if val is None or val == "":
        return default
    return val


# ── Quote ────────────────────────────────────────────────────────────────────

def cmd_quote(ticker: str):
    """Detaylı fiyat + temel metrikler."""
    t = yf.Ticker(ticker)
    info = t.info

    print(f"{'='*60}")
    print(f"  {ticker} — {safe_get(info, 'longName', safe_get(info, 'shortName', ticker))}")
    print(f"  Sektör: {safe_get(info, 'sector', 'N/A')} | Endüstri: {safe_get(info, 'industry', 'N/A')}")
    print(f"  Ülke: {safe_get(info, 'country', 'N/A')} | Borsa: {safe_get(info, 'exchange', 'N/A')}")
    print(f"{'='*60}")
    print()

    price = safe_get(info, 'currentPrice') or safe_get(info, 'regularMarketPrice')
    prev = safe_get(info, 'previousClose')
    change = None
    if price and prev:
        change = (price - prev) / prev * 100

    print(f"  Fiyat:           {fmt_num(price)}")
    if change is not None:
        sign = "+" if change >= 0 else ""
        print(f"  Günlük Değişim:  {sign}{change:.2f}%")
    print(f"  52W Yüksek:      {fmt_num(safe_get(info, 'fiftyTwoWeekHigh'))}")
    print(f"  52W Düşük:       {fmt_num(safe_get(info, 'fiftyTwoWeekLow'))}")
    print()
    print(f"  Piyasa Değeri:   {fmt_num(safe_get(info, 'marketCap'))}")
    print(f"  Firma Değeri:    {fmt_num(safe_get(info, 'enterpriseValue'))}")
    print()
    print(f"  F/K (Trailing):  {fmt_num(safe_get(info, 'trailingPE'))}")
    print(f"  F/K (Forward):   {fmt_num(safe_get(info, 'forwardPE'))}")
    print(f"  EV/EBITDA:       {fmt_num(safe_get(info, 'enterpriseToEbitda'))}")
    print(f"  EV/Revenue:      {fmt_num(safe_get(info, 'enterpriseToRevenue'))}")
    print(f"  P/B:             {fmt_num(safe_get(info, 'priceToBook'))}")
    print()
    print(f"  Brüt Marj:       {fmt_pct(safe_get(info, 'grossMargins'))}")
    print(f"  EBITDA Marjı:    {fmt_pct(safe_get(info, 'ebitdaMargins'))}")
    print(f"  Kâr Marjı:       {fmt_pct(safe_get(info, 'profitMargins'))}")
    print(f"  ROE:             {fmt_pct(safe_get(info, 'returnOnEquity'))}")
    print(f"  ROA:             {fmt_pct(safe_get(info, 'returnOnAssets'))}")
    print()
    div_yield = safe_get(info, 'dividendYield')
    print(f"  Temettü Verimi:  {fmt_pct(div_yield) if div_yield else 'N/A'}")
    print(f"  Beta:            {fmt_num(safe_get(info, 'beta'))}")
    print()

    # Analist hedefleri
    target_mean = safe_get(info, 'targetMeanPrice')
    target_low = safe_get(info, 'targetLowPrice')
    target_high = safe_get(info, 'targetHighPrice')
    if target_mean:
        upside = ((target_mean - price) / price * 100) if price else None
        print(f"  Analist Hedef:   {fmt_num(target_low)} — {fmt_num(target_mean)} — {fmt_num(target_high)}")
        if upside is not None:
            print(f"  Potansiyel:      {'+' if upside >= 0 else ''}{upside:.1f}%")
        rec = safe_get(info, 'recommendationKey', 'N/A')
        num_analysts = safe_get(info, 'numberOfAnalystOpinions', 'N/A')
        print(f"  Tavsiye:         {rec} ({num_analysts} analist)")


# ── Fundamentals ─────────────────────────────────────────────────────────────

def cmd_fundamentals(ticker: str):
    """Temel finansal tablolar özeti."""
    t = yf.Ticker(ticker)
    info = t.info

    print(f"{'='*60}")
    print(f"  {ticker} — Temel Göstergeler")
    print(f"{'='*60}")
    print()

    rows = [
        ("Piyasa Değeri", fmt_num(safe_get(info, 'marketCap'))),
        ("Firma Değeri (EV)", fmt_num(safe_get(info, 'enterpriseValue'))),
        ("Gelir (TTM)", fmt_num(safe_get(info, 'totalRevenue'))),
        ("EBITDA (TTM)", fmt_num(safe_get(info, 'ebitda'))),
        ("Net Kâr (TTM)", fmt_num(safe_get(info, 'netIncomeToCommon'))),
        ("SNA (TTM)", fmt_num(safe_get(info, 'freeCashflow'))),
        ("", ""),
        ("Brüt Marj", fmt_pct(safe_get(info, 'grossMargins'))),
        ("EBITDA Marjı", fmt_pct(safe_get(info, 'ebitdaMargins'))),
        ("Op. Marjı", fmt_pct(safe_get(info, 'operatingMargins'))),
        ("Kâr Marjı", fmt_pct(safe_get(info, 'profitMargins'))),
        ("", ""),
        ("ROE", fmt_pct(safe_get(info, 'returnOnEquity'))),
        ("ROA", fmt_pct(safe_get(info, 'returnOnAssets'))),
        ("Gelir Büyümesi", fmt_pct(safe_get(info, 'revenueGrowth'))),
        ("Kazanç Büyümesi", fmt_pct(safe_get(info, 'earningsGrowth'))),
        ("", ""),
        ("F/K (Trailing)", fmt_num(safe_get(info, 'trailingPE'))),
        ("F/K (Forward)", fmt_num(safe_get(info, 'forwardPE'))),
        ("EV/EBITDA", fmt_num(safe_get(info, 'enterpriseToEbitda'))),
        ("EV/Revenue", fmt_num(safe_get(info, 'enterpriseToRevenue'))),
        ("P/B", fmt_num(safe_get(info, 'priceToBook'))),
        ("P/FCF", fmt_num(safe_get(info, 'priceToFreeCashflows') if safe_get(info, 'priceToFreeCashflows') else None)),
        ("", ""),
        ("Net Borç", fmt_num(safe_get(info, 'totalDebt', 0) - safe_get(info, 'totalCash', 0)) if safe_get(info, 'totalDebt') else "N/A"),
        ("Toplam Borç", fmt_num(safe_get(info, 'totalDebt'))),
        ("Nakit", fmt_num(safe_get(info, 'totalCash'))),
        ("Borç/Özsermaye", fmt_num(safe_get(info, 'debtToEquity'))),
    ]

    for label, val in rows:
        if label == "":
            print()
        else:
            print(f"  {label:<22} {val}")


# ── Compare (Peer Comps Tablosu) ─────────────────────────────────────────────

def cmd_compare(tickers: List[str]):
    """Peer karşılaştırma tablosu — equity-analyst comps workflow'u için."""
    print(f"{'='*100}")
    print(f"  Peer Karşılaştırma — {', '.join(tickers)}")
    print(f"{'='*100}")
    print()

    header = f"  {'Ticker':<12} {'PD':>10} {'EV':>10} {'EV/EBITDA':>10} {'F/K':>8} {'EV/Rev':>8} {'BrütM':>7} {'EBITDAM':>8} {'ROE':>7} {'Büyüme':>8}"
    print(header)
    print("  " + "-" * (len(header) - 2))

    data = []
    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            info = t.info
            row = {
                'ticker': ticker,
                'mcap': safe_get(info, 'marketCap'),
                'ev': safe_get(info, 'enterpriseValue'),
                'ev_ebitda': safe_get(info, 'enterpriseToEbitda'),
                'pe': safe_get(info, 'trailingPE'),
                'ev_rev': safe_get(info, 'enterpriseToRevenue'),
                'gross_margin': safe_get(info, 'grossMargins'),
                'ebitda_margin': safe_get(info, 'ebitdaMargins'),
                'roe': safe_get(info, 'returnOnEquity'),
                'rev_growth': safe_get(info, 'revenueGrowth'),
            }
            data.append(row)

            print(f"  {ticker:<12} {fmt_num(row['mcap'], 1):>10} {fmt_num(row['ev'], 1):>10} "
                  f"{fmt_num(row['ev_ebitda'], 1):>10} {fmt_num(row['pe'], 1):>8} {fmt_num(row['ev_rev'], 1):>8} "
                  f"{fmt_pct(row['gross_margin']):>7} {fmt_pct(row['ebitda_margin']):>8} "
                  f"{fmt_pct(row['roe']):>7} {fmt_pct(row['rev_growth']):>8}")
        except Exception as e:
            print(f"  {ticker:<12} ⚠️ Veri alınamadı: {e}")

    # İstatistiksel özet
    if len(data) >= 3:
        print("  " + "-" * (len(header) - 2))
        import statistics
        for stat_name, stat_func in [("Median", statistics.median), ("Min", min), ("Max", max)]:
            vals = {}
            for key in ['ev_ebitda', 'pe', 'ev_rev', 'gross_margin', 'ebitda_margin', 'roe', 'rev_growth']:
                nums = [r[key] for r in data if r[key] is not None and isinstance(r[key], (int, float))]
                vals[key] = stat_func(nums) if nums else None

            print(f"  {stat_name:<12} {'':>10} {'':>10} "
                  f"{fmt_num(vals['ev_ebitda'], 1):>10} {fmt_num(vals['pe'], 1):>8} {fmt_num(vals['ev_rev'], 1):>8} "
                  f"{fmt_pct(vals['gross_margin']):>7} {fmt_pct(vals['ebitda_margin']):>8} "
                  f"{fmt_pct(vals['roe']):>7} {fmt_pct(vals['rev_growth']):>8}")


# ── Earnings ─────────────────────────────────────────────────────────────────

def cmd_earnings(ticker: str):
    """Earnings date + geçmiş sürprizler."""
    t = yf.Ticker(ticker)
    info = t.info

    print(f"{'='*60}")
    print(f"  {ticker} — Earnings Bilgisi")
    print(f"{'='*60}")
    print()

    # Earnings date (calendar)
    try:
        cal = t.calendar
        if cal is not None and not (hasattr(cal, 'empty') and cal.empty):
            print(f"  Sonraki Earnings: {cal}")
    except Exception:
        pass

    # Earnings history
    try:
        eh = t.earnings_history
        if eh is not None and not eh.empty:
            print()
            print("  Son Earnings Sürprizleri:")
            print(f"  {'Dönem':<12} {'Beklenti':>10} {'Gerçekleşme':>12} {'Sürpriz':>10}")
            print("  " + "-" * 46)
            for _, row in eh.tail(8).iterrows():
                eps_est = row.get('epsEstimate', None)
                eps_act = row.get('epsActual', None)
                surprise = row.get('surprisePercent', None)
                period = str(row.get('quarter', ''))[:10] if 'quarter' in row else str(row.name)[:10]
                print(f"  {period:<12} {fmt_num(eps_est):>10} {fmt_num(eps_act):>12} {fmt_pct(surprise/100 if surprise else None):>10}")
    except Exception:
        pass

    # Analist önerileri
    rec = safe_get(info, 'recommendationKey', 'N/A')
    target = safe_get(info, 'targetMeanPrice')
    print()
    print(f"  Tavsiye:         {rec}")
    print(f"  Hedef Fiyat:     {fmt_num(target)}")


# ── JSON ─────────────────────────────────────────────────────────────────────

def cmd_json(ticker: str):
    """Ham info dict'i JSON olarak döndür — programatik erişim için."""
    t = yf.Ticker(ticker)
    info = t.info
    # None ve NaN temizle
    clean = {}
    for k, v in info.items():
        if v is None:
            continue
        if isinstance(v, float) and (v != v):  # NaN check
            continue
        clean[k] = v
    print(json.dumps(clean, indent=2, default=str))


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if not HAS_YFINANCE:
        print("❌ yfinance yüklü değil. Kur: pip install yfinance")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="BBB Finans — Yahoo Finance CLI (yurt dışı peer verileri)",
        epilog="BIST verileri için: bbb_financials.py veya bbb_kap.py kullanın."
    )
    sub = parser.add_subparsers(dest="command")

    # quote
    p_quote = sub.add_parser("quote", help="Detaylı fiyat + metrikler")
    p_quote.add_argument("ticker", help="Hisse ticker (ör: LVS, WYNN)")

    # fundamentals
    p_fund = sub.add_parser("fundamentals", help="Temel finansal göstergeler")
    p_fund.add_argument("ticker", help="Hisse ticker")

    # compare
    p_comp = sub.add_parser("compare", help="Peer karşılaştırma tablosu")
    p_comp.add_argument("tickers", help="Virgülle ayrılmış ticker'lar (ör: LVS,WYNN,MGM)")

    # earnings
    p_earn = sub.add_parser("earnings", help="Earnings date + sürpriz geçmişi")
    p_earn.add_argument("ticker", help="Hisse ticker")

    # json
    p_json = sub.add_parser("json", help="Ham veri (JSON)")
    p_json.add_argument("ticker", help="Hisse ticker")

    # Shorthand: `bbb_yfinance.py LVS` → quote LVS
    if len(sys.argv) == 2 and not sys.argv[1].startswith("-") and sys.argv[1].upper() not in ("QUOTE", "FUNDAMENTALS", "COMPARE", "EARNINGS", "JSON"):
        cmd_quote(sys.argv[1].upper())
        return

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    if args.command == "quote":
        cmd_quote(args.ticker.upper())
    elif args.command == "fundamentals":
        cmd_fundamentals(args.ticker.upper())
    elif args.command == "compare":
        tickers = [t.strip().upper() for t in args.tickers.split(",")]
        cmd_compare(tickers)
    elif args.command == "earnings":
        cmd_earnings(args.ticker.upper())
    elif args.command == "json":
        cmd_json(args.ticker.upper())


if __name__ == "__main__":
    main()
