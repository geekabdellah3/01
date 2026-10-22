# Deliverable I — Competing models and international transferability

Implements the strategy proposed by the author: M1 (universal), M2 (organisational contingency), M3 (national institutional contextualisation), judged by out-of-sample prediction, then a transferability matrix. Files: `PREDICTIVE_COMPARISON_AND_TRANSFER.xlsx`, script `02_SCRIPTS/contextual/18_predictive_transfer.py`.

## Models
All models contain country-specific sector fixed effects, log size, log age and the main effects of foreign ownership (≥10%), exporter status, log top-manager experience and female top manager. Score θ = nominal one-dimensional trait on the six common items.
- U0 controls only; **M1** U1 common linear slope; U2 common level-dependent (piecewise-linear by thirds) shape.
- **M2** C1: U2 + θ × (size, age, foreign ownership, exporter, manager experience, manager gender).
- National: N1 country-specific linear slopes; N2 common level-dependent shape + country deviations. X = C1 + N2.
- **M3** (θ × national institutional indicator Z_c) is **not estimated**: with seven countries it has at most a handful of degrees of freedom, and it is nested in N1/N2 (any θ×Z_c term is a restriction of θ×country). If country-specific slopes bring no predictive gain, no Z_c interaction can be justified on predictive grounds. External indicators (e.g. governance, trust, culture) were deliberately not added, following the recommended sequence.

## Protocol
10-fold cross-validation repeated 3 times, folds stratified by country and identical for all models; the item parameters of the score are re-estimated on training folds only and applied to test firms (outcome-free score, no leakage of outcomes); moderators standardised on training data; paired comparisons use firm-level squared errors averaged over repeats (95% CI, normal approximation, ignores dependence across folds). An initial run in which only C1 and X carried the extra main effects showed an apparent contingency gain (RMSE 0.787 vs 0.799) that disappeared once all models carried the same main effects; this is why the baseline was equalised.

## Results (log sales per employee, N = 5,913)
RMSE out of sample: U0 0.7924; U1 0.7873; U2 0.7872; C1 0.7871; N1 0.7877; N2 0.7876; X 0.7873. Paired reduction in mean squared error: U0→U1 0.0081 (95% CI 0.0044 to 0.0118; 1.3%); U1→U2 0.0001 (−0.0008, 0.0011); U2→C1 0.0002 (−0.0017, 0.0020); U1→N1 −0.0006 (−0.0019, 0.0007); U2→N2 −0.0006 (−0.0018, 0.0006); C1→X −0.0003; N2→X 0.0005. For sales growth (RMSE 0.0876 → 0.0875) and employment growth (0.0650 → 0.0650) no model improves on controls beyond 0.1%.
**Reading:** the common linear association gives a small but reliable predictive gain for productivity; neither organisational contingency nor national slopes adds out-of-sample value (the case labelled "Scenario A" in the proposal). This does not exclude contextual effects that WBES cannot measure.

## Transferability (slope-only models on country-sector-demeaned data; score and controls outcome-free)
Productivity, linear shape. Out-of-sample R² (explained share of within-cell variance) of a model estimated in the source country and applied to the target; local R² from 5×10-fold CV in the target; LOCO = trained on the other six countries.
| Source ↓ / Target → | CAN | FRA | DEU | ITA | JPN | GBR | USA |
|---|---|---|---|---|---|---|---|
| CAN | – | −0.018 | 0.021 | 0.064 | 0.030 | 0.008 | 0.013 |
| FRA | 0.012 | – | 0.013 | 0.026 | 0.016 | 0.016 | −0.001 |
| DEU | 0.022 | −0.014 | – | 0.032 | 0.032 | 0.010 | 0.009 |
| ITA | 0.012 | −0.074 | −0.055 | – | −0.000 | −0.017 | −0.028 |
| JPN | 0.026 | −0.023 | 0.023 | 0.053 | – | 0.023 | −0.005 |
| GBR | 0.003 | −0.012 | 0.005 | 0.031 | 0.026 | – | −0.036 |
| USA | 0.020 | −0.023 | 0.008 | 0.041 | −0.002 | −0.028 | – |
| LOCO | 0.030 | −0.012 | 0.028 | 0.050 | 0.030 | 0.009 | 0.003 |
| Local (CV) | 0.021 | −0.016 | 0.032 | 0.070 | 0.034 | 0.021 | 0.021 |
Across the 42 source–target pairs the local model is better in 88% of pairs (mean advantage 0.020 R² units); a model trained on the other six countries loses little (mean 0.006; local better in 5 of 7 targets; local exceeds the LOCO interval only in the United States). All R² values are very small (maximum 0.07). Employment and sales growth give no transferable signal either way (local R² mostly ≤ 0.03).
**Reading:** single-country models transfer imperfectly, but a pooled model estimated elsewhere is nearly as good as a local one. The data therefore support limited transferability losses, not the need for a country-specific model. A transfer loss would in any case not show that the cause is institutional.

## Still needed for the institutional claim (M3)
More countries or time variation; verified, comparable institutional indicators; multilevel design with country-level uncertainty; measures of integration and use of controls.
