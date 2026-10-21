"""STEP 5-6: LCA model enumeration K=1..8 for specs A,B,C,D; fit indices, entropy, BVR, local maxima, parametric comparators."""
import os, sys, pickle, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
from lca_core import *
log("04_lca_select: start")
d = load_analytic()
KMAX = 8
store = {}; sel_rows = []; bvr_rows = []; comp_rows = []
def prep(tag):
    cols = [c for c in d if c.startswith(tag + "_")]
    X = d[cols].fillna(-1).astype(int).values; keep = (X >= 0).any(1)
    ncat = [int(X[keep, j].max()) + 1 for j in range(X.shape[1])]
    return [c[2:] for c in cols], X[keep], ncat, keep
for tag in ["A", "B", "C", "D"]:
    items, X, ncat, keep = prep(tag); N = len(X)
    log(f"spec {tag}: N={N} items={items} ncat={ncat}")
    store[tag] = dict(items=items, ncat=ncat, keep=keep, models={})
    for K in range(1, KMAX + 1):
        t = time.time()
        r = fit_lca(X, ncat, K, n_starts=60 if K > 1 else 2, n_full=8, seed=SEED + K)
        inf = information(r["ll"], r["n_par"], N); es = entropy_stats(r["post"])
        bv = bvr(X, ncat, r["theta"], r["pi"]); bvv = np.array([b[4] for b in bv])
        r["info"] = inf; r["ent"] = es; store[tag]["models"][K] = {k: v for k, v in r.items()}
        mn = float(np.min(r["pi"]))
        sel_rows.append(dict(spec=tag, K=K, N=N, n_par=r["n_par"], logLik=r["ll"], **inf, rel_entropy=es["rel_entropy"],
             min_avepp=es["min_avepp"], min_class_share=mn, smallest_class_n=int(round(mn * N)),
             n_starts_reaching_best=r["n_reaching_best"], n_full_runs=r["n_full"], n_distinct_ll=r["n_distinct_solutions"],
             converged=r["converged"], bvr_max=float(bvv.max()), bvr_share_gt3p84=float((bvv > 3.84).mean()), bvr_mean=float(bvv.mean())))
        for (j, l, chi, df_, ratio) in bv: bvr_rows.append(dict(spec=tag, K=K, item_j=items[j], item_l=items[l], chi2=chi, df=df_, chi2_over_df=ratio))
        log(f"  {tag} K={K} ll={r['ll']:.1f} BIC={inf['BIC']:.1f} ent={es['rel_entropy']:.3f} minpi={mn:.3f} reach_best={r['n_reaching_best']}/{r['n_full']} [{time.time()-t:.0f}s]")
    # continuous / hybrid comparators on the same likelihood
    for kind, K in [("nrm1", 1), ("nrm2", 1), ("hyb", 2), ("hyb", 3)]:
        t = time.time(); p = fit_param(X, ncat, kind, K=K, n_starts=3 if kind == "hyb" else 2)
        inf = information(p["ll"], p["n_par"], N)
        comp_rows.append(dict(spec=tag, model=f"{kind}" + (f"_K{K}" if kind == "hyb" else ""), N=N, n_par=p["n_par"], logLik=p["ll"], **inf))
        store[tag]["models"][f"{kind}_{K}"] = dict(ll=p["ll"], n_par=p["n_par"], Beta=p["Beta"], pik=p["pik"], Xs=p["Xs"], cls=p["cls"], post=p["post"], kind=kind, K=K)
        log(f"  {tag} {kind}{K} ll={p['ll']:.1f} npar={p['n_par']} BIC={inf['BIC']:.1f} [{time.time()-t:.0f}s]")
    for K in range(1, KMAX + 1):
        r = store[tag]["models"][K]
        comp_rows.append(dict(spec=tag, model=f"lca_K{K}", N=N, n_par=r["n_par"], logLik=r["ll"], **r["info"]))
sel = pd.DataFrame(sel_rows); comp = pd.DataFrame(comp_rows)
sel["dBIC_vs_min"] = sel.groupby("spec").BIC.transform(lambda s: s - s.min())
sel["dAIC_vs_min"] = sel.groupby("spec").AIC.transform(lambda s: s - s.min())
comp["dBIC_vs_min"] = comp.groupby("spec").BIC.transform(lambda s: s - s.min())
with pd.ExcelWriter(os.path.join(RES, "lca/LCA_MODEL_SELECTION.xlsx")) as w:
    sel.to_excel(w, sheet_name="fit_by_K", index=False)
    comp.to_excel(w, sheet_name="LCA_vs_continuous_vs_hybrid", index=False)
pd.DataFrame(bvr_rows).to_excel(os.path.join(RES, "lca/bvr_all.xlsx"), index=False)
pickle.dump(store, open(os.path.join(RES, "lca/lca_store.pkl"), "wb"))
print(sel[["spec","K","n_par","logLik","AIC","BIC","aBIC","rel_entropy","min_avepp","min_class_share","n_starts_reaching_best","bvr_share_gt3p84"]].round(3).to_string())
print(comp.sort_values(["spec","BIC"]).groupby("spec").head(5).round(1).to_string())
log("04_lca_select: done")
