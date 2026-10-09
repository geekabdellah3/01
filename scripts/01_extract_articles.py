"""Phase 1 - structured extraction of the three source articles.

Content below was extracted by reading the PDFs (data/raw/*.pdf).  Every citation to a PDF page is
RESOLVED AUTOMATICALLY by searching the PDF text for a verbatim needle (page numbers are never typed by
hand).  If a needle is not found the script stops, so unverifiable page numbers cannot enter the output.
Page numbers = PDF page index (identical to the printed page number in all three PDFs).

Output: outputs/01_ARTICLE_EXTRACTION.xlsx
"""
import sys, os, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from common import ROOT, OUT, log

PDF = {"PHAN": "Phan_2026.pdf", "SIME": "Sime_Tadesse_2025.pdf", "ADEW": "Adewumi_Zhang_2026_JCP.pdf"}
CITE = {"PHAN": "Phan (2026), Discover Sustainability 7:848", "SIME": "Sime & Tadesse (2025), J. Innovation & Entrepreneurship 14:9",
        "ADEW": "Adewumi & Zhang (2026), J. Cleaner Production 548:147857"}

def norm(t):
    t = re.sub("\xad\\s*", "", t).replace("​", "").replace("‑", "-").replace("–", "-").replace("−", "-")
    t = re.sub(r"-\n", "", t)
    t = t.replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", t).lower()

def load_pages():
    pages = {}
    for k, f in PDF.items():
        txt = subprocess.run(["pdftotext", os.path.join(ROOT, "data", "raw", f), "-"], capture_output=True, text=True).stdout
        pages[k] = [norm(p) for p in txt.split("\f")]
    return pages
PAGES = load_pages()
VERIFY = []

def P(art, *needles):
    """Return 'p.X; p.Y' for the pages where every needle's first hit lies; raises if a needle is missing."""
    out = []
    for n in needles:
        nn = norm(n)
        hits = [i + 1 for i, p in enumerate(PAGES[art]) if nn in p]
        VERIFY.append(dict(article=art, needle=n, pages_found=",".join(map(str, hits)), verified=bool(hits)))
        if hits:
            out.append(hits[0])
    return "; ".join(f"p.{x}" for x in sorted(set(out))) if out else "UNVERIFIED"

# ---------------------------------------------------------------- 18 extraction fields -----------------------------
F = []   # (field_no, field, art, content, pages)
def add(no, field, art, content, *needles):
    F.append(dict(field_no=no, field=field, article=CITE[art], extracted_content=content,
                  pdf_pages=P(art, *needles) if needles else "n/a (not stated)"))

# ===== PHAN
add(1, "Research question", "PHAN", "Does adopting green economy practices (GEPs) make firms more likely to introduce product and process innovation? Which of ten GEP dimensions matter?", "investigates the impact of GEP adoption on firm innovation")
add(2, "Theoretical framework", "PHAN", "Resource-Based View (green physical-capital upgrading builds capabilities); Porter Hypothesis (environmental practice induces innovation offsets); Institutional Theory (coercive/normative/mimetic pressures, legitimacy).", "Resource-Based View", "Porter Hypothesis", "Institutional Theory explains")
add(3, "Hypotheses", "PHAN", "H1: Firms with greater adoption of GEPs are more likely to engage in innovation activities.", "Firms with greater adoption of GEPs are more likely to engage in innovation activities")
add(4, "Dataset and survey years", "PHAN", "World Bank Enterprise Surveys, Green Economy module, selected countries, 2018-2023. Original 46 countries; Timor-Leste, Indonesia, Peru, Bangladesh excluded (non-standardised module questions).", "four countries, namely Timor-Leste, Indonesia, Peru, and Bangladesh")
add(5, "Countries and sample sizes", "PHAN", "Final N = 18,860 firms, 42 countries after dropping missing observations. India = 7,486 (39.69%), Egypt 1,491; Morocco = 195 (1.03%); South Korea not included.", "final sample comprises 18,860", "Table 3 Data distribution by country")
add(6, "Dependent variables", "PHAN", "PRODUCT (binary: new product/service introduced; item h1) and PROCESS (binary: new or significantly improved process; item h5).", "Firm innovation is proxied by two binary indicators", "Table 1 Variable description")
add(7, "Independent variables", "PHAN", "GEP index = sum of 10 binary practice indicators (GEP1..GEP10, items BMGc23a-j), range 0-10; each GEP also entered separately.", "Each adopted practice is assigned a score of 1", "Table 1 Variable description")
add(8, "Moderating variables", "PHAN", "None estimated (cross-country institutional moderators only suggested as future research).", "National programs, such as carbon pricing")
add(9, "Mediating variables", "PHAN", "None estimated; mechanisms (resource efficiency, process redesign, eco-products) are discussed verbally only.", "prompting them to redesign production")
add(10, "Control variables", "PHAN", "CFL (checking/savings account, k6), DEBT (credit line/loan, k8), SIZE (ln full-time workers, l1), FO (foreign ownership %, b2b), LARGE (large-owner ownership, b3), AGE (ln years since founding, a14y; b5), SKILL (skilled/total workers; l4a1, l4a, l4a2, l4b). Country, year and industry fixed effects.", "The other firm-level control variables include cash flow", "All specifications incorporate country, year, and industry fixed effects")
add(11, "Exact mathematical equations", "PHAN", "(1) PRODUCT_ij = b0 + b1-5 GEP_ij + b6 CFL_ij + b7 DEBT_ij + b8 SIZE_ij + b9 FO_ij + b9 LARGE_ij + b9 AGE_ij + b9 SKILL_ij + e_i ;  (2) identical with PROCESS_ij as dependent variable. [Reproduced AS PRINTED: the coefficient label b9 is repeated four times and 'b1-5' is used although the baseline has one GEP index - a typographical inconsistency in the source.]", "Model 1 aims to investigate how the adoption of GEP affects product innovation", "Model 2 aims to investigate how the adoption of GEP affects process innovation")
add(12, "Variable operationalization", "PHAN", "See Variables sheet (Table 1 of the article).", "Table 1 Variable description")
add(13, "Estimation methodology", "PHAN", "Logistic regression (odds ratios), country/year/industry FE, robust SE clustered by country; baseline GEP index, then ten separate GEP regressions. No survey weights reported.", "We employ logistic regression to examine how the adoption of GEPs influences firm innovation")
add(14, "Main empirical results", "PHAN", "One more GEP raises odds of product innovation by 15.7% (OR 1.157, z=5.880) and process innovation by 19.4% (OR 1.194, z=8.885), p<0.01. All ten GEPs positive and significant; machinery upgrades largest (OR 2.419 product; 2.794 process). DEBT positive and significant; SIZE significant for product innovation only.", "odds ratio = 1.157", "machinery upgrades exhibit the most pronounced effect", "Table 6 The GEP index and firm innovation")
add(15, "Robustness checks", "PHAN", "Re-estimation excluding India (39.69% of sample): OR 1.185 (product) and 1.214 (process). Separate regressions per GEP to limit multicollinearity.", "Table 9 The GEP index and firm innovation, excluding India")
add(16, "Identification assumptions", "PHAN", "Selection on observables with country/year/industry FE; no instrument, no exogeneity test; the authors acknowledge that cross-sectional data prevent establishing cause and effect. 'Impact' wording in the title is therefore not causal evidence.", "Because green investments and innovation outcomes rarely occur simultaneously")
add(17, "Limitations", "PHAN", "GEP index records adoption, not intensity/quality; cross-sectional data, no time lags; national institutional environments not modelled; no panel structure in WBES.", "5.3 Limitations and future research", "absence of a consistent panel structure")
add(18, "Potential contribution to Inclusive Growth", "PHAN", "Supplies the ENVIRONMENTAL dimension (D4) and the product/process-innovation operationalisation (h1, h5) with explicit WBES codes. Introduces the 'inclusive green economy' framing (UNEP). It studies innovation as an OUTCOME of green practice - not an inclusive-growth outcome. Its GEP module (BMGc23a-j) is NOT in our Morocco/Korea files.", "inclusive green economy")

# ===== SIME & TADESSE
add(1, "Research question", "SIME", "(1) What makes up productivity, employment and innovation at the firm level in Africa? (2) Do different innovation types affect different labour groups and their productivities in the same way? (3) Do innovation intensity and selection effects differ?", "what makes up productivity, employment, and innovation at the firm level in Africa")
add(2, "Theoretical framework", "SIME", "Schumpeterian creative destruction; linear/induced/evolutionary innovation theories and Oslo Manual system view; compensation theory (Vivarelli): product innovation labour-friendly, process innovation labour-saving, offset by market mechanisms; CDM-type productivity literature.", "creative destruction", "Compensation mechanisms can offset")
add(3, "Hypotheses", "SIME", "No formal numbered hypotheses; three research questions only.", "what makes up productivity, employment, and innovation at the firm level in Africa")
add(4, "Dataset and survey years", "SIME", "WBES pseudo-panel pooled across all available waves per country (not only the last two), cohorts defined by legal status x firm size x industry (the only variables common to all datasets).", "pseudo-panel data from the World Bank Enterprise Surveys", "Pseudo-panel based on legal status, firm size, and industry type")
add(5, "Countries and sample sizes", "SIME", "Ethiopia, Ghana, Cameroon, Rwanda, Zambia, Senegal, Cote d'Ivoire, Kenya, Zimbabwe. 2,923 observations after dropping missing values on innovation (from ~11 thousand); 2,673 with >=1 innovation, 250 with none (all 250 non-innovators are in Cameroon).", "2923 observations after removing the missing values", "Table 1 Innovation by country")
add(6, "Dependent variables", "SIME", "Labour productivity = total annual sales / employment (all permanent FT, production, non-production, skilled, unskilled); Employment = number of permanent FT employees by the same categories.", "Computed productivity from employment and sales", "Variable choice and definitions")
add(7, "Independent variables", "SIME", "Treatment: innovation dummy (overall, product, process, R&D; =1 if any) and innovation 'dose' (count, 0-10).", "Innovation, dose")
add(8, "Moderating variables", "SIME", "None (mediation by adjustment time, market imperfection, complementarity left to future GSEM+PSM work).", "mediating effects of adjustment time")
add(9, "Mediating variables", "SIME", "None estimated.", "mediating effects of adjustment time")
add(10, "Control variables", "SIME", "Ownership shares (largest owner, private domestic/foreign, government, other), sales shares (national, indirect/direct exports), capacity utilisation (f1), hours per week (f2), start-up employment, power outages, generator use, firm size, legal status, international quality certificate, own website, foreign-licensed technology, formal training, external-bureaucracy index (factor analysis, polychoric correlations).", "Possible covariate variables", "external bureaucracy variables")
add(11, "Exact mathematical equations", "SIME", "No numbered equations. ATE = E(Y1 - Y0) and ATT = E(Y1 - Y0 | D=1) are given in prose; the symbols Y1, Y0 are not rendered in the published PDF (verified on the page image). Overlap condition P(Ti=1|Xi) < 1.", "average treatment effect on the treated (ATT)", "conditional independence and common support")
add(12, "Variable operationalization", "SIME", "Innovation dummy = 1 if any of nine innovation-related indicators is positive (inconsistency: dose is later said to range 0-10); productivity computed from sales/employment 'on recommendation from project leaders'.", "Create a dummy variable for innovation", "Innovation as a dose ranged from 0 to 10")
add(13, "Estimation methodology", "SIME", "Propensity score matching (ATT; nearest-neighbour/caliper/kernel types described; balance tests; Rosenbaum-type sensitivity gamma) and dose-response function (Hirano-Imbens GPS; Bia-Mattei/Guardabascio-Ventura extensions). Descriptive t-tests and point-biserial correlations first.", "Propensity score matching method", "Dose", "The sensitivity parameter")
add(14, "Main empirical results", "SIME", "Mixed: combined innovation raises employment of non-production and skilled workers but lowers productivity of permanent, non-production, skilled and unskilled workers; only production-worker productivity rises. Process innovation: positive on production-worker productivity and on employment of skilled/non-production/production workers, negative on non-production/skilled productivity. R&D: negative productivity effects (10%) except production workers; positive employment effects. Dose-response broadly consistent with PSM.", "overall combined effects of all types of innovations", "Conclusion and the way forward")
add(15, "Robustness checks", "SIME", "Different innovation types estimated separately (Tables 17-46), dose-response vs PSM comparison, matching-quality diagnostics (pseudo-R2, standardised bias, LR chi2) reported in Appendix B; sensitivity analysis described but gamma values not reported in main text.", "The sensitivity parameter", "Table 7 Impact of overall innovation on the productivity of labor")
add(16, "Identification assumptions", "SIME", "Conditional independence given observed covariates; common support; no unmeasured confounders (acknowledged as a source of hidden bias). Pseudo-panel cohorts rather than firm panel.", "conditional independence and common support", "hidden bias")
add(17, "Limitations", "SIME", "Data for other African countries unavailable; WBES content prevents alternative productivity and innovation measures; innovation dummy is imprecise; heavy missingness (11k to 2,923 obs.).", "Limitations and areas of future research", "intrinsic imprecision for innovation")
add(18, "Potential contribution to Inclusive Growth", "SIME", "Supplies the EMPLOYMENT and labour-segment logic: disaggregates employment and productivity by worker category (production/non-production, skilled/unskilled), showing that growth and job creation can diverge from productivity - exactly the trade-off an inclusive-growth framework must respect. Sales-per-worker definition of productivity (not value added).", "creation of jobs is accompanied by decreased productivity")

# ===== ADEWUMI & ZHANG
add(1, "Research question", "ADEW", "Does employee education enhance the financial effectiveness of green innovation (GI)? How do education levels shape this across contexts? How does the moderating effect vary by firm characteristics?", "Our investigation addresses three core questions")
add(2, "Theoretical framework", "ADEW", "Resource-Based View and human capital theory; absorptive capacity theory extended to 'stratified absorptive capacity'; sustainability transitions theory; cognitive-load argument for diminishing returns of formal education.", "stratified absorptive capacity", "sustainability transitions")
add(3, "Hypotheses", "ADEW", "H1: A firm's GI efforts positively affect its financial performance. H2: The positive financial-performance impact of GI is stronger at lower than at higher levels of employee education.", "Hypothesis 1. A firm's GI efforts will positively affect", "Hypothesis 2. The positive financial performance impact of GI is")
add(4, "Dataset and survey years", "ADEW", "WBES 2018-2019 cross-section; manufacturing and selected services (no agriculture, mining, finance).", "2018-2019 WBES")
add(5, "Countries and sample sizes", "ADEW", "8,941 firms, 42 countries: 5,155 manufacturing / 3,786 services; 1,606 North Africa, 5,504 Europe, 1,831 Asia; 6,213 SMEs / 2,728 large.", "aggregate sample of 8941 cross-sectional firm observations", "1606 North African firms")
add(6, "Dependent variables", "ADEW", "Sales growth = proportional change in sales over the past three years normalised by current-year sales, i.e. (S_t - S_t-3)/S_t [per text]; profit growth = sales growth x gross profit margin; GPM = (sales - cost of goods sold)/sales (mechanism test).", "Sales growth is expressed as the proportional change in sales over the past three years", "profit growth is determined by multiplying sales growth by the GPM")
add(7, "Independent variables", "ADEW", "Green innovation (GI): sector-standardised count of 10 eco-friendly investments adopted in the previous three years.", "standardized GI score was obtained as", "ecofriendly investments over the past three years")
add(8, "Moderating variables", "ADEW", "Education index = 0.5 x (share of FT permanent employees with secondary education) + 1.0 x (share with university degree), range 0-1.5; interaction GI x Education index. Heterogeneity by sector, region, firm size.", "we assigned a weight of 0.5 to secondary education", "Education index \u00d7 GI")
add(9, "Mediating variables", "ADEW", "None formal; GPM tested as a separate outcome ('mechanism robustness').", "Testing mechanism robustness")
add(10, "Control variables", "ADEW", "Competition, industry concentration, exporter, legal status (corporate), ln firm age, foreign ownership, SME, small/medium city, Asia, North Africa, manufacturing (IHS transform for zero/negative values).", "Measurement details of all variables")
add(11, "Exact mathematical equations", "ADEW", "(1) GI_std_is = (GI_is - mean GI_s)/sigma_s ; (2) Education index = [0.5(edu1) + 1.0(edu2)]/100 ; (3) y_i = GI_i b1 + x1_i b2 + u_i ; (4) GI_i = x1_i a1 + x2_i a2 + v_i  (2SLS; x2 = excluded instrument rd_std; interaction GI x Edu instrumented by rd_std x Edu).", "standardized GI score was obtained as", "our model is formally specified as")
add(12, "Variable operationalization", "ADEW", "See Variables sheet (Table 2 of the article). No WBES questionnaire codes are printed in the article.", "Measurement details of all variables")
add(13, "Estimation methodology", "ADEW", "OLS (with interaction) and 2SLS (Stata ivregress) with country-clustered robust SE; LIML for small KIBS sample; Heckman-type control function; nearest-neighbour PSM; bootstrap (200 reps).", "ivregress", "addressing self-selection bias")
add(14, "Main empirical results", "ADEW", "2SLS baseline: GI -> sales growth 0.111*** (SE 0.033), profit growth 0.070** (0.027); GI x Education -0.053* (0.031) for sales growth, -0.030 (0.031) for profit growth (n.s.). OLS GI effect only 0.029** (sales). Benefits of GI shrink as education rises: strongest in low-tech manufacturing, Europe, large firms.", "Regression results for the baseline analysis", "less is more")
add(15, "Robustness checks", "ADEW", "Weak-instrument tests (KP/Cragg-Donald 216.5), Durbin-Wu-Hausman, Heckman-type selection correction, PSM, GPM outcome, nonlinear education term (no inverted U), sector/region/size subsamples.", "Durbin-Wu-Hausman", "Analysis by gross profit margins")
add(16, "Identification assumptions", "ADEW", "Instrument rd_std (region-standardised R&D intensity) relevant and excluded from performance equation conditional on region FE - questionable because R&D may affect sales through non-GI channels (the authors recognise this for raw R&D); selection model excluded via government spending on education.", "region-standardized R&D intensity instrument", "exclusion restriction")
add(17, "Limitations", "ADEW", "Cross-sectional; cannot assess net profitability or implementation costs; GI types not decomposed.", "5.3. Limitations of the study", "reliance on cross-sectional data")
add(18, "Potential contribution to Inclusive Growth", "ADEW", "Supplies the SOCIAL-INCLUSION logic via workforce educational composition (human capital) and the idea that returns to green innovation are distributed unequally across education levels; sales-growth definition for D1; environmental dimension via GI. Its education index (secondary + university shares) is NOT reproducible with the Morocco/Korea files (only a high-school share exists).", "inclusive")

# ---------------------------------------------------------------- Variables sheet --------------------------------------
V = []
def var(art, role, name, definition, scale, formula, code, needle, ref):
    V.append(dict(article=CITE[art], role=role, variable_name_authors=name, definition=definition, measurement_scale=scale,
                  formula=formula, wbes_code_as_printed=code, pdf_page=P(art, needle), table_or_equation=ref))
A = "PHAN"
var(A, "Dependent", "PRODUCT", "Firm reports introducing new products or services", "binary 0/1", "1 if h1=Yes", "h1", "Table 1 Variable description", "Table 1")
var(A, "Dependent", "PROCESS", "Firm reports introducing new or significantly improved process", "binary 0/1", "1 if h5=Yes", "h5", "Table 1 Variable description", "Table 1")
for i, (nm, cd) in enumerate([("Heating and cooling improvements", "BMGc23a"), ("Climate-friendly energy generation on-site", "BMGc23b"), ("Machinery upgrades", "BMGc23c"),
                              ("Energy management systems", "BMGc23d"), ("Waste minimization, recycling, waste management", "BMGc23e"), ("Air pollution control measures", "BMGc23f"),
                              ("Water management measures", "BMGc23g"), ("Upgrades of vehicles, vessels or aircraft in the fleet", "BMGc23h"),
                              ("Improvement of lighting systems", "BMGc23i"), ("Other pollution control measures", "BMGc23j")], 1):
    var(A, "Independent", f"GEP{i}", nm, "binary 0/1", "1 if firm implemented the measure", cd, "Table 1 Variable description", "Table 1")
var(A, "Independent", "GEP", "Green Economy Practices index", "count 0-10", "GEP1+GEP2+...+GEP10", "BMGc23a-j", "Table 1 Variable description", "Table 1")
var(A, "Control", "CFL", "Firm has checking and/or savings account", "binary", "1 if yes", "k6", "Table 1 Variable description", "Table 1")
var(A, "Control", "DEBT", "Firm has line of credit or loan from a financial institution", "binary", "1 if yes", "k8", "Table 1 Variable description", "Table 1")
var(A, "Control", "SIZE", "Natural log of number of full-time workers", "continuous (log)", "ln(l1)", "l1", "Table 1 Variable description", "Table 1")
var(A, "Control", "FO", "Foreign ownership", "% 0-100", "share owned by foreign shareholders", "b2b", "Table 1 Variable description", "Table 1")
var(A, "Control", "LARGE", "Ownership by large shareholders", "% 1-100", "as reported", "b3", "Table 1 Variable description", "Table 1")
var(A, "Control", "AGE", "Ln(years from founding to survey year)", "continuous (log)", "ln(survey year - founding year)", "a14y; b5", "Table 1 Variable description", "Table 1")
var(A, "Control", "SKILL", "Skilled workers / total employment (skilled+semi+unskilled)", "share 0-1", "l4a1 / (l4a1+l4a2+l4b)  [as printed: l4a1; l4a; l4a2; l4b]", "l4a1; l4a; l4a2; l4b", "Table 1 Variable description", "Table 1")
A = "SIME"
var(A, "Dependent", "Labor productivity", "Total annual sales per employee (all permanent FT; production; non-production; skilled; unskilled)", "continuous (LCU/worker; logs used in tables e.g. 'logppw')", "sales / employment_category", "not printed (WBES sales and employment items)", "Variable choice and definitions", "Variable table p.15")
var(A, "Dependent", "Employment", "Number of employees by category (permanent FT, production, non-production, skilled, unskilled)", "count", "as reported in WBES", "not printed", "Variable choice and definitions", "Variable table p.15")
var(A, "Treatment", "Innovation (dummy)", "1 if any innovation (overall/product/process/R&D), 0 otherwise", "binary", "innovation_dummy = 1 if any of nine innovation indicators positive", "h1 is named for new product", "Create a dummy variable for innovation", "Data management, p.10")
var(A, "Treatment", "Innovation (dose)", "Number of innovation activities", "count 0-10 (as stated)", "count of innovation indicators", "not printed", "Innovation, dose", "Variable table p.15")
for nm, d in [("f1", "Capacity utilisation (%)"), ("f2", "Hours per week operated"), ("own_web", "Own website"), ("training_pfemp", "Formal training: permanent FT employees"),
              ("tec_foreign", "Technology: foreign licensed"), ("quace_int", "International quality certificate"), ("extbrcy", "External bureaucracy index (factor analysis)")]:
    var(A, "Covariate", nm, d, "see article", "as defined", "f1/f2 printed as codes; others are authors' Stata names", "Possible covariate variables", "Variable table p.16")
A = "ADEW"
var(A, "Dependent", "Sales growth", "Proportional change in sales over past three years normalised by current-year sales", "continuous (IHS where <=0)", "(S_t - S_t-3)/S_t [per text]", "not printed", "Sales growth is expressed as the proportional change in sales over the past three years", "Table 2")
var(A, "Dependent", "Profit growth", "Sales growth x gross profit margin", "continuous", "sales growth x GPM", "not printed", "profit growth is determined by multiplying sales growth by the GPM", "Table 2")
var(A, "Dependent", "Gross Profit Margin (GPM)", "(sales - cost of goods sold) / sales", "ratio", "(Sales - COGS)/Sales", "not printed", "Measurement details of all variables", "Table 2")
var(A, "Independent", "Green innovation (GI)", "Sector-standardised count (0-10) of eco-friendly investments in last 3 years", "z-score", "(GI_is - mean_s)/sd_s", "not printed (10 items listed in Table 1)", "standardized GI score was obtained as", "Eq. (1); Table 1")
var(A, "Moderator", "Education index", "0.5 x share secondary + 1.0 x share university among FT permanent employees", "index 0-1.5", "[0.5 edu1 + 1.0 edu2]/100", "not printed", "we assigned a weight of 0.5 to secondary education", "Eq. (2); Table 2")
var(A, "Instrument", "rd_std", "Firm R&D standardised by regional mean", "z-score", "(R&D_i - mean_region)/sd_region", "not printed", "region-standardized R&D intensity instrument", "Section 3.2.4; Table 2")
var(A, "Control", "SMEs / Large", "SMEs = 5-99 employees, large = 100+", "binary", "WBES size classes", "not printed", "Measurement details of all variables", "Table 2")
var(A, "Control", "Exporter; legal status; ln firm age; foreign ownership; city size; region; ISIC sector", "see Table 2", "binary / log", "see article", "not printed (ISIC ranges printed)", "Measurement details of all variables", "Table 2")

# ---------------------------------------------------------------- Key results -----------------------------------------
R = [
 dict(article=CITE["PHAN"], result="GEP index -> product innovation (odds ratio, logit, FE)", estimate="1.157***", stat="z = 5.880", n="18,860", pdf_page=P("PHAN", "Table 6 The GEP index and firm innovation"), table="Table 6"),
 dict(article=CITE["PHAN"], result="GEP index -> process innovation", estimate="1.194***", stat="z = 8.885", n="18,860", pdf_page=P("PHAN", "Table 6 The GEP index and firm innovation"), table="Table 6"),
 dict(article=CITE["PHAN"], result="Excluding India: GEP -> product / process", estimate="1.185*** / 1.214***", stat="z = 10.411 / 13.655", n="11,374 / 11,217", pdf_page=P("PHAN", "Table 9 The GEP index and firm innovation, excluding India"), table="Table 9"),
 dict(article=CITE["ADEW"], result="2SLS+interaction: GI -> sales growth", estimate="0.111***", stat="SE 0.033", n="8,941", pdf_page=P("ADEW", "Regression results for the baseline analysis"), table="Table 4"),
 dict(article=CITE["ADEW"], result="2SLS+interaction: GI -> profit growth", estimate="0.070**", stat="SE 0.027", n="8,941", pdf_page=P("ADEW", "Regression results for the baseline analysis"), table="Table 4"),
 dict(article=CITE["ADEW"], result="2SLS+interaction: GI x Education index -> sales growth", estimate="-0.053*", stat="SE 0.031", n="8,941", pdf_page=P("ADEW", "Regression results for the baseline analysis"), table="Table 4"),
 dict(article=CITE["ADEW"], result="OLS+interaction: GI -> sales growth (endogeneity bias comparison)", estimate="0.029**", stat="SE 0.012", n="8,941", pdf_page=P("ADEW", "Regression results for the baseline analysis"), table="Table 4"),
 dict(article=CITE["SIME"], result="PSM ATT: overall innovation -> labour productivity (ln, permanent workers), matched", estimate="-0.2155 (treated 14.396 vs control 14.789)", stat="t = -1.82 (10%)", n="2,923 pre-matching", pdf_page=P("SIME", "Table 7 Impact of overall innovation on the productivity of labor"), table="Table 7 (App. B)"),
 dict(article=CITE["SIME"], result="Firms with >=1 innovation vs none", estimate="2,673 vs 250", stat="-", n="2,923", pdf_page=P("SIME", "Table 1 Innovation by country"), table="Table 1 (App. A)"),
]

# ---------------------------------------------------------------- Equations sheet -------------------------------------
E = [
 dict(article=CITE["PHAN"], eq="(1)", latex_like="PRODUCT_ij = b0 + b1-5 GEP_ij + b6 CFL_ij + b7 DEBT_ij + b8 SIZE_ij + b9 FO_ij + b9 LARGE_ij + b9 AGE_ij + b9 SKILL_ij + e_i", note="as printed (repeated b9)", pdf_page=P("PHAN", "Model 1 aims to investigate how the adoption of GEP affects product innovation")),
 dict(article=CITE["PHAN"], eq="(2)", latex_like="PROCESS_ij = same right-hand side", note="as printed", pdf_page=P("PHAN", "Model 2 aims to investigate how the adoption of GEP affects process innovation")),
 dict(article=CITE["SIME"], eq="text", latex_like="ATE = E(Y1 - Y0); ATT = E(Y1 - Y0 | D=1); overlap P(T=1|X) < 1", note="symbols not rendered in PDF; no numbered equation", pdf_page=P("SIME", "average treatment effect on the treated (ATT)")),
 dict(article=CITE["ADEW"], eq="(1)", latex_like="GI_std_is = (GI_is - mean(GI_s)) / sigma_s", note="sector standardisation", pdf_page=P("ADEW", "standardized GI score was obtained as")),
 dict(article=CITE["ADEW"], eq="(2)", latex_like="Education index = (0.5*edu1 + 1.0*edu2) / 100", note="range 0-1.5", pdf_page=P("ADEW", "we assigned a weight of 0.5 to secondary education")),
 dict(article=CITE["ADEW"], eq="(3)", latex_like="y_i = GI_i b1 + x1_i b2 + u_i", note="structural equation", pdf_page=P("ADEW", "our model is formally specified as")),
 dict(article=CITE["ADEW"], eq="(4)", latex_like="GI_i = x1_i a1 + x2_i a2 + v_i", note="first stage; x2 = rd_std (and rd_std x Education for the interaction)", pdf_page=P("ADEW", "our model is formally specified as")),
]

def main():
    bad = [v for v in VERIFY if not v["verified"]]
    if bad:
        for b in bad: print("UNVERIFIED:", b["article"], repr(b["needle"]))
        raise SystemExit("Fix needles before writing output: unverifiable page citations are not allowed.")
    ex = pd.DataFrame(F).sort_values(["field_no", "article"], key=lambda s: s if s.name == "field_no" else s.map({CITE[k]: i for i, k in enumerate(["PHAN", "SIME", "ADEW"])}))
    wide = ex.pivot(index=["field_no", "field"], columns="article", values="extracted_content").reset_index()
    pages = ex.pivot(index=["field_no", "field"], columns="article", values="pdf_pages").reset_index()
    readme = pd.DataFrame({"note": [
        "Extracted by reading the three PDFs in data/raw. Page numbers are verified automatically against the PDF text (see Page_verification).",
        "'not printed' = the article does not print a WBES questionnaire code; no codes were inferred.",
        "Source inconsistencies are flagged in-line (Phan eq. b9 repeated; Sime & Tadesse innovation count 'nine indicators' vs dose 0-10).",
        "Statistical significance symbols are as printed by the authors."]})
    with pd.ExcelWriter(os.path.join(OUT, "01_ARTICLE_EXTRACTION.xlsx"), engine="openpyxl") as xw:
        readme.to_excel(xw, sheet_name="README", index=False)
        wide.to_excel(xw, sheet_name="Fields_1-18", index=False)
        pages.to_excel(xw, sheet_name="Field_pages", index=False)
        ex.to_excel(xw, sheet_name="Fields_long", index=False)
        pd.DataFrame(V).to_excel(xw, sheet_name="Variables", index=False)
        pd.DataFrame(E).to_excel(xw, sheet_name="Equations", index=False)
        pd.DataFrame(R).to_excel(xw, sheet_name="Key_results", index=False)
        pd.DataFrame(VERIFY).to_excel(xw, sheet_name="Page_verification", index=False)
    log(f"01 extraction written: {len(F)} field records, {len(V)} variables, {len(VERIFY)} verified needles", "extraction.log")
    print("ok", len(F), len(V), len(VERIFY))

if __name__ == "__main__":
    main()
