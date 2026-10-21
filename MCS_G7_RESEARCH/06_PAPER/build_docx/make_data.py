import os, sys, json
sys.path.insert(0, "02_SCRIPTS"); from common import *
from PIL import Image
sel = pd.read_excel(os.path.join(RES, "lca/LCA_MODEL_SELECTION.xlsx"), sheet_name="fit_by_K"); a = sel[sel.spec == "A"]
t2 = [[int(r.K), int(r.n_par), f"{r.logLik:,.1f}", f"{r.BIC:,.1f}", f"{r.aBIC:,.1f}", f"{r.rel_entropy:.2f}", f"{r.min_avepp:.2f}", f"{100*r.min_class_share:.1f}"] for r in a.itertuples()]
cd = pd.read_excel(os.path.join(RES, "descriptive/EDA_TABLES.xlsx"), sheet_name="country_descriptives")
t1 = [[r.cid, int(r.n), f"{r.median_employees:.0f}", f"{100*r.share_r2_yes:.0f}", f"{100*r.share_r4_yes:.0f}", f"{100*r.share_r8_yes:.0f}", f"{r.mean_S_core:.2f}"] for r in cd.itertuples()]
v = pd.read_excel(os.path.join(RES, "dimensionality/DIMENSIONALITY_TABLES.xlsx"), sheet_name="structure_verdict_BIC")
t3 = [[r.spec, r.family, r.model, int(r.n_par), f"{r.BIC:,.1f}", f"{r.dBIC_vs_spec_best:,.1f}"] for r in v.itertuples()]
o = pd.read_excel(os.path.join(RES, "lca/LCA_OUTCOME_INCREMENTAL.xlsx"), sheet_name="coefficients")
m = pd.read_excel(os.path.join(RES, "lca/LCA_OUTCOME_INCREMENTAL.xlsx"), sheet_name="models")
names = {"ln_lp": "Log sales per employee", "sales_growth3y_ann": "Annualised sales growth (3y)", "emp_growth3y_ann": "Annualised employment growth (3y)"}
t4 = []
for y, nm in names.items():
    th = o[(o.outcome == y) & (o.model == "M2")].iloc[0]; cs = o[(o.outcome == y) & (o.model == "M1")].iloc[0]
    pcl = m[(m.outcome == y) & (m.model.str.startswith("pseudo-class draws A3"))].iloc[0]
    cv = m[(m.outcome == y) & (m.model == "M0 controls")].cv_rmse.iloc[0]; cvt = m[(m.outcome == y) & (m.model.str.startswith("M2"))].cv_rmse.iloc[0]; cvc = m[(m.outcome == y) & (m.model.str.startswith("M3a"))].cv_rmse.iloc[0]
    t4.append([nm, f"{th.coef:.4f} ({th.se_rubin:.4f})", f"{cs.coef:.4f} ({cs.se_rubin:.4f})", f"{pcl.p:.2f}", f"{cv:.4f} / {cvt:.4f} / {cvc:.4f}"])
figs = {}
for k, f in {"model": "MANAGEMENT_CONTROL_MODEL.png", "heat": "Fig_LCA_A3_heatmap.png", "dim": "Fig4_dimensionality.png", "nl": "Fig5_nonlinear_theta.png"}.items():
    p = os.path.join(FIG, f); w, h = Image.open(p).size; figs[k] = dict(path=os.path.abspath(p), w=w, h=h)
json.dump(dict(t1=t1, t2=t2, t3=t3, t4=t4, figs=figs), open("06_PAPER/build_docx/data.json", "w"), indent=1)
print(t1, t2[:2], t3[:2], t4)
