# Cross-Agent Entegrasyon — Can'ın Araçları

**Lokasyon:** `~/.openclaw/workspace-can/skills/bbb-finans/scripts/`

## DCF Tools API Tablosu

| Modül | Fonksiyon | Girdi | Çıktı | Kullanım |
|-------|-----------|-------|-------|----------|
| **Veri Kaynakları** | | | | |
| `bbb_mkk.py` | `get_disclosure_data()` | disclosureId | XBRL field dict | KAP'tan finansal veri çek |
| `bbb_financials.py` | `get_financials()` | ticker, period | Gelir tablosu + bilanço | İş Yatırım API (fallback). IC = BV Equity + BV Debt - Cash + R&D Asset + Op Lease Debt |
| **WACC Pipeline** | | | | |
| `dcf_tools/wacc.py` | `compute_levered_beta()` | β_U, tax, D/E | β_L | Hamada β_L = β_U × (1+(1-t)×D/E) |
| `dcf_tools/wacc.py` | `compute_cost_of_equity()` | Rf, β_L, ERP, CRP, λ | Ke | Ke = Rf + β_L×ERP + λ×CRP |
| `dcf_tools/wacc.py` | `compute_wacc()` | mcap, debt, Ke, Kd, tax | WACC | (E/V)×Ke + (D/V)×Kd×(1-t) + (PS/V)×Kps |
| `dcf_tools/wacc.py` | `compute_full_wacc()` | Tüm WACC girdileri | Dict (β_L, Ke, WACC, weights) | Tek çağrıda tam WACC pipeline |
| `dcf_tools/beta_lookup.py` | `get_beta()` | industry, market | {industry, β_U, n_firms} | 95 Damodaran sektör, Türkçe alias, fuzzy match |
| `dcf_tools/beta_lookup.py` | `multi_business_beta()` | [(sektör, pay), ...] | weighted β_U | Revenue-weighted multi-business beta |
| `dcf_tools/synthetic_rating.py` | `get_synthetic_rating()` | ICR, mcap_usd_b | {rating, spread_bps} | ICR → Sentetik rating (AAA ICR≥8.50, spread 59bps) |
| `dcf_tools/synthetic_rating.py` | `cost_of_debt()` | ICR, Rf, country_spread | {pre_tax_kd, after_tax_kd} | Rf + Country Spread + Company Spread |
| `dcf_tools/erp_updater.py` | `get_turkey_erp()`, `get_country_erp()` | — | ERP decimals | Damodaran ERP verisi |
| **Projeksiyon & Değerleme** | | | | |
| `dcf_tools/projection_engine.py` | `run_dcf()` | `DCFInputs` dataclass | `DCFResult` (projections, TV, equity bridge) | 10 yıllık FCFF projeksiyon + terminal value + equity bridge + failure adj. |
| `dcf_tools/projection_engine.py` | `print_dcf_result()` | `DCFResult` | formatted text | Sonuç tablosu yazdırma |
| `dcf_tools/option_value.py` | `option_value_with_dilution()` | OptionParams, equity_value | {total_option_value, diluted_price} | B-S iteratif dilution: S_adj = (S×shares + opt_val×options)/(shares+options) |
| `dcf_tools/option_value.py` | `treasury_stock_method()` | options, K, S, shares | diluted_shares | Basit seyreltme hesabı |
| **Diğer Araçlar** | | | | |
| `dcf_tools/monte_carlo.py` | `run_dcf_simulation()` | DCF params + distributions | simulation results | Monte Carlo simülasyonu |
| `dcf_tools/rd_lookup.py` | `capitalize_rd()`, `get_rd_amort_years()` | R&D expenses, years | R&D asset, amort | R&D kapitalizasyonu |
| `dcf_tools/dual_track.py` | `dual_track_analysis()` | TL + USD params | cross-check | TL vs USD çapraz kontrol |
