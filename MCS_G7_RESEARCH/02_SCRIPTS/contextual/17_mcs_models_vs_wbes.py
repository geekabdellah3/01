"""Confirmatory comparison of theory-implied groupings of WBES items (nominal-response models; same likelihood scale)."""
import os, sys, time, warnings
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
from lca_core import *
warnings.filterwarnings("ignore")
d = load_analytic(); items = ["r1", "r2", "r3", "r4", "r5", "r8", "r9"]
X = d[[f"C_{c}" for c in items]].fillna(-1).astype(int).values; keep = (X >= 0).any(1); X = X[keep]; nc = [int(X[:, j].max()) + 1 for j in range(len(items))]; N = len(X)
ix = {c: i for i, c in enumerate(items)}
def A(groups):                       # groups: list of item lists -> assign per item
    a = [None] * len(items)
    for dim, g in enumerate(groups):
        for c in g: a[ix[c]] = [dim]
    return a
models = {
 "U  one factor (Bloom/WMS-type sophistication; Ouchi 'output control' as a single family)": (A([items]), 1),
 "MB2  cybernetic {r1,r2,r3,r4,r5} + reward {r8,r9}  (Malmi & Brown: cybernetic vs reward)": (A([["r1", "r2", "r3", "r4", "r5"], ["r8", "r9"]]), 2),
 "RES2  monitoring {r1,r2,r3} + results controls {r4,r5,r8,r9}  (Merchant & Van der Stede-type results controls)": (A([["r1", "r2", "r3"], ["r4", "r5", "r8", "r9"]]), 2),
 "BLK3  monitoring {r1,r2,r3} + targets {r4,r5} + rewards {r8,r9}  (Otley/Ferreira-Otley areas; also questionnaire blocks)": (A([["r1", "r2", "r3"], ["r4", "r5"], ["r8", "r9"]]), 3),
 "EXP2  unrestricted two factors (all items on both)": ([[0, 1]] * len(items), 2)}
rows = []
for nm, (a, D) in models.items():
    t = time.time(); r = fit_cfa(X, nc, a, D, rho_grid=(0.5, 0.7, 0.85, 0.95)); inf = information(r["ll"], r["n_par"], N)
    rows.append(dict(model=nm, factors=D, N=N, n_par=r["n_par"], logLik=r["ll"], AIC=inf["AIC"], BIC=inf["BIC"], rho=r["rho"] if D > 1 else np.nan)); print(rows[-1], round(time.time() - t), flush=True)
res = pd.DataFrame(rows); res["dBIC_vs_best"] = res.BIC - res.BIC.min(); res["dBIC_vs_U"] = res.BIC - res.loc[0, "BIC"]
res.to_excel(os.path.join(ROOT, "08_CONTEXTUAL_FIT/MCS_MODEL_FIT_ON_WBES.xlsx"), index=False); print(res.round(1).to_string()); log("17_mcs_models: done")
