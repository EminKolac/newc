# Infrastructure

## 1. Topology

```
                   ┌─────────────────────┐
                   │   Edge / API Gateway│
                   │   (Cloudflare + WAF)│
                   └──────────┬──────────┘
                              │
                ┌─────────────┴───────────────┐
                │                             │
        ┌───────▼────────┐           ┌────────▼────────┐
        │  Web dashboard │           │  Webhook ingest │
        │  (Next.js)     │           │  (KAP, SEC)     │
        └───────┬────────┘           └────────┬────────┘
                │                             │
                └──────────────┬──────────────┘
                               │
                  ┌────────────▼────────────┐
                  │   LangGraph Orchestrator│  (Python, FastAPI)
                  │   (k8s, 3 replicas)     │
                  └────────────┬────────────┘
                               │
        ┌───────────┬──────────┼──────────┬───────────┐
        │           │          │          │           │
   ┌────▼──────┐┌───▼─────┐┌───▼─────┐┌───▼─────┐┌────▼──────┐
   │ vLLM      ││ Postgres││ Qdrant  ││ Redis   ││ MCP        │
   │ Cluster   ││ (primary││ (vectors││ (cache, ││ Gateway    │
   │ (H200 x8) ││  + repl)││  + meta)││  pubsub)││ (Fintables,│
   │           ││         ││         ││         ││  Quartr,   │
   │           ││         ││         ││         ││  TCMB,...) │
   └───────────┘└─────────┘└─────────┘└─────────┘└────────────┘
                               │
                  ┌────────────▼────────────┐
                  │  Execution layer (OMS)  │
                  │  IBKR + TR Prime FIX    │
                  └─────────────────────────┘
```

---

## 2. Compute: vLLM on H200

**Cluster**: 8x NVIDIA H200 (141 GB HBM3e), shared via Architecht infra.

**Models served**:

| Model | Purpose | Slots | Notes |
|---|---|---|---|
| Qwen3-235B-A22B (FP8) | PM agent, complex synthesis | 1 (TP=8) | Largest model, called sparingly |
| Qwen2.5-72B + LoRA stack | All specialist agents | 4 (TP=2 each) | LoRA hot-swapped per agent |
| Qwen2.5-32B | Compliance Agent (deterministic, cheap) | 2 (TP=1) | High throughput |
| bge-m3 + e5-mistral-7b | Embeddings | 1 | CPU-fallback also available |
| bge-reranker-v2-m3 | RAG reranking | 1 | Small, batch-friendly |

**vLLM features used**:
- Paged attention (memory efficiency)
- Continuous batching
- LoRA hot-swap (specialist agents share base weights)
- Speculative decoding (Qwen2.5-72B with Qwen2.5-7B drafter)
- Prefix caching (system prompts are large + static)

**Why open-weight models**:
- Per-token economics: ~10x cheaper than frontier API calls at our volume
- No data egress to a third party (compliance + LP confidence)
- Fine-tuning latitude (LoRA per agent)
- Already familiar production stack

**Fallback to API**:
- If vLLM cluster has incident, agents auto-failover to Anthropic Claude (Opus 4.6 / Sonnet 4.6) via API
- Failover is observable; cost-aware throttling ensures we don't blow the budget on an extended outage
- This is also the dev environment default

---

## 3. State and storage

### Postgres (managed)

- LangGraph checkpoints (one row per node transition)
- Trade ledger
- LP records
- Audit log
- Restricted lists (versioned)
- Replicated synchronously to a second AZ; nightly backup to S3 + cross-region

### Qdrant (self-hosted)

- All RAG namespaces (see [`data-and-mcps.md`](data-and-mcps.md))
- 3-node cluster, replication factor 2
- Backed up to S3 nightly

### Redis

- Tool result cache (TTL per source: 5min for prices, 1d for fundamentals, infinite for filings)
- Pub/sub for real-time events (KAP webhook → agent runs)
- Rate limit counters (per-MCP)

### Object storage (S3-compatible)

- Raw filings, transcripts, scraped HTML
- Daily snapshots of all derived data
- Immutable audit trail (object lock enabled)

---

## 4. Observability

### Tracing

- **LangSmith** (or self-hosted Langfuse) for every agent run
- One trace = one `run_id`; every node, prompt, tool call, and retrieval is a span
- Searchable by ticker, intent, agent, outcome

### Metrics (Prometheus + Grafana)

Operational:
- Per-agent: p50/p95/p99 latency, error rate, tokens in/out, cost per run
- vLLM: GPU utilization, KV cache hit rate, TTFT, TPS
- MCPs: success rate, latency, rate-limit headroom
- Qdrant: query latency, recall@k

Business:
- Trades/day, gross/net exposure, P&L attribution
- Adversarial rejection rate
- Compliance block rate
- Limit-breach incidents (target: 0)

### Alerts (PagerDuty)

- Any kill-switch event → SEV-1
- Any limit breach → SEV-1
- Agent gold-set drift > 5% → SEV-2
- MCP outage > 10 min during market hours → SEV-2
- vLLM cluster unhealthy → SEV-2 (failover should kick in automatically)

### Daily artifacts (auto-generated, human-reviewed)

- 08:00: Macro brief + overnight watchlist (PDF, emailed)
- 17:00: EOD attribution + risk dashboard
- 22:00: Lessons-namespace digest (what was learned today)

The existing [`check_analyst_reports.sh`](../check_analyst_reports.sh) is the prototype for the daily-artifact email pipeline.

---

## 5. Deployment

- **Kubernetes** on a managed control plane (GKE or EKS)
- **GitOps** with ArgoCD: every config change is a PR, every PR has a diff, every deploy is auditable
- **CI** runs: lint, type-check (pyright strict), unit tests, integration tests against a sandbox MCP, eval suite on the gold set
- **CD** is gated: production deploys require Risk Officer + Engineering Lead double approval
- **Blue/green** for the orchestrator; **canary** for agent prompt/model changes (5% of runs to new version, compare outputs for 24h before promoting)

---

## 6. Security

- **Secrets**: HashiCorp Vault (or cloud KMS); no plaintext secrets in repo or env files
- **Network**: orchestrator runs in a private VPC; only the gateway is public; MCP gateway is the only egress path
- **Access**:
  - Engineering: read prod logs, deploy via ArgoCD, no direct DB access in prod
  - PM / Risk: dashboard + kill switch
  - Compliance: dashboard + audit trail read-only
  - Auditor (regulator): time-boxed read-only access to audit trail
- **Hardware MFA** for all production access
- **Penetration testing**: annual third-party assessment

---

## 7. Cost model (steady state, Year 2)

| Item | Monthly USD |
|---|---|
| GPU compute (amortized via Architecht) | $8,000 |
| Postgres (managed, multi-AZ) | $1,500 |
| Qdrant (3-node cluster, self-hosted on cloud VMs) | $1,200 |
| Redis (managed) | $400 |
| K8s control plane + workers (non-GPU) | $2,000 |
| Object storage + egress | $800 |
| LangSmith / observability | $1,000 |
| Cloudflare + WAF | $300 |
| **Total infra** | **~$15,200/mo (~$182k/yr)** |

The dominant Year-1 number is the team and the data, not the infra. By Year 2 the infra is small relative to AUM-scaled fees.

---

## 8. Disaster recovery

- **RPO** (recoverable to within): 5 minutes
- **RTO** (recovery time): 30 minutes for trading; 4 hours for full system
- **Cold standby region** with replicated Postgres + Qdrant snapshots
- **Manual trading playbook**: documented step-by-step on how to manage the open book by hand if the system is fully down for > 1 day. Every PM is expected to be able to execute this.
- **Quarterly DR drill** — fire the kill switch in production sandbox, fail over, recover, document.

---

## 9. Repo & code conventions

- **Python 3.12+**, `uv` for env management
- `pyright --strict`, `ruff`, `pytest` mandatory in CI
- Pydantic v2 for all inter-agent contracts
- LangGraph for orchestration
- Heavy reliance on `Annotated` types and TypedDict for state schemas
- No agent reads another agent's prose; only structured objects
- Every module has a `README.md` with purpose + ownership + on-call contact
