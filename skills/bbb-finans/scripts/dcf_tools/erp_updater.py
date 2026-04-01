#!/usr/bin/env python3
"""
Country ERP (Equity Risk Premium) Otomatik Güncelleme
Damodaran'ın ERP sayfasından ülke bazlı risk primi verilerini çeker.

Kaynak: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html
Alternatif Excel: https://pages.stern.nyu.edu/~adamodar/pc/datasets/ctryprem.xlsx

Rate limiting uygulanır. Cache 24 saat geçerlidir.
"""

import json
import time
import re
import sys
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ─── Config ───────────────────────────────────────────────────────────────────
DAMODARAN_ERP_URL = "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html"
DAMODARAN_ERP_EXCEL = "https://pages.stern.nyu.edu/~adamodar/pc/datasets/ctryprem.xlsx"
CACHE_DIR = Path.home() / ".cache" / "bbb-finans"
CACHE_FILE = CACHE_DIR / "country_erp.json"
CACHE_TTL = 86400  # 24 hours
RATE_LIMIT_DELAY = 2.0

# Fallback data (January 2024)
FALLBACK_ERP: Dict[str, Dict[str, Any]] = {
    "Turkey": {
        "country": "Turkey",
        "region": "Emerging Markets",
        "moodys_rating": "B1",
        "country_risk_premium": 0.0583,   # %5.83 (Ocak 2026 Damodaran)
        "equity_risk_premium": 0.1006,    # %10.06 (4.23 + 5.83)
        "country_default_spread": 0.0383, # %3.83
        "updated": "2026-01-15",
    },
    "United States": {
        "country": "United States",
        "region": "Developed Markets",
        "moodys_rating": "Aaa",
        "country_risk_premium": 0.0,
        "equity_risk_premium": 0.0423,    # %4.23 (Ocak 2026 Damodaran implied ERP)
        "country_default_spread": 0.0,
        "updated": "2026-01-15",
    },
    "Germany": {
        "country": "Germany",
        "region": "Developed Markets",
        "moodys_rating": "Aaa",
        "country_risk_premium": 0.0,
        "equity_risk_premium": 0.0423,    # %4.23 (Mature Market ERP = ABD bazlı)
        "country_default_spread": 0.0,
        "updated": "2026-01-15",
    },
    "Brazil": {
        "country": "Brazil",
        "region": "Emerging Markets",
        "moodys_rating": "Ba2",
        "country_risk_premium": 0.0327,
        "equity_risk_premium": 0.0807,
        "country_default_spread": 0.0218,
        "updated": "2024-01-01",
    },
    "India": {
        "country": "India",
        "region": "Emerging Markets",
        "moodys_rating": "Baa3",
        "country_risk_premium": 0.0234,
        "equity_risk_premium": 0.0714,
        "country_default_spread": 0.0156,
        "updated": "2024-01-01",
    },
    "China": {
        "country": "China",
        "region": "Emerging Markets",
        "moodys_rating": "A1",
        "country_risk_premium": 0.0094,
        "equity_risk_premium": 0.0574,
        "country_default_spread": 0.0063,
        "updated": "2024-01-01",
    },
    "South Africa": {
        "country": "South Africa",
        "region": "Emerging Markets",
        "moodys_rating": "Ba2",
        "country_risk_premium": 0.0384,
        "equity_risk_premium": 0.0864,
        "country_default_spread": 0.0256,
        "updated": "2024-01-01",
    },
    "Russia": {
        "country": "Russia",
        "region": "Emerging Markets",
        "moodys_rating": "Ca",
        "country_risk_premium": 0.1656,
        "equity_risk_premium": 0.2136,
        "country_default_spread": 0.1104,
        "updated": "2024-01-01",
    },
}


def _load_cache() -> Optional[Dict]:
    """Load cached ERP data if fresh."""
    if CACHE_FILE.exists():
        age = time.time() - CACHE_FILE.stat().st_mtime
        if age < CACHE_TTL:
            with open(CACHE_FILE) as f:
                return json.load(f)
    return None


def _save_cache(data: Dict):
    """Save ERP data to cache."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_erp_from_web() -> Optional[Dict[str, Dict]]:
    """
    Damodaran'ın ERP sayfasından ülke verilerini çeker.
    HTML tabloyu parse eder.
    """
    if not HAS_REQUESTS:
        print("[WARN] requests kütüphanesi yok, fallback kullanılıyor.", file=sys.stderr)
        return None

    try:
        time.sleep(RATE_LIMIT_DELAY)
        resp = requests.get(
            DAMODARAN_ERP_URL,
            headers={"User-Agent": "Mozilla/5.0 BBB-Finans/1.0"},
            timeout=30,
        )
        resp.raise_for_status()
        html = resp.text

        # Parse HTML table rows
        # Format: Country | Moody's | Rating-Based Default Spread | Total ERP | Country Risk Premium
        result = {}
        
        # Find table rows
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL | re.IGNORECASE)
        
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL | re.IGNORECASE)
            if len(cells) >= 4:
                country = re.sub(r'<[^>]+>', '', cells[0]).strip()
                if not country or country.lower() in ('country', 'region', ''):
                    continue
                
                moodys = re.sub(r'<[^>]+>', '', cells[1]).strip() if len(cells) > 1 else ""
                
                # Parse spread values (handle percentage format)
                def parse_pct(val: str) -> float:
                    val = re.sub(r'<[^>]+>', '', val).strip().replace('%', '').replace(',', '.')
                    try:
                        return float(val) / 100
                    except (ValueError, TypeError):
                        return 0.0
                
                default_spread = parse_pct(cells[2]) if len(cells) > 2 else 0.0
                total_erp = parse_pct(cells[3]) if len(cells) > 3 else 0.0
                country_premium = parse_pct(cells[4]) if len(cells) > 4 else 0.0
                
                if country and (total_erp > 0 or default_spread > 0):
                    result[country] = {
                        "country": country,
                        "moodys_rating": moodys,
                        "country_default_spread": round(default_spread, 6),
                        "equity_risk_premium": round(total_erp, 6),
                        "country_risk_premium": round(country_premium, 6),
                        "updated": datetime.now().strftime("%Y-%m-%d"),
                    }
        
        return result if result else None

    except Exception as e:
        print(f"[WARN] Damodaran ERP sayfası çekilemedi: {e}", file=sys.stderr)
        return None


def get_erp_data(force_refresh: bool = False) -> Dict[str, Dict]:
    """
    ERP verilerini döndürür. Önce cache, sonra web, sonra fallback.
    
    Args:
        force_refresh: Cache'i yoksay, web'den çek
        
    Returns:
        {country_name: {country, moodys_rating, country_default_spread, 
         equity_risk_premium, country_risk_premium, updated}}
    """
    if not force_refresh:
        cached = _load_cache()
        if cached:
            return cached
    
    web_data = fetch_erp_from_web()
    if web_data:
        _save_cache(web_data)
        return web_data
    
    return FALLBACK_ERP


def get_country_erp(country: str, force_refresh: bool = False) -> Optional[Dict]:
    """
    Tek bir ülkenin ERP verisini döndürür.
    
    Args:
        country: Ülke adı (case-insensitive, partial match)
        
    Returns:
        ERP dict veya None
    """
    data = get_erp_data(force_refresh)
    
    # Exact match
    if country in data:
        return data[country]
    
    # Case-insensitive match
    country_lower = country.lower()
    for key, val in data.items():
        if key.lower() == country_lower:
            return val
    
    # Partial match
    for key, val in data.items():
        if country_lower in key.lower():
            return val
    
    return None


def get_turkey_erp(force_refresh: bool = False) -> Dict:
    """Türkiye ERP verisini döndürür (shortcut)."""
    result = get_country_erp("Turkey", force_refresh)
    return result or FALLBACK_ERP["Turkey"]


if __name__ == "__main__":
    print("=== Country ERP Güncelleme ===\n")
    
    # Test fallback
    turkey = get_turkey_erp()
    print(f"  Türkiye:")
    print(f"    Rating: {turkey['moodys_rating']}")
    print(f"    Country Risk Premium: {turkey['country_risk_premium']:.2%}")
    print(f"    Equity Risk Premium: {turkey['equity_risk_premium']:.2%}")
    print(f"    Default Spread: {turkey['country_default_spread']:.2%}")
    print(f"    Güncelleme: {turkey['updated']}")
    
    us = get_country_erp("United States")
    if us:
        print(f"\n  ABD:")
        print(f"    ERP: {us['equity_risk_premium']:.2%}")
    
    # Try web fetch
    print("\n  Web'den güncelleme deneniyor...")
    web = fetch_erp_from_web()
    if web:
        print(f"  ✅ {len(web)} ülke çekildi.")
        tr = web.get("Turkey")
        if tr:
            print(f"  Türkiye (güncel): ERP={tr['equity_risk_premium']:.2%}")
    else:
        print("  ⚠️ Web erişimi başarısız, fallback kullanılıyor.")
    
    print("\n✅ erp_updater.py çalışıyor.")
