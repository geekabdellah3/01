# Deliverable H — Modelling management control (MCS) frameworks and mapping them to WBES

Files: `MCS_MODEL_SPECIFICATIONS.xlsx` (formal specifications, construct–item mapping, coverage), `MCS_MODEL_FIT_ON_WBES.xlsx` (competing item structures), figure `Fig_MCS_models_WBES_coverage.png`; scripts `19_mcs_model_mapping.py`, `17_mcs_models_vs_wbes.py`.

## 1. Frameworks formalised (only what verified records support)
| Framework | Formal specification (our notation) | Verification |
|---|---|---|
| Malmi & Brown (2008) | x_ij = λ_jk C_ik + ε; package = joint distribution of (C_i1…C_i5); Performance = f(C_i) | Five categories verified |
| Simons (1995); Tessier & Otley (2012) | x_ij = λ S_ik + μ U_ik; effects depend on use U ∈ {diagnostic, interactive} | Four systems and modes verified |
| Otley (1999); Ferreira & Otley (2009) | Areas A1…A5 (objectives, strategies and plans, targets, rewards, information flows); coherence | Five areas, twelve-question extension verified |
| Merchant & Van der Stede | Results, action, personnel, cultural controls | Four types verified |
| Ouchi (1979) | Market, bureaucracy, clan; social and informational preconditions | Verified (abstract) |
| Grabner & Moers (2013) | System = package + internal consistency | Verified (abstract) |
| Bloom & Van Reenen (2007) | Score = Σ practices (monitoring, targets, incentives) | Verified (abstract) |
| Chenhall (2003); Otley (2016) | Effect = β + δ′Context | Verified (summaries) |

## 2. Mapping to WBES (judgemental; strength reflects conceptual fit and wording verification)
Coverage = (observed + 0.5 × partial) / constructs: Bloom–Van Reenen tradition 1.00; Otley/Ferreira–Otley 0.70; Malmi & Brown 0.50 (cybernetic and reward observed, planning partial, administrative and cultural not); Merchant & Van der Stede 0.50; Chenhall/Otley (contingency) 0.50 (organisational variables only); Ouchi 0.33; Simons 0.12 (diagnostic use compatible, nothing on belief, boundary or interactive use); Grabner & Moers 0.00 (internal consistency not identifiable from presence). The scores summarise a judgement, not a measurement.

## 3. Do the WBES items follow the structure of the frameworks? (nominal-response models, 7 items: r1, r2, r3, r4, r5, r8, r9; N = 6,294)
| Model | Parameters | BIC | ΔBIC vs one factor | factor correlation |
|---|---|---|---|---|
| One factor (sophistication) | 26 | 57,628.9 | 0 | – |
| Malmi & Brown: cybernetic {r1–r5} + reward {r8, r9} | 27 | 57,637.5 | +8.5 | ≥ 0.7 |
| Results controls {r4, r5, r8, r9} + monitoring {r1–r3} | 27 | 57,642.8 | +13.8 | ≈ 0.95 (grid maximum) |
| Three families: monitoring, targets, rewards | 27 | 57,639.1 | +10.2 | ≈ 0.95 (grid maximum) |
| Unrestricted two factors | 40 | 57,672.4 | +43.4 | 0.7 |

No framework-implied split improves on one factor; the restricted models collapse toward perfect factor correlation. Caveats: wording partly unverified; each gate item and its follow-up item share a questionnaire block, which can mimic or mask family structure; correlations were searched on a grid up to 0.95; items mapping to administrative, cultural, belief, boundary or interactive constructs do not exist.

## 4. Consequences
(1) The empirical content of the control frameworks that WBES can address reduces to cybernetic/results/reward controls, which behave as one dimension. (2) Differences between frameworks (package types, levers, Ouchi mechanisms) concern constructs WBES does not observe. (3) Statements about the *structure of a control system* cannot be derived from these data.
