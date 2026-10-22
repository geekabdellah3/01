# Deliverable K — V6: response to the review of V5

Files: `ROBUSTNESS_V6_A.xlsx` (`02_SCRIPTS/contextual/25a_robustness_v6.py`), `ROBUSTNESS_V6_B.xlsx` (`25b_wildboot_hb.py`), manuscript `06_PAPER/revision_v6/MCS_Practices_Transferability_WBES_G7_v6.docx`.

| Review point | Action | Outcome |
|---|---|---|
| r4×r8 structure, collinearity | Cross-tab, φ, VIF (A) | r8 asked of all; 14% of bonus firms report no targets (Germany 35%); φ(T,I) = 0.22; VIF 1.05–1.21; limits inference on T×I |
| Power / "no gain" claims | Wording changed to "no detectable gain"; CI compared with oracle gain; no equivalence claimed | N1 vs P1 corrected CI (−0.0031, 0.0035) includes 0 and 0.0028 |
| Hierarchical / shrinkage model | Partial-pooling BLUP in cross-validation (B) | Best point estimate: −0.0014 vs P1 (p = 0.11), −0.0012 vs N1 (p = 0.25) |
| τ, I² intervals; leave-one-out | Q-profile CIs; LOCO heterogeneity (A) | τ 0.114 (0.070–0.346); I² 79% (58–97); stays 65–82% without any country |
| Outliers, Canada | No truncation, 5/95, median regression (A) | I² 77–81%; unchanged |
| Weights | WLS with supplied weights (A) | Incentive heterogeneity weaker: Q = 11.0, p = 0.088, I² = 45% |
| Clustered inference | Restricted wild cluster bootstrap, 73 clusters (B) | Incentives/productivity p = 0.015 (Holm 0.105); targets/sales growth 0.006 (Holm 0.054); asymptotic clustered p-values (0.0000) dropped as anti-conservative |
| Transfer defined on practices only | Practice-only transfer with controls fixed at LOCO estimates (A) | Local better in 81% of pairs, mean 0.017 (full model 93%, 0.033): about half of the loss comes from controls |
| Local − LOCO combined test | Inverse-variance combination (A) | +0.0095 (0.0023–0.0167), p = 0.010: LOCO is close but detectably slightly worse |
| Claim vs global score (6.8) | Stated with source (latent-score analysis: 88%, 0.020) and caveat on different predictors | |
| Text/abstract inconsistencies | Abstract, 6.4, 7.1, 7.3, H1/H3 statements rewritten | Monitoring significant in 3 of 7 countries; H1 not supported for targets; H3 only suggestively for incentives |
| Survival bias, reverse causality, winsorisation | Added to Sections 4 and 10 | |
| Morocco section | Removed (one-sentence scope note) | |
| References | Completed (Merchant & Van der Stede 2017, Nadeau & Bengio 2003, Ouchi 1979, Cameron et al. 2008); added Bloom et al. 2013, Bloom, Genakos, Sadun & Van Reenen 2012, Scur et al. 2021, Ichniowski et al. 1997, Lazear 2000; removed Moroccan and thesis-only items | Lazear and Bloom et al. (2013) cited without effect sizes (abstract versions differ) |
| Questionnaire verification (r2, r4, r8) | **Not possible here** (World Bank site unreachable; no questionnaires supplied) | Remains the first blocking item |
| Reading the central papers | **Not possible here** (paywalled full texts) | Remains to be done by the author |

Notes: the earlier asymptotic sector-cluster Wald p-values (0.0000) were wrong in practice with 7–15 clusters per country; sectors are strata in the sampling design, so clustering at sector is a conservative sensitivity analysis rather than the design-based choice. The V5 statement "LOCO close to local" was replaced by the combined-test result.
