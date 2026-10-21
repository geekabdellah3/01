import os, sys, pickle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.stats import spearmanr
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
X = pd.read_excel(os.path.join(ROOT, "08_CONTEXTUAL_FIT/CONTEXT_TABLES.xlsx"), sheet_name=None)
cs, hs, mo = X["country_slopes"], X["heterogeneity_Q_I2"], X["firm_moderators"]
# descriptive: country slope vs country mean/SD of the latent trait (n=7; descriptive only)
d = load_analytic(); store = pickle.load(open(os.path.join(RES, "lca/lca_store.pkl"), "rb")); dd = d[store["A"]["keep"]].reset_index(drop=True)
nr = store["A"]["models"]["nrm1_1"]; th = nr["post"] @ nr["Xs"][:, 1]; th = th if np.corrcoef(th, dd.S_core.fillna(dd.S_core.mean()))[0, 1] > 0 else -th; dd["th"] = th
g = dd.groupby("cid").th.agg(["mean", "std"]).reindex(CORDER)
sl = cs[(cs.score.str.startswith("latent")) & (cs.outcome.str.startswith("Log"))].set_index("country").beta.reindex(CORDER)
rs = [spearmanr(g["mean"], sl), spearmanr(g["std"], sl)]
desc = pd.DataFrame({"country": CORDER, "mean_theta_EAP": g["mean"].values, "sd_theta_EAP": g["std"].values, "slope_lnLP_calibrated": sl.values})
desc.to_excel(os.path.join(ROOT, "08_CONTEXTUAL_FIT/country_slope_vs_distribution.xlsx"), index=False)
print(desc.round(3), "spearman mean:", rs[0], "spearman sd:", rs[1])
fig, axs = plt.subplots(1, 3, figsize=(13, 4.3), sharey=True)
for ax, o in zip(axs, ["Log sales per employee", "Sales growth (ann.)", "Employment growth (ann.)"]):
    s = cs[(cs.outcome == o) & cs.score.str.startswith("latent")].set_index("country").reindex(CORDER); h = hs[(hs.outcome == o) & hs.score.str.startswith("latent")].iloc[0]
    y = np.arange(len(CORDER))[::-1] + 1.5
    ax.errorbar(s.beta, y, xerr=[s.beta - s.ci_lo, s.ci_hi - s.beta], fmt="o", color="#0072B2", capsize=2, ms=5)
    ax.plot([h.b_random - 1.96 * h.se_random, h.b_random + 1.96 * h.se_random], [0.3, 0.3], color="#D55E00", lw=3); ax.plot(h.b_random, 0.3, "D", color="#D55E00", ms=7)
    ax.plot([h.pred_lo, h.pred_hi], [-.2, -.2], color="#999", lw=2)
    ax.axvline(0, color="#ccc", lw=.8); ax.set_yticks(list(y) + [0.3, -.2]); ax.set_yticklabels([f"{c} (n={int(n)})" for c, n in zip(CORDER, s.N)] + ["Random-effects pooled", "95% prediction interval"], fontsize=8)
    ax.set_title(f"{o}\nQ={h.Q:.1f}, df=6, p={h.p:.2f}; I²={h.I2:.0f}%", fontsize=9, loc="left"); ax.set_xlabel("Slope per latent SD (95% CI)")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "Fig6_country_slopes.png"), dpi=300); plt.savefig(os.path.join(FIG, "Fig6_country_slopes.pdf")); plt.close()
fig, ax = plt.subplots(figsize=(8, 4.2)); m = mo[mo.outcome == "Log sales per employee"]; y = np.arange(len(m))[::-1]
ax.errorbar(m.interaction, y, xerr=[m.interaction - m.ci_lo, m.ci_hi - m.interaction], fmt="o", color="#0072B2", capsize=2); ax.axvline(0, color="#ccc")
ax.set_yticks(y); ax.set_yticklabels([f"{a} (Holm p={p:.2f})" for a, p in zip(m.moderator, m.p_holm)], fontsize=8); ax.set_xlabel("Interaction with EAP score, log sales per employee (95% CI)")
ax.set_title("Firm-level moderators of the score-productivity association", fontsize=9, loc="left"); plt.tight_layout()
plt.savefig(os.path.join(FIG, "Fig7_moderators.png"), dpi=300); plt.savefig(os.path.join(FIG, "Fig7_moderators.pdf")); plt.close(); log("14_context_figures: done")
