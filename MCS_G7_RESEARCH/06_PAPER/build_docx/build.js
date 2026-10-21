const fs = require("fs"), path = require("path");
const D = require("docx");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType, ImageRun, LevelFormat, BorderStyle, PageNumber, Footer, TabStopType } = D;
const data = JSON.parse(fs.readFileSync("data.json", "utf8"));
const FONT = "Times New Roman";
const dir = "..";
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
const T1 = [caption("**Table 1.** Management-module universe by country: sample size, median permanent full-time employees, share reporting each practice (among valid responses) and mean core score (number of practices present among r2, r4, r8; range 0–3)."),
  table(["Country", "N", "Median employees", "r2 monitoring (%)", "r4 targets (%)", "r8 bonuses (%)", "Mean core score"], data.t1, [1300, 1000, 1500, 1500, 1400, 1400, 1260])];
const T2 = [caption("**Table 2.** Latent class models, specification A (r1, r2, r4, r8, r10, r11; N = 6,294). Smallest class share in %."),
  table(["K", "Parameters", "Log-likelihood", "BIC", "Adjusted BIC", "Relative entropy", "Min. AvePP", "Smallest class (%)"], data.t2, [600, 1100, 1500, 1300, 1400, 1200, 1100, 1160])];
const T3 = [caption("**Table 3.** Best model by family and specification (BIC; ΔBIC relative to the best model of the specification). 'nrm1/nrm2' = one/two-dimensional continuous latent-trait models; 'hyb_K' = K classes × one trait."),
  table(["Spec.", "Family", "Model", "Parameters", "BIC", "ΔBIC"], data.t3, [800, 2600, 1300, 1300, 1700, 1660], ["c", "l", "c", "c", "c", "c"])];
const T4 = [caption("**Table 4.** Associations of the continuous score and the core score with outcomes (OLS, country and country-specific sector fixed effects, log size, log age; HC3 SE in parentheses), p-value of latent classes (K = 3) added to the continuous score (median over 50 pseudo-class draws), and 10-fold cross-validated RMSE for controls only / continuous score / classes. Associations only."),
  table(["Outcome", "Continuous score (per SD)", "Core score (per practice)", "Classes | score: p", "CV-RMSE (controls / score / classes)"], data.t4, [2300, 1700, 1700, 1300, 2360], ["l", "c", "c", "c", "c"])];
const afterPrefix = {
  "**4.1": [...T1], "**4.3": [...T2, figure("heat", 600), caption("**Figure 1.** Conditional response probabilities (%) of the three-class solution (specification A). Codes are 0-based and categories nominal; classes are ordered by mean core score and carry no substantive label.")],
  "**4.4": [...T3, figure("dim", 620), caption("**Figure 2.** Left: scree of polychoric eigenvalues (specification C; supporting only, unstable). Centre: two-factor loadings (assumes code order = ordinal order). Right: observed versus independence-expected combinations of r2, r4, r8.")],
  "**4.6": [...T4, figure("nl", 620), caption("**Figure 3.** Partial association of the continuous score with outcomes (cubic regression spline, 95% CI; dashed: linear). Histogram shows the score distribution.")]
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
// ---------- front matter
const title = "Management Control Practices as Configurations or Continuums? Exploratory Evidence from Seven Advanced Economies";
const subtitle = "An Investigation Using World Bank Enterprise Surveys Across G7 Countries";
const abstract = "Management control research treats controls as a package, whereas management-practice research summarises practices in aggregate scores. We ask whether observable control practices form qualitatively distinct configurations or mainly differ in managerial sophistication. Using the management module of the World Bank Enterprise Surveys for seven G7 economies in 2024–2025 (6,316 establishments, mostly with 20 or more employees), we handle survey skip patterns explicitly and compare latent class, continuous latent-trait and hybrid models on a common likelihood scale. Latent classes are poorly separated (relative entropy 0.53–0.60 with three to four classes), residual dependence is substantial, and the three-class solution is ordered along the sophistication gradient without crossing on monitoring, targets and bonuses. Continuous and hybrid models fit better than purely discrete ones, and classes add no explanatory power over a continuous score for productivity or growth, which show modest positive associations with the score. Cross-country measurement invariance is only partial. A small, unstable class with targets but few bonuses is a tentative lead. We distinguish accumulation, configuration and integration of practices (only the first two are observable) and propose a four-layer model separating observed practices, empirical structure, theoretical interpretation and associations. The findings are exploratory, cross-sectional and limited by unverified question wording for several items; they are not evidence of distinct control systems and say nothing about interactive control use, AI, internal audit or dynamic capabilities.";
const kw = "management control systems; management control packages; latent class analysis; levers of control; World Bank Enterprise Surveys; management practices";
const refs = [
 "Armenakis, A. A., & Harris, S. G. (2002). Crafting a change message to create transformational readiness. *Journal of Organizational Change Management, 15*(2), 169–183. https://doi.org/10.1108/09534810210423080",
 "Athey, S., & Stern, S. (1998). *An empirical framework for testing theories about complementarity in organizational design* (NBER Working Paper No. 6600). National Bureau of Economic Research.",
 "Bedford, D. S., & Malmi, T. (2015). Configurations of control: An exploratory analysis. *Management Accounting Research, 27*, 2–26. https://doi.org/10.1016/j.mar.2015.04.002",
 "Bedford, D. S., Malmi, T., & Sandelin, M. (2016). Management control effectiveness and strategy: An empirical analysis of packages and systems. *Accounting, Organizations and Society, 51*, 12–28. https://doi.org/10.1016/j.aos.2016.04.002",
 "Bhimani, A. (2020). Digital data and management accounting: Why we need to rethink research methods. *Journal of Management Control, 31*(1–2), 9–23. https://doi.org/10.1007/s00187-020-00295-z",
 "Bloom, N., Brynjolfsson, E., Foster, L., Jarmin, R., Patnaik, M., Saporta-Eksten, I., & Van Reenen, J. (2019). What drives differences in management practices? *American Economic Review, 109*(5), 1648–1683. https://doi.org/10.1257/aer.20170491",
 "Bloom, N., & Van Reenen, J. (2007). Measuring and explaining management practices across firms and countries. *Quarterly Journal of Economics, 122*(4), 1351–1408. https://doi.org/10.1162/qjec.2007.122.4.1351",
 "Grabner, I., & Moers, F. (2013). Management control as a system or a package? Conceptual and empirical issues. *Accounting, Organizations and Society, 38*(6), 407–419. https://doi.org/10.1016/j.aos.2013.09.002",
 "Hyland, M. C., Francis, D. C., & Rodriguez Meza, J. (n.d.). *Are management practices failing or aiding the private sector in South America?* (Policy Research Working Paper No. 8783). World Bank. [Year and details to be completed from the original record.]",
 "Knudsen, D.-R. (2020). Elusive boundaries, power relations, and knowledge production: A systematic review of the literature on digitalization in accounting. *International Journal of Accounting Information Systems, 36*, 100441. https://doi.org/10.1016/j.accinf.2019.100441",
 "Malmi, T., & Brown, D. A. (2008). Management control systems as a package: Opportunities, challenges and research directions. *Management Accounting Research, 19*(4), 287–300. https://doi.org/10.1016/j.mar.2008.09.003",
 "Milgrom, P., & Roberts, J. (1995). Complementarities and fit: Strategy, structure, and organizational change in manufacturing. *Journal of Accounting and Economics, 19*(2–3), 179–208.",
 "Murrell, P., Karalashvili, N., & Francis, D. C. (2024). Transactional governance structures: New cross-country data and an application to the effect of uncertainty. *Journal of Law, Economics, and Organization, 40*(3), 891–929. [Earlier version: Francis, D. C., Karalashvili, N., & Murrell, P. (2018), World Bank Policy Research Working Paper 8564.]",
 "Nielsen, S. (2022). Management accounting and the concepts of exploratory data analysis and unsupervised machine learning: A literature study and future directions. *Journal of Accounting & Organizational Change, 18*(5), 811–853.",
 "Nylund, K. L., Asparouhov, T., & Muthén, B. O. (2007). Deciding on the number of classes in latent class analysis and growth mixture modeling: A Monte Carlo simulation study. *Structural Equation Modeling, 14*(4), 535–569.",
 "Scur, D., Sadun, R., Van Reenen, J., Lemos, R., & Bloom, N. (2021). The World Management Survey at 18: Lessons and the way forward. *Oxford Review of Economic Policy, 37*(2), 231–258. https://doi.org/10.1093/oxrep/grab009",
 "Simons, R. (1995). *Levers of control: How managers use innovative control systems to drive strategic renewal*. Harvard Business School Press.",
 "Teece, D. J. (2007). Explicating dynamic capabilities: The nature and microfoundations of (sustainable) enterprise performance. *Strategic Management Journal, 28*(13), 1319–1350. https://doi.org/10.1002/smj.640",
 "Tessier, S., & Otley, D. (2012). A conceptual development of Simons' Levers of Control framework. *Management Accounting Research, 23*(3), 171–185.",
 "Vermunt, J. K. (2010). Latent class modeling with covariates: Two improved three-step approaches. *Political Analysis, 18*(4), 450–469.",
 "Widener, S. K. (2007). An empirical analysis of the levers of control framework. *Accounting, Organizations and Society, 32*(7–8), 757–788."
];
const children = [
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 120 }, children: [new TextRun({ text: title, bold: true, size: 36, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: subtitle, italics: true, size: 26, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 360 }, children: [new TextRun({ text: "[Author name(s) and affiliation(s)] — Draft for internal review", size: 22, font: FONT })] }),
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: "Abstract", bold: true, size: 28, font: FONT })] }),
  body(abstract), body("**Keywords:** " + kw),
  new Paragraph({ children: [new D.PageBreak()] }),
  ...md("introduction.md"), ...md("literature_review.md"), ...md("methodology.md"), ...md("results.md"), ...md("discussion.md"),
  figure("model", 620), caption("**Figure 4.** Proposed four-layer model of observable management-control practices. Solid lines: structure or associations estimated in this study; dashed: theoretical interpretation not tested. No arrow implies causation."),
  ...md("theoretical_contribution.md"), ...md("limitations.md"),
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: "Data availability and reproducibility", bold: true, size: 28, font: FONT })] }),
  body("The analysis used a merged file of WBES microdata supplied by the research team (10,968 establishments, seven country-years). Scripts, seeds, software versions and an execution log are provided in the project repository (MCS_G7_RESEARCH/07_REPRODUCIBILITY). Bibliographic records were verified through publisher and repository metadata; full texts were not consulted, and a systematic literature search remains to be completed."),
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: "References", bold: true, size: 28, font: FONT })] }),
  ...refs.map(r => new Paragraph({ children: runs(r, { size: 21 }), spacing: { after: 100, line: 270 }, indent: { left: 567, hanging: 567 } }))
];
const doc = new Document({
  creator: "Research team", title,
  styles: { default: { document: { run: { font: FONT, size: 24 } } } },
  numbering,
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 20, font: FONT })] })] }) }, children }]
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync("../Beyond_MCS_Packages_WBES_G7.docx", b); console.log("ok", b.length); });
