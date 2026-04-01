#!/usr/bin/env python3
"""
Monte Carlo DCF Simulasyonu — Evrensel Script
10.000 iterasyon ile DCF parametrelerine surekli olasilik dagilimi atar,
hisse basi deger dagilimini hesaplar.

Kullanim:
  python3 monte_carlo_dcf.py --config {TICKER}_mc_config.json [--iterations 10000] [--output sonuc.md]

Config dosyasi T2/T3 tamamlandiktan sonra Bear/Base/Bull parametrelerinden uretilir.
"""

import argparse
import json
import os
import sys
from datetime import date

import numpy as np


# ── PERT dagilimi (Beta-PERT) ──────────────────────────────
def pert_sample(minimum, mode, maximum, size=1, lambd=4):
    """PERT (Beta-PERT) dagilimidan orneklem.
    Goldman/Damodaran tercih ettigi DCF dagilimi.
    lambda=4 standart (mode'a 4x agirlik)."""
    if minimum >= maximum:
        return np.full(size, mode)
    mu = (minimum + lambd * mode + maximum) / (lambd + 2)
    if mu <= minimum or mu >= maximum:
        return np.full(size, mode)
    # Simetrik durum veya mode=mu durumunda (mode-mu) sifir olabilir
    denom = (mode - mu) * (maximum - minimum)
    if abs(denom) < 1e-12:
        # Simetrik PERT -> Beta(4,4) kullan (simetrik, merkez agirlikli)
        alpha = 4.0
        beta_param = 4.0
    else:
        alpha = ((mu - minimum) * (2 * mode - minimum - maximum)) / denom
        if alpha <= 0:
            alpha = 1.0
        beta_param = alpha * (maximum - mu) / (mu - minimum)
        if beta_param <= 0:
            beta_param = 1.0
    samples = np.random.beta(alpha, beta_param, size=size)
    return minimum + samples * (maximum - minimum)


def triangle_sample(minimum, mode, maximum, size=1):
    """Ucgen dagilim."""
    return np.random.triangular(minimum, mode, maximum, size=size)


def normal_sample(mean, std, size=1):
    """Normal dagilim."""
    return np.random.normal(mean, std, size=size)


def sample_parameter(spec, n):
    """Config'teki parametre spec'inden n orneklem uret."""
    d = spec["dagilim"]
    if d == "pert":
        return pert_sample(spec["min"], spec["mode"], spec["max"], size=n)
    elif d in ("triangle", "triangular"):
        return triangle_sample(spec["min"], spec["mode"], spec["max"], size=n)
    elif d == "normal":
        return normal_sample(spec["mean"], spec["std"], size=n)
    elif d == "fixed":
        return np.full(n, spec["value"])
    else:
        raise ValueError(f"Bilinmeyen dagilim tipi: {d}")


# ── DCF Hesaplama (tek iterasyon) ──────────────────────────
def compute_dcf_value(baz_gelir, gelir_buyume_y1, gelir_buyume_cagr_y2_5,
                      hedef_ebit_marji, terminal_buyume, wacc_terminal,
                      terminal_roc, vergi_orani, sc_y1_5, sc_y6_10,
                      pay_sayisi, net_borc, iflas_olasiligi,
                      sfp_explicit, sfp_terminal, projeksiyon_yili=10,
                      baz_ebit_marji=None):
    """Tam 10Y DCF hesabi — tek iterasyon."""

    # WACC yolu: Y1-5 sabit (sfp_explicit dahil), Y6-10 lineer terminal'e
    wacc_y1_5 = wacc_terminal + sfp_explicit - sfp_terminal
    # Y6-10: lineer interpolasyon
    wacc_path = []
    for y in range(1, projeksiyon_yili + 1):
        if y <= 5:
            wacc_path.append(wacc_y1_5)
        else:
            # Lineer: Y6 -> wacc_y1_5'ten wacc_terminal'e 5 adimda
            t = (y - 5) / 5.0
            wacc_path.append(wacc_y1_5 * (1 - t) + wacc_terminal * t)

    # Gelir projeksiyonu
    revenues = [baz_gelir]
    # Y1 buyumesi
    revenues.append(baz_gelir * (1 + gelir_buyume_y1))

    # Y2-5: CAGR
    for y in range(2, 6):
        revenues.append(revenues[-1] * (1 + gelir_buyume_cagr_y2_5))

    # Y6-10: buyume azaliyor (lineer interpolasyon CAGR -> terminal_buyume)
    for y in range(6, projeksiyon_yili + 1):
        t = (y - 5) / 5.0
        g = gelir_buyume_cagr_y2_5 * (1 - t) + terminal_buyume * t
        revenues.append(revenues[-1] * (1 + g))

    # EBIT marji: baz'dan hedef'e lineer yakinsama (Y7'de hedef)
    if baz_ebit_marji is None:
        baz_ebit_marji = hedef_ebit_marji * 0.87  # default ~%87 baslangic
    margins = []
    for y in range(1, projeksiyon_yili + 1):
        if y <= 7:
            t = y / 7.0
            margins.append(baz_ebit_marji + t * (hedef_ebit_marji - baz_ebit_marji))
        else:
            margins.append(hedef_ebit_marji)

    # Vergi orani: Y1-6 sabit, Y7-10 lineer artis (~%25'e)
    etrs = []
    for y in range(1, projeksiyon_yili + 1):
        if y <= 6:
            etrs.append(vergi_orani)
        else:
            t = (y - 6) / 4.0
            etrs.append(vergi_orani + t * (0.25 - vergi_orani))

    # FCFF hesabi
    fcffs = []
    for y in range(1, projeksiyon_yili + 1):
        rev = revenues[y]
        ebit = rev * margins[y - 1]
        nopat = ebit * (1 - etrs[y - 1])
        delta_rev = revenues[y] - revenues[y - 1]
        sc = sc_y1_5 if y <= 5 else sc_y6_10
        reinv = delta_rev / sc if sc > 0 else 0
        fcff = nopat - reinv
        fcffs.append(fcff)

    # PV hesabi
    cdf = 1.0
    pv_sum = 0.0
    for y in range(projeksiyon_yili):
        cdf /= (1 + wacc_path[y])
        pv_sum += fcffs[y] * cdf

    # Terminal value
    terminal_rr = terminal_buyume / terminal_roc if terminal_roc > 0 else 0
    last_rev = revenues[projeksiyon_yili]
    terminal_nopat = last_rev * hedef_ebit_marji * (1 - 0.25) * (1 + terminal_buyume)
    terminal_fcff = terminal_nopat * (1 - terminal_rr)

    denom = wacc_terminal - terminal_buyume
    if denom <= 0.001:
        denom = 0.001  # guvenlik siniri

    tv = terminal_fcff / denom
    pv_tv = tv * cdf  # son yilin CDF'i ile iskonto

    # Equity bridge
    oav = pv_sum + pv_tv
    oav_adj = oav * (1 - iflas_olasiligi)
    equity = oav_adj + net_borc  # net_borc = nakit - borc (pozitif = net nakit)

    hisse_degeri = equity / pay_sayisi if pay_sayisi > 0 else 0

    return max(hisse_degeri, 0)  # negatif deger 0 olarak sinirla


# ── Ana Monte Carlo Dongusu ────────────────────────────────
def run_monte_carlo(config, n_iterations=10000, seed=42):
    """N iterasyonlu Monte Carlo simulasyonu."""
    np.random.seed(seed)
    params = config["parametreler"]

    # Orneklemleri uret
    gelir_y1 = sample_parameter(params["gelir_buyume_y1"], n_iterations)
    cagr_y2_5 = sample_parameter(params["gelir_buyume_cagr_y2_5"], n_iterations)
    ebit_marj = sample_parameter(params["hedef_ebit_marji"], n_iterations)
    term_g = sample_parameter(params["terminal_buyume"], n_iterations)
    wacc_t = sample_parameter(params["wacc_terminal"], n_iterations)
    term_roc = sample_parameter(params["terminal_roc"], n_iterations)

    # Sabit parametreler
    baz_gelir = config["baz_gelir"]
    vergi = config.get("vergi_orani", 0.23)
    sc15 = config.get("sales_capital_y1_5", 5.0)
    sc610 = config.get("sales_capital_y6_10", 4.5)
    pay = config["pay_sayisi"]
    net_borc = config.get("net_borc", 0)
    iflas = config.get("iflas_olasiligi", 0.01)
    sfp_e = config.get("sfp_explicit", 0)
    sfp_t = config.get("sfp_terminal", 0)
    proj_yil = config.get("projeksiyon_yili", 10)
    baz_ebit = config.get("baz_ebit_marji", None)

    results = np.zeros(n_iterations)

    for i in range(n_iterations):
        results[i] = compute_dcf_value(
            baz_gelir=baz_gelir,
            gelir_buyume_y1=gelir_y1[i],
            gelir_buyume_cagr_y2_5=cagr_y2_5[i],
            hedef_ebit_marji=ebit_marj[i],
            terminal_buyume=term_g[i],
            wacc_terminal=wacc_t[i],
            terminal_roc=term_roc[i],
            vergi_orani=vergi,
            sc_y1_5=sc15,
            sc_y6_10=sc610,
            pay_sayisi=pay,
            net_borc=net_borc,
            iflas_olasiligi=iflas,
            sfp_explicit=sfp_e,
            sfp_terminal=sfp_t,
            projeksiyon_yili=proj_yil,
            baz_ebit_marji=baz_ebit
        )

    return results


# ── Tornado Analizi ────────────────────────────────────────
def tornado_analysis(config, n_iterations=5000):
    """Her parametreyi tek tek 1 sigma kaydirip etkisini olc."""
    params = config["parametreler"]
    base_result = np.median(run_monte_carlo(config, n_iterations))

    sensitivities = {}
    for pname, pspec in params.items():
        # Parametreyi yukari kaydir
        config_up = json.loads(json.dumps(config))
        if pspec["dagilim"] in ("pert", "triangle", "triangular"):
            shift = (pspec["max"] - pspec["min"]) * 0.15
            config_up["parametreler"][pname] = {
                "dagilim": "fixed", "value": pspec["mode"] + shift
            }
        elif pspec["dagilim"] == "normal":
            config_up["parametreler"][pname] = {
                "dagilim": "fixed", "value": pspec["mean"] + pspec["std"]
            }
        up_result = np.median(run_monte_carlo(config_up, n_iterations))

        # Asagi kaydir
        config_dn = json.loads(json.dumps(config))
        if pspec["dagilim"] in ("pert", "triangle", "triangular"):
            config_dn["parametreler"][pname] = {
                "dagilim": "fixed", "value": pspec["mode"] - shift
            }
        elif pspec["dagilim"] == "normal":
            config_dn["parametreler"][pname] = {
                "dagilim": "fixed", "value": pspec["mean"] - pspec["std"]
            }
        dn_result = np.median(run_monte_carlo(config_dn, n_iterations))

        sensitivities[pname] = {
            "up_effect": up_result - base_result,
            "down_effect": dn_result - base_result,
            "total_swing": abs(up_result - dn_result)
        }

    # Etki buyuklugune gore sirala
    sorted_sens = sorted(sensitivities.items(),
                         key=lambda x: x[1]["total_swing"], reverse=True)
    return sorted_sens


# ── Rapor Uretici ──────────────────────────────────────────
def generate_report(results, config, tornado=None, deterministic_base=None):
    """Monte Carlo sonuclarini Markdown rapor olarak uret."""
    ticker = config.get("ticker", "SIRKET")
    mevcut_fiyat = config.get("mevcut_fiyat", None)

    mean_val = np.mean(results)
    median_val = np.median(results)
    std_val = np.std(results)
    p10 = np.percentile(results, 10)
    p25 = np.percentile(results, 25)
    p75 = np.percentile(results, 75)
    p90 = np.percentile(results, 90)
    var_95 = np.percentile(results, 5)  # %5'lik alt kuyruk
    cvar_95 = np.mean(results[results <= var_95])

    lines = []
    lines.append(f"## Monte Carlo Simulasyon Sonuclari -- {ticker}")
    lines.append(f"### Iterasyon: {len(results):,} | Tarih: {date.today()}")
    lines.append("")
    lines.append("### Dagilim Istatistikleri")
    lines.append("| Metrik | Deger |")
    lines.append("|--------|-------|")
    lines.append(f"| Ortalama (Beklenen Deger) | {mean_val:.1f} TL |")
    lines.append(f"| Medyan (P50) | {median_val:.1f} TL |")
    lines.append(f"| Standart Sapma | {std_val:.1f} TL |")
    lines.append(f"| 10. Yuzdelik (P10) | {p10:.1f} TL |")
    lines.append(f"| 25. Yuzdelik (P25) | {p25:.1f} TL |")
    lines.append(f"| 75. Yuzdelik (P75) | {p75:.1f} TL |")
    lines.append(f"| 90. Yuzdelik (P90) | {p90:.1f} TL |")
    lines.append(f"| Minimum | {np.min(results):.1f} TL |")
    lines.append(f"| Maximum | {np.max(results):.1f} TL |")
    lines.append(f"| VaR %95 (asagi yon riski) | {var_95:.1f} TL |")
    lines.append(f"| CVaR %95 (kosullu VaR) | {cvar_95:.1f} TL |")

    if mevcut_fiyat is not None:
        lines.append("")
        lines.append("### Olasilik Degerlendirmesi")
        lines.append("| Esik | Olasilik |")
        lines.append("|------|----------|")
        p_above_current = np.mean(results > mevcut_fiyat) * 100
        lines.append(f"| > Mevcut fiyat ({mevcut_fiyat:.1f} TL) | %{p_above_current:.1f} |")

        if deterministic_base:
            p_above_target = np.mean(results > deterministic_base) * 100
            lines.append(f"| > Hedef fiyat ({deterministic_base:.1f} TL) | %{p_above_target:.1f} |")

    if deterministic_base:
        lines.append("")
        lines.append("### Deterministic vs Monte Carlo Karsilastirma")
        lines.append("| Yontem | Deger | Fark |")
        lines.append("|--------|-------|------|")
        lines.append(f"| Deterministic Base (T3) | {deterministic_base:.1f} TL | -- |")
        diff_mean = ((mean_val / deterministic_base) - 1) * 100
        diff_med = ((median_val / deterministic_base) - 1) * 100
        lines.append(f"| MC Ortalama | {mean_val:.1f} TL | {diff_mean:+.1f}% sapma |")
        lines.append(f"| MC Medyan | {median_val:.1f} TL | {diff_med:+.1f}% sapma |")

    if tornado:
        lines.append("")
        lines.append("### Hassasiyet Siralamasi (Tornado Analizi)")
        lines.append("| Parametre | Baz +/- 1sigma Etkisi | Rank |")
        lines.append("|-----------|----------------------|------|")
        for rank, (pname, sens) in enumerate(tornado, 1):
            swing = sens["total_swing"]
            readable = pname.replace("_", " ").title()
            lines.append(f"| {readable} | +/-{swing/2:.1f} TL | {rank} |")

    lines.append("")
    lines.append("> Deterministic ve MC ortalamasi arasinda >%10 fark varsa")
    lines.append("> parametrelerin dagilim seklini gozden gecir (asimetri kontrol).")

    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Monte Carlo DCF Simulasyonu")
    parser.add_argument("--config", required=True, help="JSON config dosyasi")
    parser.add_argument("--iterations", type=int, default=10000, help="Iterasyon sayisi")
    parser.add_argument("--output", default=None, help="Cikti Markdown dosyasi")
    parser.add_argument("--no-tornado", action="store_true", help="Tornado analizini atla (hizli mod)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    # Config oku
    with open(args.config, 'r', encoding='utf-8') as f:
        config = json.load(f)

    print(f"Monte Carlo DCF baslatiliyor: {config.get('ticker', '?')}")
    print(f"  Iterasyon: {args.iterations:,}")
    print(f"  Parametre sayisi: {len(config['parametreler'])}")

    # Simulasyon
    results = run_monte_carlo(config, args.iterations, seed=args.seed)

    # Tornado (opsiyonel)
    tornado = None
    if not args.no_tornado:
        print("  Tornado analizi yapiliyor...")
        tornado = tornado_analysis(config, n_iterations=min(args.iterations, 5000))

    # Deterministic baz (varsa)
    det_base = config.get("deterministic_base", None)
    mevcut = config.get("mevcut_fiyat", None)

    # Rapor
    report = generate_report(results, config, tornado, det_base)

    if args.output:
        out_dir = os.path.dirname(args.output)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n[OK] Rapor yazildi: {args.output}")
    else:
        print("\n" + report)

    # Ozet
    print(f"\n--- OZET ---")
    print(f"  Ortalama: {np.mean(results):.1f} TL")
    print(f"  Medyan:   {np.median(results):.1f} TL")
    print(f"  P10-P90:  {np.percentile(results,10):.1f} - {np.percentile(results,90):.1f} TL")
    if mevcut:
        p_up = np.mean(results > mevcut) * 100
        print(f"  P(>{mevcut:.0f} TL): %{p_up:.1f}")


if __name__ == "__main__":
    main()
