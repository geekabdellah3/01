"""Diagnostics to separate restricted range / ceiling from genuine slope heterogeneity (associations only)."""
import os, sys, pickle, warnings
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
import statsmodels.formula.api as smf
from scipy import stats
warnings.filterwarnings("ignore")
d = load_analytic(); store = pickle.load(open(os.path.join(RES, "lca/lca_store.pkl"), "rb")); dd = d[store["A"]["keep"]].reset_index(drop=True)
nr = store["A"]["models"]["nrm1_1"]; th = nr["post"] @ nr["Xs"][:, 1]; th = th if np.corrcoef(th, dd.S_core.fillna(dd.S_core.mean()))[0, 1] > 0 else -th
dd["theta"] = (th - th.mean()) / th.std()
w = lambda s: s.clip(s.quantile(.01), s.quantile(.99))
dd["sales_growth3y_ann"] = w(dd.sales_growth3y_ann); dd["emp_growth3y_ann"] = w(dd.emp_growth3y_ann); dd["ln_lp"] = dd.groupby("cid").ln_lp.transform(lambda s: s.clip(s.quantile(.005), s.quantile(.995)))
OUT = {"ln_lp": "Log sales per employee", "sales_growth3y_ann": "Sales growth (ann.)", "emp_growth3y_ann": "Employment growth (ann.)"}
def het(b, se):
    b, se = np.array(b), np.array(se); wt = 1 / se ** 2; bb = (wt * b).sum() / wt.sum(); Q = ((b - bb) ** 2 * wt).sum(); return Q, stats.chi2.sf(Q, len(b) - 1), max(0, (Q - len(b) + 1) / Q) * 100
lo = max(dd[dd.cid == c].theta.quantile(.10) for c in CORDER); hi = min(dd[dd.cid == c].theta.quantile(.90) for c in CORDER)
rows = []; summ = []
for y, lab in OUT.items():
    bs, ses = [], []
    for c in CORDER:
        s = dd[(dd.cid == c) & dd.theta.between(lo, hi)].dropna(subset=[y, "ln_emp", "ln_age"])
        m = smf.ols(f"{y} ~ theta + ln_emp + ln_age + C(sector_c)", s).fit(cov_type="HC3")
        bs.append(m.params["theta"]); ses.append(m.bse["theta"]); rows.append(dict(outcome=lab, country=c, N_common_support=int(m.nobs), share_of_country=float((dd.cid == c).pipe(lambda k: s.shape[0] / k.sum())), beta=m.params["theta"], se=m.bse["theta"], ci_lo=m.conf_int().loc["theta", 0], ci_hi=m.conf_int().loc["theta", 1]))
    Q, p, I2 = het(bs, ses); summ.append(dict(outcome=lab, support=f"[{lo:.2f}, {hi:.2f}] in SD of pooled score", Q=Q, p=p, I2=I2))
cs = pd.DataFrame(rows); ss = pd.DataFrame(summ)
# ceiling: slopes below/above the country median
crow = []
for y, lab in OUT.items():
    for c in CORDER:
        s = dd[dd.cid == c].dropna(subset=[y, "ln_emp", "ln_age"]).copy(); med = s.theta.median(); s["hi"] = (s.theta > med).astype(float)
        m = smf.ols(f"{y} ~ theta + theta:hi + hi + ln_emp + ln_age + C(sector_c)", s).fit(cov_type="HC3")
        crow.append(dict(outcome=lab, country=c, slope_below_median=m.params["theta"], slope_above_median=m.params["theta"] + m.params["theta:hi"], diff_above_minus_below=m.params["theta:hi"], p_diff=m.pvalues["theta:hi"]))
ce = pd.DataFrame(crow)
pw = []
q1, q2 = dd.theta.quantile([1 / 3, 2 / 3])
for y, lab in OUT.items():
    s = dd.dropna(subset=[y, "ln_emp", "ln_age"]).copy(); s["t1"] = s.theta.clip(upper=q1); s["t2"] = (s.theta.clip(q1, q2) - q1); s["t3"] = (s.theta.clip(lower=q2) - q2)
    m = smf.ols(f"{y} ~ t1 + t2 + t3 + ln_emp + ln_age + C(sector_c)", s).fit(cov_type="HC3")
    for k, nm in [("t1", "lower third"), ("t2", "middle third"), ("t3", "upper third")]: pw.append(dict(outcome=lab, segment=nm, slope=m.params[k], ci_lo=m.conf_int().loc[k, 0], ci_hi=m.conf_int().loc[k, 1], N=int(m.nobs)))
pw = pd.DataFrame(pw)
pd.set_option("display.width", 220)
print(ss.round(4).to_string()); print(cs[cs.outcome.str.startswith("Log")].round(3).to_string()); print(ce[ce.outcome.str.startswith("Log")].round(3).to_string()); print(pw.round(4).to_string())
log("16_support_ceiling: done")
# ---- does a COMMON nonlinear (level-dependent) shape absorb country heterogeneity? ----
trow = []
for y, lab in OUT.items():
    s = dd.dropna(subset=[y, "ln_emp", "ln_age"]).copy(); s["t1"] = s.theta.clip(upper=q1); s["t2"] = (s.theta.clip(q1, q2) - q1); s["t3"] = (s.theta.clip(lower=q2) - q2)
    for c in CORDER[:-1]: s[f"dv_{c}"] = s.theta * (s.cid == c)
    devs = " + ".join(f"dv_{c}" for c in CORDER[:-1])
    for nm, form in [("linear common slope + country-specific slopes", "theta + " + devs), ("common piecewise shape + country-specific linear deviations", "t1 + t2 + t3 + " + devs)]:
        m = smf.ols(f"{y} ~ {form} + ln_emp + ln_age + C(sector_c)", s).fit(cov_type="HC3")
        names = [n for n in m.params.index if n.startswith("dv_")]; L = np.zeros((len(names), len(m.params)))
        for i, n in enumerate(names): L[i, list(m.params.index).index(n)] = 1
        wt = m.wald_test(L, use_f=False, scalar=True); trow.append(dict(outcome=lab, model=nm, N=int(m.nobs), wald_chi2=float(wt.statistic), df=len(names), p=float(wt.pvalue)))
    mm = smf.ols(f"{y} ~ t1 + t2 + t3 + ln_emp + ln_age + C(sector_c)", s).fit(cov_type="HC3")
    L = np.zeros((1, len(mm.params))); L[0, list(mm.params.index).index("t1")] = 1; L[0, list(mm.params.index).index("t3")] = -1; wt = mm.wald_test(L, use_f=False, scalar=True)
    trow.append(dict(outcome=lab, model="lower-third slope = upper-third slope (pooled)", N=int(mm.nobs), wald_chi2=float(wt.statistic), df=1, p=float(wt.pvalue)))
tt = pd.DataFrame(trow); print(tt.round(4).to_string())
with pd.ExcelWriter(os.path.join(ROOT, "08_CONTEXTUAL_FIT/SUPPORT_CEILING_DIAGNOSTICS.xlsx")) as wx:
    cs.to_excel(wx, sheet_name="common_support_slopes", index=False); ss.to_excel(wx, sheet_name="common_support_heterogeneity", index=False)
    ce.to_excel(wx, sheet_name="below_above_median", index=False); pw.to_excel(wx, sheet_name="pooled_piecewise", index=False); tt.to_excel(wx, sheet_name="common_shape_vs_country_slopes", index=False)
