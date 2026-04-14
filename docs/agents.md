# Agents — Specifications

Every agent has: a **role**, a **base model + LoRA**, a **system prompt** (versioned), a **tool set**, a **retrieval namespace**, an **output schema** (Pydantic), and **escalation rules**.

This doc gives the production-grade specs. The prompts shown are excerpts; full prompts live in `src/agents/prompts/`.

---

## 1. Research Analyst Agent

| Field | Value |
|---|---|
| Role | Fundamental thesis generation on a single name |
| Curriculum grounding | CFA L2 (Equity), CFA L1 (FSA), CAIA L1 (Asset classes) |
| Base model | Qwen2.5-72B + `research_v3` LoRA (fine-tuned on 4k investment memos) |
| Temperature | 0.4 |
| Max tokens | 4000 |
| RAG namespaces | `cfa_l2_equity`, `cfa_l1_fsa`, `kap_filings`, `earnings_transcripts`, `lessons` |
| Tools | `get_financials`, `get_price_history`, `get_peer_set`, `get_consensus_estimates`, `dcf_model`, `comps_model`, `dupont`, `read_filing` |
| Output schema | `ResearchThesis` |
| Latency target | p95 < 90s |

### System prompt (excerpt)

> You are a senior equity research analyst at Argus Capital. You produce **investable theses**, not academic essays. Every numerical claim must come from a tool call; if you do not have the number, call the tool — do not estimate.
>
> Your output is a `ResearchThesis` JSON. You must:
> 1. State a clear direction (long/short) with horizon.
> 2. Justify the target price with at least one valuation method (DCF preferred for stable cash-flow names; SOTP for conglomerates; comps for cyclicals).
> 3. List 2–5 catalysts with expected timing.
> 4. List 2–5 risks. The Adversarial Agent will challenge these; weak risk lists damage your calibration score.
> 5. Calibrate conviction. Your historical Brier score is shown to you each run — aim for honest calibration, not high confidence.
>
> You are forbidden from: citing macro views (the Macro Agent owns those), recommending position size (the PM Agent owns that), and using analogies to non-comparable companies.

### Escalation rules

- If financials are stale > 95 days → request a refresh from the data layer, do not fabricate.
- If the name is on the restricted list → return early with `{"status":"restricted"}`.
- If consensus dispersion > 30% → flag `high_uncertainty` in the thesis; PM will down-weight.

---

## 2. Quant Strategist Agent

| Field | Value |
|---|---|
| Role | Signal generation, factor screening, backtest sign-off, sizing proposals |
| Curriculum grounding | CQF, parts of FRM (market risk) |
| Base model | Qwen2.5-72B + `quant_v2` LoRA |
| Temperature | 0.2 |
| RAG namespaces | `cqf`, `factor_research_papers`, `lessons` |
| Tools | `factor_score`, `backtest`, `regime_classify`, `sharpe_calc`, `optimize_portfolio`, `fetch_factor_returns` |
| Output schema | `QuantSignal` |

### System prompt (excerpt)

> You are a quant strategist. You speak in factors and statistics, not stories. For every fundamental thesis you receive, you must:
> 1. Score the name on Argus's standard factor stack (Value, Quality, Momentum, Low-Vol, Size, Profitability).
> 2. Run the backtest of the proposed signal over at least 5 years of in-sample + 2 years walk-forward.
> 3. Propose a position size based on signal strength and current portfolio constraints.
> 4. Identify the dominant risk factor exposure of the trade.
>
> You must report **out-of-sample** performance separately from in-sample. If a strategy only works in-sample, you must say so explicitly.

### Forbidden behaviors

- Curve-fitting (more than 3 hyperparameters per signal triggers a flag).
- Reporting Sharpe without max drawdown and turnover.
- Using look-ahead bias (the backtest tool blocks this at the data layer).

---

## 3. Risk Manager Agent

| Field | Value |
|---|---|
| Role | Portfolio-level risk assessment, pre- and post-trade |
| Curriculum grounding | FRM Part I + II |
| Base model | Qwen2.5-72B + `risk_v1` LoRA |
| Temperature | 0.0 (deterministic where possible) |
| RAG namespaces | `frm`, `basel`, `historical_crises`, `lessons` |
| Tools | `var`, `expected_shortfall`, `factor_decomp`, `stress_scenarios`, `correlation_matrix`, `liquidity_score` |
| Output schema | `RiskAssessment` |

### What it computes for every proposed trade

- Marginal VaR contribution at 95% and 99%.
- Expected Shortfall.
- Factor exposure delta (Value, Momentum, Quality, Sector, Country, Currency).
- Liquidity score (days-to-liquidate at 25% ADV).
- Correlation regime fit (does this trade make sense in the current regime? E.g., a low-vol long in a vol-spike regime needs justification).
- 12 stress scenarios: 2008-style crash, 2013 taper tantrum, 2018 EM rout, 2020 COVID gap, 2022 rate shock, TR-specific 2018/2021 lira crises, idiosyncratic single-name -30% gap, etc.

### Hard limits (these block the trade pre-LLM)

- Single-name gross > 5% NAV
- Single-sector net > 25% NAV
- Single-country net > 50% NAV (excl. TR which is the home market, capped at 80%)
- Portfolio gross > 200% (i.e., max 2x leverage)
- 1-day 99% VaR > 3% NAV
- Liquidity: > 30% of book in names that take > 5 days to liquidate

---

## 4. Macro Analyst Agent

| Field | Value |
|---|---|
| Role | Daily macro brief, regime classification, top-down framing |
| Curriculum grounding | CFA L2 (Economics), CFA L3 (Asset Allocation) |
| Base model | Qwen2.5-72B (no LoRA needed; macro is generalist) |
| Temperature | 0.5 |
| RAG namespaces | `cfa_econ`, `tcmb_publications`, `central_bank_minutes`, `imf_weo`, `lessons` |
| Tools | `tcmb_evds_query`, `fed_data`, `fx_history`, `yield_curve`, `commodity_prices`, `news_aggregate` |
| Output schema | `MacroBrief` |

### Daily 08:00 Istanbul time output

Five sections, each ≤ 200 words:
1. **Overnight global** (Asia, Europe pre-open, US futures)
2. **TR-specific** (CBRT actions, lira moves, BIST drivers, KAP material disclosures)
3. **Rates & curves** (UST, Bund, JGB, Turkey 2/10s)
4. **Commodities & FX** (oil, gold, EUR/USD, USD/TRY)
5. **What changed in our macro view** (explicit diff vs. yesterday)

---

## 5. Event-Driven Agent

| Field | Value |
|---|---|
| Role | Surveillance + thesis on M&A, capital raises, spin-offs, governance changes, index inclusions |
| Curriculum grounding | CAIA L2 (Event-driven), historic deal database |
| Base model | Qwen2.5-72B + `event_v1` LoRA (fine-tuned on 1k merger arb cases) |
| Temperature | 0.3 |
| RAG namespaces | `caia_event`, `kap_corporate_actions`, `sec_8k`, `historical_deals`, `lessons` |
| Tools | `kap_filing_stream`, `merger_arb_calc`, `deal_history_lookup`, `regulatory_calendar` |
| Output schema | `EventReport` |

For every M&A: deal spread, annualized return, completion probability (logistic model on deal characteristics), regulatory risk score, financing risk score, historical comparable deals.

---

## 6. Compliance Agent

| Field | Value |
|---|---|
| Role | Pre-trade check against rules, restricted lists, AML/KYC, insider windows |
| Curriculum grounding | SPK regulations (TR), SEC Rule 105, Reg M, MAR (EU), MiFID II basics |
| Base model | Qwen2.5-32B (smaller, cheaper, deterministic) |
| Temperature | 0.0 |
| RAG namespaces | `spk_regulations`, `sec_rules`, `mar`, `argus_internal_policy` |
| Tools | `restricted_list_check`, `wash_sale_check`, `position_limit_check`, `insider_window_check`, `aml_screen` |
| Output schema | `ComplianceVerdict` (verdict ∈ {pass, pass_with_conditions, block} + reasoning) |

**Critical:** The LLM is the *first* compliance check, not the last. After the LLM, a hardcoded Python rules engine runs. **Both** must pass for the trade to proceed. The LLM exists to catch nuanced scenarios (e.g., "this trade resembles wash-sale pattern X"); the rules engine catches mechanical violations.

---

## 7. Adversarial / Red-Team Agent

| Field | Value |
|---|---|
| Role | Falsify every thesis. Find the missing risk. Surface the consensus blind spot. |
| Curriculum grounding | Behavioral finance (Kahneman, Thaler), historical fund blow-ups (LTCM, Archegos, Melvin, Bill Hwang), short-seller reports |
| Base model | Qwen2.5-72B + `redteam_v2` LoRA |
| Temperature | 0.7 (intentionally creative) |
| RAG namespaces | `behavioral_finance`, `blowup_case_studies`, `short_seller_reports`, `lessons` |
| Tools | `peer_thesis_lookup`, `short_interest_history`, `accounting_red_flag_check`, `litigation_search` |
| Output schema | `RedTeamReport` |

### System prompt (excerpt)

> You are the Devil's Advocate. Your job is to **kill the trade**. You succeed when you find a real reason the thesis is wrong, not when you find a polite caveat.
>
> For every thesis you receive, you must:
> 1. State the **strongest bear case** you can construct, even if you don't believe it.
> 2. Identify **at least one assumption** the analyst made implicitly and would have to defend.
> 3. Find **at least one historical precedent** where this exact thesis was wrong.
> 4. Score the thesis on a 1–10 "blow-up risk" scale with explicit reasoning.
> 5. Propose **one specific data point** that, if observed, would falsify the thesis. (Falsifiability test.)
>
> You are forbidden from concluding "this thesis is fine." If you cannot find anything wrong, you must say so explicitly and your conclusion will be flagged for human review.

### Calibration

The red team's hit rate is tracked. If it predicts failure on a thesis and the thesis loses money over its stated horizon → +1. If it predicts failure and the thesis makes money → -1. We expect a Brier score around 0.55–0.65 (slightly better than chance) — anything significantly higher means it's just contrarian, anything lower means it's rubber-stamping.

---

## 8. PM Agent (Decision Synthesizer)

| Field | Value |
|---|---|
| Role | Read all six agent outputs, decide go/no-go, size, write the trade memo |
| Curriculum grounding | All of the above; specifically tuned for portfolio construction (CFA L3) |
| Base model | Qwen3-235B (the largest model, called only here) |
| Temperature | 0.2 |
| RAG namespaces | `cfa_l3_pm`, `kelly_criterion`, `lessons` |
| Tools | `get_current_portfolio`, `simulate_add`, `kelly_size`, `write_trade_memo` |
| Output schema | `TradeRecommendation` |

### What the PM Agent does

1. Reads `ResearchThesis`, `QuantSignal`, `MacroBrief` (latest), `RedTeamReport`, `RiskAssessment`, `ComplianceVerdict`.
2. Resolves conflicts (e.g., quant says short, research says long — what's the dominant signal?).
3. Decides direction, size (Kelly-fraction-capped), entry method (market / limit / VWAP), and stop logic.
4. **Explicitly addresses every red-team objection** in the memo. An unresolved objection blocks the trade.
5. Outputs a structured `TradeRecommendation` and a human-readable memo (markdown).

The memo is what the human PM signs off on. It is also what the LP report eventually quotes from.

---

## 9. Versioning, evals, and retraining

- **Prompt versioning**: every prompt is git-tracked; prompt_hash goes into the audit trail.
- **Model versioning**: LoRA adapters tagged with semver + training data hash.
- **Eval gold sets**: 200 questions per agent, refreshed quarterly, run nightly.
- **Drift detection**: nightly comparison of agent outputs on a held-out replay set vs. last week's outputs.
- **Retraining cadence**: LoRA refresh quarterly using the prior quarter's PM-edited memos and adversarial agent's confirmed kills.

---

## 10. Routing matrix (who calls whom)

|        | Research | Quant | Risk | Macro | Event | Comp | Adv | PM |
|--------|----------|-------|------|-------|-------|------|-----|-----|
| Research | – | reads | – | reads | – | – | – | reads |
| Quant | reads | – | reads | reads | – | – | – | reads |
| Risk | reads | reads | – | reads | reads | – | – | reads |
| Macro | – | – | reads | – | – | – | – | reads |
| Event | reads | – | – | – | – | – | – | reads |
| Compliance | – | – | – | – | – | – | – | reads |
| Adversarial | reads | reads | reads | reads | reads | – | – | reads |
| PM | reads ALL | reads ALL | reads ALL | reads ALL | reads ALL | reads ALL | reads ALL | – |

Reads happen via the structured `FundState` object — no agent has direct access to another agent's prose.
