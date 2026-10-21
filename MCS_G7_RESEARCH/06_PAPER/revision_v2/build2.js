const fs = require("fs"), path = require("path");
const D = require("docx");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType, ImageRun, LevelFormat, BorderStyle, PageNumber, Footer, TabStopType } = D;
const data = JSON.parse(fs.readFileSync("data2.json", "utf8"));
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
const T = {
 t1: [cap("**Table 1.** Management-module universe by country: sample size, median permanent full-time employees, share reporting each practice among valid responses, and mean core score (number of practices present among r2, r4, r8; 0–3)."), table(["Country","N","Median employees","r2 monitoring (%)","r4 targets (%)","r8 bonuses (%)","Mean core score"], data.t1, [1300,1000,1500,1500,1400,1400,1260])],
 t2: [cap("**Table 2.** Latent class models, specification A (r1, r2, r4, r8, r10, r11; N = 6,294), retained from the earlier analysis (one to six classes). Smallest class in %."), table(["K","Parameters","Log-likelihood","BIC","Adjusted BIC","Relative entropy","Min. AvePP","Smallest class (%)"], data.t2, [600,1100,1500,1300,1400,1200,1100,1160])],
 t3: [cap("**Table 3.** Cross-country invariance (specification A). Upper panel: multi-group latent class models (ΔBIC relative to the best model within K). Lower panel: item-wise tests, freeing one item across countries (ΔBIC < 0 favours non-invariance)."),
       table(["K","Model","Parameters","BIC","ΔBIC"], data.t_mg, [600,4800,1200,1500,1260], ["c","l","c","c","c"]), new Paragraph({spacing:{after:80},children:[]}),
       table(["K","Item","LR","df","ΔBIC (free − invariant)","Verdict"], data.t_dif, [600,900,1100,800,2400,3560], ["c","c","c","c","c","l"])],
 t4: [cap("**Table 4.** Country-specific associations between the latent score (country-specific-prior posterior mean, per latent SD) and outcomes: slope [95% CI] (n). Country and sector fixed effects (sector within country), log size and log age; HC3. Heterogeneity: Cochran's Q and I²; random-effects mean."),
       table(["Country","Log sales per employee","Sales growth (annual)","Employment growth (annual)"], data.t_sl, [2000,2500,2400,2460], ["l","c","c","c"])],
 t5: [cap("**Table 5.** Tests of equality of country-specific slopes, productivity (6 df): robust Wald statistics across scores and specifications."), table(["Score","Country-specific control slopes","Covariance","Wald χ²","p"], data.t_sp, [3600,1700,1700,1100,1260], ["l","c","c","c","c"])],
 t6: [cap("**Table 6.** Firm-level moderators of the score–productivity association (interaction with the pooled-prior score, per SD): estimate [95% CI], unadjusted and Holm p, and estimate when θ×country terms are included."), table(["Moderator","N","Interaction [95% CI]","p","Holm p","With country slopes"], data.t_mo, [2400,800,2300,900,900,2060], ["l","c","c","c","c","c"])],
 t7: [cap("**Table 7.** Equifinality: equality of adjusted performance across combinations of r2, r4, r8 with the same core score (pooled; Wald test), and equivalence of productivity differences against an illustrative margin of ±0.05 log points."), table(["Outcome","Core score","Combinations","N","Wald χ²","p","Holm p"], data.t_eq, [2400,1000,1500,800,1000,1000,1260], ["l","c","c","c","c","c","c"]), new Paragraph({spacing:{after:80},children:[]}), table(["Core score","Contrast","Difference [95% CI]","Margin","Equivalent?"], data.t_ep, [1100,1800,3000,1500,1960], ["c","c","c","c","c"])]
};
const afterPrefix = {
 "**6.1": [...T.t1], "**6.2": [...T.t2, figure("dim", 600), caption("**Figure 2.** Retained structural evidence. Left: polychoric eigenvalues (supporting only). Centre: two-factor loadings (assumes code order = ordinal order). Right: observed versus independence-expected combinations of r2, r4, r8.")],
 "**6.3": [...T.t3], "**6.4": [...T.t4, figure("forest", 640), caption("**Figure 3.** Country-specific slopes of the latent score (95% CI), random-effects pooled mean and 95% prediction interval, by outcome."), ...T.t5],
 "**6.5": [...T.t6, figure("mods", 520), caption("**Figure 4.** Interactions of the score with firm-level moderators, productivity (95% CI).")], "**6.6": [...T.t7]
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

const title = "Universal Structure, Contextual Effectiveness? Exploratory Evidence on Management Control Practices in Seven Advanced Economies";
const subtitle = "A study using World Bank Enterprise Surveys for the G7 economies, 2024–2025";
const abstract = "Are management control practices universally effective, or does their effectiveness depend on their alignment with national and organisational contexts? Using the management-practices module of the World Bank Enterprise Surveys for seven G7 economies (6,316 establishments, mostly with 20 or more employees), we separate four ideas: universality of practices, of statistical structure, of effectiveness, and contextual fit. For six common items, practices share a dominant continuous dimension; latent classes are poorly separated (relative entropy 0.53–0.60) and add no explanatory power beyond a continuous score. Measurement invariance across countries is partial and depends on the number of classes, and the reliability of the score varies from 0.35 to 0.65. The association between the score and productivity is positive in most countries but close to zero in France and the United Kingdom, and its heterogeneity is statistically detectable in most, though not all, specifications; growth associations are small. Firm-level moderators, combinations of practices and nonlinearities are not reliably different from zero after multiple-testing correction, and equifinality is neither demonstrated nor rejected. Because implementation, integration and national context are not measured, contextual fit is treated as a theoretical interpretation and a research agenda, including a separate agenda for Morocco, rather than as an empirical finding. All results are exploratory, cross-sectional associations, and wording of several items could not be verified.";
const kw = "management control systems; contextual fit; management practices; latent class analysis; measurement invariance; institutional context; World Bank Enterprise Surveys";
const refs = [
 "Armenakis, A. A., & Harris, S. G. (2002). Crafting a change message to create transformational readiness. *Journal of Organizational Change Management, 15*(2), 169–183. https://doi.org/10.1108/09534810210423080",
 "Bedford, D. S., & Malmi, T. (2015). Configurations of control: An exploratory analysis. *Management Accounting Research, 27*, 2–26. https://doi.org/10.1016/j.mar.2015.04.002",
 "Bloom, N., Brynjolfsson, E., Foster, L., Jarmin, R., Patnaik, M., Saporta-Eksten, I., & Van Reenen, J. (2019). What drives differences in management practices? *American Economic Review, 109*(5), 1648–1683. https://doi.org/10.1257/aer.20170491",
 "Bloom, N., Sadun, R., & Van Reenen, J. (2012). The organization of firms across countries. *Quarterly Journal of Economics, 127*(4), 1663–1705. https://doi.org/10.1093/qje/qje029",
 "Bloom, N., & Van Reenen, J. (2007). Measuring and explaining management practices across firms and countries. *Quarterly Journal of Economics, 122*(4), 1351–1408. https://doi.org/10.1162/qjec.2007.122.4.1351",
 "Burns, J., & Scapens, R. W. (2000). Conceptualizing management accounting change: An institutional framework. *Management Accounting Research, 11*(1), 3–25. https://doi.org/10.1006/mare.1999.0119",
 "Chenhall, R. H. (2003). Management control systems design within its organizational context: Findings from contingency-based research and directions for the future. *Accounting, Organizations and Society, 28*(2–3), 127–168.",
 "Daanoune, & Tirhzaoui. (n.d.). *The changes in management control systems of industrial companies in Morocco: An exploratory study*. HAL working paper. [Authors' initials, year and details to be completed from the original record.]",
 "DiMaggio, P. J., & Powell, W. W. (1983). The iron cage revisited: Institutional isomorphism and collective rationality in organizational fields. *American Sociological Review, 48*(2), 147–160.",
 "Drazin, R., & Van de Ven, A. H. (1985). Alternative forms of fit in contingency theory. *Administrative Science Quarterly, 30*(4), 514–539.",
 "Grabner, I., & Moers, F. (2013). Management control as a system or a package? Conceptual and empirical issues. *Accounting, Organizations and Society, 38*(6), 407–419. https://doi.org/10.1016/j.aos.2013.09.002",
 "Gresov, C., & Drazin, R. (1997). Equifinality: Functional equivalence in organization design. *Academy of Management Review, 22*(2), 403–428.",
 "Hall, P. A., & Soskice, D. (Eds.). (2001). *Varieties of capitalism: The institutional foundations of comparative advantage*. Oxford University Press.",
 "Hammouch, Manta, & Palazzo. (2024). Adapting management control systems to organizational contingency factors: A study of Moroccan industrial companies. *Businesses*. [Volume and pages to be completed from the original record.]",
 "Harrison, G. L., & McKinnon, J. L. (1999). Cross-cultural research in management control systems design: A review of the current state. *Accounting, Organizations and Society, 24*(5–6), 483–506.",
 "Higgins, J. P. T., & Thompson, S. G. (2002). Quantifying heterogeneity in a meta-analysis. *Statistics in Medicine, 21*(11), 1539–1558. https://doi.org/10.1002/sim.1186",
 "Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics, 6*(2), 65–70.",
 "Malmi, T., & Brown, D. A. (2008). Management control systems as a package: Opportunities, challenges and research directions. *Management Accounting Research, 19*(4), 287–300. https://doi.org/10.1016/j.mar.2008.09.003",
 "McSweeney, B. (2002). Hofstede's model of national cultural differences and their consequences: A triumph of faith – a failure of analysis. *Human Relations, 55*(1), 89–118.",
 "Murrell, P., Karalashvili, N., & Francis, D. C. (2024). Transactional governance structures: New cross-country data and an application to the effect of uncertainty. *Journal of Law, Economics, and Organization, 40*(3), 891–929.",
 "Nielsen, S. (2022). Management accounting and the concepts of exploratory data analysis and unsupervised machine learning: A literature study and future directions. *Journal of Accounting & Organizational Change, 18*(5), 811–853.",
 "Otley, D. (2016). The contingency theory of management accounting and control: 1980–2014. *Management Accounting Research, 31*, 45–62.",
 "Scur, D., Sadun, R., Van Reenen, J., Lemos, R., & Bloom, N. (2021). The World Management Survey at 18: Lessons and the way forward. *Oxford Review of Economic Policy, 37*(2), 231–258. https://doi.org/10.1093/oxrep/grab009",
 "Simons, R. (1995). *Levers of control: How managers use innovative control systems to drive strategic renewal*. Harvard Business School Press.",
 "Teece, D. J. (2007). Explicating dynamic capabilities: The nature and microfoundations of (sustainable) enterprise performance. *Strategic Management Journal, 28*(13), 1319–1350. https://doi.org/10.1002/smj.640",
 "Tessier, S., & Otley, D. (2012). A conceptual development of Simons' Levers of Control framework. *Management Accounting Research, 23*(3), 171–185."
];
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: t, bold: true, size: 28, font: FONT })], spacing: { before: 360, after: 160 } });
const children = [
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 120 }, children: [new TextRun({ text: title, bold: true, size: 36, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: subtitle, italics: true, size: 26, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 360 }, children: [new TextRun({ text: "[Author name(s) and affiliation(s)] — Revised draft for internal review (version 2)", size: 22, font: FONT })] }),
  H1("Abstract"), body(abstract), body("**Keywords:** " + kw), new Paragraph({ children: [new D.PageBreak()] }),
  ...md("s1_intro.md"), ...md("s2_lit.md"), figure("frame", 600), caption("**Figure 1.** Conceptual framework: practices, structure, implementation/integration, context and outcomes. Solid = observed or estimated; dotted = unobserved mechanism; dashed = contextual moderation (theory). No arrow implies causation."),
  ...md("s3_hyp.md"), ...md("s4_data.md"), ...md("s5_strategy.md"), ...md("s6_results.md"), ...md("s7_disc.md"), ...md("s8_contrib.md"), ...md("s9_impl.md"), ...md("s10_lim.md"), ...md("s11_conc.md"),
  H1("Data availability and reproducibility"), body("Analyses used a merged WBES file supplied by the research team. Scripts, seeds, software versions and logs are in the project repository (MCS_G7_RESEARCH/02_SCRIPTS, 07_REPRODUCIBILITY, 08_CONTEXTUAL_FIT). The original manuscript and dataset were not overwritten."),
  H1("References"), ...refs.map(r => new Paragraph({ children: runs(r, { size: 21 }), spacing: { after: 100, line: 270 }, indent: { left: 567, hanging: 567 } }))
];
const doc = new Document({ creator: "Research team", title, styles: { default: { document: { run: { font: FONT, size: 24 } } } }, numbering,
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 20, font: FONT })] })] }) }, children }] });
Packer.toBuffer(doc).then(b => { fs.writeFileSync("MCS_Contextual_Fit_WBES_G7_v2.docx", b); console.log("ok", b.length); });
