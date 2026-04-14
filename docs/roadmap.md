# Roadmap

A 24-month execution plan, organized in six phases. Each phase has explicit gates — we don't advance until the gate is met.

---

## Phase 0 — Foundation (Months 0–3)

**Goal:** Legal entity stood up, infra deployed, RAG corpus v1 indexed, agent stack v0 running on paper.

### Workstreams

**Legal & regulatory**
- Engage Turkish legal counsel; submit SPK portfolio management license pre-application
- Engage Cayman counsel for master/feeder structuring
- Draft PPM, LPA, subscription docs (templates from prior funds, customized)
- Engage fund administrator (Apex / Trident / Citco) — RFP and shortlist
- Auditor selection (Big 4 — KPMG or PwC TR)
- D&O insurance quotes

**Tech foundation**
- Stand up k8s cluster on Architecht infra
- Deploy vLLM with Qwen2.5-72B + Qwen3-235B
- Deploy Qdrant cluster, Postgres, Redis
- Wire up MCPs: Fintables, Quartr, TCMB EVDS, Bigdata.com
- LangGraph orchestrator skeleton (the [`src/`](../src/) tree in this repo)
- LangSmith / Langfuse for tracing

**Data**
- License + ingest CFA L1, L2, L3 curriculum (this is the largest single ingest job)
- License + ingest CAIA L1, L2
- License + ingest FRM Part I, II
- License + ingest CQF curriculum
- Build KAP filings backfill (5y rolling)
- Build SEC EDGAR ingestion for global universe candidates
- Build Quartr transcripts pipeline (BIST-100 priority)

**Agents v0**
- Implement all 7 agents with v1 prompts
- Build the gold-set evals (200 questions per agent)
- Implement deterministic risk envelope + restricted list
- Implement the kill switch (web + Slack + hardware)

### Gate to advance to Phase 1

- All 7 agents pass their gold-set eval at ≥ 70%
- End-to-end: a triggered run produces a memo, traverses compliance, simulates execution, posts to journal
- Risk envelope blocks 100% of synthetic limit-breach attempts
- Kill switch tested in DR drill
- SPK pre-application acknowledged

---

## Phase 1 — Paper Trading (Months 3–6)

**Goal:** Run the full agent stack on a $10M paper portfolio for 90 calendar days. Daily PM brief, weekly investment committee.

### Workstreams

**Operations**
- Daily 08:00 macro brief published internally
- Daily 17:00 P&L attribution + risk dashboard
- Weekly investment committee (Mondays 10:00) reviewing all proposed trades
- All trades simulated in OMS sandbox; modeled fills using historic spreads
- Adversarial agent's objections explicitly logged + tracked

**Calibration**
- Track agent calibration: predicted probabilities vs. realized outcomes
- Weekly retro: which agents under/over-confident, which signals worked
- Begin populating the `lessons` namespace

**Improvements**
- Iterate prompts based on PM feedback
- Train first LoRA adapters on PM-edited memos
- Champion/challenger framework live

### Gate to advance to Phase 2

- 90 days of clean paper trades, zero kill-switch events
- Agent calibration: predicted-vs-actual within 10pp
- Adversarial rejection rate in 15–35% target band
- Compliance agent zero false-negatives on red-team tests
- Paper Sharpe ≥ 1.0 (we'd like 1.5 but won't gate on it; paper-trading luck is real)
- SPK license received OR clear path to receipt within 60 days

---

## Phase 2 — Friends & Family (Months 6–9)

**Goal:** First live capital. $5M GP commit + ~$5–10M friends & family. Trading real money slowly.

### Workstreams

**Go-live**
- Fund admin live, NAV calc daily, audited monthly
- IBKR + TR Prime broker accounts funded
- First trade executed (planned, small, well-understood name) — celebrate, then pretend it never happened
- Slow capital deployment over 6 weeks (target 70% deployed by end of week 6)

**Operations**
- Live attribution vs. paper attribution — investigate every divergence > 25bps
- LP-grade reporting infrastructure (monthly NAV statement, quarterly letter draft pipeline)
- Counterparty due diligence on prime broker, custodians

**Improvements**
- First quarter's lessons distilled and indexed
- Begin recording earnings calls in real-time for Quartr-fast turnaround
- Build the "watchlist" feature — names the agents are studying but haven't transacted

### Gate to advance to Phase 3

- 90 days of live trading, zero limit breaches, zero compliance incidents
- Live performance within 100bps of paper performance (proves simulation fidelity)
- Audit clean
- LP statements going out on time, no errors
- Two LP references willing to talk to seed-stage prospects

---

## Phase 3 — Seed Raise (Months 9–12)

**Goal:** Build a 6-month audited live track record, run a structured seed raise to $25M LP capital.

### Workstreams

**Fundraising**
- Pitch deck, DDQ, 6-month track record
- Target investors: TR family offices (15+), regional pensions (3–5), select global EM allocators (5–10)
- Cap intro events, conferences (SuperReturn, Context Summits)
- Maintain "no fee discount for seed" discipline (founders' fee class only for top 3 anchors)

**Operations**
- Hire: COO/CFO, second portfolio manager, head of investor relations
- Office space (currently working from Architecht / TVF infrastructure-of-convenience)
- Annual independent audit

**Tech**
- v2 of the agent stack — second LoRA refresh, expanded gold sets
- First "lessons" retrieval producing measurable improvement on calibration

### Gate to advance to Phase 4

- $25M committed (target); $15M minimum to advance
- 6-month live track: net return annualized ≥ 12%, Sharpe ≥ 1.2, max DD ≤ 8%
- Operational due diligence by 3+ allocators passed
- Team: at minimum CIO, COO/CFO, 2x analyst-PM, head of risk

---

## Phase 4 — Scale (Months 12–24)

**Goal:** Add the macro and event-driven sleeves, scale capital to $100M+, prove scalability of the AI infrastructure.

### Workstreams

**Strategy expansion**
- TR Macro sleeve goes live (was paper-trading throughout Phase 2–3)
- Event-driven sleeve goes live
- Cross-asset volatility hedge sleeve added
- Stat arb sleeve evaluated; goes live only if capacity-tested

**Capital**
- Open capacity for additional $50–75M
- Begin discussions with global EM allocators (CalPERS-tier names)
- Maintain quarterly subscriptions, ensure no sleeve becomes capacity-constrained

**Tech**
- Multi-region deployment
- Proper DR setup with quarterly drills
- Begin work on global EM equity sleeve (Year 2+)
- Custom embeddings model fine-tune on TR financial corpus (research project)

**Team**
- Headcount target: 12 (CIO, COO/CFO, 4 PM/analyst, 2 risk/compliance, 4 engineering)

### Gate to advance to Phase 5

- $100M AUM
- 18-month live track: net return annualized ≥ 15%, Sharpe ≥ 1.5, max DD ≤ 10%
- 3+ sleeves in production with independent attribution
- Zero limit breaches, zero compliance incidents to date
- Allocator DDQ pass rate ≥ 80% on the institutional tier

---

## Phase 5 — Global EM (Months 24–36)

**Goal:** Add global EM equity sleeve. Scale to $250M+. Begin to build the institutional client base.

### Workstreams

**Strategy expansion**
- Global EM equity sleeve live (Brazil, Mexico, SA, Indonesia, Vietnam, KSA, UAE, Egypt — explicitly excluding China A-shares)
- Multilingual RAG corpus: Arabic + Portuguese + Spanish curriculum + filings
- Hire 1–2 regional specialists

**Capital & client base**
- $250M target
- Open separately managed accounts (SMAs) for $50M+ allocators on demand
- Annual investor conference

**Tech**
- Larger fine-tunes (consider full fine-tune of a 70B for the Research Analyst role given accumulated training data)
- Real-time anomaly detection layer added
- Public API for LP positional reporting

---

## Critical path & dependencies

```
                Phase 0 (3mo)
                    │
            ┌───────┴────────┐
            ▼                ▼
      SPK license       Gold-set ≥ 70%
            │                │
            └────────┬───────┘
                     ▼
                Phase 1 (3mo paper)
                     │
                Calibration OK
                     │
                     ▼
                Phase 2 (3mo F&F)
                     │
                Live = paper ± 100bps
                     │
                     ▼
                Phase 3 (3mo seed raise)
                     │
                $15M+ committed
                     │
                     ▼
                Phase 4 (12mo scale)
                     │
                $100M + 3 sleeves
                     │
                     ▼
                Phase 5 (12mo global EM)
```

The hardest gate is **Phase 1 → Phase 2**: the SPK license. Start that on Day 1. Everything else is in our control; that one isn't.

---

## What can derail this

| Risk | Mitigation |
|---|---|
| SPK license delayed beyond 12 months | Start Day 1; engage former SPK officials as advisors; have a Cayman-only Plan B that markets to non-TR LPs only |
| Founding PM departure | Founder vesting + equity locks; co-PM hired by Phase 3 |
| First-year drawdown > 10% | Conservative sizing in Phase 2; intentionally low capital deployment in early months; clear LP communication |
| LLM model regression / capability stagnation | Open-weight stack means we can swap base models; champion/challenger always running |
| TR macro shock (lira crisis, snap election) | Macro sleeve and long-vol sleeve are designed for exactly this; risk envelope holds |
| Key-vendor outage (Fintables, Quartr) | Secondary sources for every primary; manual operating mode documented |
| Insider trading / market abuse incident | Hardcoded restricted list + LLM compliance + insider window checks; this is the existential risk and the reason for the belt-and-braces design |

---

## Decision points the founder should sit with now

1. **Geographic strategy.** Is the long game TR-anchored EM specialist, or is TR a stepping stone to a global multi-strat? Both are viable; the answer changes Phase-5 hiring.
2. **AUM ceiling discipline.** Many funds blow up by raising past their alpha decay point. Argus should probably soft-cap at $1.5–2B even if demand exists, to preserve TR/EM mid-cap edge.
3. **Open-source posture.** Some of the engineering (LangGraph patterns, prompt templates) could be open-sourced as a marketing flywheel. Most cannot. The line should be drawn explicitly.
4. **Public-facing brand.** Argus is a fund name, not a tech-product brand. If there's any thought of building a separate AI-tooling business off this, set up the IP and entity structure now, not later.
