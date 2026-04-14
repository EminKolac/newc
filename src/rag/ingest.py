"""Corpus ingestion pipelines — runs nightly + on webhook for filings."""
from __future__ import annotations

from pathlib import Path


def ingest_curriculum(source_dir: Path, namespace: str) -> int:
    """Ingest a CFA/CAIA/FRM/CQF curriculum drop. Returns chunk count."""
    raise NotImplementedError


def ingest_kap_filings(since_iso: str) -> int:
    """Pull KAP material disclosures since the given timestamp; chunk + embed + index."""
    raise NotImplementedError


def ingest_sec_filings(since_iso: str) -> int:
    raise NotImplementedError


def ingest_transcripts(since_iso: str) -> int:
    raise NotImplementedError


def integrity_audit(namespace: str, sample_pct: float = 0.01) -> dict:
    """Re-embed a sample and compare to stored embeddings; report drift / corruption."""
    raise NotImplementedError
