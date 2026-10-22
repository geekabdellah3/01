"""V6 robustness (part a): r4 x r8 structure; leave-one-country-out heterogeneity; CIs for tau and I2; weighted; winsorisation/median regression for incentives;
combined local-minus-LOCO test; practice-only transfer with controls held fixed."""
import os, sys, warnings
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
import statsmodels.api as sm
from scipy import stats
from scipy.optimize import brentq
warnings.filterwarnings("ignore")
OUTD = os.path.join(ROOT, "08_CONTEXTUAL_FIT")
d = load_analytic(); dd = d.copy(); dd["M"], dd["T"], dd["I"] = dd.A_r2, dd.A_r4, dd.A_r8
raw_lp = dd.ln_lp.copy(); dd["lp_raw"] = raw_lp
dd["lp_w"] = dd.groupby("cid").ln_lp.transform(lambda s: s.clip(s.quantile(.005), s.quantile(.995)))
dd["lp_w5"] = dd.groupby("cid").ln_lp.transform(lambda s: s.clip(s.quantile(.05), s.quantile(.95)))
PR = ["M", "T", "I"]; out = {}
# ---- (a) r4 x r8 structure
s = dd.dropna(subset=["M", "T", "I"]); rows = []
for c in ["ALL"] + CORDER:
    g = s if c == "ALL" else s[s.cid == c]; t = pd.crosstab(g["T"], g["I"])
    rows.append(dict(country=c, N=len(g), P_I_given_T1=float(g[g["T"] == 1]["I"].mean()), P_I_given_T0=float(g[g["T"] == 0]["I"].mean()), n_T0_I1=int(((g["T"] == 0) & (g["I"] == 1)).sum()), share_T0_I1_of_I1=float(((g["T"] == 0) & (g["I"] == 1)).sum() / max(1, (g["I"] == 1).sum())), phi_T_I=float(np.corrcoef(g["T"], g["I"])[0, 1]), phi_M_T=float(np.corrcoef(g["M"], g["T"])[0, 1]), phi_M_I=float(np.corrcoef(g["M"], g["I"])[0, 1])))
out["r4_r8_structure"] = pd.DataFrame(rows)
# VIF after controls
s2 = dd.dropna(subset=["M", "T", "I", "ln_emp", "ln_age", "lp_w"]); F = pd.get_dummies(s2.sector_c.astype(str), dtype=float).values; base = np.c_[F, s2.ln_emp, s2.ln_age]; vif = {}
for j, p in enumerate(PR):
    others = [q for q in PR if q != p]; Xo = np.c_[base, s2[others].values]; r = s2[p].values - Xo @ np.linalg.lstsq(Xo, s2[p].values, rcond=None)[0]; r0 = s2[p].values - base @ np.linalg.lstsq(base, s2[p].values, rcond=None)[0]; vif[p] = float(1 / (1 - (1 - (r ** 2).sum() / (r0 ** 2).sum())))
out["VIF_after_controls"] = pd.DataFrame([vif]); print(out["r4_r8_structure"].round(3).to_string()); print(out["VIF_after_controls"].round(3))
# ---- helpers
def country_betas(y, weights=False, data=None, subset=None):
    data = dd if data is None else data; b, se, n = {p: [] for p in PR}, {p: [] for p in PR}, []
    for c in CORDER:
        sc = data[data.cid == c].dropna(subset=[y, "M", "T", "I", "ln_emp", "ln_age"])
        if subset is not None: sc = sc[subset(sc)]
        X = np.c_[pd.get_dummies(sc.sector_c.astype(str), dtype=float).values, sc.ln_emp, sc.ln_age, sc[PR].values]; k = X.shape[1] - 3
        m = (sm.WLS(sc[y].values, X, weights=sc.wmedian.values) if weights else sm.OLS(sc[y].values, X)).fit(cov_type="HC3")
        for j, p in enumerate(PR): b[p].append(m.params[k + j]); se[p].append(m.bse[k + j])
        n.append(len(sc))
    return {p: np.array(b[p]) for p in PR}, {p: np.array(se[p]) for p in PR}, n
def het(b, se):
    wt = 1 / se ** 2; bb = (wt * b).sum() / wt.sum(); Q = (wt * (b - bb) ** 2).sum(); k = len(b); I2 = max(0, (Q - (k - 1)) / Q) * 100
    c_ = wt.sum() - (wt ** 2).sum() / wt.sum(); tau2 = max(0, (Q - (k - 1)) / c_); return Q, stats.chi2.sf(Q, k - 1), I2, np.sqrt(tau2), c_
def qprofile(b, se):
    """Q-profile 95% CI for tau^2 (Viechtbauer 2007) and implied I2."""
    k = len(b)
    def Qg(t2):
        w = 1 / (se ** 2 + t2); mu = (w * b).sum() / w.sum(); return (w * (b - mu) ** 2).sum()
    lo_q, hi_q = stats.chi2.ppf(.025, k - 1), stats.chi2.ppf(.975, k - 1)
    def solve(target):
        if Qg(0) < target: return 0.0
        hi = 10.0
        return brentq(lambda t: Qg(t) - target, 0, hi)
    t_lo, t_hi = solve(hi_q), solve(lo_q); wt = 1 / se ** 2; s2 = (k - 1) * wt.sum() / (wt.sum() ** 2 - (wt ** 2).sum())
    return np.sqrt(t_lo), np.sqrt(t_hi), 100 * t_lo / (t_lo + s2), 100 * t_hi / (t_hi + s2)
# ---- (b) productivity: main, LOCO, CIs, weighted, winsorisation variants
rows = []; bm, sem, nn = country_betas("lp_w")
for p in PR:
    Q, pQ, I2, tau, _ = het(bm[p], sem[p]); tl, th, il, ih = qprofile(bm[p], sem[p]); rows.append(dict(spec="main (winsorised 0.5/99.5 within country, HC3)", practice=p, Q=Q, p=pQ, I2=I2, tau=tau, tau_ci_lo=tl, tau_ci_hi=th, I2_ci_lo=il, I2_ci_hi=ih))
    for i, c in enumerate(CORDER):
        keep = np.arange(7) != i; Q, pQ, I2, tau, _ = het(bm[p][keep], sem[p][keep]); rows.append(dict(spec=f"leave out {c}", practice=p, Q=Q, p=pQ, I2=I2, tau=tau))
for nm, y, wts in [("weighted WLS (wmedian)", "lp_w", True), ("no winsorisation", "lp_raw", False), ("winsorised 5/95 within country", "lp_w5", False)]:
    b_, se_, n_ = country_betas(y, weights=wts)
    for p in PR: Q, pQ, I2, tau, _ = het(b_[p], se_[p]); rows.append(dict(spec=nm, practice=p, Q=Q, p=pQ, I2=I2, tau=tau, **{f"beta_{c}": b_[p][i] for i, c in enumerate(CORDER)}))
# median regression for incentives coefficient by country
from statsmodels.regression.quantile_regression import QuantReg
bq, sq = [], []
for c in CORDER:
    sc = dd[dd.cid == c].dropna(subset=["lp_raw", "M", "T", "I", "ln_emp", "ln_age"]); X = np.c_[pd.get_dummies(sc.sector_c.astype(str), dtype=float).values, sc.ln_emp, sc.ln_age, sc[PR].values]
    r = QuantReg(sc.lp_raw.values, X).fit(q=0.5, max_iter=2000); bq.append(r.params[-3:]); sq.append(r.bse[-3:])
bq, sq = np.array(bq), np.array(sq)
for j, p in enumerate(PR): Q, pQ, I2, tau, _ = het(bq[:, j], sq[:, j]); rows.append(dict(spec="median regression (no winsorisation)", practice=p, Q=Q, p=pQ, I2=I2, tau=tau, **{f"beta_{c}": bq[i, j] for i, c in enumerate(CORDER)}))
out["heterogeneity_robustness"] = pd.DataFrame(rows); H = out["heterogeneity_robustness"]; print(H[H.practice == "I"].round(4).to_string())
# ---- (c) local minus LOCO: combined test (inverse-variance pooled mean of the seven target-specific differences)
T = pd.read_excel(os.path.join(OUTD, "THREE_PRACTICES_TABLES.xlsx"), sheet_name="transfer_vs_local"); T = T[(T.outcome.str.startswith("Log")) & (T.benchmark.str.startswith("LOCO"))]
g = T.gap_local_minus_benchmark.values; se = (T.ci_hi.values - T.ci_lo.values) / 3.92; w = 1 / se ** 2; mfix = (w * g).sum() / w.sum(); sfix = np.sqrt(1 / w.sum())
out["local_minus_LOCO_combined"] = pd.DataFrame([dict(pooled_gap_fixed=mfix, ci_lo=mfix - 1.96 * sfix, ci_hi=mfix + 1.96 * sfix, z=mfix / sfix, p=2 * stats.norm.sf(abs(mfix / sfix)), simple_mean=g.mean(), n_positive=int((g > 0).sum()), Q_heterogeneity_of_gaps=float((w * (g - mfix) ** 2).sum()))]); print(out["local_minus_LOCO_combined"].round(4).to_string())
# ---- (d) practice-only transfer: control coefficients held fixed at the target's LOCO estimates
def demean(df, cols):
    o = df.copy()
    for c in cols: o[c] = df[c] - df.groupby("sector_c")[c].transform("mean")
    return o
s3 = dd.dropna(subset=["lp_w", "M", "T", "I", "ln_emp", "ln_age"]).copy(); s3 = demean(s3, ["lp_w", "M", "T", "I", "ln_emp", "ln_age"])
G = {c: (s3[s3.cid == c][["ln_emp", "ln_age"]].values, s3[s3.cid == c][PR].values, s3[s3.cid == c].lp_w.values) for c in CORDER}
tr_rows = []; loc_rows = []
for t in CORDER:
    oth = [k for k in CORDER if k != t]; Xc_o = np.vstack([G[k][0] for k in oth]); Xp_o = np.vstack([G[k][1] for k in oth]); y_o = np.concatenate([G[k][2] for k in oth])
    gam = np.linalg.lstsq(np.c_[Xc_o, Xp_o], y_o, rcond=None)[0][:2]           # control coefficients from the six other countries only
    Xct, Xpt, yt = G[t]; rt = yt - Xct @ gam; den = (rt ** 2).sum()
    # local practice slopes by CV on the control-adjusted target outcome
    e_loc = np.zeros(len(rt))
    for rep in range(5):
        f = np.random.default_rng(SEED + rep).permutation(len(rt)) % 10
        for k in range(10):
            trm, tem = f != k, f == k; b = np.linalg.lstsq(Xpt[trm], rt[trm], rcond=None)[0]; e_loc[tem] += ((rt[tem] - Xpt[tem] @ b) ** 2) / 5
    b_loco = np.linalg.lstsq(Xp_o, y_o - Xc_o @ gam, rcond=None)[0]; e_loco = (rt - Xpt @ b_loco) ** 2
    rg = np.random.default_rng(SEED + 11); dl = e_loco - e_loc; bs = [dl[rg.integers(0, len(dl), len(dl))].sum() / den for _ in range(400)]
    loc_rows.append(dict(target=t, N=len(rt), R2_practice_only_local=1 - e_loc.sum() / den, R2_practice_only_LOCO=1 - e_loco.sum() / den, gap_local_minus_LOCO=dl.sum() / den, ci_lo=np.percentile(bs, 2.5), ci_hi=np.percentile(bs, 97.5)))
    for s_ in oth:
        Xcs, Xps, ys = G[s_]; bsrc = np.linalg.lstsq(Xps, ys - Xcs @ gam, rcond=None)[0]; tr_rows.append(dict(source=s_, target=t, R2_practice_only=1 - ((rt - Xpt @ bsrc) ** 2).sum() / den, R2_local=1 - e_loc.sum() / den))
out["practice_only_transfer_matrix"] = pd.DataFrame(tr_rows); out["practice_only_local_vs_LOCO"] = pd.DataFrame(loc_rows)
M_ = out["practice_only_transfer_matrix"]; print(M_.pivot(index="source", columns="target", values="R2_practice_only").reindex(index=CORDER, columns=CORDER).round(3).to_string()); print(out["practice_only_local_vs_LOCO"].round(4).to_string())
share = float(np.mean([r.R2_local > r.R2_practice_only for r in M_.itertuples()])); gap = float(np.mean([r.R2_local - r.R2_practice_only for r in M_.itertuples()])); print("practice-only: local better in", share, "mean gap", gap)
out["practice_only_summary"] = pd.DataFrame([dict(share_pairs_local_better=share, mean_gap=gap)])
with pd.ExcelWriter(os.path.join(OUTD, "ROBUSTNESS_V6_A.xlsx")) as w:
    for k, v in out.items(): v.to_excel(w, sheet_name=k[:31], index=False)
log("25a robustness v6: done")
