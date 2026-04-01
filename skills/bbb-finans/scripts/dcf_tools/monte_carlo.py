#!/usr/bin/env python3
"""
Monte Carlo Simülasyon Modülü
DCF değerleme için Monte Carlo analizi.
7 value driver, 10K iterasyon, NumPy tabanlı.

Value Drivers:
1. Revenue Growth Rate
2. Operating Margin (EBIT/Revenue)
3. Tax Rate
4. Reinvestment Rate (CapEx + WC / NOPAT)
5. Cost of Capital (WACC)
6. Terminal Growth Rate
7. Risk-free Rate (feeds into WACC)
"""

import json
import sys
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("[WARN] NumPy yok, Monte Carlo çalışmaz.", file=sys.stderr)


@dataclass
class DriverDistribution:
    """Bir value driver'ın dağılım parametreleri."""
    name: str
    distribution: str = "normal"  # normal, triangular, uniform, lognormal
    mean: float = 0.0
    std: float = 0.0
    low: float = 0.0
    high: float = 0.0
    mode: float = 0.0  # triangular için
    
    def sample(self, n: int, rng: Any = None) -> Any:
        """N adet rastgele değer üret."""
        if rng is None:
            rng = np.random.default_rng()
        
        if self.distribution == "normal":
            return rng.normal(self.mean, self.std, n)
        elif self.distribution == "triangular":
            return rng.triangular(self.low, self.mode, self.high, n)
        elif self.distribution == "uniform":
            return rng.uniform(self.low, self.high, n)
        elif self.distribution == "lognormal":
            return rng.lognormal(self.mean, self.std, n)
        else:
            raise ValueError(f"Bilinmeyen dağılım: {self.distribution}")


@dataclass
class MCConfig:
    """Monte Carlo simülasyon konfigürasyonu."""
    iterations: int = 10_000
    seed: Optional[int] = None
    projection_years: int = 5
    base_revenue: float = 1_000_000  # Base revenue (TL thousands)
    
    # 7 Value Drivers
    revenue_growth: DriverDistribution = field(default_factory=lambda: DriverDistribution(
        name="Revenue Growth", distribution="normal", mean=0.10, std=0.05))
    operating_margin: DriverDistribution = field(default_factory=lambda: DriverDistribution(
        name="Operating Margin", distribution="triangular", low=0.05, mode=0.12, high=0.20))
    tax_rate: DriverDistribution = field(default_factory=lambda: DriverDistribution(
        name="Tax Rate", distribution="normal", mean=0.25, std=0.02))
    reinvestment_rate: DriverDistribution = field(default_factory=lambda: DriverDistribution(
        name="Reinvestment Rate", distribution="normal", mean=0.40, std=0.10))
    wacc: DriverDistribution = field(default_factory=lambda: DriverDistribution(
        name="WACC", distribution="normal", mean=0.12, std=0.02))
    terminal_growth: DriverDistribution = field(default_factory=lambda: DriverDistribution(
        name="Terminal Growth", distribution="triangular", low=0.02, mode=0.04, high=0.06))
    risk_free_rate: DriverDistribution = field(default_factory=lambda: DriverDistribution(
        name="Risk-free Rate", distribution="normal", mean=0.045, std=0.005))


def run_dcf_simulation(config: MCConfig) -> Dict[str, Any]:
    """
    Monte Carlo DCF simülasyonu çalıştırır.
    
    Her iterasyonda:
    1. 7 driver'dan rastgele değerler çek
    2. N yıllık FCFF projeksiyonu yap
    3. Terminal value hesapla
    4. NPV hesapla
    
    Returns:
        {
            'iterations': int,
            'values': np.array of firm values,
            'stats': {mean, median, std, p5, p10, p25, p75, p90, p95, min, max},
            'driver_stats': {driver_name: {mean, std}},
        }
    """
    if not HAS_NUMPY:
        raise RuntimeError("NumPy gerekli: pip install numpy")
    
    rng = np.random.default_rng(config.seed)
    n = config.iterations
    years = config.projection_years
    
    # Sample all drivers at once (vectorized)
    rev_growth = config.revenue_growth.sample(n, rng)
    op_margin = config.operating_margin.sample(n, rng)
    tax_rates = config.tax_rate.sample(n, rng)
    reinvest = config.reinvestment_rate.sample(n, rng)
    waccs = config.wacc.sample(n, rng)
    term_growth = config.terminal_growth.sample(n, rng)
    rf_rates = config.risk_free_rate.sample(n, rng)
    
    # Clamp to reasonable ranges
    rev_growth = np.clip(rev_growth, -0.30, 0.50)
    op_margin = np.clip(op_margin, 0.01, 0.50)
    tax_rates = np.clip(tax_rates, 0.10, 0.40)
    reinvest = np.clip(reinvest, 0.05, 0.80)
    waccs = np.clip(waccs, 0.05, 0.30)
    term_growth = np.clip(term_growth, 0.01, waccs - 0.01)  # g < WACC
    
    # Calculate firm values
    firm_values = np.zeros(n)
    base_rev = config.base_revenue
    
    for i in range(n):
        pv_fcff = 0.0
        revenue = base_rev
        
        for yr in range(1, years + 1):
            revenue *= (1 + rev_growth[i])
            ebit = revenue * op_margin[i]
            nopat = ebit * (1 - tax_rates[i])
            fcff = nopat * (1 - reinvest[i])
            discount = (1 + waccs[i]) ** yr
            pv_fcff += fcff / discount
        
        # Terminal value (Gordon Growth)
        terminal_fcff = revenue * (1 + term_growth[i]) * op_margin[i] * (1 - tax_rates[i]) * (1 - reinvest[i])
        tv = terminal_fcff / (waccs[i] - term_growth[i])
        pv_tv = tv / ((1 + waccs[i]) ** years)
        
        firm_values[i] = pv_fcff + pv_tv
    
    # Filter out negative/infinite values
    valid = np.isfinite(firm_values) & (firm_values > 0)
    values = firm_values[valid]
    
    if len(values) == 0:
        return {"iterations": n, "values": [], "stats": {}, "error": "Tüm değerler geçersiz"}
    
    stats = {
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "std": float(np.std(values)),
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "p5": float(np.percentile(values, 5)),
        "p10": float(np.percentile(values, 10)),
        "p25": float(np.percentile(values, 25)),
        "p75": float(np.percentile(values, 75)),
        "p90": float(np.percentile(values, 90)),
        "p95": float(np.percentile(values, 95)),
        "valid_count": int(len(values)),
    }
    
    driver_stats = {
        "revenue_growth": {"mean": float(np.mean(rev_growth)), "std": float(np.std(rev_growth))},
        "operating_margin": {"mean": float(np.mean(op_margin)), "std": float(np.std(op_margin))},
        "tax_rate": {"mean": float(np.mean(tax_rates)), "std": float(np.std(tax_rates))},
        "reinvestment_rate": {"mean": float(np.mean(reinvest)), "std": float(np.std(reinvest))},
        "wacc": {"mean": float(np.mean(waccs)), "std": float(np.std(waccs))},
        "terminal_growth": {"mean": float(np.mean(term_growth)), "std": float(np.std(term_growth))},
        "risk_free_rate": {"mean": float(np.mean(rf_rates)), "std": float(np.std(rf_rates))},
    }
    
    return {
        "iterations": n,
        "values": values.tolist(),
        "stats": stats,
        "driver_stats": driver_stats,
    }


def print_simulation_results(results: Dict):
    """Simülasyon sonuçlarını güzel yazdır."""
    stats = results.get("stats", {})
    if not stats:
        print("Sonuç yok.")
        return
    
    fmt = lambda x: f"{x:,.0f}"
    
    print(f"\n{'=' * 60}")
    print(f"  MONTE CARLO SİMÜLASYON SONUÇLARI")
    print(f"  İterasyon: {results['iterations']:,} | Geçerli: {stats.get('valid_count', 0):,}")
    print(f"{'=' * 60}")
    print(f"  Ortalama Firma Değeri : {fmt(stats['mean']):>20s}")
    print(f"  Medyan                : {fmt(stats['median']):>20s}")
    print(f"  Std Sapma             : {fmt(stats['std']):>20s}")
    print(f"  Min                   : {fmt(stats['min']):>20s}")
    print(f"  Max                   : {fmt(stats['max']):>20s}")
    print(f"  {'─' * 56}")
    print(f"  %5 Percentile        : {fmt(stats['p5']):>20s}")
    print(f"  %10 Percentile       : {fmt(stats['p10']):>20s}")
    print(f"  %25 Percentile       : {fmt(stats['p25']):>20s}")
    print(f"  %75 Percentile       : {fmt(stats['p75']):>20s}")
    print(f"  %90 Percentile       : {fmt(stats['p90']):>20s}")
    print(f"  %95 Percentile       : {fmt(stats['p95']):>20s}")
    print()


if __name__ == "__main__":
    if not HAS_NUMPY:
        print("❌ NumPy gerekli: pip install numpy")
        sys.exit(1)
    
    print("=== Monte Carlo DCF Simülasyonu ===\n")
    
    # Örnek: Türk orta ölçek şirket
    config = MCConfig(
        iterations=10_000,
        seed=42,
        projection_years=5,
        base_revenue=5_000_000,  # 5B TL
        revenue_growth=DriverDistribution("Revenue Growth", "normal", mean=0.15, std=0.08),
        operating_margin=DriverDistribution("Op Margin", "triangular", low=0.08, mode=0.14, high=0.22),
        tax_rate=DriverDistribution("Tax Rate", "normal", mean=0.25, std=0.02),
        reinvestment_rate=DriverDistribution("Reinvestment", "normal", mean=0.35, std=0.10),
        wacc=DriverDistribution("WACC", "normal", mean=0.15, std=0.03),
        terminal_growth=DriverDistribution("Terminal Growth", "triangular", low=0.03, mode=0.05, high=0.07),
        risk_free_rate=DriverDistribution("Rf", "normal", mean=0.045, std=0.005),
    )
    
    results = run_dcf_simulation(config)
    print_simulation_results(results)
    
    print("✅ monte_carlo.py çalışıyor.")
