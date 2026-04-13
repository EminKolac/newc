"""KAP arsivleme - bildirim indirme, kaydetme, index olusturma."""

import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .client import KAPClient
from .fetcher import KAPFetcher
from .models import (
    KAP_BASE, ArchiveResult, KAPAttachment, KAPDetail, KAPDisclosure,
)


# Arsivleme icin ilgili bildirim kategorileri
# Fon portfoy raporlari gibi ilgisiz bildirimleri atla
RELEVANT_CATEGORIES = {"ODA", "FR", "GK", "TEM", "SA", "YON", "DG"}

# Arsivlemede oncelikli kategoriler (metin olarak da kaydedilir)
TEXT_SAVE_CATEGORIES = {"ODA", "YON", "GK", "TEM", "SA", "DG"}


class KAPArchiver:
    """KAP bildirimleri arsivleme: PDF indirme, metin kaydetme, index olusturma."""

    def __init__(self, fetcher: KAPFetcher):
        self.fetcher = fetcher

    def archive(self, ticker: str, dest_dir: Path,
                last: str = "6m", categories: List[str] = None,
                ids: List[str] = None,
                force: bool = False) -> ArchiveResult:
        """
        Toplu arsivleme:
        1. Tum bildirimleri cek ve filtrele
        2. Her bildirim icin: ek dosyalari indir + metin kaydet
        3. index.md olustur

        ids: Belirtilirse sadece bu ID'ler arsivlenir (kategori filtresi atlanir).
             AI'nin secici arsivleme icin kullandigi mod.
        """
        result = ArchiveResult()
        self.fetcher.client.set_archive_mode(True)

        try:
            # 1. Bildirimleri cek (cache bypass)
            all_disc = self.fetcher.fetch_all_disclosures(ticker)
            result.total_disclosures = len(all_disc)

            # 2. Filtrele
            filtered = self.fetcher.fetch_disclosures(
                ticker, category=None, last=last,
            )

            if ids:
                # Secici mod: sadece belirtilen ID'leri al (kategori filtresi yok)
                id_set = set(ids)
                filtered = [d for d in filtered if d.id in id_set]
            else:
                # Toplu mod: kategori filtresi uygula
                valid_cats = set(categories) if categories else RELEVANT_CATEGORIES
                filtered = [d for d in filtered if d.category in valid_cats]

            # Ayni ticker'a ait olanlari filtrele (fon raporlarini atla)
            # ids modunda ticker filtresi ATLANIR — AI cross-company secim yapmis olabilir
            # Coklu ticker destegi: KAP "ALBRK, ALK" gibi virgullu dondurebilir
            if not ids:
                ticker_upper = ticker.upper()
                filtered = [d for d in filtered if
                            not d.ticker or
                            ticker_upper in [t.strip() for t in (d.ticker or "").split(",")]]

            result.filtered_disclosures = len(filtered)

            # 3. Her bildirim icin islem yap
            dest_dir.mkdir(parents=True, exist_ok=True)

            for disc in filtered:
                try:
                    self._process_disclosure(disc, dest_dir, force, result)
                except Exception as e:
                    result.errors.append(f"[{disc.id}] {disc.title}: {e}")

            # 4. Index olustur
            result.index_path = self._generate_index(ticker, dest_dir, filtered)

        finally:
            self.fetcher.client.set_archive_mode(False)

        return result

    def _process_disclosure(self, disc: KAPDisclosure, dest_dir: Path,
                            force: bool, result: ArchiveResult):
        """Tek bir bildirimi isle: detay cek, dosyalari indir/kaydet."""
        date_str = disc.date.strftime("%Y-%m-%d")
        title_slug = _slugify(disc.title)[:50]
        base_name = f"{date_str}_{disc.category.lower()}_{title_slug}_{disc.id}"

        # Detay cek (ek dosya bilgisi icin)
        detail = self.fetcher.fetch_detail(disc.id)

        if detail and detail.attachments:
            # Ek dosyali bildirim -> alt klasor
            disc_dir = dest_dir / base_name
            disc_dir.mkdir(parents=True, exist_ok=True)

            # Bildirim metnini kaydet
            txt_path = disc_dir / "bildirim.txt"
            if force or not txt_path.exists():
                self._save_text(detail, txt_path)
                result.saved_texts += 1
            else:
                result.skipped += 1

            # Ek dosyalari indir
            for att in detail.attachments:
                self.download_attachment(att, disc_dir, force, result)

        elif disc.category in TEXT_SAVE_CATEGORIES:
            # Metin bildirimi -> tek dosya
            txt_path = dest_dir / f"{base_name}.txt"
            if force or not txt_path.exists():
                if detail:
                    self._save_text(detail, txt_path)
                    result.saved_texts += 1
                else:
                    result.skipped += 1
            else:
                result.skipped += 1

    def download_attachment(self, attachment: KAPAttachment, dest_dir: Path,
                            force: bool = False, result: ArchiveResult = None):
        """Tek ek dosya indir."""
        dest_path = dest_dir / attachment.safe_file_name
        if not force and dest_path.exists():
            if result:
                result.skipped += 1
            return dest_path

        print(f"  ⬇ {attachment.file_name}...", end=" ", flush=True)
        success = self.fetcher.client.download_file(
            attachment.download_url, dest_path
        )

        if success:
            print(f"✅ ({dest_path.stat().st_size // 1024} KB)")
            if result:
                result.downloaded_files += 1
        else:
            print("❌")
            if result:
                result.errors.append(f"Indirilemedi: {attachment.file_name}")

        return dest_path if success else None

    def download_disclosure_pdf(self, disc_id: str, dest_dir: Path) -> Optional[Path]:
        """Bildirim metnini PDF olarak indir."""
        dest_path = dest_dir / f"bildirim_{disc_id}.pdf"
        url = f"{KAP_BASE}/tr/api/BildirimPdf/{disc_id}"
        success = self.fetcher.client.download_file(url, dest_path)
        return dest_path if success else None

    def _save_text(self, detail: KAPDetail, path: Path):
        """Bildirim metnini .txt olarak kaydet."""
        lines = [
            f"KAP Bildirimi #{detail.id}",
            f"Tarih: {detail.date.strftime('%d.%m.%Y %H:%M')}",
            f"Sirket: {detail.company}",
            f"Konu: {detail.title}",
            f"",
            "-" * 60,
            f"",
            detail.content or "(Icerik yok)",
        ]
        path.write_text("\n".join(lines), encoding="utf-8")

    def _generate_index(self, ticker: str, dest_dir: Path,
                        disclosures: List[KAPDisclosure]) -> Path:
        """index.md olustur."""
        index_path = dest_dir / "index.md"
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        lines = [
            f"# {ticker} - KAP Bildirim Arsivi",
            f"",
            f"Son guncelleme: {now}",
            f"Toplam bildirim: {len(disclosures)}",
            f"",
            f"| Tarih | Kategori | Baslik | Dosyalar |",
            f"|-------|----------|--------|----------|",
        ]

        for d in disclosures:
            date_str = d.date.strftime("%Y-%m-%d")
            att = f"{d.attachment_count} PDF" if d.attachment_count > 0 else "metin"
            title = d.title[:50]
            lines.append(f"| {date_str} | {d.category} | {title} | {att} |")

        index_path.write_text("\n".join(lines), encoding="utf-8")
        return index_path


def _slugify(text: str) -> str:
    """Baslik metninden dosya sistemi icin guvenli slug olustur."""
    text = text.lower().strip()
    # Turkce karakterleri donustur
    tr_map = str.maketrans("çğöşüıÇĞÖŞÜİ", "cgosui" + "CGOSUI")
    text = text.translate(tr_map)
    # Sadece alfanumerik ve tire
    text = re.sub(r'[^a-z0-9\-]', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')
