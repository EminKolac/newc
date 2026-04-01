#!/usr/bin/env python3
"""
Option Value Iterative Solver
Black-Scholes with dilution, iterative convergence.

Şirketin opsiyonlarının (employee stock options, warrants) değerini hesaplar.
Dilution etkisi iteratif olarak çözülür çünkü opsiyon değeri hisse fiyatına,
hisse fiyatı da opsiyon değerine bağlıdır (circular reference).

Kullanım: DCF modelinde opsiyon değerini özsermayeden düşmek için.
"""

import math
import sys
from typing import Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class OptionParams:
    """Opsiyon parametreleri."""
    num_options: float  # Opsiyon sayısı
    exercise_price: float  # Kullanım fiyatı
    expiration_years: float  # Vadeye kalan süre (yıl)
    stock_price: float  # Güncel hisse fiyatı
    risk_free_rate: float  # Risksiz faiz oranı
    volatility: float  # Yıllık volatilite (σ)
    dividend_yield: float = 0.0  # Temettü verimi
    shares_outstanding: float = 1.0  # Mevcut hisse sayısı


def _norm_cdf(x: float) -> float:
    """Standart normal kümülatif dağılım fonksiyonu (yaklaşık)."""
    # Abramowitz & Stegun approximation
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    
    sign = 1 if x >= 0 else -1
    x = abs(x)
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x / 2)
    
    return 0.5 * (1.0 + sign * y)


def black_scholes_call(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    q: float = 0.0,
) -> Dict[str, float]:
    """
    Black-Scholes European Call option fiyatı.
    
    Args:
        S: Hisse fiyatı
        K: Kullanım fiyatı (strike)
        T: Vadeye kalan süre (yıl)
        r: Risksiz faiz oranı
        sigma: Volatilite
        q: Temettü verimi
        
    Returns:
        {'price': float, 'd1': float, 'd2': float, 'N_d1': float, 'N_d2': float}
    """
    if T <= 0 or sigma <= 0 or S <= 0:
        intrinsic = max(S - K, 0)
        return {"price": intrinsic, "d1": 0, "d2": 0, "N_d1": 0, "N_d2": 0}
    
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    N_d1 = _norm_cdf(d1)
    N_d2 = _norm_cdf(d2)
    
    price = S * math.exp(-q * T) * N_d1 - K * math.exp(-r * T) * N_d2
    
    return {
        "price": round(price, 6),
        "d1": round(d1, 6),
        "d2": round(d2, 6),
        "N_d1": round(N_d1, 6),
        "N_d2": round(N_d2, 6),
    }


def option_value_with_dilution(
    params: OptionParams,
    equity_value: Optional[float] = None,
    max_iterations: int = 100,
    tolerance: float = 0.001,
) -> Dict[str, float]:
    """
    Dilution etkisiyle opsiyon değeri (iteratif çözüm).
    
    Circular reference:
    - Opsiyon değeri = f(hisse fiyatı)
    - Hisse fiyatı = (Equity - Opsiyon Değeri) / (Hisse + Opsiyonlar)
    
    Iteratif yakınsama ile çözülür.
    
    Args:
        params: Opsiyon parametreleri
        equity_value: Toplam özsermaye değeri (None → stock_price × shares)
        max_iterations: Max iterasyon
        tolerance: Yakınsama eşiği ($)
        
    Returns:
        {
            'option_value_per': Opsiyon başına değer,
            'total_option_value': Toplam opsiyon değeri,
            'diluted_stock_price': Seyreltilmiş hisse fiyatı,
            'dilution_pct': Seyreltme yüzdesi,
            'iterations': Yakınsama iterasyon sayısı,
            'converged': bool,
        }
    """
    if equity_value is None:
        equity_value = params.stock_price * params.shares_outstanding
    
    n_options = params.num_options
    n_shares = params.shares_outstanding
    
    # Initial guess: undiluted stock price
    stock_price = equity_value / n_shares
    prev_option_value = 0.0
    
    for iteration in range(1, max_iterations + 1):
        # Step 1: Calculate option value at current stock price
        bs = black_scholes_call(
            S=stock_price,
            K=params.exercise_price,
            T=params.expiration_years,
            r=params.risk_free_rate,
            sigma=params.volatility,
            q=params.dividend_yield,
        )
        option_value_per = bs["price"]
        total_option_value = option_value_per * n_options
        
        # Step 2: Adjust stock price for dilution
        # Damodaran Excel formula:
        # Adjusted S = (S × shares + option_value_per × options) / (shares + options)
        diluted_shares = n_shares + n_options
        
        if diluted_shares > 0:
            new_stock_price = (stock_price * n_shares + option_value_per * n_options) / diluted_shares
        else:
            new_stock_price = 0
        
        # Check convergence
        if abs(total_option_value - prev_option_value) < tolerance:
            dilution_pct = (total_option_value / equity_value * 100) if equity_value > 0 else 0
            return {
                "option_value_per": round(option_value_per, 4),
                "total_option_value": round(total_option_value, 2),
                "diluted_stock_price": round(new_stock_price, 4),
                "undiluted_stock_price": round(equity_value / n_shares, 4),
                "dilution_pct": round(dilution_pct, 2),
                "iterations": iteration,
                "converged": True,
                "bs_details": bs,
            }
        
        prev_option_value = total_option_value
        stock_price = new_stock_price if new_stock_price > 0 else stock_price * 0.5
    
    # Did not converge
    return {
        "option_value_per": round(option_value_per, 4),
        "total_option_value": round(total_option_value, 2),
        "diluted_stock_price": round(stock_price, 4),
        "undiluted_stock_price": round(equity_value / n_shares, 4),
        "dilution_pct": round(total_option_value / equity_value * 100, 2) if equity_value > 0 else 0,
        "iterations": max_iterations,
        "converged": False,
    }


def treasury_stock_method(
    num_options: float,
    exercise_price: float,
    stock_price: float,
    shares_outstanding: float,
) -> Dict[str, float]:
    """
    Hazine hisse yöntemi ile seyreltilmiş hisse sayısı.
    Daha basit yaklaşım (iteratif değil).
    
    Returns:
        {'diluted_shares': float, 'net_new_shares': float, 'dilution_pct': float}
    """
    if stock_price <= 0 or stock_price <= exercise_price:
        return {
            "diluted_shares": shares_outstanding,
            "net_new_shares": 0,
            "dilution_pct": 0,
        }
    
    proceeds = num_options * exercise_price
    shares_bought_back = proceeds / stock_price
    net_new = num_options - shares_bought_back
    diluted = shares_outstanding + net_new
    dilution_pct = (net_new / shares_outstanding) * 100
    
    return {
        "diluted_shares": round(diluted, 0),
        "net_new_shares": round(net_new, 0),
        "dilution_pct": round(dilution_pct, 2),
    }


if __name__ == "__main__":
    print("=== Option Value Iterative Solver ===\n")
    
    # Test 1: Basic Black-Scholes
    bs = black_scholes_call(S=100, K=90, T=2, r=0.05, sigma=0.30)
    print(f"  Black-Scholes: S=100, K=90, T=2, r=5%, σ=30%")
    print(f"  Call Price: ${bs['price']:.2f}")
    print(f"  d1={bs['d1']:.4f}, d2={bs['d2']:.4f}")
    
    # Test 2: Dilution iteration
    print(f"\n  --- Dilution İterasyon ---")
    params = OptionParams(
        num_options=10_000_000,
        exercise_price=50.0,
        expiration_years=3.0,
        stock_price=80.0,
        risk_free_rate=0.05,
        volatility=0.35,
        dividend_yield=0.01,
        shares_outstanding=100_000_000,
    )
    
    result = option_value_with_dilution(params, equity_value=8_000_000_000)
    print(f"  Opsiyon/adet: ${result['option_value_per']:.2f}")
    print(f"  Toplam opsiyon değeri: ${result['total_option_value']:,.0f}")
    print(f"  Seyreltilmiş fiyat: ${result['diluted_stock_price']:.2f}")
    print(f"  Seyreltme: {result['dilution_pct']:.2f}%")
    print(f"  İterasyon: {result['iterations']} | Yakınsama: {result['converged']}")
    
    # Test 3: Treasury stock method
    print(f"\n  --- Hazine Hisse Yöntemi ---")
    tsm = treasury_stock_method(10_000_000, 50, 80, 100_000_000)
    print(f"  Seyreltilmiş hisse: {tsm['diluted_shares']:,.0f}")
    print(f"  Net yeni hisse: {tsm['net_new_shares']:,.0f}")
    print(f"  Seyreltme: {tsm['dilution_pct']:.2f}%")
    
    print("\n✅ option_value.py çalışıyor.")
