"""FundState — the canonical run state for the Argus LangGraph orchestrator.

Every node in the graph reads from and writes to this object. It is checkpointed
into Postgres after every node transition, making any run fully replayable.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

# ----- primitives ----------------------------------------------------------

Ticker = str  # e.g. "THYAO.IS", "AAPL"
SourceID = str  # opaque ID into the data lineage graph


class ToolCall(BaseModel):
    name: str
    args: dict
    result_summary: str
    source_id: SourceID
    data_as_of_utc: datetime
    latency_ms: int


class RetrievedChunk(BaseModel):
    namespace: str
    chunk_id: str
    text: str
    score: float
    metadata: dict


class MarketSnapshot(BaseModel):
    """Frozen at run-start so all agents see the same market."""
    timestamp_utc: datetime
    prices: dict[Ticker, float]
    fx: dict[str, float]  # e.g. {"USDTRY": 32.85}
    rates: dict[str, float]  # e.g. {"TR_2Y": 0.4250}


# ----- agent output schemas ------------------------------------------------

class Catalyst(BaseModel):
    description: str
    expected_date: Optional[datetime] = None
    probability: float = Field(ge=0.0, le=1.0)


class Risk(BaseModel):
    description: str
    severity: Literal["low", "medium", "high"]
    mitigation: Optional[str] = None


class ResearchThesis(BaseModel):
    ticker: Ticker
    direction: Literal["long", "short"]
    conviction: float = Field(ge=0.0, le=1.0)
    horizon_days: int
    target_price: float
    target_price_methodology: Literal["DCF", "comps", "SOTP", "other"]
    catalysts: list[Catalyst]
    key_risks: list[Risk]
    citations: list[SourceID] = Field(min_length=3)
    confidence_intervals: dict


class QuantSignal(BaseModel):
    ticker: Ticker
    composite_score: float  # standardized
    factor_scores: dict[str, float]  # value/quality/momentum/...
    backtest_sharpe_oos: float
    backtest_max_dd_oos: float
    proposed_size_bps: float
    dominant_factor: str
    citations: list[SourceID]


class MacroBrief(BaseModel):
    timestamp_utc: datetime
    overnight_global: str
    tr_specific: str
    rates_curves: str
    commodities_fx: str
    view_diff: str
    citations: list[SourceID]


class EventReport(BaseModel):
    ticker: Ticker
    event_type: Literal["M&A", "spinoff", "secondary", "rights", "index_change", "governance"]
    summary: str
    expected_value_bps: float
    completion_probability: float = Field(ge=0.0, le=1.0)
    regulatory_risk_score: float = Field(ge=0.0, le=1.0)
    citations: list[SourceID]


class StressScenario(BaseModel):
    name: str
    description: str
    portfolio_pnl_bps: float


class RiskAssessment(BaseModel):
    var_95_1d_bps: float
    var_99_1d_bps: float
    expected_shortfall_99_1d_bps: float
    factor_exposures: dict[str, float]
    liquidity_score: float = Field(ge=0.0, le=1.0)
    correlation_regime: str
    stress_scenarios: list[StressScenario]
    envelope_breach: bool
    breach_details: list[str] = Field(default_factory=list)


class RedTeamReport(BaseModel):
    bear_case: str
    implicit_assumptions: list[str]
    historical_precedents: list[str]
    blowup_risk_score: int = Field(ge=1, le=10)
    falsifying_observation: str
    rejection_recommended: bool


class ComplianceVerdict(BaseModel):
    verdict: Literal["pass", "pass_with_conditions", "block"]
    reasoning: str
    conditions: list[str] = Field(default_factory=list)
    rule_citations: list[str]
    deterministic_check_passed: bool


class TradeRecommendation(BaseModel):
    ticker: Ticker
    direction: Literal["long", "short"]
    size_bps: float
    entry_method: Literal["market", "limit", "vwap", "twap"]
    entry_price_limit: Optional[float] = None
    stop_loss_pct: Optional[float] = None
    take_profit_pct: Optional[float] = None
    horizon_days: int
    addressed_redteam_objections: list[str]
    memo_markdown: str


# ----- top-level state -----------------------------------------------------

class Intent(str, Enum):
    IDEA = "idea"
    EVENT = "event"
    RISK = "risk"
    MACRO = "macro"
    REBAL = "rebal"
    TRADE_REVIEW = "trade-review"


class FundState(BaseModel):
    """The single source of truth flowing through the LangGraph."""

    # identifiers
    run_id: UUID
    parent_run_id: Optional[UUID] = None
    triggered_by: Literal["cron", "webhook", "human", "agent"]
    timestamp_utc: datetime

    # input
    intent: Intent
    payload: dict

    # working memory
    universe: list[Ticker] = Field(default_factory=list)
    retrieved_context: list[RetrievedChunk] = Field(default_factory=list)
    market_snapshot: Optional[MarketSnapshot] = None

    # agent outputs
    research: Optional[ResearchThesis] = None
    quant: Optional[QuantSignal] = None
    macro: Optional[MacroBrief] = None
    event: Optional[EventReport] = None
    risk: Optional[RiskAssessment] = None
    adversarial: Optional[RedTeamReport] = None
    compliance: Optional[ComplianceVerdict] = None

    # decision
    pm_recommendation: Optional[TradeRecommendation] = None
    final_decision: Optional[Literal["execute", "reject", "escalate"]] = None

    # audit
    prompt_hashes: dict[str, str] = Field(default_factory=dict)
    model_versions: dict[str, str] = Field(default_factory=dict)
    tool_calls: list[ToolCall] = Field(default_factory=list)
