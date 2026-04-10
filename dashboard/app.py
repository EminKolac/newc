"""
US Market & Geopolitical Risk Dashboard
Tracks S&P 500, Nasdaq, Dow, Oil, USD Index, Gold
with volatility metrics and US-Iran / Strait of Hormuz news alerts.

Uses only stdlib + requests + flask (no yfinance/feedparser needed).
"""

import math
import threading
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import quote_plus

import requests
from flask import Flask, jsonify, render_template, request as flask_request

app = Flask(__name__)

# ── Tracked instruments ──────────────────────────────────────────────────────
INSTRUMENTS = {
    "S&P 500":         {"symbol": "^GSPC",    "category": "index"},
    "Nasdaq":          {"symbol": "^IXIC",    "category": "index"},
    "Dow Jones":       {"symbol": "^DJI",     "category": "index"},
    "WTI Crude Oil":   {"symbol": "CL=F",     "category": "commodity"},
    "US Dollar Index": {"symbol": "DX-Y.NYB", "category": "currency"},
    "Gold":            {"symbol": "GC=F",     "category": "commodity"},
}

ALERT_THRESHOLD_PCT = 2.0

YAHOO_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# ── In-memory cache ──────────────────────────────────────────────────────────
cache = {
    "market_data": {},
    "news": [],
    "alerts": [],
    "last_update": None,
}
cache_lock = threading.Lock()

# Period → Yahoo Finance query parameters (range, interval)
PERIOD_MAP = {
    "1d":  ("1d",  "5m"),
    "5d":  ("5d",  "15m"),
    "1mo": ("1mo", "1d"),
    "3mo": ("3mo", "1d"),
    "6mo": ("6mo", "1d"),
    "1y":  ("1y",  "1d"),
    "ytd": ("ytd", "1d"),
}


# ── Yahoo Finance helpers ────────────────────────────────────────────────────

def _yahoo_chart(symbol, range_="1mo", interval="1d"):
    """Call Yahoo Finance v8 chart API and return parsed JSON."""
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{quote_plus(symbol)}"
        f"?range={range_}&interval={interval}&includePrePost=false"
    )
    resp = requests.get(url, headers=YAHOO_HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    result = data.get("chart", {}).get("result")
    if not result:
        return None
    return result[0]


def fetch_market_data():
    """Return current price snapshot for every instrument."""
    out = {}
    for name, info in INSTRUMENTS.items():
        sym = info["symbol"]
        try:
            chart = _yahoo_chart(sym, range_="5d", interval="1d")
            if chart is None:
                out[name] = {"symbol": sym, "error": "No chart data"}
                continue

            meta = chart.get("meta", {})
            quotes = chart.get("indicators", {}).get("quote", [{}])[0]
            timestamps = chart.get("timestamp", [])

            closes = quotes.get("close", [])
            highs = quotes.get("high", [])
            lows = quotes.get("low", [])
            volumes = quotes.get("volume", [])

            # Filter out None values from the end
            valid = [(c, h, l, v) for c, h, l, v in zip(closes, highs, lows, volumes)
                     if c is not None]
            if len(valid) < 2:
                out[name] = {"symbol": sym, "error": "Insufficient data"}
                continue

            current = valid[-1][0]
            prev_close_val = valid[-2][0]
            change = current - prev_close_val
            change_pct = (change / prev_close_val) * 100

            out[name] = {
                "symbol": sym,
                "category": info["category"],
                "price": round(current, 2),
                "change": round(change, 2),
                "change_pct": round(change_pct, 2),
                "high": round(valid[-1][1], 2),
                "low": round(valid[-1][2], 2),
                "volume": int(valid[-1][3] or 0),
                "prev_close": round(prev_close_val, 2),
            }
        except Exception as exc:
            out[name] = {"symbol": sym, "error": str(exc)}
    return out


def fetch_historical(symbol, period="1mo"):
    """Return OHLCV history for charting."""
    range_, interval = PERIOD_MAP.get(period, ("1mo", "1d"))
    try:
        chart = _yahoo_chart(symbol, range_=range_, interval=interval)
        if chart is None:
            return {"error": "No data available"}

        timestamps = chart.get("timestamp", [])
        quotes = chart.get("indicators", {}).get("quote", [{}])[0]

        dates = [datetime.utcfromtimestamp(t).strftime("%Y-%m-%d %H:%M") for t in timestamps]
        closes = quotes.get("close", [])
        highs = quotes.get("high", [])
        lows = quotes.get("low", [])
        opens = quotes.get("open", [])
        volumes = quotes.get("volume", [])

        def clean(arr):
            return [round(x, 2) if x is not None else None for x in arr]

        def clean_vol(arr):
            return [int(x) if x is not None else 0 for x in arr]

        return {
            "dates": dates,
            "open": clean(opens),
            "high": clean(highs),
            "low": clean(lows),
            "close": clean(closes),
            "volume": clean_vol(volumes),
        }
    except Exception as exc:
        return {"error": str(exc)}


def calculate_volatility(symbol, period="3mo"):
    """Compute daily, annualised vol, rolling 20-day vol, and max drawdown."""
    range_, interval = PERIOD_MAP.get(period, ("3mo", "1d"))
    try:
        chart = _yahoo_chart(symbol, range_=range_, interval=interval)
        if chart is None:
            return {"error": "No chart data"}

        quotes = chart.get("indicators", {}).get("quote", [{}])[0]
        timestamps = chart.get("timestamp", [])
        closes = quotes.get("close", [])
        highs = quotes.get("high", [])
        lows = quotes.get("low", [])

        # Filter out None
        valid = [(t, c, h, l) for t, c, h, l in zip(timestamps, closes, highs, lows)
                 if c is not None and h is not None and l is not None]
        if len(valid) < 22:
            return {"error": "Insufficient data for volatility calculation"}

        close_vals = [v[1] for v in valid]
        high_vals = [v[2] for v in valid]
        low_vals = [v[3] for v in valid]
        ts_vals = [v[0] for v in valid]

        # Daily log returns
        returns = []
        for i in range(1, len(close_vals)):
            if close_vals[i - 1] > 0:
                returns.append(close_vals[i] / close_vals[i - 1] - 1)

        n = len(returns)
        mean_r = sum(returns) / n
        var_r = sum((r - mean_r) ** 2 for r in returns) / (n - 1)
        daily_vol = math.sqrt(var_r)
        ann_vol = daily_vol * math.sqrt(252)

        # 20-day rolling annualised volatility
        window = 20
        rolling_dates = []
        rolling_vals = []
        for i in range(window, len(returns) + 1):
            chunk = returns[i - window:i]
            m = sum(chunk) / window
            v = sum((r - m) ** 2 for r in chunk) / (window - 1)
            rolling_dates.append(datetime.utcfromtimestamp(ts_vals[i]).strftime("%Y-%m-%d"))
            rolling_vals.append(round(math.sqrt(v) * math.sqrt(252) * 100, 2))

        # Max drawdown
        peak = close_vals[0]
        max_dd = 0
        for c in close_vals[1:]:
            if c > peak:
                peak = c
            dd = (c - peak) / peak
            if dd < max_dd:
                max_dd = dd

        # ATR(20) — average of daily high-low over last 20 bars
        hl = [h - l for h, l in zip(high_vals[-20:], low_vals[-20:])]
        atr_20 = sum(hl) / len(hl)

        return {
            "daily_volatility": round(daily_vol * 100, 3),
            "annualized_volatility": round(ann_vol * 100, 2),
            "max_drawdown": round(max_dd * 100, 2),
            "atr_20": round(atr_20, 2),
            "rolling_vol": {
                "dates": rolling_dates,
                "values": rolling_vals,
            },
        }
    except Exception as exc:
        return {"error": str(exc)}


# ── News via Google News RSS (stdlib XML) ────────────────────────────────────

def fetch_news():
    """Fetch US-Iran / Strait of Hormuz headlines from Google News RSS."""
    queries = [
        "US Iran ceasefire",
        "Strait of Hormuz",
        "Iran oil sanctions",
        "Iran nuclear deal",
        "Middle East oil supply disruption",
        "US Iran military",
    ]
    items = []
    for query in queries:
        try:
            url = (
                "https://news.google.com/rss/search?"
                f"q={quote_plus(query)}&hl=en-US&gl=US&ceid=US:en"
            )
            resp = requests.get(url, headers=YAHOO_HEADERS, timeout=10)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)

            for item_el in root.iter("item"):
                title = item_el.findtext("title", "")
                link = item_el.findtext("link", "")
                pub = item_el.findtext("pubDate", "")
                source_el = item_el.find("source")
                source = source_el.text if source_el is not None else "Unknown"

                items.append({
                    "title": title,
                    "link": link,
                    "published": pub,
                    "source": source,
                    "query": query,
                })
                if len([i for i in items if i["query"] == query]) >= 3:
                    break
        except Exception:
            pass

    # Deduplicate by title
    seen = set()
    unique = []
    for item in items:
        if item["title"] not in seen:
            seen.add(item["title"])
            unique.append(item)
    return unique[:25]


# ── Alerts ───────────────────────────────────────────────────────────────────

def check_alerts(market_data):
    """Flag instruments that moved more than ALERT_THRESHOLD_PCT."""
    alerts = []
    for name, data in market_data.items():
        pct = data.get("change_pct")
        if pct is None:
            continue
        if abs(pct) >= ALERT_THRESHOLD_PCT:
            direction = "UP" if pct > 0 else "DOWN"
            alerts.append({
                "instrument": name,
                "change_pct": pct,
                "price": data["price"],
                "direction": direction,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "message": (
                    f"{name} moved {direction} {abs(pct):.2f}% "
                    f"to {data['price']:,.2f}"
                ),
            })
    return alerts


# ── Background updater ───────────────────────────────────────────────────────

def background_updater():
    while True:
        try:
            md = fetch_market_data()
            alerts = check_alerts(md)
            news = fetch_news()
            with cache_lock:
                cache["market_data"] = md
                cache["alerts"] = alerts
                cache["news"] = news
                cache["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{cache['last_update']}] Cache refreshed.")
        except Exception as exc:
            print(f"Background update error: {exc}")
        time.sleep(60)


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/market-data")
def api_market_data():
    with cache_lock:
        return jsonify({"data": cache["market_data"], "last_update": cache["last_update"]})


@app.route("/api/historical/<path:symbol>")
def api_historical(symbol):
    period = flask_request.args.get("period", "1mo")
    allowed = {"1d", "5d", "1mo", "3mo", "6mo", "1y", "ytd"}
    if period not in allowed:
        period = "1mo"
    return jsonify(fetch_historical(symbol, period))


@app.route("/api/volatility")
def api_volatility():
    result = {}
    for name, info in INSTRUMENTS.items():
        result[name] = calculate_volatility(info["symbol"])
    return jsonify(result)


@app.route("/api/volatility/<path:symbol>")
def api_volatility_single(symbol):
    period = flask_request.args.get("period", "3mo")
    return jsonify(calculate_volatility(symbol, period))


@app.route("/api/news")
def api_news():
    with cache_lock:
        return jsonify(cache["news"])


@app.route("/api/alerts")
def api_alerts():
    with cache_lock:
        return jsonify(cache["alerts"])


@app.route("/api/instruments")
def api_instruments():
    return jsonify(INSTRUMENTS)


# ── Entrypoint ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Kick off background thread
    t = threading.Thread(target=background_updater, daemon=True)
    t.start()

    # Blocking initial load so the first page render has data
    print("Loading initial market data ...")
    md = fetch_market_data()
    alerts = check_alerts(md)
    news = fetch_news()
    with cache_lock:
        cache["market_data"] = md
        cache["alerts"] = alerts
        cache["news"] = news
        cache["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Ready. Starting server on http://0.0.0.0:5000")

    app.run(debug=False, host="0.0.0.0", port=5000)
