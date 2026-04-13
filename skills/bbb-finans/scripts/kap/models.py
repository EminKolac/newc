"""KAP veri modelleri."""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


KAP_BASE = "https://www.kap.org.tr"

CATEGORIES = {
    "ODA": "Ozel Durum Aciklamasi",
    "FR":  "Finansal Rapor",
    "GK":  "Genel Kurul",
    "TEM": "Temettu",
    "SA":  "Sermaye Artirimi",
    "YON": "Yonetim",
    "ORT": "Ortaklik",
    "DG":  "Diger",
    "DKB": "Devre Kesici Bildirimi",
}

IMPORTANCE_CRITICAL = [
    "temettu", "kar payi", "kar dagitim", "sermaye artirimi",
    "bedelli", "bedelsiz", "birlesme", "bolunme", "devir",
    "iflas", "konkordato", "sorusturma", "finansal rapor",
    "zarar", "gelir tablosu", "bilanco",
]

IMPORTANCE_MEDIUM = [
    "yonetim kurulu", "genel kurul", "atama", "istifa",
    "pay alim", "pay satim", "ortaklik", "geri alim",
    "derecelendirme", "kredi notu",
]


@dataclass
class KAPDisclosure:
    """KAP bildirim verisi."""
    id: str
    title: str
    company: str
    ticker: str
    date: datetime
    category: str = "DG"
    summary: str = ""
    attachment_count: int = 0
    is_late: bool = False
    has_multilang: bool = False
    url: str = ""

    # Geriye uyumluluk: eski kodun kullandigi alanlar
    @property
    def subject(self) -> str:
        return self.title

    @property
    def importance(self) -> str:
        text = (self.title + " " + self.summary).lower()
        if any(k in text for k in IMPORTANCE_CRITICAL):
            return "high"
        elif any(k in text for k in IMPORTANCE_MEDIUM):
            return "medium"
        return "low"


@dataclass
class KAPAttachment:
    """Bildirim ek dosyasi."""
    obj_id: str
    file_name: str
    file_extension: str = ""

    @property
    def download_url(self) -> str:
        return f"{KAP_BASE}/tr/api/file/download/{self.obj_id}"

    @property
    def safe_file_name(self) -> str:
        """Dosya sistemi icin guvenli dosya adi."""
        import re
        name = self.file_name
        # Turkce karakterleri koru, ozel karakterleri kaldir
        name = re.sub(r'[<>:"/\\|?*]', '_', name)
        return name.strip()


@dataclass
class KAPDetail:
    """Bildirim detayi."""
    id: str
    title: str
    company: str
    date: datetime
    content: str
    attachments: List[KAPAttachment] = field(default_factory=list)
    raw_fields: Dict[str, str] = field(default_factory=dict)


@dataclass
class KAPCompanyProfile:
    """Sirket profil verisi."""
    ticker: str
    name: str
    member_oid: str = ""
    sector: str = ""
    market: str = ""
    indices: str = ""
    address: str = ""
    website: str = ""
    email: str = ""
    auditor: str = ""
    board_members: List[str] = field(default_factory=list)
    ownership: Dict[str, str] = field(default_factory=dict)
    recent_disclosures: List["KAPDisclosure"] = field(default_factory=list)


@dataclass
class ArchiveResult:
    """Arsivleme islem sonucu."""
    total_disclosures: int = 0
    filtered_disclosures: int = 0
    downloaded_files: int = 0
    saved_texts: int = 0
    skipped: int = 0
    errors: List[str] = field(default_factory=list)
    index_path: Optional[Path] = None
