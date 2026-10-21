"""Cross-check of the in-house EM against the independent StepMix implementation (complete cases, spec A)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
from lca_core import *
from stepmix.stepmix import StepMix
d = load_analytic(); X = d[[f"A_{c}" for c in ["r1","r2","r4","r8","r10","r11"]]].dropna().astype(int).values; nc = [int(X[:, j].max()) + 1 for j in range(6)]
rows = []
for K in (2, 3, 4):
    mine = fit_lca(X, nc, K, n_starts=40, n_full=5, seed=SEED)
    sm = StepMix(n_components=K, measurement="categorical", n_init=20, random_state=SEED, max_iter=2000, abs_tol=1e-9, verbose=0).fit(X)
    ll_sm = sm.score(X) * len(X)
    rows.append(dict(K=K, N=len(X), ll_inhouse=mine["ll"], ll_stepmix=float(ll_sm), abs_diff=abs(mine["ll"] - ll_sm)))
r = pd.DataFrame(rows); print(r)
r.to_csv(os.path.join(RES, "robustness/crosscheck_stepmix.csv"), index=False); log("12_crosscheck: " + r.round(3).to_json(orient="records"))
