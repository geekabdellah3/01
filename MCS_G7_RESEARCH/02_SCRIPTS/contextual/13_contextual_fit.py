"""Deliverable D: cross-country heterogeneity of the MCS-performance association, organisational contingencies, equifinality.
All associations; exploratory. Measurement uncertainty handled with plausible values (M=20). Outcomes as in 06_outcomes."""
import os, sys, pickle, warnings
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
from lca_core import *
import statsmodels.api as sm, statsmodels.formula.api as smf
from scipy import stats
warnings.filterwarnings("ignore")
OUTD = os.path.join(ROOT, "08_CONTEXTUAL_FIT"); M = 20
d = load_analytic(); store = pickle.load(open(os.path.join(RES, "lca/lca_store.pkl"), "rb"))
raw = load_raw(); raw = raw[raw.r1.notna()].copy(); raw["firm_key"] = raw.cid + "_" + raw.source_row.astype(str)
extra = raw.set_index("firm_key")[["b2b", "d3b", "d3c", "b7", "b7a"]]
dd = d[store["A"]["keep"]].reset_index(drop=True).join(extra, on="firm_key")
nr = store["A"]["models"]["nrm1_1"]; nodes = nr["Xs"][:, 1]; post = nr["post"]
sign = -1 if np.corrcoef(post @ nodes, dd.S_core.fillna(dd.S_core.mean()))[0, 1] < 0 else 1
nodes = sign * nodes; dd["theta"] = post @ nodes; dd["theta_z"] = (dd.theta - dd.theta.mean()) / dd.theta.std()
# Regression calibration with COUNTRY-SPECIFIC priors: posterior of theta re-weighted by N(mu_c, sd_c); item parameters pooled.
# (Unconditional plausible values were tried first and rejected: they attenuate slopes by ~ the reliability.)
cidx = dd.cid.values; mu = {c: 0.0 for c in CORDER}; sd = {c: 1.0 for c in CORDER}
def reweight(c):
    r = stats.norm.pdf(nodes, mu[c], sd[c]) / stats.norm.pdf(nodes, 0, 1); pw = post[cidx == c] * r[None, :]; return pw / pw.sum(1, keepdims=True)
for it in range(60):
    for c in CORDER:
        pw = reweight(c); e1 = pw @ nodes; e2 = pw @ nodes ** 2; mu[c] = e1.mean(); sd[c] = float(np.sqrt(max(1e-4, e2.mean() - e1.mean() ** 2)))
tc = np.zeros(len(dd)); rel = []
for c in CORDER:
    pw = reweight(c); e1 = pw @ nodes; pv_ = (pw @ nodes ** 2) - e1 ** 2; tc[cidx == c] = e1
    rel.append(dict(country=c, prior_mean=mu[c], prior_sd=sd[c], reliability=float(np.var(e1) / (np.var(e1) + pv_.mean())), sd_EAP_country_prior=float(np.std(e1))))
dd["theta_c"] = tc; relt = pd.DataFrame(rel); print(relt.round(3))
# invariant-subset score: drop r8 (DIF in both K=3 and K=4 solutions)
it5 = ["r1", "r2", "r4", "r10", "r11"]; X5 = dd[[f"A_{c}" for c in it5]].fillna(-1).astype(int).values; nc5 = [int(X5[:, j].max()) + 1 for j in range(5)]
p5 = fit_param(X5, nc5, "nrm1", n_starts=2); t5 = p5["post"] @ p5["Xs"][:, 1]
if np.corrcoef(t5, dd.theta)[0, 1] < 0: t5 = -t5
dd["theta5"] = t5; dd["theta5_z"] = (t5 - t5.mean()) / t5.std()
w = lambda s: s.clip(s.quantile(.01), s.quantile(.99))
dd["sales_growth3y_ann"] = w(dd.sales_growth3y_ann); dd["emp_growth3y_ann"] = w(dd.emp_growth3y_ann)
dd["ln_lp"] = dd.groupby("cid").ln_lp.transform(lambda s: s.clip(s.quantile(.005), s.quantile(.995)))
# moderators (labels from 2024 data-dictionary snippets of other countries; unverified for the G7 files)
dd["foreign10"] = np.where(dd.b2b >= 10, 1.0, np.where(dd.b2b >= 0, 0.0, np.nan))
dd["exporter"] = np.where((dd.d3b.fillna(-1) >= 0) & (dd.d3c.fillna(-1) >= 0), ((dd.d3b + dd.d3c) > 0).astype(float), np.nan)
dd["ln_mgr_exp"] = np.log(dd.b7.where(dd.b7 > 0)); dd["female_mgr"] = dd.b7a.map({1: 1.0, 2: 0.0})
dd["small_firm"] = (dd.employees < 50).astype(float).where(dd.employees.notna())
OUT = {"ln_lp": "Log sales per employee", "sales_growth3y_ann": "Sales growth (ann.)", "emp_growth3y_ann": "Employment growth (ann.)"}
ctry = CORDER
def fit_country(y, xcol, data, c, weights=False):
    s = data[data.cid == c].dropna(subset=[y, xcol, "ln_emp", "ln_age"])
    f = f"{y} ~ {xcol} + ln_emp + ln_age + C(sector_c)"
    m = (smf.wls(f, s, weights=s.wmedian) if weights else smf.ols(f, s)).fit(cov_type="HC3")
    return m.params[xcol], m.bse[xcol], int(m.nobs), s
def het_stats(b, se):
    b, se = np.array(b), np.array(se); wt = 1 / se ** 2; bbar = (wt * b).sum() / wt.sum(); Q = (wt * (b - bbar) ** 2).sum(); k = len(b)
    I2 = max(0, (Q - (k - 1)) / Q) * 100; tau2 = max(0, (Q - (k - 1)) / (wt.sum() - (wt ** 2).sum() / wt.sum()))
    wr = 1 / (se ** 2 + tau2); bre = (wr * b).sum() / wr.sum(); sre = np.sqrt(1 / wr.sum())
    return dict(Q=Q, df=k - 1, p=stats.chi2.sf(Q, k - 1), I2=I2, tau=np.sqrt(tau2), b_fixed=bbar, b_random=bre, se_random=sre,
                pred_lo=bre - stats.t.ppf(.975, k - 2) * np.sqrt(tau2 + sre ** 2), pred_hi=bre + stats.t.ppf(.975, k - 2) * np.sqrt(tau2 + sre ** 2))
res = {}
# ---------- STEP 2: country-specific slopes with PV (Rubin) and EAP; invariant-subset and core-score sensitivity ----------
rows = []; hrows = []
for y, lab in OUT.items():
    for score, desc in [("theta_c", "latent trait, country-specific-prior EAP (per latent SD)"), ("theta_z", "EAP score (per SD of EAP)"), ("theta5_z", "5-item invariant-subset EAP (excl. r8)"), ("S_core", "core score (r2+r4+r8; per practice)")]:
        bs, ses = [], []
        for c in ctry:
            b, se, n, _ = fit_country(y, score, dd, c)
            s_ = dd[(dd.cid == c)].dropna(subset=[y, "ln_emp", "ln_age", score])
            bs.append(b); ses.append(se)
            rows.append(dict(outcome=lab, score=desc, country=c, N=len(s_), beta=b, se=se, ci_lo=b - 1.96 * se, ci_hi=b + 1.96 * se))
        h = het_stats(bs, ses); h.update(outcome=lab, score=desc); hrows.append(h)
cs = pd.DataFrame(rows); hs = pd.DataFrame(hrows)
# weighted sensitivity (EAP)
wr = []
for y, lab in OUT.items():
    bs, ses = [], []
    for c in ctry:
        b, se, n, _ = fit_country(y, "theta_z", dd, c, weights=True); bs.append(b); ses.append(se); wr.append(dict(outcome=lab, country=c, N=n, beta_wmedian=b, se=se))
    h = het_stats(bs, ses); h.update(outcome=lab, score="EAP, wmedian-weighted WLS"); hrows.append(h)
hs = pd.DataFrame(hrows); wr = pd.DataFrame(wr)
print(hs.round(4).to_string()); log("step2 done")
# ---------- STEP 3: pooled slope-equality Wald tests ----------
def slope_test(y, xcol, data, extra_slopes=False, cluster=False):
    s = data.dropna(subset=[y, xcol, "ln_emp", "ln_age"]).copy()
    f = f"{y} ~ C(sector_c) + {xcol}:C(cid) + " + ("ln_emp:C(cid) + ln_age:C(cid)" if extra_slopes else "ln_emp + ln_age")
    mod = smf.ols(f, s)
    m = mod.fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(s.sector_c)[0]}) if cluster else mod.fit(cov_type="HC3")
    names = [n for n in m.params.index if n.startswith(f"{xcol}:C(cid)")]
    L = np.zeros((len(names) - 1, len(m.params)))
    for i, n in enumerate(names[1:]): L[i, list(m.params.index).index(names[0])] = -1; L[i, list(m.params.index).index(n)] = 1
    wt = m.wald_test(L, use_f=False, scalar=True)
    return float(wt.statistic), float(wt.pvalue), int(m.nobs)
trows = []
for y, lab in OUT.items():
    for score, desc in [("theta_c", "latent trait, country-specific prior"), ("theta_z", "EAP"), ("theta5_z", "5-item invariant subset"), ("S_core", "core score")]:
        for ex in (False, True):
            for cl in (False, True):
                st, p, n = slope_test(y, score, dd, ex, cl); trows.append(dict(outcome=lab, score=desc, country_specific_control_slopes=ex, cov="cluster(sector)" if cl else "HC3", N=n, wald_chi2=st, df=6, p=p))
ts = pd.DataFrame(trows)
print(ts.round(4).to_string()); log("step3 done")
# ---------- STEP 4: organisational contingencies ----------
mrows = []
mods = {"ln_emp": "Size (log employees)", "ln_age": "Age (log years)", "foreign10": "Foreign ownership >=10%", "exporter": "Exporter (any)", "ln_mgr_exp": "Top-manager experience (log)", "female_mgr": "Female top manager"}
for y, lab in OUT.items():
    for mv, mlab in mods.items():
        s = dd.dropna(subset=[y, "theta_z", mv, "ln_emp", "ln_age"]).copy(); s["mod"] = s[mv] if mv in ("foreign10", "exporter", "female_mgr") else (s[mv] - s[mv].mean()) / s[mv].std()
        base = "C(sector_c) + theta_z + mod + theta_z:mod" + ("" if mv == "ln_emp" else " + ln_emp") + ("" if mv == "ln_age" else " + ln_age")
        m = smf.ols(f"{y} ~ {base}", s).fit(cov_type="HC3")
        m2 = smf.ols(f"{y} ~ {base} + theta_z:C(cid)", s).fit(cov_type="HC3")
        k2 = [n for n in m2.params.index if n == "theta_z:mod"][0]
        mrows.append(dict(outcome=lab, moderator=mlab, N=int(m.nobs), interaction=m.params["theta_z:mod"], se=m.bse["theta_z:mod"], ci_lo=m.conf_int().loc["theta_z:mod", 0], ci_hi=m.conf_int().loc["theta_z:mod", 1], p=m.pvalues["theta_z:mod"],
                          interaction_given_country_slopes=m2.params[k2], p_given_country_slopes=m2.pvalues[k2]))
mo = pd.DataFrame(mrows)
def holm(p):
    p = np.asarray(p); o = np.argsort(p); m_ = len(p); adj = np.empty(m_); run = 0
    for i, j in enumerate(o): run = max(run, (m_ - i) * p[j]); adj[j] = min(1, run)
    return adj
mo["p_holm"] = holm(mo.p.values); mo["p_given_country_holm"] = holm(mo.p_given_country_slopes.values)
print(mo.round(4).to_string()); log("step4 done")
# ---------- STEP 5: equifinality ----------
erows = []; eq_pairs = []
dd["combo"] = dd.A_r2.astype("Int64").astype(str) + dd.A_r4.astype("Int64").astype(str) + dd.A_r8.astype("Int64").astype(str)
margins = {"ln_lp": 0.05, "sales_growth3y_ann": 0.005, "emp_growth3y_ann": 0.005}
for y, lab in OUT.items():
    for lev, combos in [(1, ["100", "010", "001"]), (2, ["110", "101", "011"])]:
        for scope in ["POOLED"] + ctry:
            s = dd[dd.combo.isin(combos)].dropna(subset=[y, "ln_emp", "ln_age"]).copy()
            if scope != "POOLED": s = s[s.cid == scope]
            if s.combo.nunique() < 3 or s.groupby("combo").size().min() < 15: continue
            ref = combos[0]; m = smf.ols(f"{y} ~ C(combo, Treatment('{ref}')) + ln_emp + ln_age + C(sector_c)", s).fit(cov_type="HC3")
            names = [n for n in m.params.index if n.startswith("C(combo")]; L = np.zeros((len(names), len(m.params)))
            for i, n in enumerate(names): L[i, list(m.params.index).index(n)] = 1
            wt = m.wald_test(L, use_f=False, scalar=True)
            erows.append(dict(outcome=lab, core_score_level=lev, scope=scope, combos="/".join(combos), N=int(m.nobs), n_by_combo=str(s.groupby("combo").size().to_dict()), wald_chi2=float(wt.statistic), df=len(names), p=float(wt.pvalue)))
            if scope == "POOLED":
                ci = m.conf_int()
                for n in names:
                    b, lo, hi = m.params[n], ci.loc[n, 0], ci.loc[n, 1]; mg = margins[y]
                    eq_pairs.append(dict(outcome=lab, core_score_level=lev, contrast=n.split("T.")[1].rstrip("]") + " vs " + ref, diff=b, ci_lo=lo, ci_hi=hi, margin=mg, equivalent_within_margin=(lo > -mg) and (hi < mg)))
er = pd.DataFrame(erows); er["p_holm"] = holm(er.p.values); ep = pd.DataFrame(eq_pairs)
# configuration x country beyond theta x country (soft classes A3)
p3 = pickle.load(open(os.path.join(RES, "lca/model_A3.pkl"), "rb"))["post"]; cdf = dd.copy()
for c in range(1, 3): cdf[f"pc{c}"] = p3[:, c]
crow = []
for y, lab in OUT.items():
    s = cdf.dropna(subset=[y, "theta_z", "ln_emp", "ln_age"]).copy()
    a = smf.ols(f"{y} ~ C(sector_c) + theta_z:C(cid) + ln_emp + ln_age", s).fit()
    b = smf.ols(f"{y} ~ C(sector_c) + theta_z:C(cid) + ln_emp + ln_age + pc1 + pc2", s).fit()
    c_ = smf.ols(f"{y} ~ C(sector_c) + theta_z:C(cid) + ln_emp + ln_age + (pc1 + pc2):C(cid)", s).fit()
    for nm, sm_, bg in [("classes beyond country-specific theta slopes", a, b), ("class x country interactions beyond classes", b, c_)]:
        F = ((sm_.ssr - bg.ssr) / (bg.df_model - sm_.df_model)) / (bg.ssr / bg.df_resid); crow.append(dict(outcome=lab, test=nm, N=int(bg.nobs), df=int(bg.df_model - sm_.df_model), F=F, p=stats.f.sf(F, bg.df_model - sm_.df_model, bg.df_resid), dR2=bg.rsquared - sm_.rsquared))
cx = pd.DataFrame(crow); cx["p_holm"] = holm(cx.p.values)
print(er.round(4).to_string()); print(ep.round(4).to_string()); print(cx.round(4).to_string()); log("step5 done")
# ---------- STEP 6: country-specific nonlinearity ----------
nrows = []
for y, lab in OUT.items():
    for c in ["POOLED"] + ctry:
        s = dd.dropna(subset=[y, "theta_z", "ln_emp", "ln_age"]); s = s if c == "POOLED" else s[s.cid == c]
        a = smf.ols(f"{y} ~ theta_z + ln_emp + ln_age + C(sector_c)", s).fit(); b = smf.ols(f"{y} ~ cr(theta_z, df=4) + ln_emp + ln_age + C(sector_c)", s).fit()
        F = ((a.ssr - b.ssr) / (b.df_model - a.df_model)) / (b.ssr / b.df_resid); g = np.linspace(s.theta_z.quantile(.05), s.theta_z.quantile(.95), 25)
        P = s.iloc[[0]].copy(); P = pd.concat([P] * 25, ignore_index=True); P["theta_z"] = g; P["ln_emp"] = s.ln_emp.mean(); P["ln_age"] = s.ln_age.mean()
        sp = b.predict(P).values; lin = a.params["theta_z"] * g; dev = (sp - sp.mean()) - (lin - lin.mean())
        nrows.append(dict(outcome=lab, scope=c, N=int(b.nobs), F_spline_vs_linear=F, p=stats.f.sf(F, b.df_model - a.df_model, b.df_resid), max_abs_deviation_from_linear=np.abs(dev).max(), outcome_sd=s[y].std()))
nl = pd.DataFrame(nrows); nl["p_holm"] = holm(nl.p.values); nl["max_dev_in_outcome_SD"] = nl.max_abs_deviation_from_linear / nl.outcome_sd
print(nl.round(4).to_string())
with pd.ExcelWriter(os.path.join(OUTD, "CONTEXT_TABLES.xlsx")) as wx:
    cs.to_excel(wx, sheet_name="country_slopes", index=False); hs.to_excel(wx, sheet_name="heterogeneity_Q_I2", index=False); wr.to_excel(wx, sheet_name="weighted_slopes", index=False)
    ts.to_excel(wx, sheet_name="pooled_slope_equality_Wald", index=False)
    mo.to_excel(wx, sheet_name="firm_moderators", index=False); er.to_excel(wx, sheet_name="equifinality_tests", index=False); ep.to_excel(wx, sheet_name="equifinality_pairs", index=False)
    cx.to_excel(wx, sheet_name="config_x_country", index=False); nl.to_excel(wx, sheet_name="nonlinearity_by_country", index=False)
sc = ts.assign(sig05=ts.p < .05).groupby("outcome").agg(n_specs=("p", "size"), n_p_lt_05=("sig05", "sum"), min_p=("p", "min"), max_p=("p", "max")).reset_index()
sc.to_excel(os.path.join(OUTD, "spec_curve_summary.xlsx"), index=False); print(sc)
pickle.dump(dict(cs=cs, hs=hs), open(os.path.join(OUTD, "ctx_main.pkl"), "wb")); log("13_contextual_fit: done")
