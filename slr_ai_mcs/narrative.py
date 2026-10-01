# -*- coding: utf-8 -*-
"""Hand-written analytical layer. Every claim cites article IDs from the reading sheet."""

REL_READING = {
 "R1": "Established quantitatively in two samples (Vietnam, Europe); effect sizes differ widely (.814 vs .330). Qualitative support only for availability/speed (A9).",
 "R2": "No inferential test of predictive capability exists in the corpus. Evidence is interview-based (A9, A16) plus satisfaction with forecasting (A27) as a proxy. Predictive accuracy is never measured.",
 "R3": "Only one study models what drives automation (A2: strategy x efficiency objective). Qualitative studies describe automation as an effect rather than a variable to be explained.",
 "R4": "Consistent positive evidence in three surveys (A3, A26, A27) but outcomes are perceived satisfaction/performance, not forecast accuracy or budget quality.",
 "R5": "Positive in two surveys (A13 self-report; A37 SEM) and five qualitative/design studies. Effects are on perceived effectiveness. A2 shows the effect depends on WHICH technology (analytics yes, automation no).",
 "R6": "Contested. Positive in three surveys (A5, A7, A46) and several cases; flat in the only longitudinal behavioural study (A47: BP requirements do not rise) and negative/ambivalent in A34, A35, A40, A25. A47 appears on both sides: BP trend flat, but digital-BP association b=.157.",
 "R7": "Mixed. Direct positive effects are found when the outcome is managerial/MC effectiveness or perceived success (A11, A12, A23), not when it is firm performance (A26 direct null; A27 weak; A2 automation null, joint use negative).",
 "R8": "Best-replicated mechanism in the corpus (A19 b=.549; A37 b=.555), but only two studies and both use perceived effectiveness.",
 "R9": "One survey (A11, managerial effectiveness as proxy) and interview perceptions (A16). Decision quality is never measured directly.",
 "R10": "Not separable from R6: strategic involvement is how A46 and A7 operationalise the business-partner role, so it is not an independent outcome of that role. No study tests it as a consequence.",
 "R11": "One survey path (A5: BP role -> impact on management decisions) and three qualitative accounts of HOW controllers support decisions (A22, A8, A34). Mechanism remains a black box in the quantitative study.",
 "R12": "Purely qualitative (A22, A8, A34). Interactive use of MCS is measured quantitatively (A12, A39) but as managers' use of controls, not as controller-manager interaction.",
 "R13": "No study links the controller / business-partner role to firm performance. A5 stops at controllership effectiveness (coded under R11).",
 "R14": "Qualitative only (A22, A8). A12 and A28 give indirect support (interactive use -> digital sensing/seizing capability; flexible analysis leaves room for local interpretation).",
 "R15": "No study measures interpretation. A15 is the only causal test and it concerns AI explainability -> acceptance (n=164 online participants); A22 documents interpretation shaping decisions qualitatively.",
 "R16": "No evidence found. No study follows a managerial decision to an implemented organisational action.",
 "R17": "Only indirect: A12 (DDC incl. 'transforming' -> digital transformation success) and A49 (PMS evolution -> service value). No study measures organisational adaptation and then performance.",
 "R18": "Evidence is mixed and heterogeneous. Competence/self-efficacy/ease (A43, A15, A9) and strategy-function alignment (A2) matter; perceived usefulness (A43) and leadership/culture (A7) do not. Coercive pressure is qualitative only (A45).",
 "R19": "Quantitative: only A5 (human skills for BA -> controllership effectiveness via BP role). The rest is qualitative/indirect (A16, A18, A32, A34).",
 "R20": "Qualitative only (A9, A18, A28, A40, A45). No quantitative test of what conditions convert technology into organisational change.",
 "E1":  "Contradictory: automation raises effectiveness in A13 (self-report) but not in A2; A46 rejects time-saving as mechanism; A34 and A22 show how time released can be re-absorbed or learning lost.",
 "E2":  "Consistent but thin: A27 (survey), A2 (negative joint effect), A29 (design science). Selection of relevance is never studied as a mechanism.",
 "E3":  "Reverse arrow relative to the chain. MCS use predicts digital capability/innovation (A12, A39). A41 (abstract) points the same way.",
 "E4":  "Standardisation is the best-tested organisational channel (A37 indirect b=.255) and is echoed qualitatively (A4, A9, A28).",
 "E5":  "No average effect on role strain (A24) but a strong conditional one; qualitative studies describe identity work and boundary strategies (A18, A25, A35).",
 "E6":  "Qualitative only. This is the empirical entry point for the 'sensemaking' argument: digital data create a demand for interpretation and contextualisation that is documented but never measured.",
 "E7":  "A single survey (A2). If replicated, it would invert the assumed causal order (BP orientation precedes analytics use).",
 "E8":  "Three surveys (A3, A23, A26): MA/MC practice quality carries or adds to technology effects.",
 "E9":  "Tasks and instruments change in survey data (A7, A14, A23, A47), but strategic instruments do not (A7) and traditional tools remain most important (A32).",
 "E10": "Quantitative nulls (A7 ORG; A37 centralisation) contradict qualitative reports of integration/centralisation (A9, A18, A40).",
 "E11": "Single study (A27) and it bypasses the decision node.",
 "E12": "Single supplementary analysis (A46).",
 "E13": "Moderation is inconsistently supported: clear in A24 and in A2 (efficiency objective); marginal in A19 and A46 (p<.10); null or reversed in A3, A12, A15 and in A2 (BP objective).",
}

PUZZLES = [
 ("P1. Digitalisation improves information but not (always) performance",
  "A11, A37, A19 (information/effectiveness up); A26, A2, A27 (performance null, conditional or weak); A38 (review names the gap)",
  "Information quality rises strongly with digitalisation (A11 b=.814; A37 b=.330) and predicts effectiveness (A11 b=.624; A37 b=.555). When firm performance is the outcome the picture changes: A26 finds no direct effect (only via planning), A2 finds none for automation and a negative joint effect, A27 finds weak, specification-dependent effects. Direct positive effects (A11, A23, A12) use managerial effectiveness or perceived success as outcome.",
  "Why effectiveness rises while financial performance does not; whether the gap is measurement (perceived vs financial), time (A27 observed a short window, H1 2020), or organisational (A26: embedding required). No study traces information -> use -> action -> result."),
 ("P2. Automation reduces workload but does not improve effectiveness",
  "A2, A46 (quant nulls); A9, A16 (workload released); A34, A22 (re-absorption, loss of learning); A13 and A19 (opposite results)",
  "Interviews report time released for analysis (A9, A16). The only survey test finds no effect of automation on effectiveness (A2 b=-.003) and a negative joint effect with analytics (b=-.222). A46 finds controller involvement rises with data quality, not with time saved. A34 shows time re-absorbed by data harmonisation. A13 reports automation as the strongest predictor (self-report, single source) and A19 a marginal positive moderation (p<.10).",
  "Where released time goes and whether it becomes analysis or advice (A9 asserts, A34 contests); A2's resource-constraint explanation is untested; no threshold or maturity condition is modelled."),
 ("P3. More data produces lower satisfaction or poorer action",
  "A27, A29, A2; A1, A28 (relevance and meaning are constructed)",
  "Higher volume of forecast inputs and KPIs lowers forecast satisfaction and counter-measure effectiveness (A27, with controls). KPI overload swamps analysts, and AI is used to filter alarms (A29). Joint use of automation and analytics lowers effectiveness (A2). Relevance has to be produced and arbitrated (A1).",
  "Who or what selects relevance (controller, algorithm, manager); whether AI filtering relocates rather than removes the problem; no study tests focus/selection as a mediator."),
 ("P4. Technology adoption rises but controller involvement does not",
  "A47, A34, A40, A35, A24 (null/ambivalent) vs A7, A46, A5, A9 (positive)",
  "Positive results rest on self-reported tasks (A7), involvement (A46) or perceived mediated effectiveness (A5). The only longitudinal behavioural study finds digital and ESG requirements rising while business-partner requirements stay flat (A47), although the two co-occur (b=.157). Qualitative cases show substitution by integrated ERP (A40: 85% vs 31% of coded references) and re-technicisation at intermediate maturity (A34).",
  "Whether the contradiction is measurement (job ads vs perceived tasks), time, or contingency (maturity, ownership, role orientation); no study follows the same controllers over a digital change."),
 ("P5. Business-partner activity improves decision support but the mechanism is not explained",
  "A5, A46, A2; A22, A34, A8, A32",
  "The BP role fully or partly mediates BA capabilities -> controllership effectiveness while the scorekeeper role does not (A5). Qualitative studies show BP controllers questioning and challenging managers, giving sense to data and orchestrating co-authoring (A22, A34, A8). A46: data quality, not time, drives involvement. A2: BP objective raises analytics use (reverse order).",
  "What BP activity consists of (A5 measures role intensity, not activities); whether decision impact arises from access, dialogue or interpretation; the causal order between analytics and BP orientation."),
 ("P6. Information quality improves, but organisational use depends on managerial interaction",
  "A11, A37, A19 vs A22, A28, A1, A8, A40; A41 and A12 (interactive use)",
  "Information quality is the strongest quantitative predictor of effectiveness (A37 b=.555). Qualitative studies show that numbers acquire meaning only in discussion (A22, A28), that relevance is contested (A1) and that use depends on acceptance (A40: acceptance -> 83% high use; resistance -> 91% limited use). A41 (abstract) says effectiveness depends on mode of use.",
  "No quantitative test of information quality x interaction, or of interaction as mediator. Interactive use (Simons) is measured as managers' use of controls (A12, A39), not controller-manager dialogue."),
 ("P7. Digital tools are implemented but organisational change is limited",
  "A7, A37, A32, A47, A1 (limited change) vs A9, A18, A40, A28 (change described)",
  "Surveys find no effect on MC organisation or strategic instruments (A7) and no shift in centralisation (A37); traditional tools and the traditional role persist (A32, A47); two epistemic cultures coexist (A1). Cases describe cross-functional integration (A9), role recomposition (A18), redefinition of performance (A28).",
  "Whether change is layering rather than replacement; why the same technology yields different organisational outcomes (A40: integration level and acceptance matter); implementation processes are never measured quantitatively."),
 ("P8. MCS practices mediate technology effects, so technology alone is insufficient",
  "A26, A23, A37, A11, A5, A3, A12, A41",
  "Seven studies test mediators and use eight different ones: planning performance (A26), MAS development (A23), standardisation, central locus of information and information quality (A37), information quality (A11), BP role (A5), satisfaction (A3), digital dynamic capabilities (A12). Only information quality recurs (A11, A37). A26 finds no direct effect; A23, A11, A37 find both direct and indirect effects.",
  "What makes a practice a conduit; whether the mediators are alternative channels or one process measured differently; no head-to-head test."),
 ("P9. Causal direction between digital capability and MCS / controller orientation is unsettled",
  "A12, A39, A41 (MCS -> digital); A2 (BP objective -> analytics); A24 (orientation as moderator)",
  "Interactive use (b=.355) and beliefs (b=.279) predict digital dynamic capabilities (A12); levers of control predict digital innovation (A39; R2=.607). A BP objective raises analytics use independently (A2).",
  "Reciprocity and co-evolution; cross-sectional designs cannot order the variables."),
 ("P10. Enabling conditions work as main effects, rarely as moderators, and top-management / culture evidence conflicts",
  "A3, A12, A15, A2-H1b (moderation null/reversed); A7 (leadership, innovation, trust culture null); A17 (top management is a main driver, abstract); A40 (top-down structures limit); A19, A46 (marginal); A24, A2-H1a (clear)",
  "Contingency variables have direct effects in A3 but none of the moderations holds; beliefs moderate negatively in A12; decision type does not moderate in A15. Leadership and culture are null for digitalisation in A7 but central in A17 and A40. Competence is the only condition that is consistently positive (A7, A43, A5, plus qualitative A9, A16, A40, A45).",
  "Which conditions act at which stage (adoption vs effect); why contingency logic fails statistically while qualitative work finds contextual dependence."),
 ("P11. Adoption is not driven by perceived usefulness",
  "A43; A15; A45",
  "SME intention to adopt rests on self-efficacy (b=.349) and ease of use (b=.231), not on perceived usefulness (b=.183, p=.065) (A43). Transparency increases acceptance (A15). Coercive and normative pressure shape bounded adoption (A45).",
  "Whether adoption drivers are the same as effectiveness drivers; TAM-based studies measure intention, not use or outcome."),
 ("P12. Digitalisation helps business-partner-oriented accountants and strains watchdog-oriented ones",
  "A24; A35; A18",
  "No average effect on role conflict or ambiguity, but a robust interaction: watchdog orientation amplifies strain, BP orientation buffers it (A24). The ERP creates dirty work that clashes with the BP role (A35). Fluid identity and upskilling support adaptation (A18).",
  "Who performs the watchdog / control-integrity function in an AI environment; what exactly buffers strain (skills, identity, role clarity)."),
]

MECH = [
 ("M1. Interpretation / sensemaking (contextualisation of data)",
  "P1, P3, P5, P6, P8: information improves but outcomes need something between information and action; relevance and meaning are constructed.",
  "None. No study measures sensemaking or interpretation. Closest: A15 (AI understandability -> acceptance, F=15.54).",
  "A5 (BP role mediates, content unspecified); A46 (data quality, not time, drives involvement); A41 (abstract: mode of use); A32 (controller as interpreter, descriptive, n=35); A12 (interactive use -> digital sensing).",
  "A1, A22, A28, A34, A8, A35 (+A45 interpretive skills). Six studies, all qualitative.",
  "Yes. Documented qualitatively, never operationalised or tested."),
 ("M2. Controller-manager interaction / managerial dialogue",
  "P5, P6: BP activity helps decisions; use of information depends on interaction.",
  "Interactive use of MCS (A12 b=.355; A39 b=.281) - an antecedent of digital capability, not a mediator and not controller-manager dialogue.",
  "A41 (abstract) mode of use; A24 (role orientation conditions strain).",
  "A22 (debate, questioning), A8 (co-authoring), A28 (reviews), A34 (challenging managers), A1.",
  "Yes. Interaction as mediator between controller role and decision is untested."),
 ("M3. Controller involvement / business partnering as transmission",
  "P4, P5, P2: technology reaches decisions through the controller; but BP does not trend up (A47).",
  "A5 (mediation, 6 paths, n=322); A46 (b=.467); A7 (strategic tasks).",
  "A2 (BP objective -> analytics); A24 (BP orientation buffers strain).",
  "A9, A34, A18, A16, A8, A25.",
  "Partly tested once (A5). Boundary conditions and content of the role untested; contradicted by A47, A34, A40."),
 ("M4. Organisational translation: embedding technology in planning / standardised processes",
  "P1, P7, P8: technology effects pass through MCS practices; structure does not change.",
  "A26 (planning mediation, no direct effect); A37 (standardisation, indirect b=.255); A23 (MAS development).",
  "A12 (digital 'transforming' capability, b=.789); A14 (adoption of modern methods).",
  "A28, A9 (levers), A40 (integration, acceptance), A45 (policy translation), A4, A18.",
  "Partly. Embedding is tested as a statistical mediator; implementation processes are not."),
 ("M5. Competence / analytical capability to use the technology",
  "P2, P4, P10, P11: competence is the only condition that is consistently positive.",
  "A7 (b sig.), A43 (self-efficacy b=.349), A5 (human skills).",
  "A15 (AI skills, exploratory); A32 (expertise main success factor, descriptive).",
  "A9, A16, A34, A40, A45, A18.",
  "Partly. Tested as antecedent, rarely as the channel through which tools become decision support."),
 ("M6. Attention / relevance selection (overload management)",
  "P3, P2: more data worsens outcomes; joint automation-analytics lowers effectiveness.",
  "A27 (data volume negative, with controls).",
  "A2 (negative joint effect; authors suggest resource constraints).",
  "A29 (KPI overload and AI filter), A1 (relevance), A28.",
  "Yes. Selection is inferred, not measured."),
 ("M7. Role identity and boundary work",
  "P4, P9, P12: roles re-compose rather than shift to BP.",
  "A24 (orientation x digitalisation -> strain).",
  "A47 (layering of responsibilities).",
  "A18, A25, A35 (A38 review: horizontal power struggles).",
  "Yes as a mediator of technology effects on controller contribution."),
 ("M8. Strategy-function alignment (goal alignment)",
  "P9: objectives precede and shape tool use.",
  "A2 (strategy x efficiency objective -> automation b=.148; BP objective -> analytics).",
  "A12 and A39 (control use shapes digital capability).",
  "A9 (vision, roadmap as lever).",
  "Yes. Single survey; direction untested."),
 ("M9. Organisational learning (thin; do not adopt yet)",
  "P1, P2, P7 could be time-lag or learning effects, but the corpus offers little.",
  "None.",
  "A27 (short crisis window, weak performance effect).",
  "A22 (learning lost if automated), A18 (adaptation), A4.",
  "Evidence is too thin to justify introducing it from this corpus."),
]

CHAIN = [
 ("1. Digital capabilities -> Informational capacity",
  "A + C + F",
  "A11, A37 (A); A9, A16, A29 (C); A27, A29, A2, A34 (F)",
  "Digitalisation raises information quality in two surveys (A11 b=.814; A37 b=.330). Interviews report speed, depth, better forecasts. Against: data volume lowers satisfaction (A27), KPI overload (A29), data-harmonisation burden (A34).",
  "Predictive capability and timeliness are never measured. 'Informational capacity' is measured as perceived quality; overload and quality are not modelled together."),
 ("2. Informational capacity -> Controller / business partner",
  "B + C + F",
  "A5, A46, A7 (B); A9, A18, A8 (C); A47, A34, A40, A35, A24 (F)",
  "Analytics/IS sophistication is associated with BP role and strategic involvement (A5; A46 b=.467; A7). A46's supplementary test points to data quality rather than time saved. Against: BP requirements flat (A47), re-technicisation (A34), ERP substitution (A40), dirty work (A35).",
  "Informational capacity is not an explicit mediator (only A46's supplementary analysis). The arrow is tested from technology capability, not from information quality to role. Longitudinal data (A47) contradict cross-sectional data."),
 ("3. Controller / BP -> Interaction",
  "C (E for quantitative)",
  "A22, A8, A34, A1 (C); A32 (descriptive)",
  "Cases show controllers questioning and challenging managers, orchestrating co-authoring, giving sense to data.",
  "No quantitative measure of controller-manager interaction. A12 and A39 measure interactive use of controls, which is a different construct."),
 ("4. Interaction -> Interpretation / sensemaking",
  "C (+ indirect B proxy)",
  "A22, A28, A8, A1 (C); A12 (indirect B)",
  "Meaning of numbers depends on use and local interpretation (A28); deliberation produces learning (A22). A12: interactive use raises digital sensing/seizing/transforming capability (b=.355).",
  "Interpretation is not measured anywhere. A12 concerns organisational capability, not interpretation of information."),
 ("5. Interpretation -> Managerial decision",
  "A (narrow proxy) + C",
  "A15 (A); A22, A45, A34 (C)",
  "A15: more understandable AI reasoning raises acceptance of AI recommendations (F=15.54), regardless of decision type. Qualitatively, interpretation and professional judgement shape decisions (A22, A45).",
  "A15 tests explainability of an algorithm with online participants, not controllers' interpretation of accounting information; acceptance is not decision quality."),
 ("6. Managerial decision -> Organisational action",
  "E (B for bypass)",
  "A27 (bypass: digital maturity -> counter-measure effectiveness); A28 (qual, resource allocation)",
  "No study follows a decision to an action. A27 links digitalised forecasting directly to counter-measure effectiveness without a decision node.",
  "The node 'organisational action' is operationalised only in A27. Nothing on implementation of decisions."),
 ("7. Organisational action -> Performance",
  "B + F",
  "A26, A27, A12 (B); A26, A2, A27 (F)",
  "Planning/budgeting performance mediates digitalisation -> corporate performance (A26); counter-measure effectiveness is linked to digital maturity (A27); DDC -> success (A12 b=.789). Direct digital -> performance is null in A26, weak in A27, and absent for automation in A2.",
  "'Action' is proxied by practice quality (planning performance) or by perceived success. No measure of what was done as a result of a decision."),
]

FRAGMENT_TEXT = """
**Verdict: the literature is fragmented. The chain is a plausible narrative assembled from non-overlapping studies, not an empirically established sequence.**

Evidence for fragmentation (all computed from the reading sheet):

1. **No study covers the chain.** The longest tested sub-chains have three to four nodes: A37 (digitalisation -> standardisation -> information quality -> MC effectiveness), A5 (BA capabilities -> BP role -> controllership effectiveness), A11 (digital -> information quality -> managerial effectiveness), A26 (digital -> planning performance -> performance), A23 (technology -> MAS -> performance), A12 (control use -> digital capability -> success; reverse order). No quantitative study includes interaction or interpretation between the controller and the decision.
2. **Mediators do not replicate.** Seven quantitative studies test a mediator (A3, A5, A11, A12, A23, A26, A37); they use eight different mediators (planning performance, MAS development, standardisation, central locus of information, information quality, BP role, satisfaction, digital dynamic capabilities). Only information quality recurs (A11, A37).
3. **The chain's middle is qualitative.** Arrows 3, 4 and part of 5 rest on qualitative studies (A22, A8, A28, A34, A1). Arrows 6 and 7-as-specified have no direct evidence.
4. **Outcomes are not comparable.** At least eight outcome constructs are used: managerial effectiveness (A11), MC effectiveness (A19, A37), finance-function effectiveness (A2), controllership effectiveness (A5), corporate performance (A26), digital transformation success (A12), counter-measure effectiveness (A27), budgeting benefits (A3). Almost all are perceptual self-reports.
5. **Quantitative and qualitative strands rarely share constructs.** Surveys test technology -> information/practice -> effectiveness; cases explain roles, meaning and organisational response. Only A5/A46 (quant) and A34/A22 (qual) meet on the controller as intermediary, and they do not measure the same thing.
6. **Narrow empirical base.** Six of 22 quantitative or mixed studies draw on German or DACH samples (A5, A7, A19, A26, A27, A46). One experiment (A15) and one longitudinal behavioural study (A47) are the only designs that are not cross-sectional self-reports. AI-specific measures are rare: most surveys measure 'digitalisation' broadly.
7. **Arrows pointing the other way exist.** MCS use predicts digital capability (A12, A39) and a BP objective predicts analytics use (A2).

What would count as chain evidence is a study that measures digital capability, information quality, controller-manager interaction, interpretation and a decision/action outcome in the same sample. None exists in these 50 rows.
"""

# ------------------------------------------------------------------ block syntheses
SYNTH = OrderedDictLike = [
 ("SENSING / DIGITAL CAPABILITIES", """
**Strongest empirical findings**
- Digitalisation raises information quality: A11 (b=.814), A37 (b=.330). Information/IS quality raises MC effectiveness: A19 (b=.549), A37 (b=.555).
- Digitalisation of the control function raises MC effectiveness directly (A37, b=.321); analytics raises finance-function effectiveness (A2, b=.465); all five digital dimensions improve the MC function in A13 (self-report).
- Digital tools raise satisfaction with budgeting (A3), forecasting (A27) and, via planning, performance (A26).
- Predictive capacity improves qualitatively (A9, A16); not tested.

**Strongest articles:** A37 (n=246, four mechanisms), A2 (separates automation from analytics), A11, A19, A26, A5.

**Contradictions**
- Automation: no effect and a negative joint effect with analytics (A2) vs strongest predictor (A13) vs marginal moderation (A19).
- Direct performance effect: null (A26), weak (A27) vs positive (A11, A12, A23).
- Data volume lowers satisfaction/effectiveness (A27); KPI overload (A29); data-harmonisation burden (A34).

**Missing links:** predictive accuracy is never measured; AI-specific effects are rarely isolated (A15 experiment, A29 design science, A16 interviews, A22); the 'Sensing' column is coded 1 in 86 of 99 findings only because digitalisation is the corpus's selection criterion - it does not discriminate between studies.
"""),
 ("SENSEMAKING / INTERPRETATION", """
**Strongest empirical findings** (all qualitative)
- Support to non-routine decisions is maieutic (questioning, debate, learning) and AI can sustain or erode this depending on whether outputs are scrutinised (A22).
- Relevance is produced and arbitrated, not given by data (A1); controllers keep a sense-making and legitimation role (A1).
- The meaning of a KPI depends on use; a common platform works when it leaves room for local interpretation (A28).
- Controllers who master Big Data tools give sense to data and challenge managers (A34); cloud co-authoring (A8); the ERP is a sense-giving device for accountants' own work (A35).
- Proxies: understandability of AI reasoning raises acceptance (A15); controllers are expected to translate accounting language for managers (A32, descriptive).

**Strongest articles:** A22, A1, A28, A34.

**Explicitly measured or inferred?** Not measured in any quantitative study (0 quantitative articles have a finding coded 1; 25 findings are coded 0.5, mostly information quality, transparency or data volume). In the quantitative studies it is inferred: from the unexplained mediating role of the BP role (A5), from the 'quality not time' result (A46), from 'mode of use' (A41, abstract).

**Block-definition caution:** the bibliometric block bundles information quality, managerial decision making, interaction and competence with interpretation. The first of these is the best-tested construct in the corpus; interpretation itself is the least tested. High bibliometric weight for the block should not be read as empirical grounding for sensemaking.
"""),
 ("CONTROLLER / BUSINESS PARTNER", """
**Role transformation**
- Positive: strategic tasks rise with digitalisation (A7); strategic involvement rises with MAIS sophistication (A46 b=.467; weaker in family firms, p<.10); proactive BP in SMEs (A9); role broadening (A18); anticipated by practitioners (A16).
- Null or ambivalent: BP requirements flat 2016-2023 while digital and ESG requirements rise (A47); effects 'ambivalent', re-technicisation at intermediate maturity (A34); full ERP integration -> limited MC contribution (A40); dirty work clashes with BP role (A35); BP is one of six boundary strategies (A25); no average effect on role strain (A24).

**Decision involvement:** BP role -> impact on management decisions (A5); questioning and challenge in non-routine decisions (A22, A34); co-authoring (A8).

**Mediation:** one test (A5, n=322): full mediation for tangible resources (both outcomes) and for human skills -> decision impact; partial for intangible resources and part of human skills; scorekeeper role does not mediate.

**Contradictions:** A47 vs A7/A46 (behavioural trace vs self-report); A2 reverses the causal order (BP objective -> analytics); A24: benefit is conditional on role orientation.

**Strongest articles:** A5, A46, A47, A24, A34.
"""),
 ("ORGANISATIONAL TRANSLATION / CHANGE", """
**Implementation, adaptation and change**
- Quantitative: digitalisation has no effect on MC organisation or strategic instruments (A7), and no shift in centralisation (A37); it does standardise (A37 indirect b=.255) and embed in planning (A26); it raises adoption of modern MA methods (A14).
- Qualitative: barriers and levers (A9); fluid role identity (A18); platform design and local interpretation (A28); ERP integration and acceptance (A40); external pressure translated into internal policy (A45); BI implementation success factors (A4, abstract).

**How technology becomes action:** evidence points to four channels, none traced to an action: embedding in planning/standardised processes (A26, A37, A23), acceptance and skills (A40, A43), translation of pressure into policy (A45), and local interpretation (A28). A27 is the closest to action (counter-measure effectiveness).

**Contradiction:** quantitative null on structure (A7, A37) vs qualitative integration (A9, A40, A18).
"""),
 ("PLANNING", """
- Digitalisation raises satisfaction with conventional (b=.279) and modern (b=.387) budgeting; satisfaction -> benefits (A3).
- Digitalisation affects performance only via planning/budgeting performance (A26).
- Digitalised forecasting raises satisfaction and counter-measure effectiveness in crisis; data volume works against it (A27).
- Qualitative: budgeting and forecasting automated (A9); better forecasts (A16). Descriptive: budget remains the most important tool (A32).

The bibliometric figure shows n=1 for Planning; the reading sheet contains at least five studies with direct planning evidence (A3, A26, A27, A9, A32) - the bibliometric weight understates the empirical base.

**Limits:** outcomes are perceived satisfaction or performance; no study measures forecast accuracy or budget quality.
"""),
 ("CYBERNETIC CONTROL", """
- Information/IS quality -> MC effectiveness (A19, A37); digitalisation -> MC effectiveness (A37); analytics -> finance-function effectiveness (A2); BA capabilities -> controllership effectiveness via BP role (A5); digital dimensions -> MC function (A13).
- Qualitative: common KPI language (A28), KPI overload and AI triage (A29), PMS evolution (A49), anomaly detection (A16).
- A41 (abstract only): effectiveness depends on diagnostic vs interactive use of data analytics - no estimates in the sheet.

**Contradictions:** automation vs effectiveness (A2 vs A13); KPI overload (A29) vs improved monitoring (A16).
**Limit:** control effectiveness is always a perception; the quality of performance measurement itself is not measured.
"""),
 ("ADMINISTRATIVE CONTROL", """
- Standardisation carries digitalisation into information quality (A37 b=.255); centralisation does not (A37); MC organisation does not change (A7); standardised processes are an antecedent of digitalisation (A7).
- Qualitative: standardise-and-automate lever and cross-functional integration (A9); integrated ERP automates MC tasks away (A40); common KPI language (A28); standardised reporting from BI (A4, abstract); internalised policies and data governance (A45).
- Boundary systems: small effect on transformation success (A12 b=.087) and on digital innovation (A39 b=.231).

Standardisation is both outcome (A37), antecedent (A7) and design condition (A28): the direction is not settled.
"""),
 ("CULTURAL CONTROL", """
- Beliefs raise digital dynamic capabilities (A12 b=.279) and digital innovation (A39 b=.234) but moderate the capability -> success link negatively (A12 b=-.393).
- Culture: organisational culture affects satisfaction with conventional budgeting only (A3, b=.128) and does not moderate; innovation and trust culture are null for digitalisation (A7).
- Qualitative: BI nurtures a data-driven culture (A4, abstract); two epistemic cultures coexist (A1); resistance -> 91% limited use, acceptance -> 83% high use (A40); resistance and fear of job loss (A9).
"""),
 ("REWARDS & COMPENSATION", """
**No empirical evidence found on the effect of AI or digitalisation on rewards, incentives or compensation.** No finding in the corpus is coded 1 on this block. The only item is A48, a design-thinking/data-analytics lifecycle applied to incentive design; the sheet describes the framework and reports no outcome. The figure's n=0 is consistent with this.
"""),
 ("CONDITIONS / ENABLERS", """
| Condition | Evidence | Direction |
|---|---|---|
| Top management support | A17 (abstract): main driver. A7: strategic leadership ns. A40: top-down policies limit effectiveness. | **Contradictory** |
| Resources | A9 (qual), A17 (abstract). No verified quantitative test; A2's resource-constraint explanation is untested. | Qualitative only |
| Competences | A7 (digital competences sig.), A43 (self-efficacy b=.349), A5 (human skills), A32 (expertise, descriptive), A15 (AI skills, exploratory); qualitative A9, A16, A40, A45. | **Most consistent** |
| Culture | A3 (culture matters for conventional budgeting only; no moderation), A7 (null), A12 (negative moderation), A40 and A9 (resistance). | Mixed |
| Institutional / coercive pressure | A45 only (qualitative); A42 has no extractable findings. | Qualitative only |
| SMEs | A9, A17, A43, A45. Drivers: self-efficacy and ease, not usefulness (A43); compliance-bounded adoption (A45); resource and knowledge barriers (A9). | Consistent but few |
| Adoption conditions | A43 (usefulness ns), A15 (transparency +), A2 (strategy-function alignment). | Mixed |
| Other | Family control weakens MAIS -> involvement (A46, p<.10); digital maturity (A34); integration level (A40). | Single studies |
"""),
 ("OUTCOMES", """
- **Performance:** positive direct (A11, A12, A23, A17-abstract); null direct, positive via planning (A26); weak (A27); automation null and joint negative (A2).
- **Decision quality:** never measured objectively. Proxies: impact on management decisions (A5), managerial effectiveness (A11), AI acceptance (A15), perceived (A16).
- **Control effectiveness:** positive (A19, A37, A13, A5, A2-analytics). Always perceptual.
- **Organisational action:** only A27 (counter-measure effectiveness); A28 qualitative (resource allocation).
"""),
]

QA = [
 ("1. Which blocks are strongly empirically grounded?",
  "**Sensing -> information quality -> control effectiveness** (A11, A37, A19; plus A2, A13) and **Planning** (A3, A26, A27) have three or more independent inferential studies pointing the same way, with the caveat that outcomes are perceptual. **Conditions** are well covered by volume (11 quantitative articles) but only *competence* is consistent. **Controller / Business Partner** is moderately grounded (A5, A46, A7, A24, A47) but contested."),
 ("2. Which blocks are supported mainly by qualitative findings?",
  "**Sensemaking** (A1, A8, A22, A28, A34, A35), **Organisational translation** (A9, A18, A28, A40, A45, A49; the quantitative studies A7 and A37 are nulls), **controller-manager interaction**, **Administrative control** (4 qualitative articles vs 2 quantitative), and **institutional/coercive pressure** (A45 only)."),
 ("3. Which blocks are mostly conceptual?",
  "**Rewards & compensation** (A48 is a framework; no results), **sensemaking as a measured construct**, **organisational action**, **decision quality** and **organisational adaptation -> performance**. The conceptual papers (A21, A44, A6) and reviews (A10, A20, A30, A31, A38, A50) discuss these but do not add empirical findings."),
 ("4. Which arrows between blocks are empirically established?",
  "Quantitatively, with replication: **digital -> information quality** (A11, A37) and **information quality -> control effectiveness** (A19, A37). Quantitatively, single or conflicting studies: **digital -> planning** (A3, A26, A27); **digital capability -> BP role -> controllership effectiveness** (A5); **digital -> standardisation -> information quality** (A37); **MCS use -> digital capability** (A12, A39; reverse direction). Qualitatively only: **controller -> interaction -> interpretation**, **conditions -> translation**."),
 ("5. Which arrows are missing?",
  "No evidence found: **decision -> organisational action** (R16), **controller role -> performance** (R13). No quantitative test: **controller -> interaction** (R12), **interaction -> interpretation** (R14), **interpretation -> decision** (R15, except the A15 proxy), **organisational adaptation -> performance** (R17), **conditions -> translation** (R20), **sensing -> predictive capability** (R2). The two links the figure needs most - interaction and interpretation - are the two without any quantitative evidence."),
 ("6. Where are the strongest null or contradictory findings?",
  "(i) Automation: no effect and a negative joint effect with analytics (A2) against the strongest effect (A13). (ii) No direct digital -> performance effect (A26) and weak crisis effect (A27). (iii) BP requirements flat (A47) against positive self-reports (A7, A46) and qualitative substitution or re-technicisation (A40, A34). (iv) No change in MC organisation or strategic instruments (A7), no shift in centralisation (A37). (v) Usefulness does not predict adoption (A43). (vi) Beliefs moderate in the wrong direction (A12); all contingency moderations null (A3)."),
 ("7. Which contradictions create the need for an interpretive or organisational mechanism?",
  "**Interpretive:** P3 (more data, worse outcomes), P5 (BP helps but mechanism unknown), P6 (information quality vs use depends on interaction), P1 (information up, performance not). **Organisational:** P7 (tools implemented, little structural change), P8 (practices mediate), P1 (A26's embedding), P4 (maturity and substitution), P10 (conditions). The two sets overlap on P1, P5 and P8, which is why the corpus does not discriminate cleanly between the two kinds of mechanism."),
 ("8. Does the evidence justify positioning the controller / business partner as a bridge?",
  "**Yes, as a conditional bridge, not as a general one.** For: the only mediation test (A5) shows the BP role transmits BA capabilities into controllership effectiveness, and the scorekeeper role does not; qualitative studies show what bridging looks like (A22, A8, A34); boundary spanning/bridging is a documented strategy (A25). Against: BP requirements do not rise over time (A47); ERP can absorb the controller's tasks (A40); re-technicisation at intermediate maturity (A34); dirty work (A35); the BP objective may precede analytics rather than follow it (A2). A5 is a single German large-firm survey with perceived outcomes and no coefficients in the sheet. The defensible claim is: *the controller is a candidate bridge whose bridging depends on maturity, skills, ownership and role orientation.*"),
 ("9. Does the evidence justify introducing sensemaking as the mechanism?",
  "**Not as an established mechanism; yes as a theoretically motivated candidate.** It is documented in six qualitative articles and it fits the black-box structure of A5, A46 and A41. It is not measured in any study. Two further cautions: the figure's Sensemaking block mixes strongly tested constructs (information quality, decision making) with the untested one (interpretation); and the A35 'sense-giving' finding concerns accountants making sense of their own work, not of data."),
 ("10. Or do the findings suggest another mechanism more strongly?",
  "**Organisational translation through embedding is the better-evidenced mechanism; sensemaking is the better-motivated one.** Quantitative mediators that do appear are: information quality (A11, A37), standardisation (A37), planning/budgeting performance (A26), MAS development (A23) and the BP role (A5). These are practice-embedding channels. Interpretation appears only qualitatively. The two operate at different levels: embedding explains *whether* technology reaches effectiveness; interpretation explains *how* controllers convert information into decisions. The corpus cannot rank them because no study measures both. Competence (M5) and attention/relevance selection (M6) also arise from the puzzles and are untested."),
]
