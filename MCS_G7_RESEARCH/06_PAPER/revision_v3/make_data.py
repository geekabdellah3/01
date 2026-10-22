import os, sys, json
sys.path.insert(0, "../../02_SCRIPTS"); from common import *
from PIL import Image
C = pd.read_excel(os.path.join(ROOT, "08_CONTEXTUAL_FIT/CONTEXT_TABLES.xlsx"), sheet_name=None)
R_ = pd.read_excel(os.path.join(RES, "robustness/ROBUSTNESS_TABLES.xlsx"), sheet_name=None)
old = json.load(open("../build_docx/data.json"))
f = lambda x, n=3: f"{x:.{n}f}"
cs = C["country_slopes"]; cs = cs[cs.score.str.startswith("latent")]
t_sl = []
for c in CORDER:
    row = [c]
    for o in ["Log sales per employee", "Sales growth (ann.)", "Employment growth (ann.)"]:
        r = cs[(cs.country == c) & (cs.outcome == o)].iloc[0]; n = 3 if o.startswith("Log") else 4
        row.append(f"{r.beta:.{n}f} [{r.ci_lo:.{n}f}, {r.ci_hi:.{n}f}] (n={int(r.N)})")
    t_sl.append(row)
hs = C["heterogeneity_Q_I2"]; hh = hs[hs.score.str.startswith("latent")].set_index("outcome")
t_sl.append(["Random-effects pooled"] + [f"{hh.loc[o,'b_random']:.{3 if o.startswith('Log') else 4}f} (SE {hh.loc[o,'se_random']:.{3 if o.startswith('Log') else 4}f})" for o in ["Log sales per employee", "Sales growth (ann.)", "Employment growth (ann.)"]])
t_sl.append(["Q (df = 6), p; I²"] + [f"{hh.loc[o,'Q']:.1f}, p = {hh.loc[o,'p']:.3f}; I² = {hh.loc[o,'I2']:.0f}%" for o in ["Log sales per employee", "Sales growth (ann.)", "Employment growth (ann.)"]])
ts = C["pooled_slope_equality_Wald"]; ts = ts[ts.outcome.str.startswith("Log")]
t_sp = [[r.score, "yes" if r.country_specific_control_slopes else "no", r["cov"], f"{r.wald_chi2:.1f}", f"{r.p:.4f}"] for _, r in ts.iterrows()]
w = C["weighted_slopes"]; hw = hs[hs.score.str.contains("wmedian")]
t_sp.append(["EAP, weighted WLS (wmedian) - Q test", "-", "HC3", f"{hw[hw.outcome.str.startswith('Log')].iloc[0].Q:.1f}", f"{hw[hw.outcome.str.startswith('Log')].iloc[0].p:.4f}"])
mo = C["firm_moderators"]; mo = mo[mo.outcome == "Log sales per employee"]
t_mo = [[r.moderator, int(r.N), f"{r.interaction:.3f} [{r.ci_lo:.3f}, {r.ci_hi:.3f}]", f"{r.p:.3f}", f"{r.p_holm:.2f}", f"{r.interaction_given_country_slopes:.3f} (p = {r.p_given_country_slopes:.3f})"] for _, r in mo.iterrows()]
eq = C["equifinality_tests"]; eq = eq[(eq.scope == "POOLED")]
t_eq = [[r.outcome, int(r.core_score_level), r.combos, int(r.N), f"{r.wald_chi2:.1f}", f"{r.p:.3f}", f"{r.p_holm:.2f}"] for _, r in eq.iterrows()]
ep = C["equifinality_pairs"]; ep = ep[ep.outcome == "Log sales per employee"]
t_ep = [[r.core_score_level, r.contrast, f"{r['diff']:.3f} [{r.ci_lo:.3f}, {r.ci_hi:.3f}]", f"±{r.margin}", "yes" if r.equivalent_within_margin else "no"] for _, r in ep.iterrows()]
mg = R_["multigroup_invariance"]; dif = R_["item_DIF_LR"]
t_mg = [[int(r.K), r.model, int(r.n_par), f"{r.BIC:,.1f}", f"{r.dBIC_vs_best_within_K:,.1f}"] for _, r in mg.iterrows()]
t_dif = [[int(r.K), r["item"], f"{r.LR:.1f}", int(r.df), f"{r.dBIC_free_minus_inv:.1f}", r.verdict] for _, r in dif.iterrows()]
rel = pd.read_excel(os.path.join(ROOT, "08_CONTEXTUAL_FIT/country_slope_vs_distribution.xlsx"))
figs = {}
for k, fn in {"frame": "Fig_Framework_contextual_fit.png", "forest": "Fig6_country_slopes.png", "mods": "Fig7_moderators.png", "dim": "Fig4_dimensionality.png"}.items():
    p = os.path.abspath(os.path.join(FIG, fn)); w_, h_ = Image.open(p).size; figs[k] = dict(path=p, w=w_, h=h_)
json.dump(dict(t1=old["t1"], t2=old["t2"][:6], t_sl=t_sl, t_sp=t_sp, t_mo=t_mo, t_eq=t_eq, t_ep=t_ep, t_mg=t_mg, t_dif=t_dif, figs=figs), open("data2.json", "w"), indent=1)
print(t_sl); print(t_sp); print(t_mo); print(t_eq); print(t_ep)
