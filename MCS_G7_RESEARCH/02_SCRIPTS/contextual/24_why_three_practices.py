"""Why can a common model of the three practices stay competitive out of sample although slope heterogeneity (notably incentives) is detectable?
Oracle gain of country-specific slopes vs the cost of estimating them; simulation of out-of-sample power at the estimated heterogeneity."""
import os, sys, warnings
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
warnings.filterwarnings("ignore")
d = load_analytic(); dd = d.copy(); dd["M"], dd["T"], dd["I"] = dd.A_r2, dd.A_r4, dd.A_r8
dd["ln_lp"] = dd.groupby("cid").ln_lp.transform(lambda s: s.clip(s.quantile(.005), s.quantile(.995)))
s0 = dd.dropna(subset=["ln_lp", "M", "T", "I", "ln_emp", "ln_age"]).reset_index(drop=True); n = len(s0)
F = pd.get_dummies(s0.sector_c.astype(str), dtype=float).values; C = pd.get_dummies(s0.cid, dtype=float).reindex(columns=CORDER).values
base = np.c_[F, s0.ln_emp.values, s0.ln_age.values]; P = s0[["M", "T", "I"]].values; y = s0.ln_lp.values
Xc = np.c_[base, P]; b = np.linalg.lstsq(Xc, y, rcond=None)[0]; res = y - Xc @ b; sig2 = res.var(ddof=Xc.shape[1])
Pr = P - base @ np.linalg.lstsq(base, P, rcond=None)[0]; var_res = Pr.var(0)
H = pd.read_excel(os.path.join(ROOT, "08_CONTEXTUAL_FIT/THREE_PRACTICES_TABLES.xlsx"), sheet_name="Q3_heterogeneity"); H = H[H.outcome.str.startswith("Log")].set_index("practice")
tau = np.array([H.loc[p, "tau"] for p in ["M", "T", "I"]]); mu = np.array([H.loc[p, "RE_mean"] for p in ["M", "T", "I"]])
oracle_by = tau ** 2 * var_res; oracle = oracle_by.sum(); cost = sig2 * 18 / (0.9 * n)
rows = [dict(item="tau (M, T, I)", value=str(np.round(tau, 4).tolist())), dict(item="residual variance of practice indicators (M, T, I)", value=str(np.round(var_res, 4).tolist())),
        dict(item="sigma2 (residual MSE of common model)", value=round(float(sig2), 4)), dict(item="oracle MSE gain if country slopes were known (sum over practices)", value=round(float(oracle), 5)),
        dict(item="  of which monitoring, targets, incentives", value=str(np.round(oracle_by, 5).tolist())), dict(item="expected out-of-sample cost of estimating 18 extra slopes (sigma2 x 18 / n_train)", value=round(float(cost), 5)),
        dict(item="expected net gain (oracle - cost)", value=round(float(oracle - cost), 5)), dict(item="oracle gain as % of residual MSE", value=round(100 * float(oracle / sig2), 3))]
print(pd.DataFrame(rows).to_string())
def cv_mse(X, yv, folds):
    se = 0.0
    for f in folds:
        trn = np.setdiff1d(np.arange(len(yv)), f); bb = np.linalg.lstsq(X[trn], yv[trn], rcond=None)[0]; se += ((yv[f] - X[f] @ bb) ** 2).sum()
    return se / len(yv)
rng = np.random.default_rng(SEED); folds = np.array_split(rng.permutation(n), 10); Xn = np.c_[base, np.hstack([P[:, [j]] * C for j in range(3)])]; srows = []
for nm, mult in [("estimated heterogeneity (tau)", 1.0), ("2 x tau", 2.0), ("3 x tau", 3.0)]:
    g = []
    for _ in range(100):
        bc = np.hstack([b[-3 + j] + mult * tau[j] * rng.standard_normal(7) for j in range(3)]); ysim = base @ b[:-3] + Xn[:, base.shape[1]:] @ bc + rng.choice(res, n, replace=True)
        g.append(cv_mse(Xc, ysim, folds) - cv_mse(Xn, ysim, folds))
    g = np.array(g); srows.append(dict(heterogeneity=nm, mean_oos_mse_gain_national_vs_common=g.mean(), share_sims_national_better=float((g > 0).mean()), p5=np.percentile(g, 5), p95=np.percentile(g, 95)))
sim = pd.DataFrame(srows); print(sim.round(5).to_string())
with pd.ExcelWriter(os.path.join(ROOT, "08_CONTEXTUAL_FIT/WHY_COMMON_MODEL_COMPETES_3P.xlsx")) as w: pd.DataFrame(rows).to_excel(w, sheet_name="oracle_gain_vs_cost", index=False); sim.to_excel(w, sheet_name="simulated_oos_power", index=False)
log("24 why 3p: done")
