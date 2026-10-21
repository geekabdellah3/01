"""STEP 9: cross-country validity & robustness of the LCA solution (spec A reference)."""
import os, sys, pickle, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
from lca_core import *
from lca_core import _em_lca
d = load_analytic(); store = pickle.load(open(os.path.join(RES, "lca/lca_store.pkl"), "rb"))
ITA = ["r1", "r2", "r4", "r8", "r10", "r11"]
def mat(frame, tag="A", items=ITA):
    X = frame[[f"{tag}_{c}" for c in items]].fillna(-1).astype(int).values; k = (X >= 0).any(1); return X, k
XA, kA = mat(d); dA = d[kA].reset_index(drop=True); XA = XA[kA]; ncat = [int(XA[:, j].max()) + 1 for j in range(6)]
g = pd.Categorical(dA.cid, categories=CORDER).codes
out = {}
# ---------------- (a) multi-group invariance -----------------------------------------
rows = []; dif = []
for K in (3, 4):
    m = store["A"]["models"][K]; init = dict(theta=m["theta"], pi=m["pi"])
    full = fit_lca_mg(XA, ncat, K, g, free_items=(), init=init)                           # all items invariant
    free = fit_lca_mg(XA, ncat, K, g, free_items=tuple(range(6)), init=init)              # all items free by country (metric of country-specific LCA, labels tied to pooled start)
    N = len(XA)
    for nm, r in [("full invariance (pooled theta, country-specific prevalence)", full), ("no invariance (country-specific theta)", free)]:
        inf = information(r["ll"], r["n_par"], N); rows.append(dict(K=K, model=nm, n_par=r["n_par"], logLik=r["ll"], **inf))
    # prevalence-homogeneous baseline: same pi across countries
    pooled = store["A"]["models"][K]; inf = information(pooled["ll"], pooled["n_par"], N)
    rows.append(dict(K=K, model="pooled, no country differences in prevalence", n_par=pooled["n_par"], logLik=pooled["ll"], **inf))
    for j, it in enumerate(ITA):                                                           # item-wise DIF via LR of freeing one item
        r = fit_lca_mg(XA, ncat, K, g, free_items=(j,), init=init)
        lr = 2 * (r["ll"] - full["ll"]); ddf = (7 - 1) * K * (ncat[j] - 1)
        from scipy.stats import chi2
        dif.append(dict(K=K, item=it, LR=lr, df=ddf, p=chi2.sf(lr, ddf), dBIC_free_minus_inv=-lr + ddf * np.log(N) , verdict="non-invariant (BIC)" if (-lr + ddf * np.log(N)) < 0 else "invariant (BIC)"))
    out[f"mg_prev_K{K}"] = pd.DataFrame(full["pi"], index=CORDER, columns=[f"C{k+1}" for k in range(K)]).reset_index()
    log(f"mg K={K} done")
mg = pd.DataFrame(rows); mg["dBIC_vs_best_within_K"] = mg.groupby("K").BIC.transform(lambda s: s - s.min()); dif = pd.DataFrame(dif)
# ---------------- (b) country-specific LCA -------------------------------------------
crow = []; cprof = []
ref = store["A"]["models"][3]
for ci, c in enumerate(CORDER):
    Xc = XA[g == ci]; Nc = len(Xc); best = None
    for K in range(1, 6):
        r = fit_lca(Xc, ncat, K, n_starts=40 if K > 1 else 2, n_full=5, seed=SEED + K); inf = information(r["ll"], r["n_par"], Nc); es = entropy_stats(r["post"])
        crow.append(dict(country=c, N=Nc, K=K, logLik=r["ll"], BIC=inf["BIC"], aBIC=inf["aBIC"], AIC=inf["AIC"], rel_entropy=es["rel_entropy"], min_class_share=float(r["pi"].min()), reach_best=r["n_reaching_best"]))
        if K == 3:
            perm, dist = align_classes(ref["theta"], ref["pi"], r["theta"], r["pi"]); cprof.append(dict(country=c, K=3, mean_abs_diff_to_pooled_profile=dist / 2, prevalence_matched=str(np.round(r["pi"][perm], 3).tolist())))
cs = pd.DataFrame(crow); cs["best_BIC_K"] = cs.groupby("country").BIC.transform(lambda s: cs.loc[s.idxmin(), "K"]); cp = pd.DataFrame(cprof)
log("country-specific done")
# ---------------- (c) sensitivity of pooled solution ---------------------------------
def dist_to_ref(X, nc, K, w=None, seed=1, n_starts=40):
    r = fit_lca(X, nc, K, w=w, n_starts=n_starts, n_full=5, seed=seed); perm, dd_ = align_classes(ref["theta"] if K == 3 else store["A"]["models"][4]["theta"], ref["pi"] if K == 3 else store["A"]["models"][4]["pi"], r["theta"], r["pi"]) if all(a == b for a, b in zip(nc, ncat)) else (None, np.nan)
    inf = information(r["ll"], r["n_par"], len(X)); es = entropy_stats(r["post"]); return r, inf, es, dd_
srows = []
def add(name, X, nc, K, w=None, seed=1):
    r, inf, es, dd_ = dist_to_ref(X, nc, K, w=w, seed=seed)
    srows.append(dict(scenario=name, K=K, N=len(X), logLik=r["ll"], BIC=inf["BIC"], rel_entropy=es["rel_entropy"], min_class_share=float(r["pi"].min()), profile_dist_to_pooled=dd_, reach_best=f'{r["n_reaching_best"]}/{r["n_full"]}'))
    return r
for K in (3, 4):
    add("baseline (seed 1)", XA, ncat, K)
    for sd in (2, 3, 4, 5): add(f"different random seed {sd}", XA, ncat, K, seed=sd * 7919)
    add("wmedian weights (normalised)", XA, ncat, K, w=dA.wmedian.values / dA.wmedian.mean())
    add("wstrict weights (normalised)", XA, ncat, K, w=dA.wstrict.values / dA.wstrict.mean())
    cc = (XA >= 0).all(1); add("complete cases only (no FIML)", XA[cc], ncat, K)
    sz = (dA.employees >= 50).values; add("firms with >=50 employees", XA[sz], ncat, K)
    sz2 = (dA.employees < 50).values; add("firms with <50 employees", XA[sz2], ncat, K)
    for c in CORDER:
        msk = (dA.cid != c).values; add(f"leave out {c}", XA[msk], ncat, K)
    rng = np.random.default_rng(SEED); idx = rng.permutation(len(XA)); h1, h2 = idx[: len(idx) // 2], idx[len(idx) // 2:]
    add("split-half 1", XA[h1], ncat, K); add("split-half 2", XA[h2], ncat, K)
    # drop one item at a time -> profile stability on remaining items (distance not comparable) report BIC-selected K shape only
sens = pd.DataFrame(srows)
# spec D (-7 kept) is in model selection; leave-one-item-out K selection
lrows = []
for drop in ITA:
    items = [i for i in ITA if i != drop]; X_, k_ = mat(d, "A", items); X_ = X_[k_]; nc = [int(X_[:, j].max()) + 1 for j in range(5)]
    for K in range(1, 6):
        r = fit_lca(X_, nc, K, n_starts=30 if K > 1 else 2, n_full=4, seed=SEED + K); inf = information(r["ll"], r["n_par"], len(X_)); es = entropy_stats(r["post"])
        lrows.append(dict(dropped=drop, K=K, N=len(X_), BIC=inf["BIC"], rel_entropy=es["rel_entropy"], min_class_share=float(r["pi"].min())))
loi = pd.DataFrame(lrows); loi["bestK_by_BIC"] = loi.groupby("dropped").BIC.transform(lambda s: loi.loc[s.idxmin(), "K"])
log("sensitivity done")
with pd.ExcelWriter(os.path.join(RES, "robustness/ROBUSTNESS_TABLES.xlsx")) as w:
    mg.to_excel(w, sheet_name="multigroup_invariance", index=False); dif.to_excel(w, sheet_name="item_DIF_LR", index=False)
    for k, v in out.items(): v.to_excel(w, sheet_name=k, index=False)
    cs.to_excel(w, sheet_name="country_specific_LCA", index=False); cp.to_excel(w, sheet_name="country_profile_vs_pooled", index=False)
    sens.to_excel(w, sheet_name="pooled_sensitivity", index=False); loi.to_excel(w, sheet_name="leave_one_item_out", index=False)
pd.set_option("display.width", 220)
print(mg.round(1).to_string()); print(dif.round(3).to_string()); print(cs.pivot(index="country", columns="K", values="BIC").round(0).to_string()); print(cs.groupby("country").best_BIC_K.first())
print(cp.to_string()); print(sens.round(3).to_string()); print(loi.groupby("dropped").bestK_by_BIC.first())
log("07_robustness: done")
