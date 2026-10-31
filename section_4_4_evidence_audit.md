# Critical Evidence Audit of Section 4.4 — "The Business Partner as a Translation Mechanism"

Target journal: *JOCM*. Basis: the supplied literature review matrix (`Lecture_Articles-3.xlsx`, sheet *Fiches de Lecture*). No original article was re-read. Every finding below is as reported in the matrix, and numbers are quoted from it.

---

## 0. Read this first: scope, mapping and data-integrity caveats

**0.1 Scope.** The matrix holds **49 rows (A1–A50; A13 is absent from this file), not A1–A40**. Its title says "38 articles". I read all 49. This matters because **Elo et al. (2026) can only be A47**, which lies outside A1–A40. (`slr_ai_mcs/REPORT.md` in this repo, built from an earlier copy of the sheet, lists an A13 on Moroccan financial institutions. It is peripheral to this audit.)

**0.2 There is no author column, so author-year to A-ID mapping is partly inferred.**

| Citation in your brief | Mapped to | Basis | Confidence |
|---|---|---|---|
| Boerner et al. (2025) | **A5** | Title, abstract, design (BAC → BP role → controllership effectiveness, n = 322 German firms) | High (inferred) |
| Bedford et al. (2025) | **A2** | Title/abstract (automation, analytics, BP objective, finance-function effectiveness, n = 137) | High (inferred) |
| Elo et al. (2026) | **A47** | 7,426 Finnish job ads, controller role trends | High (inferred) |
| Andreassen (2020) | **A33** | Title/abstract (role change, decision makers' expectations of and involvement of MAs). The "conclusions" cell holds literature-review headings, so only abstract-level findings are usable | Medium |
| Järvenpää et al. (2023) | **Not resolvable** | No row in the matrix identifies this source. Nearest in content: A22, A1, A34, A28 | — |
| Gimpl et al. (2026) | A37 | Named in the matrix's own conclusion cell | High |
| Getzin et al. (2026) | A45 | Named in the matrix's own conclusion cell | High |
| Teece (2007); Malmi & Brown (2008) | **Not in the matrix** | Malmi & Brown appears only as a cited framework in A9. A12 uses Teece et al. (1997) | — |

**Please confirm the mappings, and tell me which row is Järvenpää.** I do not attach author names to any other A-ID, because I would be inventing them. The draft in §10 uses `[A#]` tags where the author-year is unknown.

**0.3 Teece (2007) and Malmi & Brown (2008).** My use of these two frameworks comes from background knowledge, not from the matrix. Check my characterisations against the originals before citing them.

**0.4 Row-level data problems that affect this audit.**
- **A4**: the methodology, theory, variable and hypothesis cells are copied from A15 (an AI-transparency experiment). Only the abstract is usable (qualitative insider action research, BI pilot).
- **A9** is typed "quantitative" but is 14 interviews. **A16** is typed hypothetico-deductive but is interview-based.
- **A8, A10, A17, A25, A35, A41, A42** are abstract-level only. Findings from them are flagged "(abs.)".
- **A33**: the findings cell is literature-review text. Findings come from the abstract.
- **A5**: the matrix gives no path coefficients, only full/partial mediation.
- **A41** has no results. **A42** has "lecture intégrale requise".

**0.5 "Tension" is used in four different senses in the matrix.** None of them is the IPC/IPR tension in your framework:
- epistemic tension between two cultures (A1);
- role tension, conflict or ambiguity (A24, A34);
- professional-boundary tension (A25);
- tension between a global and a local accounting language (A28).

No row describes an **IPC–IPR misalignment** explicitly. The nearest are A2 (joint automation × analytics lowers effectiveness, "might be a result of resource constraints"), A34 (time absorbed by data work), A27 (too much data harms) and A29 ("KPI overload"). Your tension construct is therefore an interpretation imposed on this evidence.

**0.6 "AI-induced" is not what the BP studies examine.** A5 studies business analytics capabilities. A2 studies automation and analytics. A47 studies job ads on "digitalisation". A34 studies Big Data. The AI-specific rows are A15 (experiment, non-controller participants), A22 (practitioner discourse about AI), A29 (design science), A45 and A42 (adoption), A18 (AI/RPA as one driver), and the reviews A6, A10, A20, A31. **No study in the matrix observes a business partner handling AI-generated information.**

**0.7 Statuses used.** DS = DIRECTLY SUPPORTED, IS = INDIRECTLY SUPPORTED, TI = THEORETICAL INFERENCE, ND = NOT DOCUMENTED, MX = CONTRADICTORY OR MIXED. Absence in the matrix is not treated as proof the phenomenon does not exist.

---

## 1. Studies relevant to Section 4.4 (A1–A50), by theme

| Theme | Studies |
|---|---|
| Role transformation / competencies | A47, A24, A25, A18, A33, A34, A35, A9, A16, A30, A32, A38, A46, A7, A40, A10, A20, A31, A50, A45 |
| Business partnering practices / BP role | A5, A2, A24, A34, A9, A18, A25, A47, A46, A32, A16, A35, A30 |
| Human judgement and AI/analytic output | A22, A15, A45, A35, A21, A29, A1 |
| Filtering, interpretation, sensemaking | A1, A22, A34, A28, A32, A8, A21, A50, A27 |
| Business analytics capability → control effectiveness | A5, A2, A37, A19, A11, A41, A26, A27, A46 |
| Sensing, seizing, transforming (Teece lens) | **A12 only (measured)**. Others only by interpretation |
| MCS as a package / levers | A9 (cites Malmi & Brown), A12, A39, A41 (Simons); no row tests a package |
| Interdependencies between controls | Adjacent only: A37, A26, A28, A1, A48, A49 |
| Routines, decision rights, coordination | A9, A7, A37, A30, A18, A25, A40, A28, A8 |
| Information-processing framing | A2, A26, A37 (explicit OIPT/Galbraith/Tushman & Nadler); A27, A29 (information overload) |

---

## 2. Evidence matrix (Q1–Q12)

| # | Research question | Supporting studies | Exact reported findings (matrix) | Evidence type | Status | Missing evidence |
|---|---|---|---|---|---|---|
| **Q1** | Does digitalisation transform management accountants' competencies and responsibilities? | A9, A18, A33, A25, A46, A7, A30, A32, A47, A34, A16, A50, A45; reviews A10, A20, A31, A38 | **A9**: controller moves from information provider to proactive BP; competences broaden (analytics, IT, communication); "does not create a new profession". **A7** (n = 189): digitalisation raises strategic and operational *tasks* and operational *instruments*; no significant effect on strategic instruments or on organisation of MC. **A46**: MAIS sophistication → controller strategic involvement, β = 0.467, p < 0.01; weaker in family firms (−0.151, p < 0.10). **A47**: digitalisation/automation requirements rise strongly; traditional role stays dominant. **A18**: "fluid role identity". **A33** (abs.): divisional roles narrower, group-level business roles broader. | Quant (surveys A7, A46; content analysis A47); qual (A9, A18, A33, A25, A34); reviews | **DS** for *change in competencies/responsibilities*. **MX** for *direction* (BP-ward) | Longitudinal observation of tasks actually performed; AI-specific evidence |
| **Q2** | Are analytical capabilities insufficient by themselves for control effectiveness? | A5, A26, A2, A41 (abs.); qualifying: A37, A19, A11, A27 | **A5**: all BAC → effectiveness paths are mediated by the BP role; full mediation for tangible resources (both outcomes) and for human skills → decision impact. **A26**: digitalisation has no direct effect on performance; effect runs through planning/budgeting performance. **A2**: automation not associated with effectiveness (b = −0.003); automation × analytics negative (b = −0.222, p < 0.01). **A41** (abs.): DA improves effectiveness "by the way it is used". *Qualifying*: **A37** digitalisation → MCE directly (β = 0.321); **A19** IS quality → MCE (β = 0.549); **A2** analytics use → effectiveness (b = 0.465, p < 0.01). | Quant (cross-sectional), one abstract | **MX** (leaning IS). "Not alone" is supported; "insufficient to guarantee" is not tested by anyone | A design that tests complementarity, not only mediation. Evidence on *AI* analytics |
| **Q3** | Does the BP role mediate analytics capability → controllership effectiveness? | **A5** | PLS-SEM, 322 large German firms: all BAC dimensions → output quality and decision impact are positively mediated by the BP role. Full mediation for tangible → both outcomes and human skills → decision impact. The scorekeeper role has no significant mediating effect. | Quant, cross-sectional, perceptual | **DS** (single study) | Replication; coefficients (absent from sheet); causal ordering (see §6.3); measures of *what the BP does*; non-German, non-large, AI contexts |
| **Q4** | Is BP positively associated with use of analytical tools? | **A2**; adjacent A46, A47 | **A2**: BP objective and digitalisation strategy have "positive but independent effects on the use of analytics" (interaction b = −0.015, ns). **A47**: digitalisation positively associated with BP tasks (β = 0.157, p < 0.01), "without establishing causality". **A46**: MAIS sophistication → involvement in strategy. | Quant cross-sectional; content analysis | **DS** (A2: association); **direction unresolved** | Temporal order. A2 has BP *objective* → analytics, while A5/A46 have analytics → BP. Measures of BP *practice* rather than objective |
| **Q5** | Do controllers interpret, contextualise and challenge analytical information? | A34, A1, A22, A32, A28; weaker: A8 (abs.), A50, A45, A21 | **A34**: controllers who master Big Data "give sense to data, reflect on business opportunities, challenge operational units and top management"; otherwise they become "retechnicised". **A1**: data does not make relevance. Relevance is produced and arbitrated; controllers "mainly retain a sense-making and legitimation role". **A22**: MA support for non-routine decisions is "maieutic" (questioning, debating); AI is not expected to deliver perfect answers; results should not be accepted on "autopilot". **A32** (n = 35, descriptive): controller expected to turn accounting language into clear information for management. **A35** (abs.): over-reliance on the IT system can limit professional judgement (counter-evidence). | Qual (A34, A1, A22); descriptive quant (A32); abstracts | **DS** for digital/analytical information. **IS** for *AI-generated* output | Observed interaction with AI outputs; who challenges and with what effect |
| **Q6** | Can BP activities be linked to organisational sensing? | A34, A1, A22 (interpretive activities); A12 (sensing construct, no BP); A38 | A34: controllers "spot business opportunities". A12 measures "digital sensing" (n = 415; interactive MCS use → DDCs, β = 0.355), but BP is not in the model. | Qual; quant on a different construct | **TI** (weak) | A study linking a BP/controller measure to a sensing measure |
| **Q7** | Can BP activities be linked to organisational seizing? | A5 (decision impact), A46, A9, A33 (abs.), A32 | A5: BP role mediates "controllership impact on management decisions". A46: controller strategic involvement (support role weaker than advisory role in family firms). A9: BP participates in strategic support and coordinates the digital transformation. | Quant (perceptual); qual | **IS** for *decision influence*. The label "seizing" is **TI** | Evidence of mobilisation, investment or commitment decisions shaped by BPs |
| **Q8** | Does BP *directly* contribute to transforming control arrangements? | Nearest: A25, A9, A18 | A25 (abs.): "organizational restructuring work" is one of six boundary-work strategies of finance professionals. A9: MC becomes "transversal, integrated", a "coordination node" (a statement about the MC function, not the control system). **Contradicting adjacent**: A7 (no significant effect of digitalisation on organisation of MC); A37 (centralisation path not supported). | Qual; abstracts | **ND** | Any case documenting a BP initiating or shaping changes to control rules, KPIs, rights or incentives |
| **Q9** | Do BPs identify interdependencies among control-package components? | None. Adjacent: A28, A1, A26, A37, A48 | A28: KPI scope widened to the whole product lifecycle, which "changes the definition of performance and even managers' responsibilities". Nobody in the matrix says who noticed this. A26: planning/budgeting performance carries the digitalisation effect. A37: digitalisation → standardisation (administrative) → information quality. | Qual/quant, none about BPs | **ND** | Observed cross-control reasoning by controllers |
| **Q10** | Coordinated reconfiguration across several control categories facilitated by BP? | None. Adjacent: A48, A9, A4 (abs.), A12 | A48: iterative DAL-DT loop applied to incentives, capital budgeting and workforce planning; "obstacles: leader reluctance, misunderstanding, resources". The controller's role is not reported. A12/A39: levers tested separately. | Qual case; surveys | **ND** | Package-level reconfiguration evidence; BP participation |
| **Q11** | Does BP help recognise or address IPC–IPR misalignment? | Components only: A34, A2, A27, A29; frame A2, A26, A37 | A34: the data-handling load crowds out advice (strongest at intermediate maturity). A2: joint automation × analytics lowers effectiveness ("might be a result of resource constraints"). A27: higher data volume is negatively associated with counter-measure effectiveness. | Mixed | **TI** (weak). BP participation itself is **ND**. In A34 the BP role is *displaced* by the tension | Study that names a mismatch and shows who detects/addresses it |
| **Q12** | Does BP take part in repeated adaptation when reconfiguration creates new informational requirements? | None. Adjacent: A48, A49, A18 | A48: iterative loop; A49: PMS evolve along the servitisation journey; A18: continuous micro role transitions (2014–2023). | Longitudinal qual | **ND** for BP. **IS** for the existence of recursion | Longitudinal case that traces the second-order effect and the controller's part in it |

**Summary.** Q1, Q3, Q4, Q5 are documented (though Q1's direction is mixed). Q2, Q7, Q6, Q11 are partial or inferential. **Q8, Q9, Q10, Q12 have no support in the matrix.**

---

## 3. Mapping BP activity onto Teece (2007)

Level caution: Teece's capabilities are organisational and routine-based. The BP role is an individual or functional practice (A5 measures it at MC-department level). BP is at most a **candidate microfoundation or contributing practice**, not a dynamic capability.

| Dynamic capability | BP activity | Supporting studies | Direct evidence | Theoretical interpretation | Limitations | Verdict |
|---|---|---|---|---|---|---|
| **Sensing** | Making sense of data; spotting opportunities; questioning results; local–global translation of KPIs | A34, A1, A22, A28, A32; construct: A12 | A34 and A1 (qual) show interpretation and challenge. A12 measures sensing but without BP | BP interpretation may feed the *filtering and interpreting* part of sensing | No study links BP to a sensing measure. A34's "opportunity spotting" is individual-level; Teece's sensing is organisation-level scanning and learning. A1: controllers "mainly keep a sense-making role" | **Defensible as a qualified contribution**, framed as proposition |
| **Seizing** | Turning information into decision input; participating in strategy; framing options | A5, A46, A9, A33 (abs.) | A5: BP role → impact on management decisions (mediation). A46: involvement in strategy β = 0.467 | Decision influence is a plausible ingredient of seizing | Seizing also covers mobilising resources, commitment and investment, which no study shows BPs doing. Self-reported effectiveness. A47: BP discourse is not rising. A46: weaker in family firms | **Defensible only for "decision influence"**. Do not claim seizing |
| **Transforming** | Restructuring work; coordination across functions; changing routines/decision rights | A25 (abs.), A9, A18 | None. A7 and A37 report null effects on organisational dimensions | Would require BP → routine/decision-right change | No BP-attributed change in any control. A25 concerns the profession's boundaries, not the control system | **Speculative: exclude as a claim** from 4.4. Keep as research agenda |
| *(Aggregate check)* | MCS use → DDCs | A12 (n = 415) | Interactive MCS use β = 0.355; belief systems β = 0.279; DDC → DTS β = 0.789; moderations not supported (belief × DDC β = −0.393) | The only empirical MCS–sensing/seizing/transforming link in the corpus | **No BP involved.** The antecedent is interactive/belief-system *use*, not a translator role | Use as the bridge to §4.5, and separately from BP |

---

## 4. Cross-control translation: what the corpus does and does not show

Controls classified with Malmi & Brown (2008), by my reading of each row. The authors do not use this typology, and Simons' levers do not map one-to-one onto it.

| Control type | Studies with findings | What is documented |
|---|---|---|
| Planning | A26, A27, A3, A7, A32 | Digital planning/budgeting tools improve planning performance (A26). Forecast digital maturity helps in a crisis (A27) |
| Cybernetic | A29, A28, A49, A4 (abs.), A37 | KPI platforms and BI; KPI overload (A29); a common KPI language (A28); PMS evolution (A49) |
| Reward / compensation | **A48 only** | DAL-DT used to design and adjust incentives |
| Administrative | A37, A9, A7, A40, A18, A30 | Standardisation (A37 indirect β = 0.255); centralisation path not supported; MC organisation becomes more transversal (A9); full ERP integration reduces the controller's contribution (85% vs 31% of coded references, A40) |
| Cultural | A1, A12, A39, A4 (abs.), A48 | Epistemic cultures (A1); belief systems → DDCs (A12) and digital innovation (A39) |

| Required distinction | Evidence in the matrix |
|---|---|
| **Change within a single control** | Abundant: A26, A27, A29, A28, A3, A49, A48, A7 |
| **Relationships between controls** | Present, but not about BPs: A37 (digitalisation → administrative design → effectiveness; one path unsupported); A28 (KPI scope → managers' responsibilities); A1 (epistemic cultures ↔ analytic machineries); A12/A39 (levers have different effects) |
| **Actual package reconfiguration** | **None demonstrated.** A48, A9 and A4 (abs.) describe several control areas changing in one organisation, without a reconfiguration mechanism or a package analysis |
| **BP participation in cross-control coordination** | **None.** Nearest: A8 (abs.: controller "orchestrates a co-authoring process" among managers), A9 (controller as coordination node), A25 (bridging) |

**Chain test.**

| Link | Status |
|---|---|
| AI-induced informational tension | Partly: tensions exist (A34, A2, A27, A29, A1), not AI-specific, not IPC/IPR-labelled |
| → BP interpretation | **Supported** (qual: A34, A1, A22, A32; quant mediation A5) |
| → recognition of cross-control interdependencies | **Not documented** |
| → organisational response | Documented for *professional* responses (A25) and organisation-level measures (A9), not BP-attributed |
| → potential package reconfiguration | Conceptual only |

I do not infer cross-control coordination from the fact that A9, A12, A48 or A28 discuss several control categories.

---

## 5. Comparison with the established literature

| Source | Already known | Not established | What the article could extend | Classification of extension |
|---|---|---|---|---|
| **Elo et al. (2026) [A47]** | Digitalisation and automation requirements rise strongly (H2); sustainability requirements rise (H3); traditional role dominates; **BP requirements do not significantly rise (H1 rejected)**; digitalisation–BP tasks β = 0.157, p < 0.01, not causal. Layering, not substitution | What controllers *do* (job ads show demanded discourse, not enacted practice); outcomes; AI; mechanisms | Use as a boundary condition: BP is not the default destination of the role | **Not a source for the mechanism.** The extension is contextual |
| **Boerner et al. (2025) [A5]** | BAC → effectiveness runs through the BP role; the scorekeeper does not mediate | The content of the BP role; causality; AI; any organisational change; interplay with other controls; non-large or non-German firms | Say what "the BP role" does (H2), then what it does across controls (H3) | H2 is a **reformulation/contextual re-description** of A5's black box. H3 would be a **new mechanism**, but is untested |
| **Bedford et al. (2025) [A2]** | BP objective associated with analytics use (independent of digitalisation strategy); analytics → effectiveness (b = 0.465); automation null; automation × analytics negative. Uses the information-processing view | BP's conversion role; mechanism; AI. **Order**: BP → analytics, the reverse of A5 | The negative joint effect is the clearest corpus signal of capacity strain (IPC-like) | **Contextual**. The information-processing framing is not original (A2, A26, A37 already use it) |
| **Andreassen (2020) [A33, inferred]** | Roles polarise: divisional narrower; group-level business roles broader; jurisdictional competition; decision makers' expectations shift | Information-processing tensions; control packages; AI | BP translation is likely stratified by level; relevant to "who translates" | **Contextual** |
| **Järvenpää et al. (2023) [unmapped]** | Per your brief: information filtering, interpretation and sense-giving. Cannot be verified from the matrix | — | If it documents sense-giving by MAs, it is the closest precedent for H2 | Unknown. Do not claim novelty over it until verified |
| **Teece (2007)** | (Not in the matrix) Organisation-level microfoundations of sensing, seizing, transforming. A12 operationalises the triad empirically | Whether a controller-level practice is a microfoundation | Position BP as a candidate contributing practice | **Contextual application** |
| **Malmi & Brown (2008)** | (Not in the matrix; cited in A9) Controls form a package of five types | How packages reconfigure under digital or AI change; who coordinates | Cross-control interdependence under informational change | **Potentially a new mechanism if specified. Presently a contextual application.** Theoretical integration alone is not originality |

**Closest prior framing for your chain: A37 (Gimpl et al. 2026).** It applies OIPT to digitalisation, information quality and control effectiveness, with two organisational-design mediators (standardisation, centralisation). It already finds that design consequences are not automatic (centralisation path not supported). Your contribution sits on top of it (adding dynamic capabilities and a translator), not in the IPT lens.

---

## 6. The theoretical gap

### 6.1 H1, H2, H3 compared

| | H1 Analytical translation | H2 Organisational translation | H3 Cross-control translation |
|---|---|---|---|
| Claim | BP translates analytical capability into decision-relevant information | BP translates information-processing tensions into organisationally actionable responses | BP identifies and coordinates the consequences of informational change across interdependent controls |
| Best evidence | A5 (mediation), A2, A46, A32, A34, A9 | A25 (responses), A9, A18, A1, A22 (partial) | None directly. Adjacent: A28, A37, A48, A8 |
| Strength | **Best supported** (quant + qual), with caveats | **Partly supported** (interpretation yes; organisational response not BP-attributed) | **Not supported; theoretical only** |

**Verdict: H1 is the best supported.** H3 is not favoured merely because it is more original.

### 6.2 Assumptions required to move between hypotheses

**H1 → H2**
1. The mediation in A5 is produced by interpretive activity (the matrix reports mediation of a role, not activities).
2. Interpretation is passed to decision makers who act on it (A5's "impact on decisions" is perceived, not an organisational response).
3. The relevant tensions are informational (IPC–IPR) and not professional, epistemic or role tensions (see §0.5).
4. The BP role exists where tensions arise. A47, A34, A35, A40 suggest the BP role may be displaced exactly then.

**H2 → H3**
1. Responses involve more than one control type.
2. Controllers know the other controls well enough to see interdependencies.
3. They communicate them and are listened to (decision rights, hierarchy).
4. The interdependencies are the *consequence* of informational change, not of design or politics.
5. Reconfiguration happens at package level rather than piecemeal.

None of these five is documented in the matrix.

### 6.3 Ordering ambiguity (a likely reviewer objection)
- A5: capability → BP role → effectiveness.
- A2: BP objective → analytics use.
- A46: MAIS sophistication → involvement.
- A47: digitalisation ~ BP tasks.

The BP role is variously an antecedent, a mediator and an outcome. Cross-sectional designs cannot settle this, so "BP *translates*" is one of several readings.

### 6.4 Rival explanations
- **Senior managers**: A1 (data-driven shift started as a narrative; controllers keep sense-making), A17 (top management is a main driver), A40 (top-down policies, family management), A48 (leader reluctance), A9 (no roadmap). A7 found strategic leadership **not** significant for the digitalisation of MC.
- **IT specialists and data analysts**: A38 (power shifts to whoever masters technology), A33 and A25 (jurisdictional competition), A18 (IT/data specialist roles), A35 and A40 (the system defines the role).
- **Cross-functional / agile teams**: A18, A25, A9, A30.
- **System design**: A28 (platform design), A40 (ERP integration), A19 (IS quality).
- **Institutional/regulatory pressure**: A45, A42, A18.

---

## 7. Diagnostic table

| Theoretical claim | Evidence strength | Originality relative to reviewed studies | Reviewer objection | Recommended treatment |
|---|---|---|---|---|
| C1 Digitalisation changes MA competencies and responsibilities (layering) | Strong, converging (A47, A7, A9, A18, A46, A30) | None (known) | Direction is mixed (A47, A34, A40) | **Retain as established finding** |
| C2 BAC → controllership effectiveness is mediated by the BP role | Moderate; single study (A5) | None (known) | One cross-sectional survey; no coefficients in the sheet; order ambiguity | **Retain as established finding**, with explicit qualification |
| C3 BP objective associated with analytics use (A2) | Moderate; single study | None | Reverse order vs A5 | **Retain, qualified** |
| C4 Analytical capability alone is insufficient | Mixed (A5, A26, A2 vs A37, A19) | Low | "Insufficient" is untested; several direct effects reported | **Retain as qualified interpretation** ("depends on complements") |
| C5 Controllers interpret, contextualise and challenge information | Moderate, qualitative (A34, A1, A22, A32) | Low–moderate | Conditional on skills/maturity; not AI-specific | **Retain as qualified interpretation** |
| C6 H1: BP translates analytic capability into decision-relevant information | Moderate | Low (re-description of A5) | "Translation" is inferred from mediation | **Retain as qualified interpretation** |
| C7 BP orientation buffers role strain under digitalisation (A24) | Moderate; cross-sectional | None | Not a translation finding | Use as a boundary condition |
| C8 BP contributes to sensing | Weak; inferential | Moderate | No BP–sensing test; level mismatch | **Develop as theoretical proposition** |
| C9 BP contributes to seizing | Weak–moderate for decision influence only | Moderate | Seizing ≠ decision influence | **Qualified interpretation** for decision influence; proposition for "seizing" |
| C10 BP contributes to transforming | None | — | Overreach | **Move to research agenda** |
| C11 H2: BP translates IP tensions into organisational responses | Weak–moderate | Moderate | "Tension" equivocation; response not BP-attributed | **Develop as theoretical proposition** |
| C12 H3: BP identifies cross-control interdependencies | None | Potentially high | Entirely inferred; rivals unexamined | **Develop as a clearly labelled proposition (outside the empirical synthesis)**, or move to the research agenda |
| C13 BP facilitates coordinated package reconfiguration | None | Potentially high | Unsupported | **Move to research agenda** |
| C14 BP participates in recursive adaptation | None for BP (recursion exists, A48, A49, A18) | Potentially high | Unsupported | **Move to research agenda** |
| C15 BP is a dynamic capability | None; level mismatch | — | Category error | **Remove** |
| C16 BP causes organisational change | None; all effect studies measure effectiveness, not change | — | Causal overreach | **Remove** |
| C17 Evidence is AI-specific | None for BP | — | Extrapolation from digitalisation/analytics | **Remove** as a claim; state the extrapolation |

**Studies that contradict or limit the proposed mechanism.**
- A47: BP requirements flat.
- A34: retechnicisation, strongest at intermediate maturity.
- A35 (abs.): IT-system dirty work clashes with the BP role.
- A40: full ERP integration shrinks the controller contribution.
- A46: family control weakens involvement.
- A33 (abs.): divisional roles narrow.
- A7: no effect on organisation of MC or on strategic instruments.
- A37: centralisation path unsupported.
- A12: moderation unsupported or negative.
- A26: no direct effect of digitalisation.
- A2: BP is independent of digitalisation strategy.

Several of these do not refute the mechanism. They bound it.

---

## 8. Recommended structure of Section 4.4

1. **What is established: BP as conditioning practice.** A5, A2, A46, A7, with the caveats of §6.3. Add layering (A47) and boundary conditions (A24, A34, A40, A33, A46-family). *Empirical synthesis.*
2. **Interpretive functions with direct support.** Interpretation, contextualisation, challenge (A34, A1, A22, A32, A28). State that the cases are digitalisation or Big Data, not AI, and that AI-specific evidence is mostly attitudinal or discursive (A22, A15, A45). *Empirical synthesis.*
3. **Relation to sensing and seizing.** Present as theoretical interpretation: BP as a candidate contributing practice (not a capability). Anchor on A12 for the aggregate link. Limit seizing to decision influence. *Theory development, clearly marked.*
4. **Transforming.** State that no study ties BP to altered routines or controls; cite A7 and A37 as cautionary nulls; leave A25 and A9 as nearest adjacent evidence. *Gap statement.*
5. **Cross-control translation as a bounded proposition.** Within-control vs between-control vs package vs BP participation (§4). Put the proposition in the theory section, with the five assumptions of §6.2 listed. *Theory development.*
6. **Transition to §4.5.** The conditioning role of BP, the IPC–IPR strain visible in A2, A34, A27, A29, and the A12 evidence that interactive MCS use is linked to dynamic capabilities all motivate the need to explain reconfiguration. Avoid claiming it has been demonstrated.

Do not repeat 4.3 content. I have not seen your 4.3 text, so please check for overlap on role transformation (Q1).

---

## 9. Revised passage (draft, JOCM register)

*Author-year is given only where the matrix names the source or the mapping is high-confidence; otherwise `[A#]` is a placeholder for the citation.*

> **4.4 The business partner as a translation mechanism**
>
> Digitalisation changes what is expected of management controllers, but the evidence points to accumulation rather than replacement. A longitudinal analysis of 7,426 Finnish controller job advertisements shows that traditional responsibilities remain dominant, that digitalisation and automation requirements rise strongly, and that business partner requirements do not increase significantly; digitalisation is positively associated with business partner tasks (β = 0.157, p < 0.01), though not in a way that establishes causality (Elo et al., 2026 [A47]). Qualitative studies describe similar broadening, from information provision to a more proactive advisory role, while stressing that the job is extended rather than replaced [A9, A18]. Business partnering therefore cannot be assumed to be the default outcome of digitalisation. Other studies point to re-technicisation at intermediate digital maturity [A34], to ERP integration absorbing controller tasks [A40], and to weaker strategic involvement under family control [A46].
>
> Within this variation, the business partner role appears to matter for whether analytical resources translate into effective controllership. Using survey data from 322 large German firms, Boerner et al. (2025) [A5] report that the relationships between business analytics capabilities and both controllership output quality and impact on management decisions are positively mediated by the business partner role. The mediation is full for tangible analytics resources and for human skills in relation to decision impact, and the scorekeeper role does not mediate. Bedford et al. (2025) [A2] find that a business partnering objective and a firm's digitalisation strategy are each positively associated with analytics use, and that analytics use is associated with finance function effectiveness (b = 0.465), whereas automation is not and the joint use of automation and analytics is negatively associated with effectiveness. Both studies are cross-sectional and rely on perceptual measures, and they imply different orderings of analytics and business partnering. They are therefore best read as evidence that business partnering and analytical capability are interdependent, rather than as proof that the business partner causes analytics to become effective.
>
> What the business partner actually does in this conversion is mostly addressed in qualitative work. Controllers who master data tools are described as giving sense to data, identifying business opportunities, and challenging operational units and top management [A34]. Relevance is described as produced and arbitrated through organisational devices rather than given by the data, with controllers retaining a sense-making and legitimation role [A1]. In non-routine decisions, accounting support is described as questioning and debate rather than the supply of answers, and practitioners expect AI to leave this intact provided results are scrutinised rather than accepted automatically [A22]. We use "translation" in this limited sense: interpreting, contextualising and challenging analytical output so that it becomes usable in decisions. These studies concern digitalisation, analytics and Big Data, not AI-generated information in particular, and they report that interpretive capacity depends on skills and on whether data work crowds out advisory work [A34, A35].
>
> From a dynamic capabilities perspective (Teece, 2007), these practices can be read as candidate micro-level contributions to the interpretation and filtering that organisational sensing requires and, through their effect on decision inputs, to seizing. We stress that this is an interpretation. The only study in our corpus that measures sensing, seizing and transforming links them to interactive control use and belief systems, not to business partnering [A12], and the business partner role is a functional practice, not an organisational capability. We find no study that links business partnering to changes in routines, decision rights or control arrangements, so we do not treat it as contributing to transforming. Evidence on organisational dimensions is also cautionary: digitalisation of management control shows no significant effect on its organisation or on strategic instruments [A7], and a decentralisation path is not supported [A37].
>
> A more specific question follows from viewing management controls as a package (Malmi & Brown, 2008). Studies document change within individual controls, such as planning and budgeting [A26], performance indicators [A28, A29] and incentives [A48], and some report relationships between controls, for example between digital tools, standardisation and information quality [A37], or between KPI scope and managerial responsibilities [A28]. None of them shows controllers identifying, communicating or coordinating such interdependencies, or a package being reconfigured with their participation. We therefore advance cross-control translation only as a theoretical proposition: that business partners, because they interpret information for decision makers across functions, are positioned to notice how informational change in one control bears on others. Its validity depends on assumptions that the reviewed evidence does not test, including that controllers understand the other controls, that their interpretations are heeded, and that senior managers, IT specialists and cross-functional teams do not perform this role instead [A1, A17, A25, A33, A38, A40].
>
> The business partner role may thus condition how far analytical capability becomes usable information, and may be one practice through which tensions in information processing become visible. Whether this carries through to the reconfiguration of the management control package is the question taken up in the next section, where we examine how misalignments between information-processing capacity and requirements may prompt such reconfiguration.

---

## 10. Reviewer assessment (anonymous, JOCM)

1. **Is 4.4 sufficiently supported by the corpus?** Only partly. The conditioning role of business partnering and the interpretive functions are supported. The chain to *transforming* and to *cross-control coordination* is not.
2. **Strongest argument.** The BP role mediates the link between analytic capability and controllership effectiveness (A5), complemented by A2 and A46 and by the qualitative descriptions of interpretation (A34, A1, A22).
3. **Currently speculative.** BP → recognition of cross-control interdependencies → coordinated package reconfiguration → recursive adaptation (Q8–Q10, Q12). Also BP → seizing or sensing as *organisational capabilities*.
4. **Differentiated from prior research?** Only conceptually. H1 is already known (A5). H2 re-describes A5's black box with partial qualitative support. H3 is the only element that would be new, and it is untested. The information-processing framing is not new (A2, A26, A37).
5. **Credible bridge to Teece?** Only a weak one. It works if BP is a candidate microfoundation or contributing practice and the claim stops at sensing/seizing contributions. It does not work if BP is a dynamic capability or contributes to transforming. The one corpus link between MCS and dynamic capabilities (A12) does not involve BP.
6. **Explains organisational change?** Not yet. All the effect studies measure effectiveness or performance, not change. The change evidence is about roles (A9, A18, A25, A33), and the control-level evidence is thin (A9, A28, A48, A49).
7. **Evidence needed for the weakest claim (cross-control translation):** a longitudinal, multi-case study of AI introduction that traces actual episodes in which a controller or BP flags a consequence of an informational change in one control for another (for instance a KPI change that affects incentives, decision rights or budget rules). It should show how the flag was communicated and negotiated, whether it altered more than one control, and whether comparable changes proceeded without a BP. Rival actors (CFO, IT, project teams) must be coded. A survey with Malmi & Brown package measures, BP-activity items and time-separated outcome measures would be a complementary quantitative route.

### Recommendation: **REVISE**

- **Theoretical coherence.** The core logic (AI → IPC/IPR → MCS package ↔ dynamic capabilities, BP as potential interpretive and coordinating mechanism) is coherent *if* BP stays a "potential mechanism". It becomes incoherent if BP is presented as a capability or as a cause of change.
- **Evidence quality.** One survey mediation (A5), one reverse-ordered association (A2), qualitative interpretation studies, and a longitudinal null on BP growth (A47). The matrix evidence is mostly cross-sectional and perceptual.
- **Originality.** Modest as it stands. H3 is potentially original, but it is a proposition, not a finding.
- **Relevance to organisational change.** Currently low. It improves if section 4.4 shifts from "effectiveness" to a clear account of what would change, in which controls, and who would notice.
- **Condition.** If the current Section 4.4 asserts BP → transforming or cross-control coordination as established, the verdict becomes **MAJOR RECONCEPTUALISATION** of those claims. I have not seen your existing 4.4 text; this verdict applies to the mechanism as described in your brief.

---

## Appendix: confirmations needed

1. Confirm the A-ID mapping for Boerner (A5), Bedford (A2), Elo (A47), Andreassen (A33).
2. Identify which row (if any) is Järvenpää et al. (2023).
3. Supply the existing Section 4.3 and 4.4 text so overlap and the verdict can be checked against it.
4. Provide full texts of A5, A2, A47 and A34 if you want findings verified beyond the matrix. I have not read any original article.
