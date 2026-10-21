# 3. Data and methods

**Data.** The user-supplied merged file contains 10,968 establishments from seven WBES country-years (Canada 2024, France 2025, Germany 2025, Italy 2024, Japan 2025, United Kingdom 2024, United States 2024). The original `.dta` files could not be accessed; the CSV contains codes without value labels. Question wording was verified only partially (r5 for Italy 2024; r1–r3, r8–r9 through secondary descriptions) and not at all for r6, r7, r10 and r11, which are therefore treated as nominal without substantive labels.

**Universe and skip patterns.** The management module is asked of 6,316 establishments (88.5% with ≥20 permanent full-time employees). Within this universe r1, r2, r4, r8, r10 and r11 are asked of all; r3 only if r2 = yes, r5–r7 only if r4 = yes, r9 only if r8 = yes (verified in the data). Code −9 (don't know) is treated as missing; −7 (does not apply; r1, r10, r11) is set to missing in the main analyses and kept as a category in a sensitivity specification.

**Specifications.** A: r1, r2, r4, r8, r10, r11 (N = 6,294 with ≥1 observed item). B: conditional items with a structural-absence category. C: all 11 items, skipped items omitted from the likelihood. D: A with −7 retained.

**Latent class analysis.** Categorical LCA by EM with full-information treatment of missing items, 40–60 random starts, eight full runs per K, K = 1–8, fixed seeds. The implementation was verified against StepMix (log-likelihood differences ≤0.003). Selection used AIC, BIC, adjusted BIC, relative entropy, average posterior probabilities, class sizes, local-maximum diagnostics and bivariate residuals. Profiles carry bootstrap intervals (150 replicates with class alignment).

**Gradient versus configuration.** (i) Class ordering and crossings on directional indicators (r2, r4, r8); (ii) BIC comparison on the same likelihood of K-class LCA, a 1-D nominal-response trait, a 2-D trait and a hybrid (K classes × 1-D trait); (iii) outcome regressions comparing a transparent score (number of r2/r4/r8 present), the continuous trait and latent classes (soft posterior regressors, pseudo-class draws with Rubin's rules, 10-fold cross-validated RMSE).

**Dimensionality.** Polychoric correlations, parallel analysis, minimum-residual EFA with promax rotation (assumes code order = ordinal order and is therefore used only as supporting evidence), nominal MCA and country-specific Tucker congruence.

**Cross-country.** Pooled, country-specific and multi-group LCA (shared item-response probabilities, country-specific prevalence), item-wise differential item functioning by likelihood ratio, leave-one-country-out, weights, size, split-half, leave-one-item-out.

**Outcomes and nonlinearity.** Log sales per employee, annualised three-year sales growth and employment growth (definitions of n3 and l2 unverified), winsorised, with country and country-specific sector fixed effects, log size and log age; HC3 standard errors; natural cubic splines, quadratic terms and interactions; Holm correction over 30 tests. All associations are cross-sectional.
