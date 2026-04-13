"""BBB KAP - Modular KAP.org.tr Entegrasyonu"""

from .models import KAPDisclosure, KAPDetail, KAPAttachment, KAPCompanyProfile, ArchiveResult
from .client import KAPClient
from .fetcher import KAPFetcher
from .parser import (
    parse_rsc_stream, parse_disclosure_list, parse_disclosure_detail,
    parse_attachments, parse_company_profile, parse_kap_financial_page,
    clean_html, fix_turkish_encoding,
)
from .archiver import KAPArchiver
from .formatter import (
    format_disclosures, format_detail, format_profile,
    format_summary, format_search_results, format_archive_result,
    format_kap_summary,
)

__all__ = [
    "KAPDisclosure", "KAPDetail", "KAPAttachment", "KAPCompanyProfile", "ArchiveResult",
    "KAPClient", "KAPFetcher", "KAPArchiver",
    "parse_rsc_stream", "parse_disclosure_list", "parse_disclosure_detail",
    "parse_attachments", "parse_company_profile", "parse_kap_financial_page",
    "clean_html", "fix_turkish_encoding",
    "format_disclosures", "format_detail", "format_profile",
    "format_summary", "format_search_results", "format_archive_result",
    "format_kap_summary",
]
