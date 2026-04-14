# `src/` — Argus Capital code skeleton

A scaffolded LangGraph project. Stubs only — every module compiles and exposes its public interface, but business logic is `NotImplementedError` until each phase of the roadmap delivers it.

```
src/
├── orchestrator/
│   ├── graph.py            # the LangGraph state machine
│   └── state.py            # FundState (Pydantic) + sub-models
├── agents/
│   ├── base.py             # AgentBase: prompt loading, tool binding, output validation
│   ├── research_analyst.py
│   ├── quant_strategist.py
│   ├── risk_manager.py
│   ├── macro_analyst.py
│   ├── event_driven.py
│   ├── compliance.py
│   ├── adversarial.py
│   ├── pm.py
│   └── prompts/            # versioned system prompts (one .md file per agent)
├── tools/
│   ├── market_data.py      # MCP wrappers (Fintables, Quartr, TCMB, etc.)
│   ├── analytics.py        # quant primitives (factor scores, Sharpe, etc.)
│   ├── risk.py             # VaR, ES, stress, factor decomp
│   ├── portfolio.py        # optimization (cvxpy, PyPortfolioOpt)
│   ├── compliance.py       # restricted list, position limits, deterministic gates
│   └── execution.py        # OMS / FIX wrappers (IBKR, TR Prime)
├── rag/
│   ├── ingest.py           # corpus ingestion pipelines
│   ├── chunk.py            # domain-aware chunking strategies
│   ├── retrieve.py         # hybrid retrieval + reranking
│   └── lessons.py          # nightly lessons-distillation job
└── config/
    ├── fund.yaml           # capital, sleeve allocations, risk envelope
    ├── agents.yaml         # per-agent model + LoRA + prompt version
    └── mcps.yaml           # MCP endpoints + auth refs
```

**Intentional design properties:**
- Every agent emits a Pydantic model (no free-form prose between agents)
- Every tool result carries `source_id` + `data_as_of_utc`
- The risk envelope and restricted-list checks live in `tools/compliance.py` as deterministic Python — never gated on an LLM call
- `orchestrator/state.py` is the single source of truth for the run state schema
