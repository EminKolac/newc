"""MCP wrappers — Fintables (BIST), Quartr (transcripts), TCMB EVDS, Bigdata.com.

Every wrapper returns a `ToolResult` carrying `source_id`, `data_as_of_utc`,
and a provenance chain. Downstream agents are required to cite `source_id`s.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ToolResult(BaseModel):
    payload: Any
    source_id: str
    data_as_of_utc: datetime
    provenance: list[str]


# ----- Fintables (BIST) ----------------------------------------------------

def fintables_query(sql: str) -> ToolResult:
    """Read-only SQL over the Fintables BIST data warehouse.

    Validates SQL is read-only, applies row cap and timeout, caches with TTL
    based on table type (5min for prices, 1d for fundamentals).
    """
    raise NotImplementedError("wire to mcp__fintables__veri_sorgula")


def fintables_search_documents(filter: dict, sort: str, page_size: int) -> ToolResult:
    """Full-text + filter search over KAP filings, broker reports, transcripts."""
    raise NotImplementedError("wire to mcp__fintables__dokumanlarda_ara")


def fintables_load_chunks(chunk_ids: list[str]) -> ToolResult:
    raise NotImplementedError("wire to mcp__fintables__dokuman_chunk_yukle")


# ----- Quartr (earnings transcripts) ---------------------------------------

def quartr_get_transcript(ticker: str, quarter: str) -> ToolResult:
    raise NotImplementedError


# ----- TCMB EVDS (TR macro time series) ------------------------------------

def tcmb_series(series_code: str, start: datetime, end: datetime) -> ToolResult:
    raise NotImplementedError


# ----- Bigdata.com ---------------------------------------------------------

def bigdata_query(query: str, **kwargs) -> ToolResult:
    """Branded reference: 'Bigdata.com' (https://bigdata.com)."""
    raise NotImplementedError
