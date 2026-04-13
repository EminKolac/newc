"""KAP veri ayristirma - RSC stream, HTML, JSON parse."""

import codecs
import html as html_lib
import json
import re
from datetime import datetime
from typing import Dict, List, Optional

from .models import (
    KAP_BASE, KAPAttachment, KAPCompanyProfile, KAPDetail, KAPDisclosure,
)


# ── RSC Stream Parse ──

def parse_rsc_stream(html_text: str) -> List[str]:
    """Next.js RSC stream'den tum chunk'lari cikar."""
    items = re.findall(
        r'self\.__next_f\.push\(\[1,"(.*?)"?\]\)', html_text, re.DOTALL
    )
    return [item.replace('\\"', '"').replace('\\n', '\n') for item in items]


def decode_rsc_chunks(html_text: str) -> str:
    """RSC chunk'larini birlestirir ve unicode unescape yapar."""
    chunks = parse_rsc_stream(html_text)
    if not chunks:
        return ""
    # En buyuk chunk'i bul (genellikle veri iceren)
    combined = ""
    for c in chunks:
        try:
            combined += codecs.decode(c, 'unicode_escape')
        except Exception:
            combined += c
    return combined


# ── Bildirim Listesi Parse (bildirim-sorgu-sonuc) ──

def parse_disclosure_list(html_text: str) -> List[KAPDisclosure]:
    """
    bildirim-sorgu-sonuc sayfasindan yapilandirilmis bildirim JSON'u cikar.
    Bu endpoint disclosureBasic JSON nesneleri dondurur.
    """
    decoded = decode_rsc_chunks(html_text)
    if not decoded:
        return []

    # disclosureBasic JSON bloklarini cikar
    pattern = r'\{"disclosureBasic":\{[^}]+\}\}'
    matches = re.findall(pattern, decoded)

    disclosures = []
    for m in matches:
        try:
            obj = json.loads(m)
            db = obj["disclosureBasic"]

            # Tarih parse
            date_str = db.get("publishDate", "")
            try:
                date = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
            except ValueError:
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    date = datetime.now()

            disc = KAPDisclosure(
                id=str(db.get("disclosureIndex", "")),
                title=fix_turkish_encoding(db.get("title", "")),
                company=fix_turkish_encoding(db.get("companyTitle", "")),
                ticker=db.get("stockCode", ""),
                date=date,
                category=db.get("disclosureClass", "DG"),
                summary=fix_turkish_encoding(db.get("summary", "") or ""),
                attachment_count=db.get("attachmentCount", 0) or 0,
                is_late=db.get("isLate", False) or False,
                has_multilang=(db.get("hasMultiLanguageSupport", "") == "Y"),
                url=f"{KAP_BASE}/tr/Bildirim/{db.get('disclosureIndex', '')}",
            )
            disclosures.append(disc)
        except (json.JSONDecodeError, KeyError):
            continue

    return disclosures


# ── Bildirim Detay Parse ──

def _is_rsc_junk(text: str) -> bool:
    """Metnin RSC/React bileşen ağacı artığı olup olmadığını kontrol et."""
    markers = ['parallelRouterKey', '__PAGE__', 'segmentPath', 'templateStyles',
               'notFoundStyles', 'errorScripts', 'HL["/_next/static']
    hits = sum(1 for m in markers if m in text)
    return hits >= 2


def _extract_rsc_children_text(decoded: str) -> str:
    """RSC tree'deki children alanlarindan okunabilir metin cikar."""
    # RSC'de metin iceren children: "children":"metin" veya children\\":\\"metin\\"
    texts = []
    for m in re.finditer(r'children[\\]*":[\\]*"([^"\\]{10,})', decoded):
        val = m.group(1).strip()
        # RSC kontrol metinlerini ve Next.js sablonlarini atla
        if any(skip in val for skip in ['/_next/', '__PAGE__', 'segmentPath',
                                         'parallelRouter', 'undefined',
                                         'could not be found',
                                         'system-ui', 'Segoe UI',
                                         'prefers-color-scheme']):
            continue
        texts.append(val)
    return ' '.join(texts) if texts else ""


def parse_disclosure_detail(html_text: str) -> Optional[KAPDetail]:
    """Bildirim detay sayfasindan icerik + attachment JSON cikar."""
    decoded = decode_rsc_chunks(html_text)
    if not decoded:
        return None

    # Attachments
    attachments = parse_attachments(decoded)

    # Icerik
    clean_text = clean_html(decoded)

    # ODA alanlari
    fields = {}
    oda_fields = re.findall(r'oda_(\w+)\|\s*(.*?)(?=oda_|\Z)', clean_text)
    for key, val in oda_fields:
        fields[key] = fix_turkish_encoding(val.strip()[:500])

    # Aciklama metni
    explanation = ""
    if "ExplanationTextBlock" in fields:
        explanation = fields["ExplanationTextBlock"]
    else:
        for marker in ["Aciklamalar", "Explanations", "Bildirim Icerigi"]:
            idx = clean_text.find(marker)
            if idx > 0:
                explanation = clean_text[idx:idx + 3000].strip()
                break

    if not explanation:
        # RSC artigi kontrolu: clean_text sadece React bileşen verisi mi?
        candidate = clean_text[:3000]
        if _is_rsc_junk(candidate):
            # RSC tree'den metin cikarmayi dene
            rsc_text = _extract_rsc_children_text(decoded)
            if rsc_text:
                explanation = rsc_text[:3000]
            else:
                explanation = "(Bu bildirim yapilandirilmis form verisi icerir. Metin icerigi cikarilamadi. Ek dosyalara veya KAP sayfasina bakiniz.)"
        else:
            explanation = candidate

    # Baslik
    title = fields.get("MaterialEventDisclosureGeneralAbstract", "")
    if not title:
        for key in fields:
            if "Abstract" in key:
                title = fields[key][:100]
                break

    # Sirket
    company = ""
    comp_match = re.search(r'Ilgili Sirketler.*?\]\s*(.*?)(?:Ilgili Fonlar|Turkce)', clean_text)
    if comp_match:
        company = comp_match.group(1).strip()

    # Tarih
    date_match = re.search(r'(\d{2}[./]\d{2}[./]\d{4}\s+\d{2}:\d{2}:\d{2})', clean_text)
    if date_match:
        ds = date_match.group(1).replace('/', '.')
        try:
            date = datetime.strptime(ds, "%d.%m.%Y %H:%M:%S")
        except ValueError:
            date = datetime.now()
    else:
        date = datetime.now()

    return KAPDetail(
        id="",  # Caller set eder
        title=fix_turkish_encoding(title or "Bildirim"),
        company=fix_turkish_encoding(company),
        date=date,
        content=fix_turkish_encoding(explanation),
        attachments=attachments,
        raw_fields=fields,
    )


# ── Attachment Parse ──

def parse_attachments(decoded_text: str) -> List[KAPAttachment]:
    """RSC decoded text'ten attachments JSON array'ini cikar."""
    att_match = re.search(r'"attachments":\[(.*?)\]', decoded_text)
    if not att_match:
        return []

    att_raw = att_match.group(1).strip()
    if not att_raw:
        return []

    try:
        items = json.loads('[' + att_raw + ']')
    except json.JSONDecodeError:
        return []

    attachments = []
    for item in items:
        if isinstance(item, dict) and "objId" in item:
            attachments.append(KAPAttachment(
                obj_id=item["objId"],
                file_name=fix_turkish_encoding(item.get("fileName", "")),
                file_extension=item.get("fileExtension", ""),
            ))
    return attachments


# ── KAP Finansal Sayfa Parse ──

def parse_kap_financial_page(html_text: str, ticker: str) -> Optional[dict]:
    """KAP SSR payload'dan finansal veri parse et."""
    result = {
        "ticker": ticker.upper(),
        "company": "",
        "periods": [],
        "balance_sheet": {},
        "income_statement": {},
    }

    # Sirket adi
    name_match = re.search(r'"companyName":"([^"]+)"', html_text)
    if name_match:
        result["company"] = name_match.group(1)
    else:
        name_match = re.search(r'companyname="([^"]+)"', html_text, re.IGNORECASE)
        if name_match:
            result["company"] = name_match.group(1)

    # Donemler
    periods = re.findall(r'children\\":\\"(\d{4}/\d{1,2})\\"', html_text)
    if not periods:
        periods = re.findall(r'children":"(\d{4}/\d{1,2})"', html_text)
    seen = set()
    for p in periods:
        if p not in seen:
            result["periods"].append(p)
            seen.add(p)

    # Finansal kalemler
    item_starts = list(re.finditer(
        r'((?:ifrs-full|kap-fr)_[A-Za-z]+)\\{0,2}",\{', html_text
    ))

    for i, match in enumerate(item_starts):
        item_id = match.group(1)
        start = match.start()
        end = item_starts[i + 1].start() if i + 1 < len(item_starts) else min(start + 1500, len(html_text))
        row = html_text[start:end]

        section = "income_statement" if "gelir_" in row else "balance_sheet"

        label_match = re.search(r'children\\":\\"([^\\"]+)\\"', row)
        if not label_match:
            label_match = re.search(r'children":"([^"]+)"', row)
        label = label_match.group(1) if label_match else item_id

        values = {}
        val_pattern = r'(?:bilanco|gelir)_(\d{4}/\d{1,2})_\d+\\"[^}]*?children\\":\\"([^\\"]+)\\"'
        for vm in re.finditer(val_pattern, row):
            period, value = vm.group(1), vm.group(2)
            if value and not value.startswith("$") and value != "undefined":
                values[period] = value
        if not values:
            val_pattern2 = r'(?:bilanco|gelir)_(\d{4}/\d{1,2})_\d+"[^}]*?children":"([^"]+)"'
            for vm in re.finditer(val_pattern2, row):
                period, value = vm.group(1), vm.group(2)
                if value and not value.startswith("$") and value != "undefined":
                    values[period] = value

        if label and values:
            result[section][item_id] = {"label": label, "values": values}

    return result if (result["balance_sheet"] or result["income_statement"]) else None


# ── Sirket Profili Parse ──

def parse_company_profile(html_text: str, ticker: str, oid: str = "") -> KAPCompanyProfile:
    """SSR sayfasindan sirket profili cikar. Simdilik temel bilgileri dondurur."""
    return KAPCompanyProfile(
        ticker=ticker.upper(),
        name="",
        member_oid=oid,
    )


# ── Yardimci Fonksiyonlar ──

def clean_html(text: str) -> str:
    """HTML tag'lerini temizle, metin cikar."""
    text = text.replace('\\u003c', '<').replace('\\u003e', '>')
    text = text.replace('\\u0026', '&').replace('\\u0027', "'")
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'\s+', ' ', clean)
    return html_lib.unescape(clean).strip()


def fix_turkish_encoding(text: str) -> str:
    """
    RSC'deki bozuk Turkce karakterleri duzelt.
    UTF-8 double encoding: bytes latin-1 olarak okunmus, tekrar UTF-8 decode gerekir.
    Ornek: 'Ã–zel Durum AÃ§Ä±klamasÄ±' -> 'Özel Durum Açıklaması'

    Kok neden: codecs.decode('unicode_escape') bazi Turkce karakterleri dogru cikarirken
    (\\u0131 -> ı), bazi raw UTF-8 byte'larini Latin-1 olarak yorumlar (\\u00c3\\u00bc -> Ã¼).
    Sonuc: ayni metinde hem dogru ı (U+0131) hem bozuk Ã¼ bulunur.
    text.encode('latin-1') yaklasimi basarisiz olur cunku ı Latin-1 araliginda degil (>U+00FF).
    Cozum: her double-encoded 2-byte UTF-8 dizisini tek tek regex ile duzelt.
    """
    if not text:
        return ""

    # Double-encoded UTF-8 gostergesi kontrolu (hiz icin)
    if '\u00c3' not in text and '\u00c4' not in text and '\u00c5' not in text:
        return text

    # Oncelikle tam metin donusumu dene (tum karakterler Latin-1 ise)
    try:
        return text.encode('latin-1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass

    # Karisik encoding: tek tek 2-byte UTF-8 dizilerini duzelt
    # Pattern: UTF-8 lead byte (C0-DF) + continuation byte (80-BF) — Latin-1 karsiliklari
    def _fix_pair(m):
        try:
            return m.group(0).encode('latin-1').decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            return m.group(0)

    return re.sub(r'[\u00c0-\u00df][\u0080-\u00bf]', _fix_pair, text)
