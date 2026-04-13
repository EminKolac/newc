#!/usr/bin/env python3
"""
BBB Finans - İş Yatırım Finansal Tablo Modülü
Fetches detailed financial statements (147+ items) from İş Yatırım API.
Covers: Balance Sheet, Income Statement, Cash Flow Statement.
Banks use financial_group='2' (UFRS), others use '1' (XI_29).

Also provides stock price data (OHLCV) and index data via isyatirimhisse package.
"""

import logging
import sys
import os
import json
import time
import hashlib
import sqlite3
import pickle
import argparse
import requests
import warnings
import datetime as _dt_module
from datetime import datetime, date as _date, timedelta as _timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple

logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore")

# ─── Config ───────────────────────────────────────────────────────────────────
BASE_URL = "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"
_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = Path(os.environ.get("BBB_CACHE_DIR", os.path.join(_PROJECT_DIR, "bbb_cache")))
CACHE_TTL = 3600 * 24 * 7  # 7 days (raw per-year API call cache) - Offline-First Strategy
TIMEOUT = 15  # 15s — İş Yatırım bazen 10-12sn yanıt veriyor, 4sn çok kısa
RATE_LIMIT_DELAY = 0.5  # seconds between requests

# ── Sunucu modu: Railway'de İş Yatırım API çağrısı yapılmaz ──
# RAILWAY_ENVIRONMENT Railway tarafından otomatik set edilir (production, staging vb.)
# True → sunucu sadece DB'den okur, cache miss olursa boş döner
# False → lokal mod, İş Yatırım API'den veri çekilebilir
_IS_SERVER_MODE = bool(os.environ.get("RAILWAY_ENVIRONMENT"))

# ── SQLite Cache Config (fetch_financials level) ──
_CACHE_DIR = os.path.join(_PROJECT_DIR, "bbb_cache")
_CACHE_DB  = os.path.join(_CACHE_DIR, "financials.db")
_CACHE_TTL_DEFAULT = 7 * 24 * 3600   # 7 gün — normal dönem
_CACHE_TTL_EARNINGS = 2 * 24 * 3600  # 2 gün — kazanç sezonu (yeni dönem verisi bekleniyor)

# Kazanç sezonu ayları: Şubat-Mart (FY), Mayıs (Q1), Ağustos (Q2), Kasım (Q3)
_EARNINGS_MONTHS = {2, 3, 5, 8, 11}


def _get_cache_ttl() -> int:
    """Mevcut aya göre cache TTL döndür.
    Kazanç sezonunda (Şub-Mar, May, Ağu, Kas) kısa TTL → yeni veriler daha çabuk yansır.
    """
    from datetime import datetime
    if datetime.now().month in _EARNINGS_MONTHS:
        return _CACHE_TTL_EARNINGS
    return _CACHE_TTL_DEFAULT

# Banks that need UFRS (financial_group=2)
BANK_TICKERS = {
    "GARAN", "AKBNK", "ISCTR", "YKBNK", "HALKB", "VAKBN", "QNBTR", "TSKB",
    "ALBRK", "SKBNK", "ICBCT", "DENIZ", "KLNMA", "ISBTR", "TURSG"
}

# ─── Financial Item Categories ────────────────────────────────────────────────
BALANCE_SHEET_CODES = {
    "1A": "Dönen Varlıklar",
    "1AA": "Nakit ve Nakit Benzerleri",
    "1AB": "Finansal Yatırımlar",
    "1AC": "Ticari Alacaklar",
    "1AF": "Stoklar",
    "1AK": "Duran Varlıklar",
    "1BL": "TOPLAM VARLIKLAR",
    "2A": "Kısa Vadeli Yükümlülükler",
    "2AA": "Kısa Vadeli Finansal Borçlar",
    "2B": "Uzun Vadeli Yükümlülükler",
    "2BA": "Uzun Vadeli Finansal Borçlar",
    "2N": "Özkaynaklar",
    "2O": "Ana Ortaklığa Ait Özkaynaklar",
    "2OA": "Ödenmiş Sermaye",
    "2ODB": "TOPLAM KAYNAKLAR",
}

INCOME_CODES = {
    "3C": "Satış Gelirleri (Hasılat)",
    "3CA": "Satışların Maliyeti",
    "3D": "BRÜT KAR",
    "3DF": "FAALİYET KARI",
    "3HACA": "Finansman Gideri Öncesi Faaliyet Karı (EBIT proxy)",
    "3HB": "Finansal Gelirler",
    "3HC": "Finansal Giderler",
    "3I": "VERGİ ÖNCESİ KAR",
    "3IA": "Vergi Geliri/Gideri",
    "3J": "SÜRDÜRÜLEN FAALİYETLER NET KAR",
    "3L": "DÖNEM NET KARI",
    "3Z": "Ana Ortaklık Payları Net Kar",
    "3HCA": "Parasal Kazanç/Kayıp (IAS 29)",
}

CASHFLOW_CODES = {
    "4C": "İşletme Faaliyetlerinden Net Nakit",
    "4CA": "Düzeltme Öncesi Kar",
    "4CAB": "Amortisman & İtfa Payları (D&A)",
    "4CAI": "Sabit Sermaye Yatırımları (CapEx)",
    "4CAK": "Yatırım Faaliyetlerinden Nakit",
    "4CB": "Serbest Nakit Akım (FCF)",
    "4CBA": "Finansal Borçlardaki Değişim",
    "4CBB": "Temettü Ödemeleri",
    "4CBE": "Finansman Faaliyetlerinden Nakit",
    "4CBI": "Nakit Değişimi",
    "4CBL": "Dönem Sonu Nakit",
}

DCF_ITEM_CODES = [
    # Income Statement
    "3C",    # Revenue
    "3CA",   # COGS
    "3D",    # Gross Profit
    "3DC",   # R&D Expenses
    "3DA",   # Marketing/Selling Expenses
    "3DB",   # G&A Expenses
    "3DF",   # Operating Profit (EBIT)
    "3HACA", # EBIT (broader: pre-financing operating profit)
    "3HB",   # Financial Income
    "3HC",   # Financial Expenses (interest expense proxy)
    "3HCA",  # IAS 29 monetary gain/loss
    "3I",    # EBT
    "3IA",   # Tax
    "3J",    # Net Income (continuing)
    "3L",    # Net Income
    "3LB",   # Minority Interest (NCI) in P&L
    "3Z",    # Net Income (parent)
    "3ZD",   # EPS (basic) — used to derive share count
    "3ZE",   # Diluted EPS — used to derive diluted share count
    # Balance Sheet
    "1A",    # Current Assets (for WC calc)
    "1AA",   # Cash
    "1AC",   # Trade Receivables
    "1AF",   # Inventories
    "1BL",   # Total Assets
    "2A",    # Current Liabilities (for WC calc)
    "2AA",   # Short-term financial debt
    "2AAGAA",# Short-term trade payables
    "2BA",   # Long-term financial debt
    "2N",    # Total Equity
    "2O",    # Parent equity
    "2OA",   # Paid-in capital
    "2ODA",  # Minority Interest (NCI) in Balance Sheet
    # Cash Flow
    "4B",    # D&A (from supplementary)
    "4BB",   # Financial Expenses (from supplementary)
    "4CAB",  # D&A (from cash flow)
    "4CAF",  # Working Capital Change
    "4CAI",  # CapEx
    "4C",    # Operating Cash Flow
    "4CB",   # Free Cash Flow
    # Supplementary
    "4BC",   # Domestic sales
    "4BD",   # International sales
    "4BE",   # Net FX position
]


# ─── Raw Cache (per-year API call, file-based JSON) ──────────────────────────
def _raw_cache_key(params: dict) -> str:
    key_str = json.dumps(params, sort_keys=True)
    return hashlib.md5(key_str.encode()).hexdigest()


def _raw_cache_get(params: dict) -> Optional[dict]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / f"{_raw_cache_key(params)}.json"
    if path.exists():
        age = time.time() - path.stat().st_mtime
        if age < CACHE_TTL:
            with open(path) as f:
                return json.load(f)
    return None


def _raw_cache_set(params: dict, data: dict):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / f"{_raw_cache_key(params)}.json"
    with open(path, "w") as f:
        json.dump(data, f)


def _invalidate_raw_cache_for_year(ticker: str, year: int):
    """Belirli ticker+yıl için raw JSON cache dosyalarını sil (API'den taze veri çekilmesini zorla)."""
    for fg_label in ["XI_29", "UFRS", "UFRS_K", "UFRS_A"]:
        params = {
            "companyCode": ticker.upper(), "exchange": "TRY",
            "financialGroup": fg_label,
            "year1": year, "period1": 3, "year2": year, "period2": 6,
            "year3": year, "period3": 9, "year4": year, "period4": 12,
        }
        path = CACHE_DIR / f"{_raw_cache_key(params)}.json"
        if path.exists():
            path.unlink()


# ─── SQLite Cache (fetch_financials level, 90-day TTL) ───────────────────────
# ── Thread-local connection pool — her thread kendi bağlantısını yeniden kullanır ──
import threading as _threading
_thread_local = _threading.local()


def _cache_connect():
    """Thread-local SQLite bağlantısı, WAL modu aktif.
    Her thread tek bir bağlantı kullanır (connection reuse).
    close() çağırmayın — bağlantı thread ömrü boyunca yaşar.
    """
    conn = getattr(_thread_local, "conn", None)
    if conn is not None:
        try:
            conn.execute("SELECT 1")  # Bağlantı hâlâ canlı mı?
            return conn
        except Exception:
            pass  # Bozuk bağlantı — yeniden aç

    os.makedirs(_CACHE_DIR, exist_ok=True)
    conn = sqlite3.connect(_CACHE_DB, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS financials_cache (
            key         TEXT PRIMARY KEY,
            ticker      TEXT NOT NULL,
            data        BLOB NOT NULL,
            created_at  REAL NOT NULL
        )
    """)
    conn.commit()
    _thread_local.conn = conn
    return conn


def _cache_key(ticker: str, exchange: str = "TRY") -> str:
    """Cache key only depends on ticker + exchange (yıl bağımsız).
    Bu sayede sync scripti ve canlı sayfa istekleri aynı key'e düşer."""
    raw = f"{ticker.upper()}:{exchange.upper()}"
    return hashlib.md5(raw.encode()).hexdigest()


def _filter_by_years(data: dict, start_year: int = None, end_year: int = None) -> dict:
    """Cache'den gelen tüm veriyi istenen yıl aralığına filtrele.
    period_key format: '2019/Q1', '2020/FY', '2025/Q3'
    """
    if not start_year and not end_year:
        return data
    filtered = {}
    for code, item in data.items():
        values = item.get("values", {})
        filtered_values = {}
        for period_key, val in values.items():
            try:
                year = int(period_key.split("/")[0])
                if start_year and year < start_year:
                    continue
                if end_year and year > end_year:
                    continue
                filtered_values[period_key] = val
            except (ValueError, IndexError):
                filtered_values[period_key] = val  # format tanınamadıysa dahil et
        filtered[code] = {**item, "values": filtered_values}
    return filtered


def _should_invalidate_for_new_period(cached_data: dict, now: datetime) -> bool:
    """Cache'deki verinin son dönemine göre yeni dönem beklentisi kontrolü.

    Türkiye'de çeyrek raporları genellikle şu takvimde yayınlanır:
    - Q1 (Mart sonu) → Mayıs'ta yayınlanır
    - Q2 (Haziran sonu) → Ağustos'ta yayınlanır
    - Q3 (Eylül sonu) → Kasım'da yayınlanır
    - FY (Aralık sonu) → Şubat-Mart'ta yayınlanır

    Eğer cache'deki son dönem, beklenen dönemden eskiyse → invalidate.
    """
    try:
        latest = get_latest_period(cached_data)
        if not latest:
            return False

        year_str, period_str = latest.split("/")
        cached_year = int(year_str)

        # Cache'deki son dönem → çeyrek numarası (FY=4, Q1=1, Q2=2, Q3=3)
        if period_str == "FY":
            cached_q = 4
        elif period_str.startswith("Q"):
            cached_q = int(period_str[1:])
        else:
            return False

        current_month = now.month
        current_year = now.year

        # Beklenen dönem hesapla (tarih → beklenen minimum dönem)
        # Şubat-Mart → en az Q3 olmalı (FY henüz gelmemiş olabilir)
        # Mayıs+ → FY gelmiş olmalı
        # Ağustos+ → FY + Q1 gelmiş olmalı
        # Kasım+ → FY + Q1 + Q2 gelmiş olmalı
        expected_year = current_year
        if current_month >= 11:      # Kasım+ → Q2 verisi gelmiş olmalı
            expected_q = 2
        elif current_month >= 8:     # Ağustos+ → Q1 verisi gelmiş olmalı
            expected_q = 1
            expected_year = current_year
        elif current_month >= 5:     # Mayıs+ → FY verisi gelmiş olmalı
            expected_q = 4
            expected_year = current_year - 1
        elif current_month >= 2:     # Şubat+ → Q3 verisi gelmiş olmalı
            expected_q = 3
            expected_year = current_year - 1
        else:                        # Ocak → henüz yeni dönem beklentisi yok
            return False

        # Cache'deki veri beklenen dönemden eski mi?
        cached_score = cached_year * 10 + cached_q
        expected_score = expected_year * 10 + expected_q

        return cached_score < expected_score

    except Exception:
        return False  # Parse hatası → invalidate yapma


def _cache_get(key: str, bypass_ttl: bool = False):
    """Cache'den veri çek. TTL aşıldıysa veya bulunamazsa None döner.

    Args:
        key: Cache anahtarı
        bypass_ttl: True ise TTL kontrolünü atla (eski veri karşılaştırması için)
    """
    try:
        conn = _cache_connect()
        row = conn.execute(
            "SELECT data, created_at FROM financials_cache WHERE key = ?", (key,)
        ).fetchone()
        if row:
            data_blob, created_at = row
            # Sunucu modunda TTL bypass edilir — veri güncelleme sadece lokalden yapılır,
            # sunucuda "süresi doldu" diye veriyi silmek anlamsız.
            if bypass_ttl or _IS_SERVER_MODE or time.time() - created_at < _get_cache_ttl():
                return pickle.loads(data_blob)
    except Exception:
        pass  # Cache hatası sessizce geçilir
    return None


# ─── Restatement (Retroaktif Düzeltme) Tespiti ───────────────────────────────

_RESTATEMENT_LOG = os.path.join(os.path.expanduser("~/.bbb_cache"), "restatement_log.jsonl")

# Önemli finansal kalemler (restatement tespiti için öncelikli)
_KEY_ITEMS = {
    "3C": "Satış Gelirleri",
    "3D": "Brüt Kar",
    "3DF": "Faaliyet Karı",
    "3I": "Vergi Öncesi Kar",
    "3J": "Net Kar (Sürdürülen)",
    "3L": "Dönem Net Karı",
    "3Z": "Ana Ortaklık Net Karı",
    "1BL": "Toplam Varlıklar",
    "2N": "Özkaynaklar",
    "4C": "İşletme Nakit Akımı",
    "4CB": "Serbest Nakit Akımı",
}

# Restatement olarak sayılacak maksimum yıl (dinamik — enflasyon muhasebesi dahil)
_RESTATEMENT_MAX_YEAR = datetime.now().year - 1  # her zaman geçen yıl ve öncesi


def detect_restatement_changes(
    old_data: dict,
    new_data: dict,
    threshold: float = None,
    ticker: str = "",
    exchange: str = "TRY",
) -> List[dict]:
    """Eski ve yeni finansal veri arasındaki retroaktif düzeltmeleri tespit et.
    
    Aynı period + aynı field için değerleri karşılaştırır. Sadece
    _RESTATEMENT_MAX_YEAR ve öncesindeki dönemlere bakar.
    
    Bankalar için daha toleranslı threshold kullanılır (%10 vs %5) çünkü
    UFRS bankacılık formatında bazı kalemler farklı hesaplanabilir.
    
    Args:
        old_data: Eski finansal veri (cache'deki)
        new_data: Yeni finansal veri (API'dan gelen)
        threshold: Minimum değişim oranı (None=otomatik: banka %10, diğer %5)
        ticker: Ticker sembolü (log için ve banka tespiti için)
        exchange: Borsa (log için)
    
    Returns:
        Restatement listesi: [{ticker, exchange, period, field, field_name,
                               old_value, new_value, diff_pct}]
    """
    restatements = []
    
    if not old_data or not new_data:
        return restatements
    
    # Auto-detect threshold based on ticker
    if threshold is None:
        is_bank = ticker.upper() in BANK_TICKERS if ticker else False
        threshold = 0.10 if is_bank else 0.05
    
    for code, new_item in new_data.items():
        old_item = old_data.get(code)
        if not old_item:
            continue
        
        new_values = new_item.get("values", {})
        old_values = old_item.get("values", {})
        field_name = new_item.get("name_tr", code)
        
        for period_key, new_val in new_values.items():
            # Sadece belirli yıl öncesi dönemlere bak
            try:
                year = int(period_key.split("/")[0])
                if year > _RESTATEMENT_MAX_YEAR:
                    continue
            except (ValueError, IndexError):
                continue
            
            old_val = old_values.get(period_key)
            if old_val is None:
                continue
            
            # Her ikisi de sayısal olmalı
            try:
                old_f = float(old_val)
                new_f = float(new_val)
            except (ValueError, TypeError):
                continue
            
            # Sıfırdan sıfıra değişme → restatement değil
            if old_f == 0 and new_f == 0:
                continue
            
            # Sıfır değer varsa karşılaştırma yapma (bölme hatası)
            if old_f == 0:
                continue
            
            # Değişim oranını hesapla
            diff_pct = abs(new_f - old_f) / abs(old_f)
            
            if diff_pct > threshold:
                restatements.append({
                    "ticker":     ticker,
                    "exchange":   exchange,
                    "period":     period_key,
                    "field":      code,
                    "field_name": field_name,
                    "old_value":  old_f,
                    "new_value":  new_f,
                    "diff_pct":   round(diff_pct * 100, 2),  # yüzde
                })
    
    return restatements


def log_restatements(cache_key: str, restatements: List[dict]) -> None:
    """Restatement'ları JSONL log dosyasına append et.
    
    Dosya yoksa otomatik oluşturulur. Her satır bir JSON nesnesidir.
    
    Args:
        cache_key: Cache key (referans için)
        restatements: detect_restatement_changes() sonucu
    """
    if not restatements:
        return
    
    os.makedirs(os.path.dirname(_RESTATEMENT_LOG), exist_ok=True)
    detected_at = datetime.now().isoformat()
    
    try:
        with open(_RESTATEMENT_LOG, "a", encoding="utf-8") as f:
            for r in restatements:
                entry = {
                    "detected_at": detected_at,
                    "cache_key":   cache_key,
                    **r,
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        pass  # Log hatası sessizce geçilir


def get_expired_cache_tickers(ttl_days: int = 90) -> List[str]:
    """Cache'de TTL süresi dolmuş ticker'ları döndür.
    
    Args:
        ttl_days: TTL gün sayısı (default: 90)
    
    Returns:
        Süresi dolmuş ticker listesi
    """
    try:
        threshold = time.time() - (ttl_days * 24 * 3600)
        conn = _cache_connect()
        rows = conn.execute(
            "SELECT ticker FROM financials_cache WHERE created_at < ?",
            (threshold,)
        ).fetchall()
        return [row[0] for row in rows if row[0]]
    except Exception:
        return []


def _cache_set(key: str, ticker: str, data, detect_restatements: bool = True) -> None:
    """Veriyi cache'e yaz. Restatement tespiti yapar. Başarısızlık sessizce geçilir.
    
    Args:
        key: Cache anahtarı
        ticker: Ticker sembolü
        data: Finansal veri
        detect_restatements: True ise eski veriyle karşılaştırma yap
    """
    try:
        # Restatement tespiti: eski veriyi TTL'ye bakmadan çek
        if detect_restatements:
            old_data = _cache_get(key, bypass_ttl=True)
            if old_data:
                # ticker ve exchange bilgisini key'den çıkaramayız, ticker parametresini kullan
                exchange = "TRY"  # default
                restatements = detect_restatement_changes(
                    old_data, data,
                    threshold=0.05,
                    ticker=ticker,
                    exchange=exchange,
                )
                if restatements:
                    log_restatements(key, restatements)

        # Normal cache yazma (pickle kullanımı mevcut — internal cache, dış girdi yok)
        conn = _cache_connect()
        conn.execute(
            "INSERT OR REPLACE INTO financials_cache (key, ticker, data, created_at) VALUES (?,?,?,?)",
            (key, ticker, pickle.dumps(data), time.time())
        )

        # LRU eviction — max 700 entry, en eski kayıtları sil
        # Not: BIST'te ~600 hisse destekleniyor, 700 yeterli headroom sağlar
        _MAX_CACHE_ENTRIES = 700
        count = conn.execute("SELECT COUNT(*) FROM financials_cache").fetchone()[0]
        if count > _MAX_CACHE_ENTRIES:
            excess = count - _MAX_CACHE_ENTRIES
            conn.execute(
                "DELETE FROM financials_cache WHERE key IN "
                "(SELECT key FROM financials_cache ORDER BY created_at ASC LIMIT ?)",
                (excess,)
            )

        conn.commit()
    except Exception:
        pass


def cache_stats() -> dict:
    """Cache istatistikleri döndür."""
    try:
        conn = _cache_connect()
        count = conn.execute("SELECT COUNT(*) FROM financials_cache").fetchone()[0]
        oldest = conn.execute("SELECT MIN(created_at) FROM financials_cache").fetchone()[0]
        newest = conn.execute("SELECT MAX(created_at) FROM financials_cache").fetchone()[0]
        tickers = conn.execute("SELECT DISTINCT ticker FROM financials_cache").fetchall()
        size_bytes = os.path.getsize(_CACHE_DB) if os.path.exists(_CACHE_DB) else 0
        return {
            "total_entries": count,
            "entry_count": count,  # eski uyumluluk
            "tickers": [t[0] for t in tickers],
            "oldest_entry": oldest,
            "newest_entry": newest,
            "db_size_mb": round(size_bytes / 1024 / 1024, 2),
            "server_mode": _IS_SERVER_MODE,
        }
    except Exception as e:
        return {"error": str(e)}


def cache_clear(ticker: str = None) -> int:
    """Ticker'a ait (veya tüm) cache girdilerini sil. Silinen sayısını döndür."""
    try:
        conn = _cache_connect()
        if ticker:
            c = conn.execute("DELETE FROM financials_cache WHERE ticker = ?", (ticker.upper(),))
        else:
            c = conn.execute("DELETE FROM financials_cache")
        conn.commit()
        deleted = c.rowcount
        return deleted
    except Exception:
        return 0


def cache_warm(tickers: list, start_year: int = None, end_year: int = None,
               verbose: bool = True) -> dict:
    """
    Birden fazla ticker için cache'i önceden doldur (pre-warm).
    Her ticker için fetch_financials() çağırır (2016→bugün arası tüm veri).
    start_year/end_year parametreleri artık sadece filtreleme için kullanılır,
    cache key'ini etkilemez.
    """
    results = {"success": [], "failed": [], "already_cached": []}
    for ticker in tickers:
        key = _cache_key(ticker, "TRY")
        if _cache_get(key) is not None:
            results["already_cached"].append(ticker)
            if verbose:
                logger.debug("[CACHE] %s — zaten cache'de", ticker)
            continue
        if verbose:
            logger.debug("[FETCH] %s — API'den çekiliyor...", ticker)
        data = fetch_financials(ticker)
        if data:
            results["success"].append(ticker)
        else:
            results["failed"].append(ticker)
    return results


# ─── API ──────────────────────────────────────────────────────────────────────
def _detect_financial_group(ticker: str) -> str:
    """Auto-detect: banks use UFRS (2), others use XI_29 (1)."""
    ticker_upper = ticker.upper()
    if ticker_upper in BANK_TICKERS:
        return "2"
    return "1"


def _fetch_year(ticker: str, year: int, exchange: str = "TRY",
                financial_group: Optional[str] = None) -> List[dict]:
    """Fetch 4 quarters of a single year."""
    if financial_group is None:
        financial_group = _detect_financial_group(ticker)

    fg_map = {"1": "XI_29", "2": "UFRS", "3": "UFRS_K", "4": "UFRS_A"}
    fg_label = fg_map.get(financial_group, financial_group)

    params = {
        "companyCode": ticker.upper(),
        "exchange": exchange.upper(),
        "financialGroup": fg_label,
        "year1": year, "period1": 3,
        "year2": year, "period2": 6,
        "year3": year, "period3": 9,
        "year4": year, "period4": 12,
    }

    cached = _raw_cache_get(params)
    if cached is not None:
        return cached

    try:
        resp = requests.get(BASE_URL, params=params, timeout=TIMEOUT, verify=False)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("value", [])
        if items:
            _raw_cache_set(params, items)
        time.sleep(RATE_LIMIT_DELAY)
        return items
    except requests.Timeout:
        logger.warning("Timeout fetching %s %d", ticker, year)
        return None
    except requests.RequestException as e:
        logger.warning("Request error for %s %d: %s", ticker, year, e)
        return None
    except (json.JSONDecodeError, KeyError) as e:
        # JSONDecodeError (Expecting value) hatası alındığında sistemi sonsuz loopa sokmamak için:
        logger.warning("Parse error for %s %d: %s", ticker, year, e)
        return None


def fetch_financials(ticker: str, start_year: int = None, end_year: int = None,
                     exchange: str = "TRY", financial_group: Optional[str] = None,
                     no_cache: bool = False) -> Dict[str, dict]:
    """
    Fetch financial data for a ticker across years.

    Cache davranışı: Her zaman 2016'dan bugüne kadar tüm veri çekilir ve
    cache'e yazılır. start_year/end_year yalnızca döndürülen veriyi filtreler.
    Bu sayede sync scripti ve canlı sayfa istekleri aynı cache key'ini kullanır.

    Returns: dict of {itemCode: {
        'code': str,
        'name_tr': str,
        'name_en': str,
        'values': {period: value, ...}
    }}
    """
    SYNC_START_YEAR = 2016
    now = datetime.now()
    current_year = now.year

    # Cache key: sadece ticker + exchange (yıl bağımsız)
    key = _cache_key(ticker.upper(), exchange)

    # ── Offline-First Strategy: ALWAYS check SQLite Cache First ──
    # no_cache parametresi olsa bile (force refresh hariç) önce cache'e bakıyoruz.
    # Ancak burada no_cache=True ise bypass edilir.
    if not no_cache:
        cached = _cache_get(key)
        if cached is not None:
            # ── D4: Akıllı cache invalidation — yeni dönem beklentisi kontrolü ──
            # Sunucu modunda invalidation yapılmaz — veri sadece lokal güncelleme ile gelir.
            if not _IS_SERVER_MODE and _should_invalidate_for_new_period(cached, now):
                logger.info("Smart invalidation: cache stale for %s — expecting new period", ticker)
                # Cache'i bypass, aşağıda API'den taze veri çekilecek
            else:
                # start_year/end_year filtresi uygula (caller isterse)
                if start_year or end_year:
                    return _filter_by_years(cached, start_year, end_year)
                return cached  # <100ms, NO API CALL

    # ── Sunucu modu: İş Yatırım API'ye gitme ──
    # Sunucuda cache miss → boş dön. Veri güncelleme sadece lokalden yapılır.
    if _IS_SERVER_MODE and not no_cache:
        logger.info("Cache miss for %s — sunucu modunda, API çağrısı yapılmıyor", ticker)
        return {}

    if financial_group is None:
        financial_group = _detect_financial_group(ticker)

    # Her zaman 2016'dan bugüne kadar tüm veriyi çek
    fetch_start = SYNC_START_YEAR
    fetch_end = current_year

    result = {}
    periods = [3, 6, 9, 12]
    consecutive_errors = 0

    for year in range(fetch_start, fetch_end + 1):
        items = _fetch_year(ticker, year, exchange, financial_group)
        
        # Circuit Breaker: If API fails/timeouts consecutively, stop trying
        if items is None:
            consecutive_errors += 1
            if consecutive_errors >= 2:
                logger.warning("Too many errors/timeouts for %s, aborting fetch loop early.", ticker)
                break
            continue  # Skip processing for this failed year
        else:
            consecutive_errors = 0

        if not items:
            # Try other financial groups as fallback (only if no error occurred)
            for alt_fg in ["1", "2", "3", "4"]:
                if alt_fg != financial_group:
                    alt_items = _fetch_year(ticker, year, exchange, alt_fg)
                    if alt_items:  # Found valid data with alt group
                        items = alt_items
                        financial_group = alt_fg
                        break
        
        if not items:
            continue

        for item in items:
            code = item.get("itemCode", "").strip()
            if not code:
                continue

            if code not in result:
                result[code] = {
                    "code": code,
                    "name_tr": (item.get("itemDescTr") or "").strip(),
                    "name_en": (item.get("itemDescEng") or "").strip(),
                    "values": {},
                }

            for i, period in enumerate(periods, 1):
                val_key = f"value{i}"
                val = item.get(val_key)
                if val is not None and val != "None" and val != "":
                    period_key = f"{year}/Q{period // 3}" if period < 12 else f"{year}/FY"
                    try:
                        result[code]["values"][period_key] = float(val)
                    except (ValueError, TypeError):
                        result[code]["values"][period_key] = val

    # ── SQLite Cache'e Yaz (başarılı veya kısmi başarılı sonuçlar) ──
    # no_cache=True bile olsa cache'e yaz — no_cache sadece OKUMA'yı bypass eder,
    # API'den çekilen taze veri her zaman cache'e kaydedilir.
    _cache_set(key, ticker.upper(), result)

    # Caller'ın istediği yıl aralığını filtrele
    if result and (start_year or end_year):
        return _filter_by_years(result, start_year, end_year)

    return result


def get_item(data: dict, code: str, period: Optional[str] = None) -> Any:
    """Get a specific item value. If period is None, returns latest available."""
    item = data.get(code)
    if item is None:
        return None

    values = item.get("values", {})
    if not values:
        return None

    if period:
        return values.get(period)

    # Return latest period value
    sorted_periods = sorted(values.keys())
    if sorted_periods:
        return values[sorted_periods[-1]]
    return None


def get_latest_period(data: dict) -> Optional[str]:
    """Find the latest period with data."""
    all_periods = set()
    for item in data.values():
        all_periods.update(item.get("values", {}).keys())
    if not all_periods:
        return None

    def period_sort_key(p: str):
        # "2025/Q3" → (2025, 3), "2025/FY" → (2025, 4), "2024/Q2" → (2024, 2)
        try:
            year_str, period_str = p.split("/")
            year = int(year_str)
            if period_str == "FY":
                quarter = 4
            elif period_str.startswith("Q"):
                quarter = int(period_str[1:])
            else:
                quarter = 0
            return (year, quarter)
        except Exception:
            return (0, 0)

    return max(all_periods, key=period_sort_key)


# ─── TTM Calculation ─────────────────────────────────────────────────────────
def calculate_ttm(data: dict, code: str) -> Optional[float]:
    """
    Calculate Trailing Twelve Months for income/cashflow items.
    TTM = Latest Q + Previous FY - Same Q last year
    For FY items, just return FY value.
    """
    latest = get_latest_period(data)
    if not latest:
        return None

    item = data.get(code)
    if not item:
        return None

    values = item.get("values", {})

    # If latest is FY, return it directly
    if "/FY" in latest:
        return values.get(latest)

    # Parse latest period
    parts = latest.split("/")
    year = int(parts[0])
    quarter = parts[1]  # Q1, Q2, Q3

    # Need: latest cumulative + prev FY - same quarter last year cumulative
    prev_fy = f"{year - 1}/FY"
    same_q_prev = f"{year - 1}/{quarter}"

    latest_val = values.get(latest)
    prev_fy_val = values.get(prev_fy)
    same_q_prev_val = values.get(same_q_prev)

    if all(v is not None for v in [latest_val, prev_fy_val, same_q_prev_val]):
        try:
            return float(latest_val) + float(prev_fy_val) - float(same_q_prev_val)
        except (ValueError, TypeError):
            return None

    return latest_val  # Fallback to latest


# ─── DCF Data Export ──────────────────────────────────────────────────────────
def _derive_share_count(data: dict, period: str) -> dict:
    """
    Derive basic and diluted share counts.
    
    Priority (Kaya Brief 2026-02-18):
    1. Paid-in Capital (2OA) - Kesin veri (Türk şirketleri nominal 1 TL)
    2. EPS türetme - Yedek (sadece 2OA yoksa)
    
    Türk şirketleri için nominal değer %99 1 TL'dir.
    Hisse sayısı = 2OA değeri (direkt adet, bölme yok).
    """
    result = {"basic_shares": None, "diluted_shares": None, "method": None}
    
    # 1. ÖNCELİK: Paid-in Capital (2OA) - Kesin Veri
    cap_item = data.get("2OA")
    if cap_item:
        val = cap_item.get("values", {}).get(period)
        if val is None:
            # FALLBACK: 2OA'nın kendi en güncel verisi
            # (bazı şirketler bilanço kalemlerini her quarter raporlamıyor)
            sorted_cap_periods = sorted(cap_item.get("values", {}).keys())
            if sorted_cap_periods:
                val = cap_item["values"][sorted_cap_periods[-1]]
        if val is not None:
            try:
                # Veri TL cinsinden geliyor (Örn: 3,509,100,000)
                # Hisse adedi = Tutar / 1 TL (Nominal) = direkt adet
                cap = float(val)
                if cap > 0:
                    # 2OA = Ödenmiş Sermaye (TL)
                    # Nominal 1 TL → hisse adedi = cap (direkt)
                    # Nominal 0.1 TL → hisse adedi = cap / 0.1 = cap * 10
                    # İş Yatırım API'si 2OA'yı TL cinsinden döndürüyor, nominal değer ayrı kontrol edilmeli.
                    # BIST şirketlerinin %99'unda nominal 1 TL → cap direkt adet.
                    # Nominal 0.1 TL şirketler için aşağıda fallback var (EPS türetme doğrular).
                    # TODO: Nominal değer için 2OB (sermaye yapısı) kodu varsa çek.
                    result["basic_shares"] = cap  # Direkt adet (1 TL nominal varsayımı)
                    result["diluted_shares"] = cap
                    result["method"] = "paid_in_capital_1tl_nominal"
                    result["nominal_value_assumed"] = 1.0  # TL
                    return result  # Bulduysan dön, EPS'e bakma
            except (ValueError, TypeError):
                pass

    # 2. YEDEK: EPS Türetme (Sadece 2OA yoksa)
    net_income = None
    # Try parent net income first, then total
    for code in ["3Z", "3L"]:
        item = data.get(code)
        if item:
            val = item.get("values", {}).get(period)
            if val is not None:
                try:
                    net_income = float(val)
                    break
                except (ValueError, TypeError):
                    pass
    
    # Basic EPS → basic shares
    eps_item = data.get("3ZD")
    if eps_item and net_income and net_income != 0:
        eps_val = eps_item.get("values", {}).get(period)
        if eps_val is not None:
            try:
                eps = float(eps_val)
                if eps != 0:
                    basic = net_income / eps
                    if basic > 0:
                        result["basic_shares"] = basic
                        result["method"] = "eps_derived"
            except (ValueError, TypeError):
                pass
    
    # Diluted EPS → diluted shares
    deps_item = data.get("3ZE")
    if deps_item and net_income and net_income != 0:
        deps_val = deps_item.get("values", {}).get(period)
        if deps_val is not None:
            try:
                deps = float(deps_val)
                if deps != 0:
                    diluted = net_income / deps
                    if diluted > 0:
                        result["diluted_shares"] = diluted
            except (ValueError, TypeError):
                pass
    
    # If no diluted, default to basic
    if result["diluted_shares"] is None:
        result["diluted_shares"] = result["basic_shares"]
    
    return result


def get_dcf_data(ticker: str, **kwargs) -> dict:
    """Get all items needed for DCF valuation, including derived metrics."""
    data = fetch_financials(ticker, **kwargs)
    if not data:
        return {"error": f"No data for {ticker}"}

    latest = get_latest_period(data)
    result = {
        "ticker": ticker.upper(),
        "latest_period": latest,
        "currency": kwargs.get("exchange", "TRY"),
        "items": {},
        "ttm": {},
        "derived": {},
    }

    for code in DCF_ITEM_CODES:
        item = data.get(code)
        if item:
            result["items"][code] = {
                "name": item["name_tr"],
                "name_en": item.get("name_en", ""),
                "latest": get_item(data, code),
                "all_periods": item["values"],
            }
            # Calculate TTM for income/cashflow items
            if code.startswith("3") or code.startswith("4"):
                ttm = calculate_ttm(data, code)
                if ttm is not None:
                    result["ttm"][code] = ttm

    # ── Derived Metrics ───────────────────────────────────────────────────
    if latest:
        # Share count (MVP blocker!)
        shares = _derive_share_count(data, latest)
        result["derived"]["shares"] = shares
        
        # Total debt
        st_debt = get_item(data, "2AA", latest)
        lt_debt = get_item(data, "2BA", latest)
        if st_debt is not None or lt_debt is not None:
            result["derived"]["total_debt"] = (
                (float(st_debt) if st_debt else 0) +
                (float(lt_debt) if lt_debt else 0)
            )
        
        # Net debt
        cash = get_item(data, "1AA", latest)
        if cash is not None and "total_debt" in result["derived"]:
            result["derived"]["net_debt"] = (
                result["derived"]["total_debt"] - float(cash)
            )
        
        # Interest Coverage Ratio (ICR = EBIT / Net Interest Expense)
        # FIX (Kaya 2026-02-19): 3HC = Finansal Giderler içinde saf faiz + FX kur farkı zararları var.
        # Çözüm: Net finansman gideri = abs(3HC) - abs(3HB) kullan (3HB = Finansal Gelirler).
        # Bu FROTO gibi büyük net FX pozisyonu olan şirketlerde ICR'ı doğru hesaplar.
        # Use TTM values for income items when latest period is not FY
        # This gives a more accurate 12-month picture vs partial-year cumulative
        ebit_ttm = calculate_ttm(data, "3DF") or calculate_ttm(data, "3HACA")
        interest_ttm = calculate_ttm(data, "3HC") or calculate_ttm(data, "4BB")
        fin_income_ttm = calculate_ttm(data, "3HB")  # Finansal Gelirler (net ICR için)
        # Fallback to point-in-time if TTM unavailable
        ebit = ebit_ttm if ebit_ttm is not None else (get_item(data, "3DF", latest) or get_item(data, "3HACA", latest))
        interest = interest_ttm if interest_ttm is not None else (get_item(data, "3HC", latest) or get_item(data, "4BB", latest))
        fin_income_raw = fin_income_ttm if fin_income_ttm is not None else get_item(data, "3HB", latest)
        if interest is not None:
            result["derived"]["interest_expense"] = abs(float(interest))
        if ebit is not None and interest is not None:
            try:
                int_exp_gross = abs(float(interest))
                fin_income = abs(float(fin_income_raw)) if fin_income_raw is not None else 0.0
                int_exp_net = int_exp_gross - fin_income  # Net finansman gideri
                result["derived"]["interest_expense_gross"] = round(int_exp_gross, 2)
                result["derived"]["fin_income_3hb"] = round(fin_income, 2)
                result["derived"]["interest_expense_net"] = round(int_exp_net, 2)
                if int_exp_net > 0:
                    result["derived"]["icr"] = round(float(ebit) / int_exp_net, 2)
                else:
                    # Net finansman geliri → borçsuz/nakit zengini → ICR = None (AAA territory)
                    result["derived"]["icr"] = None
            except (ValueError, TypeError, ZeroDivisionError):
                pass
        
        # Effective tax rate — TTM bazlı (Damodaran metodolojisi: TTM EBT / TTM Tax)
        # Kümülatif dönem (örn. 9M) yerine trailing 12 aylık vergi yükü kullanılır.
        ebt_ttm = calculate_ttm(data, "3I")
        tax_ttm = calculate_ttm(data, "3IA")
        if ebt_ttm is not None and tax_ttm is not None:
            try:
                if ebt_ttm > 0:
                    result["derived"]["effective_tax_rate"] = round(
                        abs(tax_ttm) / ebt_ttm, 4
                    )
            except (ValueError, TypeError, ZeroDivisionError):
                pass
        else:
            # Fallback: kümülatif dönem (TTM hesaplanamıyorsa — veri eksikliği)
            ebt = get_item(data, "3I", latest)
            tax = get_item(data, "3IA", latest)
            if ebt is not None and tax is not None:
                try:
                    ebt_f = float(ebt)
                    if ebt_f > 0:
                        result["derived"]["effective_tax_rate"] = round(
                            abs(float(tax)) / ebt_f, 4
                        )
                except (ValueError, TypeError, ZeroDivisionError):
                    pass
        
        # NCI flag
        nci_bs = get_item(data, "2ODA", latest)
        nci_pl = get_item(data, "3LB", latest)
        result["derived"]["has_nci"] = (nci_bs is not None and float(nci_bs or 0) != 0)
        if nci_bs is not None:
            result["derived"]["nci_balance_sheet"] = float(nci_bs)
        if nci_pl is not None:
            result["derived"]["nci_income"] = float(nci_pl)
        
        # Finansal Yatırımlar (Kaya Brief 2026-02-18: non_operating_assets için otomatik)
        # 1AB = Kısa vadeli finansal yatırımlar
        # 1BC = Uzun vadeli finansal yatırımlar
        fin_invest_st = get_item(data, "1AB", latest) or 0
        fin_invest_lt = get_item(data, "1BC", latest) or 0
        result["derived"]["financial_investments"] = float(fin_invest_st) + float(fin_invest_lt)
        # P1-C: Ayrı ayrı da expose et (breakdown için)
        result["derived"]["fin_invest_st_1AB"] = float(fin_invest_st)
        result["derived"]["fin_invest_lt_1BC"] = float(fin_invest_lt)
    
    # ── Missing items notes ───────────────────────────────────────────────
    missing = []
    for code, label in [
        ("3DC", "R&D Expenses"),
        ("2ODA", "NCI (Balance Sheet)"),
        ("3LB", "NCI (Income)"),
        ("3HC", "Financial Expenses"),
        ("4CAF", "Working Capital Change"),
        ("3ZE", "Diluted EPS"),
    ]:
        if code not in result["items"]:
            missing.append(f"{code}: {label}")
    if missing:
        result["notes"] = {"missing_items": missing}

    return result


# ─── Display ──────────────────────────────────────────────────────────────────
def format_number(val: Any) -> str:
    """Format large numbers for display."""
    if val is None or val == "" or val == "None":
        return "-"
    try:
        n = float(val)
        if abs(n) >= 1e9:
            return f"{n / 1e9:,.1f}B"
        elif abs(n) >= 1e6:
            return f"{n / 1e6:,.1f}M"
        elif abs(n) >= 1e3:
            return f"{n / 1e3:,.1f}K"
        else:
            return f"{n:,.0f}"
    except (ValueError, TypeError):
        return str(val)


def print_financials(ticker: str, data: dict, section: str = "all"):
    """Pretty-print financial data."""
    latest = get_latest_period(data)
    print(f"\n{'=' * 70}")
    print(f"  {ticker.upper()} — Finansal Tablolar (Kaynak: İş Yatırım)")
    print(f"  Son Dönem: {latest}")
    print(f"{'=' * 70}")

    sections = {
        "balance": ("BİLANÇO", BALANCE_SHEET_CODES),
        "income": ("GELİR TABLOSU", INCOME_CODES),
        "cashflow": ("NAKİT AKIŞ TABLOSU", CASHFLOW_CODES),
    }

    for key, (title, codes) in sections.items():
        if section != "all" and section != key:
            continue
        print(f"\n  ── {title} ──")
        for code, label in codes.items():
            val = get_item(data, code)
            print(f"  {code:8s} {label:55s} {format_number(val):>15s}")

    print()


def print_all_items(ticker: str, data: dict, period: Optional[str] = None):
    """Print ALL financial items (not just summary)."""
    latest = period or get_latest_period(data)
    print(f"\n{'=' * 80}")
    print(f"  {ticker.upper()} — TÜM FİNANSAL KALEMLER ({latest})")
    print(f"{'=' * 80}")

    for code in sorted(data.keys()):
        item = data[code]
        val = item["values"].get(latest) if latest else None
        indent = "  " if len(code) <= 3 else "    " if len(code) <= 5 else "      "
        print(f"{indent}{code:10s} {item['name_tr']:55s} {format_number(val):>15s}")

    print(f"\n  Toplam kalem sayısı: {len(data)}")


# ─── CLI Yardımcı Fonksiyonlar ────────────────────────────────────────────────

def _cli_smart_refresh():
    """Akıllı güncelleme: İş Yatırım'da yeni FY verisi olanları tespit et, sadece onları güncelle."""
    import pickle

    # Dinamik yıl: Ocak-Nisan → önceki yılın FY'si aranır (yıllık raporlar Şubat-Mart açıklanır)
    _now = datetime.now()
    target_fy_year = _now.year - 1
    target_fy_label = f"{target_fy_year}/FY"

    stats = cache_stats()
    if stats.get("total_entries", 0) == 0:
        print("❌ Cache boş! Önce --cache-warm ile doldurun.")
        return

    conn = _cache_connect()
    rows = conn.execute("SELECT ticker, data FROM financials_cache").fetchall()

    # Hangi hisselerin hedef FY verisi YOK?
    needs_check = []
    already_fy = 0
    for ticker, data_blob in rows:
        data = pickle.loads(data_blob)
        has_fy = False
        for item_data in data.values():
            if target_fy_label in item_data.get("values", {}):
                has_fy = True
                break
        if has_fy:
            already_fy += 1
        else:
            needs_check.append(ticker)

    print(f"━━━ AKILLI GÜNCELLEME ({target_fy_label}) ━━━")
    print(f"  Toplam hisse:     {len(rows)}")
    print(f"  Zaten {target_fy_label}:  {already_fy}")
    print(f"  Kontrol edilecek: {len(needs_check)}")
    print()

    if not needs_check:
        print("✅ Tüm hisseler güncel!")
        return

    # Aşama 1: Hafif probe — yeni FY verisi var mı?
    print(f"🔍 Aşama 1: {len(needs_check)} hissede yeni FY yoklaması...")
    has_new_fy = []
    errors = []
    for i, ticker in enumerate(needs_check, 1):
        try:
            fg = _detect_financial_group(ticker)
            params = {
                "companyCode": ticker, "exchange": "TRY",
                "financialGroup": "UFRS" if fg == "2" else "XI_29",
                "year1": target_fy_year, "period1": 12,
                "year2": target_fy_year, "period2": 12,
                "year3": target_fy_year, "period3": 12,
                "year4": target_fy_year, "period4": 12,
            }
            resp = requests.get(BASE_URL, params=params, timeout=TIMEOUT, verify=False)
            items = resp.json().get("value", [])
            if items:
                has_new_fy.append(ticker)
            if i % 50 == 0:
                print(f"  ... {i}/{len(needs_check)} kontrol edildi", flush=True)
        except Exception as e:
            errors.append(ticker)
        time.sleep(RATE_LIMIT_DELAY)

    print(f"\n  Yeni FY tespit:   {len(has_new_fy)} hisse")
    print(f"  Hata:             {len(errors)} hisse")

    if not has_new_fy:
        print("\n✅ Yeni FY verisi olan hisse bulunamadı.")
        return

    # Aşama 2: Sadece yeni FY olanları tam güncelle
    print(f"\n📥 Aşama 2: {len(has_new_fy)} hisse güncelleniyor...")
    ok = 0
    for i, ticker in enumerate(has_new_fy, 1):
        try:
            # Raw JSON cache'i hedef yıl için sil — eski Q3 verisini bypass et
            _invalidate_raw_cache_for_year(ticker, target_fy_year)
            data = fetch_financials(ticker, no_cache=True)
            if data:
                ok += 1
            print(f"  [{i}/{len(has_new_fy)}] ✅ {ticker}: {len(data)} kalem", flush=True)
        except Exception as e:
            print(f"  [{i}/{len(has_new_fy)}] ❌ {ticker}: {e}", flush=True)
        time.sleep(RATE_LIMIT_DELAY)

    print(f"\n★ SONUÇ: {ok}/{len(has_new_fy)} başarıyla güncellendi")
    new_stats = cache_stats()
    print(f"  Cache: {new_stats.get('total_entries', '?')} hisse, {new_stats.get('db_size_mb', '?')} MB")


def _cli_refresh_all():
    """Tüm cache'deki hisseleri İş Yatırım'dan yeniden çek."""
    stats = cache_stats()
    tickers = stats.get("tickers", [])
    if not tickers:
        print("❌ Cache boş!")
        return

    print(f"🔄 {len(tickers)} hisse yeniden çekiliyor...")
    print("⚠️  Bu işlem uzun sürebilir (~15-20 dakika)")

    ok = 0
    fail = []
    for i, ticker in enumerate(tickers, 1):
        try:
            data = fetch_financials(ticker, no_cache=True)
            if data:
                ok += 1
            if i % 25 == 0:
                print(f"  ... {i}/{len(tickers)} tamamlandı", flush=True)
        except Exception:
            fail.append(ticker)
        time.sleep(RATE_LIMIT_DELAY)

    print(f"\n★ SONUÇ: {ok}/{len(tickers)} başarılı, {len(fail)} hata")
    if fail:
        print(f"  Hatalı: {', '.join(fail[:20])}")


# ─── Fiyat & Endeks (isyatirimhisse) ─────────────────────────────────────────

def get_stock_price(ticker: str, start_date: str = None, end_date: str = None):
    """
    BIST hisse fiyat verilerini getirir (OHLCV, günlük).

    Args:
        ticker: Hisse kodu (örn: THYAO)
        start_date: Başlangıç tarihi (dd-mm-yyyy). Varsayılan: 1 yıl önce
        end_date: Bitiş tarihi (dd-mm-yyyy). Varsayılan: bugün

    Returns:
        pandas.DataFrame veya None
    """
    try:
        from isyatirimhisse import fetch_stock_data
    except ImportError:
        logger.error("isyatirimhisse paketi yüklü değil: pip install isyatirimhisse")
        return None

    if not start_date:
        start_date = (_date.today() - _timedelta(days=365)).strftime('%d-%m-%Y')
    if not end_date:
        end_date = _date.today().strftime('%d-%m-%Y')

    try:
        df = fetch_stock_data(symbols=ticker, start_date=start_date, end_date=end_date)
        return df
    except Exception as e:
        logger.error("Fiyat verisi alınamadı (%s): %s", ticker, e)
        return None


def get_index_data(index: str = "XU100", start_date: str = None, end_date: str = None):
    """
    BIST endeks verilerini getirir (XU100, XU030, vb.).

    Args:
        index: Endeks kodu (örn: XU100)
        start_date: Başlangıç tarihi (dd-mm-yyyy). Varsayılan: 1 yıl önce
        end_date: Bitiş tarihi (dd-mm-yyyy). Varsayılan: bugün

    Returns:
        pandas.DataFrame veya None
    """
    try:
        from isyatirimhisse import fetch_index_data
    except ImportError:
        logger.error("isyatirimhisse paketi yüklü değil: pip install isyatirimhisse")
        return None

    if not start_date:
        start_date = (_date.today() - _timedelta(days=365)).strftime('%d-%m-%Y')
    if not end_date:
        end_date = _date.today().strftime('%d-%m-%Y')

    try:
        df = fetch_index_data(indices=index, start_date=start_date, end_date=end_date)
        return df
    except Exception as e:
        logger.error("Endeks verisi alınamadı (%s): %s", index, e)
        return None


def _print_summary(ticker: str):
    """Hisse özet kartı: fiyat, market cap, pay sayısı, temel çarpanlar."""
    ticker = ticker.upper()

    # 1. DCF data (türetilmiş veriler + TTM dahil)
    dcf = get_dcf_data(ticker)
    if not dcf or not dcf.get("ttm"):
        print(f"[HATA] {ticker} için veri bulunamadı.", file=sys.stderr)
        return

    ttm = dcf.get("ttm", {})
    derived = dcf.get("derived", {})
    latest = dcf.get("latest_period", "?")

    # 2. Pay sayısı
    shares_info = derived.get("shares", {})
    if isinstance(shares_info, dict):
        shares = shares_info.get("basic_shares", 0)
    else:
        shares = 0

    # 3. Son fiyat (isyatirimhisse DataFrame: HGDG_KAPANIS, PD, SERMAYE)
    price = None
    market_cap = None
    price_date = None
    market_cap_usd = None
    try:
        df = get_stock_price(ticker)
        if df is not None and len(df) > 0:
            last = df.iloc[-1]
            price = float(last.get("HGDG_KAPANIS", 0) or 0) or None
            market_cap = float(last.get("PD", 0) or 0) or None
            market_cap_usd = float(last.get("PD_USD", 0) or 0) or None
            price_date = str(last.get("HGDG_TARIH", ""))[:10]
    except Exception:
        pass

    if market_cap is None:
        market_cap = (price * shares) if (price and shares) else None
    revenue = ttm.get("3C", 0)
    ebit = ttm.get("3DF", 0)
    net_income = ttm.get("3J", 0)
    da = ttm.get("4B", 0) or ttm.get("4CAB", 0)
    ebitda = (ebit + da) if ebit and da else None
    net_debt = derived.get("net_debt", 0)
    ev = (market_cap + net_debt) if market_cap else None
    icr = derived.get("icr", None)
    eff_tax = derived.get("effective_tax_rate", None)

    # Marjlar
    gross_margin = (ttm.get("3D", 0) / revenue * 100) if revenue else None
    ebit_margin = (ebit / revenue * 100) if revenue else None
    net_margin = (net_income / revenue * 100) if revenue else None

    # Çarpanlar
    pe = (market_cap / net_income) if (market_cap and net_income and net_income > 0) else None
    ev_ebitda = (ev / ebitda) if (ev and ebitda and ebitda > 0) else None
    pb = None
    equity = None
    try:
        fin_data = fetch_financials(ticker, start_year=2025, end_year=2025)
        if fin_data and "2O" in fin_data:
            vals = fin_data["2O"]["values"]
            # Son FY veya Q değerini al
            for p in sorted(vals.keys(), reverse=True):
                equity = vals[p]
                break
            if equity and equity > 0 and market_cap:
                pb = market_cap / equity
    except Exception:
        pass

    # EPS
    eps = (net_income / shares) if (net_income and shares) else None

    # ROIC
    roic = None
    try:
        total_debt = derived.get("total_debt", 0)
        fin_data2 = fetch_financials(ticker, start_year=2025, end_year=2025)
        if fin_data2 and "2N" in fin_data2:
            equity_total = None
            cash = None
            for p in sorted(fin_data2["2N"]["values"].keys(), reverse=True):
                equity_total = fin_data2["2N"]["values"][p]
                break
            if "1AA" in fin_data2:
                for p in sorted(fin_data2["1AA"]["values"].keys(), reverse=True):
                    cash = fin_data2["1AA"]["values"][p]
                    break
            if equity_total and cash is not None:
                ic = equity_total + total_debt - cash
                nopat = ebit * (1 - (eff_tax or 0.22)) if ebit else None
                if nopat and ic and ic > 0:
                    roic = nopat / ic * 100
    except Exception:
        pass

    # FCF
    ocf = ttm.get("4C", None)
    capex = ttm.get("4CAI", None)
    fcf = (ocf - abs(capex)) if (ocf is not None and capex is not None) else None

    # 5. Çıktı
    def fmt(v, suffix="", div=1, decimals=0):
        if v is None:
            return "—"
        v2 = v / div
        if decimals == 0:
            return f"{v2:,.0f}{suffix}"
        return f"{v2:,.{decimals}f}{suffix}"

    def fmtb(v):
        """Milyar TL formatı"""
        if v is None:
            return "—"
        return f"{v/1e9:,.1f}B TL"

    price_line = f"{fmt(price, ' TL', decimals=2)}"
    if price_date:
        price_line += f"  ({price_date})"

    mcap_line = fmtb(market_cap)
    if market_cap_usd:
        mcap_line += f"  (${market_cap_usd/1e9:,.1f}B)"

    print(f"""
╔══════════════════════════════════════════════════════╗
  {ticker} — ÖZET KART
  Son dönem: {latest} | Para birimi: TRY
╚══════════════════════════════════════════════════════╝

  Fiyat               : {price_line}
  Pay Sayısı          : {fmt(shares)}
  Piyasa Değeri       : {mcap_line}
  Net Borç            : {fmtb(net_debt)}
  Firma Değeri (EV)   : {fmtb(ev)}

  ── TTM FİNANSALLAR ──
  Hasılat              : {fmtb(revenue)}
  EBITDA               : {fmtb(ebitda)}
  Faaliyet Kârı (EBIT) : {fmtb(ebit)}
  Net Kâr              : {fmtb(net_income)}
  FCF                  : {fmtb(fcf)}

  ── MARJLAR ──
  Brüt Marj            : {fmt(gross_margin, '%', decimals=1) if gross_margin else '—'}
  EBIT Marjı           : {fmt(ebit_margin, '%', decimals=1) if ebit_margin else '—'}
  Net Marj             : {fmt(net_margin, '%', decimals=1) if net_margin else '—'}

  ── ÇARPANLAR ──
  F/K (P/E)            : {fmt(pe, 'x', decimals=1) if pe else '—'}
  FD/FAVÖK (EV/EBITDA) : {fmt(ev_ebitda, 'x', decimals=1) if ev_ebitda else '—'}
  PD/DD (P/BV)         : {fmt(pb, 'x', decimals=1) if pb else '—'}
  EPS                  : {fmt(eps, ' TL', decimals=2) if eps else '—'}

  ── VERİMLİLİK ──
  ROIC                 : {fmt(roic, '%', decimals=1) if roic else '—'}
  ICR                  : {fmt(icr, 'x', decimals=1) if icr else '—'}
  Efektif Vergi Oranı  : {fmt(eff_tax*100 if eff_tax else None, '%', decimals=1)}
""")


def _print_stock_price(ticker: str, start_date: str = None, end_date: str = None):
    """CLI: Fiyat verisini ekrana bas."""
    df = get_stock_price(ticker, start_date, end_date)
    if df is None or (hasattr(df, 'empty') and df.empty):
        print(f"[HATA] {ticker} fiyat verisi bulunamadı.", file=sys.stderr)
        return
    # Son 10 gün
    cols = [c for c in ['HGDG_TARIH', 'HGDG_KAPANIS', 'HGDG_MIN', 'HGDG_MAX', 'HGDG_HACIM'] if c in df.columns]
    if not cols:
        cols = list(df.columns)
    tail = df[cols].tail(10)
    print(f"\n{'='*70}")
    print(f"  {ticker} — Fiyat Verileri (Son {len(tail)} gün)")
    print(f"{'='*70}")
    for _, row in tail.iterrows():
        parts = []
        for c in cols:
            val = row[c]
            if 'TARIH' in c:
                parts.append(f"  {val}")
            elif 'HACIM' in c:
                parts.append(f"  Hacim: {val:,.0f}")
            else:
                label = c.replace('HGDG_', '')
                parts.append(f"  {label}: {val:.2f}")
        print("".join(parts))
    print()


def _print_index_data(index: str, start_date: str = None, end_date: str = None):
    """CLI: Endeks verisini ekrana bas."""
    df = get_index_data(index, start_date, end_date)
    if df is None or (hasattr(df, 'empty') and df.empty):
        print(f"[HATA] {index} endeks verisi bulunamadı.", file=sys.stderr)
        return
    tail = df.tail(10)
    print(f"\n{'='*70}")
    print(f"  {index} — Endeks (Son {len(tail)} gün)")
    print(f"{'='*70}")
    for _, row in tail.iterrows():
        date_val = row.get('DATE', row.get('HGDG_TARIH', ''))
        val = row.get('VALUE', row.get('END_DEGER', ''))
        try:
            print(f"  {date_val}  {float(val):>12,.2f}")
        except (ValueError, TypeError):
            print(f"  {date_val}  {val}")
    print()


# ─── CLI ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="BBB Finans — İş Yatırım Finansal Tablo")
    parser.add_argument("ticker", nargs="?", help="Hisse kodu (örn: THYAO)")
    parser.add_argument("--start-year", type=int, help="Başlangıç yılı")
    parser.add_argument("--end-year", type=int, help="Bitiş yılı")
    parser.add_argument("--exchange", default="TRY", choices=["TRY", "USD"])
    parser.add_argument("--group", choices=["1", "2", "3"],
                        help="Finansal grup (1=XI_29, 2=UFRS, 3=UFRS_K). Otomatik seçilir.")
    parser.add_argument("--section", default="all",
                        choices=["all", "balance", "income", "cashflow"],
                        help="Gösterilecek tablo")
    parser.add_argument("--full", action="store_true", help="Tüm kalemleri göster")
    parser.add_argument("--dcf", action="store_true", help="DCF için JSON çıktı")
    parser.add_argument("--json", action="store_true", help="JSON çıktı")
    parser.add_argument("--period", help="Belirli dönem (örn: 2024/FY veya 2024/Q3)")
    # ── Cache CLI ──
    parser.add_argument("--cache-stats", action="store_true", dest="cache_stats",
                        help="SQLite cache istatistiklerini göster")
    parser.add_argument("--cache-clear", metavar="TICKER|ALL", dest="cache_clear",
                        help="Ticker (veya ALL) için cache'i temizle")
    parser.add_argument("--cache-warm", nargs="+", metavar="TICKER", dest="cache_warm",
                        help="Belirtilen ticker'lar için cache'i ön ısıt")
    parser.add_argument("--no-cache", action="store_true", dest="no_cache",
                        help="SQLite cache'i bypass et (her zaman API'den çek)")
    parser.add_argument("--smart-refresh", action="store_true", dest="smart_refresh",
                        help="Akıllı güncelleme: yeni FY verisi olanları tespit et ve güncelle")
    parser.add_argument("--refresh-all", action="store_true", dest="refresh_all",
                        help="Tüm cache'deki hisseleri İş Yatırım'dan yeniden çek")
    # ── Fiyat & Endeks CLI ──
    parser.add_argument("--price", action="store_true",
                        help="Hisse fiyat verileri (OHLCV, son 1 yıl)")
    parser.add_argument("--index", metavar="INDEX",
                        help="Endeks verileri (örn: XU100, XU030)")
    parser.add_argument("--summary", action="store_true",
                        help="Özet kart: fiyat, market cap, pay sayısı, temel çarpanlar")

    args = parser.parse_args()

    # ── Summary ──
    if args.summary:
        if not args.ticker:
            print("[HATA] --summary için ticker gerekli (örn: THYAO)", file=sys.stderr)
            sys.exit(1)
        _print_summary(args.ticker)
        return

    # ── Fiyat & Endeks ──
    if args.price:
        if not args.ticker:
            print("[HATA] --price için ticker gerekli (örn: THYAO)", file=sys.stderr)
            sys.exit(1)
        _print_stock_price(args.ticker)
        return

    if args.index:
        _print_index_data(args.index)
        return

    # ── Cache komutları ──
    if args.cache_stats:
        print(json.dumps(cache_stats(), indent=2, default=str))
        return

    if args.cache_clear:
        target = None if args.cache_clear.upper() == "ALL" else args.cache_clear
        n = cache_clear(target)
        label = args.cache_clear.upper() if target else "TÜM"
        print(f"Silindi: {n} entry ({label})")
        return

    if args.cache_warm:
        sy = args.start_year or 2019
        ey = args.end_year or 2026
        result = cache_warm(args.cache_warm, start_year=sy, end_year=ey, verbose=True)
        print(f"\nSonuç: {result}")
        return

    if args.smart_refresh:
        _cli_smart_refresh()
        return

    if args.refresh_all:
        _cli_refresh_all()
        return

    if not args.ticker:
        parser.print_help()
        sys.exit(1)

    kwargs = {"exchange": args.exchange}
    if args.start_year:
        kwargs["start_year"] = args.start_year
    if args.end_year:
        kwargs["end_year"] = args.end_year
    if args.group:
        kwargs["financial_group"] = args.group
    if args.no_cache:
        kwargs["no_cache"] = True

    if args.dcf:
        result = get_dcf_data(args.ticker, **kwargs)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    data = fetch_financials(args.ticker, **kwargs)

    if not data:
        print(f"[HATA] {args.ticker} için veri bulunamadı.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        # Convert to serializable format
        output = {}
        for code, item in data.items():
            output[code] = {
                "name_tr": item["name_tr"],
                "name_en": item["name_en"],
                "values": {k: v for k, v in item["values"].items()},
            }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    if args.full:
        print_all_items(args.ticker, data, args.period)
    else:
        print_financials(args.ticker, data, args.section)


if __name__ == "__main__":
    main()
