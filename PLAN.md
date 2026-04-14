# Argus Capital — AI-Native Hedge Fund

> **Project codename:** Argus (the all-seeing of Greek myth — a hundred eyes, never all asleep at once).
> **One-line pitch:** A multi-agent, AI-native long/short equity + global-macro hedge fund, anchored in BIST and selected EM/DM equities, run on a LangGraph orchestrator, vLLM-served open-weight LLMs, and a domain-specific RAG corpus distilled from CFA / CAIA / FRM / CQF curricula and primary-source filings.

---

## 1. Executive Summary

Argus Capital is designed as a **systematic-discretionary hybrid** hedge fund where every investment decision is generated, stress-tested, and documented by a coordinated set of specialist AI agents, then ratified by a small human investment committee. The fund's edge is not a single secret model — it is the **integration**: domain-grounded LLM agents, a curated knowledge base, real-time market and filings feeds via MCP, and a strict risk/compliance envelope, all running on owned GPU infrastructure.

| Dimension | Choice |
|---|---|
| Domicile (target) | Cayman Master / Feeder + Turkish onshore advisor (SPK-licensed) |
| Strategies (Year 1) | 1) BIST L/S equity, 2) TR macro (FX/rates), 3) Event-driven (M&A, capital markets) |
| Strategies (Year 2+) | 4) Global EM equity L/S, 5) Cross-asset volatility, 6) Statistical arbitrage |
| Target AUM | $25M seed → $100M Y2 → $500M Y4 |
| Target gross/net return | 18–25% gross / 12–18% net (Sharpe ≥ 1.5 target) |
| Fee structure | 1.5% / 15% with high-water mark, 1-yr soft lock-up |
| Decision latency | Idea → trade thesis: < 4h. Risk re-rate: < 60s. |
| Human-in-the-loop | All trades > 50bps NAV require PM sign-off. Kill switches always-on. |

---

## 2. Investment Thesis

1. **Information asymmetry is collapsing for global mega-caps but persists in EM and mid-cap names.** BIST in particular has thin sell-side coverage, slow analyst report dissemination, and Turkish-language primary filings that global LLMs handle poorly out-of-the-box. A domain-tuned agent stack with native Turkish corpus wins here.
2. **LLMs are now economically viable as analyst labor.** A senior analyst costs ~$300k/yr fully loaded and covers ~15 names. A specialist agent on a fine-tuned 70B model costs ~$15k/yr in inference and can cover the entire BIST-100 with daily refresh.
3. **The bottleneck is no longer compute or knowledge — it is grounding, orchestration, and risk control.** That is exactly the architectural problem we are good at.

---

## 3. Capability Map

```
                           ┌──────────────────────────────────┐
                           │  Investment Committee (Human)    │
                           │  PM • Risk Officer • Compliance  │
                           └──────────────┬───────────────────┘
                                          │ approves / vetoes
                           ┌──────────────▼───────────────────┐
                           │   PM Agent (Decision Synthesis)  │
                           └──────────────┬───────────────────┘
                                          │
       ┌──────────┬────────────┬──────────┼──────────┬────────────┬──────────┐
       │          │            │          │          │            │          │
   ┌───▼────┐ ┌───▼────┐ ┌─────▼────┐ ┌───▼────┐ ┌───▼────┐ ┌─────▼────┐ ┌───▼────┐
   │Research│ │Quant   │ │Risk      │ │Macro   │ │Event   │ │Compliance│ │Adversa-│
   │Analyst │ │Strate- │ │Manager   │ │Analyst │ │Driven  │ │Agent     │ │ rial   │
   │(CFA)   │ │gist(CQF│ │(FRM)     │ │(CFA)   │ │(CAIA)  │ │(SPK/SEC) │ │ (Red)  │
   └───┬────┘ └───┬────┘ └─────┬────┘ └───┬────┘ └───┬────┘ └─────┬────┘ └───┬────┘
       │          │            │          │          │            │          │
       └──────────┴────────────┴────┬─────┴──────────┴────────────┴──────────┘
                                    │
                          ┌─────────▼──────────┐
                          │  Tool / MCP Layer  │
                          ├────────────────────┤
                          │ Fintables • Quartr │
                          │ TCMB EVDS • KAP    │
                          │ Refinitiv • Apify  │
                          │ Black-Scholes lib  │
                          │ Optimizer (cvxpy)  │
                          └─────────┬──────────┘
                                    │
                          ┌─────────▼──────────┐
                          │   RAG Corpus       │
                          │ CFA L1-L3 • CAIA   │
                          │ FRM • CQF • SPK    │
                          │ KAP filings • TCMB │
                          │ Earnings calls     │
                          └─────────┬──────────┘
                                    │
                          ┌─────────▼──────────┐
                          │  vLLM Serving Layer │
                          │ Qwen3-235B (router)│
                          │ Qwen2.5-72B (LoRA) │
                          │ on H200 cluster    │
                          └────────────────────┘
```

---

## 4. The Seven Agents (one-paragraph specs)

1. **Research Analyst Agent (CFA-grounded)** — produces fundamental theses on individual names: DCF, comps, DuPont, earnings quality, management track record.
2. **Quant Strategist Agent (CQF-grounded)** — runs factor screens, signal generation, backtests, and portfolio construction proposals.
3. **Risk Manager Agent (FRM-grounded)** — computes pre-trade VaR, ES, factor exposures, scenario / stress tests, correlation regimes.
4. **Macro Analyst Agent (CFA-grounded)** — monitors TCMB, Fed, ECB, oil, FX, sovereign credit; produces the daily macro brief.
5. **Event-Driven Agent (CAIA-grounded)** — surveils KAP/SEC filings for M&A, spin-offs, capital raises, governance changes.
6. **Compliance Agent (SPK/SEC-grounded)** — checks every proposed trade against position limits, leverage limits, restricted lists, insider windows, AML.
7. **Adversarial / Red-Team Agent** — explicitly tries to falsify every trade thesis, surface omitted risks, and stress the consensus. Inherits from the PhD-level adversarial multi-agent design.

Detailed system prompts, tools, and routing rules: see [`docs/agents.md`](docs/agents.md).

---

## 5. Tech Stack

| Layer | Choice | Rationale |
|---|---|---|
| Orchestration | **LangGraph** | Stateful graphs, checkpointing, native human-in-the-loop |
| Base LLMs | **Qwen3-235B** (router/PM), **Qwen2.5-72B + LoRA** (specialists) | Open weights, multilingual (TR/EN), runs on owned H200s, no per-token API tax |
| Serving | **vLLM** | Already in production at Architecht; speculative decoding + paged attention |
| Vector store | **Qdrant** (self-hosted) | Hybrid (BM25 + dense), filtering on rich metadata |
| Embeddings | **bge-m3** + **e5-mistral-7b** ensemble | Multilingual; finance-tuned variants where available |
| Workflow store | **Postgres** + **Redis** | LangGraph checkpoints, cache, pub/sub |
| Market data MCP | **Fintables** (BIST), **Quartr** (transcripts), **TCMB EVDS**, **Refinitiv** (global) | Already integrated |
| Web/news | **Apify**, **Bigdata.com** | Structured + unstructured news |
| Backtesting | **vectorbt**, **zipline-reloaded**, custom event simulator | Mature OSS |
| Optimization | **cvxpy**, **PyPortfolioOpt**, **Riskfolio-Lib** | Mean-variance, risk parity, Black-Litterman |
| Execution | **IBKR**, **Garanti BBVA Yatırım** prime, FIX 4.4 | TR + global coverage |
| Observability | **LangSmith** + **Prometheus** + **Grafana** | Trace every agent decision; alert on drift |

---

## 6. Capital, Costs, and Path to Profitability

| Year | AUM (target) | Mgmt fee (1.5%) | Perf fee (15%, assuming 18% gross) | Total revenue | OpEx | Net |
|---|---|---|---|---|---|---|
| Y1 | $25M | $375k | ~$675k | $1.05M | $1.6M | -$550k |
| Y2 | $100M | $1.5M | ~$2.7M | $4.2M | $2.4M | $1.8M |
| Y3 | $250M | $3.75M | ~$6.75M | $10.5M | $3.5M | $7.0M |
| Y4 | $500M | $7.5M | ~$13.5M | $21M | $5.0M | $16M |

**OpEx breakdown (steady state):** ~40% personnel, ~20% data (Bloomberg/Refinitiv/Quartr/Fintables), ~15% prime brokerage + execution, ~10% compute (already amortized via Architecht), ~10% legal/audit/admin, ~5% other.

**Seed required:** ~$2M working capital + $5–10M GP commit signal capital. Total raise target Y0–Y1: **$25M LP + $5M GP**.

---

## 7. KPIs

**Performance (annualized):**
- Net return ≥ 15%
- Sharpe ≥ 1.5
- Max drawdown ≤ 12%
- Beta to BIST-100 ≤ 0.4 (market-neutral target on equity sleeve)
- Hit rate ≥ 55% on conviction trades

**System (per quarter):**
- Agent thesis accuracy (calibrated) ≥ 60% on 90-day forward returns
- Adversarial agent rejection rate: 15–35% (too low → rubber stamp, too high → noise)
- Compliance agent false-positive rate ≤ 5%
- p95 idea-to-trade latency ≤ 4h
- LLM hallucination rate (audited weekly via gold set) ≤ 2%

**Operational:**
- Zero limit breaches per quarter
- 100% of trades have full audit trail (prompt → retrieved context → agent reasoning → decision)
- Quarterly LP report auto-drafted, human-edited

---

## 8. Risk Posture

Argus is **explicitly conservative for an AI-native fund.** The single biggest existential risk is not poor returns — it is a hallucinated trade or a missed compliance breach causing a regulatory or reputational disaster. Hence:

- **Hard kill switch** wired to every agent — any human in compliance/risk can halt the entire stack in one click.
- **Two-key trade arming** — any single trade > 100bps of NAV requires both PM agent recommendation **and** human PM signature.
- **Restricted-list enforcement** is hardcoded, not LLM-judged.
- **All agent outputs are timestamped, hashed, and stored immutably** for 7 years.
- **Adversarial agent runs on every thesis** — its objections must be explicitly resolved in the trade memo.

Full framework: [`docs/risk-compliance.md`](docs/risk-compliance.md).

---

## 9. Roadmap (Headline)

| Phase | Months | Goal |
|---|---|---|
| 0 — Foundation | 0–3 | Legal entity, SPK pre-application, RAG corpus build, agent v0 in paper-trade |
| 1 — Paper Trading | 3–6 | Full agent stack live on paper portfolio, daily PM brief, weekly committee |
| 2 — Friends & Family | 6–9 | $5M GP capital, live trading, slow ramp |
| 3 — Seed Raise | 9–12 | Audited 6-month track, $25M LP target |
| 4 — Scale | 12–24 | Add macro + event-driven sleeves, $100M target |
| 5 — Global EM | 24–36 | Expand to MENA + EM ex-Asia, $250M target |

Detailed milestones: [`docs/roadmap.md`](docs/roadmap.md).

---

## 10. Why this can actually work

- **Owned GPU economics.** Architecht-class H200 capacity removes the per-token tax that kills most AI-fund unit economics.
- **A defensible TR data moat.** Native Turkish RAG over KAP + Fintables + TCMB is hard to replicate from outside Turkey.
- **A rare-skill team.** PhD-level adversarial multi-agent design + production LangGraph + BIST domain knowledge is a small intersection.
- **Realistic ambition.** Year-1 AUM target is intentionally modest. We're optimizing for a clean track and zero blow-ups, not viral launch numbers.

---

## Document Map

| Doc | Purpose |
|---|---|
| [`docs/architecture.md`](docs/architecture.md) | Multi-agent system, LangGraph state machine, data flows |
| [`docs/agents.md`](docs/agents.md) | Per-agent spec: prompts, tools, retrieval namespaces, escalation rules |
| [`docs/strategies.md`](docs/strategies.md) | The actual investment strategies and signal definitions |
| [`docs/data-and-mcps.md`](docs/data-and-mcps.md) | Data sources, MCP plugins, RAG corpus design |
| [`docs/risk-compliance.md`](docs/risk-compliance.md) | Risk framework, regulatory mapping, kill-switch design |
| [`docs/infrastructure.md`](docs/infrastructure.md) | vLLM, Qdrant, Postgres, observability, deployment |
| [`docs/roadmap.md`](docs/roadmap.md) | Month-by-month execution plan |
| [`src/`](src/) | Code skeleton (LangGraph orchestrator + agent + tool stubs) |
