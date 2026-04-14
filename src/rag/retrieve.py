"""Hybrid retrieval — BM25 + dense (bge-m3 + e5-mistral-7b ensemble) + reranker."""
from __future__ import annotations

from typing import Iterable

from ..orchestrator.state import RetrievedChunk


def retrieve(
    query: str,
    namespaces: Iterable[str],
    top_k: int = 10,
    metadata_filter: dict | None = None,
) -> list[RetrievedChunk]:
    """Hybrid retrieve from Qdrant.

    Pipeline:
      1. Sparse BM25 over the namespaces -> top-50 candidates
      2. Dense ensemble (bge-m3 + e5-mistral-7b, score-averaged) -> top-50
      3. Reciprocal rank fusion -> top-50 unified
      4. Reranker (bge-reranker-v2-m3) -> top_k
      5. Cite-or-die: every chunk carries a stable chunk_id used as source_id
    """
    raise NotImplementedError


def retrieve_lessons(thesis_summary: str, top_k: int = 5) -> list[RetrievedChunk]:
    """Specialized retrieve over the `lessons` namespace, weighted by recency + reinforcement."""
    raise NotImplementedError
