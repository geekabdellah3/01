# LCA robustness report (all numbers produced by scripts 04–09, 12; see 03_RESULTS)

Reference solution: specification A (r1, r2, r4, r8, r10, r11; N = 6,294 firms with ≥1 observed item; categories treated as nominal; FIML for item-level missing).

## 1. Implementation check
The in-house EM (numpy; R/poLCA unavailable) was compared with StepMix 3.0.0 on complete cases (N = 4,989): log-likelihood differences 0.0001 (K=2), 0.001 (K=3), 0.003 (K=4). `robustness/crosscheck_stepmix.csv`.

## 2. Number of classes
| Spec | BIC-min K | Notes |
|---|---|---|
| A (6 universal items) | 4 (53,186.6); K=3 53,199.1; K=5 53,191.3 | BIC essentially flat K=3–5 (Δ ≤ 13); aBIC minimum K=5–6; AIC still falling at K=8 |
| B (conditional items, structural-absence category) | 5 (106,380.3) | K=3 106,422.6; K=4 106,397.5 |
| C (all 11 items, skipped = missing) | 4 (106,155.5) | high residual dependence between gate and child items (BVR>900) |
| D (A with −7 kept as category) | 6 (62,638.3) | K=5 62,654.6 |

Relative entropy is low-to-moderate (A: 0.53 at K=3, 0.60 at K=4; B: 0.75 at K=4), minimum average posterior probability 0.64–0.70 (A). In spec A, 47% of item pairs show bivariate residuals > 3.84 at K=3/4 (local independence not satisfied). The parametric bootstrap LRT was **NOT TESTED**.

## 3. Discrete vs continuous structure on the same likelihood
Best BIC by family (ΔBIC to the best model of the specification):
- A: hybrid (3 classes × 1-D trait) 0; 2-D continuous +25.6; 1-D continuous +122.3; LCA (K=4) +128.5.
- B: 2-D continuous 0; hybrid +35.4; LCA (K=5) +367.7; 1-D continuous +1,111.6.
- C: 2-D continuous 0; hybrid +16.0; 1-D continuous +156.4; LCA (K=4) +235.9.
- D: 2-D continuous 0; hybrid +51.7; LCA (K=6) +237.7.
Caveat: in B/C/D the conditional items are structurally linked to their gates, which favours a second continuous dimension; the 2-D model uses a 7×7 quadrature grid.

## 4. Seeds, weights, subsamples (spec A; `ROBUSTNESS_TABLES.xlsx`)
- Seeds: identical log-likelihood and profiles for five seeds (profile distance ≤ 0.014). K=3: 5/5 starts reach the optimum; K=4: 2–5 of 5.
- K=3 profiles are fairly stable under normalised survey weights (distance 0.22–0.24), complete cases (0.17), leave-one-country-out (0.09–0.41), split-halves (0.13–0.29), firm size (≥50: 0.44; <50: 0.38).
- K=4 is **not** stable: distances up to 1.3; the 5–7% class is recovered inconsistently (class share 4.7–17%).
- Leave-one-item-out BIC-best K: 3 when dropping r2, r4, r8 or r10; 4 for r11; 5 for r1.

## 4b. Cross-country validity
- Country-specific LCA, BIC-best K: 2 for CAN, DEU, FRA, JPN, USA; 3 for GBR, ITA. Country-specific K=3 profiles differ from the pooled profile by a mean absolute probability difference of 0.45–0.89 (USA closest, ITA farthest).
- Multi-group LCA: with K=3, full invariance is rejected by BIC (free item parameters ΔBIC = −245), with DIF on r2, r8, r10, r11; with K=4, the fully invariant model is preferred by BIC (free model +541) and only r8 shows DIF. Conclusion on invariance therefore **depends on K**; measurement comparability across countries is only partial.
- Country composition (pooled K=3 solution, mean posterior probability of C3, the class with the highest core score): GBR 70%, USA 66%, CAN 56%, FRA 49%, DEU 41%, JPN 27%, ITA 22%. These are descriptive and are **not** interpreted as institutional effects.
- Sector codes are country-specific and sampling frames differ (size strata, sector coverage); sector composition could therefore not be harmonised.

## 5. Classification uncertainty
Modal assignment shares 19–52% (A, K=3) with AvePP 0.70–0.84. Outcome analyses therefore use soft posterior regressors and pseudo-class draws (M=50, Rubin pooling; fraction of missing information 0.31–0.47).

## 6. What was NOT done
Parametric bootstrap LRT; design-based variance estimation; BCH/ML three-step; R/poLCA replication; verification against the original `.dta` files; ordinal-restricted LCA.
