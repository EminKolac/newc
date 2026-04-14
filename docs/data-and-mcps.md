# Data Sources, MCPs, and the RAG Corpus

The fund's edge is in the integration of three data layers:
1. **Real-time market and filings data** (via MCPs)
2. **A curated, domain-grounded RAG corpus** (CFA / CAIA / FRM / CQF + filings + transcripts)
3. **Episodic memory of the fund's own decisions** (the "lessons" namespace)

---

## 1. MCP plugins (real-time, structured)

Each MCP is wrapped as a LangGraph tool node with a typed Pydantic interface, retry logic, and result caching.

| MCP | Coverage | Used by | Refresh |
|---|---|---|---|
| **Fintables** | BIST equities: prices, fundamentals, analyst reports, KAP filings, TR macro | Research, Quant, Event, Macro, Compliance | tick / EOD |
| **Quartr** | Earnings call transcripts, IR materials (global) | Research, Event | Same-day post-call |
| **TCMB EVDS** | TR macro time series — rates, FX reserves, monetary aggregates, BoP | Macro | Daily |
| **Bigdata.com** | Global structured + unstructured financial data | Macro, Event, Research | Continuous |
| **Refinitiv / LSEG** | Global equity, FX, rates, derivatives (Year 2+ subscription) | All | Tick / EOD |
| **Apify** | Web scraping for TR financial press, regulator websites, broker reports not on Fintables | Macro, Event | Per-target schedule |
| **KAP webhook** | Material disclosure stream, BIST | Event (primary), Compliance | Push, sub-5-min |
| **SEC EDGAR** | 10-K, 10-Q, 8-K, 13F (US names) | Research, Event | Push on filing |
| **IBKR API** | Order entry, positions, balances, executions | OMS layer | Real-time |

> **Branding note:** when surfacing data from the Bigdata.com MCP in any LP-facing output, always use the exact branding "Bigdata.com" and link to https://bigdata.com.

### MCP wrapper pattern

```python
class FintablesTool(BaseTool):
    name = "fintables.veri_sorgula"
    description = "Read-only SQL over BIST data warehouse"
    args_schema = VeriSorgulaArgs

    def _run(self, sql: str) -> ToolResult:
        # 1. validate SQL is read-only (rejects DML)
        # 2. apply timeout + row cap
        # 3. tag result with data_as_of_utc
        # 4. cache (5-min TTL for prices, 1-day for fundamentals)
        # 5. return as ToolResult with source_id
```

Every tool result is wrapped in `ToolResult` carrying `source_id`, `data_as_of_utc`, and a `provenance` chain. Downstream agents are required to cite `source_id`s.

---

## 2. RAG Corpus

### Namespaces

| Namespace | Source | Approx chunk count | Refresh |
|---|---|---|---|
| `cfa_l1_fsa` | CFA L1 Financial Statement Analysis | 8k | Annual (curriculum cycle) |
| `cfa_l2_equity` | CFA L2 Equity readings | 12k | Annual |
| `cfa_l2_fixed_income` | CFA L2 Fixed Income | 9k | Annual |
| `cfa_l3_pm` | CFA L3 Portfolio Management & Asset Allocation | 14k | Annual |
| `cfa_econ` | CFA Economics readings (L1+L2) | 6k | Annual |
| `caia_l1` | CAIA L1 (asset class survey) | 7k | Annual |
| `caia_l2_event` | CAIA L2 event-driven sections | 4k | Annual |
| `frm_p1` | FRM Part I (foundations, quant, fin markets, val) | 11k | Annual |
| `frm_p2` | FRM Part II (market, credit, op, inv, current issues) | 13k | Annual |
| `cqf` | CQF curriculum + lab notebooks | 15k | Per-cohort release |
| `kap_filings` | KAP material disclosures (rolling 5y) | 200k+ | Daily |
| `kap_corporate_actions` | M&A, capital changes, governance | 30k | Daily |
| `sec_8k` | SEC 8-K filings (US names in universe) | 50k | On filing |
| `sec_10k_10q` | Annual + quarterly reports | 80k | On filing |
| `earnings_transcripts` | Quartr global, BIST-100 priority | 100k+ | Same-day post-call |
| `tcmb_publications` | CBRT inflation reports, financial stability, minutes | 5k | Per-publication |
| `central_bank_minutes` | Fed, ECB, BoE, BoJ, ECB minutes | 3k | Per-meeting |
| `imf_weo` | IMF World Economic Outlook chapters | 1k | Semi-annual |
| `factor_research_papers` | SSRN selected, AQR / Asness / French canon | 5k | Curated quarterly |
| `behavioral_finance` | Kahneman, Thaler, Montier excerpts (licensed) | 2k | Static |
| `blowup_case_studies` | LTCM, Archegos, Melvin, Bill Hwang, Quant Quake 2007, March 2020 | 1k | Static + as-they-happen |
| `short_seller_reports` | Muddy Waters, Hindenburg, Citron public reports | 3k | On publication |
| `spk_regulations` | SPK rule book + opinions | 4k | Per amendment |
| `sec_rules` | Selected SEC rules (Reg M, Rule 105, 13D/G, 13F) | 2k | Per amendment |
| `mar` | EU Market Abuse Regulation | 1k | Static |
| `argus_internal_policy` | Internal compliance manual, restricted lists | 0.5k | Per change |
| `historical_deals` | M&A database, 20y of deal characteristics + outcomes | 50k | Quarterly refresh |
| `lessons` | **Auto-distilled from fund's own decisions** | growing | Nightly |

### Chunking strategy

- **Curriculum content:** semantic chunking on section + subsection boundaries; 800-1200 tokens per chunk; metadata `{source, l1/l2/l3, topic, subtopic, page}`.
- **Filings:** structural chunking on XBRL tag + section header (Item 1, Risk Factors, MD&A, etc.); metadata `{ticker, filing_type, period, item, ts}`.
- **Transcripts:** speaker-aware chunking; metadata `{ticker, call_type, quarter, speaker_role, ts}`.
- **News:** event-based (one chunk per article + one per material entity-event extracted by NER pre-processor).

### Retrieval

- **Hybrid search**: BM25 (sparse) + dense embeddings (bge-m3 + e5-mistral-7b ensemble averaged at score level).
- **Reranker**: bge-reranker-v2-m3 on top-50 → top-10.
- **Filtering**: every query carries metadata filters (ticker, date range, source whitelist).
- **Multilingual**: TR queries match TR + EN chunks; EN queries match EN chunks. Cross-language reranking handled by the multilingual reranker.

### Anti-poisoning

- Every ingested chunk is signed (sha256 over content + source URL + timestamp).
- Source allow-list per namespace (only KAP, only SEC, only the licensed CFA package, etc.).
- Periodic integrity audit: re-embed a 1% sample and compare to stored embeddings.

---

## 3. Episodic memory → "lessons"

The most distinctive component. Nightly batch:

1. Pull all completed runs from the prior 24h with materialized P&L (or marked-to-market for unrealized).
2. Identify outlier outcomes — top decile winners and bottom decile losers by PnL impact.
3. For each, run a "lessons agent" (separate from the trading agents) that produces a structured `Lesson`:
   - The original thesis
   - What actually happened
   - Which assumptions held / broke
   - What signal would have predicted the outcome earlier
   - A 1-paragraph "lesson" indexed for future retrieval
4. Index into the `lessons` Qdrant namespace.

Future agent runs retrieve from `lessons` automatically. This is how the system improves without retraining the base models.

### Anti-overfitting on lessons

- A lesson must appear in ≥ 3 distinct outcomes to gain weight.
- Lessons are decay-weighted (older lessons matter less unless reinforced).
- A lesson cannot contradict a deterministic rule (you can't "learn your way around" a hard limit).

---

## 4. Data acquisition cost (steady state, Year 2)

| Source | Annual cost (USD) |
|---|---|
| Fintables (enterprise) | $30k |
| Quartr | $20k |
| TCMB EVDS | $0 (public) |
| Bigdata.com | $40k |
| Refinitiv Eikon (2 seats) | $50k |
| Apify (managed scraping) | $15k |
| KAP webhook (custom) | $5k infra |
| SEC EDGAR | $0 (public) |
| IBKR | per-execution |
| Bloomberg Terminal (1 seat, PM only) | $30k |
| **Total** | **~$190k** |

This is the largest single OpEx line after personnel. It is also the most defensible — every dollar here is ammunition the agents use directly.

---

## 5. Data lineage as a first-class concern

Every number in every LP report can be traced — through the PM memo → through the agent reasoning → through the tool call → through the MCP response → to the source row in Fintables/SEC/KAP, with timestamps at every hop.

This is a non-negotiable design property. It is the difference between an AI fund regulators trust and one they shut down.
