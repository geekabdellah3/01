# -*- coding: utf-8 -*-
"""
Coded evidence base for the AI x MCS systematic review.
Source: Lecture_Articles-2_copy.xlsx ("Fiches de Lecture", 50 rows A1-A50).
Every number below is taken from the reading sheet; nothing is imported from memory.

Relationship tag format:  "<REL>.<STANCE>.<MODE>"
  STANCE: S  = supports            S~ = indirect / proxy support
          N  = null                X  = mixed / contradictory
  MODE:   Q  = quantitative inferential test
          D  = descriptive survey / content analysis (no inferential test of the link)
          L  = qualitative / design-science
          U  = abstract-level only (sheet gives no result detail) -> not counted as verified
"""

BLOCKS = ["Sensing", "Sensemaking", "BusinessPartner", "Translation", "Planning",
          "Cybernetic", "Administrative", "Cultural", "Rewards", "Conditions", "Outcomes"]

# ---------------------------------------------------------------- corpus triage
# design: Q quantitative, L qualitative, M mixed, S secondary/review/conceptual, X excluded from evidence
ART = {
 "A1":  dict(short="Epistemic control (MediaCorp case)", y=2025, d="L", method="Single case; 27 interviews (22 respondents) + documents 2010-2023", sample="22 respondents", ctx="Listed multinational media group, 9 countries", note=""),
 "A2":  dict(short="Digitalization of the finance function", y=2025, d="M", method="Survey regression with interactions (+11 interviews)", sample="n=137 finance professionals", ctx="European firms, multi-sector", note=""),
 "A3":  dict(short="Digitalization & satisfaction with budgeting", y=2025, d="Q", method="Survey, PLS-SEM", sample="n=399 budgeting professionals", ctx="58 countries, mostly services", note=""),
 "A4":  dict(short="BI system adoption & reporting capabilities", y=2025, d="L", method="Insider action research (BI pilot) - ABSTRACT ONLY", sample="1 multinational group", ctx="Engineering & construction", note="Sheet row mismatch: method/theory/hypotheses cells are copied from A15. Only the abstract and keywords were used."),
 "A5":  dict(short="Controllership effectiveness & business analytics", y=2025, d="Q", method="Survey, PLS-SEM mediation", sample="n=322 large firms", ctx="Germany, multi-sector", note="No path coefficients in the sheet (only full/partial mediation)."),
 "A6":  dict(short="Review of AI & management accounting", y=2025, d="S", method="Narrative historical review", sample="-", ctx="-", note="No findings in sheet; secondary."),
 "A7":  dict(short="Influencing factors & effects of MC digitalization", y=2025, d="Q", method="Survey, regressions + mediation", sample="n=189 firms", ctx="DACH, multi-sector", note=""),
 "A8":  dict(short="Controller's practice & cloud (IKEA Italy)", y=2025, d="L", method="Pragmatic-constructivist case, interviews - ABSTRACT ONLY", sample="2 stores", ctx="IKEA Italy", note="Abstract only."),
 "A9":  dict(short="Digitalisation & MC of SMEs", y=2025, d="L", method="14 semi-structured expert interviews (2021)", sample="14 CFOs/heads of MC/MAs", ctx="SMEs, DACH", note="Sheet labels it 'quantitative' but the method is qualitative."),
 "A10": dict(short="MA & AI literature review", y=2025, d="S", method="Systematic review (91 articles) - abstract only", sample="91 articles", ctx="-", note="Secondary."),
 "A11": dict(short="Digital transformation, info quality & governance efficiency", y=2025, d="Q", method="Survey (convenience), mediation model", sample="n=320 firms", ctx="Hanoi, Vietnam", note=""),
 "A12": dict(short="MCS for digital transformation success", y=2025, d="Q", method="Survey, SEM (EQS)", sample="n=415 managers", ctx="Spain & Colombia, multi-sector", note="MCS -> digital capability direction (reverse of the chain)."),
 "A13": dict(short="Digital transformation & MC improvement", y=2025, d="Q", method="Survey, PCA + multiple regression (SPSS)", sample="n=149 professionals / 90 institutions", ctx="Morocco, financial institutions", note="Self-reported, single source; R2adj=.585."),
 "A14": dict(short="Digital transformation & modern MA methods in banks", y=2025, d="Q", method="Survey, multiple regression", sample="n=228 / 12 banks", ctx="Jordan, commercial banks", note="No coefficients in sheet."),
 "A15": dict(short="AI transparency & AI acceptance", y=2025, d="Q", method="Online experiment 2x2 between-subjects, ANOVA", sample="n=164 (Prolific)", ctx="International online panel; hypothetical scenario", note="Participants are not controllers/managers in situ."),
 "A16": dict(short="AI & Big Data in MC of Moroccan firms", y=2025, d="L", method="Semi-structured interviews", sample="controllers, CFOs, CEOs (n not given)", ctx="Large firms, Rabat-Sale-Kenitra, Morocco", note="Sheet labels the approach H-D, but the study is interview-based."),
 "A17": dict(short="Steering digitalization & MC maturity in SMEs", y=2024, d="Q", method="Survey - ABSTRACT ONLY", sample="n=132 firms", ctx="Italy, mostly SMEs", note="No coefficients in sheet."),
 "A18": dict(short="Fluid role identity of MAs (Finnish bank)", y=2024, d="L", method="Longitudinal interpretive case; 36 interviews 2014-2023", sample="36 interviews", ctx="OP Financial Group, Finland (bank)", note=""),
 "A19": dict(short="IS quality in MA & MC effectiveness", y=2024, d="Q", method="Survey, hierarchical regression", sample="n=125 firms", ctx="German Mittelstand", note="Respondents mainly CEOs/top managers."),
 "A20": dict(short="AI in managerial accounting - SLR", y=2024, d="S", method="Systematic review (9 primary studies)", sample="9 studies", ctx="-", note="Secondary."),
 "A21": dict(short="AI in MC: emergent forms, practices, infrastructures", y=2024, d="S", method="Conceptual paper", sample="-", ctx="-", note="Conceptual."),
 "A22": dict(short="Maieutic role 'when MA goes digital'", y=2024, d="L", method="Multiple case; 14 interviews on 5 non-routine decisions; discourse analysis", sample="14 managers/controllers", ctx="Not stated in sheet", note=""),
 "A23": dict(short="Modern technology, MAS & organizational performance", y=2024, d="Q", method="Survey, regression (R2=.456)", sample="n not given", ctx="Saudi non-financial firms", note="Self-reported, cross-sectional; coefficients not in sheet."),
 "A24": dict(short="Digitalization & MA role conflict/ambiguity", y=2024, d="Q", method="Survey, regression with interactions", sample="n=242 management accountants", ctx="Netherlands, for-profit firms", note=""),
 "A25": dict(short="Digitalization tensions & boundary work", y=2024, d="L", method="Interviews - ABSTRACT ONLY", sample="senior finance professionals (n not given)", ctx="-", note="Abstract only."),
 "A26": dict(short="Digitalization -> performance via planning & budgeting", y=2024, d="Q", method="Survey, OLS mediation", sample="n=266 management accountants", ctx="Germany", note="Coefficients not in sheet."),
 "A27": dict(short="Digital maturity of forecasting in crisis", y=2023, d="Q", method="Survey, CFA + OLS (Jul-Sep 2020)", sample="n=180 firms (6% response)", ctx="Germany, firms >= EUR50m", note="Low response rate."),
 "A28": dict(short="Digitalisation & accounting language games", y=2023, d="L", method="Case study (NPD performance platform)", sample="1 multi-division firm", ctx="'Semicom'", note=""),
 "A29": dict(short="AI vs 'KPI overload' in process monitoring", y=2023, d="L", method="Design science (BI + neural network)", sample="1 organisation", ctx="Healthcare/public org, anti-corruption", note="No performance metrics in sheet."),
 "A30": dict(short="Literature review: digitalisation & MC", y=2023, d="S", method="Systematic review", sample="-", ctx="-", note="Secondary."),
 "A31": dict(short="MA, EDA & unsupervised ML", y=2022, d="S", method="Narrative review", sample="-", ctx="-", note="Secondary."),
 "A32": dict(short="Success factors, tools, controllers' tasks (digitalization)", y=2022, d="Q", method="Descriptive survey, Mann-Whitney", sample="n=35 controllers", ctx="Serbia, multi-sector", note="Small n; no digitalization variable tested."),
 "A33": dict(short="Digital technology & changing roles (dream/nightmare)", y=2020, d="L", method="Exploratory case, interviews + NVivo", sample="n/a in sheet", ctx="Nordic insurance/finance firm", note="NO FINDINGS EXTRACTABLE: 'conclusions' cell contains literature-review sections only."),
 "A34": dict(short="Back to basics or ready for take-off? (controllers)", y=2020, d="L", method="Cross-sectional field study, semi-structured interviews", sample="n not given", ctx="Large French firms (>=250 staff)", note=""),
 "A35": dict(short="Occupational identities of MAs & the IT system", y=2018, d="L", method="Qualitative case - ABSTRACT ONLY", sample="1 organisation", ctx="SAP ERP", note="Abstract only."),
 "A36": dict(short="Digitalisation brings new opportunities to MC", y=2017, d="X", method="Interpretive analysis of 3 vendor promotional videos", sample="3 videos", ctx="US & Germany (vendors)", note="Vendor claims, not organisational evidence - excluded from counts."),
 "A37": dict(short="Digitalization & org. design -> MC effectiveness", y=2026, d="Q", method="Survey, SEM (information-processing view)", sample="n=246 business units", ctx="European firms, multi-sector", note=""),
 "A38": dict(short="Elusive boundaries, power & knowledge production (SLR)", y=2020, d="S", method="Systematic review 2007-2017", sample="-", ctx="-", note="Secondary."),
 "A39": dict(short="Levers of control & digital innovation (banks)", y=2026, d="Q", method="PLS-SEM + ANN", sample="n not given", ctx="Indonesia, banking", note="MCS -> digital innovation direction."),
 "A40": dict(short="MC contribution to performance steering under ERP", y=2026, d="L", method="Qualitative, coded references (ERP case data)", sample="n not given", ctx="Moroccan firms", note="Percentages are shares of coded references, not firms."),
 "A41": dict(short="Data analytics used diagnostically/interactively", y=2026, d="Q", method="Empirical - method unspecified (ABSTRACT ONLY)", sample="n not given", ctx="Multi-sector", note="No results in sheet; unverified."),
 "A42": dict(short="Org. change factors & AI adoption in MA", y=2026, d="L", method="Comparative multiple case", sample="n not given", ctx="USA, Germany, Austria", note="NO FINDINGS EXTRACTABLE: sheet lists variables only ('lecture integrale requise')."),
 "A43": dict(short="TAM extension for digital MA in SMEs", y=2025, d="Q", method="Survey, PLS-SEM", sample="n=225 SMEs", ctx="Bangladesh", note=""),
 "A44": dict(short="Digital data & MA: rethinking research methods", y=2020, d="S", method="Methodological essay", sample="-", ctx="-", note="Conceptual."),
 "A45": dict(short="Institutional pressures on AI adoption (SMEs)", y=2026, d="L", method="12 semi-structured interviews", sample="12 interviews", ctx="Austria, Germany, USA; SMEs and large firms", note=""),
 "A46": dict(short="MAIS sophistication, family control, controller involvement", y=2026, d="Q", method="Survey, regression with interaction", sample="n=136 firms", ctx="German Mittelstand", note=""),
 "A47": dict(short="Trends in controller roles (Finland)", y=2026, d="Q", method="Longitudinal content analysis of job ads 2016-2023", sample="7,426 ads", ctx="Finland", note="Measures demanded roles, not enacted roles."),
 "A48": dict(short="Design-thinking Data Analytic Lifecycle (bank)", y=2024, d="L", method="Critical case study", sample="1 bank", ctx="Vietnam, commercial bank", note="Sheet gives a framework description, no outcome results."),
 "A49": dict(short="PMS in digital servitization (longitudinal)", y=2025, d="L", method="Longitudinal case", sample="1 firm", ctx="Logistics, wine & spirits", note=""),
 "A50": dict(short="Impact of IT on the MA profession (bibliometrics)", y=2025, d="S", method="Bibliometric analysis (183 articles)", sample="183 articles", ctx="-", note="Secondary."),
}

DEFAULT_SIG = {"L": "n/a (qualitative)"}

# ---------------------------------------------------------------- findings
# (art, finding, IV, mechanism, mediator, moderator/condition, outcome, dir, sig, short, codes[11], tags)
# codes order: Sensing, Sensemaking, BusinessPartner, Translation, Planning, Cybernetic,
#              Administrative, Cultural, Rewards, Conditions, Outcomes
F = []
def f(art, finding, iv, mech, med, mod, out, d, sig, short, codes, tags=""):
    F.append(dict(art=art, finding=finding, iv=iv, mech=mech, med=med, mod=mod, out=out, dir=d, sig=sig,
                  short=short, codes=[float(x) for x in codes.split()], tags=[t for t in tags.split() if t]))

# ---- A1
f("A1","Digitalisation does not replace narrative logic with data-driven logic: two epistemic cultures (narrative-driven, data-driven) coexist and compete over what counts as relevant",
  "Data-driven transformation","Coexistence of epistemic cultures","-","-","Definition of relevant knowledge","n/a","n/a (qualitative)",
  "A1: two epistemic cultures coexist","0.5 1 0.5 1 0 0.5 0 0.5 0 0 0","E6.S.L")
f("A1","Relevance is not given by the data: it is actively produced and arbitrated through organisational, technical and managerial devices ('epistemic control')",
  "Data availability","Arbitration of relevance by control devices","-","-","Perceived relevance of information","n/a","n/a (qualitative)",
  "A1: relevance is constructed, not given","0.5 1 0.5 1 0 0.5 0.5 0.5 0 0 0","E6.S.L")
f("A1","The move to a data-driven strategy was initiated by narrative logic; controllers mostly keep a sense-making and legitimation role",
  "Strategy shift to data-driven","Narrative-led initiation; controller as sense-maker/legitimiser","-","-","Controller role","n/a","n/a (qualitative)",
  "A1: controllers remain sense-makers","0.5 1 1 0.5 0 0 0 0 0 0 0","E6.S.L")
# ---- A2
f("A2","Digitalization strategy x finance-function efficiency objective -> more automation",
  "Digitalization strategy x efficiency objective","Strategic alignment between firm and function","-","Efficiency objective","Automation of finance function","+","Yes (b=.148)",
  "A2: strategy x efficiency -> automation b=.148","1 0 0 0 0 0 0 0 0 1 0","R3.S.Q R18.S.Q E13.S.Q")
f("A2","Digitalization strategy and business-partnering objective each raise analytics use independently; their interaction is not significant",
  "Digitalization strategy; BP objective","Independent main effects","-","BP objective","Analytics use","+ / 0","Main effects yes; interaction No (b=-.015)",
  "A2: strategy and BP objective -> analytics; interaction ns","1 0 0.5 0 0 0 0 0 0 1 0","R18.X.Q E7.S.Q E13.N.Q")
f("A2","Digitalization strategy x efficiency objective -> more analytics use",
  "Digitalization strategy x efficiency objective","Strategic alignment","-","Efficiency objective","Analytics use","+","Yes (b=.190, p<.05)",
  "A2: strategy x efficiency -> analytics b=.190*","1 0 0 0 0 0 0 0 0 1 0","R18.S.Q")
f("A2","Automation has no effect on finance-function effectiveness",
  "Automation","Time/effort saving (assumed, untested)","-","-","Finance function effectiveness","0","No (b=-.003)",
  "A2: automation -> effectiveness b=-.003 ns","1 0 0 0 0 0 0 0 0 0 1","R7.N.Q E1.N.Q")
f("A2","Analytics use raises finance-function effectiveness",
  "Analytics use","Information processing","-","-","Finance function effectiveness","+","Yes (b=.465, p<.01)",
  "A2: analytics -> effectiveness b=.465**","1 0.5 0 0 0 0 0 0 0 0 1","R7.S.Q")
f("A2","Using automation AND analytics together lowers effectiveness (negative interaction); authors speculate resource constraints (untested)",
  "Automation x analytics","Possible resource constraint (not tested)","-","-","Finance function effectiveness","-","Yes (b=-.222, p<.01)",
  "A2: automation x analytics -> effectiveness b=-.222**","1 0 0 0 0 0 0 0 0 0 1","R7.N.Q E1.N.Q E2.S.Q")
# ---- A3
f("A3","Digitalization intensity raises user satisfaction with both conventional (b=.279) and modern (b=.387) budgeting methods",
  "Digitalization intensity","Satisfaction with budgeting methods","Satisfaction (CBM/MBM)","-","Budgeting satisfaction","+","Yes (p<.001)",
  "A3: digitalization -> satisfaction CBM b=.279, MBM b=.387 ***","1 0 0 0 1 0 0 0 0 0 0.5","R4.S.Q")
f("A3","Satisfaction with budgeting methods is associated with budgeting benefits (b=.411 CBM; b=.385 MBM)",
  "Satisfaction with budgeting","Perceived benefit","-","-","Budgeting benefits","+","Yes (p<.001)",
  "A3: satisfaction -> benefits b=.411/.385 ***","0 0 0 0 1 0 0 0 0 0 1","R4.S.Q E8.S.Q")
f("A3","Internal contingencies (strategy support, participation, culture) have direct effects on satisfaction; culture matters for conventional methods only",
  "Strategy support; participation; organisational culture","Direct effects","-","-","Budgeting satisfaction","+","Yes (b=.128-.194)",
  "A3: BS, PE (CBM+MBM), OC (CBM only) -> satisfaction","0 0 0 0 1 0 0 1 0 1 0.5","C_CULT.S.Q")
f("A3","None of the tested contingencies moderates the digitalization-satisfaction link (all interactions ns)",
  "Digitalization x contingencies","Moderation","-","Culture, participation, strategy support","Budgeting satisfaction","0","No (e.g. OC x Dig b=.025 p=.653)",
  "A3: all moderation tests ns","1 0 0 0 1 0 0 1 0 1 0","E13.N.Q C_CULT.N.Q")
# ---- A4 (abstract only)
f("A4","BI solution leverages reporting-process capabilities: streamlined/standardised processes, better resource use, more data flexibility, with reported gains for MC and organisational performance",
  "BI system implementation","Reporting-process capability","-","Critical success factors (organisational, process, technological)","MC and organisational performance","+","n/a (qualitative)",
  "A4: BI -> standardised reporting, resource gains (abstract)","1 0 0 0.5 0 0.5 1 0 0 0.5 0.5","E4.S.L R5.S.L R7.S.L")
f("A4","BI implementation nurtures a data-driven culture",
  "BI system implementation","Cultural change","-","-","Data-driven culture","+","n/a (qualitative)",
  "A4: BI -> data-driven culture (abstract)","1 0 0 0.5 0 0 0 1 0 0 0","")
# ---- A5
f("A5","Business-analytics capabilities (tangible, intangible, human skills) improve controllership output quality and impact on decisions BY WAY OF the business-partner role: full mediation for tangible resources (both outcomes) and for human skills -> decision impact; partial for intangible resources and part of human skills",
  "BA capabilities (tangible, intangible, human skills)","Controller business-partner role","Business-partner role","-","Controllership output quality; impact on management decisions","+","Yes (mediation; coefficients not in sheet)",
  "A5: BAC -> BP role -> effectiveness (full/partial mediation)","1 0 1 0 0 0.5 0 0 0 0.5 1","R6.S.Q R11.S.Q R19.S.Q C_COMP.S.Q")
f("A5","The traditional scorekeeper role has no significant mediating effect between BA capabilities and controllership effectiveness",
  "BA capabilities","Scorekeeper role","Scorekeeper role","-","Controllership effectiveness","0","No",
  "A5: scorekeeper mediation ns","1 0 0.5 0 0 0.5 0 0 0 0 1","R6.S.Q")
# ---- A7
f("A7","Digitalization of MC increases strategic tasks and operational tasks of the control function, and the use of operational instruments",
  "Digitalization of MC","Task and instrument broadening","-","-","Strategic/operational tasks; operational instruments","+","Yes",
  "A7: digitalization -> strategic & operational tasks, operational instruments","1 0 1 0.5 0 0.5 0 0 0 0 0","R6.S.Q E9.S.Q")
f("A7","Digitalization has no significant effect on strategic instruments or on the organisation of the MC function",
  "Digitalization of MC","Structural change (not observed)","-","-","Strategic instruments; MC organisation","0","No",
  "A7: digitalization -> strategic instruments, MC organisation ns","1 0 0 1 0 0.5 1 0 0 0 0","E9.N.Q E10.N.Q")
f("A7","Digital competencies, standardised processes and data management drive digitalization of MC; strategic leadership, innovation culture and trust culture do not",
  "Digital competences; process standardisation; data management; leadership; innovation/trust culture","Capability antecedents","-","-","Digitalization of MC","+ / 0","Yes for COMP, PROC, DATA; No for LEAD, INNO, TRUS",
  "A7: COMP, PROC, DATA sig; leadership, innovation & trust culture ns","0.5 0 0 0 0 0 1 1 0 1 0","R18.X.Q C_COMP.S.Q C_CULT.N.Q C_TM.N.Q")
# ---- A9
f("A9","Digitalization automates and standardises repetitive work (reporting, data collection, budgeting, variance analysis), freeing controllers for deeper analysis, scenarios, forecasts and strategic decision support",
  "Digitalization (RPA, automation)","Task automation -> time released","-","-","Controller activity mix","+","n/a (qualitative)",
  "A9: automation frees time for analysis/scenarios","1 0 0.5 0 1 0.5 1 0 0 0 0","R3.S.L E1.S.L R4.S.L R2.S.L E4.S.L")
f("A9","Greater availability and transparency of data speed up and deepen analyses",
  "Data availability/transparency","Information access","-","-","Speed and depth of analysis","+","n/a (qualitative)",
  "A9: data availability -> faster, deeper analysis","1 0.5 0 0 0 0.5 0 0 0 0 0","R1.S.L")
f("A9","MC becomes more cross-functional, integrated and partly centralised; controllers act as coordination nodes with ties to sales, marketing, purchasing and IT",
  "Digitalization","Organisational integration","-","-","MC organisation","+","n/a (qualitative)",
  "A9: more cross-functional, partly centralised MC","1 0 0.5 1 0 0 1 0 0 0 0","E10.S.L")
f("A9","Controllers move from information provider to proactive business partner (strategic support, steering the digital transformation, dialogue with management); competences broaden but the job is extended rather than replaced",
  "Digitalization","Role expansion","-","Competences (analytics, IT, communication)","Controller role","+","n/a (qualitative)",
  "A9: controller -> proactive business partner","1 0 1 0.5 0 0 0 0 0 0.5 0","R6.S.L")
f("A9","Obstacles: scarce internal resources, no roadmap, knowledge gaps, resistance/job-loss fear, silos; levers: vision, standardise/automate, train, pilot projects, clarify roles, adapt organisation",
  "Resources; knowledge; resistance; silos","Barriers and levers","-","SMEs","Digitalization progress","-","n/a (qualitative)",
  "A9: barriers = resources, knowledge, resistance, silos","1 0 0 0.5 0 0 0 0.5 0 1 0","R18.S.L R20.S.L C_RES.S.L C_COMP.S.L C_CULT.S.L C_SME.S.L")
# ---- A11
f("A11","Digital transformation in MA strongly improves management-accounting information quality",
  "Digital transformation in MA","Information capability","-","-","Information quality","+","Yes (b=.814, p<.001)",
  "A11: digital transformation -> info quality b=.814***","1 0.5 0 0 0 0 0 0 0 0 0","R1.S.Q")
f("A11","Digital transformation raises managerial effectiveness directly (b=.209), and information quality raises it strongly (b=.624); the indirect effect via information quality is b=.508 -> partial mediation",
  "Digital transformation in MA","Information quality -> managerial decisions","Information quality","-","Managerial effectiveness","+","Yes (p=.004; p<.001; indirect p=.002)",
  "A11: IQ -> managerial effectiveness b=.624***; indirect b=.508**","1 0.5 0 0 0 0 0 0 0 0 1","R9.S.Q R7.S.Q")
# ---- A12
f("A12","Interactive use of MCS (b=.355) and belief systems (b=.279) raise digital dynamic capabilities (sensing, seizing, transforming); diagnostic use also does (b=.167); boundary systems do not",
  "Interactive use of MCS; belief systems","Control use shapes digital capability","Digital dynamic capabilities","-","Digital dynamic capabilities","+","Yes (p<.001; diagnostic p<.01; boundary ns)",
  "A12: interactive MCS b=.355***, beliefs b=.279*** -> DDC","1 0.5 0 0.5 0 0.5 0 1 0 1 0","E3.S.Q R14.S~.Q")
f("A12","Digital dynamic capabilities strongly predict digital transformation success (b=.789)",
  "Digital dynamic capabilities","Sensing-seizing-transforming","-","-","Digital transformation success","+","Yes (p<.001)",
  "A12: DDC -> DTS b=.789***","1 0 0 1 0 0 0 0 0 0 1","R7.S.Q R17.S~.Q")
f("A12","Interactive MCS use does not moderate DDC -> success (b=.071 ns); belief systems moderate NEGATIVELY (b=-.393, p<.05), the opposite of the hypothesis; boundary systems add a small direct effect (b=.087)",
  "DDC x interactive MCS; DDC x beliefs","Moderation","-","Interactive MCS use; belief systems","Digital transformation success","0 / -","iMCS No; Beliefs Yes (reverse sign)",
  "A12: DDC x iMCS ns; DDC x beliefs b=-.393* (reverse)","1 0 0 0 0 0 0 1 0 1 1","E13.N.Q C_CULT.X.Q")
# ---- A13
f("A13","All five digital dimensions improve the MC function (R2adj=.585): automation b=.434, BI/Big Data b=.368, cybersecurity b=.214, cloud b=.148, data visualisation b=.084",
  "Automation; BI/Big Data; visualisation; cloud; cybersecurity","Technology breadth","-","-","Improvement of MC function (self-reported)","+","Yes (p=.001-.037)",
  "A13: automation b=.434**, BI/Big Data b=.368**, others .08-.21","1 0 0 0 0 0.5 0.5 0 0 0 0.5","R5.S.Q E1.S.Q")
# ---- A14
f("A14","Digital transformation (technology, process, people) increases adoption of modern management-accounting methods in banks; authors link it to better access to information, real-time reporting and decisions",
  "Digital transformation (technology, process, people)","Adoption of modern methods","-","-","Adoption of modern MA methods","+","Yes (coefficients not in sheet)",
  "A14: digital transformation -> modern MA methods adoption","1 0 0 1 0 0.5 0 0 0 0 0","E9.S.Q")
# ---- A15
f("A15","A more transparent (understandable) AI raises acceptance of AI recommendations in managerial forecasting",
  "AI transparency (understandability of reasoning)","Understanding -> trust -> acceptance","-","-","AI acceptance","+","Yes (F=15.54, p<.001)",
  "A15: transparency -> acceptance F=15.54***","1 0.5 0 0 0 0 0 0 0 1 0","R15.S~.Q R18.S.Q")
f("A15","Decision type (operational vs strategic) does not moderate the transparency effect",
  "Transparency x decision type","Moderation","-","Decision type","AI acceptance","0","No (F=0.26, p=.608)",
  "A15: decision type moderation ns F=.26","1 0.5 0 0 0 0 0 0 0 1 0","E13.N.Q")
f("A15","Exploratory: AI skills condition the pattern - low-skill managers behave as hypothesised; high-skill managers accept AI more in strategic decisions",
  "AI skills; confidence in technology","Skill-dependent acceptance","-","AI proficiency","AI acceptance","+ / conditional","Exploratory; not reported in sheet",
  "A15: AI skills reshape acceptance (exploratory)","1 0.5 0 0 0 0 0 0 0 1 0","C_COMP.S~.Q E13.S~.Q")
# ---- A16
f("A16","Big Data/AI strengthen predictive capacity: better forecasts, real-time anomaly detection, demand anticipation",
  "Big Data / AI","Predictive analytics","-","-","Predictive capability of MC","+","n/a (qualitative)",
  "A16: Big Data/AI -> better forecasts, anomaly detection","1 0 0 0 0.5 1 0 0 0 0 0","R2.S.L R5.S.L")
f("A16","AI automates repetitive tasks (e.g. financial reports) -> time saved, fewer errors, time for higher-value analysis",
  "AI automation","Time release","-","-","Workload; accuracy","+","n/a (qualitative)",
  "A16: AI automation -> time savings, accuracy","1 0 0 0 0 0.5 0 0 0 0 0","R3.S.L E1.S.L")
f("A16","Interviewees perceive that Big Data/AI improve decision quality (detailed, up-to-date data; predictive analyses)",
  "Big Data / AI","Information -> decision","-","-","Decision quality (perceived)","+","n/a (qualitative)",
  "A16: Big Data/AI -> perceived better decisions","1 0.5 0.5 0 0 0 0 0 0 0 0.5","R9.S.L")
f("A16","Weak mastery of Big Data tools reduces analytical effectiveness and decision quality; training is needed",
  "Insufficient competence","Competence gap","-","-","Effectiveness of analyses","-","n/a (qualitative)",
  "A16: weak Big Data mastery limits effectiveness","1 0 0.5 0 0 0 0 0 0 1 0.5","C_COMP.S.L R19.S~.L")
f("A16","AI/Big Data make data-security management more complex; corrupted data could distort forecasts and decisions",
  "AI / Big Data integration","Data-security exposure","-","-","Reliability of control","-","n/a (qualitative)",
  "A16: data security complexity","1 0 0 0 0 0.5 0.5 0 0 0.5 0","")
f("A16","Controllers see AI/Big Data as both opportunity and threat and expect to evolve toward business-partner roles (anticipated, not observed)",
  "AI / Big Data","Anticipated role change","-","-","Controller role (expected)","+ (anticipated)","n/a (qualitative)",
  "A16: controllers expect BP role (anticipation)","1 0 1 0 0 0 0 0 0 0 0","R6.S~.L")
# ---- A17 (abstract)
f("A17","Digitalization delivers significant benefits for company performance and for internal/external communication (abstract-level; no coefficients in sheet)",
  "Digitalization","Benefits","-","-","Performance; communication","+","Reported significant (no detail)",
  "A17: digitalization -> performance & communication (abstract)","1 0 0 0 0 0 0 0 0 0 1","R7.S.U")
f("A17","Top management, human resources and financial resources are the main drivers of digitalization; medium-sized firms are more active than small ones",
  "Top management; HR; financial resources; size","Resource-based drivers","-","SMEs","Digitalization","+","Reported significant (no detail)",
  "A17: top mgmt, HR, finance drive digitalization (abstract)","1 0 0 0 0 0 0 0 0 1 0","C_TM.S.U C_RES.S.U C_SME.S.U R18.S.U")
f("A17","Training in digitalization is key to a more mature MCS and higher performance (abstract-level)",
  "Training","Competence","-","SMEs","MCS maturity; performance","+","Reported (no detail)",
  "A17: training -> MCS maturity (abstract)","1 0 0 0 0 0.5 0 0 0 1 0.5","C_COMP.S.U")
# ---- A18
f("A18","Digitalization (RPA, AI, BI), centralised systems and regulation cut routine local tasks, widen analysis/communication tasks and create specialised HQ roles",
  "Digitalization; centralisation; regulation","Task shift","-","-","Controller work","+","n/a (qualitative)",
  "A18: routine tasks fall, analytic/communication tasks rise","1 0 1 1 0 0 0.5 0 0 0 0","R6.S.L E10.S.L")
f("A18","Controllers develop a fluid role identity that lets them switch between bean counter, business partner and IT/data specialist without dissonance; upskilling and agile teams enable the adaptation",
  "Digitalization; regulation","Fluid role identity","Fluid role identity","Upskilling; agile teams","Adaptation of controller role","+","n/a (qualitative)",
  "A18: fluid identity + upskilling enable role adaptation","1 0.5 1 1 0 0 0 0 0 1 0","R20.S.L R19.S~.L E5.S.L")
f("A18","Risk that specialised data roles are filled by non-accountants",
  "Digitalization","Boundary erosion","-","-","Accountants' jurisdiction","-","n/a (qualitative)",
  "A18: risk of non-accountants in data roles","1 0 0.5 0.5 0 0 0 0 0 0 0","E5.S.L")
# ---- A19
f("A19","Information-systems quality in MA strongly predicts MC effectiveness (b=.549; R2 .065 -> .349)",
  "IS quality in MA","Information quality -> control","-","-","MC effectiveness","+","Yes (p<.01)",
  "A19: IS quality -> MC effectiveness b=.549**","1 0.5 0 0 0 1 0 0 0 0 1","R8.S.Q")
f("A19","Process automation strengthens the IS quality -> MC effectiveness link (interaction b=.149)",
  "IS quality x automation","Moderation","-","Degree of automation","MC effectiveness","+","Marginal (p<.10)",
  "A19: IS quality x automation b=.149 (p<.10)","1 0 0 0 0 1 0.5 0 0 0.5 1","E13.S.Q E1.S~.Q")
# ---- A22
f("A22","MA support for non-routine decisions is 'maieutic': it questions, debates, confronts intuitions and teaches - both in how answers are used and in how analyses are produced",
  "Controller/manager involvement in non-routine decisions","Questioning, deliberation, learning","-","Uncertainty and ambiguity of the decision","Decision quality / learning","n/a","n/a (qualitative)",
  "A22: MA supports decisions by questioning and debate","0 1 1 0 0 0 0 0 0 0.5 0.5","R11.S.L R12.S.L R14.S.L R15.S.L")
f("A22","Practitioners voice three AI discourses (computation, judgment, interaction); AI need not destroy the maieutic role and may strengthen it if outputs keep being scrutinised rather than accepted on 'autopilot'",
  "AI in MC","Scrutiny / human-AI interaction","-","Balance between discourses","Maintenance of maieutic role","+ / conditional","n/a (qualitative)",
  "A22: AI can sustain the maieutic role if scrutinised","1 1 0.5 0.5 0 0 0 0 0 0.5 0","E6.S.L R15.S.L")
f("A22","If AI automates hypothesis-setting, collection and analysis, learning opportunities in the analytic process may be lost",
  "AI automation of analysis","Loss of learning","-","-","Maieutic role / learning","-","n/a (qualitative)",
  "A22: automating the process erodes learning","1 1 0.5 0 0 0 0 0 0 0 0","E1.N.L")
# ---- A23
f("A23","Modern technology raises MAS development (+); MAS development raises organisational performance (+); technology also raises performance directly (+) (R2=.456)",
  "Modern technology applications","MAS development","MAS development","-","Organizational performance","+","Yes (coefficients not in sheet)",
  "A23: technology -> MAS -> performance; also direct","1 0 0 0.5 0 0.5 0 0 0 0 1","E9.S.Q E8.S.Q R7.S.Q")
# ---- A24
f("A24","On average, anticipated digitalization of the finance function does not raise role conflict or ambiguity",
  "Anticipated digitalization","Role strain","-","-","Role conflict; role ambiguity","0","No",
  "A24: average effect of digitalization on role strain ns","1 0 0.5 0 0 0 0 0 0 0 0","E5.N.Q")
f("A24","Watchdog-oriented accountants experience more role conflict and ambiguity as digitalization rises; business-partner-oriented ones experience less (robust to alternative measures)",
  "Digitalization x watchdog-to-BP orientation","Role orientation fit","-","Watchdog vs business-partner orientation","Role conflict; role ambiguity","+ / -  (conditional)","Yes (interaction)",
  "A24: digitalization x watchdog orientation -> strain","1 0 1 0 0 0 0 0 0 1 0","E5.S.Q E13.S.Q")
# ---- A25 (abstract)
f("A25","Finance professionals answer digitalization with six boundary-work strategies (expand into BP roles, other specialisms, defend, cross-functional collaboration, boundary spanning/bridging, restructuring); perceptions of boundary permeability drive the choice",
  "Digitalization tensions","Boundary work","-","Perceived boundary permeability","Strategy chosen; inter-professional competition","n/a","n/a (qualitative)",
  "A25: six boundary-work responses incl. BP and bridging (abstract)","1 0.5 1 1 0 0 0 0 0 0 0","E5.S.L R6.X.L E10.S~.L")
# ---- A8 (abstract)
f("A8","Cloud platform: manager interactions are partly governed, partly supported by cloud information; the controller orchestrates a co-authoring process in which managers integrate facts, possibilities, values and communication -> better decision support (abstract-level)",
  "Cloud information platform","Co-authoring orchestrated by controller","-","-","Decision support","+","n/a (qualitative)",
  "A8: controller orchestrates co-authoring via cloud (abstract)","1 1 1 0.5 0 0 0 0 0 0 0.5","R6.S.L R11.S.L R12.S.L R14.S.L R15.S~.L")
# ---- A26
f("A26","Digitalization of MAC has no significant direct effect on corporate performance",
  "Digitalization of MAC (AI, predictive analytics, RPA, scenario models)","-","-","-","Corporate performance (subjective)","0","No",
  "A26: digitalization -> performance direct ns","1 0 0 0 1 0 0 0 0 0 1","R7.N.Q")
f("A26","The effect of digitalization on performance runs through planning and budgeting performance (significant indirect effect): digital tools pay off only when embedded in planning/steering processes",
  "Digitalization of MAC","Embedding in planning & budgeting","Planning/budgeting performance","-","Corporate performance","+ (indirect)","Yes (indirect)",
  "A26: digitalization -> planning performance -> performance (full mediation)","1 0 0 1 1 0.5 0 0 0 0 1","R4.S.Q R7.S.Q E8.S.Q")
# ---- A27
f("A27","Higher digitalization/automation of forecasting before the crisis raises satisfaction with forecasting during the crisis (robust to controls)",
  "Digitalization/automation of forecasting","Less effort, faster forecasts","-","-","Forecast satisfaction","+","Yes",
  "A27: DIGI -> forecast satisfaction (robust)","1 0 0 0 1 0 0 0 0 0 0.5","R4.S.Q R2.S~.Q")
f("A27","A larger volume of forecast inputs and KPIs lowers forecast satisfaction and counter-measure effectiveness (significant with controls)",
  "Data volume (inputs + KPIs)","Information overload / loss of focus","-","-","Forecast satisfaction; counter-measure effectiveness","-","Yes (with controls)",
  "A27: data volume -> satisfaction, counter-measures (neg.)","1 0.5 0 0 1 0.5 0 0 0 0 0.5","E2.S.Q")
f("A27","Digitalization/automation (and, less clearly, methodological sophistication) raise the effectiveness of counter-measures during the crisis",
  "Digital maturity of forecasting","Better informational base -> faster action","-","-","Counter-measure effectiveness (organisational action)","+","Yes in one specification; borderline in the other",
  "A27: DIGI -> counter-measure effectiveness (mixed specs)","1 0 0 0 1 0 0 0 0 0 1","E11.S.Q")
f("A27","Digital maturity of forecasting has only weak, specification-dependent effects on the firm's economic situation during the crisis",
  "Digital maturity of forecasting","Short observation window","-","-","Economic situation in crisis","0 / +","Weak: sig. in one model, ns with controls",
  "A27: DIGI -> economic situation weak/spec-dependent","1 0 0 0 1 0 0 0 0 0 1","R7.X.Q")
# ---- A28
f("A28","A performance platform with common KPIs creates a shared 'language' that enables cross-division comparison and consistent resource allocation",
  "Digital KPI platform","Standardised language","-","-","Comparability; resource allocation","+","n/a (qualitative)",
  "A28: common KPIs -> comparability & resource allocation","1 0.5 0 1 0 1 1 0 0 0 0.5","R5.S.L E4.S.L")
f("A28","Digitalization does not create a single truth: the meaning of numbers depends on use; the platform works when flexible, customised analyses leave room for local interpretation and fails when it overrides local practice",
  "Digital platform","Local interpretation within a common language","-","Flexibility of analysis paths","Acceptance/usefulness of the platform","± conditional","n/a (qualitative)",
  "A28: meaning depends on use; flexibility needed","1 1 0 1 0 1 0.5 0 0 0.5 0","E6.S.L R20.S.L R14.S~.L")
f("A28","Common KPIs extend across the product life cycle, redefining what 'performance' means and managers' responsibilities",
  "Digital KPI platform","Redefinition of performance","-","-","Scope of performance/responsibilities","+","n/a (qualitative)",
  "A28: KPI scope widens, redefining performance","1 0 0 1 0 1 0 0 0 0 0.5","E10.S~.L")
# ---- A29
f("A29","BI computes KPIs and flags anomalies but floods analysts with alarms ('KPI overload'); a supervised neural network learns the analyst's judgement, removes false positives and catches anomalies missed by rules",
  "BI + supervised AI","Automation of alarm triage","-","-","Fraud/anomaly detection; alarm overload","+","n/a (design science; no metrics in sheet)",
  "A29: BI floods analyst; AI filters false positives","1 0.5 0 0 0 1 0 0 0 0 0.5","R5.S.L E2.S.L")
# ---- A32
f("A32","Controllers are seen mainly as management support; the controller is expected to translate accounting language into clear, usable information for managers (interpreter / business-partner conception)",
  "Digital context (not measured)","Perceived role","-","-","Perceived role of controller","n/a","Descriptive (n=35)",
  "A32: controller perceived as interpreter of information (n=35)","0.5 0.5 1 0 0 0 0 0 0 0 0","R11.S~.D E6.S~.D")
f("A32","Controller expertise/competence is rated the main success factor of controlling, followed by a developed accounting function and a partnership with management",
  "Controller expertise","Human capital","-","-","Success of controlling","+","Descriptive",
  "A32: expertise = main success factor (n=35)","0.5 0 1 0 0 0 0 0 0 1 0.5","C_COMP.S.D R19.S~.D")
f("A32","Despite intensive digitalization the most important tools remain traditional (budget, variance analysis, short-term results); advanced tools expand gradually",
  "Digitalization","Layering of tools","-","-","Tools used","0 (stability)","Descriptive",
  "A32: traditional tools still most important (n=35)","0.5 0 0 0 1 1 0 0 0 0 0","E9.N.D")
# ---- A34
f("A34","Digitalization/Big Data does not automatically strengthen the controller's strategic role; effects are ambivalent",
  "Digital era / Big Data","Role ambivalence","-","Digital maturity","Controller strategic role","0 / ±","n/a (qualitative)",
  "A34: effect on strategic role is ambivalent","1 0 1 0 0 0 0 0 0 0.5 0","R6.X.L")
f("A34","Digitalization can re-technicise the function: time goes to collecting, harmonising and fiabilising data, crowding out advice - strongest at intermediate digital maturity",
  "Digitalization at intermediate maturity","Data-wrangling workload","-","Digital maturity","Time for business partnering","-","n/a (qualitative)",
  "A34: re-technicisation at intermediate maturity","1 0 1 0.5 0 0 0 0 0 1 0","R6.N.L E1.N.L")
f("A34","Controllers who master Big Data tools become active actors in digital transformation: they give sense to data, spot opportunities and challenge managers ('augmented business partner')",
  "Mastery of Big Data tools","Sense-giving and challenge","-","Tool mastery","Controller contribution to decisions","+","n/a (qualitative)",
  "A34: mastery -> controllers give sense to data, challenge managers","1 1 1 0.5 0 0 0 0 0 1 0.5","R6.S.L R12.S.L E6.S.L R19.S~.L")
# ---- A35 (abstract)
f("A35","The ERP/IT system regulates identity (defines appropriate behaviour) and is a sense-giving device through which accountants make sense of their work",
  "IT/ERP system","Identity regulation and identity work","-","-","Occupational identity","n/a","n/a (qualitative)",
  "A35: ERP = identity regulator and sense-giving device (abstract)","1 1 0.5 0 0 0 0.5 0 0 0 0","E5.S.L E6.S~.L")
f("A35","The system creates 'dirty' work that clashes with the business-partner role and may limit professional judgement and business insight",
  "IT/ERP system","Dirty work -> role dissonance","-","-","Business-partner role enactment","-","n/a (qualitative)",
  "A35: ERP dirty work clashes with BP role (abstract)","1 0.5 1 0 0 0 0 0 0 0 0","R6.N.L E5.S.L")
# ---- A37
f("A37","Digitalization of the control function raises MC effectiveness directly (b=.321)",
  "Digitalization of control function","Direct","-","-","MC effectiveness","+","Yes (p<.001)",
  "A37: digitalization -> MC effectiveness b=.321***","1 0 0 0 0 1 0 0 0 0 1","R5.S.Q")
f("A37","Digitalization raises information quality (b=.330), which is the strongest predictor of MC effectiveness (b=.555)",
  "Digitalization","Information quality","Information quality","-","MC effectiveness","+","Yes (p<.001)",
  "A37: digitalization -> IQ b=.330***; IQ -> MCE b=.555***","1 0.5 0 0 0 1 0 0 0 0 1","R1.S.Q R8.S.Q")
f("A37","Standardisation of the control function carries digitalization into information quality (indirect b=.255)",
  "Digitalization","Standardisation","Standardisation","-","Information quality","+ (indirect)","Yes (p<.001)",
  "A37: standardisation mediates digitalization -> IQ b=.255***","1 0.5 0 1 0 0 1 0 0 0 0","E4.S.Q")
f("A37","Digitalization does not significantly shift the locus of information (b=.113, p=.083) and the indirect path via centralised decision-making is ns (b=.035)",
  "Digitalization","Centralisation","Central locus of information","-","MC effectiveness","0","No",
  "A37: centralisation path ns","1 0 0 1 0 0 1 0 0 0 0","E10.N.Q")
# ---- A39
f("A39","Levers of control predict digital innovation in banks: interactive b=.281, beliefs b=.234, boundary b=.231 are significant; diagnostic b=.195 is not (p=.066); R2=.607",
  "Levers of control","MCS use shapes digital innovation","-","-","Digital innovation","+","Yes (p=.010-.048); diagnostic No",
  "A39: interactive b=.281*, beliefs .234*, boundary .231*; diagnostic ns","1 0.5 0 0.5 0 0.5 0.5 1 0 1 0","E3.S.Q")
# ---- A40
f("A40","Fully integrated ERP is associated with a limited contribution of MC (85% of coded references) versus partial integration (31%): MC tasks are automated away; with partial integration controllers keep costing, budgeting, dashboards, reporting",
  "ERP integration","Automation substitutes MC tasks","-","Degree of integration","MC contribution","- (substitution)","n/a (qualitative; share of coded references)",
  "A40: full ERP -> limited MC contribution 85% vs 31%","1 0 0.5 1 0 0.5 1 0 0 0 0","R6.N.L E10.S.L")
f("A40","Non-ERP systems: with specific software MC is limited to reporting; with standard software there is no distinct MC contribution (absorbed in accounting)",
  "Type of digital system","System type fixes MC place","-","-","MC contribution","-","n/a (qualitative)",
  "A40: system type determines MC role","1 0 0.5 1 0 0 1 0 0 0 0","R6.N.L")
f("A40","Organisational/behavioural factors limit what the technology delivers: centralised structures, family management, top-down policies, union influence; acceptance -> 83% high use, resistance -> 91% limited use; IT skills and training matter",
  "Acceptance vs resistance; structure; skills","Use conditions","-","Centralisation; ownership; unions","Level of digital use / decision effectiveness","+ / -","n/a (qualitative; share of coded references)",
  "A40: acceptance -> 83% high use; resistance -> 91% limited use","1 0 0 1 0 0 0.5 1 0 1 0.5","C_CULT.S.L C_TM.X.L C_COMP.S.L C_OWN.S.L R18.S.L R20.S.L")
# ---- A41 (abstract)
f("A41","Data analytics improves MC effectiveness not through use alone but through how it is used (diagnostic vs interactive) - abstract-level claim, no estimates in sheet",
  "Data analytics (diagnostic vs interactive use)","Mode of use","-","Mode of use","MC effectiveness","+ (mode-dependent)","Not reported in sheet",
  "A41: effect depends on mode of use (abstract)","1 0.5 0 0 0 1 0 0 0 0 1","R5.S~.U E13.S~.U")
# ---- A43
f("A43","SME intention to adopt digital MA is raised by self-efficacy (b=.349) and perceived ease of use (b=.231); R2=.663",
  "Self-efficacy; ease of use","Technology acceptance","-","-","Adoption intention","+","Yes (p=.001; p=.028)",
  "A43: self-efficacy b=.349**, ease of use b=.231*","0.5 0 0 0 0 0 0 0 0 1 0","R18.S.Q C_COMP.S.Q C_SME.S.Q C_TAM.S.Q")
f("A43","Perceived usefulness (b=.183, p=.065) and personal awareness (b=.145, p=.081) do not significantly raise adoption intention",
  "Perceived usefulness; personal awareness","Technology acceptance","-","-","Adoption intention","0","No",
  "A43: usefulness b=.183 ns; awareness ns","0.5 0 0 0 0 0 0 0 0 1 0","R18.N.Q C_TAM.N.Q")
# ---- A45
f("A45","Regulatory (coercive) pressure - data protection, e-invoicing, financial supervision, ESG - makes SMEs adopt AI cautiously, within compliance limits (reporting automation, secure analysis)",
  "Coercive regulatory pressure","Compliance-bounded adoption","-","-","AI adoption pattern","+ (bounded)","n/a (qualitative)",
  "A45: coercive pressure -> cautious, compliance-bounded AI","1 0 0 0.5 0 0 0.5 0 0 1 0","R18.S.L C_INST.S.L C_SME.S.L")
f("A45","Professional norms lead SMEs to use AI as decision support under professional supervision, keeping judgement over AI outputs",
  "Normative pressure from professional standards","Supervised AI use","-","-","AI use pattern","+","n/a (qualitative)",
  "A45: AI as supervised decision support; judgement retained","1 0.5 0.5 0 0 0 0 0 0 1 0","R18.S.L R15.S~.L C_INST.S.L")
f("A45","Peer and industry practice (mimetic/normative) encourage incremental, operations-oriented AI adoption, requiring data literacy",
  "Mimetic/normative pressure","Imitation and selection","-","-","Incremental AI adoption","+","n/a (qualitative)",
  "A45: peer practice -> incremental adoption","1 0 0 0 0 0 0 0 0 1 0","R18.S.L C_INST.S.L C_COMP.S.L")
f("A45","Internal norms translate external pressures into internal AI, data-security and governance policies",
  "External pressures","Translation into internal policy","Internal norms/policies","-","Structured, controlled AI integration","+","n/a (qualitative)",
  "A45: external pressure translated into internal AI policy","1 0 0 1 0 0 0.5 0 0 1 0","R20.S.L")
f("A45","Professional roles shift from recording toward analytical, interpretive and advisory functions; education/knowledge norms build interpretive and challenging skills that improve integration of AI outputs into managerial decisions",
  "Educational/knowledge norms","Interpretive competence","-","-","Integration of AI outputs in decisions","+","n/a (qualitative)",
  "A45: roles become analytic/interpretive; skills aid decision integration","1 0.5 1 0.5 0 0 0 0 0 1 0.5","R6.S.L R15.S~.L C_COMP.S.L")
# ---- A46
f("A46","More sophisticated MA information systems raise controller involvement in strategy development (b=.467)",
  "MAIS sophistication","Capability -> involvement","-","-","Controller involvement in strategy","+","Yes (p<.01)",
  "A46: MAIS sophistication -> strategic involvement b=.467**","1 0 1 0 0 0 0 0 0 0 0.5","R6.S.Q")
f("A46","The MAIS -> involvement link is weaker in family-controlled firms (interaction b=-.151)",
  "MAIS x family control","Ownership conditions the translation","-","Family control","Controller involvement","- (weaker)","Marginal (p<.10)",
  "A46: family control weakens link b=-.151 (p<.10)","1 0 1 0.5 0 0 0 0 0 1 0","E13.S.Q C_OWN.S.Q")
f("A46","Supplementary tests: the increase in involvement comes from data/information quality, not from time freed by automation",
  "Information quality vs time saving","Quality, not time","-","-","Controller involvement","+ (quality) / 0 (time)","Supplementary analysis",
  "A46: quality, not time saved, drives involvement","1 0.5 1 0 0 0 0 0 0 0 0","E12.S.Q E1.N.Q")
# ---- A47
f("A47","The traditional controller role stays dominant and business-partner requirements do not rise significantly over 2016-2023",
  "Time (digital era)","Role layering","-","-","Share of business-partner requirements in ads","0","No (H1 rejected)",
  "A47: BP requirements flat 2016-2023","0.5 0 1 0 0 0 0 0 0 0 0","R6.N.Q")
f("A47","Digitalization/automation requirements and sustainability/ESG responsibilities in controller ads rise sharply",
  "Time","Layering of responsibilities","-","-","Digital and ESG requirements","+","Yes (H2, H3 supported)",
  "A47: digital & ESG requirements rise","1 0 0.5 0.5 0 0 0 0 0 0 0","E9.S.D")
f("A47","Across ads, digitalization requirements co-occur with business-partner tasks (b=.157) although BP does not trend upward",
  "Digitalization requirements","Co-occurrence","-","-","Business-partner tasks","+ (association)","Yes (p<.01)",
  "A47: digitalization ~ BP tasks b=.157**","1 0 1 0 0 0 0 0 0 0 0","R6.S.Q")
# ---- A48
f("A48","Design-thinking Data Analytic Lifecycle: an iterative loop turning organisational data into MC plans and adjusting them from observed results; applied to performance data to design and adjust incentive mechanisms",
  "Data analytics + design thinking","Iterative design-adjust loop","-","-","MC plans; incentive design","n/a","n/a (qualitative; framework, no outcome results in sheet)",
  "A48: DAL-DT loop incl. reward design (framework only)","1 0.5 0 1 0.5 0.5 0 0 0.5 0 0","")
# ---- A49
f("A49","The PMS evolves under digital servitization: ecosystem data integrated and analysed by BI become performance information that is itself sold as a service",
  "Digital servitization; ecosystem data","PMS evolution","-","-","PMS content; new value-adding service","+","n/a (qualitative)",
  "A49: PMS evolves; performance data becomes a service","1 0 0 1 0 1 0 0 0 0 0.5","R5.S.L R17.S~.L")

NOT_EXTRACTABLE = ["A33", "A42"]
SECONDARY = [a for a, m in ART.items() if m["d"] == "S"]
EXCLUDED = [a for a, m in ART.items() if m["d"] == "X"]
