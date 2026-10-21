"""STEP 8: empirical control structure - EFA on polychoric correlations, category ordering diagnostics, co-occurrence patterns, model-class verdict."""
import os, sys, pickle, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from poly import *
from lca_core import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
d = load_analytic(); store = pickle.load(open(os.path.join(RES, "lca/lca_store.pkl"), "rb"))
res = os.path.join(RES, "dimensionality")
def Xof(tag):
    cols = [c for c in d if c.startswith(tag + "_")]; X = d[cols].fillna(-1).astype(int).values; k = (X >= 0).any(1)
    return [c[2:] for c in cols], X[k], [int(X[k, j].max()) + 1 for j in range(len(cols))], k
sheets = {}
# --- EFA spec A and C (code order = ordinal order: ASSUMPTION flagged) -------------------
for tag in ["A", "C"]:
    items, X, nc, k = Xof(tag); Rm = polychoric_matrix(X, nc); Rm_p = nearest_psd(Rm)
    ev = np.linalg.eigvalsh(Rm_p)[::-1]
    fits = []
    for nf in (1, 2, 3):
        L, h, rmsr = minres(Rm, nf); P, Phi = varimax_oblimin_promax(L)
        fits.append(dict(spec=tag, n_factors=nf, RMSR=rmsr, pct_common_variance=100 * h.sum() / len(items)))
        sheets[f"EFA_{tag}_{nf}f_loadings"] = pd.DataFrame(P, index=items, columns=[f"F{i+1}" for i in range(nf)]).round(3).reset_index()
        if nf == 2: sheets[f"EFA_{tag}_2f_factor_corr"] = pd.DataFrame(Phi).round(3)
    sheets[f"EFA_{tag}_fit"] = pd.DataFrame(fits); sheets[f"EFA_{tag}_eigen"] = pd.DataFrame({"factor": range(1, len(ev) + 1), "eigenvalue": ev})
    if tag == "C": sheets["EFA_C_polychoric"] = pd.DataFrame(Rm, index=items, columns=items).round(3).reset_index()
    # country consistency: 1-factor loadings (spec A) and Tucker congruence
    if tag == "A":
        L_all, _, _ = minres(Rm, 1); L_all = L_all[:, 0] * np.sign(L_all[:, 0].sum()); rows = []
        for c in CORDER:
            m = (d[k].cid == c).values; Lc, _, rm = minres(polychoric_matrix(X[m], nc), 1); Lc = Lc[:, 0] * np.sign(Lc[:, 0].sum())
            cong = float(Lc @ L_all / np.sqrt((Lc @ Lc) * (L_all @ L_all)))
            rows.append({"country": c, "tucker_congruence_vs_pooled": cong, "RMSR_1f": rm, **{it: round(l, 3) for it, l in zip(items, Lc)}})
        sheets["EFA_A_1f_by_country"] = pd.DataFrame(rows)
# --- empirical category ordering along the continuous trait (spec A, NRM-1D) ---------------
itA, XA, ncA, kA = Xof("A"); nr = store["A"]["models"]["nrm1_1"]; th = nr["post"] @ nr["Xs"][:, 1]
if np.corrcoef(th, np.where(XA[:, 1] >= 0, XA[:, 1], 0))[0, 1] < 0: th = -th
rows = []
for j, it in enumerate(itA):
    for c in range(ncA[j]):
        m = XA[:, j] == c; rows.append(dict(item=it, category_0based=c, n=int(m.sum()), mean_theta=th[m].mean() if m.any() else np.nan, sd_theta=th[m].std() if m.any() else np.nan))
catord = pd.DataFrame(rows); sheets["category_order_vs_theta"] = catord
catord["rank_by_theta"] = catord.groupby("item").mean_theta.rank(); sheets["category_order_vs_theta"] = catord
mono = catord.groupby("item").apply(lambda g_: bool(g_.sort_values("category_0based").mean_theta.is_monotonic_increasing)).rename("code_order_monotone_in_theta").reset_index()
sheets["code_order_check"] = mono
# marginal reliability of theta
ps = nr["post"]; Xs = nr["Xs"][:, 1]; pv = (ps * (Xs[None, :] ** 2)).sum(1) - (ps @ Xs) ** 2
sheets["theta_reliability"] = pd.DataFrame([{"marginal_reliability": float(np.var(ps @ Xs) / (np.var(ps @ Xs) + pv.mean()))}])
# --- co-occurrence: gate patterns observed vs independence ---------------------------------
g3 = d[["cid", "A_r2", "A_r4", "A_r8"]].dropna(); rows = []
p_ind = {k_: g3[f"A_{k_}"].mean() for k_ in ("r2", "r4", "r8")}
for pat in itertools.product((0, 1), repeat=3):
    obs = ((g3.A_r2 == pat[0]) & (g3.A_r4 == pat[1]) & (g3.A_r8 == pat[2])).mean()
    exp = np.prod([p_ind[k_] if v else 1 - p_ind[k_] for k_, v in zip(("r2", "r4", "r8"), pat)])
    row = dict(pattern_r2_r4_r8="".join(map(str, pat)), observed_share=obs, expected_if_independent=exp, ratio=obs / exp, n=int(obs * len(g3)))
    for c in CORDER: row[c] = ((g3.cid == c) & (g3.A_r2 == pat[0]) & (g3.A_r4 == pat[1]) & (g3.A_r8 == pat[2])).sum() / (g3.cid == c).sum()
    rows.append(row)
sheets["gate_patterns"] = pd.DataFrame(rows).sort_values("observed_share", ascending=False)
itB, XB, ncB, kB = Xof("B"); pat = pd.Series(["-".join(map(str, r)) for r in XB[(XB >= 0).all(1)]]).value_counts()
sheets["specB_top_patterns"] = pd.DataFrame({"pattern(r1,r3x,r5x,r6x,r7x,r9x,r10,r11)": pat.index[:25], "n": pat.values[:25], "share": (pat.values[:25] / pat.sum()).round(4)})
sheets["specB_pattern_summary"] = pd.DataFrame([{"n_complete": int(pat.sum()), "distinct_patterns": int(len(pat)), "possible_patterns": int(np.prod(ncB)), "patterns_with_n1": int((pat == 1).sum()), "share_in_top10": float(pat.values[:10].sum() / pat.sum())}])
# --- verdict table: best model by BIC within each family ------------------------------------
cmp_ = pd.read_excel(os.path.join(RES, "lca/LCA_MODEL_SELECTION.xlsx"), sheet_name="LCA_vs_continuous_vs_hybrid")
cmp_["family"] = cmp_.model.map(lambda m: "LCA (discrete)" if m.startswith("lca") else ("1-D continuous" if m == "nrm1" else ("2-D continuous" if m == "nrm2" else "hybrid class x 1-D trait")))
verd = cmp_.loc[cmp_.groupby(["spec", "family"]).BIC.idxmin()][["spec", "family", "model", "n_par", "logLik", "BIC"]]
verd["dBIC_vs_spec_best"] = verd.groupby("spec").BIC.transform(lambda s: s - s.min()); sheets["structure_verdict_BIC"] = verd.round(1)
with pd.ExcelWriter(os.path.join(res, "DIMENSIONALITY_TABLES.xlsx")) as w:
    for k_, v in sheets.items(): v.to_excel(w, sheet_name=k_[:31], index=False)
# figure: loadings spec C 2f + eigen scree + gate patterns
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
e = sheets["EFA_C_eigen"]; ax[0].plot(e.factor, e.eigenvalue, "o-", color="#0072B2"); ax[0].axhline(1, color="#999", ls=":"); ax[0].set_xlabel("Factor"); ax[0].set_ylabel("Eigenvalue (polychoric, spec C)"); ax[0].set_title("Scree", loc="left", fontsize=9)
l2 = sheets["EFA_C_2f_loadings"].set_index("index"); 
ax[1].scatter(l2.F1, l2.F2, color="#D55E00")
for it, r_ in l2.iterrows(): ax[1].annotate(it, (r_.F1, r_.F2), fontsize=8, xytext=(3, 3), textcoords="offset points")
ax[1].axhline(0, color="#ccc"); ax[1].axvline(0, color="#ccc"); ax[1].set_xlabel("Factor 1 (promax)"); ax[1].set_ylabel("Factor 2"); ax[1].set_title("2-factor loadings (order assumed)", loc="left", fontsize=9)
gp = sheets["gate_patterns"]; ax[2].barh(gp.pattern_r2_r4_r8, gp.observed_share, color="#0072B2", label="observed"); ax[2].plot(gp.expected_if_independent, range(len(gp)), "D", color="#E69F00", label="independence")
ax[2].set_xlabel("Share of firms"); ax[2].set_ylabel("r2 r4 r8 (1=present)"); ax[2].legend(frameon=False, fontsize=7); ax[2].set_title("Gate-practice combinations", loc="left", fontsize=9)
plt.tight_layout(); plt.savefig(os.path.join(FIG, "Fig4_dimensionality.png"), dpi=300); plt.savefig(os.path.join(FIG, "Fig4_dimensionality.pdf")); plt.close()
pd.set_option("display.width", 220)
for k_ in ["EFA_A_fit", "EFA_C_fit", "EFA_A_1f_loadings", "EFA_C_2f_loadings", "EFA_C_2f_factor_corr", "EFA_C_eigen", "EFA_A_1f_by_country", "code_order_check", "theta_reliability", "gate_patterns", "specB_pattern_summary", "structure_verdict_BIC"]:
    print(k_); print(sheets[k_].round(3).to_string())
print(catord.round(2).to_string())
log("08_dimensionality: done")
