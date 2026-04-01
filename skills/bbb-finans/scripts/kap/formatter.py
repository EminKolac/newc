"""KAP terminal goruntuleme - bildirim, detay, profil formatlama."""

import json
from typing import Dict, List

from .models import (
    CATEGORIES, ArchiveResult, KAPCompanyProfile, KAPDetail, KAPDisclosure,
)

# Emoji esleme
_IMP_EMOJI = {"high": "\U0001f534", "medium": "\U0001f7e1", "low": "\U0001f7e2"}
_CAT_EMOJI = {
    "ODA": "\u26a0\ufe0f", "FR": "\U0001f4ca", "GK": "\U0001f3db\ufe0f",
    "TEM": "\U0001f4b0", "SA": "\U0001f4c8", "YON": "\U0001f464",
    "ORT": "\U0001f465", "DG": "\U0001f4c4", "DKB": "\U0001f6a8",
}


def format_disclosures(header: str, disclosures: List[KAPDisclosure], fmt: str = "text") -> str:
    """Bildirim listesini formatla."""
    if fmt == "json":
        return json.dumps([_disc_dict(d) for d in disclosures], indent=2, ensure_ascii=False)

    if not disclosures:
        return f"\U0001f4cb {header}: KAP bildirimi bulunamadi."

    lines = [
        f"\n{'='*70}",
        f"\U0001f4cb KAP BILDIRIMLERI: {header} ({len(disclosures)} bildirim)",
        f"{'='*70}",
    ]

    for i, d in enumerate(disclosures, 1):
        imp = _IMP_EMOJI.get(d.importance, "\u26aa")
        cat = _CAT_EMOJI.get(d.category, "\U0001f4c4")
        cat_name = CATEGORIES.get(d.category, d.category)
        att_info = f" \U0001f4ce{d.attachment_count}" if d.attachment_count > 0 else ""

        lines.extend([
            f"",
            f"  {i}. {imp}{cat} {d.title}{att_info}",
            f"     \U0001f3e2 {d.company}",
        ])
        if d.summary:
            lines.append(f"     \U0001f4dd {d.summary[:80]}")
        lines.extend([
            f"     \U0001f4c5 {d.date.strftime('%d/%m/%Y %H:%M')}  |  \U0001f3f7\ufe0f {cat_name}",
            f"     \U0001f517 {d.url}",
        ])

    lines.extend([
        f"",
        f"  \U0001f534 Kritik  \U0001f7e1 Orta  \U0001f7e2 Dusuk",
        f"  \U0001f4a1 Detay: bbb kap {header.split()[0]} --id <ID>",
        f"{'='*70}",
    ])
    return "\n".join(lines)


def format_detail(detail: KAPDetail, fmt: str = "text") -> str:
    """Bildirim detayini formatla."""
    if fmt == "json":
        d = {
            "id": detail.id, "title": detail.title, "company": detail.company,
            "date": detail.date.isoformat(), "content": detail.content,
            "attachments": [{"obj_id": a.obj_id, "file_name": a.file_name,
                            "file_extension": a.file_extension} for a in detail.attachments],
            "raw_fields": detail.raw_fields,
        }
        return json.dumps(d, indent=2, ensure_ascii=False)

    if not detail:
        return "\u274c Bildirim detayi bulunamadi."

    lines = [
        f"\n{'='*70}",
        f"\U0001f4cb BILDIRIM DETAYI: #{detail.id}",
        f"{'='*70}",
    ]

    if detail.company:
        lines.append(f"  \U0001f3e2 Sirket: {detail.company}")
    if detail.title:
        lines.append(f"  \U0001f4d1 Konu:   {detail.title}")

    lines.extend([f"", f"{'_'*70}", f"  \U0001f4dd ICERIK", f"{'_'*70}"])

    content = detail.content
    if content:
        words = content.split()
        current = "  "
        for word in words:
            if len(current) + len(word) > 75:
                lines.append(current)
                current = "  " + word
            else:
                current += " " + word if current.strip() else "  " + word
        if current.strip():
            lines.append(current)
    else:
        lines.append("  (Icerik cikarilamadi)")

    # Ek dosyalar
    if detail.attachments:
        lines.extend([f"", f"{'_'*70}", f"  \U0001f4ce EK DOSYALAR ({len(detail.attachments)})"])
        for a in detail.attachments:
            lines.append(f"  \u2022 {a.file_name}  [{a.file_extension}]")
            lines.append(f"    ID: {a.obj_id}")
            lines.append(f"    Indir: bbb kap --download {a.obj_id}")

    # Onemli ek alanlar
    important_keys = {
        "UpdateAnnouncementFlag": "Guncelleme mi?",
        "CorrectionAnnouncementFlag": "Duzeltme mi?",
        "DelayedAnnouncementFlag": "Ertelenmis mi?",
    }
    shown = []
    for key, label in important_keys.items():
        if key in detail.raw_fields:
            val = detail.raw_fields[key][:100]
            if "Evet" in val or "Yes" in val:
                shown.append(f"  \u26a0\ufe0f {label}: {val}")
    if shown:
        lines.extend([f"", f"{'_'*70}"] + shown)

    lines.extend([f"", f"{'='*70}"])
    return "\n".join(lines)


def format_profile(profile: KAPCompanyProfile, fmt: str = "text") -> str:
    """Sirket profilini formatla."""
    if fmt == "json":
        d = profile.__dict__.copy()
        d["recent_disclosures"] = [_disc_dict(dd) for dd in d.get("recent_disclosures", [])]
        return json.dumps(d, indent=2, ensure_ascii=False)

    if not profile:
        return "\u274c Sirket profili bulunamadi."

    lines = [
        f"\n{'='*70}",
        f"\U0001f3e2 SIRKET PROFILI: {profile.ticker} - {profile.name}",
        f"{'='*70}",
    ]

    for label, val in [
        ("Sektor", profile.sector), ("Pazar", profile.market),
        ("Endeksler", profile.indices), ("Website", profile.website),
        ("E-posta", profile.email), ("Bagimsiz Denetci", profile.auditor),
        ("Adres", profile.address),
    ]:
        if val:
            lines.append(f"  {label:20s}: {val}")

    if profile.recent_disclosures:
        lines.extend([f"", f"{'_'*70}", f"  \U0001f4cb SON BILDIRIMLER"])
        for d in profile.recent_disclosures[:5]:
            imp = _IMP_EMOJI.get(d.importance, "\u26aa")
            lines.append(f"  {imp} [{d.id}] {d.title[:50]}  ({d.date.strftime('%d/%m/%Y')})")

    lines.extend([f"", f"{'='*70}"])
    return "\n".join(lines)


def format_summary(summary: Dict, fmt: str = "text") -> str:
    """Ozet gorunumu formatla."""
    if fmt == "json":
        return json.dumps(summary, indent=2, ensure_ascii=False, default=str)

    profile = summary.get("profile")
    important = summary.get("important_disclosures", [])
    all_disc = summary.get("all_disclosures", [])

    lines = []
    if profile:
        lines.extend([
            f"\n{'='*70}",
            f"\U0001f4ca OZET: {profile.ticker} - {profile.name}",
            f"{'='*70}",
        ])
        if profile.sector:
            lines.append(f"  \U0001f4c2 Sektor: {profile.sector}")

    if important:
        lines.extend([f"", f"{'_'*70}", f"  \U0001f534 ONEMLI BILDIRIMLER", f"{'_'*70}"])
        for d in important:
            imp = _IMP_EMOJI.get(d.importance, "\u26aa")
            lines.append(f"  {imp} {d.title[:55]:55s} | {d.date.strftime('%d/%m/%Y')}")
            if d.summary:
                lines.append(f"     \U0001f4dd {d.summary[:70]}")

    if all_disc:
        lines.extend([f"", f"{'_'*70}", f"  \U0001f4cb SON BILDIRIMLER ({len(all_disc)})", f"{'_'*70}"])
        for d in all_disc:
            cat = _CAT_EMOJI.get(d.category, "\U0001f4c4")
            lines.append(f"  {cat} [{d.id}] {d.title[:45]:45s} | {d.date.strftime('%d/%m/%Y')}")

    lines.extend([f"", f"{'='*70}"])
    return "\n".join(lines)


def format_search_results(keyword: str, disclosures: List[KAPDisclosure], fmt: str = "text") -> str:
    """Arama sonuclarini formatla."""
    if fmt == "json":
        return json.dumps([_disc_dict(d) for d in disclosures], indent=2, ensure_ascii=False)

    if not disclosures:
        return f"\U0001f50d '{keyword}' icin KAP bildirimi bulunamadi."

    lines = [
        f"\n{'='*70}",
        f"\U0001f50d KAP ARAMA: '{keyword}' ({len(disclosures)} sonuc)",
        f"{'='*70}",
    ]

    for i, d in enumerate(disclosures, 1):
        imp = _IMP_EMOJI.get(d.importance, "\u26aa")
        lines.extend([
            f"",
            f"  {i}. {imp} {d.title}",
            f"     \U0001f3e2 {d.company}  |  \U0001f4c5 {d.date.strftime('%d/%m/%Y %H:%M')}",
        ])
        if d.summary:
            lines.append(f"     \U0001f4dd {d.summary[:80]}")
        if d.url:
            lines.append(f"     \U0001f517 {d.url}")

    lines.extend([f"", f"{'='*70}"])
    return "\n".join(lines)


def format_archive_result(result: ArchiveResult) -> str:
    """Arsivleme sonucu ozeti."""
    lines = [
        f"\n{'='*70}",
        f"\U0001f4e6 KAP ARSIVLEME SONUCU",
        f"{'='*70}",
        f"  Taranan bildirim:    {result.total_disclosures}",
        f"  Filtrelenen:         {result.filtered_disclosures}",
        f"  Indirilen dosya:     {result.downloaded_files}",
        f"  Kaydedilen metin:    {result.saved_texts}",
        f"  Atlanan (mevcut):    {result.skipped}",
    ]
    if result.errors:
        lines.append(f"  Hata:                {len(result.errors)}")
        for e in result.errors[:5]:
            lines.append(f"    \u26a0\ufe0f {e}")
    if result.index_path:
        lines.append(f"  Index:               {result.index_path}")
    lines.extend([f"", f"{'='*70}"])
    return "\n".join(lines)


def format_kap_summary(summary: dict) -> str:
    """KAP finansal ozet tablosu."""
    if not summary:
        return "\u274c KAP finansal ozet bulunamadi."

    lines = [
        f"\n{'='*70}",
        f"\U0001f4ca KAP FINANSAL OZET: {summary.get('ticker', '')} - {summary.get('company', '')}",
        f"{'='*70}",
    ]

    periods = summary.get("periods", [])
    if periods:
        lines.append(f"  Donemler: {', '.join(periods[:6])}")

    for section, label in [("balance_sheet", "BILANCO"), ("income_statement", "GELIR TABLOSU")]:
        items = summary.get(section, {})
        if items:
            lines.extend([f"", f"{'_'*70}", f"  {label}"])
            for item_id, item_data in items.items():
                lbl = item_data.get("label", item_id)[:35]
                vals = item_data.get("values", {})
                val_str = " | ".join(f"{p}: {v}" for p, v in list(vals.items())[:4])
                lines.append(f"  {lbl:35s} {val_str}")

    lines.extend([f"", f"{'='*70}"])
    return "\n".join(lines)


# ── Yardimci ──

def _disc_dict(d: KAPDisclosure) -> dict:
    return {
        "id": d.id, "title": d.title, "company": d.company,
        "ticker": d.ticker, "date": d.date.isoformat(),
        "category": d.category, "summary": d.summary,
        "attachment_count": d.attachment_count, "url": d.url,
    }
