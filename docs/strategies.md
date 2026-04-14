# Investment Strategies

This is the actual menu of strategies Argus trades. Each is a separate "sleeve" with its own capital allocation, risk budget, and dedicated agent specialization.

---

## Sleeve 1 — BIST Long/Short Equity (anchor strategy)

**Capital allocation:** 50% of NAV at launch, scaling down to 35% as other sleeves prove out.

**Universe:** BIST-100 + 30 selected mid-caps (BIST-150 ex names with < $20M ADV).

**Style:** Fundamental long/short with a quant overlay. Target market beta 0.0 ± 0.3.

### Signals

| Signal | Source | Weight | Horizon |
|---|---|---|---|
| Earnings revision (consensus +/– 28d) | Fintables, broker reports | 25% | 60d |
| Analyst report sentiment shift | Daily KAP analyst reports + Quartr | 15% | 30d |
| Quality factor (ROIC, FCF yield, net debt/EBITDA) | Filings | 20% | 180d |
| Momentum (12-1m, risk-adjusted) | Prices | 15% | 90d |
| Insider transactions (KAP disclosure) | KAP | 10% | 60d |
| Earnings call sentiment delta | Quartr transcripts → LLM scoring | 15% | 90d |

**Combination:** weighted z-scores → composite alpha → top quintile long, bottom quintile short. Discretionary overlay from Research Analyst Agent + PM Agent: any name failing the qualitative test (governance, accounting integrity, stranded asset) is removed regardless of quant score.

### Position sizing

Kelly-fraction-capped at 25% of full Kelly to prevent over-betting on noisy signals. Max single-name = 5% gross / 4% net.

### Hedging

Net BIST-100 beta hedged with XU100 futures (VIOP) when |beta| > 0.2.

---

## Sleeve 2 — TR Macro (FX, rates)

**Capital allocation:** 20% NAV.

**Style:** Discretionary directional / RV (relative value) on USD/TRY, EUR/TRY, Turkish 2Y/10Y yields, CDS, and inflation-linked vs. nominal spread.

**Edge thesis:** TCMB policy regime shifts are infrequent but high-magnitude events. The Macro Agent monitors:
- TCMB rate decisions and minutes
- CBRT reserves (gross + net)
- Inflation prints (CPI, PPI, core)
- Current account, capital flows
- Political calendar (elections, cabinet reshuffles)

Plus narrative monitoring across Bigdata.com news and Apify-scraped TR financial press.

### Trade types

1. **Outright USD/TRY direction** (sized small; max 1% NAV at risk per trade, hedged with options where vol is reasonable)
2. **2s10s steepener / flattener** when curve is at extremes
3. **Real vs. nominal yield spread** as inflation expectations gauge
4. **Sovereign CDS** vs. similar-rated peers (ZAR, BRL, MXN sovereigns)

### Risk

USD/TRY positions sized by 99% 1-week ES, capped at 50bps NAV per position. No naked short USD/TRY > 100bps NAV (the lira can devalue rapidly; the asymmetry favors caution).

---

## Sleeve 3 — Event-Driven (M&A, capital markets, index inclusions)

**Capital allocation:** 15% NAV.

**Style:** Merger arbitrage, post-IPO drift, secondary offering plays, BIST/MSCI index inclusion-exclusion trades.

### Trade types

1. **TR M&A arb** — KAP-disclosed deals; the Event Agent computes spread, completion probability, regulatory risk.
2. **Cross-border arb** — TR companies acquired by/ acquiring foreign entities; FX-hedged.
3. **Capital market events** — secondary offerings (often discount → reversal trade), rights issues, spin-offs.
4. **Index rebalances** — XU100, MSCI Turkey: anticipatory positioning ahead of effective date, exit on event.

### Edge thesis

TR event-driven space is under-served by global merger arb shops (too small, too local). Local players exist but lack systematic discipline. Argus's Event Agent watches KAP in near-real-time (sub-5-minute latency on disclosures) and runs a calibrated probability model on every announced deal.

---

## Sleeve 4 — Global EM Equity (Year 2+)

**Capital allocation:** 10% NAV at launch, scaling to 20% Year 2.

**Universe:** MSCI EM constituents in: Brazil, Mexico, South Africa, Indonesia, Vietnam, Saudi Arabia, UAE, Egypt. Explicitly excluding China A-shares for political risk reasons.

**Style:** Pair trades within EM (e.g., long PETR4, short PBR; long Brazilian banks, short SA banks) and country tilts based on macro regime classification.

### Edge thesis

These markets share structural traits with TR (EM volatility, FX exposure, sovereign-corporate linkages). The macro framework and country-level fundamental work transfers. We avoid markets where local language barriers would cripple the RAG corpus until we can fund Arabic / Portuguese curriculum builds.

---

## Sleeve 5 — Cross-Asset Volatility (Year 2+)

**Capital allocation:** 5% NAV.

**Style:** Long-volatility tail hedges + selective short-volatility carry. The "cheap insurance" sleeve.

### Trade types

1. **VIX call spreads** when VIX is < 15 and Argus's macro stress score is elevated
2. **Put-spread collars** on BIST-100 around known event windows (TCMB meetings, elections)
3. **Variance swap dispersion** (long single-name vol, short index vol) when correlations are at extremes

### Function

This sleeve exists primarily as a portfolio hedge. Its expected return is modestly negative most quarters, with positive convexity in stressed environments. Sized to absorb ~30% of expected portfolio drawdown in a 2-sigma stress scenario.

---

## Sleeve 6 — Statistical Arbitrage (Year 2+, optional)

**Capital allocation:** 5% NAV.

**Style:** Short-horizon (1-5d) mean-reversion and pairs trading on the BIST-150, fully systematic.

### Edge thesis

BIST microstructure has retail-driven mean reversion patterns that persist after transaction costs for small books. This sleeve is capacity-constrained (probably caps at $25M before alpha decays). Worth running because:
- It diversifies horizon (the rest of the book is 30-180 day)
- It generates consistent small returns to fund the long-vol sleeve
- It produces a continuous flow of execution data that informs the broader execution algos

---

## Cross-sleeve risk budget

```
                        Target  Max
Equity gross            120%    180%
Equity net (BIST beta)  ±30%    ±60%
FX gross                30%     60%
Rates DV01              $25k    $50k per bp
Vega (cross-asset)      $10k    $25k
Total VaR (99% 1d)      1.5%    3.0%
```

Hard limits enforced by the Risk Agent + a deterministic envelope check. Soft limits trigger Risk Agent escalation but don't auto-block.

---

## Strategy ↔ agent mapping

| Sleeve | Primary agent | Secondary agents |
|---|---|---|
| BIST L/S | Research, Quant | Macro, Risk, Adversarial |
| TR Macro | Macro | Quant (RV signals), Risk |
| Event-Driven | Event | Research, Compliance, Risk |
| Global EM | Research, Macro | Quant |
| Cross-asset Vol | Risk (drives sizing), Macro (drives timing) | Quant |
| Stat Arb | Quant (sole owner) | Risk envelope |

---

## What we explicitly do NOT do

- **No crypto** — outside circle of competence; Compliance posture would also be ugly.
- **No private equity / illiquid credit** — wrong vehicle structure.
- **No high-frequency trading** — wrong infrastructure (we're hours-to-days, not micros).
- **No Russia / sanctioned jurisdictions.**
- **No naked options short of size** — convexity is one-way; we are not gamma sellers.
- **No proprietary basket products / ETF wrappers in Year 1** — focus is the fund.

The discipline of saying no to adjacent opportunities is the most important strategy decision.
