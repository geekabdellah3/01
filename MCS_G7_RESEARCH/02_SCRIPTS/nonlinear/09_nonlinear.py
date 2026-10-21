"""STEP 10: nonlinearity and interaction checks (associational; no causal claim)."""
import os, sys, pickle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
import statsmodels.formula.api as smf, statsmodels.api as sm
from scipy import stats
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
d = load_analytic(); store = pickle.load(open(os.path.join(RES, "lca/lca_store.pkl"), "rb"))
dd = d[store["A"]["keep"]].reset_index(drop=True); nr = store["A"]["models"]["nrm1_1"]; th = nr["post"] @ nr["Xs"][:, 1]
if np.corrcoef(th, dd.S_core.fillna(dd.S_core.mean()))[0, 1] < 0: th = -th
dd["theta_z"] = (th - th.mean()) / th.std()
w = lambda s: s.clip(s.quantile(.01), s.quantile(.99))
dd["sales_growth3y_ann"] = w(dd.sales_growth3y_ann); dd["emp_growth3y_ann"] = w(dd.emp_growth3y_ann)
dd["ln_lp"] = dd.groupby("cid").ln_lp.transform(lambda s: s.clip(s.quantile(.005), s.quantile(.995)))
dd["mon"] = dd.B_r3x; dd["tgt"] = dd.A_r4; dd["bon"] = dd.A_r8; dd["mon_yes"] = dd.A_r2
CTRL = "C(cid) + C(sector_c) + ln_emp + ln_age"
OUT = ["ln_lp", "sales_growth3y_ann", "emp_growth3y_ann"]
rows = []
def ft(y, sm_f, bg_f, label, data):
    a = smf.ols(f"{y} ~ {sm_f}", data).fit(); b = smf.ols(f"{y} ~ {bg_f}", data).fit()
    d1 = b.df_model - a.df_model; F = ((a.ssr - b.ssr) / d1) / (b.ssr / b.df_resid)
    rows.append(dict(outcome=y, test=label, n=int(b.nobs), df_num=d1, F=F, p=stats.f.sf(F, d1, b.df_resid), dR2=b.rsquared - a.rsquared))
for y in OUT:
    # Q5 spline vs linear in theta
    D = dd.dropna(subset=[y, "theta_z", "ln_emp", "ln_age"])
    ft(y, f"theta_z + {CTRL}", f"cr(theta_z, df=5) + {CTRL}", "Q5 nonlinearity of theta (5-df natural/cubic regression spline vs linear)", D)
    ft(y, f"theta_z + {CTRL}", f"theta_z + I(theta_z**2) + {CTRL}", "Q5b quadratic term in theta", D)
    ft(y, f"theta_z + {CTRL}", f"theta_z*ln_emp + {CTRL}", "Q5c theta x firm size interaction", D)
    ft(y, f"theta_z + {CTRL}", f"theta_z*C(cid) + {CTRL}", "Q5d theta slope heterogeneity across countries", D)
    # Q1 monitoring intensity: linear vs category dummies (levels 0..3)
    D1 = dd.dropna(subset=[y, "mon", "ln_emp", "ln_age"])
    ft(y, f"mon + {CTRL}", f"C(mon) + {CTRL}", "Q1 diminishing returns in monitoring breadth (r3x categories vs linear)", D1)
    # Q2/Q3 interactions
    D2 = dd.dropna(subset=[y, "mon", "tgt", "bon", "ln_emp", "ln_age"])
    ft(y, f"C(mon) + tgt + {CTRL}", f"C(mon)*tgt + {CTRL}", "Q2 targets x monitoring breadth", D2)
    ft(y, f"C(mon) + bon + {CTRL}", f"C(mon)*bon + {CTRL}", "Q3 bonuses x monitoring breadth", D2)
    # Q4 gate-practice combinations
    D3 = dd.dropna(subset=[y, "mon_yes", "tgt", "bon", "ln_emp", "ln_age"])
    ft(y, f"mon_yes + tgt + bon + {CTRL}", f"mon_yes*tgt + mon_yes*bon + tgt*bon + {CTRL}", "Q4a pairwise interactions among monitoring/targets/bonus", D3)
    ft(y, f"mon_yes*tgt + mon_yes*bon + tgt*bon + {CTRL}", f"mon_yes*tgt*bon + {CTRL}", "Q4b three-way interaction", D3)
    ft(y, f"mon_yes + tgt + bon + {CTRL}", f"C(mon_yes*4+tgt*2+bon) + {CTRL}", "Q4c all 8 combination cells vs additive", D3)
T = pd.DataFrame(rows)
# Holm correction within family of tests
T = T.sort_values("p").reset_index(drop=True); m_ = len(T); T["p_holm"] = np.minimum(1, np.maximum.accumulate((m_ - np.arange(m_)) * T.p.values)); T["significant_holm_5pct"] = T.p_holm < .05
# partial-effect curves of theta
fig, axs = plt.subplots(1, 3, figsize=(12.5, 3.6)); grid = np.linspace(-2, 2, 41)
curves = []
for ax, y, lab in zip(axs, OUT, ["Log sales per employee", "Annualised sales growth (3y)", "Annualised employment growth (3y)"]):
    D = dd.dropna(subset=[y, "theta_z", "ln_emp", "ln_age"]); m = smf.ols(f"{y} ~ cr(theta_z, df=5) + {CTRL}", D).fit(cov_type="HC3")
    base = D.iloc[[0]].copy(); P = pd.concat([base] * len(grid), ignore_index=True); P["theta_z"] = grid; P["ln_emp"] = D.ln_emp.mean(); P["ln_age"] = D.ln_age.mean()
    pr = m.get_prediction(P).summary_frame(); y0 = pr["mean"].iloc[len(grid) // 2]
    ax.plot(grid, pr["mean"] - y0, color="#0072B2"); ax.fill_between(grid, pr["mean_ci_lower"] - y0, pr["mean_ci_upper"] - y0, alpha=.2, color="#0072B2")
    lin = smf.ols(f"{y} ~ theta_z + {CTRL}", D).fit(); ax.plot(grid, lin.params["theta_z"] * grid, "--", color="#D55E00", lw=1, label="linear")
    ax.set_xlabel("Continuous control-practice score (SD, NRM-1D EAP)"); ax.set_title(lab, fontsize=9, loc="left"); ax.axhline(0, color="#ccc", lw=.6)
    ax2 = ax.twinx(); ax2.hist(D.theta_z, bins=30, color="#999", alpha=.25); ax2.set_yticks([]); ax2.spines["right"].set_visible(False)
    for g_, v in zip(grid, pr["mean"] - y0): curves.append(dict(outcome=y, theta_z=g_, partial_effect=v))
axs[0].legend(frameon=False, fontsize=7); axs[0].set_ylabel("Partial association (relative to mean score)")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "Fig5_nonlinear_theta.png"), dpi=300); plt.savefig(os.path.join(FIG, "Fig5_nonlinear_theta.pdf")); plt.close()
# cell means of gate combinations (adjusted for controls)
cm = []
for y in OUT:
    D = dd.dropna(subset=[y, "mon_yes", "tgt", "bon", "ln_emp", "ln_age"]).copy(); D["cell"] = (D.mon_yes * 4 + D.tgt * 2 + D.bon).astype(int)
    m = smf.ols(f"{y} ~ C(cell) + {CTRL}", D).fit(cov_type="HC3")
    for c in range(8):
        n_ = int((D.cell == c).sum()); nm = f"{int(c>>2&1)}{int(c>>1&1)}{int(c&1)}"
        if c == 0: cm.append(dict(outcome=y, cell_r2_r4_r8=nm, n=n_, coef_vs_000=0.0, se=0.0))
        else: cm.append(dict(outcome=y, cell_r2_r4_r8=nm, n=n_, coef_vs_000=m.params.get(f"C(cell)[T.{c}]", np.nan), se=m.bse.get(f"C(cell)[T.{c}]", np.nan)))
cm = pd.DataFrame(cm)
with pd.ExcelWriter(os.path.join(RES, "nonlinear/NONLINEAR_TABLES.xlsx")) as w:
    T.to_excel(w, sheet_name="tests", index=False); cm.to_excel(w, sheet_name="gate_cells_adjusted", index=False); pd.DataFrame(curves).to_excel(w, sheet_name="theta_curves", index=False)
    pd.DataFrame({"limitations": ["Cross-sectional, self-reported practices; associations only (no causal interpretation).", "Co-occurrence (patterns), statistical interaction (non-additivity) and economic complementarity (Milgrom-Roberts supermodularity) are distinct; only statistical interaction is tested here.",
      "Sales/employee is in local currency; identified only within country (country FE). n3 and l2 definitions unverified.", "r3x has four levels only; 'nonlinearity' in monitoring breadth is limited to category contrasts.",
      "Outcome regressions use HC3 SEs without survey weights and without clustering; multiple tests Holm-adjusted across the family."]}).to_excel(w, sheet_name="limitations", index=False)
pd.set_option("display.width", 220); print(T.round(4).to_string()); print(cm.round(3).to_string())
log("09_nonlinear: done")
