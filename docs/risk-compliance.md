# Risk & Compliance Framework

> The first job of an AI-native fund is to **not** become the cautionary tale. This document is the rule book that protects the franchise.

---

## 1. Risk philosophy

- **Survival first, return second.** Argus targets a Sharpe of 1.5 with max drawdown ≤ 12%, not 25% returns at any cost.
- **Tail risk is real.** EM and TR specifically have fat-tailed return distributions. We size for the tail, not the mean.
- **Leverage is a privilege, not a right.** Gross caps are non-negotiable, regardless of opportunity.
- **Human override always wins.** A human can halt the system in one click, no LLM in the loop.
- **An undocumented trade is a forbidden trade.** Every fill must trace back to a memo.

---

## 2. The risk envelope (hard limits)

These are enforced by a deterministic Python rules engine that runs **after** the Compliance and Risk Agents. No LLM can bypass them.

```
LIMIT                                 HARD CAP
────────────────────────────────────  ─────────
Single name gross                     5% NAV
Single name net (long or short)       4% NAV
Single sector net (GICS L1)           25% NAV
Single country net (ex-TR)            50% NAV
TR country net                        80% NAV
Total equity gross                    180%
Total equity net                      ±60% NAV
FX gross exposure                     60% NAV
Rates DV01                            $50k per bp NAV-normalized
Vega (cross-asset)                    $25k per vol point
Single deal merger arb                3% NAV
Total merger arb book                 15% NAV
1-day 99% portfolio VaR               3.0% NAV
1-day 99.5% Expected Shortfall        4.0% NAV
20-day stressed VaR (2008 scenario)   12% NAV
Liquidity (% in >5d-to-liquidate)     30%
Counterparty concentration (one PB)   60% of margin
Cash & equivalents floor              5% NAV
Single-day net change in gross        ±20% NAV (circuit breaker)
```

Breach behavior:
- **Pre-trade breach** → trade rejected, alert to PM and Risk Officer.
- **Post-trade breach** (mark-to-market move) → automatic reduction trade queued, requires human ack within 60 min, otherwise auto-executes.
- **Egregious breach** (e.g., > 1.5x cap) → kill switch armed automatically; full halt pending committee review.

---

## 3. The kill switch

Three independent kill-switch surfaces:

1. **Web dashboard button** — one click, halts all new orders, cancels all open orders, holds positions, pages the on-call.
2. **Slack / Telegram command** `/argus halt` — same effect, accessible from phone.
3. **Hardware kill** — physical button in the office (yes, really) wired to the same endpoint.

Kill switch can only be released by **two named officers** with separate credentials. No agent can release it.

---

## 4. Pre-trade compliance pipeline

```
proposed trade
     │
     ▼
┌────────────────────────────┐
│ 1. Compliance Agent (LLM)  │  ← nuanced check, returns reasoning
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│ 2. Rules engine (Python)   │  ← mechanical: limits, restricted list
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│ 3. Risk envelope check     │  ← portfolio-level limits
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│ 4. Two-key approval if     │
│    size > 50bps NAV        │
└────────────┬───────────────┘
             │
             ▼
        OMS / FIX
```

Trade only proceeds if **all four** pass. Any fail → log → notify → terminate run.

---

## 5. Restricted list management

Sources fed into the daily restricted-list job:

- Material non-public information (MNPI) wall: anyone at Argus or affiliates with insider knowledge marks the name; the list is loaded into the rules engine.
- TVF / sovereign relationships: any name where the firm has a known conflict (board seat, advisory mandate).
- Insider blackout windows: PM's personal account holdings → no trading by the fund in the same names without committee approval.
- Regulatory restricted lists: SPK + SEC published.
- AML / sanctions: OFAC, EU, UN consolidated lists.

Updated every morning at 06:00 Istanbul. Any change rebroadcasts to all running agent sessions.

---

## 6. Regulatory mapping

Argus must comply with overlapping regimes. The Compliance Agent's RAG namespace covers all of these:

| Regime | Relevant when | Key obligations |
|---|---|---|
| **SPK (TR)** | Always (TR-domiciled advisor) | License, capital adequacy, disclosure, market-abuse, AML |
| **CMB regulations on collective investment** | TR fund vehicle | Risk reporting, NAV publication |
| **SEC (US)** | If accepting US LPs / trading US names | Form ADV, 13F (if > $100M US AUM), Reg M, Rule 105 |
| **MAR (EU)** | If trading EU-listed names | Insider lists, market sounding records, STORs |
| **MiFID II** | If using EU brokers | Best execution, transaction reporting |
| **FATCA / CRS** | Any LPs in scope | Investor due diligence, reporting |
| **GDPR / KVKK (TR)** | LP data, employee data | Lawful basis, DPIA for AI processing |

Material new regulation triggers a compliance review and a corresponding update to the Compliance Agent's prompt + RAG corpus.

---

## 7. Model risk management

Borrowed from SR 11-7 / Basel principles for traditional model risk management, adapted for LLM-driven decisions:

| Practice | Implementation |
|---|---|
| **Model inventory** | Every agent + LoRA + prompt version registered in the model catalog with owner, last review date |
| **Validation** | Quarterly independent validation: prompt eval against gold set, output schema conformance, calibration test |
| **Performance monitoring** | Daily: agent decision quality vs. realized outcomes; weekly: drift detection |
| **Champion/challenger** | Every agent has a shadow model running on the same inputs; swap if challenger beats by ≥ 5% on the gold set for 4 consecutive weeks |
| **Documentation** | Every agent has a "model card" — purpose, training data, evals, known limitations |
| **Change control** | Prompt or model change requires sign-off from Risk Officer + diff review |

---

## 8. The "AI-specific" risks (and our mitigations)

| Risk | Mitigation |
|---|---|
| **Hallucinated facts** | Cite-or-die: numerical claims must reference a `source_id`; post-processor strips uncited numbers |
| **Jailbreak / prompt injection** | All tool outputs sanitized; agent inputs filtered for instruction-injection patterns; agents have no privileged actions (cannot bypass risk envelope) |
| **Concept drift** | Daily eval on gold set; alert on > 5% drop; champion/challenger ready |
| **Adversarial market data** | Sanity checks on tool outputs (price moves > 20% in a tick → flagged); cross-source validation |
| **LP-facing hallucination** | All LP communications human-edited before send |
| **Over-reliance on consensus** | Adversarial agent's job; calibration tracked |
| **Black swan / regime change** | Stress scenarios include past unprecedented moves; long-vol sleeve provides convexity; kill switch always available |
| **Single-point-of-failure infrastructure** | Multi-region deploy; cold standby; manual trading playbook |
| **Vendor data outage** | Per-source SLA monitoring; secondary data source for every primary; no trade gates on a single feed |

---

## 9. Incident response

Severity levels:

| Sev | Definition | Response |
|---|---|---|
| **SEV-1** | Limit breach, kill switch fired, trading halted, > 100bps unexpected loss | All-hands, incident commander assigned, post-mortem within 24h, LP notification within 48h if material |
| **SEV-2** | Agent malfunction without limit breach, data outage > 1h during market hours | On-call engages, post-mortem within 5 days |
| **SEV-3** | Minor degradation, single tool failure, gold-set drift > 5% | Tracked in normal sprint, addressed within 1 week |

Every incident produces a **blameless post-mortem** that becomes a chunk in the `lessons` namespace.

---

## 10. The 7-year audit trail

For every trade ever executed by Argus, we retain:

1. The trigger event (cron / webhook / human request).
2. Frozen market snapshot at trigger time.
3. Every prompt sent to every agent (with hash + version tag).
4. Every model output (with model + LoRA version).
5. Every tool call (request + response + `data_as_of_utc`).
6. Every retrieved RAG chunk (with `source_id` + chunk hash).
7. The PM agent's recommendation.
8. The human approver's identity + timestamp (if applicable).
9. The execution record (venue, fills, fees).
10. The post-trade attribution and P&L.

Stored immutably (write-once Postgres + S3 with object lock). Indexed for fast lookup by trade ID. Available to regulators on demand.

---

## 11. The two questions every trade must answer

Before any trade leaves the system, the PM agent's memo must explicitly answer:

1. **What is the bear case, and why are we taking it anyway?** (Surfaced from the Adversarial Agent's report.)
2. **What single observation would falsify our thesis, and at what price level / date does that trigger our exit?**

Failure to answer either → trade blocked at the PM gate, not the compliance gate. This is a **discipline** check, not a regulatory one — but it is what separates Argus from an AI-flavored momentum chaser.
