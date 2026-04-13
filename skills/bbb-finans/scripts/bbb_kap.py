#!/usr/bin/env python3
"""
BBB KAP - Modular KAP.org.tr Entegrasyonu

KAP.org.tr'den bildirim, sirket profili, finansal ozet ve tam finansal tablo verilerini ceker.
Bildirim arsivleme ve PDF indirme destegi.

Kullanim:
    bbb kap EBEBK                          # Son bildirimler (varsayilan 20)
    bbb kap EBEBK --all                    # Tum bildirimler (150+)
    bbb kap EBEBK --last 6m               # Son 6 ay
    bbb kap EBEBK --last 3m --category ODA # Son 3 ay ODA'lar
    bbb kap EBEBK --id 1564560            # Bildirim detayi + ek dosyalar
    bbb kap EBEBK --archive               # Toplu arsivleme (kap_docs/ klasorune)
    bbb kap EBEBK --archive --last 1y     # Son 1 yil arsivle
    bbb kap EBEBK --download <objId>      # Tek ek dosya indir
    bbb kap EBEBK --profile               # Sirket profili
    bbb kap EBEBK --kap-summary           # KAP finansal ozet
    bbb kap EBEBK --summary               # Ozet gorunum
    bbb kap EBEBK --financials            # Finansal bildirimler
    bbb kap EBEBK --lookup                # Sirket bilgisi
    bbb kap --today                       # Bugunun bildirimleri
    bbb kap --today --category ODA        # Bugun sadece ODA'lar
    bbb kap --date 2026-03-24             # Belirli tarihin tum bildirimleri
    bbb kap --date 2026-03-24 --category ODA  # Belirli tarih + kategori filtre
    bbb kap search "temettu"              # Anahtar kelime aramasi
    bbb kap EBEBK --json                  # JSON cikti
"""

import argparse
import json
import os
import sys
from pathlib import Path

# kap package'i ayni dizinde
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kap.client import KAPClient
from kap.fetcher import KAPFetcher
from kap.archiver import KAPArchiver
from kap.formatter import (
    format_disclosures, format_detail, format_profile,
    format_summary, format_search_results, format_archive_result,
    format_kap_summary,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="BBB KAP - KAP.org.tr Entegrasyonu",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("ticker", nargs="?", help="Hisse kodu (EBEBK, THYAO) veya 'search'")
    parser.add_argument("keyword", nargs="?", help="Arama kelimesi (search komutu ile)")
    parser.add_argument("--json", action="store_true", help="JSON cikti formati")

    # Bildirim komutlari
    grp = parser.add_argument_group("Bildirim komutlari")
    grp.add_argument("--all", action="store_true", help="Tum bildirimler")
    grp.add_argument("--last", type=str, metavar="SURE",
                     help="Zaman filtresi: 1w, 2w, 1m, 3m, 6m, 1y")
    grp.add_argument("--category", type=str, metavar="KAT",
                     help="Kategori: ODA, FR, GK, TEM, SA, YON, ORT, DG")
    grp.add_argument("--limit", type=int, default=20, help="Sonuc limiti (varsayilan: 20)")
    grp.add_argument("--id", type=str, metavar="ID", help="Bildirim detayi")

    # Sirket bilgi komutlari
    grp2 = parser.add_argument_group("Sirket bilgi komutlari")
    grp2.add_argument("--profile", action="store_true", help="Sirket profili")
    grp2.add_argument("--lookup", action="store_true", help="Sirket bilgisi (memberOid, sektor)")
    grp2.add_argument("--kap-summary", action="store_true", help="KAP finansal ozet")
    grp2.add_argument("--summary", action="store_true", help="Ozet gorunum")
    grp2.add_argument("--financials", action="store_true", help="Finansal bildirimler")
    grp2.add_argument("--today", action="store_true", help="Bugunun bildirimleri")
    grp2.add_argument("--date", type=str, metavar="TARIH",
                      help="Belirli tarihin tum bildirimleri (YYYY-MM-DD)")

    # Arsivleme komutlari
    grp3 = parser.add_argument_group("Arsivleme komutlari")
    grp3.add_argument("--archive", action="store_true", help="Toplu arsivleme")
    grp3.add_argument("--ids", type=str, metavar="ID,ID,...",
                      help="Sadece belirtilen bildirim ID'lerini arsivle (virgul ile ayir)")
    grp3.add_argument("--download", type=str, metavar="OBJID", help="Tek ek dosya indir")
    grp3.add_argument("--dest", type=str, metavar="PATH",
                      help="Hedef klasor (arsivleme varsayilani: companies/{TICKER}/kap_docs)")

    return parser


def main():
    parser = build_parser()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    fmt = "json" if args.json else "text"

    # Client ve fetcher olustur
    client = KAPClient()
    fetcher = KAPFetcher(client)
    archiver = KAPArchiver(fetcher)

    # ── Arama ──
    if args.ticker and args.ticker.lower() == "search":
        keyword = args.keyword or ""
        if not keyword:
            print('Kullanim: bbb kap search "temettu"')
            sys.exit(1)
        results = fetcher.search(keyword)
        print(format_search_results(keyword, results, fmt))
        return

    # ── Bugunun bildirimleri ──
    if args.today:
        disclosures = fetcher.fetch_today(args.category)
        if args.limit and args.limit != 20:  # Kullanici acikca limit verdiyse uygula
            disclosures = disclosures[:args.limit]
        print(format_disclosures(f"BUGUN ({len(disclosures)})", disclosures, fmt))
        return

    # ── Tarihli bildirim sorgu (tum BIST) ──
    if args.date:
        disclosures = fetcher.fetch_by_date(args.date, args.category)
        if args.limit and args.limit != 20:
            disclosures = disclosures[:args.limit]
        print(format_disclosures(f"{args.date} ({len(disclosures)})", disclosures, fmt))
        return

    # Ticker gerektiren komutlar
    if not args.ticker:
        parser.error("Hisse kodu gerekli (ornek: bbb kap EBEBK)")

    ticker = args.ticker.upper()

    # ── Lookup ──
    if args.lookup:
        company = fetcher.lookup_company(ticker)
        if company:
            print(json.dumps(company, ensure_ascii=False, indent=2))
        else:
            print(f"[HATA] {ticker} bulunamadi.", file=sys.stderr)
            sys.exit(1)
        return

    # ── KAP Finansal Ozet ──
    if args.kap_summary:
        summary = fetcher.fetch_kap_summary(ticker)
        if summary:
            if fmt == "json":
                print(json.dumps(summary, ensure_ascii=False, indent=2))
            else:
                print(format_kap_summary(summary))
        else:
            print(f"[HATA] {ticker} KAP ozet verisi bulunamadi.", file=sys.stderr)
            sys.exit(1)
        return

    # ── Bildirim Detay ──
    if args.id:
        detail = fetcher.fetch_detail(args.id)
        if detail:
            print(format_detail(detail, fmt))
        else:
            print(f"\u274c Bildirim #{args.id} bulunamadi.")
        return

    # ── Profil ──
    if args.profile:
        profile = fetcher.fetch_profile(ticker)
        if profile:
            print(format_profile(profile, fmt))
        else:
            print(f"\u274c {ticker} profili bulunamadi.")
        return

    # ── Ozet ──
    if args.summary:
        summary = fetcher.fetch_summary(ticker)
        print(format_summary(summary, fmt))
        return

    # ── Finansal Bildirimler ──
    if args.financials:
        disclosures = fetcher.fetch_financial_disclosures(ticker)
        print(format_disclosures(f"{ticker} (Finansal)", disclosures, fmt))
        return

    # ── Tek Dosya Indirme ──
    if args.download:
        from kap.models import KAPAttachment
        att = KAPAttachment(obj_id=args.download, file_name=f"{args.download}.pdf")
        dest = Path(args.dest) if args.dest else Path(".")
        dest.mkdir(parents=True, exist_ok=True)
        result = archiver.download_attachment(att, dest)
        if result:
            print(f"\u2705 Indirildi: {result}")
        else:
            print(f"\u274c Indirme basarisiz: {args.download}")
            sys.exit(1)
        return

    # ── Toplu Arsivleme ──
    if args.archive:
        if args.dest:
            dest = Path(args.dest)
        else:
            # Varsayilan: workspace-kaya/research/companies/{TICKER}/kap_docs/
            base = Path.home() / ".openclaw" / "workspace-kaya" / "research" / "companies" / ticker / "kap_docs"
            dest = base

        last = args.last or "6m"
        ids = [x.strip() for x in args.ids.split(",")] if args.ids else None
        print(f"\U0001f4e6 {ticker} KAP arsivleme baslatiliyor...")
        print(f"  Hedef: {dest}")
        print(f"  Donem: Son {last}")
        if ids:
            print(f"  Secili bildirimler: {len(ids)} adet")
        print()

        result = archiver.archive(ticker, dest, last=last, ids=ids)
        print(format_archive_result(result))
        return

    # ── Varsayilan: Bildirim Listesi ──
    if args.all:
        disclosures = fetcher.fetch_disclosures(
            ticker, category=args.category, last=args.last,
        )
    else:
        disclosures = fetcher.fetch_disclosures(
            ticker, category=args.category, last=args.last, limit=args.limit,
        )

    print(format_disclosures(ticker, disclosures, fmt))


if __name__ == "__main__":
    main()
