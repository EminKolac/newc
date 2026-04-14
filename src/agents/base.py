"""AgentBase — shared scaffolding for every specialist agent.

Loads versioned prompts, binds tools, calls vLLM (or Anthropic API as fallback),
validates output against the Pydantic schema, records prompt/model versions
into FundState for the audit trail.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Type, TypeVar

from pydantic import BaseModel

PROMPTS_DIR = Path(__file__).parent / "prompts"

T = TypeVar("T", bound=BaseModel)


@dataclass(frozen=True)
class AgentSpec:
    name: str                        # e.g. "research_analyst"
    base_model: str                  # e.g. "Qwen2.5-72B"
    lora_tag: str | None             # e.g. "research_v3"
    temperature: float
    max_tokens: int
    rag_namespaces: tuple[str, ...]
    output_schema: Type[BaseModel]


class AgentBase:
    spec: AgentSpec

    def __init__(self, spec: AgentSpec):
        self.spec = spec
        self._prompt = (PROMPTS_DIR / f"{spec.name}.md").read_text(encoding="utf-8")
        self._prompt_hash = hashlib.sha256(self._prompt.encode()).hexdigest()[:12]

    @property
    def prompt(self) -> str:
        return self._prompt

    @property
    def prompt_hash(self) -> str:
        return self._prompt_hash

    @property
    def model_version(self) -> str:
        if self.spec.lora_tag:
            return f"{self.spec.base_model}+{self.spec.lora_tag}"
        return self.spec.base_model

    def call_llm(self, messages: list[dict]) -> str:
        """Dispatch to vLLM (production) or Anthropic API (dev/failover)."""
        raise NotImplementedError("wire up in src/llm/client.py")

    def parse(self, raw: str, schema: Type[T]) -> T:
        """Strict JSON parse + Pydantic validation; raises on schema violation."""
        import json
        return schema.model_validate(json.loads(raw))
