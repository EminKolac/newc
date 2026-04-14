"""Domain-aware chunking strategies — one per content type."""
from __future__ import annotations


def chunk_curriculum(text: str, source: str, level: str) -> list[dict]:
    """CFA / CAIA / FRM / CQF readings — semantic chunking on section + subsection."""
    raise NotImplementedError


def chunk_filing(filing_text: str, ticker: str, filing_type: str, period: str) -> list[dict]:
    """SEC / KAP filings — structural chunking on item / section header + XBRL tag."""
    raise NotImplementedError


def chunk_transcript(transcript: str, ticker: str, quarter: str) -> list[dict]:
    """Earnings calls — speaker-aware chunking, role-tagged (CEO/CFO/analyst)."""
    raise NotImplementedError


def chunk_news(article: str, source: str, ts_utc: str) -> list[dict]:
    """News — event-based chunking with NER-extracted entity-event metadata."""
    raise NotImplementedError
