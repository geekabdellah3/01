const fs = require("fs"), path = require("path");
const D = require("docx");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType, ImageRun, LevelFormat, BorderStyle, PageNumber, Footer, TabStopType } = D;
const data = JSON.parse(fs.readFileSync("data5.json", "utf8"));
const FONT = "Times New Roman";
const dir = ".";
// ---------- inline markdown -> runs
function runs(text, base = {}) {
  const out = []; const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g; let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), font: FONT, ...base }));
    const t = m[0];
    if (t.startsWith("**")) out.push(new TextRun({ text: t.slice(2, -2), bold: true, font: FONT, ...base }));
    else if (t.startsWith("`")) out.push(new TextRun({ text: t.slice(1, -1), font: "Courier New", size: 20, ...base }));
    else out.push(new TextRun({ text: t.slice(1, -1), italics: true, font: FONT, ...base }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), font: FONT, ...base }));
  return out;
}
const body = (t, o = {}) => new Paragraph({ children: runs(t), alignment: AlignmentType.JUSTIFIED, spacing: { after: 120, line: 300 }, ...o });
const caption = (t) => new Paragraph({ children: runs(t, { size: 20 }), spacing: { before: 60, after: 200 }, alignment: AlignmentType.LEFT });
const numbering = { config: [{ reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] };
let nlists = 0;
function newList() { const ref = "num" + (nlists++); numbering.config.push({ reference: ref, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }); return ref; }
// ---------- tables
const bd = { style: BorderStyle.SINGLE, size: 4, color: "999999" };
const borders = { top: bd, bottom: bd, left: bd, right: bd };
function table(head, rows, widths, align) {
  const total = widths.reduce((a, b) => a + b, 0);
  const cell = (t, w, hd, i) => new TableCell({ width: { size: w, type: WidthType.DXA }, borders, margins: { top: 50, bottom: 50, left: 80, right: 80 },
    shading: hd ? { fill: "E8EEF4", type: ShadingType.CLEAR, color: "auto" } : undefined,
    children: [new Paragraph({ alignment: i === 0 || (align && align[i] === "l") ? AlignmentType.LEFT : AlignmentType.CENTER, children: [new TextRun({ text: String(t), bold: hd, size: 18, font: FONT })] })] });
  return new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: widths,
    rows: [new TableRow({ tableHeader: true, children: head.map((h, i) => cell(h, widths[i], true, i)) }), ...rows.map(r => new TableRow({ children: r.map((c, i) => cell(c, widths[i], false, i)) }))] });
}
function figure(key, widthPx) {
  const f = data.figs[key]; const h = Math.round(widthPx * f.h / f.w);
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120 }, keepNext: true, children: [new ImageRun({ type: "png", data: fs.readFileSync(f.path), transformation: { width: widthPx, height: h }, altText: { title: key, description: key, name: key } })] });
}


const cap = (t) => caption(t);
const d4 = JSON.parse(fs.readFileSync("../revision_v4/data4.json", "utf8"));
const OUTH = ["Productivity", "Sales growth", "Employment growth"];
const T = {
 t1: [cap("**Table 1.** Management-module universe by country: sample size, median permanent full-time employees, share reporting each practice among valid responses, and mean core score (number of practices present among r2, r4, r8; 0–3)."), table(["Country","N","Median employees","r2 monitoring (%)","r4 targets (%)","r8 bonuses (%)","Mean core score"], data.t1, [1300,1000,1500,1500,1400,1400,1260])],
 t2: [cap("**Table 2.** Individual associations of monitoring, targets and incentives with performance (pooled; practices entered together; sector-by-country fixed effects, log size, log age; HC3): coefficient [95% CI]. Productivity = log sales per employee; growth outcomes are annualised three-year log changes."), table(["Practice","Productivity","Sales growth","Employment growth"], data.t_q1, [2300,2300,2200,2200], ["l","c","c","c"])],
 t3: [cap("**Table 3.** Combinations of practices: statistical interactions (coefficient [95% CI], p) and joint pairwise test."), table(["Term","Productivity","Sales growth","Employment growth"], data.t_q2, [2100,2500,2300,2100], ["l","c","c","c"])],
 t4: [cap("**Table 4.** Country-specific associations of each practice with productivity (separate regressions by country; coefficient [95% CI]); heterogeneity across countries (Cochran's Q, I²) and random-effects mean."), table(["Country","N","Monitoring","Targets","Incentives"], data.t_q3, [1500,800,2300,2300,2300], ["l","c","c","c","c"])],
 t5: [cap("**Table 5.** Tests of equality of each practice's coefficients across the seven countries (robust Wald, 6 df): p with HC3 errors (Holm-adjusted over the nine practice-by-outcome tests) and with sector-clustered errors."), table(["Practice","Productivity","Sales growth","Employment growth"], data.t_eq, [1700,2400,2400,2500], ["l","c","c","c"])],
 t6: [cap("**Table 6.** Organisational moderators of the practice–productivity associations: joint test of the three practice-by-moderator interactions (3 df) and Holm-adjusted p over the 18 tests (three outcomes × six moderators)."), table(["Moderator","N","Wald χ² (3 df)","p","Holm p"], data.t_mo, [3200,1000,1600,1500,1700], ["l","c","c","c","c"])],
 t7: [cap("**Table 7.** Out-of-sample comparison (10-fold cross-validation × 3, folds stratified by country and identical across models): RMSE for productivity, incremental R² over controls, RMSE for growth outcomes; lower panel: paired reductions in mean squared error for productivity (squared log points) with firm-level 95% CI and corrected resampled 95% CI (Nadeau–Bengio)."),
     table(["Model","RMSE productivity","Incremental R² (%)","RMSE sales growth","RMSE employment growth"], data.t_cv, [3600,1300,1400,1400,1300], ["l","c","c","c","c"]), new Paragraph({spacing:{after:80},children:[]}),
     table(["Comparison","Reduction [firm-level 95% CI]","Corrected 95% CI","Corrected p"], data.t_pw, [3500,2600,1900,1000], ["l","c","c","c"])],
 t8: [cap("**Table 8.** Transferability of the three-practice model for productivity: out-of-sample R² of a model estimated in the source country (rows) applied to the target (columns); LOCO = estimated on the other six countries; Local = estimated and cross-validated in the target; last row: local minus LOCO with paired bootstrap 95% CI."), table(["Source / Target","CAN","FRA","DEU","ITA","JPN","GBR","USA"], data.t_tr, [1700,1050,1050,1050,1050,1050,1050,1000])],
 tA: [cap("**Table A1.** Management control frameworks in a common notation and their observability in WBES (appendix; interpretive)."), table(["Framework","Specification (our notation)","WBES observability"], d4.t_spec, [2100,4700,2200], ["l","l","l"])]
};
const afterPrefix = {
 "**6.1 ": [...T.t1], "**6.2 ": [...T.t2], "**6.3 ": [...T.t3],
 "**6.4 ": [...T.t4, figure("forest", 640), caption("**Figure 2.** Country-specific associations of monitoring, targets and incentives with productivity (95% CI); Q-test p and I² by practice."), ...T.t5],
 "**6.5 ": [...T.t6], "**6.6 ": [...T.t7], "**6.8 ": [...T.t8],
 "**6.9 ": [figure("dim", 600), caption("**Figure 3.** Complementary analysis of latent structure (six common items). Left: polychoric eigenvalues; centre: two-factor loadings (assumes code order = ordinal order); right: observed versus independence-expected combinations of r2, r4, r8.")]
};
// ---------- md -> paragraphs
function md(file, opts = {}) {
  const lines = fs.readFileSync(path.join(dir, file), "utf8").split("\n"); const out = []; let listRef = null;
  for (const raw of lines) {
    const line = raw.trimEnd(); if (!line.trim()) { listRef = null; continue; }
    if (/^# /.test(line)) { out.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: line.replace(/^# /, ""), font: FONT, bold: true, size: 28 })], spacing: { before: 360, after: 160 } })); continue; }
    if (/^## /.test(line)) { out.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: line.replace(/^## /, ""), font: FONT, bold: true, size: 24 })], spacing: { before: 240, after: 120 } })); continue; }
    let mm;
    if ((mm = line.match(/^(\d+)\. (.*)/))) { if (!listRef) listRef = newList(); out.push(new Paragraph({ numbering: { reference: listRef, level: 0 }, children: runs(mm[2]), spacing: { after: 80, line: 290 } })); continue; }
    listRef = null;
    if (/^- /.test(line)) { out.push(new Paragraph({ numbering: { reference: "bul", level: 0 }, children: runs(line.slice(2)), spacing: { after: 80, line: 290 } })); continue; }
    if (/^\|/.test(line)) continue;
    out.push(body(line));
    for (const k of Object.keys(afterPrefix)) if (line.startsWith(k)) out.push(...afterPrefix[k]);
  }
  return out;
}


const title = "Monitoring, Targets and Incentives as Control Mechanisms: Individual, Joint and Cross-Country Associations with Performance in Seven Advanced Economies";
const subtitle = "Evidence on heterogeneity and transferability from the World Bank Enterprise Surveys (G7, 2024–2025)";
const abstract = "Structured management practices — monitoring, target setting and incentives (Bloom and Van Reenen, 2007) — are widely treated as transferable managerial technologies and correspond to core mechanisms of management control. Starting from these three observable practices, we ask whether they show the same individual and joint associations with performance in seven advanced economies (World Bank Enterprise Surveys, 6,316 establishments, mostly with 20 or more employees), and how far models of these associations transfer across countries. Entered separately, incentives show the strongest association with productivity (about 22% higher sales per employee), followed by monitoring (about 13%); targets show none. The association of incentives varies strongly across countries (I² = 79%; from 0.51 log points in Canada to 0.05 in France), whereas those of monitoring and targets do not; no joint effects among practices and no reliable organisational contingencies are found. Nevertheless, a common model of the three practices is not improved on out of sample by models with country-specific or contingent slopes: the detectable heterogeneity is small relative to the cost of estimating it, so national slopes beat the common model in only about half of simulations at the estimated heterogeneity. Single-country models transfer worse than local models in 93% of source-target pairs, but a model estimated on the other six countries performs close to a local one. The results support practice-specific heterogeneity and conditional transferability; they do not show that each country needs its own control model, and integration and use of controls, institutional characteristics and the wording of several items could not be examined or verified. All results are exploratory cross-sectional associations.";
const kw = "management control practices; monitoring, targets and incentives; transferability; heterogeneity across countries; predictive validation; World Bank Enterprise Surveys";
const refs0 = [
 "Armenakis, A. A., & Harris, S. G. (2002). Crafting a change message to create transformational readiness. *Journal of Organizational Change Management, 15*(2), 169–183. https://doi.org/10.1108/09534810210423080",
 "Athey, S., & Stern, S. (1998). *An empirical framework for testing theories about complementarity in organizational design* (NBER Working Paper No. 6600). National Bureau of Economic Research.",
 "Bloom, N., Sadun, R., & Van Reenen, J. (2016). *Management as a technology?* (NBER Working Paper No. 22327). National Bureau of Economic Research.",
 "Bloom, N., & Van Reenen, J. (2007). Measuring and explaining management practices across firms and countries. *Quarterly Journal of Economics, 122*(4), 1351–1408. https://doi.org/10.1162/qjec.2007.122.4.1351",
 "Bloom, N., & Van Reenen, J. (2010). Why do management practices differ across firms and countries? *Journal of Economic Perspectives, 24*(1), 203–224. https://doi.org/10.1257/jep.24.1.203",
 "Burns, J., & Scapens, R. W. (2000). Conceptualizing management accounting change: An institutional framework. *Management Accounting Research, 11*(1), 3–25. https://doi.org/10.1006/mare.1999.0119",
 "Chenhall, R. H. (2003). Management control systems design within its organizational context: Findings from contingency-based research and directions for the future. *Accounting, Organizations and Society, 28*(2–3), 127–168.",
 "Daanoune, & Tirhzaoui. (n.d.). *The changes in management control systems of industrial companies in Morocco: An exploratory study*. HAL working paper. [Authors' initials, year and details to be completed from the original record.]",
 "DiMaggio, P. J., & Powell, W. W. (1983). The iron cage revisited: Institutional isomorphism and collective rationality in organizational fields. *American Sociological Review, 48*(2), 147–160.",
 "Donaldson, L. (2001). *The contingency theory of organizations*. Sage.",
 "Drazin, R., & Van de Ven, A. H. (1985). Alternative forms of fit in contingency theory. *Administrative Science Quarterly, 30*(4), 514–539.",
 "Ferreira, A., & Otley, D. (2009). The design and use of performance management systems: An extended framework for analysis. *Management Accounting Research, 20*(4), 263–282. https://doi.org/10.1016/j.mar.2009.07.003",
 "Grabner, I., & Moers, F. (2013). Management control as a system or a package? Conceptual and empirical issues. *Accounting, Organizations and Society, 38*(6), 407–419. https://doi.org/10.1016/j.aos.2013.09.002",
 "Hall, P. A., & Soskice, D. (Eds.). (2001). *Varieties of capitalism: The institutional foundations of comparative advantage*. Oxford University Press.",
 "Hammouch, Manta, & Palazzo. (2024). Adapting management control systems to organizational contingency factors: A study of Moroccan industrial companies. *Businesses*. [Volume and pages to be completed from the original record.]",
 "Harrison, G. L., & McKinnon, J. L. (1999). Cross-cultural research in management control systems design: A review of the current state. *Accounting, Organizations and Society, 24*(5–6), 483–506.",
 "Higgins, J. P. T., & Thompson, S. G. (2002). Quantifying heterogeneity in a meta-analysis. *Statistics in Medicine, 21*(11), 1539–1558. https://doi.org/10.1002/sim.1186",
 "Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics, 6*(2), 65–70.",
 "Kostova, T. (1999). Transnational transfer of strategic organizational practices: A contextual perspective. *Academy of Management Review, 24*(2), 308–324.",
 "Kostova, T., & Roth, K. (2002). Adoption of an organizational practice by subsidiaries of multinational corporations: Institutional and relational effects. *Academy of Management Journal, 45*(1), 215–233.",
 "Lawrence, P. R., & Lorsch, J. W. (1967). *Organization and environment: Managing differentiation and integration*. Division of Research, Harvard Business School.",
 "Malmi, T., & Brown, D. A. (2008). Management control systems as a package: Opportunities, challenges and research directions. *Management Accounting Research, 19*(4), 287–300. https://doi.org/10.1016/j.mar.2008.09.003",
 "McSweeney, B. (2002). Hofstede's model of national cultural differences and their consequences: A triumph of faith – a failure of analysis. *Human Relations, 55*(1), 89–118.",
 "Merchant, K. A., & Van der Stede, W. A. (n.d.). *Management control systems: Performance measurement, evaluation and incentives*. Pearson. [Edition and year to be specified.]",
 "Meyer, J. W., & Rowan, B. (1977). Institutionalized organizations: Formal structure as myth and ceremony. *American Journal of Sociology, 83*(2), 340–363.",
 "Milgrom, P., & Roberts, J. (1995). Complementarities and fit: Strategy, structure, and organizational change in manufacturing. *Journal of Accounting and Economics, 19*(2–3), 179–208.",
 "Nadeau, C., & Bengio, Y. (2003). Inference for the generalization error. *Machine Learning, 52*. [Pages to be verified against the original record.]",
 "Nielsen, S. (2022). Management accounting and the concepts of exploratory data analysis and unsupervised machine learning: A literature study and future directions. *Journal of Accounting & Organizational Change, 18*(5), 811–853.",
 "Otley, D. (1999). Performance management: A framework for management control systems research. *Management Accounting Research, 10*(4), 363–382.",
 "Otley, D. (2016). The contingency theory of management accounting and control: 1980–2014. *Management Accounting Research, 31*, 45–62.",
 "Simons, R. (1995). *Levers of control: How managers use innovative control systems to drive strategic renewal*. Harvard Business School Press.",
 "Teece, D. J. (2007). Explicating dynamic capabilities: The nature and microfoundations of (sustainable) enterprise performance. *Strategic Management Journal, 28*(13), 1319–1350. https://doi.org/10.1002/smj.640",
 "Tessier, S., & Otley, D. (2012). A conceptual development of Simons' Levers of Control framework. *Management Accounting Research, 23*(3), 171–185.",
 "Zbaracki, M. J. (1998). The rhetoric and reality of total quality management. *Administrative Science Quarterly, 43*, 602–636."
];
const allmd = ["s1_intro","s2_theory","s3_rq","s4_data","s5_strategy","s6_results","s7_disc","s8_contrib","s9_impl","s10_lim","s11_conc"].map(f => fs.readFileSync(f + ".md", "utf8")).join(" ") + abstract + JSON.stringify(d4.t_spec);
const refs = refs0.filter(r => { const m = r.match(/^([A-Za-zÀ-ÿ'\-]+).*?\((\d{4}|n\.d\.)\)/); if (!m) return true; return m[2] === "n.d." ? allmd.includes(m[1]) : (allmd.includes(m[1]) && allmd.includes(m[2])); });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: t, bold: true, size: 28, font: FONT })], spacing: { before: 360, after: 160 } });
const children = [
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 120 }, children: [new TextRun({ text: title, bold: true, size: 34, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: subtitle, italics: true, size: 25, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 360 }, children: [new TextRun({ text: "[Author name(s) and affiliation(s)] — Revised draft for internal review (version 5)", size: 22, font: FONT })] }),
  H1("Abstract"), body(abstract), body("**Keywords:** " + kw), new Paragraph({ children: [new D.PageBreak()] }),
  ...md("s1_intro.md"), ...md("s2_theory.md"), figure("frame", 620), caption("**Figure 1.** From structured management practices to control mechanisms, associations with performance, heterogeneity and transferability. Solid arrows: observed or estimated; dotted: unobserved; no arrow implies causation."),
  ...md("s3_rq.md"), ...md("s4_data.md"), ...md("s5_strategy.md"), ...md("s6_results.md"), ...md("s7_disc.md"), ...md("s8_contrib.md"), ...md("s9_impl.md"), ...md("s10_lim.md"), ...md("s11_conc.md"),
  H1("Data availability and reproducibility"), body("Analyses used a merged WBES file supplied by the research team. Scripts, seeds, software versions and logs are in the project repository (MCS_G7_RESEARCH/02_SCRIPTS, 07_REPRODUCIBILITY, 08_CONTEXTUAL_FIT). Earlier versions of the manuscript and the dataset were not overwritten."),
  H1("References"), ...refs.map(r => new Paragraph({ children: runs(r, { size: 21 }), spacing: { after: 100, line: 270 }, indent: { left: 567, hanging: 567 } })),
  H1("Appendix A. Management control frameworks in a common notation"), body("The appendix records how the control frameworks used in Section 2.2 can be written in a common notation and what WBES observes of each. It is interpretive and does not define the aim of the analysis."), ...T.tA
];
const doc = new Document({ creator: "Research team", title, styles: { default: { document: { run: { font: FONT, size: 24 } } } }, numbering,
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 20, font: FONT })] })] }) }, children }] });
Packer.toBuffer(doc).then(b => { fs.writeFileSync("MCS_Practices_Transferability_WBES_G7_v5.docx", b); console.log("ok", b.length); });
