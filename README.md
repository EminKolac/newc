# Argus Capital

> **AI-native hedge fund — design and reference scaffold.**
> Multi-agent LangGraph orchestrator over a curriculum-grounded RAG corpus, BIST-anchored with a TR macro and event-driven sleeve, scaling to global EM. Open-weight LLMs (Qwen2.5/Qwen3) on H200 GPUs, MCP-integrated data layer (Fintables, Quartr, TCMB EVDS, Bigdata.com).

This repository contains:

1. **The plan** — [`PLAN.md`](PLAN.md) is the master document: thesis, structure, stack, KPIs, costs.
2. **Detailed design** — `docs/` — architecture, agents, strategies, data, risk, infrastructure, roadmap.
3. **Code scaffold** — `src/` — runnable LangGraph skeleton with state schema, agent stubs, tool wrappers, configs.
4. **Daily ops prototype** — [`check_analyst_reports.sh`](check_analyst_reports.sh) — the existing BIST analyst-report digest job that becomes the model for Argus's daily-artifact pipeline.

## Read this first

| Document | What it covers |
|---|---|
| [`PLAN.md`](PLAN.md) | Executive plan, fund structure, capital, fees, KPIs |
| [`docs/architecture.md`](docs/architecture.md) | LangGraph state machine, node graph, contracts |
| [`docs/agents.md`](docs/agents.md) | Per-agent specs (prompts, tools, RAG namespaces, escalation) |
| [`docs/strategies.md`](docs/strategies.md) | The actual investment sleeves and signals |
| [`docs/data-and-mcps.md`](docs/data-and-mcps.md) | MCPs, RAG corpus, episodic-memory loop |
| [`docs/risk-compliance.md`](docs/risk-compliance.md) | Risk envelope, kill switch, regulatory mapping |
| [`docs/infrastructure.md`](docs/infrastructure.md) | vLLM, Qdrant, Postgres, observability |
| [`docs/roadmap.md`](docs/roadmap.md) | 24-month phased plan with explicit gates |

## Code layout

```
src/
├── orchestrator/       LangGraph state machine + FundState schema
├── agents/             7 specialist agents (research, quant, risk, macro, event, compliance, adversarial) + PM
│   └── prompts/        versioned system prompts (one .md per agent)
├── tools/              MCP wrappers + deterministic analytics (VaR, factor scores, optimizer, OMS)
├── rag/                ingest, chunking, hybrid retrieve, lessons distillation
└── config/             fund.yaml, agents.yaml, mcps.yaml
```

Every public function compiles; business logic is `NotImplementedError` until each phase of the roadmap delivers it. The Pydantic schemas, the graph topology, the prompt files, and the configs are the actual deliverable of this design pass.

## Status

**Phase 0 — Foundation** (per [`docs/roadmap.md`](docs/roadmap.md)).
Design complete. Implementation begins on the seven agents, RAG ingest, and the deterministic gates.
