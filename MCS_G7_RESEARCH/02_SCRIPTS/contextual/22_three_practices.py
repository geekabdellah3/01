"""V5 core analysis: Bloom & Van Reenen's three mechanisms entered separately - Monitoring (r2), Targets (r4), Incentives (r8) - as 0/1 gates whose direction (1 = yes) is verified by the skip logic.
Q1 individual associations; Q2 combinations (pairwise interactions); Q3 stability across countries and organisational contexts; out-of-sample comparison and transferability. Associations only."""
import os, sys, warnings
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
import statsmodels.api as sm
from scipy import stats
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
OUTD = os.path.join(ROOT, "08_CONTEXTUAL_FIT")
d = load_analytic(); raw = load_raw(); raw = raw[raw.r1.notna()].copy(); raw["firm_key"] = raw.cid + "_" + raw.source_row.astype(str)
dd = d.join(raw.set_index("firm_key")[["b2b", "d3b", "d3c", "b7", "b7a"]], on="firm_key")
dd["M"], dd["T"], dd["I"] = dd.A_r2, dd.A_r4, dd.A_r8; dd["Mb"] = dd.B_r3x          # monitoring breadth 0-3 (bands of r3; sensitivity)
dd["foreign10"] = np.where(dd.b2b >= 10, 1.0, np.where(dd.b2b >= 0, 0.0, np.nan))
dd["exporter"] = np.where((dd.d3b.fillna(-1) >= 0) & (dd.d3c.fillna(-1) >= 0), ((dd.d3b + dd.d3c) > 0).astype(float), np.nan)
dd["ln_mgr_exp"] = np.log(dd.b7.where(dd.b7 > 0)); dd["female_mgr"] = dd.b7a.map({1: 1.0, 2: 0.0})
w = lambda s: s.clip(s.quantile(.01), s.quantile(.99))
dd["sales_growth3y_ann"] = w(dd.sales_growth3y_ann); dd["emp_growth3y_ann"] = w(dd.emp_growth3y_ann); dd["ln_lp"] = dd.groupby("cid").ln_lp.transform(lambda s: s.clip(s.quantile(.005), s.quantile(.995)))
OUT = {"ln_lp": "Log sales per employee", "sales_growth3y_ann": "Sales growth (ann.)", "emp_growth3y_ann": "Employment growth (ann.)"}
MODS = {"ln_emp": "Size", "ln_age": "Age", "foreign10": "Foreign ownership >=10%", "exporter": "Exporter", "ln_mgr_exp": "Manager experience (log)", "female_mgr": "Female top manager"}
PR = ["M", "T", "I"]
def holm(p):
    p = np.asarray(p); o = np.argsort(p); m_ = len(p); adj = np.empty(m_); run = 0
    for i, j in enumerate(o): run = max(run, (m_ - i) * p[j]); adj[j] = min(1, run)
    return adj
def fit(X, y, groups=None, cluster=False):
    return sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": groups}) if cluster else sm.OLS(y, X).fit(cov_type="HC3")
def FE(sub): return pd.get_dummies(sub.sector_c.astype(str), dtype=float).values
def CD(sub): return pd.get_dummies(sub.cid, dtype=float).reindex(columns=CORDER, fill_value=0.0).values
def wald(m, rows):
    L = np.zeros((len(rows), len(m.params)))
    for i, r in enumerate(rows):
        for k, v in r.items(): L[i, k] = v
    t = m.wald_test(L, use_f=False, scalar=True); return float(t.statistic), float(t.pvalue)
R1, R2, R3, RH, RM, RC = [], [], [], [], [], []
for y, lab in OUT.items():
    s0 = dd.dropna(subset=[y, "M", "T", "I", "ln_emp", "ln_age"]).reset_index(drop=True); n0 = len(s0); F = FE(s0); P = s0[PR].values; ctrl = np.c_[s0.ln_emp.values, s0.ln_age.values]; yv = s0[y].values; Cm = CD(s0); sd_y = yv.std()
    # ---- Q1 individual associations (pooled; sector-within-country FE)
    m = fit(np.c_[F, ctrl, P], yv); k0 = F.shape[1] + 2; ci = m.conf_int()
    for j, p in enumerate(PR): R1.append(dict(outcome=lab, practice=p, N=n0, beta=m.params[k0 + j], se=m.bse[k0 + j], ci_lo=ci[k0 + j, 0], ci_hi=ci[k0 + j, 1], p=m.pvalues[k0 + j], beta_in_outcome_SD=m.params[k0 + j] / sd_y))
    st, pv = wald(m, [{k0: 1}, {k0 + 1: 1}, {k0 + 2: 1}]); R1.append(dict(outcome=lab, practice="joint M,T,I", N=n0, beta=np.nan, se=np.nan, ci_lo=np.nan, ci_hi=np.nan, p=pv, beta_in_outcome_SD=np.nan))
    sb = s0.dropna(subset=["Mb"]); mb = fit(np.c_[FE(sb), sb.ln_emp.values, sb.ln_age.values, sb[["Mb", "T", "I"]].values], sb[y].values); kb = FE(sb).shape[1] + 2
    for j, p in enumerate(["Mb(0-3)", "T", "I"]): R1.append(dict(outcome=lab, practice=p + " [breadth variant]", N=len(sb), beta=mb.params[kb + j], se=mb.bse[kb + j], ci_lo=mb.conf_int()[kb + j, 0], ci_hi=mb.conf_int()[kb + j, 1], p=mb.pvalues[kb + j], beta_in_outcome_SD=mb.params[kb + j] / sb[y].std()))
    # ---- Q2 combinations
    Pi = np.c_[P[:, 0] * P[:, 1], P[:, 0] * P[:, 2], P[:, 1] * P[:, 2]]; m2 = fit(np.c_[F, ctrl, P, Pi], yv); ci2 = m2.conf_int()
    for j, nm in enumerate(["MxT", "MxI", "TxI"]): R2.append(dict(outcome=lab, term=nm, N=n0, coef=m2.params[k0 + 3 + j], se=m2.bse[k0 + 3 + j], ci_lo=ci2[k0 + 3 + j, 0], ci_hi=ci2[k0 + 3 + j, 1], p=m2.pvalues[k0 + 3 + j]))
    st, pv = wald(m2, [{k0 + 3: 1}, {k0 + 4: 1}, {k0 + 5: 1}]); R2.append(dict(outcome=lab, term="joint pairwise (3 df)", N=n0, coef=np.nan, se=np.nan, ci_lo=np.nan, ci_hi=np.nan, p=pv))
    m3 = fit(np.c_[F, ctrl, P, Pi, P.prod(1)], yv); st, pv = wald(m3, [{k0 + 6: 1}]); R2.append(dict(outcome=lab, term="three-way MxTxI", N=n0, coef=m3.params[k0 + 6], se=m3.bse[k0 + 6], ci_lo=m3.conf_int()[k0 + 6, 0], ci_hi=m3.conf_int()[k0 + 6, 1], p=pv))
    # ---- Q3 by country: separate regressions + heterogeneity
    bs = {p: [] for p in PR}; ses = {p: [] for p in PR}
    for c in CORDER:
        sc = s0[s0.cid == c]; mc = fit(np.c_[FE(sc), sc.ln_emp.values, sc.ln_age.values, sc[PR].values], sc[y].values); kc = FE(sc).shape[1] + 2; cic = mc.conf_int()
        for j, p in enumerate(PR):
            R3.append(dict(outcome=lab, country=c, practice=p, N=len(sc), beta=mc.params[kc + j], se=mc.bse[kc + j], ci_lo=cic[kc + j, 0], ci_hi=cic[kc + j, 1], prevalence=float(sc[p].mean()))); bs[p].append(mc.params[kc + j]); ses[p].append(mc.bse[kc + j])
    for p in PR:
        b, se = np.array(bs[p]), np.array(ses[p]); wt = 1 / se ** 2; bb = (wt * b).sum() / wt.sum(); Q = (wt * (b - bb) ** 2).sum(); I2 = max(0, (Q - 6) / Q) * 100
        tau2 = max(0, (Q - 6) / (wt.sum() - (wt ** 2).sum() / wt.sum())); wr = 1 / (se ** 2 + tau2); bre = (wr * b).sum() / wr.sum()
        RH.append(dict(outcome=lab, practice=p, Q=Q, p_Q=stats.chi2.sf(Q, 6), I2=I2, tau=np.sqrt(tau2), RE_mean=bre))
    # pooled equality tests: practice x country (country-specific control slopes), HC3 and sector-cluster
    for cl in (False, True):
        Xc = np.c_[F, ctrl[:, [0]] * Cm, ctrl[:, [1]] * Cm] ; blocks = [P[:, [j]] * Cm for j in range(3)]; Xf = np.c_[Xc] ; start = Xf.shape[1]
        Xf = np.c_[Xf, blocks[0], blocks[1], blocks[2]]; mm = fit(Xf, yv, groups=pd.factorize(s0.sector_c)[0], cluster=cl)
        def rows_for(j): base = start + 7 * j; return [{base: -1, base + c: 1} for c in range(1, 7)]
        for j, p in enumerate(PR): st, pv = wald(mm, rows_for(j)); RC.append(dict(outcome=lab, test=f"equality of {p} slopes across countries (6 df)", cov="cluster(sector)" if cl else "HC3", N=n0, wald_chi2=st, p=pv))
        st, pv = wald(mm, rows_for(0) + rows_for(1) + rows_for(2)); RC.append(dict(outcome=lab, test="joint equality of M,T,I slopes (18 df)", cov="cluster(sector)" if cl else "HC3", N=n0, wald_chi2=st, p=pv))
    # ---- organisational moderators (joint 3 df per moderator, with main effects)
    for mv, ml in MODS.items():
        sm_ = s0.dropna(subset=[mv]); z = sm_[mv].values if mv in ("foreign10", "exporter", "female_mgr") else (sm_[mv].values - sm_[mv].mean()) / sm_[mv].std(); Pm = sm_[PR].values
        own = mv in ("ln_emp", "ln_age")      # size/age already enter as controls: no duplicate main effect
        Xm = np.c_[FE(sm_), sm_.ln_emp.values, sm_.ln_age.values, Pm] if own else np.c_[FE(sm_), sm_.ln_emp.values, sm_.ln_age.values, Pm, z]; Xm = np.c_[Xm, Pm * z[:, None]]; mmod = fit(Xm, sm_[y].values)
        base = FE(sm_).shape[1] + 2 + 3 + (0 if own else 1); st, pv = wald(mmod, [{base + j: 1} for j in range(3)])
        RM.append(dict(outcome=lab, moderator=ml, N=len(sm_), wald_chi2_3df=st, p=pv, **{f"int_{PR[j]}": mmod.params[base + j] for j in range(3)}, **{f"se_{PR[j]}": mmod.bse[base + j] for j in range(3)}))
R1, R2, R3, RH, RM, RC = map(pd.DataFrame, (R1, R2, R3, RH, RM, RC))
R2["p_holm"] = np.nan; msk = R2.term.isin(["MxT", "MxI", "TxI"]); R2.loc[msk, "p_holm"] = holm(R2.loc[msk, "p"].values)
RM["p_holm"] = holm(RM.p.values); RC["p_holm_within_cov"] = np.nan
print(R1.round(4).to_string()); print(R2.round(4).to_string()); print(RH.round(4).to_string()); print(RC.round(4).to_string()); print(RM.round(4).to_string()); print("Q1-Q3 done", flush=True)
# ---------- figure: country-specific coefficients by practice (productivity)
fig, axs = plt.subplots(1, 3, figsize=(12.5, 3.9), sharey=True); colr = {"M": "#0072B2", "T": "#009E73", "I": "#D55E00"}
for ax, p, ttl in zip(axs, PR, ["Monitoring (r2)", "Targets (r4)", "Incentives (r8)"]):
    g = R3[(R3.outcome == "Log sales per employee") & (R3.practice == p)].set_index("country").reindex(CORDER); y_ = np.arange(7)[::-1]
    ax.errorbar(g.beta, y_, xerr=[g.beta - g.ci_lo, g.ci_hi - g.beta], fmt="o", color=colr[p], capsize=2); ax.axvline(0, color="#ccc")
    h = RH[(RH.outcome == "Log sales per employee") & (RH.practice == p)].iloc[0]; ax.set_title(f"{ttl}\nQ p = {h.p_Q:.2f}, I² = {h.I2:.0f}%", fontsize=9, loc="left"); ax.set_yticks(y_); ax.set_yticklabels([f"{c} ({int(n)})" for c, n in zip(CORDER, g.N)], fontsize=8); ax.set_xlabel("Association with log sales per employee (95% CI)")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "Fig8_three_practices_by_country.png"), dpi=300); plt.savefig(os.path.join(FIG, "Fig8_three_practices_by_country.pdf")); plt.close()
# ---------- out-of-sample comparison
K_F, REP = 10, 3; CV, PW = [], []
for y, lab in OUT.items():
    s0 = dd.dropna(subset=[y, "M", "T", "I", "ln_emp", "ln_age"] + list(MODS)).reset_index(drop=True); n = len(s0); F = FE(s0); P = s0[PR].values; Cm = CD(s0); yv = s0[y].values
    Z = np.c_[[(s0[m_].values - s0[m_].mean()) / s0[m_].std() for m_ in MODS]].T; base = np.c_[F, Z[:, 0:2], Z[:, 2:]]          # same main effects in every model
    Pi = np.c_[P[:, 0] * P[:, 1], P[:, 0] * P[:, 2], P[:, 1] * P[:, 2]]
    D_ = {"U0": base, "P1 universal (M,T,I common slopes)": np.c_[base, P], "P2 universal + combinations": np.c_[base, P, Pi],
          "C1 organisational contingency": np.c_[base, P] if False else np.c_[base, P, np.hstack([P * Z[:, [j]] for j in range(6)])],
          "N1 national slopes (M,T,I x country)": np.c_[base, np.hstack([P[:, [j]] * Cm for j in range(3)])],
          "X organisational + national": np.c_[base, P, np.hstack([P * Z[:, [j]] for j in range(6)]), np.hstack([P[:, [j]] * Cm[:, 1:] for j in range(3)])]}
    sse = {k_: np.zeros(n) for k_ in D_}; fm = {k_: [] for k_ in D_}; ntt = []
    for rep in range(REP):
        rng = np.random.default_rng(SEED + rep); fold = np.zeros(n, int)
        for c in CORDER:
            ii = rng.permutation(np.where(s0.cid.values == c)[0]); fold[ii] = np.arange(len(ii)) % K_F
        pr_ = {k_: np.zeros(n) for k_ in D_}
        for f in range(K_F):
            te = fold == f; trn = ~te
            if rep == 0: ntt.append((trn.sum(), te.sum()))
            for k_, X in D_.items():
                b = np.linalg.lstsq(X[trn], yv[trn], rcond=None)[0]; pr_[k_][te] = X[te] @ b; fm[k_].append(float(((yv[te] - pr_[k_][te]) ** 2).mean()))
        for k_ in D_: sse[k_] += (yv - pr_[k_]) ** 2 / REP
    ratio = np.mean([b / a for a, b in ntt]); J = REP * K_F
    for k_ in D_: CV.append(dict(outcome=lab, model=k_, N=n, rmse_oos=float(np.sqrt(sse[k_].mean())), incr_R2_vs_U0=1 - sse[k_].sum() / sse["U0"].sum()))
    for ref, mdl in [("U0", "P1 universal (M,T,I common slopes)"), ("P1 universal (M,T,I common slopes)", "P2 universal + combinations"), ("P1 universal (M,T,I common slopes)", "C1 organisational contingency"), ("P1 universal (M,T,I common slopes)", "N1 national slopes (M,T,I x country)"), ("C1 organisational contingency", "X organisational + national")]:
        dl = sse[ref] - sse[mdl]; m_, se = dl.mean(), dl.std(ddof=1) / np.sqrt(n); fd = np.array(fm[ref]) - np.array(fm[mdl]); nb = np.sqrt((1 / J + ratio) * fd.var(ddof=1))
        PW.append(dict(outcome=lab, reference=ref, model=mdl, mse_reduction=m_, ci_lo=m_ - 1.96 * se, ci_hi=m_ + 1.96 * se, rel_pct=100 * m_ / sse[ref].mean(), nb_ci_lo=fd.mean() - stats.t.ppf(.975, J - 1) * nb, nb_ci_hi=fd.mean() + stats.t.ppf(.975, J - 1) * nb, nb_p=2 * stats.t.sf(abs(fd.mean() / nb), J - 1)))
CV, PW = pd.DataFrame(CV), pd.DataFrame(PW); print(CV.round(4).to_string()); print(PW.round(4).to_string()); print("CV done", flush=True)
# ---------- transferability of the three-practice model
def demean(df, cols):
    out = df.copy()
    for c in cols: out[c] = df[c] - df.groupby("sector_c")[c].transform("mean")
    return out
TR, TP = [], []
for y, lab in OUT.items():
    s0 = dd.dropna(subset=[y, "M", "T", "I", "ln_emp", "ln_age"]).copy(); s0 = demean(s0, [y, "M", "T", "I", "ln_emp", "ln_age"]); G = {c: (s0[s0.cid == c][PR + ["ln_emp", "ln_age"]].values, s0[s0.cid == c][y].values) for c in CORDER}
    for t_ in CORDER:
        Xt, yt = G[t_]; oth = [k for k in CORDER if k != t_]; Xo = np.vstack([G[k][0] for k in oth]); yo = np.concatenate([G[k][1] for k in oth]); den = (yt ** 2).sum()
        b_loco = np.linalg.lstsq(Xo, yo, rcond=None)[0]; e_loco = (yt - Xt @ b_loco) ** 2; e_loc = np.zeros(len(yt)); e_glob = np.zeros(len(yt)); rg = np.random.default_rng(SEED + 5)
        for rep in range(5):
            f = np.random.default_rng(SEED + rep).permutation(len(yt)) % 10
            for k in range(10):
                trm, tem = f != k, f == k; bl = np.linalg.lstsq(Xt[trm], yt[trm], rcond=None)[0]; e_loc[tem] += ((yt[tem] - Xt[tem] @ bl) ** 2) / 5
                bg = np.linalg.lstsq(np.vstack([Xo, Xt[trm]]), np.concatenate([yo, yt[trm]]), rcond=None)[0]; e_glob[tem] += ((yt[tem] - Xt[tem] @ bg) ** 2) / 5
        for nm, e in [("LOCO (six other countries)", e_loco), ("global pooled incl. target training folds", e_glob)]:
            dl = e - e_loc; bsr = [dl[rg.integers(0, len(dl), len(dl))].sum() / den for _ in range(400)]
            TP.append(dict(outcome=lab, target=t_, N_target=len(yt), benchmark=nm, R2_local=1 - e_loc.sum() / den, R2_benchmark=1 - e.sum() / den, gap_local_minus_benchmark=dl.sum() / den, ci_lo=np.percentile(bsr, 2.5), ci_hi=np.percentile(bsr, 97.5)))
        for s_ in oth:
            Xs_, ys_ = G[s_]; b = np.linalg.lstsq(Xs_, ys_, rcond=None)[0]; TR.append(dict(outcome=lab, source=s_, target=t_, R2_transfer=1 - ((yt - Xt @ b) ** 2).sum() / den, R2_local=1 - e_loc.sum() / den))
TR, TP = pd.DataFrame(TR), pd.DataFrame(TP); print(TP[TP.outcome == "Log sales per employee"].round(4).to_string()); print(TR[TR.outcome == "Log sales per employee"].pivot(index="source", columns="target", values="R2_transfer").reindex(index=CORDER, columns=CORDER).round(3).to_string())
with pd.ExcelWriter(os.path.join(OUTD, "THREE_PRACTICES_TABLES.xlsx")) as wx:
    R1.to_excel(wx, sheet_name="Q1_individual", index=False); R2.to_excel(wx, sheet_name="Q2_combinations", index=False); R3.to_excel(wx, sheet_name="Q3_by_country", index=False); RH.to_excel(wx, sheet_name="Q3_heterogeneity", index=False)
    RC.to_excel(wx, sheet_name="Q3_equality_Wald", index=False); RM.to_excel(wx, sheet_name="organisational_moderators", index=False); CV.to_excel(wx, sheet_name="oos_models", index=False); PW.to_excel(wx, sheet_name="oos_paired", index=False)
    TP.to_excel(wx, sheet_name="transfer_vs_local", index=False); TR.to_excel(wx, sheet_name="transfer_matrix_long", index=False)
log("22 three practices: done")
