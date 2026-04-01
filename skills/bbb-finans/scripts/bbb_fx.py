#!/usr/bin/env python3
"""
BBB FX - Döviz Kurları Modülü

TCMB kurlarını çeşitli kaynaklardan alır.
Öncelik: TCMB XML > Truncgil API > Yahoo Finance fallback

Kullanım:
    from bbb_fx import get_rates, get_rate, format_rates
    rates = get_rates()
    usd = get_rate("USD")
"""

import json
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

try:
    import requests
except ImportError:
    print("HATA: pip install requests")
    sys.exit(1)


# Desteklenen para birimleri
SUPPORTED = {
    "USD": "ABD Doları",
    "EUR": "Euro",
    "GBP": "İngiliz Sterlini",
    "CHF": "İsviçre Frangı",
    "JPY": "Japon Yeni",
    "AUD": "Avustralya Doları",
    "CAD": "Kanada Doları",
    "SAR": "Suudi Riyali",
    "CNY": "Çin Yuanı",
    "RUB": "Rus Rublesi",
}

# TCMB XML kur kaynağı (API key gerektirmez)
TCMB_XML_URL = "https://www.tcmb.gov.tr/kurlar/today.xml"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
}


@dataclass
class FXRate:
    """Döviz kuru verisi"""
    code: str
    name: str
    buying: float   # Alış
    selling: float  # Satış
    effective_buying: Optional[float] = None   # Efektif alış
    effective_selling: Optional[float] = None  # Efektif satış
    change_pct: Optional[float] = None
    date: str = ""


def fetch_tcmb_xml() -> Dict[str, FXRate]:
    """TCMB XML'den güncel kurları çek (en güvenilir kaynak)"""
    rates = {}
    try:
        resp = requests.get(TCMB_XML_URL, headers=HEADERS, timeout=10)
        resp.raise_for_status()

        root = ET.fromstring(resp.content)
        date_str = root.attrib.get("Date", "")

        for currency in root.findall(".//Currency"):
            code = currency.attrib.get("CurrencyCode", "")
            if code not in SUPPORTED:
                continue

            def get_float(tag):
                el = currency.find(tag)
                if el is not None and el.text:
                    try:
                        return float(el.text)
                    except ValueError:
                        pass
                return None

            buying = get_float("ForexBuying")
            selling = get_float("ForexSelling")
            eff_buying = get_float("BanknoteBuying")
            eff_selling = get_float("BanknoteSelling")

            if buying and selling:
                rates[code] = FXRate(
                    code=code,
                    name=SUPPORTED.get(code, code),
                    buying=buying,
                    selling=selling,
                    effective_buying=eff_buying,
                    effective_selling=eff_selling,
                    date=date_str,
                )

    except Exception as e:
        print(f"TCMB XML hatası: {e}", file=sys.stderr)

    return rates


def fetch_yahoo_fallback(codes: List[str] = None) -> Dict[str, FXRate]:
    """Yahoo Finance'dan kur çek (fallback)"""
    rates = {}
    if codes is None:
        codes = list(SUPPORTED.keys())

    try:
        import yfinance as yf
        for code in codes:
            try:
                ticker = yf.Ticker(f"{code}TRY=X")
                info = ticker.info
                price = info.get("regularMarketPrice", 0)
                prev = info.get("previousClose", 0)
                if price and price > 0:
                    change = ((price - prev) / prev * 100) if prev > 0 else None
                    rates[code] = FXRate(
                        code=code,
                        name=SUPPORTED.get(code, code),
                        buying=round(price, 4),
                        selling=round(price, 4),
                        change_pct=round(change, 2) if change else None,
                        date=datetime.now().strftime("%Y-%m-%d"),
                    )
            except Exception:
                continue
    except ImportError:
        pass

    return rates


def get_rates() -> Dict[str, FXRate]:
    """Tüm kurları al (TCMB öncelikli, fallback Yahoo)"""
    rates = fetch_tcmb_xml()
    if not rates:
        rates = fetch_yahoo_fallback()
    return rates


def get_rate(code: str) -> Optional[FXRate]:
    """Tek bir kur al"""
    code = code.upper()
    rates = get_rates()
    return rates.get(code)


def format_rate(rate: FXRate, fmt: str = "text") -> str:
    """Tek kur formatla"""
    if fmt == "json":
        return json.dumps(rate.__dict__, indent=2, ensure_ascii=False)

    change_str = f"  ({rate.change_pct:+.2f}%)" if rate.change_pct is not None else ""
    lines = [
        f"\n{'='*50}",
        f"💱 {rate.code}/TRY - {rate.name}",
        f"{'='*50}",
        f"",
        f"  📅 Tarih:           {rate.date}",
        f"  💰 Döviz Alış:      {rate.buying:>10.4f} TL",
        f"  💰 Döviz Satış:     {rate.selling:>10.4f} TL",
    ]

    if rate.effective_buying:
        lines.append(f"  💵 Efektif Alış:    {rate.effective_buying:>10.4f} TL")
    if rate.effective_selling:
        lines.append(f"  💵 Efektif Satış:   {rate.effective_selling:>10.4f} TL")

    if rate.change_pct is not None:
        lines.append(f"  📊 Değişim:         {rate.change_pct:>+10.2f}%")

    lines.extend([f"", f"{'='*50}"])
    return "\n".join(lines)


def format_rates(rates: Dict[str, FXRate], fmt: str = "text") -> str:
    """Tüm kurları formatla"""
    if fmt == "json":
        return json.dumps({k: v.__dict__ for k, v in rates.items()}, indent=2, ensure_ascii=False)

    if not rates:
        return "❌ Kur verisi alınamadı."

    date_str = next(iter(rates.values())).date if rates else ""
    lines = [
        f"\n{'='*60}",
        f"💱 DÖVİZ KURLARI (TCMB) - {date_str}",
        f"{'='*60}",
        f"  {'Döviz':<6} {'İsim':<22} {'Alış':>10} {'Satış':>10}",
        f"  {'─'*54}",
    ]

    for code in ["USD", "EUR", "GBP", "CHF", "JPY", "AUD", "CAD", "SAR", "CNY", "RUB"]:
        if code in rates:
            r = rates[code]
            lines.append(f"  {r.code:<6} {r.name:<22} {r.buying:>10.4f} {r.selling:>10.4f}")

    lines.extend([f"", f"{'='*60}"])
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        # Tüm kurları göster
        rates = get_rates()
        print(format_rates(rates))
        return

    code = sys.argv[1].upper()
    fmt = "json" if "--json" in sys.argv else "text"

    if code == "LIST" or code == "ALL":
        rates = get_rates()
        print(format_rates(rates, fmt))
    else:
        rate = get_rate(code)
        if rate:
            print(format_rate(rate, fmt))
        else:
            print(f"❌ {code} kuru bulunamadı. Desteklenen: {', '.join(SUPPORTED.keys())}")
            sys.exit(1)


if __name__ == "__main__":
    main()
