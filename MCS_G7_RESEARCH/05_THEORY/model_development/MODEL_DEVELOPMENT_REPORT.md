# Model development report

Figure: `MANAGEMENT_CONTROL_MODEL.png/.svg/.pdf`. Four layers; solid = estimated in this study; dashed = theoretical reading not tested; no causal arrows.

## How the model emerged (data → theory, not theory → data)
1. **Layer 1 – observable practices.** Only what WBES records: indicator monitoring (r2, r3), reaction to problems (r1), targets (r4–r7), target-linked bonuses (r8, r9), two items of unverified wording (r10, r11). Wording was verified only partly (see `VARIABLE_AUDIT.xlsx`). The module is asked of 6,316 of 10,968 firms (mostly 20+ employees); r3, r5–r7, r9 are asked only if their gate (r2, r4, r8) is "yes" (skip logic verified in the data).
2. **Layer 2 – empirical structure.**
   - *Dominant continuous dimension.* Parallel analysis on polychoric correlations of the six universal items retains one factor (eigenvalue 2.54 vs 1.09 95th-percentile); 1-factor loadings: r2 .82, r4 .71, r8 .54, r1 .41, r10 .46, r11 .34 (|loading|; sign arbitrary). The nominal 1-D latent trait has marginal reliability 0.60 — informative but far from precise at firm level. Country-specific one-factor solutions have Tucker congruence .93–.99 with the pooled solution.
   - *Discrete profiles are weak.* LCA entropy .53–.60, BIC flat for K=3–5, strong residual dependence; K=3 classes are ordered along the core score without crossing on the three yes/no practices (0/9 crossings, Kendall's W = 1). K=4 adds a small (≈5–7%) class with targets but fewer bonuses, unstable across subsamples.
   - *Both continuous and discrete elements.* Hybrid (3 classes × 1 trait) has the lowest BIC in spec A; a 2-D continuous model is best in B, C, D. We therefore do **not** report a typology of distinct control systems; we report a gradient with, at most, tentative secondary structure.
   - *Combinations.* Of three gates (r2, r4, r8): all present 43% (1.35× independence), none present 10% (3.7×), most partial combinations rarer than independence (exception: bonus-only, 1.12×).
   - *Associations among practices.* Monitoring–targets is the strongest (bias-corrected V = .41); bonuses and r10/r11 are looser (V .15–.27).
3. **Layer 3 – interpretation.** Malmi & Brown: observed items are mainly cybernetic and reward controls; cultural, planning and administrative controls are essentially unobserved, so "package" here means co-occurrence of a subset. Simons: monitoring and targets are *compatible* with diagnostic control; interactive use and belief/boundary systems are unobserved. Bloom & Van Reenen: an aggregate score captures most of the structure we can detect.
4. **Layer 4 – associations.** Larger firms score higher (mean core score 1.86 → 2.51 from <50 to 250+ employees). Within country and controlling size, age and sector, one SD of the continuous score is associated with +0.128 log points of sales per employee, +0.003 annual sales growth, +0.002 annual employment growth (HC3; no weights). Latent classes add no explanatory power beyond the continuous score (pseudo-class F tests all p>0.28). Non-linearity: modest curvature for productivity (Holm p<.05). No robust interaction among monitoring, targets and bonuses after Holm correction.

## What the model does **not** claim
No causal effects; no validated constructs; no diagnostic/interactive typology; no institutional explanation of country differences; no universal control system. Outcome variable definitions n3 and l2 are unverified (assumed sales/employment three fiscal years earlier).

## Unobserved but theoretically important
Mode of use of information (diagnostic/interactive), beliefs and boundaries, cultural and planning controls, AI-enabled analytics, internal-audit feedback, dynamic capabilities, readiness for change.
