# Deliverable C — Empirical analysis plan (as implemented)

Hypotheses were formulated **after** an earlier exploratory phase on the same data; none is pre-registered. Implementation: `02_SCRIPTS/contextual/13_contextual_fit.py` (results `CONTEXT_TABLES.xlsx`), `14_context_figures.py`, `15_framework_figure.py`.

| Hypothesis | Operationalisation | Disposition |
|---|---|---|
| H1 common sophistication dimension | One-factor structure; parallel analysis; continuous vs discrete BIC; country-specific one-factor Tucker congruence | **Tested** (earlier phase; retained) |
| H2 measurement structure differs across countries | Multi-group LCA invariance; item DIF (LR); country-specific K; 5-item invariant subset | **Tested** (earlier phase; qualified) |
| H3 MCS–performance slope varies across countries | Country-specific slopes; Cochran Q, I², random-effects prediction interval; pooled Wald test of slope equality | **Tested** (new) |
| H4 performance associations depend on combinations and context | Gate-combination equality within equal core-score levels; class×country interactions; firm-level moderators (size, age, foreign ownership, export, manager experience/gender) | **Partly tested** (new); national-institution moderation cannot be tested with 7 countries |
| H5 equifinality | Equality and equivalence (CI within ±margin) of combinations with equal core score | **Weakly testable**; cross-country equifinality reformulated as proposition |

## Variables
Outcomes: log sales per employee (ln_lp), annualised 3-year sales growth, annualised 3-year employment growth (n3, l2 definitions unverified). Score: latent trait θ from the nominal 1-D model on spec-A items (country-specific-prior posterior mean, per latent SD; pooled-prior EAP kept for continuity with the earlier phase), 5-item subset excluding r8 (DIF item), and core score S = r2+r4+r8. Controls: ln employees, ln age, country-specific sector fixed effects (sector codes are country-specific). Moderators: foreign ownership ≥10% (b2b), exporter (d3b+d3c>0), ln top-manager experience (b7), female top manager (b7a), size, age (labels from data-dictionary snippets of other 2024 surveys; not verified for the G7 files).

## Equations
Country-specific: y_i = α_s(i) + β_c θ_i + γ_c' X_i + ε_i, estimated separately for each country c (HC3). Pooled: y_ic = α_s(i) + Σ_c β_c θ_i·1[c] + γ' X_i (or γ_c) + ε; **H0: β_1 = … = β_7** by robust Wald test (6 df), with HC3 and sector-clustered covariances. Heterogeneity: Q = Σ w_c(β_c − β̄)², I² = (Q − 6)/Q, DerSimonian–Laird τ², 95% prediction interval with t(5). Moderation: y = α_s + β θ + δ m + λ θ·m + γ'X, with and without θ×country terms. Measurement uncertainty: regression calibration, i.e. the posterior mean of θ computed with a country-specific normal prior (mean and variance estimated by EM; item parameters pooled). Unconditional plausible values were tried first and **rejected** because they attenuate slopes by roughly the reliability (they gave slopes about 0.6 times the calibrated ones).

## Multiple testing and effect sizes
Holm within families (moderators, equifinality, class×country, nonlinearity); the heterogeneity analysis is reported as a specification-curve summary (13 specifications per outcome) because the specifications are not independent. Effect sizes: slopes with 95% CIs, I², outcome-SD units for nonlinearity deviations, ΔR².

## Robustness
Alternative scores (country-prior calibrated θ, pooled EAP, invariant subset, core score); with/without country-specific control slopes; HC3 vs sector-clustered; weighted WLS (wmedian); equivalence margins stated explicitly (±0.05 log points; ±0.005 growth) and flagged as arbitrary.

## Tables and figures
T: country sample; LCA fit (retained); invariance/DIF; country slopes with Q/I²; specification-curve of slope-equality tests; moderators; equifinality; class×country; nonlinearity by country. Figures: framework; forest plot of country slopes (Fig 6); moderators (Fig 7); existing structure figures.

## Not possible with the available data
Design-based variance (no PSU/strata); national institutional or cultural moderators; integration/use measures; causal identification.
