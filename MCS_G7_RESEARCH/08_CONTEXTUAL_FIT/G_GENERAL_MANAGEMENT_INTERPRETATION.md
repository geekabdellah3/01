# Deliverable G — Interpretation through general management theory, then bridge to management control

**Order of reasoning requested:** (1) interpret the WBES results through recognised general-management frameworks; (2) only then relate them to the management-control (MC) literature. The earlier manuscript went the other way (MC concepts first). This note and manuscript v3 reverse the order.

## 1. Choice of general frameworks (default proposed; the choice is the author's to confirm)
Primary lens: **contingency (fit) theory and institutional theory of the adoption, implementation and transfer of management practices**, because the data are about *which practices firms report* and *how those reports relate to performance across contexts*. Counterpoint: **management as a technology** (universalist). Supporting: **capability/absorptive-capacity** arguments. Alternative primary lens that the author may prefer (it matches the doctoral project): dynamic capabilities (Teece, 2007); it is kept here as a supporting lens because WBES has no capability measures.

| Framework | Core proposition (as stated in verified records) | Key sources |
|---|---|---|
| Contingency / fit | No single best way to organise; performance depends on fit between structure and conditions; fit has several forms (selection, interaction, systems) | Lawrence & Lorsch (1967); Donaldson (2001); Drazin & Van de Ven (1985) |
| Institutional: legitimacy and decoupling | Formal structures reflect institutionalised rules; adoption for legitimacy can be decoupled from ongoing activities; isomorphic pressures; rhetoric can diverge from practice | Meyer & Rowan (1977); DiMaggio & Powell (1983); Zbaracki (1998) |
| Transfer of practices | Transfer success is institutionalisation at the recipient unit and is shaped by country institutional profile, organisational context and individuals; adoption can be ceremonial | Kostova (1999); Kostova & Roth (2002) |
| Management as technology | Differences in management practices explain firm and national productivity; adoption differs across countries; dispersion has a long tail | Bloom & Van Reenen (2007, 2010); Bloom, Sadun & Van Reenen (2016) |
| Capabilities | Ability to recognise, assimilate and apply external information depends on prior related knowledge | Cohen & Levinthal (1990); Teece (2007) |
| Equifinality | Functionally equivalent configurations can yield similar performance | Gresov & Drazin (1997) |

## 2. Empirical implications of each framework and what the data show
| Framework | Implication observable in WBES | Observed | Reading |
|---|---|---|---|
| Management as technology | Common structure; positive slope in every country; differences in adoption, not effects | Common dimension (partial invariance); positive slope in 5/7 countries, ≈0 in FRA, GBR; large adoption differences | Partly consistent |
| Contingency / fit | Slope varies with measured contingencies (size, age, ownership, exports, managers) | No moderator robust after Holm; foreign ownership suggestive (+0.12, Holm p = 0.33) | Not supported with the contingencies available; relevant contingencies (environment, technology) not measured |
| Institutional decoupling | High adoption with weak link to outcomes, esp. where adoption is widespread | Weakest slopes in highest-adoption countries (FRA, GBR); slope flattens in the upper third of the score (0.164 → 0.013; equality p = 0.009, unadjusted) | Consistent, but **not discriminated** from ceiling/restricted range/measurement error; integration not observed |
| Transfer / embeddedness | Stronger link where parent or relational support exists; country institutional profile matters | Foreign ownership signal (suggestive); country institutions not measurable | Not testable beyond a suggestive proxy |
| Capabilities | Stronger link with more experienced managers | Manager experience: null | Not supported with this proxy |
| Equifinality | Combinations with equal core score perform similarly | Not rejected, not demonstrated (wide CIs); monitoring+bonus > monitoring+targets (+0.187 log points, exploratory) | Inconclusive |

## 3. New diagnostics bearing on the decoupling-versus-artefact question
- **Common support.** Restricting every country to the score range present in all countries (−0.40 to 0.69 pooled SD; 29–51% of each country's firms): productivity heterogeneity Q = 11.9, p = 0.064, I² = 50% (versus Q = 13.5, p = 0.036 with pooled-prior EAP on the full sample). Slopes become imprecise (e.g. CAN 0.73, GBR −0.38). Heterogeneity is attenuated but not removed; power is low.
- **Level dependence.** A common piecewise shape (thirds of the pooled score) lowers the Wald statistic for country-specific slopes from 10.1 (p = 0.122) to 8.0 (p = 0.241) for productivity; for growth outcomes it makes no difference (p ≈ 0.026). Within countries, below/above-median slope differences are not significant except Canada (−0.52, p = 0.002; seven tests, not Holm-adjusted). Conclusion: part of the cross-country difference in productivity slopes is compatible with a common, level-dependent association; the rest is unexplained.

Files: `SUPPORT_CEILING_DIAGNOSTICS.xlsx`, `02_SCRIPTS/contextual/16_support_ceiling.py`.

## 4. Bridge to the management-control literature (second step)
| General concept | MC counterpart | WBES contribution | Unobserved |
|---|---|---|---|
| Adoption of formal practices | Package of controls (Malmi & Brown, 2008); institutionalisation of rules and routines (Burns & Scapens, 2000) | Prevalence by size and country of monitoring, targets, bonuses | Planning, administrative, cultural controls |
| Decoupling / ceremonial adoption | Package versus system; internal consistency (Grabner & Moers, 2013); use of controls (Simons, 1995; Tessier & Otley, 2012) | Presence–outcome association weak at high adoption (suggestive) | Use, articulation, integration |
| Fit / contingency | Contingency research on MCS (Chenhall, 2003; Otley, 2016) | Firm-level moderators ≈ null | Environmental uncertainty, technology, strategy |
| Universal core of practices | Cybernetic controls (monitoring, targets) and reward controls | Common continuous dimension; weak classes | Mode of use |
| Transfer across contexts | Cross-cultural MC research (Harrison & McKinnon, 1999); critique of national-culture determinism (McSweeney, 2002) | Country heterogeneity of associations, entangled with measurement | Culture, institutions as measured constructs |
| Equifinality / configurations | Configurations of control (Bedford & Malmi, 2015) | Combinations at equal core score: inconclusive | Designed versus accreted configurations |

**Consequence for the article.** The MC concepts are positioned as domain-specific instances of the general frameworks, and the claims about control *systems* are restricted to what the general-framework reading allows: practices reported, structure estimated, associations observed; integration and use remain theoretical.
