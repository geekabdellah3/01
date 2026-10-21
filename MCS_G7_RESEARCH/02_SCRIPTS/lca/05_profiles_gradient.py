"""STEP 6-7: class profiles, classification quality, bootstrap CIs, gradient-vs-configuration tests.
usage: 05_profiles_gradient.py SPEC K [SPEC K ...]"""
import os, sys, pickle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
from lca_core import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency, kendalltau, spearmanr
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
CC = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9", "#999999", "#F0E442"]
d = load_analytic(); store = pickle.load(open(os.path.join(RES, "lca/lca_store.pkl"), "rb"))
jobs = [(sys.argv[i], int(sys.argv[i + 1])) for i in range(1, len(sys.argv), 2)]
prof_sheets = {}; diag_sheets = {}
for tag, K in jobs:
    st = store[tag]; m = st["models"][K]; items = st["items"]; ncat = st["ncat"]; keep = st["keep"]
    dd = d[keep].reset_index(drop=True); cols = [f"{tag}_{c}" for c in items]
    X = dd[cols].fillna(-1).astype(int).values; N = len(X); post = m["post"]; theta = m["theta"]; pi = m["pi"]
    # order classes by expected core score (data-ordered, NOT a substantive label)
    sc = dd.S_core.fillna(dd.S_core.mean()).values; msc = (post * sc[:, None]).sum(0) / post.sum(0)
    order = np.argsort(msc); post = post[:, order]; theta = [t[order] for t in theta]; pi = pi[order]; msc = msc[order]
    lab = [f"C{k+1}" for k in range(K)]; modal = post.argmax(1)
    # ---- conditional response probabilities + bootstrap CI ---------------------------
    rng = np.random.default_rng(SEED + 100 * K); B = 150; boot = []
    Z0 = onehot(X, ncat)
    for b in range(B):
        idx = rng.integers(0, N, N); Zb = [z[idx] for z in Z0]
        from lca_core import _em_lca
        ll, pib, thb, _ = _em_lca(Zb, np.ones(N), [t.copy() for t in theta], pi.copy(), max_iter=300, tol=1e-7)
        perm, _ = align_classes(theta, pi, thb, pib); boot.append(([t[perm] for t in thb], pib[perm]))
    rows = []
    for j, it in enumerate(items):
        for c in range(ncat[j]):
            for k in range(K):
                vals = np.array([bt[0][j][k, c] for bt in boot])
                rows.append(dict(spec=tag, K=K, item=it, category=c, cls=lab[k], prob=theta[j][k, c], ci_lo=np.percentile(vals, 2.5), ci_hi=np.percentile(vals, 97.5)))
    prof = pd.DataFrame(rows)
    prev = pd.DataFrame({"cls": lab, "model_prevalence": pi, "pi_ci_lo": np.percentile([bt[1] for bt in boot], 2.5, 0), "pi_ci_hi": np.percentile([bt[1] for bt in boot], 97.5, 0),
                         "modal_share": [(modal == k).mean() for k in range(K)], "n_modal": [(modal == k).sum() for k in range(K)],
                         "mean_core_score_S": msc, "AvePP": [post[modal == k, k].mean() for k in range(K)]})
    bycty = pd.DataFrame(post).groupby(dd.cid.values).mean().reindex(CORDER); bycty.columns = lab
    # classification error matrix (modal vs true, Nagin)
    CE = np.array([[post[modal == a, b].mean() if (modal == a).any() else np.nan for b in range(K)] for a in range(K)])
    # ---- figures ---------------------------------------------------------------------
    ncols = sum(ncat); fig = plt.figure(figsize=(max(9, 0.42 * ncols + 3), 0.55 * K + 3.2))
    ax = fig.add_subplot(111); M = np.hstack([theta[j] for j in range(len(items))]); im = ax.imshow(M, cmap="cividis", vmin=0, vmax=1, aspect="auto")
    xt = [f"{items[j]}={c}" for j in range(len(items)) for c in range(ncat[j])]
    ax.set_xticks(range(ncols)); ax.set_xticklabels(xt, rotation=90, fontsize=7); ax.set_yticks(range(K)); ax.set_yticklabels([f"{lab[k]} ({pi[k]*100:.0f}%)" for k in range(K)])
    cum = np.cumsum([0] + ncat)
    for c0 in cum[1:-1]: ax.axvline(c0 - .5, color="w", lw=2)
    for (i, j), v in np.ndenumerate(M): ax.text(j, i, f"{v*100:.0f}", ha="center", va="center", fontsize=6.5, color="k" if v > .6 else "w")
    plt.colorbar(im, ax=ax, fraction=0.03, label="P(response | class)"); ax.set_title(f"Spec {tag}, K={K}: conditional response probabilities (codes 0-based; categories nominal)", fontsize=10, loc="left")
    plt.tight_layout(); fn = f"Fig_LCA_{tag}{K}_heatmap"; plt.savefig(os.path.join(FIG, fn + ".png"), dpi=300); plt.savefig(os.path.join(FIG, fn + ".pdf")); plt.close()
    fig, axs = plt.subplots(1, 3, figsize=(13, 3.8))
    # profiles: P(top-coded category) for binary & P(each) lines would be cluttered -> use binary-yes lines + class share
    for k in range(K):
        axs[0].plot(range(len(items)), [theta[j][k, 1] if ncat[j] == 2 else np.nan for j in range(len(items))], "o-", color=CC[k], label=f"{lab[k]}")
    bi = [j for j in range(len(items)) if ncat[j] == 2]
    axs[0].clear()
    for k in range(K): axs[0].plot(range(len(bi)), [theta[j][k, 1] for j in bi], "o-", color=CC[k], label=f"{lab[k]} ({pi[k]*100:.0f}%)")
    axs[0].set_xticks(range(len(bi))); axs[0].set_xticklabels([items[j] for j in bi]); axs[0].set_ylim(0, 1.02); axs[0].set_ylabel("P(practice present | class)"); axs[0].legend(frameon=False, fontsize=7); axs[0].set_title("Gate (yes/no) indicators", fontsize=9, loc="left")
    for k in range(K): axs[1].hist(post[modal == k, k], bins=np.linspace(0, 1, 26), alpha=.6, color=CC[k], label=lab[k])
    axs[1].set_xlabel("Posterior probability of assigned (modal) class"); axs[1].set_ylabel("Firms"); axs[1].set_title("Classification uncertainty", fontsize=9, loc="left"); axs[1].legend(frameon=False, fontsize=7)
    mx = post.max(1); axs[2].hist(mx, bins=30, color="#555"); axs[2].axvline(mx.mean(), color="#D55E00"); axs[2].set_xlabel("max posterior"); axs[2].set_title(f"Share with max posterior<0.7: {(mx<.7).mean()*100:.0f}%", fontsize=9, loc="left")
    plt.tight_layout(); fn = f"Fig_LCA_{tag}{K}_profiles_uncertainty"; plt.savefig(os.path.join(FIG, fn + ".png"), dpi=300); plt.savefig(os.path.join(FIG, fn + ".pdf")); plt.close()
    # ---- gradient vs configuration ---------------------------------------------------
    gd = {}
    gate_items = [j for j, it in enumerate(items) if it in ("r2", "r4", "r8")]
    if gate_items:      # directional indicators: P(yes); class order by mean S_core is already imposed -> count reversals
        P = np.array([[theta[j][k, 1] for j in gate_items] for k in range(K)])
        rev = 0; tot = 0
        for a in range(K):
            for b in range(a + 1, K):
                for jj in range(len(gate_items)):
                    tot += 1; rev += int(P[b, jj] < P[a, jj] - 0.02)   # lower class higher by >2pp -> crossing
        gd["crossings_on_directional_items"] = f"{rev}/{tot}"
        # Kendall's W across directional items (agreement of class rankings)
        ranks = np.array([pd.Series(P[:, jj]).rank().values for jj in range(P.shape[1])]); mR = ranks.sum(0)
        gd["kendall_W_gate_items"] = float(12 * ((mR - mR.mean()) ** 2).sum() / (ranks.shape[0] ** 2 * (K ** 3 - K)))
    # non-core items: distribution differences between classes AFTER conditioning on core score
    cs = dd.S_core.values; mod_s = pd.Series(modal)
    rows = []
    for j, it in enumerate(items):
        if it in ("r2", "r4", "r8"): continue
        for s in [0, 1, 2, 3]:
            msk = (cs == s) & (X[:, j] >= 0)
            if msk.sum() < 60: continue
            tt = pd.crosstab(modal[msk], X[msk, j])
            if tt.shape[0] > 1 and tt.shape[1] > 1:
                chi, p, dof, _ = chi2_contingency(tt, correction=False); Vv = np.sqrt(chi / (tt.values.sum() * (min(tt.shape) - 1)))
                rows.append(dict(item=it, S_core=s, n=int(msk.sum()), n_classes_present=tt.shape[0], chi2=chi, p=p, cramers_V=Vv))
    within = pd.DataFrame(rows)
    # class x core-score composition
    comp = pd.crosstab(modal, np.where(np.isnan(cs), -1, cs), normalize="index").round(3); comp.index = lab
    # class vs aggregate score: share of variance of core score between classes; and how well score predicts class
    gd["eta2_core_score_by_class"] = float(1 - ((cs[~np.isnan(cs)] - (post * cs[:, None]).sum(0)[modal[~np.isnan(cs)]] * 0) ** 2).sum() * 0)  # placeholder removed below
    csv_ = ~np.isnan(cs); grand = cs[csv_].mean(); between = sum(((cs[csv_ & (modal == k)].mean() - grand) ** 2) * (csv_ & (modal == k)).sum() for k in range(K) if (csv_ & (modal == k)).any())
    gd["eta2_core_score_by_class"] = float(between / ((cs[csv_] - grand) ** 2).sum())
    gd["spearman_modal_class_vs_core_score"] = float(spearmanr(modal[csv_], cs[csv_])[0])
    # ordinal ordering test: fraction of item-category probability mass ordered monotonic across classes
    mono = []
    for j, it in enumerate(items):
        for c in range(ncat[j]):
            v = theta[j][:, c]; d_ = np.diff(v); mono.append(dict(item=it, category=c, monotone_increasing=bool((d_ >= -0.02).all()), monotone_decreasing=bool((d_ <= 0.02).all())))
    mono = pd.DataFrame(mono); gd["share_cats_monotone_across_ordered_classes"] = float((mono.monotone_increasing | mono.monotone_decreasing).mean())
    gd["rel_entropy"] = m["ent"]["rel_entropy"]; gd["min_avepp"] = m["ent"]["min_avepp"]
    key = f"{tag}{K}"
    prof_sheets[f"{key}_probs"] = prof; prof_sheets[f"{key}_prevalence"] = prev; prof_sheets[f"{key}_by_country"] = bycty.round(3).reset_index()
    diag_sheets[f"{key}_gradient"] = pd.DataFrame([gd]).T.reset_index().rename(columns={"index": "metric", 0: "value"}).astype(str)
    diag_sheets[f"{key}_within_score"] = within; diag_sheets[f"{key}_class_x_score"] = comp.reset_index()
    diag_sheets[f"{key}_class_error"] = pd.DataFrame(CE, index=lab, columns=lab).round(3).reset_index(); diag_sheets[f"{key}_monotone"] = mono
    pickle.dump(dict(order=order, theta=theta, pi=pi, post=post, items=items, ncat=ncat, keep=keep, lab=lab), open(os.path.join(RES, f"lca/model_{key}.pkl"), "wb"))
    print(key, prev.round(3).to_string()); print(gd); print(within.round(3).head(12).to_string())
with pd.ExcelWriter(os.path.join(RES, "lca/LCA_CLASS_PROFILES.xlsx")) as w:
    for k, v in prof_sheets.items(): v.to_excel(w, sheet_name=k[:31], index=False)
with pd.ExcelWriter(os.path.join(RES, "lca/LCA_DIAGNOSTICS.xlsx")) as w:
    for k, v in diag_sheets.items(): v.to_excel(w, sheet_name=k[:31], index=False)
log("05_profiles_gradient: done " + str(jobs))
