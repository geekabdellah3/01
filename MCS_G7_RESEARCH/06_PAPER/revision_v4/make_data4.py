import os, sys, json
sys.path.insert(0, "../../02_SCRIPTS"); from common import *
from PIL import Image
base = json.load(open("../revision_v2/data2.json"))
X = os.path.join(ROOT, "08_CONTEXTUAL_FIT")
spec = pd.read_excel(os.path.join(X, "MCS_MODEL_SPECIFICATIONS.xlsx"), sheet_name=None)
fs = spec["formal_specifications"]; t_spec = [[r["model"], r["formal specification (our notation)"], r["WBES observability"]] for _, r in fs.iterrows()]
cv = spec["coverage"]; t_cov = [[r.model, int(r.n_constructs), int(r.observed), int(r.partial), int(r.not_observed), f"{r.coverage_score:.2f}"] for _, r in cv.iterrows()]
fit = pd.read_excel(os.path.join(X, "MCS_MODEL_FIT_ON_WBES.xlsx"))
short = {"U": "One factor (common sophistication)", "MB2": "Malmi & Brown-type: cybernetic {r1-r5} + reward {r8, r9}", "RES2": "Results-control-type: monitoring {r1-r3} + results {r4, r5, r8, r9}", "BLK3": "Three families: monitoring, targets, rewards", "EXP2": "Unrestricted two factors"}
t_fit = [[short[r.model.split()[0]], int(r.factors), int(r.n_par), f"{r.logLik:,.1f}", f"{r.BIC:,.1f}", f"{r.dBIC_vs_U:+.1f}", "-" if pd.isna(r.rho) else f"{r.rho:.2f}"] for _, r in fit.iterrows()]
P = pd.read_excel(os.path.join(X, "PREDICTIVE_COMPARISON_AND_TRANSFER.xlsx"), sheet_name=None)
o = P["oos_by_model"]; pr = P["paired_comparisons"]
lab = {"U0": "U0 controls only", "U1": "M1 universal (common linear slope)", "U2": "M1' universal, level-dependent shape", "C1": "M2 organisational contingency", "N1": "National slopes (linear)", "N2": "National slopes + level-dependent", "X": "M2 + national slopes"}
t_pred = []
for m in ["U0", "U1", "U2", "C1", "N1", "N2", "X"]:
    r = o[(o.outcome == "Log sales per employee") & (o.model == m)].iloc[0]; g = o[(o.outcome == "Sales growth (ann.)") & (o.model == m)].iloc[0]; e = o[(o.outcome == "Employment growth (ann.)") & (o.model == m)].iloc[0]
    t_pred.append([lab[m], f"{r.rmse_oos:.4f}", f"{r.incr_R2_oos_vs_U0*100:.2f}", f"{g.rmse_oos:.4f}", f"{e.rmse_oos:.4f}"])
pp = pr[pr.outcome == "Log sales per employee"]; pl = {("U0", "U1"): "U1 vs U0", ("U1", "U2"): "U2 vs U1", ("U2", "C1"): "M2 vs M1'", ("U1", "N1"): "National slopes vs M1", ("U2", "N2"): "National + level vs M1'", ("N2", "X"): "M2 + national vs national", ("C1", "X"): "M2 + national vs M2"}
t_pair = [[pl[(r.reference, r.model)], f"{r.mean_sq_error_reduction:.4f} [{r.ci_lo:.4f}, {r.ci_hi:.4f}]", f"{r.rel_reduction_pct:.2f}"] for _, r in pp.iterrows() if (r.reference, r.model) in pl]
T = P["transfer_matrix_long"]; T = T[(T.outcome == "Log sales per employee") & (T["shape"] == "linear")]
t_tr = []
for s in CORDER:
    t_tr.append([s] + ["–" if s == t else f"{T[(T.source==s)&(T.target==t)].R2_transfer.iloc[0]:.3f}" for t in CORDER])
t_tr.append(["LOCO"] + [f"{T[(T.source.str.startswith('LOCO'))&(T.target==t)].R2_transfer.iloc[0]:.3f}" for t in CORDER])
t_tr.append(["Local (CV)"] + [f"{T[T.target==t].R2_local_cv.iloc[0]:.3f}" for t in CORDER])
figs = base["figs"]
for k, fn in {"cov": "Fig_MCS_models_WBES_coverage.png"}.items():
    p = os.path.abspath(os.path.join(FIG, fn)); w_, h_ = Image.open(p).size; figs[k] = dict(path=p, w=w_, h=h_)
base.update(t_spec=t_spec, t_cov=t_cov, t_fit=t_fit, t_pred=t_pred, t_pair=t_pair, t_tr=t_tr, figs=figs)
json.dump(base, open("data4.json", "w"), indent=1); print(t_pred, t_pair, t_tr[-2:])
