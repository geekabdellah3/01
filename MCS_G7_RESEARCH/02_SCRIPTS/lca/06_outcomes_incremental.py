"""STEP 7 (cont.): incremental explanatory value of latent classes vs transparent/continuous aggregate scores.
Outcomes (associational only): ln labour productivity, 3y annualised sales growth, 3y annualised employment growth."""
import os, sys, pickle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
from lca_core import *
import statsmodels.api as sm
from scipy import stats
d = load_analytic(); store = pickle.load(open(os.path.join(RES, "lca/lca_store.pkl"), "rb"))
keepA = store["A"]["keep"]; dd = d[keepA].reset_index(drop=True)
# data-driven continuous score from 1-D nominal response model (spec A); hybrid-free
nr = store["A"]["models"]["nrm1_1"]; dd["theta"] = nr["post"] @ nr["Xs"][:, 1]
if dd[["theta","S_core"]].corr().iloc[0,1] < 0: dd["theta"] = -dd.theta   # orient: higher = more practices (sign of a latent trait is arbitrary)
dd["theta_z"] = (dd.theta - dd.theta.mean()) / dd.theta.std()
def wins(s, lo=.01, hi=.99): return s.clip(s.quantile(lo), s.quantile(hi))
for c in ["sales_growth3y_ann", "emp_growth3y_ann"]: dd[c] = wins(dd[c])
dd["ln_lp"] = dd.groupby("cid").ln_lp.transform(lambda s: s.clip(s.quantile(.005), s.quantile(.995)))
posts = {k: pickle.load(open(os.path.join(RES, f"lca/model_{k}.pkl"), "rb"))["post"] for k in ["A3", "A4"]}
def design(frame, extra):
    X = pd.get_dummies(frame[["cid", "sector_c"]].astype(str), drop_first=True, dtype=float)
    X["ln_emp"] = frame.ln_emp; X["ln_age"] = frame.ln_age
    for e in extra: X[e] = frame[e]
    return sm.add_constant(X)
def cv_rmse(X, y, k=10, reps=3, seed=SEED):
    rng = np.random.default_rng(seed); n = len(y); errs = []
    for r in range(reps):
        idx = rng.permutation(n); folds = np.array_split(idx, k)
        se = 0
        for f in folds:
            tr = np.setdiff1d(idx, f); b = np.linalg.lstsq(X[tr], y[tr], rcond=None)[0]; se += ((y[f] - X[f] @ b) ** 2).sum()
        errs.append(np.sqrt(se / n))
    return float(np.mean(errs))
rows = []; coefrows = []
rng = np.random.default_rng(SEED)
for ycol in ["ln_lp", "sales_growth3y_ann", "emp_growth3y_ann"]:
    base = dd.dropna(subset=[ycol, "ln_emp", "ln_age", "S_core", "theta"]).copy()
    y = base[ycol].values; n = len(base)
    P = {k: posts[k][base.index.values] for k in posts}
    base["S1"] = base.S_core
    for k, Pk in P.items():
        for c in range(Pk.shape[1]): base[f"{k}_p{c+1}"] = Pk[:, c]
    specs = {"M0 controls": [], "M1 core score (linear)": ["S1"], "M1b core score (categorical)": None,
             "M2 continuous theta (NRM-1D)": ["theta_z"], "M3a classes A3 (soft)": [f"A3_p{c}" for c in (2, 3)],
             "M3b classes A4 (soft)": [f"A4_p{c}" for c in (2, 3, 4)], "M4a theta + classes A3": ["theta_z"] + [f"A3_p{c}" for c in (2, 3)],
             "M4b theta + classes A4": ["theta_z"] + [f"A4_p{c}" for c in (2, 3, 4)], "M5 core score + classes A3": ["S1"] + [f"A3_p{c}" for c in (2, 3)]}
    res = {}
    for name, ex in specs.items():
        if ex is None:
            for s in (1, 2, 3): base[f"S_{s}"] = (base.S_core == s).astype(float)
            ex = ["S_1", "S_2", "S_3"]
        Xdf = design(base, ex); X = Xdf.values; m = sm.OLS(y, X).fit(cov_type="HC3")
        res[name] = (m, Xdf, ex)
        rows.append(dict(outcome=ycol, model=name, n=n, k=X.shape[1], R2=m.rsquared, adjR2=m.rsquared_adj, AIC=m.aic, BIC=m.bic, cv_rmse=cv_rmse(X, y)))
    # nested F-tests (homoskedastic) for increments
    def ftest(small, big):
        a, b = res[small][0], res[big][0]; d1 = b.df_model - a.df_model
        F = ((a.ssr - b.ssr) / d1) / (b.ssr / b.df_resid); return F, stats.f.sf(F, d1, b.df_resid)
    for sm_, bg in [("M0 controls", "M1 core score (linear)"), ("M0 controls", "M2 continuous theta (NRM-1D)"), ("M0 controls", "M3a classes A3 (soft)"),
                    ("M2 continuous theta (NRM-1D)", "M4a theta + classes A3"), ("M2 continuous theta (NRM-1D)", "M4b theta + classes A4"),
                    ("M3a classes A3 (soft)", "M4a theta + classes A3"), ("M1 core score (linear)", "M5 core score + classes A3")]:
        F, p = ftest(sm_, bg); rows.append(dict(outcome=ycol, model=f"F-test: {sm_} -> {bg}", n=n, F=F, p=p))
    # pseudo-class draws (M=50): class coefficients with Rubin pooling, controlling theta
    for k in ["A3", "A4"]:
        Pk = P[k]; Kc = Pk.shape[1]; coefs = []; vars_ = []; Fs = []; ps = []
        for mdraw in range(50):
            u = rng.random(n)[:, None]; cls = (u > np.cumsum(Pk, 1)).sum(1).clip(max=Kc - 1)
            tmp = base.copy()
            for c in range(1, Kc): tmp[f"pc{c}"] = (cls == c).astype(float)
            exs = [f"pc{c}" for c in range(1, Kc)]
            Xb = design(tmp, ["theta_z"] + exs); Xs_ = design(tmp, ["theta_z"])
            mb = sm.OLS(y, Xb.values).fit(); ms = sm.OLS(y, Xs_.values).fit()
            nb = Xb.shape[1]; idxs = [nb - Kc + 1 + i for i in range(Kc - 1)]
            coefs.append(mb.params[idxs]); vars_.append(np.diag(mb.cov_params())[idxs])
            d1 = Kc - 1; F = ((ms.ssr - mb.ssr) / d1) / (mb.ssr / mb.df_resid); Fs.append(F); ps.append(stats.f.sf(F, d1, mb.df_resid))
        coefs = np.array(coefs); W = np.mean(vars_, 0); Bv = coefs.var(0, ddof=1); T = W + (1 + 1 / 50) * Bv
        for c in range(Kc - 1):
            coefrows.append(dict(outcome=ycol, model=k, contrast=f"C{c+2} vs C1 (given theta)", coef=coefs[:, c].mean(), se_rubin=np.sqrt(T[c]), z=coefs[:, c].mean() / np.sqrt(T[c]), frac_missing_info=(1 + 1 / 50) * Bv[c] / T[c]))
        rows.append(dict(outcome=ycol, model=f"pseudo-class draws {k}: F(class | theta)", n=n, F=float(np.median(Fs)), p=float(np.median(ps))))
    # standardised gradient coefficient
    m2 = res["M2 continuous theta (NRM-1D)"][0]; i = list(res["M2 continuous theta (NRM-1D)"][1].columns).index("theta_z")
    coefrows.append(dict(outcome=ycol, model="M2", contrast="theta (per SD)", coef=m2.params[i], se_rubin=m2.bse[i], z=m2.tvalues[i], frac_missing_info=np.nan))
    m1 = res["M1 core score (linear)"][0]; i = list(res["M1 core score (linear)"][1].columns).index("S1")
    coefrows.append(dict(outcome=ycol, model="M1", contrast="core score S (per practice)", coef=m1.params[i], se_rubin=m1.bse[i], z=m1.tvalues[i], frac_missing_info=np.nan))
out = pd.DataFrame(rows); co = pd.DataFrame(coefrows)
with pd.ExcelWriter(os.path.join(RES, "lca/LCA_OUTCOME_INCREMENTAL.xlsx")) as w:
    out.to_excel(w, sheet_name="models", index=False); co.to_excel(w, sheet_name="coefficients", index=False)
pd.set_option("display.width", 250)
print(out.round(4).to_string()); print(co.round(4).to_string())
log("06_outcomes: done")
