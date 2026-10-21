"""STEP 4: Phase I exploratory data analysis (categorical/ordinal-appropriate methods)."""
import os, sys, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../dimensionality"))
from common import *
from poly import *
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency, kendalltau
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})
OI = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00", "#F0E442", "#999999"]
log("03_eda: start")
d = load_analytic()
out = os.path.join(RES, "descriptive")

# ---- 1-3. distributions, missingness ------------------------------------------------
rows = []
for v in R:
    s = d[v]
    for scope, sub in [("ALL", d)] + [(c, d[d.cid == c]) for c in CORDER]:
        x = sub[v]; asked = x.notna().sum(); sub_ = x[x > 0]
        for k in sorted(sub_.unique()):
            rows.append(dict(variable=v, scope=scope, category=int(k), n=int((sub_ == k).sum()), pct_of_substantive=round(100 * (sub_ == k).mean(), 2)))
        rows.append(dict(variable=v, scope=scope, category="DK(-9)", n=int((x == -9).sum()), pct_of_substantive=np.nan))
        rows.append(dict(variable=v, scope=scope, category="NA(-7)", n=int((x == -7).sum()), pct_of_substantive=np.nan))
        rows.append(dict(variable=v, scope=scope, category="blank(not asked)", n=int(x.isna().sum()), pct_of_substantive=np.nan))
freq = pd.DataFrame(rows)
fig, axs = plt.subplots(3, 4, figsize=(13, 8.5)); axs = axs.ravel()
for i, v in enumerate(R):
    ax = axs[i]; sub = d[d[v] > 0]
    t = pd.crosstab(sub.cid, sub[v], normalize="index").reindex(CORDER) * 100
    bot = np.zeros(len(t))
    for j, c in enumerate(t.columns):
        ax.bar(range(len(t)), t[c].values, bottom=bot, color=OI[j % 8], label=f"{int(c)}", width=0.75); bot += t[c].values
    ax.set_xticks(range(len(t))); ax.set_xticklabels(CORDER, rotation=60, fontsize=7); ax.set_title(v, fontsize=10, loc="left", fontweight="bold")
    ax.legend(fontsize=6, ncol=3, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.22), handlelength=1)
    ax.set_ylim(0, 100)
    if i % 4 == 0: ax.set_ylabel("% of substantive responses")
axs[11].axis("off"); axs[11].text(0, 0.5, "Response codes are raw WBES codes.\nCategory order/labels not verified\nfor r6,r7,r10,r11 (see VARIABLE_AUDIT).\nUniverse: module-asked firms.", fontsize=8, va="center")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "Fig1_response_distributions.png"), dpi=300); plt.savefig(os.path.join(FIG, "Fig1_response_distributions.pdf")); plt.close()

mm = []
for v in R:
    for c in CORDER:
        x = d[d.cid == c][v]; n = len(x)
        mm.append(dict(variable=v, country=c, blank=100 * x.isna().mean(), dk=100 * (x == -9).mean(), na7=100 * (x == -7).mean()))
mm = pd.DataFrame(mm)
fig, axs = plt.subplots(1, 3, figsize=(12, 4.2), sharey=True)
for ax, (col, ttl) in zip(axs, [("blank", "Not asked (skip pattern)"), ("dk", "Don't know (-9)"), ("na7", "Does-not-apply (-7)")]):
    M = mm.pivot(index="variable", columns="country", values=col).reindex(R)[CORDER]
    im = ax.imshow(M.values, cmap="cividis_r", aspect="auto", vmin=0, vmax=max(5, M.values.max()))
    ax.set_xticks(range(7)); ax.set_xticklabels(CORDER, rotation=60); ax.set_yticks(range(11)); ax.set_yticklabels(R); ax.set_title(ttl, fontsize=10)
    for (i, j), val in np.ndenumerate(M.values): ax.text(j, i, f"{val:.0f}" if val >= 1 else ("<1" if val > 0 else ""), ha="center", va="center", fontsize=6.5, color="w" if val > M.values.max() * .55 else "k")
    plt.colorbar(im, ax=ax, fraction=0.046, label="% of module-universe firms")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "Fig2_missingness_heatmap.png"), dpi=300); plt.savefig(os.path.join(FIG, "Fig2_missingness_heatmap.pdf")); plt.close()

# ---- 4-5. pairwise associations ---------------------------------------------------
def cramers_v_bc(x, y):
    m = (x > 0) & (y > 0)
    if m.sum() < 30: return np.nan, 0
    t = pd.crosstab(x[m], y[m]); 
    if min(t.shape) < 2: return np.nan, int(m.sum())
    chi = chi2_contingency(t, correction=False)[0]; n = t.values.sum(); r, k = t.shape
    phi2 = max(0, chi / n - (k - 1) * (r - 1) / (n - 1)); rc = r - (r - 1) ** 2 / (n - 1); kc = k - (k - 1) ** 2 / (n - 1)
    return float(np.sqrt(phi2 / max(1e-9, min(kc - 1, rc - 1)))), int(m.sum())
def pair_tables(sub):
    V = np.full((11, 11), np.nan); T = np.full((11, 11), np.nan); N_ = np.zeros((11, 11), int)
    for i, a in enumerate(R):
        for j, b in enumerate(R):
            if i == j: V[i, j] = 1; continue
            V[i, j], N_[i, j] = cramers_v_bc(sub[a], sub[b])
            m = (sub[a] > 0) & (sub[b] > 0)
            if m.sum() > 30 and sub.loc[m, a].nunique() > 1 and sub.loc[m, b].nunique() > 1: T[i, j] = kendalltau(sub.loc[m, a], sub.loc[m, b])[0]
    return V, T, N_
V, T, N_ = pair_tables(d)
Vc = {c: pair_tables(d[d.cid == c])[0] for c in CORDER}
iu = np.triu_indices(11, 1)
cons = pd.DataFrame([[np.corrcoef(np.nan_to_num(Vc[a][iu]), np.nan_to_num(Vc[b][iu]))[0, 1] for b in CORDER] for a in CORDER], index=CORDER, columns=CORDER)
# ordinal-assumption polychoric on binary/ordinal-credible subset (documented assumption)
Xc = d[[f"C_{v}" for v in R]].fillna(-1).astype(int).values; ncC = [int(Xc[:, j].max()) + 1 for j in range(11)]
Rp = polychoric_matrix(Xc, ncC)
fig, axs = plt.subplots(1, 2, figsize=(12, 5))
for ax, M, ttl, cm, vm in [(axs[0], V, "Cramér's V (bias-corrected; nominal)", "cividis", (0, 1)), (axs[1], Rp, "Polychoric r (assumes code order = ordinal order)", "RdBu_r", (-1, 1))]:
    im = ax.imshow(M, cmap=cm, vmin=vm[0], vmax=vm[1]); ax.set_xticks(range(11)); ax.set_xticklabels(R, rotation=60); ax.set_yticks(range(11)); ax.set_yticklabels(R); ax.set_title(ttl, fontsize=10)
    for (i, j), val in np.ndenumerate(M):
        if i != j and not np.isnan(val): ax.text(j, i, f"{val:.2f}".replace("0.", "."), ha="center", va="center", fontsize=6, color="w" if (cm == "cividis" and val < .5) or (cm == "RdBu_r" and abs(val) > .6) else "k")
    plt.colorbar(im, ax=ax, fraction=0.046)
plt.tight_layout(); plt.savefig(os.path.join(FIG, "Fig3_pairwise_associations.png"), dpi=300); plt.savefig(os.path.join(FIG, "Fig3_pairwise_associations.pdf")); plt.close()
red = [dict(a=R[i], b=R[j], cramers_v=V[i, j], n_pairs=N_[i, j], flag=("structural: both conditional on same gate" if (R[i] in ("r5", "r6", "r7") and R[j] in ("r5", "r6", "r7")) else "")) for i, j in zip(*iu) if not np.isnan(V[i, j])]
red = pd.DataFrame(red).sort_values("cramers_v", ascending=False)

# ---- 6. country-level descriptives --------------------------------------------------
cdesc = d.groupby("cid").agg(n=("cid", "size"), median_employees=("employees", "median"), p_size20_99=("size_class_a6a", lambda s: (s == 2).mean()),
    share_r2_yes=("r2", lambda s: (s == 1).sum() / (s > 0).sum()), share_r4_yes=("r4", lambda s: (s == 1).sum() / (s > 0).sum()),
    share_r8_yes=("r8", lambda s: (s == 1).sum() / (s > 0).sum()), mean_S_core=("S_core", "mean"), sd_S_core=("S_core", "std")).reindex(CORDER).round(3)
for v in ["r2", "r4", "r8"]:
    cdesc[f"{v}_yes_wmedian"] = [np.average(d[(d.cid == c) & (d[v] > 0)][v] == 1, weights=d[(d.cid == c) & (d[v] > 0)].wmedian) for c in CORDER]
cdesc = cdesc.round(3)
# controlling for size and sector composition: ordinal logit of S_core on country (+ ln_emp, sector)
import statsmodels.formula.api as smf
dd = d.dropna(subset=["S_core", "ln_emp"]).copy()
m0 = smf.ols("S_core ~ C(cid, Treatment('USA'))", data=dd).fit(cov_type="HC3")
m1 = smf.ols("S_core ~ C(cid, Treatment('USA')) + ln_emp + ln_age", data=dd).fit(cov_type="HC3")
m2 = smf.ols("S_core ~ C(cid, Treatment('USA')) + ln_emp + ln_age + C(sector_c)", data=dd).fit(cov_type="HC3")
mt = pd.DataFrame({"raw_diff_vs_USA": m0.params, "adj_size_age": m1.params}).loc[lambda x: x.index.str.startswith("C(cid")].round(3)
# NB: sector codes are country-specific, so country contrasts cannot be sector-adjusted; sector FE only shown via R2 (country effect absorbed).
mt["R2_country_only"], mt["R2_country_size_age"], mt["R2_with_country_sector_FE"] = m0.rsquared, m1.rsquared, m2.rsquared
sizeS = dd.groupby(pd.cut(dd.employees, [19, 49, 99, 249, 1e9], labels=["<50", "50-99", "100-249", "250+"]), observed=True).S_core.agg(["mean", "size"]).round(3)

# ---- 7-8. dimensionality exploration (nominal MCA; polychoric parallel analysis) -----
XA = d[[f"A_{v}" for v in ["r1", "r2", "r4", "r8", "r10", "r11"]]]
cc = XA.dropna()
Zi = pd.get_dummies(cc.astype(int).astype(str), dtype=float); P = Zi.values / Zi.values.sum()
r_, c_ = P.sum(1), P.sum(0); S_ = (P - np.outer(r_, c_)) / np.sqrt(np.outer(r_, c_))
sv = np.linalg.svd(S_, compute_uv=False); Q_ = XA.shape[1]; inertia = sv ** 2; total = inertia.sum()
mca = pd.DataFrame({"dim": np.arange(1, len(sv) + 1), "inertia": inertia, "pct": 100 * inertia / total, "cum_pct": 100 * np.cumsum(inertia) / total}).head(8)
# Benzecri-adjusted
lam = inertia[inertia > 1 / Q_]; adj = ((Q_ / (Q_ - 1)) * (lam - 1 / Q_)) ** 2; mca_adj = pd.DataFrame({"dim": np.arange(1, len(adj) + 1), "benzecri_adj_pct": 100 * adj / adj.sum()}).head(6)
XAo = XA.fillna(-1).astype(int).values; ncA = [int(XAo[:, j].max()) + 1 for j in range(6)]
ev, pa = parallel_analysis(XAo, ncA, n_iter=30)
pa_t = pd.DataFrame({"factor": np.arange(1, 7), "eigenvalue_polychoric": ev, "parallel_95pct": pa, "retain": ev > pa})
with pd.ExcelWriter(os.path.join(out, "EDA_TABLES.xlsx")) as w:
    freq.to_excel(w, sheet_name="frequencies", index=False)
    mm.to_excel(w, sheet_name="missing_by_var_country", index=False)
    pd.DataFrame(V, index=R, columns=R).round(3).to_excel(w, sheet_name="cramers_V")
    pd.DataFrame(T, index=R, columns=R).round(3).to_excel(w, sheet_name="kendall_tau_b")
    pd.DataFrame(Rp, index=R, columns=R).round(3).to_excel(w, sheet_name="polychoric_specC_order")
    pd.DataFrame(N_, index=R, columns=R).to_excel(w, sheet_name="n_pairs")
    cons.round(3).to_excel(w, sheet_name="V_matrix_country_agreement")
    red.round(3).to_excel(w, sheet_name="redundancy_ranked", index=False)
    cdesc.to_excel(w, sheet_name="country_descriptives")
    mt.to_excel(w, sheet_name="country_diff_Score_OLS")
    sizeS.to_excel(w, sheet_name="Score_by_size")
    mca.round(3).to_excel(w, sheet_name="MCA_specA_inertia", index=False)
    mca_adj.round(3).to_excel(w, sheet_name="MCA_specA_benzecri", index=False)
    pa_t.round(3).to_excel(w, sheet_name="parallel_analysis_specA", index=False)
print(cdesc.to_string()); print(mt.to_string()); print(red.head(12).round(2).to_string()); print(cons.round(2).to_string()); print(mca.round(3).to_string()); print(pa_t.round(2).to_string()); print(sizeS)
log("03_eda: done")
