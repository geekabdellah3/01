"""V6 robustness (part b): wild cluster bootstrap (restricted, Rademacher, clusters = country x sector) for slope-equality tests;
partial-pooling (empirical-Bayes / random-slope BLUP) out-of-sample comparison against common and national slopes."""
import os, sys, warnings
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
from scipy import stats
warnings.filterwarnings("ignore")
OUTD = os.path.join(ROOT, "08_CONTEXTUAL_FIT")
d = load_analytic(); raw = load_raw(); raw = raw[raw.r1.notna()].copy(); raw["firm_key"] = raw.cid + "_" + raw.source_row.astype(str)
dd = d.join(raw.set_index("firm_key")[["b2b", "d3b", "d3c", "b7", "b7a"]], on="firm_key"); dd["M"], dd["T"], dd["I"] = dd.A_r2, dd.A_r4, dd.A_r8
dd["foreign10"] = np.where(dd.b2b >= 10, 1.0, np.where(dd.b2b >= 0, 0.0, np.nan)); dd["exporter"] = np.where((dd.d3b.fillna(-1) >= 0) & (dd.d3c.fillna(-1) >= 0), ((dd.d3b + dd.d3c) > 0).astype(float), np.nan)
dd["ln_mgr_exp"] = np.log(dd.b7.where(dd.b7 > 0)); dd["female_mgr"] = dd.b7a.map({1: 1.0, 2: 0.0})
w = lambda s: s.clip(s.quantile(.01), s.quantile(.99)); dd["sales_growth3y_ann"] = w(dd.sales_growth3y_ann); dd["emp_growth3y_ann"] = w(dd.emp_growth3y_ann); dd["ln_lp"] = dd.groupby("cid").ln_lp.transform(lambda s: s.clip(s.quantile(.005), s.quantile(.995)))
OUT = {"ln_lp": "Log sales per employee", "sales_growth3y_ann": "Sales growth (ann.)", "emp_growth3y_ann": "Employment growth (ann.)"}; PR = ["M", "T", "I"]; MODS = ["ln_emp", "ln_age", "foreign10", "exporter", "ln_mgr_exp", "female_mgr"]
FE = lambda s: pd.get_dummies(s.sector_c.astype(str), dtype=float).values; CD = lambda s: pd.get_dummies(s.cid, dtype=float).reindex(columns=CORDER, fill_value=0.0).values
def holm(p):
    p = np.asarray(p); o = np.argsort(p); m_ = len(p); adj = np.empty(m_); run = 0
    for i, j in enumerate(o): run = max(run, (m_ - i) * p[j]); adj[j] = min(1, run)
    return adj
# ---------------- wild cluster bootstrap ----------------
B = 999; rows = []; ncl = []
for y, lab in OUT.items():
    s0 = dd.dropna(subset=[y, "M", "T", "I", "ln_emp", "ln_age"]).sort_values("sector_c").reset_index(drop=True); n = len(s0); F = FE(s0); Cm = CD(s0); P = s0[PR].values; yv = s0[y].values
    ctrl = np.c_[s0.ln_emp.values[:, None] * Cm, s0.ln_age.values[:, None] * Cm]; slopes = [P[:, [j]] * Cm for j in range(3)]
    g = pd.factorize(s0.sector_c)[0]; G = g.max() + 1; starts = np.r_[0, np.flatnonzero(np.diff(g)) + 1]
    ncl.append(dict(outcome=lab, clusters_total=int(G), **{f"clusters_{c}": int(s0[s0.cid == c].sector_c.nunique()) for c in CORDER}))
    Xu = np.c_[F, ctrl, slopes[0], slopes[1], slopes[2]]; k0 = F.shape[1] + 14; XtXi = np.linalg.pinv(Xu.T @ Xu); adj = G / (G - 1) * (n - 1) / (n - Xu.shape[1])
    def wald_cr(beta, u, L):
        S = np.add.reduceat(Xu * u[:, None], starts, axis=0); V = adj * XtXi @ (S.T @ S) @ XtXi; Lb = L @ beta; return float(Lb @ np.linalg.solve(L @ V @ L.T, Lb))
    tests = {}
    for j, p in enumerate(PR):
        L = np.zeros((6, Xu.shape[1]))
        for c in range(1, 7): L[c - 1, k0 + 7 * j] = -1; L[c - 1, k0 + 7 * j + c] = 1
        tests[f"equality of {p} slopes (6 df)"] = (L, [j])
    Lj = np.vstack([tests[f"equality of {p} slopes (6 df)"][0] for p in PR]); tests["joint equality M,T,I (18 df)"] = (Lj, [0, 1, 2])
    beta_u = XtXi @ Xu.T @ yv; u_u = yv - Xu @ beta_u; rng = np.random.default_rng(SEED)
    for nm, (L, js) in tests.items():
        obs = wald_cr(beta_u, u_u, L)
        # restricted model: impose the equality for the tested practices (single common slope for each)
        cols_r = [F, ctrl] + [slopes[j].sum(1, keepdims=True) if j in js else slopes[j] for j in range(3)]; Xr = np.hstack(cols_r); br = np.linalg.pinv(Xr.T @ Xr) @ Xr.T @ yv; ur = yv - Xr @ br; fit_r = Xr @ br; cnt = 0
        for b_ in range(B):
            v = rng.choice([-1.0, 1.0], G)[g]; ys = fit_r + ur * v; bs = XtXi @ Xu.T @ ys; us = ys - Xu @ bs; cnt += wald_cr(bs, us, L) >= obs
        S0 = np.add.reduceat(Xu * u_u[:, None], starts, axis=0); rows.append(dict(outcome=lab, test=nm, wald_cluster_robust=obs, p_asymptotic_chi2=float(stats.chi2.sf(obs, L.shape[0])), p_wild_cluster_bootstrap=(cnt + 1) / (B + 1)))
    print(lab, flush=True)
wb = pd.DataFrame(rows); print(wb.round(4).to_string()); ncl = pd.DataFrame(ncl); print(ncl.to_string())
# ---------------- partial pooling out of sample ----------------
K_F, REP = 10, 3; cv_rows, pw_rows = [], []
for y, lab in OUT.items():
    s0 = dd.dropna(subset=[y, "M", "T", "I", "ln_emp", "ln_age"] + MODS).reset_index(drop=True); n = len(s0); F = FE(s0); P = s0[PR].values; Cm = CD(s0); yv = s0[y].values
    Z = np.c_[[(s0[m_].values - s0[m_].mean()) / s0[m_].std() for m_ in MODS]].T; base = np.c_[F, Z]
    Xp1 = np.c_[base, P]; Xn1 = np.c_[base, np.hstack([P[:, [j]] * Cm for j in range(3)])]; Xhb = np.c_[base, P, np.hstack([P[:, [j]] * Cm for j in range(3)])]; nb = base.shape[1]
    sse = {k_: np.zeros(n) for k_ in ["U0", "P1", "N1", "HB"]}; fm = {k_: [] for k_ in sse}; ntt = []; tau_log = []
    for rep in range(REP):
        rng = np.random.default_rng(SEED + rep); fold = np.zeros(n, int)
        for c in CORDER:
            ii = rng.permutation(np.where(s0.cid.values == c)[0]); fold[ii] = np.arange(len(ii)) % K_F
        pr_ = {k_: np.zeros(n) for k_ in sse}
        for f in range(K_F):
            te = fold == f; trn = ~te; ntt.append((trn.sum(), te.sum()))
            b0 = np.linalg.lstsq(base[trn], yv[trn], rcond=None)[0]; pr_["U0"][te] = base[te] @ b0
            b1 = np.linalg.lstsq(Xp1[trn], yv[trn], rcond=None)[0]; pr_["P1"][te] = Xp1[te] @ b1
            Xt = Xn1[trn]; bn = np.linalg.lstsq(Xt, yv[trn], rcond=None)[0]; pr_["N1"][te] = Xn1[te] @ bn
            res = yv[trn] - Xt @ bn; s2 = res @ res / (trn.sum() - Xt.shape[1]); cov = s2 * np.linalg.pinv(Xt.T @ Xt); lam = np.zeros(21)
            for j in range(3):
                bj = bn[nb + 7 * j: nb + 7 * j + 7]; sj = np.sqrt(np.diag(cov)[nb + 7 * j: nb + 7 * j + 7]); wt = 1 / sj ** 2; bb = (wt * bj).sum() / wt.sum(); Q = (wt * (bj - bb) ** 2).sum(); c_ = wt.sum() - (wt ** 2).sum() / wt.sum(); tau2 = max(0.0, (Q - 6) / c_)
                lam[7 * j: 7 * j + 7] = s2 / tau2 if tau2 > 1e-10 else 1e8; tau_log.append(np.sqrt(tau2))
            Xh = Xhb = Xhb_ = Xhb = Xhb = Xhb = None; Xh = Xhb_ = None
            Xh = Xhb = Xhb_ = None; Xfull = Xhb if False else Xhb_
            Xh = np.c_[base[trn], P[trn], np.hstack([P[trn][:, [j]] * Cm[trn] for j in range(3)])]; pen = np.r_[np.zeros(nb + 3), lam]
            bh = np.linalg.solve(Xh.T @ Xh + np.diag(pen), Xh.T @ yv[trn]); Xte = np.c_[base[te], P[te], np.hstack([P[te][:, [j]] * Cm[te] for j in range(3)])]; pr_["HB"][te] = Xte @ bh
            for k_ in sse: fm[k_].append(float(((yv[te] - pr_[k_][te]) ** 2).mean()))
        for k_ in sse: sse[k_] += (yv - pr_[k_]) ** 2 / REP
    J = REP * K_F; ratio = np.mean([b / a for a, b in ntt])
    for k_ in sse: cv_rows.append(dict(outcome=lab, model=k_, N=n, rmse_oos=float(np.sqrt(sse[k_].mean())), incr_R2_vs_U0=1 - sse[k_].sum() / sse["U0"].sum()))
    for ref, mdl in [("P1", "HB"), ("N1", "HB"), ("P1", "N1"), ("U0", "P1")]:
        dl = sse[ref] - sse[mdl]; fd = np.array(fm[ref]) - np.array(fm[mdl]); nbse = np.sqrt((1 / J + ratio) * fd.var(ddof=1))
        pw_rows.append(dict(outcome=lab, reference=ref, model=mdl, mse_reduction=dl.mean(), firm_ci_lo=dl.mean() - 1.96 * dl.std(ddof=1) / np.sqrt(n), firm_ci_hi=dl.mean() + 1.96 * dl.std(ddof=1) / np.sqrt(n), nb_ci_lo=fd.mean() - stats.t.ppf(.975, J - 1) * nbse, nb_ci_hi=fd.mean() + stats.t.ppf(.975, J - 1) * nbse, nb_p=2 * stats.t.sf(abs(fd.mean() / nbse), J - 1)))
cv, pw = pd.DataFrame(cv_rows), pd.DataFrame(pw_rows); print(cv.round(4).to_string()); print(pw.round(4).to_string())
with pd.ExcelWriter(os.path.join(OUTD, "ROBUSTNESS_V6_B.xlsx")) as wx:
    wb.to_excel(wx, sheet_name="wild_cluster_bootstrap", index=False); ncl.to_excel(wx, sheet_name="cluster_counts", index=False); cv.to_excel(wx, sheet_name="oos_with_partial_pooling", index=False); pw.to_excel(wx, sheet_name="oos_paired", index=False)
log("25b: done")
