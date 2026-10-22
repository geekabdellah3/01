"""Why can a common predictive model stay competitive although slope heterogeneity is statistically detectable?
(i) oracle gain of country-specific slopes versus the cost of estimating them; (ii) simulation of predictive power of national slopes at the estimated heterogeneity."""
import os, sys, pickle, warnings
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
warnings.filterwarnings("ignore")
d = load_analytic(); store = pickle.load(open(os.path.join(RES, "lca/lca_store.pkl"), "rb")); dd = d[store["A"]["keep"]].reset_index(drop=True)
nr = store["A"]["models"]["nrm1_1"]; th = nr["post"] @ nr["Xs"][:, 1]; th = th if np.corrcoef(th, dd.S_core.fillna(dd.S_core.mean()))[0, 1] > 0 else -th; dd["th"] = (th - th.mean()) / th.std()
dd["ln_lp"] = dd.groupby("cid").ln_lp.transform(lambda s: s.clip(s.quantile(.005), s.quantile(.995)))
sub = dd.dropna(subset=["ln_lp", "ln_emp", "ln_age", "th"]).reset_index(drop=True); n = len(sub)
S = pd.get_dummies(sub.sector_c.astype(str), dtype=float).values; C = pd.get_dummies(sub.cid, dtype=float).reindex(columns=CORDER).values
base = np.c_[S, sub.ln_emp.values, sub.ln_age.values]; y = sub.ln_lp.values; t = sub.th.values
Xu = np.c_[base, t]; b = np.linalg.lstsq(Xu, y, rcond=None)[0]; res = y - Xu @ b; sig2 = res.var(ddof=Xu.shape[1])
# residualised score variance within country (after controls)
tr = t - base @ np.linalg.lstsq(base, t, rcond=None)[0]; vt = {c: tr[sub.cid.values == c].var() for c in CORDER}; vbar = tr.var()
h = pd.read_excel(os.path.join(ROOT, "08_CONTEXTUAL_FIT/CONTEXT_TABLES.xlsx"), sheet_name="heterogeneity_Q_I2"); h = h[h.outcome.str.startswith("Log")]
tau_eap = float(h[h.score.str.startswith("EAP score")].tau.iloc[0]); tau_cal = float(h[h.score.str.startswith("latent")].tau.iloc[0])
rows = []
for nm, tau in [("tau from pooled-prior EAP (0.036/SD)", tau_eap), ("2 x tau", 2 * tau_eap), ("3 x tau", 3 * tau_eap), ("tau from calibrated score (0.062/latent SD; scale differs)", tau_cal)]:
    oracle = tau ** 2 * vbar; cost = sig2 * 6 / (0.9 * n)
    rows.append(dict(scenario=nm, tau=tau, var_resid_score=vbar, sigma2=sig2, oracle_mse_gain=oracle, est_cost_6_slopes=cost, expected_net=oracle - cost, oracle_gain_pct_of_mse=100 * oracle / sig2))
ora = pd.DataFrame(rows); print(ora.round(5).to_string())
# simulation: would national slopes beat the common slope out of sample at these heterogeneity levels?
def cv_mse(X, yv, folds):
    se = 0.0
    for f in folds:
        trn = np.setdiff1d(np.arange(len(yv)), f); bb = np.linalg.lstsq(X[trn], yv[trn], rcond=None)[0]; se += ((yv[f] - X[f] @ bb) ** 2).sum()
    return se / len(yv)
rng = np.random.default_rng(SEED); idx = rng.permutation(n); folds = np.array_split(idx, 10); Xn = np.c_[base, C * t[:, None]]
srows = []
for nm, tau in [("tau (0.036)", tau_eap), ("2 x tau", 2 * tau_eap), ("4 x tau", 4 * tau_eap)]:
    gains = []
    for _ in range(150):
        bc = b[-1] + tau * rng.standard_normal(7); ysim = base @ b[:-1] + (C * t[:, None]) @ bc + rng.choice(res, n, replace=True)
        gains.append(cv_mse(Xu[:, :], ysim, folds) - cv_mse(Xn, ysim, folds))
    gains = np.array(gains); srows.append(dict(heterogeneity=nm, tau=tau, mean_oos_mse_gain_national_vs_common=gains.mean(), share_sims_national_better=float((gains > 0).mean()), p5=np.percentile(gains, 5), p95=np.percentile(gains, 95)))
sim = pd.DataFrame(srows); print(sim.round(5).to_string())
obs = pd.read_excel(os.path.join(ROOT, "08_CONTEXTUAL_FIT/PREDICTIVE_COMPARISON_AND_TRANSFER.xlsx"), sheet_name="paired_comparisons"); obs = obs[(obs.outcome == "Log sales per employee") & (obs.reference == "U1") & (obs.model == "N1")]
with pd.ExcelWriter(os.path.join(ROOT, "08_CONTEXTUAL_FIT/WHY_COMMON_MODEL_COMPETES.xlsx")) as w:
    ora.to_excel(w, sheet_name="oracle_gain_vs_cost", index=False); sim.to_excel(w, sheet_name="simulated_oos_power", index=False); obs.to_excel(w, sheet_name="observed_national_vs_common", index=False)
log("21 why: done")
