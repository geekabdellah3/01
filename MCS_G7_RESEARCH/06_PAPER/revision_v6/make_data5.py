import os, sys, json
sys.path.insert(0, "../../02_SCRIPTS"); from common import *
from PIL import Image
X = pd.read_excel(os.path.join(ROOT, "08_CONTEXTUAL_FIT/THREE_PRACTICES_TABLES.xlsx"), sheet_name=None)
old = json.load(open("../revision_v2/data2.json"))
OUT = ["Log sales per employee", "Sales growth (ann.)", "Employment growth (ann.)"]; PN = {"M": "Monitoring (r2)", "T": "Targets (r4)", "I": "Incentives (r8)"}
def nd(o): return 3 if o.startswith("Log") else 4
q1 = X["Q1_individual"]; t_q1 = []
for p in ["M", "T", "I"]:
    row = [PN[p]]
    for o in OUT:
        r = q1[(q1.outcome == o) & (q1.practice == p)].iloc[0]; row.append(f"{r.beta:.{nd(o)}f} [{r.ci_lo:.{nd(o)}f}, {r.ci_hi:.{nd(o)}f}]")
    t_q1.append(row)
t_q1.append(["Joint test M, T, I (p)"] + [f"{q1[(q1.outcome==o)&(q1.practice=='joint M,T,I')].p.iloc[0]:.4f}" for o in OUT])
t_q1.append(["N"] + [str(int(q1[(q1.outcome == o) & (q1.practice == 'M')].N.iloc[0])) for o in OUT])
q2 = X["Q2_combinations"]; t_q2 = []
for t_ in ["MxT", "MxI", "TxI", "three-way MxTxI"]:
    row = [{"MxT": "Monitoring × Targets", "MxI": "Monitoring × Incentives", "TxI": "Targets × Incentives", "three-way MxTxI": "Three-way (M × T × I)"}[t_]]
    for o in OUT:
        r = q2[(q2.outcome == o) & (q2.term == t_)].iloc[0]; row.append(f"{r.coef:.{nd(o)}f} [{r.ci_lo:.{nd(o)}f}, {r.ci_hi:.{nd(o)}f}] (p = {r.p:.3f})")
    t_q2.append(row)
t_q2.append(["Joint pairwise test (3 df), p"] + [f"{q2[(q2.outcome==o)&(q2.term=='joint pairwise (3 df)')].p.iloc[0]:.3f}" for o in OUT])
q3 = X["Q3_by_country"]; q3 = q3[q3.outcome == OUT[0]]; t_q3 = []
for c in CORDER:
    row = [c, str(int(q3[(q3.country == c) & (q3.practice == 'M')].N.iloc[0]))]
    for p in ["M", "T", "I"]:
        r = q3[(q3.country == c) & (q3.practice == p)].iloc[0]; row.append(f"{r.beta:.3f} [{r.ci_lo:.3f}, {r.ci_hi:.3f}]")
    t_q3.append(row)
H = X["Q3_heterogeneity"]; H1 = H[H.outcome == OUT[0]].set_index("practice")
t_q3.append(["Q (df = 6), p; I²", ""] + [f"{H1.loc[p,'Q']:.1f}, p = {H1.loc[p,'p_Q']:.4f}; I² = {H1.loc[p,'I2']:.0f}%" for p in ["M", "T", "I"]])
t_q3.append(["Random-effects mean (τ)", ""] + [f"{H1.loc[p,'RE_mean']:.3f} (τ = {H1.loc[p,'tau']:.3f})" for p in ["M", "T", "I"]])
# equality tests with Holm over the 9 HC3 per-practice tests
rc = X["Q3_equality_Wald"]; hc = rc[(rc["cov"] == "HC3") & rc.test.str.startswith("equality")].copy()
def holm(p):
    p = np.asarray(p); o = np.argsort(p); m_ = len(p); adj = np.empty(m_); run = 0
    for i, j in enumerate(o): run = max(run, (m_ - i) * p[j]); adj[j] = min(1, run)
    return adj
hc["holm"] = holm(hc.p.values); cl = rc[(rc["cov"] == "cluster(sector)")]
t_eq = []
for p in ["M", "T", "I"]:
    row = [PN[p]]
    for o in OUT:
        a = hc[(hc.outcome == o) & hc.test.str.contains(f"of {p} slopes")].iloc[0]; b = cl[(cl.outcome == o) & cl.test.str.contains(f"of {p} slopes")].iloc[0]; row.append(f"p = {a.p:.4f} (Holm {a.holm:.3f}); cluster p = {b.p:.4f}")
    t_eq.append(row)
row = ["Joint (18 df)"]
for o in OUT:
    a = rc[(rc.outcome == o) & (rc["cov"] == "HC3") & rc.test.str.startswith("joint")].iloc[0]; b = rc[(rc.outcome == o) & (rc["cov"] == "cluster(sector)") & rc.test.str.startswith("joint")].iloc[0]; row.append(f"p = {a.p:.4f}; cluster p = {b.p:.4f}")
t_eq.append(row)
mo = X["organisational_moderators"]; mo = mo.assign(p_holm18=holm(mo.p.values)); mo1 = mo[mo.outcome == OUT[0]]
t_mo = [[r.moderator, int(r.N), f"{r.wald_chi2_3df:.1f}", f"{r.p:.4f}", f"{r.p_holm18:.2f}"] for _, r in mo1.iterrows()]
cv = X["oos_models"]; pw = X["oos_paired"]
t_cv = []
for m in cv.model.unique():
    row = [m]
    r = cv[(cv.outcome == OUT[0]) & (cv.model == m)].iloc[0]; row += [f"{r.rmse_oos:.4f}", f"{100*r.incr_R2_vs_U0:.2f}"]
    for o in OUT[1:]: row.append(f"{cv[(cv.outcome==o)&(cv.model==m)].iloc[0].rmse_oos:.4f}")
    t_cv.append(row)
p1 = pw[pw.outcome == OUT[0]]; t_pw = [[f"{r.model} vs {r.reference}", f"{r.mse_reduction:.4f} [{r.ci_lo:.4f}, {r.ci_hi:.4f}]", f"[{r.nb_ci_lo:.4f}, {r.nb_ci_hi:.4f}]", ("<0.001" if r.nb_p < 0.001 else f"{r.nb_p:.3f}")] for _, r in p1.iterrows()]
tr = X["transfer_matrix_long"]; tr = tr[tr.outcome == OUT[0]]; tp = X["transfer_vs_local"]; tp = tp[tp.outcome == OUT[0]]
t_tr = []
for s in CORDER: t_tr.append([s] + ["–" if s == t else f"{tr[(tr.source==s)&(tr.target==t)].R2_transfer.iloc[0]:.3f}" for t in CORDER])
lo = tp[tp.benchmark.str.startswith("LOCO")].set_index("target").reindex(CORDER)
t_tr.append(["LOCO"] + [f"{lo.loc[t,'R2_benchmark']:.3f}" for t in CORDER]); t_tr.append(["Local (CV)"] + [f"{lo.loc[t,'R2_local']:.3f}" for t in CORDER])
t_tr.append(["Local − LOCO [95% CI]"] + [f"{lo.loc[t,'gap_local_minus_benchmark']:.3f} [{lo.loc[t,'ci_lo']:.3f}, {lo.loc[t,'ci_hi']:.3f}]" for t in CORDER])
mat = tr.pivot(index="source", columns="target", values="R2_transfer").reindex(index=CORDER, columns=CORDER); off = mat.values[~np.eye(7, dtype=bool)]
loc = tr.drop_duplicates("target").set_index("target").R2_local.reindex(CORDER); share_loc = float(np.mean([loc[t] > mat.loc[s, t] for s in CORDER for t in CORDER if s != t])); mean_gap = float(np.mean([loc[t] - mat.loc[s, t] for s in CORDER for t in CORDER if s != t]))
figs = {}
for k, fn in {"frame": "Fig_Framework_v5_practices_to_transferability.png", "forest": "Fig8_three_practices_by_country.png", "dim": "Fig4_dimensionality.png"}.items():
    p = os.path.abspath(os.path.join(FIG, fn)); w_, h_ = Image.open(p).size; figs[k] = dict(path=p, w=w_, h=h_)
json.dump(dict(t1=old["t1"], t_q1=t_q1, t_q2=t_q2, t_q3=t_q3, t_eq=t_eq, t_mo=t_mo, t_cv=t_cv, t_pw=t_pw, t_tr=t_tr, share_loc=share_loc, mean_gap=mean_gap, figs=figs, t2=old["t2"][:6]), open("data5.json", "w"), indent=1)
print(t_q1, t_eq, t_pw, share_loc, mean_gap, sep="\n")
