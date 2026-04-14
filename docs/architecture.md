# Architecture

## 1. Design principles

1. **Specialization > generalism.** One agent, one job, one curriculum-grounded prompt. The PM agent does synthesis, never primary research.
2. **Every claim must be retrievable.** No agent asserts a number or a fact without a `source_id` pointing to a tool result, a RAG chunk, or a market-data row. Hallucinations are caught by a `cite-or-die` post-processor.
3. **Adversarial as a first-class citizen.** A red-team agent runs against every thesis. Its objections must be acknowledged in the trade memo (resolved or accepted-with-mitigation).
4. **Determinism where possible, sampling where useful.** Risk calcs, compliance checks, and optimization are deterministic. Idea generation and macro framing use temperature > 0.
5. **Stateful, resumable, auditable.** LangGraph checkpoints into Postgres on every node transition. Any decision can be replayed bit-for-bit.

---

## 2. The graph

LangGraph state machine. Nodes are agents or tool-callers; edges are conditional routing.

```
                   ┌────────────┐
                   │  ingest    │  (cron / webhook trigger)
                   └─────┬──────┘
                         ▼
                   ┌────────────┐
                   │  classify  │  (intent: idea | event | risk | macro | trade-review)
                   └─────┬──────┘
        ┌────────────────┼─────────────────┬────────────────┐
        ▼                ▼                 ▼                ▼
   ┌─────────┐     ┌──────────┐      ┌─────────┐     ┌──────────┐
   │research │     │event_drv │      │ macro   │     │ rebal/   │
   │_analyst │     │  agent   │      │_analyst │     │ risk     │
   └────┬────┘     └────┬─────┘      └────┬────┘     └────┬─────┘
        │                │                 │               │
        └────────┬───────┴─────────┬───────┘               │
                 ▼                 ▼                       ▼
            ┌─────────┐       ┌──────────┐           ┌──────────┐
            │  quant  │◄──────│ thesis_  │           │  risk_   │
            │_strateg.│       │ collator │           │ manager  │
            └────┬────┘       └────┬─────┘           └────┬─────┘
                 │                 │                      │
                 └────────┬────────┘                      │
                          ▼                               │
                   ┌────────────┐                         │
                   │adversarial │                         │
                   │  red-team  │                         │
                   └─────┬──────┘                         │
                         │                                │
                         ▼                                ▼
                   ┌────────────┐                  ┌──────────┐
                   │ compliance │◄─────────────────│ risk     │
                   │   gate     │                  │ envelope │
                   └─────┬──────┘                  └──────────┘
                         │
                         ▼
                   ┌────────────┐
                   │ PM agent   │  (synthesis, sizing, memo)
                   └─────┬──────┘
                         │
                  ┌──────┴───────┐
                  ▼              ▼
            ┌──────────┐    ┌──────────┐
            │ auto-    │    │ human-   │
            │ execute  │    │ approval │
            │ (<50bps) │    │ queue    │
            └────┬─────┘    └────┬─────┘
                 │               │
                 └───────┬───────┘
                         ▼
                   ┌────────────┐
                   │  OMS / FIX │
                   └─────┬──────┘
                         ▼
                   ┌────────────┐
                   │ post-trade │  (TCA, P&L attribution, journal)
                   └────────────┘
```

### Node types

- **Ingest**: cron triggers (08:00 daily macro brief, 17:00 EOD reconciliation), KAP/SEC webhooks, price-move triggers.
- **Agent nodes**: invoke an LLM with a system prompt + tools; outputs structured JSON conforming to a Pydantic schema.
- **Tool nodes**: deterministic Python — calls into MCPs or local libs.
- **Gate nodes**: hardcoded boolean checks (compliance, risk envelope). No LLM in the loop.

---

## 3. State schema

```python
class FundState(BaseModel):
    # identifiers
    run_id: UUID
    parent_run_id: Optional[UUID]            # for replays
    triggered_by: Literal["cron","webhook","human","agent"]
    timestamp_utc: datetime

    # input
    intent: Literal["idea","event","risk","macro","rebal","trade-review"]
    payload: dict                            # raw trigger data

    # working memory
    universe: list[Ticker]                   # tickers in scope this run
    retrieved_context: list[RetrievedChunk]  # RAG hits, with source_ids
    market_snapshot: MarketSnapshot          # prices, vols, rates frozen at run start

    # agent outputs (each agent writes its own slot)
    research: Optional[ResearchThesis]
    quant: Optional[QuantSignal]
    macro: Optional[MacroBrief]
    event: Optional[EventReport]
    risk: Optional[RiskAssessment]
    adversarial: Optional[RedTeamReport]
    compliance: Optional[ComplianceVerdict]

    # decision
    pm_recommendation: Optional[TradeRecommendation]
    final_decision: Optional[Literal["execute","reject","escalate"]]

    # audit
    prompt_hashes: dict[str, str]            # agent_name -> sha256 of system prompt
    model_versions: dict[str, str]           # agent_name -> model id + LoRA tag
    tool_calls: list[ToolCall]               # full trace
```

Every field is checkpointed after every node. A run can be resumed from any failure point, or branched to test a counterfactual ("what would PM have said if compliance hadn't blocked?").

---

## 4. Routing rules (selected)

```python
def route_after_classify(state: FundState) -> str:
    if state.intent == "macro":     return "macro_analyst"
    if state.intent == "event":     return "event_driven"
    if state.intent == "risk":      return "risk_manager"
    if state.intent == "rebal":     return "quant_strategist"
    return "research_analyst"  # default for "idea" and "trade-review"

def route_after_thesis_collator(state) -> list[str]:
    # always run quant + adversarial in parallel after a thesis is formed
    return ["quant_strategist", "adversarial"]

def route_after_compliance(state) -> str:
    if state.compliance.verdict == "block":
        return "log_and_terminate"
    if abs(state.pm_recommendation.size_bps) > 50:
        return "human_approval"
    return "auto_execute"
```

---

## 5. Memory model

Three memory tiers, each with a different retention policy:

| Tier | Store | Contents | Retention |
|---|---|---|---|
| Short-term | LangGraph state | Working memory of a single run | Lives with the run |
| Episodic | Postgres | Every completed run, fully replayable | 7 years (regulatory) |
| Semantic | Qdrant | RAG corpus + agent-distilled "lessons" | Indefinite, versioned |

### Episodic memory → semantic memory loop

A nightly job picks the top-k decisions by P&L impact (winners and losers), distills them into a "lesson" chunk via a summarizer agent, and indexes them into the `lessons` Qdrant namespace. Future agents retrieve from `lessons` alongside the static curriculum corpus. This is how the system learns without retraining the base model.

---

## 6. Inter-agent contracts

Every agent emits a Pydantic model. No agent reads another agent's prose — they read the structured object. Example:

```python
class ResearchThesis(BaseModel):
    ticker: Ticker
    direction: Literal["long","short"]
    conviction: float                        # 0.0–1.0, calibrated via Brier score
    horizon_days: int
    target_price: float
    target_price_methodology: Literal["DCF","comps","SOTP","other"]
    catalysts: list[Catalyst]
    key_risks: list[Risk]
    citations: list[SourceID]                # required, min 3
    confidence_intervals: dict               # explicit uncertainty
```

If a downstream agent (e.g., quant strategist) needs something the upstream agent didn't provide, it requests it via a structured `ClarificationRequest` that re-enters the graph at the right node — no telephone game.

---

## 7. Failure modes & their guards

| Failure | Guard |
|---|---|
| LLM hallucinates a number | `cite-or-die` post-processor; numbers must come from tool calls |
| Tool returns stale data | Every tool result tagged with `data_as_of_utc`; PM agent rejects if > staleness threshold |
| Agent loops (calls itself / each other) | LangGraph cycle limit per run (default 12) |
| Adversarial agent is rubber-stamping | Weekly audit: if rejection rate < 10%, sample-review and possibly retrain |
| Compliance miss | Hardcoded restricted-list check happens **after** the LLM compliance agent — belt and braces |
| Model degradation | Daily eval on a frozen 200-question gold set; alert if accuracy drops > 5% |
| Vector store poisoning | All ingested chunks signed by source; integrity check on retrieval |

---

## 8. Why LangGraph (vs. CrewAI / AutoGen / hand-rolled)

- **Native checkpointing** to Postgres — essential for audit and replay.
- **Conditional edges** — the graph really is a graph, not a chain or a free-for-all.
- **Human-in-the-loop primitives** — `interrupt()` is first-class, not bolted on.
- **Already in production** in the team's prior work; zero learning curve cost.
- **Open source**, no vendor lock-in.

CrewAI was considered but its role-play abstraction is too loose for an audited financial workflow. AutoGen's group-chat model risks message explosion. A hand-rolled orchestrator was rejected on the "you don't need to write your own state machine" principle.
