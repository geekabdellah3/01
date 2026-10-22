import os, sys, json
sys.path.insert(0, "../../02_SCRIPTS"); from common import *
d5 = json.load(open("../revision_v5/data5.json")); X = os.path.join(ROOT, "08_CONTEXTUAL_FIT")
A = pd.read_excel(os.path.join(X, "ROBUSTNESS_V6_A.xlsx"), sheet_name=None); Bt = pd.read_excel(os.path.join(X, "ROBUSTNESS_V6_B.xlsx"), sheet_name=None); T3 = pd.read_excel(os.path.join(X, "THREE_PRACTICES_TABLES.xlsx"), sheet_name=None)
OUT = ["Log sales per employee", "Sales growth (ann.)", "Employment growth (ann.)"]; PN = {"M": "Monitoring (r2)", "T": "Targets (r4)", "I": "Incentives (r8)"}
def holm(p):
    p = np.asarray(p); o = np.argsort(p); m_ = len(p); adj = np.empty(m_); run = 0
    for i, j in enumerate(o): run = max(run, (m_ - i) * p[j]); adj[j] = min(1, run)
    return adj
wb = Bt["wild_cluster_bootstrap"]; w9 = wb[wb.test.str.startswith("equality")].copy(); w9["holm_wild"] = holm(w9.p_wild_cluster_bootstrap.values)
rc = T3["Q3_equality_Wald"]; hc = rc[(rc["cov"] == "HC3") & rc.test.str.startswith("equality")].copy(); hc["holm"] = holm(hc.p.values)
t_eq = []
for p in ["M", "T", "I"]:
    row = [PN[p]]
    for o in OUT:
        a = hc[(hc.outcome == o) & hc.test.str.contains(f"of {p} slopes")].iloc[0]; b = w9[(w9.outcome == o) & w9.test.str.contains(f"of {p} slopes")].iloc[0]
        row.append(f"HC3 p = {a.p:.4f} (Holm {a.holm:.3f}); wild-bootstrap p = {b.p_wild_cluster_bootstrap:.3f} (Holm {b.holm_wild:.3f})")
    t_eq.append(row)
row = ["Joint (18 df)"]
for o in OUT:
    a = rc[(rc.outcome == o) & (rc["cov"] == "HC3") & rc.test.str.startswith("joint")].iloc[0]; b = wb[(wb.outcome == o) & wb.test.str.startswith("joint")].iloc[0]; row.append(f"HC3 p = {a.p:.4f}; wild-bootstrap p = {b.p_wild_cluster_bootstrap:.3f}")
t_eq.append(row)
H = A["heterogeneity_robustness"]; Hi = H[H.practice == "I"].set_index("spec"); main = Hi.loc["main (winsorised 0.5/99.5 within country, HC3)"]
loco = Hi[Hi.index.str.startswith("leave out")]
t_rob = [["Main specification (HC3)", f"{main.Q:.1f}", f"{main.p:.4f}", f"{main.I2:.0f} [{main.I2_ci_lo:.0f}, {main.I2_ci_hi:.0f}]", f"{main.tau:.3f} [{main.tau_ci_lo:.3f}, {main.tau_ci_hi:.3f}]"],
         [f"Leave one country out (range of 7)", f"{loco.Q.min():.1f}–{loco.Q.max():.1f}", f"{loco.p.min():.4f}–{loco.p.max():.3f}", f"{loco.I2.min():.0f}–{loco.I2.max():.0f}", f"{loco.tau.min():.3f}–{loco.tau.max():.3f}"]]
for nm in ["weighted WLS (wmedian)", "no winsorisation", "winsorised 5/95 within country", "median regression (no winsorisation)"]:
    r = Hi.loc[nm]; t_rob.append([nm[0].upper() + nm[1:], f"{r.Q:.1f}", f"{r.p:.4f}", f"{r.I2:.0f}", f"{r.tau:.3f}"])
wi = w9[(w9.outcome == OUT[0]) & w9.test.str.contains("of I slopes")].iloc[0]; t_rob.append(["Wild cluster bootstrap (73 clusters)", "–", f"{wi.p_wild_cluster_bootstrap:.3f}", "–", "–"])
cv = Bt["oos_with_partial_pooling"]; pw = Bt["oos_paired"]; old_cv = d5["t_cv"]
hb = cv[(cv.outcome == OUT[0]) & (cv.model == "HB")].iloc[0]; hb_g = [cv[(cv.outcome == o) & (cv.model == "HB")].iloc[0].rmse_oos for o in OUT[1:]]
t_cv = old_cv + [["HB partial pooling (shrunk country slopes)", f"{hb.rmse_oos:.4f}", f"{100*hb.incr_R2_vs_U0:.2f}", f"{hb_g[0]:.4f}", f"{hb_g[1]:.4f}"]]
t_pw = d5["t_pw"]; 
for ref, mdl, nm in [("P1", "HB", "HB partial pooling vs P1"), ("N1", "HB", "HB partial pooling vs N1")]:
    r = pw[(pw.outcome == OUT[0]) & (pw.reference == ref) & (pw.model == mdl)].iloc[0]; t_pw.append([nm, f"{r.mse_reduction:.4f} [{r.firm_ci_lo:.4f}, {r.firm_ci_hi:.4f}]", f"[{r.nb_ci_lo:.4f}, {r.nb_ci_hi:.4f}]", f"{r.nb_p:.3f}"])
d5.update(t_eq=t_eq, t_rob=t_rob, t_cv=t_cv, t_pw=t_pw)
json.dump(d5, open("data6.json", "w"), indent=1); print(t_eq); print(t_rob); print(t_pw[-2:])
