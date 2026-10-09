"""Phase 4 - construct the indicators, document sample flow, and test whether a composite Inclusive Growth index is defensible.

Outputs
  data/processed/analytic_dataset.csv            (derived data; raw files untouched)
  outputs/04_INCLUSIVE_GROWTH_MEASUREMENT.xlsx
  outputs/04_MEASUREMENT_DECISION.md             (all numbers are inserted from the computed results)
A composite index is evaluated as an EXPLORATORY diagnostic only; PCA is used to *test* dimensionality, not to build the index.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from scipy import stats
from common import *
import build as B

A = B.analytic()
os.makedirs(os.path.join(ROOT, "data", "processed"), exist_ok=True)
A.to_csv(os.path.join(ROOT, "data", "processed", "analytic_dataset.csv"), index=False)
log(f"analytic dataset: {A.shape}; by country {A.country.value_counts().to_dict()}", "construction.log")

# ---------------------------------------------------------------- sample flow
rows = []
for c, g in A.groupby("country"):
    n0 = len(g)
    def step(name, n): rows.append(dict(country=c, step=name, n=int(n), dropped=None))
    step("Interviewed establishments", n0)
    step("  minus: l2 = -7 (not in business 3 FY ago; no baseline) -> excluded from growth samples", n0 - g.entrant_l2_m7.sum())
    step("  valid sales growth (d2>0 & n3>0)", g.g_sales_raw.notna().sum())
    step("  valid employment growth (l1>0 & l2>0)", g.g_emp_raw.notna().sum())
    step("  valid productivity growth (both)", g.g_lp_raw.notna().sum())
    step("  valid product/process innovation (h1,h5)", (g.prod_innov.notna() & g.proc_innov.notna()).sum())
    step("  valid digitalization proxy (c22b)", g.web.notna().sum())
    gm = g[B.X_MAIN + B.controls("growth")]
    step("  complete main regressors + growth controls", gm.notna().all(axis=1).sum())
    for k, (col, est, kind, dim, labx) in B.OUTCOMES.items():
        cols = [col] + B.X_MAIN + B.controls(kind)
        step(f"  MAIN SAMPLE {k} ({col}): outcome + X + controls complete", g[cols].notna().all(axis=1).sum())
flow = pd.DataFrame(rows)
flow["dropped"] = flow.groupby("country")["n"].diff().fillna(0).astype(int)
flow.loc[flow.step.str.contains("MAIN SAMPLE"), "dropped"] = np.nan   # separate model samples, not sequential exclusions
_ms = flow[flow.step.str.contains("MAIN SAMPLE")]
RNG = {c: (int(g.n.min()), int(g.n.max())) for c, g in _ms.groupby("country")}
for r in flow.itertuples():
    log(f"{r.country} | {r.step} | n={r.n}", "exclusions.log")

# ---------------------------------------------------------------- descriptives of indicators
IND = {"g_sales": "D1 sales growth (pp/yr, winsorised)", "g_sales_raw": "D1 sales growth (raw)", "g_sales_adew": "D1 sales growth (Adewumi-Zhang formula)",
       "g_lp": "D1 productivity growth (winsorised)", "lnlp_level": "D1 ln sales per worker (LCU, not pooled)", "g_emp": "D2 employment growth (winsorised)",
       "g_emp_raw": "D2 employment growth (raw)", "g_emp_dhs": "D2 DHS arc employment growth", "female_share": "D3 female share", "lowskill_prod_share": "D3 low-skilled share (production)",
       "skilled_prod_share": "skilled share (production)", "hs_share": "D3 high-school share (l9b)", "env_energy_mgmt": "D4 energy-mgmt adoption (ge8d)",
       "env_co2_monitor": "D4 CO2 monitoring (ge7)", "prod_innov": "X product innovation", "proc_innov": "X process innovation", "web": "X website",
       "etax_file": "X e-tax filing", "ln_size_init": "ln employment 3y ago", "ln_age": "ln(1+age)", "foreign_own": "foreign >=10%", "exporter": "exporter >=10%",
       "corporation": "corporation", "credit_access": "credit access"}
def wmean(x, w):
    m = x.notna() & w.notna(); return np.average(x[m], weights=w[m]) if m.any() else np.nan
desc = []
for c, g in A.groupby("country"):
    for k, l in IND.items():
        s = g[k]
        desc.append(dict(country=c, indicator=k, description=l, n=int(s.notna().sum()), mean=s.mean(), sd=s.std(), p1=s.quantile(.01), p50=s.median(), p99=s.quantile(.99),
                         min=s.min(), max=s.max(), weighted_mean_wstrict=wmean(s, g.w_strict_std)))
desc = pd.DataFrame(desc)

# ---------------------------------------------------------------- availability matrix
avail = pd.DataFrame([
    ("D1", "Sales growth", "d2, n3", "Y", "Y", "B", "Main"), ("D1", "Real sales growth", "no deflator", "N", "N", "E", "-"),
    ("D1", "Labour-productivity growth", "d2,n3,l1,l2", "Y", "Y", "B", "Main"),
    ("D2", "Employment growth (total)", "l1, l2", "Y", "Y", "B", "Main"),
    ("D3", "Female employment share", "l5 | l5a+l5b", "Y", "Y", "B", "Main (composition)"), ("D3", "Female employment growth", "-", "N", "N", "E", "-"),
    ("D3", "Low-skilled share (production workers)", "l4a1,l4a2,l4b", "Y", "Y", "B", "Main (composition)"),
    ("D3", "Production share of workforce", "l4*, l1", "Y", "Y", "B", "Descriptive"), ("D3", "Education: high-school share", "l9b", "Y", "Y (ceiling)", "C", "Descriptive"),
    ("D3", "Category-specific employment growth", "-", "N", "N", "E", "-"),
    ("D4", "Energy-management adoption", "ge8d", "Y", "Y", "A", "Main (practice)"), ("D4", "CO2 monitoring", "ge7", "Y", "Y", "A", "Main (practice)"),
    ("D4", "Green practice index (BMGc23a-j)", "-", "N", "N", "E", "-"), ("D4", "Environmental investment / energy efficiency / waste", "-", "N", "N", "E/D", "-"),
], columns=["dimension", "indicator", "WBES items", "Morocco", "Korea", "class_cross_country", "use"])

# ---------------------------------------------------------------- correlations among dimensions
COMP = ["g_sales", "g_emp", "female_share", "lowskill_prod_share", "env_energy_mgmt", "env_co2_monitor"]
def spearman_mat(g):
    return g[COMP].corr(method="spearman")
cors = {c: spearman_mat(g) for c, g in A.groupby("country")}
cors["Pooled (within-country z)"] = None
Z = A.copy()
for k in COMP:
    Z[k] = Z.groupby("country")[k].transform(lambda s: (s - s.mean()) / s.std())
cors["Pooled (within-country z)"] = Z[COMP].corr(method="spearman")
# pairwise N and p-values for pooled
pw = []
for i, a in enumerate(COMP):
    for b in COMP[i + 1:]:
        for c, g in list(A.groupby("country")) + [("Pooled", Z)]:
            m = g[[a, b]].dropna()
            r, p = stats.spearmanr(m[a], m[b]) if len(m) > 10 else (np.nan, np.nan)
            pw.append(dict(country=c, var1=a, var2=b, spearman=r, p_value=p, n=len(m)))
pw = pd.DataFrame(pw)

# ---------------------------------------------------------------- composite diagnostics (EXPLORATORY ONLY)
def kmo(R):
    R = np.asarray(R); inv = np.linalg.pinv(R)
    d = np.sqrt(np.outer(np.diag(inv), np.diag(inv))); part = -inv / d
    np.fill_diagonal(part, 0); r = R.copy(); np.fill_diagonal(r, 0)
    return (r ** 2).sum() / ((r ** 2).sum() + (part ** 2).sum())
def cronbach(X):
    X = np.asarray(X); k = X.shape[1]
    return k / (k - 1) * (1 - X.var(axis=0, ddof=1).sum() / X.sum(axis=1).var(ddof=1))
diag = []; schemes_out = {}
for c, g in list(Z.groupby("country")) + [("Pooled", Z)]:
    cc = g[COMP].dropna()
    R = cc.corr().values
    ev, evec = np.linalg.eigh(R); order = ev.argsort()[::-1]; ev = ev[order]; evec = evec[:, order]
    off = R[np.triu_indices(len(COMP), 1)]
    diag.append(dict(country=c, n_complete_6_indicators=len(cc), n_any_valid=int(g[COMP].notna().any(axis=1).sum()),
                     share_complete=round(len(cc) / len(g), 3), cronbach_alpha=cronbach(cc), mean_interitem_corr=off.mean(), max_abs_interitem_corr=np.abs(off).max(),
                     KMO=kmo(R), eig1=ev[0], eig1_share=ev[0] / len(COMP), eig2=ev[1], n_eig_gt1=int((ev > 1).sum()),
                     pc1_loadings=", ".join(f"{k}:{v:+.2f}" for k, v in zip(COMP, evec[:, 0] * np.sign(evec[:, 0].sum())))))
    # alternative composites on complete cases
    cc = cc.copy()
    s1 = cc.mean(axis=1)
    s2 = pd.concat([cc.g_sales, cc.g_emp, cc[["female_share", "lowskill_prod_share"]].mean(axis=1), cc[["env_energy_mgmt", "env_co2_monitor"]].mean(axis=1)], axis=1).mean(axis=1)
    w = np.abs(evec[:, 0]); s3 = (cc.values * (evec[:, 0] * np.sign(evec[:, 0].sum()))).sum(axis=1)
    s4 = cc[["g_sales", "g_emp"]].mean(axis=1)
    cc2 = cc.copy(); cc2["lowskill_prod_share"] = -cc2["lowskill_prod_share"]; s5 = cc2.mean(axis=1)
    s6 = cc[["g_sales", "g_emp", "female_share"]].mean(axis=1)
    S = pd.DataFrame({"S1 equal-weight indicators": s1, "S2 equal-weight dimensions": s2, "S3 PCA-PC1 weights": s3, "S4 growth only (D1+D2)": s4,
                      "S5 = S1 with low-skill sign reversed": s5, "S6 D1+D2+female share": s6})
    schemes_out[c] = S.corr(method="spearman")
    loo = {k: stats.spearmanr(s1, cc.drop(columns=k).mean(axis=1))[0] for k in COMP}
    schemes_out[c + "_leave_one_out"] = pd.Series(loo, name="spearman vs S1 when indicator dropped").to_frame()
diag = pd.DataFrame(diag)

# ---------------------------------------------------------------- strategy evaluation
d_pool = diag[diag.country == "Pooled"].iloc[0]
mean_ic = d_pool.mean_interitem_corr; alpha = d_pool.cronbach_alpha; kmo_ = d_pool.KMO; n_cc = int(d_pool.n_complete_6_indicators); n_all = len(A)
s2s5 = schemes_out["Pooled"].loc["S1 equal-weight indicators", "S5 = S1 with low-skill sign reversed"]
s2s4 = schemes_out["Pooled"].loc["S1 equal-weight indicators", "S4 growth only (D1+D2)"]
s2s3 = schemes_out["Pooled"].loc["S1 equal-weight indicators", "S3 PCA-PC1 weights"]
s1s2 = schemes_out["Pooled"].loc["S1 equal-weight indicators", "S2 equal-weight dimensions"]
strat = pd.DataFrame([
    ("Construct validity", "Each dimension has an explicit, separately interpretable meaning; no claim beyond what is measured.",
     "Inclusive growth is a policy-defined, formative concept; indicators are not interchangeable manifestations of one trait. Direction of low-skill share is normatively ambiguous.",
     "Same as B on 4-6 indicators; D4 is two practice items (not outcomes); D3 is composition, not inclusive employment growth."),
    ("Indicator availability", f"Each outcome estimated on its own complete-case sample (Morocco N {RNG['MAR'][0]}-{RNG['MAR'][1]}, Korea N {RNG['KOR'][0]}-{RNG['KOR'][1]}).",
     f"Complete cases on all 6 indicators: {n_cc} of {n_all} firms ({100*n_cc/n_all:.1f}%); Morocco only {100*diag[diag.country=='MAR'].share_complete.iloc[0]:.0f}%.", "Same missing-data loss as B (same indicators)."),
    ("Cross-country comparability", "Only A/B-class variables used; country-specific context kept explicit.", "Within-country z-scores remove level differences and with them the cross-country comparison of interest.",
     "Within-country z-scores as in B."),
    ("Normalisation", "None needed (natural units).", "Required and arbitrary (z-score, min-max, ranking each change results).", "Same."),
    ("Weighting assumptions", "None.", f"Required. Rank correlation among schemes: S1 vs S2 {s1s2:.2f}; S1 vs PCA weights {s2s3:.2f}; S1 vs growth-only {s2s4:.2f}; reversing the sign of low-skill share: {s2s5:.2f}.",
     "Same."),
    ("Dimensional coherence (reflective test)", "Not required.", f"Cronbach alpha {alpha:.2f}; mean inter-item Spearman {mean_ic:.3f}; KMO {kmo_:.2f} (below the usual 0.60 requirement).", "Same."),
    ("Policy interpretability", "High: each coefficient answers one question (growth? jobs? composition? practice?).", "Low: a composite hides trade-offs (e.g. sales growth vs productivity vs employment).", "Medium-low."),
], columns=["criterion", "Strategy A: separate models", "Strategy B: multidimensional index", "Strategy C: reduced index on comparable dimensions"])

# ---------------------------------------------------------------- write workbook
defs = pd.DataFrame([
    ("g_sales", "100*ln(d2/n3)/3, winsorised 1/99 within country", "D1", "Annualised log nominal sales growth over 3 FY (pp/yr)"),
    ("g_sales_adew", "(d2-n3)/d2", "D1 alt.", "Adewumi & Zhang formula (S_t-S_t-3)/S_t"), ("g_sales_cagr", "100*((d2/n3)^(1/3)-1)", "D1 alt.", "CAGR"),
    ("g_lp", "g_sales - g_emp", "D1", "Annualised log growth of sales per permanent FT employee"), ("lnlp_level", "ln(d2/l1)", "D1 level", "LCU; within-country use only"),
    ("g_emp", "100*ln(l1/l2)/3, winsorised 1/99 within country", "D2", "Annualised log growth of permanent FT employment"),
    ("g_emp_dhs", "100*((l1-l2)/(0.5(l1+l2)))/3", "D2 alt.", "Davis-Haltiwanger arc growth /3"), ("g_emp_cagr", "100*((l1/l2)^(1/3)-1)", "D2 alt.", "CAGR"),
    ("female_share", "(l5 | l5a+l5b)/l1", "D3", "Share of permanent FT employees who are female (single date)"),
    ("lowskill_prod_share", "l4b/(l4a1+l4a2+l4b)", "D3", "Low-skilled among production workers only"),
    ("hs_share", "l9b/100", "D3/desc", "High-school completers (percent route)"), ("env_energy_mgmt", "ge8d==1", "D4", "Energy-management adoption in last 3 years"),
    ("env_co2_monitor", "ge7==1", "D4", "CO2-emission monitoring in last 3 years"), ("prod_innov", "h1==1", "X", "Product innovation (3y)"),
    ("proc_innov", "h5==1", "X", "Process innovation (3y)"), ("web", "c22b==1", "X", "Website (digitalization proxy)"),
], columns=["indicator", "formula", "dimension", "note"])
with pd.ExcelWriter(os.path.join(OUT, "04_INCLUSIVE_GROWTH_MEASUREMENT.xlsx"), engine="openpyxl") as xw:
    pd.DataFrame({"note": ["Indicators are separate; no composite is used in the main analysis.", "Composite diagnostics are EXPLORATORY and exist only to test whether an index is justified.",
                           "Within-country z-scores are used for diagnostics; PCA tests dimensionality and is NOT used to construct an index."]}).to_excel(xw, sheet_name="README", index=False)
    defs.to_excel(xw, sheet_name="Indicator_definitions", index=False)
    avail.to_excel(xw, sheet_name="Availability_matrix", index=False)
    flow.to_excel(xw, sheet_name="Sample_flow", index=False)
    desc.to_excel(xw, sheet_name="Descriptives", index=False)
    for k, v in cors.items():
        v.to_excel(xw, sheet_name=("Corr_" + k.split(" ")[0])[:31])
    pw.to_excel(xw, sheet_name="Pairwise_corr_N", index=False)
    diag.to_excel(xw, sheet_name="Composite_diagnostics", index=False)
    for k, v in schemes_out.items():
        v.to_excel(xw, sheet_name=("Schemes_" + k)[:31])
    strat.to_excel(xw, sheet_name="Strategy_evaluation", index=False)
log("04 measurement workbook written", "construction.log")

# ---------------------------------------------------------------- decision memo (numbers inserted from results)
def get(c, a, b):
    m = pw[(pw.country == c) & (((pw.var1 == a) & (pw.var2 == b)) | ((pw.var1 == b) & (pw.var2 == a)))].iloc[0]; return m.spearman, m.p_value, m.n
rs = get("Pooled", "g_sales", "g_emp"); rf = get("Pooled", "g_emp", "female_share"); re_ = get("Pooled", "env_energy_mgmt", "env_co2_monitor"); rg = get("Pooled", "g_sales", "female_share")
rm = {c: get(c, "g_sales", "g_emp") for c in ["MAR", "KOR"]}
md = f"""# 04 - Inclusive Firm Growth: measurement decision

## Decision
**Strategy A (separate econometric models per dimension) is adopted. A composite Inclusive Growth Index is NOT constructed.**
Strategies B (full index) and C (reduced index) are evaluated only as exploratory diagnostics (workbook `04_INCLUSIVE_GROWTH_MEASUREMENT.xlsx`).

## What the data can measure
| Dimension | Measurable? | Comparable MAR-KOR? | Indicators used | Important limitation |
|---|---|---|---|---|
| D1 Economic growth | Yes | B (harmonizable) | annualised log sales growth; productivity growth = sales growth - employment growth | nominal LCU; no deflator; windows FY2019-22 (MAR) vs FY2020-23 (KOR); sales per worker, not value added |
| D2 Employment growth | Yes | B | annualised log growth of permanent full-time employment (l1 vs l2) | total only; survivors only; temporary workers not observed 3 years ago |
| D3 Social inclusion | Only as *composition at one date* | B | female share; low-skilled share of production workers | NOT growth of female/low-skilled employment (no category data 3 years ago); skill categories exist for production workers only; high-school share is at ceiling in Korea (class C) |
| D4 Environmental | Only 2 practice items | A (identical items) | energy-management adoption (ge8d); CO2 monitoring (ge7) | the Green Economy items (BMGc23a-j) used by Phan (2026) are absent; items are practices, not environmental outcomes |

Not measurable (class E, not used): real sales growth, growth of female/skilled/low-skilled employment, university-educated share, a 10-item green index, environmental investment, energy efficiency, waste management, digital technology adoption beyond a website.

## Why a composite index is not defensible
1. **Formative, not reflective.** Inclusive growth is a policy-defined concept whose components (output growth, jobs, workforce composition, environmental practice) *cause* the construct rather than being reflections of one latent trait. Reflective tools (Cronbach alpha, factor analysis) are therefore theoretically inappropriate, and a formative index needs externally justified weights that the literature does not supply.
2. **The indicators do not move together (empirical check).** On the six comparable indicators the mean inter-item Spearman correlation is {mean_ic:.3f}, Cronbach alpha is {alpha:.2f} and KMO is {kmo_:.2f} (Kaiser's 'miserable' band, 0.50-0.60; 0.60 or more is usually required), and the first principal component explains only {100*d_pool.eig1_share:.0f}% of the variance (16.7% would arise from six uncorrelated indicators). Examples (pooled, within-country z): sales growth vs employment growth rho = {rs[0]:.2f} (n={rs[2]}); employment growth vs female share rho = {rf[0]:.2f}; sales growth vs female share rho = {rg[0]:.2f}; energy-management vs CO2-monitoring rho = {re_[0]:.2f}. Within countries, sales vs employment growth: Morocco {rm['MAR'][0]:.2f}, Korea {rm['KOR'][0]:.2f}.
3. **Weights and signs drive the ranking.** Rank correlation between equal-weight-indicator and equal-weight-dimension composites is {s1s2:.2f}; with PCA weights {s2s3:.2f}; against a growth-only composite {s2s4:.2f}; reversing the (normatively ambiguous) sign of the low-skilled share gives {s2s5:.2f}.
4. **Missing-data loss (secondary argument).** Complete cases on all six indicators: Morocco {int(diag[diag.country=="MAR"].n_complete_6_indicators.iloc[0])} of 598 ({100*diag[diag.country=="MAR"].share_complete.iloc[0]:.0f}%), Korea {int(diag[diag.country=="KOR"].n_complete_6_indicators.iloc[0])} of 1,518 ({100*diag[diag.country=="KOR"].share_complete.iloc[0]:.0f}%). The loss is material for Morocco but is not by itself decisive; separate models keep each outcome's own sample (Morocco {RNG['MAR'][0]}-{RNG['MAR'][1]}, Korea {RNG['KOR'][0]}-{RNG['KOR'][1]} after also requiring regressors and controls).
5. **Construct validity.** D3 is composition, not inclusive growth, and D4 consists of two practice items. An index built on them would present a thin set of proxies as a complete measure of Inclusive Growth.
6. **Loss of the comparison of interest.** Cross-country comparability requires within-country standardisation, which removes between-country level differences (the object of the Morocco-Korea comparison).

PCA is reported only as a dimensionality test; it is not used to build an index.

## Consequences for the econometric design
* Separate models per dimension (Phase 5) with identical regressors (product innovation, process innovation, website) and controls.
* Innovation and digitalization are treated as **explanatory variables**, not as components of inclusive growth.
* D4 is estimated as two binary practice outcomes (logit) and labelled "environmental practice adoption", never "environmental sustainability outcome".
* Composite-index results, if ever shown, are exploratory and carry no inferential weight.
"""
open(os.path.join(OUT, "04_MEASUREMENT_DECISION.md"), "w").write(md)
print(diag[["country", "n_complete_6_indicators", "cronbach_alpha", "mean_interitem_corr", "KMO", "eig1_share"]].to_string())
print(flow[flow.step.str.contains("MAIN|complete main")].to_string())
