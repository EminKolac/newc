#!/usr/bin/env python3
"""KAP Sinyal Toplayıcı — Günlük bildirim toplama, filtreleme, PDF indirme + metin çıkarma.

Çıktı: temp/kap_signals_YYYY-MM-DD.json
Her sinyal: ticker, title, date, signal_type, full_text, pdf_texts[], pdf_paths[]

Kullanım:
  python3 kap_signal_collector.py                    # Dünün sinyalleri
  python3 kap_signal_collector.py --date 2026-03-24  # Belirli tarih
  python3 kap_signal_collector.py --dry-run           # JSON yazmadan özet
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# KAP modülleri
sys.path.insert(0, str(Path(__file__).parent))
from kap.client import KAPClient
from kap.fetcher import KAPFetcher
from kap.archiver import KAPArchiver
from kap.models import KAP_BASE

logger = logging.getLogger(__name__)

# ── Sabitler ──

WORKSPACE_KAYA = Path(os.path.expanduser("~/.openclaw/workspace-kaya"))
RESEARCH_COMPANIES = WORKSPACE_KAYA / "research" / "companies"
TEMP_DIR = WORKSPACE_KAYA / "temp"
PDF_BASE_DIR = TEMP_DIR / "kap_pdfs"

# Watchlist = research/companies/ altındaki ticker klasörleri
def _load_watchlist() -> set:
    if not RESEARCH_COMPANIES.exists():
        return set()
    return {
        p.name for p in RESEARCH_COMPANIES.iterdir()
        if p.is_dir() and not p.name.startswith("_") and not p.name.startswith(".")
    }


def _extract_pdf_text(pdf_path: Path) -> str:
    """PyMuPDF ile PDF'den metin çıkar."""
    try:
        import pymupdf
        doc = pymupdf.open(str(pdf_path))
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except ImportError:
        logger.warning("pymupdf yüklü değil, PDF metin çıkarma atlanıyor")
        return ""
    except Exception as e:
        logger.warning(f"PDF okuma hatası {pdf_path}: {e}")
        return ""


def collect_signals(date_str: str, dry_run: bool = False) -> dict:
    """Belirli bir tarihin KAP sinyallerini topla, PDF'leri indir ve metin çıkar."""

    t_start = time.time()

    # 1. Bildirimleri çek ve filtrele
    client = KAPClient()
    fetcher = KAPFetcher(client)
    archiver = KAPArchiver(fetcher)

    print(f"📡 {date_str} bildirimleri çekiliyor...")
    all_discs = fetcher.fetch_by_date(date_str)
    print(f"   Toplam: {len(all_discs)} bildirim")

    signals = fetcher.filter_signals(all_discs)
    print(f"   Sinyal: {len(signals)} (elenen: {len(all_discs) - len(signals)})")

    # Watchlist
    watchlist = _load_watchlist()
    print(f"   Watchlist: {len(watchlist)} ticker")

    # Sinyal dağılımı
    from collections import Counter
    type_counts = Counter(s for s, _ in signals)
    for stype in ["TEZ", "YAPISAL", "FINANSAL", "KURUMSAL", "DIGER"]:
        if type_counts.get(stype):
            print(f"   {stype}: {type_counts[stype]}")

    if dry_run:
        # Watchlist sinyalleri
        wl_signals = [(s, d) for s, d in signals
                      if any(t.strip() in watchlist for t in (d.ticker or "").split(","))]
        print(f"\n   Watchlist sinyalleri: {len(wl_signals)}")
        for s, d in wl_signals:
            print(f"     [{s:>9}] {d.ticker:>10} | {(d.summary or '')[:55]}")
        return {"dry_run": True, "total": len(all_discs), "signals": len(signals)}

    # 2. PDF dizini hazırla
    pdf_dir = PDF_BASE_DIR / date_str
    pdf_dir.mkdir(parents=True, exist_ok=True)

    # 3. Her sinyal için detay + PDF işle
    results = []
    pdf_download_count = 0
    pdf_read_count = 0
    detail_count = 0

    for signal_type, disc in signals:
        tickers = [t.strip() for t in (disc.ticker or "").split(",")]
        in_watchlist = any(t in watchlist for t in tickers)

        entry = {
            "ticker": disc.ticker,
            "company": disc.company,
            "title": disc.title,
            "summary": disc.summary or "",
            "date": disc.date.isoformat() if disc.date else "",
            "signal_type": signal_type,
            "category": disc.category,
            "kap_id": str(disc.id),
            "kap_url": disc.url or f"https://www.kap.org.tr/tr/Bildirim/{disc.id}",
            "attachment_count": disc.attachment_count or 0,
            "in_watchlist": in_watchlist,
            "full_text": "",
            "pdf_count": 0,
            "pdf_texts": [],
            "pdf_paths": [],
        }

        # Detay çek (bildirim tam metni)
        try:
            detail = fetcher.fetch_detail(str(disc.id))
            if detail:
                entry["full_text"] = detail.content or ""
                detail_count += 1

                # PDF ekleri indir ve oku
                if detail.attachments:
                    # Watchlist → research/companies/{TICKER}/kaynaklar/
                    # Diğerleri → temp/kap_pdfs/{date}/{TICKER}/
                    primary_ticker = tickers[0] if tickers else "UNKNOWN"
                    if in_watchlist:
                        ticker_pdf_dir = RESEARCH_COMPANIES / primary_ticker / "kaynaklar"
                    else:
                        ticker_pdf_dir = pdf_dir / primary_ticker
                    ticker_pdf_dir.mkdir(parents=True, exist_ok=True)

                    for att in detail.attachments:
                        # İndir
                        ext = att.file_extension or "pdf"
                        safe_name = f"{date_str}_{disc.id}_{att.safe_file_name}"
                        # Uzantı zaten dosya adında olabilir — çift uzantıyı önle
                        if not any(safe_name.lower().endswith(f".{e}") for e in ("pdf", "xlsx", "docx", "zip", "jpg", "png")):
                            safe_name = f"{safe_name}.{ext}"
                        dest_path = ticker_pdf_dir / safe_name

                        if not dest_path.exists():
                            url = att.download_url
                            success = client.download_file(url, dest_path)
                            if success:
                                pdf_download_count += 1
                            else:
                                logger.warning(f"İndirilemedi: {att.file_name}")
                                continue

                        # Metin çıkar
                        if dest_path.exists() and ext.lower() in ("pdf", ""):
                            text = _extract_pdf_text(dest_path)
                            if text:
                                entry["pdf_texts"].append(text)
                                entry["pdf_paths"].append(str(dest_path.relative_to(WORKSPACE_KAYA)))
                                pdf_read_count += 1
                        elif dest_path.exists():
                            # PDF olmayan ek (xlsx, docx vb.) — path'i kaydet ama metin çıkarma
                            entry["pdf_paths"].append(str(dest_path.relative_to(WORKSPACE_KAYA)))

                    entry["pdf_count"] = len(entry["pdf_paths"])

        except Exception as e:
            logger.warning(f"Detay çekme hatası {disc.id}: {e}")

        results.append(entry)

    # 4. JSON çıktısı
    output = {
        "date": date_str,
        "collected_at": datetime.now().isoformat(),
        "total_disclosures": len(all_discs),
        "total_signals": len(signals),
        "eliminated": len(all_discs) - len(signals),
        "watchlist_size": len(watchlist),
        "watchlist_signals": sum(1 for r in results if r["in_watchlist"]),
        "detail_fetched": detail_count,
        "pdfs_downloaded": pdf_download_count,
        "pdfs_read": pdf_read_count,
        "duration_seconds": round(time.time() - t_start, 1),
        "type_breakdown": {
            "TEZ": type_counts.get("TEZ", 0),
            "YAPISAL": type_counts.get("YAPISAL", 0),
            "FINANSAL": type_counts.get("FINANSAL", 0),
            "KURUMSAL": type_counts.get("KURUMSAL", 0),
            "DIGER": type_counts.get("DIGER", 0),
        },
        "signals": results,
    }

    # Kaydet
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    out_path = TEMP_DIR / f"kap_signals_{date_str}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Tamamlandı ({output['duration_seconds']}s)")
    print(f"   Detay: {detail_count} | PDF indirme: {pdf_download_count} | PDF okuma: {pdf_read_count}")
    print(f"   Watchlist sinyali: {output['watchlist_signals']}/{len(results)}")
    print(f"   Çıktı: {out_path}")

    return output


def main():
    parser = argparse.ArgumentParser(description="KAP Sinyal Toplayıcı")
    parser.add_argument("--date", help="Tarih (YYYY-MM-DD). Varsayılan: dün.")
    parser.add_argument("--dry-run", action="store_true", help="JSON yazmadan özet göster")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    if args.date:
        date_str = args.date
    else:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = yesterday.strftime("%Y-%m-%d")

    result = collect_signals(date_str, dry_run=args.dry_run)

    # Çıktı özeti (cron raporu için)
    if not args.dry_run:
        print(f"\n📊 Özet: {result['total_signals']} sinyal "
              f"(TEZ:{result['type_breakdown']['TEZ']} "
              f"YAPISAL:{result['type_breakdown']['YAPISAL']} "
              f"FİNANSAL:{result['type_breakdown']['FINANSAL']} "
              f"KURUMSAL:{result['type_breakdown']['KURUMSAL']})")


if __name__ == "__main__":
    main()
