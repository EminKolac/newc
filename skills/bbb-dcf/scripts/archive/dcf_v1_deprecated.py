#!/usr/bin/env python3
"""
BBB DCF - Değerleme Aracı v4.0
İlker Başaran metodolojisine dayalı DCF hesaplama

v4.0 - Reel DCF Yaklaşımı (Fisher Düzeltmesi):
- IAS 29 reel finansallar + REEL WACC (Fisher denklemi)
- Reel WACC = (1 + Nominal WACC) / (1 + Enflasyon) - 1
- Bankalar: Earnings-based model (EBIT uygulanamaz)
- Her senaryoda cross-check ve uyarılar

Kullanım:
    python dcf.py THYAO
    python dcf.py THYAO --wacc 0.14 --inflation 0.09
    python dcf.py THYAO --output json
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple

try:
    import yfinance as yf
except ImportError:
    print("HATA: yfinance kütüphanesi gerekli. Kurulum: pip install yfinance")
    sys.exit(1)


# === WACC Tabloları ===

# Nominal WACC (sektör bazlı)
NOMINAL_WACC = {
    "Industrials": 0.14, "Financial Services": 0.13,
    "Consumer Cyclical": 0.15, "Consumer Defensive": 0.13,
    "Basic Materials": 0.14, "Energy": 0.13,
    "Technology": 0.16, "Communication Services": 0.15,
    "Real Estate": 0.14, "Utilities": 0.12, "Healthcare": 0.14,
    "default": 0.14
}

# Banka sektörü
FINANCIAL_SECTORS = {"Financial Services"}

# Varsayılanlar
DEFAULT_INFLATION = 0.09  # TÜFE tahmini %9
DEFAULT_TAX_RATE = 0.25
DEFAULT_PROJECTION_YEARS = 5
DEFAULT_SAFETY_MARGIN = 0.15


def nominal_to_real_wacc(nominal_wacc: float, inflation: float) -> float:
    """Fisher denklemi: Reel WACC = (1 + Nominal) / (1 + Enflasyon) - 1"""
    return (1 + nominal_wacc) / (1 + inflation) - 1


@dataclass
class DCFResult:
    ticker: str
    method: str  # "nominal", "real", "earnings"
    current_price: float
    target_price: float
    upside_percent: float
    valuation: str
    confidence: str
    fcff_history: List[float]
    projected_fcff: List[float]
    growth_rate_used: float
    wacc: float
    terminal_growth: float
    terminal_value: float
    enterprise_value: float
    equity_value: float
    net_debt: float
    shares_outstanding: float
    market_cap: float
    inflation_factor: float
    sensitivity: Dict[str, float]
    cross_check: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    disclaimer: str = "Bu analiz yatırım tavsiyesi değildir."


class DCFModel:
    """
    Hibrit DCF Modeli v3.0

    Otomatik olarak en uygun yöntemi seçer:
    1. Nominal: Enflasyon faktörü yüksek şirketler (havacılık vb.)
    2. Reel: IAS 29 düzeltilmiş finansallar tutarlı olan şirketler
    3. Earnings: Bankalar ve EBIT hesaplanamayan şirketler
    """

    def __init__(self, ticker: str, wacc: Optional[float] = None,
                 terminal_growth: Optional[float] = None,
                 projection_years: int = DEFAULT_PROJECTION_YEARS,
                 tax_rate: float = DEFAULT_TAX_RATE,
                 safety_margin: float = DEFAULT_SAFETY_MARGIN,
                 inflation: float = DEFAULT_INFLATION):
        self.ticker = ticker.upper()
        self.yf_ticker = f"{self.ticker}.IS" if not ticker.endswith(".IS") else ticker
        self.projection_years = projection_years
        self.tax_rate = tax_rate
        self.safety_margin = safety_margin
        self.inflation = inflation
        self._wacc_override = wacc  # Bu artık NOMINAL wacc override
        self._tg_override = terminal_growth
        self._warnings = []

        self.stock = yf.Ticker(self.yf_ticker)
        self.info = self.stock.info
        self.financials = self.stock.financials
        self.balance_sheet = self.stock.balance_sheet
        self.cashflow = self.stock.cashflow

        if self.financials is None or self.financials.empty:
            raise ValueError(f"{self.ticker} için finansal veri bulunamadı")

        # Enflasyon faktörünü tespit et
        self._inflation_factor = self._detect_inflation_factor()

        # Yöntemi belirle
        self._method = self._select_method()

    # === Veri Erişimi ===

    @property
    def sector(self) -> str:
        return self.info.get("sector", "default")

    @property
    def current_price(self) -> float:
        return self.info.get("currentPrice",
               self.info.get("regularMarketPrice",
               self.info.get("previousClose", 0)))

    @property
    def market_cap_m(self) -> float:
        return (self.info.get("marketCap", 0) or 0) / 1_000_000

    @property
    def shares_m(self) -> float:
        return (self.info.get("sharesOutstanding", 0) or 0) / 1_000_000

    @property
    def net_debt_m(self) -> float:
        debt = self.info.get("totalDebt", 0) or 0
        cash = self.info.get("totalCash", 0) or 0
        return (debt - cash) / 1_000_000

    @property
    def nominal_wacc(self) -> float:
        """Nominal WACC (sektör tablosundan veya override)"""
        if self._wacc_override:
            return self._wacc_override
        return NOMINAL_WACC.get(self.sector, NOMINAL_WACC["default"])

    @property
    def wacc(self) -> float:
        """Reel WACC = Fisher(Nominal WACC, Enflasyon)"""
        return nominal_to_real_wacc(self.nominal_wacc, self.inflation)

    @property
    def terminal_growth(self) -> float:
        if self._tg_override is not None:
            return self._tg_override
        # Reel terminal büyüme: %1-2 (gelişmiş piyasa reel büyümesi)
        return 0.02

    def _get(self, df, names, col):
        if isinstance(names, str):
            names = [names]
        for n in names:
            if n in df.index:
                v = df.loc[n, col]
                if v is not None and str(v) != 'nan':
                    return float(v)
        return 0.0

    # === Enflasyon ve Yöntem Tespiti ===

    def _detect_inflation_factor(self) -> float:
        eps = self.info.get("trailingEps", 0) or 0
        shares = self.info.get("sharesOutstanding", 0) or 0
        if not eps or not shares:
            return 1.0

        nominal_ni = eps * shares
        try:
            col = self.financials.columns[0]
            real_ni = self._get(self.financials,
                ["Net Income", "Net Income Common Stockholders"], col)
            if real_ni and abs(real_ni) > 0 and nominal_ni > 0:
                return nominal_ni / real_ni
        except:
            pass
        return 1.0

    def _select_method(self) -> str:
        """Otomatik yöntem seçimi"""
        if self.sector in FINANCIAL_SECTORS:
            self._warnings.append("Banka sektörü: Earnings-based model kullanılıyor")
            return "earnings"

        f = self._inflation_factor
        self._warnings.append(
            f"IAS 29 reel tablolar + Reel WACC (Fisher). "
            f"Enfl. faktörü: {f:.1f}x, Nominal WACC: %{self.nominal_wacc*100:.1f}, "
            f"Enflasyon: %{self.inflation*100:.0f}, Reel WACC: %{self.wacc*100:.1f}"
        )
        return "real"

    # === FCFF Hesaplama ===

    def _calc_fcff_real(self) -> List[float]:
        """Reel FCFF (finansal tablolardan)"""
        result = []
        try:
            for i in range(min(4, len(self.financials.columns))):
                col = self.financials.columns[i]
                ebit = self._get(self.financials, ["EBIT", "Operating Income"], col)
                if ebit == 0:
                    continue
                da = abs(self._get(self.cashflow,
                    ["Depreciation And Amortization", "Depreciation"], col))
                capex = abs(self._get(self.cashflow, ["Capital Expenditure"], col))
                fcff = ebit * (1 - self.tax_rate) + da - capex
                result.append(fcff / 1_000_000)
            result.reverse()
        except Exception as e:
            self._warnings.append(f"FCFF hatası: {e}")
        return result if result else [100]

    def _get_nominal_earnings(self) -> float:
        """Nominal net gelir (EPS bazlı) - Milyon TL"""
        eps = self.info.get("trailingEps", 0) or 0
        shares = self.info.get("sharesOutstanding", 0) or 0
        return (eps * shares) / 1_000_000 if eps and shares else 0

    # === Projeksiyon ===

    def _growth_rate(self) -> float:
        """Muhafazakar büyüme oranı"""
        sources = []
        eg = self.info.get("earningsGrowth")
        rg = self.info.get("revenueGrowth")
        if eg and str(eg) != 'nan':
            sources.append(float(eg))
        if rg and str(rg) != 'nan':
            sources.append(float(rg))

        if sources:
            avg = sum(sources) / len(sources)
            return max(-0.10, min(0.20, avg * 0.7))  # %30 haircut

        self._warnings.append("Büyüme verisi yok, %5 varsayıldı")
        return 0.05

    def _project(self, base: float, growth: float) -> List[float]:
        """FCFF projeksiyonu - büyümeyi terminale yakınlaştır"""
        result = []
        for y in range(1, self.projection_years + 1):
            fade = y / self.projection_years * 0.5
            yg = growth + (self.terminal_growth - growth) * fade
            result.append(round(base * ((1 + yg) ** y), 2))
        return result

    # === Değerleme Hesaplama ===

    def _tv(self, last_fcff: float, wacc: float = None) -> float:
        w = wacc or self.wacc
        g = self.terminal_growth
        if w <= g:
            return last_fcff * 10
        return last_fcff * (1 + g) / (w - g)

    def _ev(self, projected: List[float], tv: float, wacc: float = None) -> float:
        w = wacc or self.wacc
        ev = sum(f / ((1 + w) ** (i+1)) for i, f in enumerate(projected))
        ev += tv / ((1 + w) ** len(projected))
        return ev

    def _sensitivity(self, projected: List[float], net_debt: float) -> Dict:
        sens = {}
        for adj in [-0.04, -0.02, 0, 0.02, 0.04]:
            w = self.wacc + adj
            if w <= self.terminal_growth:
                continue
            tv = self._tv(projected[-1], wacc=w)
            ev = self._ev(projected, tv, wacc=w)
            eq = ev - net_debt
            price = (eq / self.shares_m * (1 - self.safety_margin)) if self.shares_m > 0 else 0
            sens[f"wacc_{int(w*100)}"] = round(price, 2)
        return sens

    def _cross_check(self) -> Dict:
        checks = {}
        try:
            col = self.cashflow.columns[0]
            fcf = self._get(self.cashflow, ["Free Cash Flow"], col)
            if fcf:
                checks["yahoo_fcf_m"] = round(fcf / 1_000_000, 0)
                if self.market_cap_m > 0:
                    checks["p_fcf"] = round(self.market_cap_m / (fcf / 1_000_000), 1)
        except:
            pass
        for k in ["trailingPE", "forwardPE", "priceToBook", "enterpriseToEbitda"]:
            v = self.info.get(k)
            if v and str(v) != 'nan':
                checks[k] = round(float(v), 2)
        return checks

    # === Ana Hesaplama ===

    def calculate(self) -> DCFResult:
        method = self._method
        growth = self._growth_rate()
        net_debt = self.net_debt_m

        if method == "real":
            # Reel FCFF direkt kullan, reel WACC ile (Fisher)
            real_fcff = self._calc_fcff_real()
            base = real_fcff[-1] if real_fcff[-1] > 0 else max(real_fcff)
            projected = self._project(base, growth)
            fcff_display = [round(f, 0) for f in real_fcff]

        else:  # earnings
            # Nominal earnings bazlı
            nom_ni = self._get_nominal_earnings()
            if nom_ni <= 0:
                # Fallback: reel
                real_fcff = self._calc_fcff_real()
                nom_ni = real_fcff[-1] if real_fcff else 100
                fcff_display = [round(f, 0) for f in real_fcff]
            else:
                fcff_display = [round(nom_ni, 0)]
            projected = self._project(nom_ni, growth)

        tv = self._tv(projected[-1])
        ev = self._ev(projected, tv)
        equity = ev - net_debt

        price = equity / self.shares_m if self.shares_m > 0 else 0
        target = price * (1 - self.safety_margin)

        upside = ((target - self.current_price) / self.current_price * 100
                  if self.current_price > 0 else 0)

        if upside > 30:
            val, conf = "Çok Ucuz", "Yüksek"
        elif upside > 15:
            val, conf = "Ucuz", "Orta-Yüksek"
        elif upside > 0:
            val, conf = "Makul", "Orta"
        elif upside > -15:
            val, conf = "Pahalı", "Düşük"
        else:
            val, conf = "Çok Pahalı", "Çok Düşük"

        return DCFResult(
            ticker=self.ticker,
            method=method,
            current_price=round(self.current_price, 2),
            target_price=round(target, 2),
            upside_percent=round(upside, 1),
            valuation=val,
            confidence=conf,
            fcff_history=fcff_display,
            projected_fcff=projected,
            growth_rate_used=round(growth, 4),
            wacc=self.wacc,
            terminal_growth=self.terminal_growth,
            terminal_value=round(tv, 0),
            enterprise_value=round(ev, 0),
            equity_value=round(equity, 0),
            net_debt=round(net_debt, 0),
            shares_outstanding=round(self.shares_m, 2),
            market_cap=round(self.market_cap_m, 0),
            inflation_factor=round(self._inflation_factor, 1),
            sensitivity=self._sensitivity(projected, net_debt),
            cross_check=self._cross_check(),
            warnings=self._warnings
        )


def format_result(result: DCFResult, fmt: str = "text") -> str:
    if fmt == "json":
        return json.dumps(result.__dict__, indent=2, ensure_ascii=False)

    method_label = {"real": "Reel (IAS 29 + Fisher WACC)",
                    "earnings": "Earnings-Based (Fisher WACC)"}

    lines = [
        f"\n{'='*55}",
        f"📊 DCF DEĞERLEMESİ: {result.ticker}",
        f"   Yöntem: {method_label.get(result.method, result.method)}",
        f"{'='*55}",
        f"",
        f"💰 Güncel Fiyat:      {result.current_price:>12,.2f} TL",
        f"🎯 Hedef Fiyat:       {result.target_price:>12,.2f} TL",
        f"📈 Potansiyel:        {result.upside_percent:>+11.1f}%",
        f"",
        f"📋 Değerleme:         {result.valuation}",
        f"🔒 Güven:             {result.confidence}",
        f"",
        f"{'─'*55}",
        f"📊 FCFF GEÇMİŞİ (M TL)",
        f"{'─'*55}",
    ]
    for i, f in enumerate(result.fcff_history):
        lines.append(f"  Yıl {i+1}: {f:>15,.0f} M TL")
    lines.extend([
        f"",
        f"{'─'*55}",
        f"📊 PROJEKSİYON (M TL)",
        f"{'─'*55}",
    ])
    for i, f in enumerate(result.projected_fcff, 1):
        lines.append(f"  +{i}Y: {f:>15,.0f} M TL")

    lines.extend([
        f"",
        f"{'─'*55}",
        f"📊 PARAMETRELER",
        f"{'─'*55}",
        f"  WACC:               {result.wacc*100:.1f}%",
        f"  Terminal Büyüme:    {result.terminal_growth*100:.1f}%",
        f"  Büyüme Oranı:      {result.growth_rate_used*100:+.1f}%",
        f"  Güvenlik Marjı:     {DEFAULT_SAFETY_MARGIN*100:.0f}%",
        f"  Enflasyon Faktörü:  {result.inflation_factor:.1f}x",
        f"",
        f"  Terminal Value:     {result.terminal_value:>15,.0f} M TL",
        f"  Enterprise Value:   {result.enterprise_value:>15,.0f} M TL",
        f"  Net Borç:           {result.net_debt:>15,.0f} M TL",
        f"  Equity Value:       {result.equity_value:>15,.0f} M TL",
        f"  Hisse Sayısı:       {result.shares_outstanding:>12,.0f} M",
        f"  Piyasa Değeri:      {result.market_cap:>15,.0f} M TL",
        f"",
        f"{'─'*55}",
        f"📉 HASSASİYET",
        f"{'─'*55}",
    ])
    for k, v in sorted(result.sensitivity.items()):
        pct = k.replace("wacc_", "")
        lines.append(f"  WACC %{pct}:       {v:>12,.2f} TL")

    if result.cross_check:
        lines.extend([f"", f"{'─'*55}", f"🔍 CROSS-CHECK", f"{'─'*55}"])
        labels = {"yahoo_fcf_m": "Yahoo FCF (M)", "p_fcf": "P/FCF",
                  "trailingPE": "F/K (trailing)", "forwardPE": "F/K (forward)",
                  "priceToBook": "PD/DD", "enterpriseToEbitda": "FD/FAVÖK"}
        for k, v in result.cross_check.items():
            lines.append(f"  {labels.get(k,k):<22}{v:>12,.2f}")

    if result.warnings:
        lines.extend([f"", f"{'─'*55}", f"⚠️  UYARILAR", f"{'─'*55}"])
        for w in result.warnings:
            lines.append(f"  • {w}")

    lines.extend([f"", f"{'─'*55}", f"⚠️  {result.disclaimer}", f"{'='*55}"])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="BBB DCF v3.0")
    parser.add_argument("ticker", help="Hisse kodu (örn: THYAO)")
    parser.add_argument("--wacc", type=float, help="Nominal WACC override")
    parser.add_argument("--inflation", type=float, default=DEFAULT_INFLATION, help="Enflasyon oranı (varsayılan: 0.09)")
    parser.add_argument("--growth", type=float, help="Terminal büyüme override")
    parser.add_argument("--years", type=int, default=5)
    parser.add_argument("--margin", type=float, default=DEFAULT_SAFETY_MARGIN)
    parser.add_argument("--output", choices=["text", "json"], default="text")

    args = parser.parse_args()

    try:
        model = DCFModel(
            ticker=args.ticker, wacc=args.wacc,
            terminal_growth=args.growth,
            projection_years=args.years,
            safety_margin=args.margin,
            inflation=args.inflation
        )
        result = model.calculate()
        print(format_result(result, args.output))
    except Exception as e:
        print(f"HATA: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
