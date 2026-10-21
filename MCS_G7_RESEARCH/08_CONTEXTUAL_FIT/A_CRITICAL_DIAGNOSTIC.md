# Deliverable A — Critical diagnostic of the existing manuscript

**Object audited:** `06_PAPER/Beyond_MCS_Packages_WBES_G7.docx` (title: *Management Control Practices as Configurations or Continuums?*), the only manuscript available in this environment. The file named `Beyond_MCS_Packages_WBES_G7-2.docx` in the brief was **not** present; if it differs from the repository version, it must be supplied so the audit can be repeated. The original manuscript and dataset are not modified by this project (new work lives in `08_CONTEXTUAL_FIT/`).

**Method of audit.** Every empirical sentence in the manuscript was traced to a stored result file (`03_RESULTS/**`) and, where the claim affects the new argument, re-examined. Verdicts: RETAIN (supported, reproducible), QUALIFY (supported but needs a caveat), VERIFY (depends on something unverified), DROP/REWRITE.

## 1. Claims register

| # | Claim in manuscript | Evidence (file) | Verdict | Reason |
|---|---|---|---|---|
| C1 | Module universe = 6,316 establishments; 88.5% have ≥20 employees | VARIABLE_AUDIT.xlsx | RETAIN | Skip logic verified in the data; but the universe is a *filter*, so results do not generalise to small firms |
| C2 | LCA (A): BIC flat K=3–5, entropy .53–.60, large residual dependence | LCA_MODEL_SELECTION.xlsx | RETAIN | Reproduced, and cross-checked with StepMix (≤0.003 log-lik) |
| C3 | K=3 classes ordered, 0/9 crossings | LCA_DIAGNOSTICS.xlsx | QUALIFY | Classes are *ordered by mean core score*, which is built from r2+r4+r8 — the same items used to count crossings. Zero crossing is therefore partly by construction; it remains informative only because it is not guaranteed for each item. The eta² (0.70) between class and core score is circular and should not be presented as evidence |
| C4 | Continuous/hybrid models beat LCA on BIC | LCA_MODEL_SELECTION.xlsx | QUALIFY | Valid on the same likelihood, but (i) 2-D model uses 7×7 quadrature; (ii) in B/C/D conditional items are structurally linked to gates, which favours extra dimensions; (iii) normality of θ is assumed. Conclusion "gradient predominates" holds for spec A (six items) and should not be generalised to the full control system |
| C5 | One factor retained (parallel analysis, 2.54 vs 1.09) | EDA_TABLES.xlsx | QUALIFY | Assumes code order = ordinal order for r1, r10, r11 — **unverified wording**; nominal category order was shown *not* monotone for r1, r10, r11 along θ. Supporting only |
| C6 | Reliability of θ = 0.60 | DIMENSIONALITY_TABLES.xlsx | RETAIN, and it matters | Moderate reliability ⇒ attenuation of θ–performance slopes; not discussed enough |
| C7 | Tucker congruence .93–.99 across countries | DIMENSIONALITY_TABLES.xlsx | QUALIFY | Congruence is a weak invariance criterion; the multi-group likelihood tests give a different message |
| C8 | Invariance rejected at K=3, retained at K=4; DIF in r2, r8, r10, r11 (K=3), r8 only (K=4) | ROBUSTNESS_TABLES.xlsx | RETAIN | Honest report that conclusion depends on K. This is the key limitation for any cross-country comparison |
| C9 | +0.128 log points sales/employee per SD of θ; growth coefficients small | LCA_OUTCOME_INCREMENTAL.xlsx | QUALIFY | (i) LCU outcome identified only within country; (ii) no survey weights; (iii) HC3 only, no clustering/design information; (iv) n3 and l2 definitions unverified; (v) θ pooled across countries although items are non-invariant |
| C10 | Classes add nothing beyond continuous score | LCA_OUTCOME_INCREMENTAL.xlsx | RETAIN | Tested with soft assignment and pseudo-class draws; but done on the pooled sample only. Not tested *within* countries |
| C11 | Nonlinearity: significant but tiny; no interactions after Holm | NONLINEAR_TABLES.xlsx | RETAIN | Family of 30 tests with Holm; ΔR² ≤ 0.04%. The tests used the classical (non-robust) F statistic — must be replaced by robust Wald tests |
| C12 | "Country gaps ITA lowest, GBR highest" | EDA_TABLES.xlsx | QUALIFY | Raw descriptive; confounded by size composition (adjusted contrasts shrink but keep order). Not an institutional effect |
| C13 | Wording of r6, r7, r10, r11 unverified | VARIABLE_AUDIT.xlsx | VERIFY (blocking) | Any substantive reading of these items is impossible |
| C14 | Discussion: "productivity may be partly reversed in causality" | Manuscript p.8 | REWRITE | Loose phrase; should read "reverse causality" |

## 2. What the existing results already say about the new question
The manuscript did **not** test whether the performance association differs across countries. A related test exists in the stored results (θ × country slope heterogeneity, classical F): log productivity F = 1.56 (p = 0.154), employment growth p = 0.14, sales growth p = 0.013 (Holm-adjusted 0.35). These are **not** sufficient evidence of universality (low power; non-robust F; θ not invariant) and are **not** evidence of contingency either. Formal, robust tests are required (Deliverable D).

## 3. Findings to retain
Structure of the module and skip logic (C1); weak class separation and flat BIC (C2); superiority of continuous/hybrid representations in spec A (C4, qualified); partial invariance depending on K (C8); associations with productivity as *associations* (C9, qualified); null incremental value of classes (C10); negligible nonlinearity (C11).

## 4. Findings requiring verification
Wording and category order of r1, r6, r7, r10, r11 (and r9 labels); definitions of n3 and l2; labels of ownership, export and manager variables (partially verified via search records: b2b = % owned by private foreign parties, b7 = top manager's years of experience in the sector, b7a = top manager female, d3b/d3c = indirect/direct export shares of sales — based on 2024 data-dictionary snippets for other countries, not on the seven G7 files); survey-design variables (PSU/strata for variance estimation are not in the CSV).

## 5. Analyses that can support the revised argument
Formal tests of cross-country slope heterogeneity; country-specific β with CIs and meta-analytic heterogeneity (Cochran's Q, I²); pooled θ×country Wald tests (robust, with regression calibration for θ uncertainty and a sensitivity score using only invariant items); firm-level moderators (size, age, foreign ownership, export, manager experience, female top manager); equifinality tests within equal core-score levels; country-specific nonlinearity with correction.

## 6. Analyses that cannot support it
- **Identifying institutional or cultural mechanisms.** With seven countries, a country-level institutional or cultural moderator has about 5 degrees of freedom; no external institutional indicator is in the data, and country fixed effects are not measures of culture or institutions.
- **Contextual fit.** Fit requires a measured context and a measured practice-context alignment; neither is in WBES.
- **Integration or mode of use (Simons).** Not measured.
- **Why practices are abandoned or fail to transfer.** Not measured.
- **Causal effects of practices on performance.**

## 7. Major methodological weaknesses (ranked)
1. Unverified wording/category order for five of eleven items.
2. Partial, K-dependent measurement invariance while the pooled θ is used for cross-country performance comparisons.
3. Unweighted, non-design-based inference; no clustering variables.
4. Performance proxies in local currency, with unverified growth denominators.
5. Moderate reliability of θ (0.60) ⇒ attenuation and spurious heterogeneity risk.
6. Circularity in class-score diagnostics (C3).
7. Hypotheses formulated after exploratory phases; no pre-registration (all new tests are exploratory/confirmatory-in-spirit only).

## 8. Risks of theoretical overinterpretation
- Reading "no configurational structure" as refuting Malmi & Brown (only a subset of controls is observed).
- Reading a common sophistication dimension as universal *effectiveness*.
- Reading cross-country differences in prevalence or slopes as culture or institutions.
- Naming the small K=4 class (targets, few bonuses) as "poor integration" — class is unstable.
- Treating "integration" as demonstrated; it is a theoretical construct here.

## 9. Inputs requiring raw data/documents not available here
Original `.dta` files with labels; questionnaire PDFs per country; PSU/strata/finite-population information; the manuscript file `-2`; external country-level institutional indicators (if the user wishes to attempt a descriptive institutional mapping, which cannot be tested statistically with seven countries).
