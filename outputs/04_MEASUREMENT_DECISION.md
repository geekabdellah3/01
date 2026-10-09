# 04 - Inclusive Firm Growth: measurement decision

## Decision
**Strategy A (separate econometric models per dimension) is adopted. A composite Inclusive Growth Index is NOT constructed.**
Strategies B (full index) and C (reduced index) are evaluated only as exploratory diagnostics (workbook `04_INCLUSIVE_GROWTH_MEASUREMENT.xlsx`).

## What the data can measure
| Dimension | Measurable? | Comparable MAR-KOR? | Indicators used | Important limitation |
|---|---|---|---|---|
| D1 Economic growth | Yes | B (harmonizable) | annualised log sales growth; productivity growth = sales growth - employment growth | nominal LCU; no deflator; windows FY2019-22 (MAR) vs FY2020-23 (KOR); sales per worker, not value added |
| D2 Employment growth | Yes | B | annualised log growth of permanent full-time employment (l1 vs l2) | total only; survivors only; temporary workers not observed 3 years ago |
| D3 Social inclusion | Only as *composition at one date* | B | female share; low-skilled share of production workers | NOT growth of female/low-skilled employment (no category data 3 years ago); skill categories exist for production workers only; high-school share is at ceiling in Korea (class C) |
| D4 Environmental | Only 2 practice items | A (identical items) | energy-management adoption (ge8d); CO2 monitoring (ge7) | the Green Economy items (BMGc23a-j) used by Phan (2026) are absent; items are practices, not environmental outcomes |

Not measurable (class E, not used): real sales growth, growth of female/skilled/low-skilled employment, university-educated share, a 10-item green index, environmental investment, energy efficiency, waste management, digital technology adoption beyond a website.

## Why a composite index is not defensible
1. **Formative, not reflective.** Inclusive growth is a policy-defined concept whose components (output growth, jobs, workforce composition, environmental practice) *cause* the construct rather than being reflections of one latent trait. Reflective tools (Cronbach alpha, factor analysis) are therefore theoretically inappropriate, and a formative index needs externally justified weights that the literature does not supply.
2. **The indicators do not move together (empirical check).** On the six comparable indicators the mean inter-item Spearman correlation is 0.061, Cronbach alpha is 0.29 and KMO is 0.52 (Kaiser's 'miserable' band, 0.50-0.60; 0.60 or more is usually required), and the first principal component explains only 27% of the variance (16.7% would arise from six uncorrelated indicators). Examples (pooled, within-country z): sales growth vs employment growth rho = 0.26 (n=2027); employment growth vs female share rho = -0.06; sales growth vs female share rho = -0.02; energy-management vs CO2-monitoring rho = 0.80. Within countries, sales vs employment growth: Morocco 0.20, Korea 0.27.
3. **Weights and signs drive the ranking.** Rank correlation between equal-weight-indicator and equal-weight-dimension composites is 0.95; with PCA weights 0.39; against a growth-only composite 0.49; reversing the (normatively ambiguous) sign of the low-skilled share gives 0.65.
4. **Missing-data loss (secondary argument).** Complete cases on all six indicators: Morocco 411 of 598 (69%), Korea 1375 of 1,518 (91%). The loss is material for Morocco but is not by itself decisive; separate models keep each outcome's own sample (Morocco 407-504, Korea 1431-1495 after also requiring regressors and controls).
5. **Construct validity.** D3 is composition, not inclusive growth, and D4 consists of two practice items. An index built on them would present a thin set of proxies as a complete measure of Inclusive Growth.
6. **Loss of the comparison of interest.** Cross-country comparability requires within-country standardisation, which removes between-country level differences (the object of the Morocco-Korea comparison).

PCA is reported only as a dimensionality test; it is not used to build an index.

## Consequences for the econometric design
* Separate models per dimension (Phase 5) with identical regressors (product innovation, process innovation, website) and controls.
* Innovation and digitalization are treated as **explanatory variables**, not as components of inclusive growth.
* D4 is estimated as two binary practice outcomes (logit) and labelled "environmental practice adoption", never "environmental sustainability outcome".
* Composite-index results, if ever shown, are exploratory and carry no inferential weight.
