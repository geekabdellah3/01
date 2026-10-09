"""Phase 6 - robustness and validation.

Tier labels
  T2  pre-specified robustness checks demanded by the research brief (checks R01-R12, diagnostics V1-V4)
  T3  EXPLORATORY analyses (sector / firm-size heterogeneity, alternative digital proxies, Morocco-only education outcome)
Every result - including non-significant coefficients - is written to results/*.csv; nothing is dropped after the fact.
Outputs: results/robustness_results.csv, vif.csv, influence.csv, heterogeneity.csv, missing_inclusion.csv, firth_d4.csv, sample_flow_checks.csv
"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor, OLSInfluence
from scipy import stats
from common import *
import build as B, svy
spec = importlib.util.spec_from_file_location("reg", os.path.join(os.path.dirname(os.path.abspath(__file__)), "05_run_regressions.py"))
R5 = importlib.util.module_from_spec(spec); spec.loader.exec_module(R5)
RES = R5.RES

A = B.analytic()
ALL = []; M4ALL = []
def keep(res, m4, cid, tier, desc):
    r = res[res.term.isin(B.X_MAIN + ["Korea"] + [f"{v}:Korea" for v in B.X_MAIN])].drop(columns=["tier"], errors="ignore").copy()
    r.insert(0, "check_id", cid); r.insert(1, "tier", tier); r.insert(2, "description", desc); ALL.append(r)
    if m4 is not None and len(m4):
        m = m4.drop(columns=["tier"], errors="ignore").copy(); m.insert(0, "check_id", cid); m.insert(1, "tier", tier); m.insert(2, "description", desc); M4ALL.append(m)
    print(f"{cid}: {desc} -> {r.groupby('model').size().to_dict()}")

def O(**over):
    """Copy of main OUTCOMES with outcome column / estimator overridden: O(D1_sales='g_sales_adew')."""
    o = dict(B.OUTCOMES)
    for k, v in over.items():
        col, est = (v, None) if isinstance(v, str) else v
        old = o[k]; o[k] = (col, est or old[1], old[2], old[3], old[4])
    return o
def run(df, cid, tier, desc, **kw):
    res, m4 = R5.run_main(df, tag=cid, **kw); keep(res, m4, cid, tier, desc); return res

# ------------------------------------------------------------------ R01-R03 weights and variance
run(A, "R01", "T2", "Unweighted OLS/logit, HC1-type robust SE", weighted=False)
run(A, "R02a", "T2", "Weights wmedian (instead of wstrict)", wcol="w_median_std")
run(A, "R02b", "T2", "Weights wweak (instead of wstrict)", wcol="w_weak_std")
run(A, "R03", "T2", "Weighted, strata ignored (HC-type SE)", strata_ignore=True)
# ------------------------------------------------------------------ R04-R06 outliers
run(A, "R04", "T2", "Growth outcomes NOT winsorised", outcomes=O(D1_sales="g_sales_raw", D1_lp="g_lp_raw", D2_emp="g_emp_raw"))
Aw = A.copy()
for k in ["g_sales", "g_emp", "g_lp"]:
    Aw[k + "_w5"] = Aw.groupby("country")[k + "_raw"].transform(lambda s: B.winsor(s, .05, .95))
run(Aw, "R05", "T2", "Growth outcomes winsorised at 5/95 within country", outcomes=O(D1_sales="g_sales_w5", D1_lp="g_lp_w5", D2_emp="g_emp_w5"))
At = A.copy()
for k in ["g_sales", "g_emp", "g_lp"]:
    lo = At.groupby("country")[k + "_raw"].transform(lambda s: s.quantile(.01)); hi = At.groupby("country")[k + "_raw"].transform(lambda s: s.quantile(.99))
    At[k + "_trim"] = At[k + "_raw"].where((At[k + "_raw"] >= lo) & (At[k + "_raw"] <= hi))
run(At, "R06", "T2", "Growth outcomes trimmed (observations outside country p1-p99 dropped)", outcomes=O(D1_sales="g_sales_trim", D1_lp="g_lp_trim", D2_emp="g_emp_trim"))
# ------------------------------------------------------------------ R07 alternative growth measures
Ag = A.copy(); Ag["g_lp_cagr"] = Ag["g_sales_cagr"] - Ag["g_emp_cagr"]
run(Ag, "R07a", "T2", "Alternative growth: sales (S_t-S_t-3)/S_t [Adewumi-Zhang], employment DHS arc growth", outcomes=O(D1_sales="g_sales_adew", D2_emp="g_emp_dhs"), only=["D1_sales", "D2_emp"])
run(Ag, "R07b", "T2", "Alternative growth: CAGR (sales, employment, productivity)", outcomes=O(D1_sales="g_sales_cagr", D2_emp="g_emp_cagr", D1_lp="g_lp_cagr"), only=["D1_sales", "D2_emp", "D1_lp"])
# ------------------------------------------------------------------ R08 data-quality exclusions (documented in report)
ratio = A.sales_t / A.sales_t3
Ak = A.copy(); badK = (A.country == "KOR") & ((ratio > 5) | (ratio < 0.2))
for k in ["g_sales", "g_lp"]: Ak.loc[badK, k] = np.nan
log(f"R08a Korea implausible sales ratio (>5 or <0.2): {int(badK.sum())} firms set missing for sales/productivity growth", "exclusions.log")
run(Ak, "R08a", "T2", "Korea: sales ratio >5 or <0.2 (likely unit/entry errors) excluded from D1", only=["D1_sales", "D1_lp"])
Ah = A.copy(); heap = (A.country == "MAR") & ((A.sales_t3 / A.sales_t).round(4) == 0.9)
for k in ["g_sales", "g_lp"]: Ah.loc[heap, k] = np.nan
log(f"R08b Morocco heaping n3 = 0.9*d2: {int(heap.sum())} firms set missing for sales/productivity growth", "exclusions.log")
run(Ah, "R08b", "T2", "Morocco: 118 firms reporting sales 3y ago = exactly 90% of current sales excluded from D1", only=["D1_sales", "D1_lp"])
Akh = A.copy()
for k in ["g_sales", "g_lp"]: Akh.loc[badK | heap, k] = np.nan
run(Akh, "R08c", "T2", "Both data-quality exclusions (R08a + R08b)", only=["D1_sales", "D1_lp"])
# ------------------------------------------------------------------ R09 alternative controls
for cid, desc, fn in [
    ("R09a", "Minimal controls: size + sector", lambda kind: [("ln_size_init" if kind == "growth" else "ln_size_cur")] + B.SECTOR_DUMMIES),
    ("R09b", "Extended controls: + credit access + female top manager", lambda kind: B.controls(kind, True)),
    ("R09c", "Extended controls: + manager experience + R&D dummy (R&D is a possible mediator)", lambda kind: B.controls(kind) + ["mgr_exp", "rd_spend"]),
]:
    allres = []; allm4 = []
    for key, oc in B.OUTCOMES.items():
        res, m4 = R5.run_main(A, tag=cid, ctrl_override=fn(oc[2]), only=[key]); allres.append(res); allm4.append(m4)
    keep(pd.concat(allres, ignore_index=True), pd.concat(allm4, ignore_index=True), cid, "T2", desc)
# region FE (country-specific): dummies, base region per country dropped
Ar = A.copy(); regcols = []
for c, g in Ar.groupby("country"):
    levels = sorted(g.region.dropna().unique())[1:]
    for lv in levels:
        nm = f"reg_{c}_{int(lv)}"; Ar[nm] = ((Ar.country == c) & (Ar.region == lv)).astype(float); regcols.append(nm)
allres = []; allm4 = []
for key, oc in B.OUTCOMES.items():
    res, m4 = R5.run_main(Ar, tag="R09d", ctrl_override=B.controls(oc[2]) + regcols, only=[key]); allres.append(res); allm4.append(m4)
keep(pd.concat(allres, ignore_index=True), pd.concat(allm4, ignore_index=True), "R09d", "T2", "Country-specific sampling-region fixed effects added")
allres = []; allm4 = []
for key, oc in B.OUTCOMES.items():
    if oc[2] != "growth": continue
    c2 = [c if c != "ln_size_init" else "ln_size_cur" for c in B.controls("growth")]
    res, m4 = R5.run_main(A, tag="R09e", ctrl_override=c2, only=[key]); allres.append(res); allm4.append(m4)
keep(pd.concat(allres, ignore_index=True), pd.concat(allm4, ignore_index=True), "R09e", "T2", "Growth models with CURRENT size ln(l1) (mechanical size-growth link; Phan-style)")
# ------------------------------------------------------------------ R10 sensitivity to harmonisation
Ah2 = A.copy()
iso = Ah2.isic4_div
Ah2["sector3_isic"] = np.where(iso.between(10, 33), "Manufacturing", np.where(iso.between(45, 47), "Retail", np.where(iso.notna(), "Other services", None)))
Ah2["sec_Retail"] = (Ah2.sector3_isic == "Retail").astype(float).where(Ah2.sector3_isic.notna())
Ah2["sec_Other services"] = (Ah2.sector3_isic == "Other services").astype(float).where(Ah2.sector3_isic.notna())
run(Ah2, "R10a", "T2", "Sector from ISIC rev.4 division of main product (d1a2_v4) instead of sampling stratum a4a")
rawb2 = {c: pd.to_numeric(load(c)[0].b2b, errors="coerce").where(lambda s: s >= 0) for c in FILES}
# foreign-ownership threshold and exporter definition require the raw items -> rebuild per country in the same order as A
def rebuild(col_fn):
    return pd.concat([col_fn(c) for c in FILES], ignore_index=True)
b2b = rebuild(lambda c: rawb2[c].reset_index(drop=True)); d3b = rebuild(lambda c: pd.to_numeric(load(c)[0].d3b, errors="coerce").where(lambda s: s >= 0).reset_index(drop=True))
d3c = rebuild(lambda c: pd.to_numeric(load(c)[0].d3c, errors="coerce").where(lambda s: s >= 0).reset_index(drop=True))
assert len(b2b) == len(A)
Af = A.copy(); Af["foreign_own"] = (b2b > 0).astype(float).where(b2b.notna()); run(Af, "R10b", "T2", "Foreign ownership = any foreign share (>0) instead of >=10%")
Af = A.copy(); Af["foreign_own"] = (b2b >= 50).astype(float).where(b2b.notna()); run(Af, "R10c", "T2", "Foreign ownership = majority foreign (>=50%)")
ex = d3b + d3c
Af = A.copy(); Af["exporter"] = (ex > 0).astype(float).where(ex.notna()); run(Af, "R10d", "T2", "Exporter = any export share (>0) instead of >=10%")
Af = A.copy(); Af["lowskill_prod_share"] = Af["lowskill_total_share"]; run(Af, "R10e", "T2", "Low-skilled = l4b / ALL permanent FT employees (not only production workers)", only=["D3_lowskill"])
Af = A.copy(); l5 = rebuild(lambda c: pd.to_numeric(load(c)[0].l5, errors="coerce").where(lambda s: s >= 0).reset_index(drop=True))
Af["female_share"] = (l5 / A.emp_t).where(l5 <= A.emp_t); run(Af, "R10f", "T2", "Female share from route l5 only (half-sample)", only=["D3_female"])
l5a = rebuild(lambda c: pd.to_numeric(load(c)[0].l5a, errors="coerce").where(lambda s: s >= 0).reset_index(drop=True))
l5b = rebuild(lambda c: pd.to_numeric(load(c)[0].l5b, errors="coerce").where(lambda s: s >= 0).reset_index(drop=True))
Af = A.copy(); Af["female_share"] = ((l5a + l5b) / A.emp_t).where((l5a + l5b) <= A.emp_t); run(Af, "R10g", "T2", "Female share from route l5a+l5b only (other half-sample)", only=["D3_female"])
# digitalization alternative proxies (T3 exploratory because not pre-specified as main)
Ae = A.copy(); Ae["web"] = Ae["etax_file"]
run(Ae, "R10h", "T3", "EXPLORATORY: digitalization proxy = e-filing of taxes (j36) instead of website")
Ai = A.copy()
# single 'any innovation' indicator in place of the two types
allres = []; allm4 = []
for key, oc in B.OUTCOMES.items():
    res, m4 = R5.run_main(Ai, tag="R10i", regs=["any_innov", "web"], only=[key])
    res = res.copy(); allres.append(res); allm4.append(m4)
r_ = pd.concat(allres, ignore_index=True).drop(columns=["tier"], errors="ignore"); r_.insert(0, "check_id", "R10i"); r_.insert(1, "tier", "T2"); r_.insert(2, "description", "Single 'any innovation' indicator (product or process) + website")
ALL.append(r_[r_.term.isin(["any_innov", "web", "Korea", "any_innov:Korea", "web:Korea"])]); print("R10i done")
# DK-as-category for the explanatory variables (keeps firms with DK answers)
Ad = A.copy(); dkcols = []
rawh1 = rebuild(lambda c: pd.to_numeric(load(c)[0].h1, errors="coerce").reset_index(drop=True)); rawh5 = rebuild(lambda c: pd.to_numeric(load(c)[0].h5, errors="coerce").reset_index(drop=True))
rawweb = rebuild(lambda c: pd.to_numeric(load(c)[0].c22b, errors="coerce").reset_index(drop=True))
for nm, raw_, col in [("dk_h1", rawh1, "prod_innov"), ("dk_h5", rawh5, "proc_innov"), ("dk_web", rawweb, "web")]:
    Ad[nm] = (raw_ == -9).astype(float); Ad.loc[Ad[nm] == 1, col] = 0.0; dkcols.append(nm)
allres = []; allm4 = []
for key, oc in B.OUTCOMES.items():
    res, m4 = R5.run_main(Ad, tag="R11", ctrl_override=B.controls(oc[2]) + dkcols, only=[key]); allres.append(res); allm4.append(m4)
keep(pd.concat(allres, ignore_index=True), pd.concat(allm4, ignore_index=True), "R11", "T2", "DK on innovation/website kept as separate category (DK dummies added) instead of listwise deletion")
# ------------------------------------------------------------------ R12 fractional logit for shares
run(A, "R12", "T2", "Fractional logit (quasi-binomial) for D3 shares instead of OLS", outcomes=O(D3_female=("female_share", "frac"), D3_lowskill=("lowskill_prod_share", "frac")), only=["D3_female", "D3_lowskill"])

pd.concat(ALL, ignore_index=True).to_csv(os.path.join(RES, "robustness_results.csv"), index=False)
if M4ALL: pd.concat(M4ALL, ignore_index=True).to_csv(os.path.join(RES, "robustness_m4_effects.csv"), index=False)

# ================================================================== diagnostics
# ---- V1 multicollinearity (VIF; unweighted design incl. controls)
vif = []
for key, (col, est, kind, dim, labx) in B.OUTCOMES.items():
    if key not in ("D1_sales", "D3_female"): continue
    for c, sub in [("MAR", A[A.country == "MAR"]), ("KOR", A[A.country == "KOR"]), ("Pooled", A)]:
        cols = B.X_MAIN + B.controls(kind) + (["Korea"] if c == "Pooled" else [])
        d = sub.dropna(subset=cols + [col])
        X = sm.add_constant(d[cols].astype(float))
        for j, nm in enumerate(X.columns):
            if nm == "const": continue
            vif.append(dict(sample=c, outcome_key=key, variable=nm, VIF=variance_inflation_factor(X.values, j), n=len(d)))
vif = pd.DataFrame(vif); vif.to_csv(os.path.join(RES, "vif.csv"), index=False)
corr = A[B.X_MAIN].corr(); corr.to_csv(os.path.join(RES, "regressor_correlations.csv"))
print("V1 VIF max:", vif.VIF.max().round(2))

# ---- V2 influence diagnostics (weighted LS Cook's D) and re-estimation dropping influential points
infl = []
for key, (col, est, kind, dim, labx) in B.OUTCOMES.items():
    if est != "ols": continue
    for c in ["MAR", "KOR"]:
        sub = A[A.country == c]; cols = B.X_MAIN + B.controls(kind) + [col]; d = sub.dropna(subset=cols)
        X = sm.add_constant(d[B.X_MAIN + B.controls(kind)].astype(float)); y = d[col].values
        wls = sm.WLS(y, X, weights=d.w_strict_std.values).fit(); cd = OLSInfluence(wls).cooks_distance[0]
        flag = cd > 4 / len(d)
        names = ["const"] + B.X_MAIN + B.controls(kind)
        r0 = svy.ols(y, X.values, w=d.w_strict_std.values, strata=(d.country + "_" + d.strata.astype(str)).values, names=names)
        keepm = ~flag
        r1 = svy.ols(y[keepm], X.values[keepm], w=d.w_strict_std.values[keepm], strata=(d.country + "_" + d.strata.astype(str)).values[keepm], names=names)
        for v in B.X_MAIN:
            j = names.index(v)
            infl.append(dict(outcome_key=key, country=c, regressor=v, n=len(d), n_influential_cook_gt_4_over_n=int(flag.sum()), max_cooks_d=float(cd.max()),
                             coef_all=r0.b[j], p_all=r0.p[j], coef_dropped=r1.b[j], p_dropped=r1.p[j]))
infl = pd.DataFrame(infl); infl.to_csv(os.path.join(RES, "influence.csv"), index=False)

# ---- V3 missing-data analysis: who is in the estimation sample? (standardised differences + inclusion logit)
mi = []; miss_logit = []
cov = ["ln_size_cur", "ln_age", "foreign_own", "exporter", "corporation", "web", "prod_innov", "proc_innov", "female_top_mgr"]
for key in ["D1_sales", "D2_emp", "D3_female", "D3_lowskill"]:
    col, est, kind = B.OUTCOMES[key][:3]
    for c in ["MAR", "KOR"]:
        sub = A[A.country == c].copy()
        inc = sub[[col] + B.X_MAIN + B.controls(kind)].notna().all(axis=1)
        for v in cov:
            a, b = sub.loc[inc, v], sub.loc[~inc, v]
            sd = np.sqrt((a.var() + b.var()) / 2)
            mi.append(dict(outcome_key=key, country=c, covariate=v, mean_included=a.mean(), mean_excluded=b.mean(), std_diff=(a.mean() - b.mean()) / sd if sd > 0 else np.nan,
                           n_included=int(inc.sum()), n_excluded=int((~inc).sum()), n_cov_valid_in_excluded=int(b.notna().sum())))
        Xc = sub[["ln_size_cur", "ln_age"]].copy(); Xc = Xc.fillna(Xc.mean()); Xc["foreign_own"] = sub.foreign_own.fillna(0); Xc["exporter"] = sub.exporter.fillna(0)
        Xc = sm.add_constant(pd.concat([Xc, pd.get_dummies(sub.sector3, drop_first=True).astype(float)], axis=1))
        m = sm.Logit(inc.astype(float), Xc).fit(disp=0, cov_type="HC1")
        lr = 2 * (m.llf - m.llnull)
        miss_logit.append(dict(outcome_key=key, country=c, n=len(sub), n_in_sample=int(inc.sum()), LR_chi2_selection_on_observables=lr, df=m.df_model, p_value=stats.chi2.sf(lr, m.df_model)))
pd.DataFrame(mi).to_csv(os.path.join(RES, "missing_inclusion.csv"), index=False); pd.DataFrame(miss_logit).to_csv(os.path.join(RES, "missing_inclusion_tests.csv"), index=False)

# ---- V4 Firth bias-reduced logit for D4 (sparse cells), unweighted
fr = []
for key in ["D4_energy", "D4_co2"]:
    col, est, kind = B.OUTCOMES[key][:3]
    for c, sub in [("MAR", A[A.country == "MAR"]), ("KOR", A[A.country == "KOR"]), ("Pooled", A)]:
        cols = B.X_MAIN + B.controls(kind) + (["Korea"] if c == "Pooled" else [])
        d = sub.dropna(subset=cols + [col]); X = np.column_stack([np.ones(len(d))] + [d[x].values for x in cols]); names = ["const"] + cols
        f = svy.firth(d[col].values, X, names); ml = svy.logit(d[col].values, X, names=names)
        for v in B.X_MAIN:
            j = names.index(v)
            fr.append(dict(outcome_key=key, sample=c, regressor=v, n=len(d), coef_firth=f.b[j], se_firth=f.se[j], p_firth=2 * stats.norm.sf(abs(f.t[j])), coef_ml_unweighted=ml.b[j], se_ml_unweighted=ml.se[j], p_ml_unweighted=ml.p[j]))
pd.DataFrame(fr).to_csv(os.path.join(RES, "firth_d4.csv"), index=False)

# ================================================================== T3 exploratory heterogeneity (Wald tests + subsample estimates)
def het(group_name, gfun):
    rows = []
    for key, (col, est, kind, dim, labx) in B.OUTCOMES.items():
        for c, sub in [("MAR", A[A.country == "MAR"]), ("KOR", A[A.country == "KOR"]), ("Pooled", A)]:
            cols = B.X_MAIN + B.controls(kind) + (["Korea"] if c == "Pooled" else [])
            d = sub.assign(_g=gfun(sub, kind)).dropna(subset=cols + [col, "_g"])
            if d._g.nunique() < 2: continue
            Xb = np.column_stack([np.ones(len(d))] + [d[x].values for x in cols]); names = ["const"] + cols
            inter = np.column_stack([d[x].values * d._g.values for x in B.X_MAIN] + [d._g.values]); inames = [f"{x}:G" for x in B.X_MAIN] + ["G"]
            X = np.column_stack([Xb, inter]); nm = names + inames
            f = {"ols": svy.ols, "logit": svy.logit, "frac": svy.fracit}[est]
            r = f(d[col].values, X, w=d.w_strict_std.values, strata=(d.country + "_" + d.strata.astype(str)).values, names=nm)
            F, p, q = svy.wald(r, [nm.index(f"{x}:G") for x in B.X_MAIN])
            rows.append(dict(group=group_name, outcome_key=key, sample=c, n=len(d), n_G1=int((d._g == 1).sum()), wald_F=F, wald_p=p, df_num=q))
            for x in B.X_MAIN:
                j0 = nm.index(x); j1 = nm.index(f"{x}:G"); V = r.V
                e1 = r.b[j0] + r.b[j1]; v1 = V[j0, j0] + V[j1, j1] + 2 * V[j0, j1]
                rows[-1].update({f"{x}_G0": r.b[j0], f"{x}_G0_p": r.p[j0], f"{x}_G1": e1, f"{x}_G1_p": 2 * stats.t.sf(abs(e1 / np.sqrt(v1)), r.df)})
    return pd.DataFrame(rows)
H1 = het("Non-manufacturing (G=1) vs manufacturing (G=0)", lambda d, k: (d.sector3 != "Manufacturing").astype(float).where(d.sector3.notna()))
H2 = het("Medium/large (G=1, >=20 employees) vs small (G=0)", lambda d, k: ((d.emp_t3 if k == "growth" else d.emp_t) >= 20).astype(float).where((d.emp_t3 if k == "growth" else d.emp_t).notna()))
pd.concat([H1, H2], ignore_index=True).to_csv(os.path.join(RES, "heterogeneity.csv"), index=False)

# ---- T3 Morocco-only education (high-school share) - exploratory, not pooled (Korea at ceiling)
Am = A[A.country == "MAR"]
cols = B.X_MAIN + B.CTRL_LEVEL; d = Am.dropna(subset=cols + ["hs_share"])
X = np.column_stack([np.ones(len(d))] + [d[x].values for x in cols]); r = svy.ols(d.hs_share.values, X, w=d.w_strict_std.values, strata=("MAR_" + d.strata.astype(str)).values, names=["const"] + cols)
t = r.table(); t["n"] = len(d); t["outcome"] = "hs_share (Morocco only)"; t.to_csv(os.path.join(RES, "morocco_education_exploratory.csv"), index=False)
log("06 robustness complete", "regressions.log")
print("robustness done")
