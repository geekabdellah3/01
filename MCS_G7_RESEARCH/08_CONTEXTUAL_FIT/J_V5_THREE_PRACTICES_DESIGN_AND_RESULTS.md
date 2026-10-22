# Deliverable J — V5: Bloom & Van Reenen practices as the starting point

**Logic reversed again, as requested:** start from the three practice families of Bloom & Van Reenen (monitoring r2, targets r4, incentives r8; direction verified by skip logic), relate them to performance individually, jointly and across contexts, then interpret with control theory. The earlier "framework coverage" heatmap is no longer part of the main argument (kept only as an appendix table in the manuscript).

Files: `THREE_PRACTICES_TABLES.xlsx` (script `02_SCRIPTS/contextual/22_three_practices.py`), `WHY_COMMON_MODEL_COMPETES_3P.xlsx` (`24_why_three_practices.py`), `PREDICTIVE_COMPARISON_AND_TRANSFER_A/_V.xlsx` and `TRANSFER_PAIRED_A/_V.xlsx` (`20_predictive_transfer_robust.py`, latent-score robustness with and without r10, r11), figures `Fig_Framework_v5_practices_to_transferability`, `Fig8_three_practices_by_country`.

## Main results (productivity unless stated)
- Individual: incentives +0.199 log points (95% CI 0.156–0.243), monitoring +0.122 (0.069–0.175), targets +0.047 (−0.010–0.104).
- Combinations: no pairwise interaction (joint p = 0.35); three-way term +0.229 (p = 0.040) not replicated for growth and not robust to multiplicity.
- Countries: incentives Q = 28.4 (p = 0.0001; Holm 0.0009), I² = 79%, from 0.509 (Canada) to 0.048 (France); monitoring p = 0.39; targets p = 0.63. Sales growth: targets p = 0.0027 (Holm 0.021).
- Organisational moderators: none robust after Holm (size p = 0.009, Holm 0.17).
- Out of sample: common slopes −1.8% mean squared error; combinations, contingency, national slopes (p = 0.91) add nothing.
- Why: oracle gain of known national slopes 0.0028 (0.45% of residual MSE) vs cost of 18 extra slopes ≈ 0.0021; national slopes win in 53% of simulations at the estimated heterogeneity, 95% at twice.
- Transfer: single-country model worse than local in 93% of pairs (mean 0.033 R²); LOCO close to local (intervals include zero everywhere).
- Latent-score robustness excluding r10, r11: same conclusions.

## Corrections made on the way
(i) Moderator tests for size and age were first degenerate (duplicate main effect) and were fixed; (ii) the sign of the local-minus-benchmark gap was reversed in the first runs and was fixed in script 22; the files `TRANSFER_PAIRED_A/_V.xlsx` (script 20) still carry the reversed sign in their columns `R2_gap_local_minus_benchmark`, `ci_lo`, `ci_hi` (true gap = −value; interval = (−ci_hi, −ci_lo)); (iii) unconditional plausible values and the earlier moderator baseline were abandoned for the reasons recorded in deliverables C and I.

## Not done
Verification of item wording against questionnaires; design-based inference; institutional indicators (M3); measures of integration and use; systematic literature review on control-practice transfer. Sundström (2024): a search found "AI in management control: Emergent forms, practices, and infrastructures", Critical Perspectives on Accounting 99, 102701; this is not cited in the manuscript because the earlier discussion about it is not visible in this session.
