"""Phase 7 - publication tables (1-10), figures, results workbook and the research report.

Reads results/*.csv produced by 05/06 and the analytic dataset; refits the Model-4 specifications only to obtain
predictive margins.  Outputs: outputs/05_ECONOMETRIC_RESULTS.xlsx, outputs/06_FIGURES/*.png, outputs/07_RESEARCH_REPORT.md
"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from scipy import stats
from common import *
import build as B, svy
spec = importlib.util.spec_from_file_location("reg", os.path.join(os.path.dirname(os.path.abspath(__file__)), "05_run_regressions.py"))
R5 = importlib.util.module_from_spec(spec); spec.loader.exec_module(R5)
RES = R5.RES; FIG = os.path.join(OUT, "06_FIGURES"); os.makedirs(FIG, exist_ok=True)

BLUE, ORANGE, GREY, INK, INK2, SURF = "#2a78d6", "#eb6834", "#8a8984", "#0b0b0b", "#52514e", "#fcfcfb"   # validated palette (Morocco, Korea)
plt.rcParams.update({"font.size": 9, "axes.facecolor": SURF, "figure.facecolor": SURF, "axes.edgecolor": "#c9c8c2", "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "text.color": INK, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#e8e7e2", "grid.linewidth": .6})
A = B.analytic()
main = pd.read_csv(os.path.join(RES, "main_results.csv")); m4 = pd.read_csv(os.path.join(RES, "m4_country_effects.csv"))
rob = pd.read_csv(os.path.join(RES, "robustness_results.csv"))
LAB = {"prod_innov": "Product innovation (h1)", "proc_innov": "Process innovation (h5)", "web": "Website (c22b)", "Korea": "Korea (vs Morocco)",
       "prod_innov:Korea": "Product innovation x Korea", "proc_innov:Korea": "Process innovation x Korea", "web:Korea": "Website x Korea",
       "ln_size_init": "ln employment 3y ago", "ln_size_cur": "ln employment (current)", "ln_age": "ln(1+age)", "foreign_own": "Foreign owned (>=10%)",
       "exporter": "Exporter (>=10%)", "corporation": "Corporation", "sec_Retail": "Retail (vs manufacturing)", "sec_Other services": "Other services (vs manufacturing)", "const": "Constant"}
def stars(p): return "***" if p < .01 else "**" if p < .05 else "*" if p < .10 else ""
def cell(c, s, p, d=3): return f"{c:.{d}f}{stars(p)}\n({s:.{d}f})"
MODELS = ["M1 Morocco", "M2 Korea", "M3 Pooled", "M4 Pooled x Korea"]

def reg_table(keys, full=True):
    """Stacked panels (one per outcome) with columns M1-M4."""
    frames = []
    for key in keys:
        col, est, kind, dim, labx = B.OUTCOMES[key]; d = main[main.outcome_key == key]
        terms = B.X_MAIN + ["Korea"] + [f"{v}:Korea" for v in B.X_MAIN] + ([c for c in B.controls(kind)] + ["const"] if full else [])
        dp = 3 if est == "logit" or col in ("female_share", "lowskill_prod_share") else 2
        rows = []
        for t in terms:
            r = {"Panel": labx, "Variable": LAB.get(t, t)}
            keep = False
            for m in MODELS:
                x = d[(d.model == m) & (d.term == t)]
                r[m] = cell(x.coef.iloc[0], x.se.iloc[0], x.p.iloc[0], dp) if len(x) else ""; keep |= bool(len(x))
            if keep: rows.append(r)
        if est == "logit":
            for t in B.X_MAIN:
                r = {"Panel": labx, "Variable": "AME " + LAB[t]}
                for m in MODELS:
                    x = d[(d.model == m) & (d.term == t)]
                    r[m] = f"{100*x.ame.iloc[0]:.1f}pp{stars(x.ame_p.iloc[0])}\n({100*x.ame_se.iloc[0]:.1f})" if len(x) and m != "M4 Pooled x Korea" else ""
                rows.append(r)
        for lab_, fn in [("Observations", lambda x: f"{int(x.n.iloc[0])}"), ("N treated: product / process / website", None), ("R2 / pseudo-R2", lambda x: f"{x.fit.iloc[0]:.3f}")]:
            r = {"Panel": labx, "Variable": lab_}
            for m in MODELS:
                x0 = d[d.model == m]
                if lab_.startswith("N treated"):
                    tt = [x0[x0.term == v].n_treated.iloc[0] for v in B.X_MAIN]; r[m] = " / ".join(str(int(v)) for v in tt)
                else: r[m] = fn(x0[x0.term == "const"])
            rows.append(r)
        r = {"Panel": labx, "Variable": "Wald p: all 3 x Korea = 0"}
        for m in MODELS:
            x = d[(d.model == m) & (d.term == "const")]
            r[m] = f"{x.wald_p_interactions.iloc[0]:.3f}" if m == "M4 Pooled x Korea" else ""
        rows.append(r)
        frames.append(pd.DataFrame(rows))
    return pd.concat(frames, ignore_index=True)

# ------------------------------------------------------------------ Table 1 article comparison
ext = pd.read_excel(os.path.join(OUT, "01_ARTICLE_EXTRACTION.xlsx"), sheet_name="Fields_1-18")
T1 = ext[ext.field_no.isin([1, 2, 4, 5, 6, 7, 10, 13, 14, 16, 18])].drop(columns="field_no")
# ------------------------------------------------------------------ Table 2 variable definitions
cw = pd.read_excel(os.path.join(OUT, "03_VARIABLE_CROSSWALK.xlsx"), sheet_name="Crosswalk")
T2 = cw[cw.role_in_study.str.contains("Main|Control|Robustness|D4|Design|Descriptive|Morocco")][["construct", "MAR_variable", "KOR_variable", "original_definition", "proposed_transformation", "class_cross_country", "class_vs_article", "n_valid_MAR", "n_valid_KOR", "role_in_study"]]
# ------------------------------------------------------------------ Table 3 descriptives
dv = [("g_sales", "Sales growth (pp/yr, winsorised)"), ("g_lp", "Productivity growth (pp/yr)"), ("g_emp", "Employment growth (pp/yr)"), ("female_share", "Female share of employees"),
      ("lowskill_prod_share", "Low-skilled share of production workers"), ("env_energy_mgmt", "Energy-management adoption"), ("env_co2_monitor", "CO2 monitoring"),
      ("prod_innov", "Product innovation"), ("proc_innov", "Process innovation"), ("web", "Website"), ("emp_t", "Employees (l1)"), ("age", "Age (years)"),
      ("foreign_own", "Foreign owned"), ("exporter", "Exporter"), ("corporation", "Corporation"), ("hs_share", "High-school share (l9b; descriptive)")]
rows = []
for k, l in dv:
    r = {"Variable": l}
    for c in ["MAR", "KOR"]:
        s = A.loc[A.country == c, k]; w = A.loc[A.country == c, "w_strict_std"]; m = s.notna()
        r[f"{c} N"] = int(m.sum()); r[f"{c} mean"] = round(s.mean(), 3); r[f"{c} SD"] = round(s.std(), 3); r[f"{c} weighted mean"] = round(np.average(s[m], weights=w[m]), 3)
    t = stats.ttest_ind(A.loc[(A.country == "MAR") & A[k].notna(), k], A.loc[(A.country == "KOR") & A[k].notna(), k], equal_var=False)
    r["Welch p (unweighted)"] = round(t.pvalue, 4); rows.append(r)
T3 = pd.DataFrame(rows)
# ------------------------------------------------------------------ Table 4 correlations
cv = ["g_sales", "g_emp", "g_lp", "female_share", "lowskill_prod_share", "env_energy_mgmt", "env_co2_monitor", "prod_innov", "proc_innov", "web", "ln_size_cur", "ln_age"]
T4 = {}
for c in ["MAR", "KOR"]:
    T4[c] = A[A.country == c][cv].corr(method="spearman").round(2)
# ------------------------------------------------------------------ Tables 5-8
T5 = reg_table(["D1_sales", "D1_lp"]); T6 = reg_table(["D2_emp"]); T7 = reg_table(["D3_female", "D3_lowskill"]); T8 = reg_table(["D4_energy", "D4_co2"])
# ------------------------------------------------------------------ Table 9 pooled & interactions summary
r9 = []
for key, (col, est, kind, dim, labx) in B.OUTCOMES.items():
    for v in B.X_MAIN:
        x = m4[(m4.outcome_key == key) & (m4.regressor == v)].iloc[0]
        m3 = main[(main.outcome_key == key) & (main.model == "M3 Pooled") & (main.term == v)].iloc[0]
        hol = main[(main.outcome_key == key) & (main.model == "M4 Pooled x Korea") & (main.term == f"{v}:Korea")].iloc[0]
        r9.append({"Outcome": labx, "Regressor": LAB[v], "M3 pooled": cell(m3.coef, m3.se, m3.p), "M4 effect Morocco": cell(x.effect_MAR, x.se_MAR, x.p_MAR), "M4 effect Korea": cell(x.effect_KOR, x.se_KOR, x.p_KOR),
                   "Korea - Morocco": cell(x.diff_KOR_minus_MAR, x.se_diff, x.p_diff), "p (diff)": round(x.p_diff, 3), "Holm p (M4 interaction, 21 tests)": round(hol.p_holm_interaction, 3),
                   "Wald p all 3 interactions": round(hol.wald_p_interactions, 3), "scale": "log-odds" if est == "logit" else "outcome units"})
T9 = pd.DataFrame(r9)
# ------------------------------------------------------------------ Table 10 robustness summary
bs = main[main.term.isin(B.X_MAIN) & main.model.isin(["M1 Morocco", "M2 Korea"])][["model", "outcome_key", "term", "coef", "p"]].rename(columns={"coef": "baseline", "p": "p_base"})
rb = rob[rob.term.isin(B.X_MAIN) & rob.model.isin(["M1 Morocco", "M2 Korea"]) & ~rob.check_id.isin(["R10i", "R10h", "R07a", "R07b", "R09e"])].merge(bs, on=["model", "outcome_key", "term"])
rb = rb[rb.estimator != "frac"] if False else rb
rb["same_sign"] = np.sign(rb.coef) == np.sign(rb.baseline); rb["sig10"] = rb.p < .10
g = rb.groupby(["model", "outcome_key", "term"]).agg(baseline=("baseline", "first"), p_base=("p_base", "first"), n_checks=("coef", "size"), share_same_sign=("same_sign", "mean"),
                                                    share_sig10=("sig10", "mean"), min_coef=("coef", "min"), max_coef=("coef", "max")).reset_index()
alt = {"R01": "Unweighted", "R04": "No winsorising", "R06": "Trimmed", "R08c": "Data-quality exclusions", "R09b": "Extended controls", "R11": "DK as category"}
for cid, nm in alt.items():
    x = rob[(rob.check_id == cid) & rob.term.isin(B.X_MAIN) & rob.model.isin(["M1 Morocco", "M2 Korea"])][["model", "outcome_key", "term", "coef", "p"]]
    x[nm] = x.apply(lambda r: f"{r.coef:.3f}{stars(r.p)}", axis=1); g = g.merge(x[["model", "outcome_key", "term", nm]], on=["model", "outcome_key", "term"], how="left")
g["baseline"] = g.apply(lambda r: f"{r.baseline:.3f}{stars(r.p_base)}", axis=1)
_u = rob[(rob.check_id == "R01") & rob.term.isin(B.X_MAIN)][["model", "outcome_key", "term", "p"]].rename(columns={"p": "p_unweighted"})
_sp = main[main.term.isin(B.X_MAIN)][["model", "outcome_key", "term", "sparse_cell_flag", "p_holm"]]
g = g.merge(_u, on=["model", "outcome_key", "term"], how="left").merge(_sp, on=["model", "outcome_key", "term"], how="left")
def verdict(r):
    if r.sparse_cell_flag is True or r.sparse_cell_flag == True: return "Unreliable: sparse cell (see Firth sensitivity)"
    if r.p_base < .10:
        return "Robust: significant in baseline, unweighted run and >=80% of checks, same sign throughout" if (r.p_unweighted < .10 and r.share_sig10 >= .8 and r.share_same_sign == 1) else "Fragile: significance depends on specification/weights"
    return "Null/imprecise: not significant in baseline or in >=80% of checks" if r.share_sig10 <= .2 else "Mixed"
g["Verdict"] = g.apply(verdict, axis=1)
g["outcome"] = g.outcome_key.map(lambda k: B.OUTCOMES[k][4]); g["regressor"] = g.term.map(LAB)
T10 = g[["model", "outcome", "regressor", "baseline", "n_checks", "share_same_sign", "share_sig10", "min_coef", "max_coef"] + list(alt.values()) + ["p_holm", "Verdict"]].round(3)
T10.to_csv(os.path.join(RES, "table10_robustness_summary.csv"), index=False)

# ------------------------------------------------------------------ workbook
diag = {k: pd.read_csv(os.path.join(RES, f)) for k, f in [("VIF", "vif.csv"), ("Influence", "influence.csv"), ("Missing_inclusion", "missing_inclusion.csv"), ("Missing_tests", "missing_inclusion_tests.csv"),
                                                      ("Firth_D4", "firth_d4.csv"), ("Heterogeneity_T3", "heterogeneity.csv"), ("Morocco_educ_T3", "morocco_education_exploratory.csv")]}
with pd.ExcelWriter(os.path.join(OUT, "05_ECONOMETRIC_RESULTS.xlsx"), engine="openpyxl") as xw:
    pd.DataFrame({"note": ["Tier 1 = pre-specified main models (Tables 5-9). Tier T2 = pre-specified robustness (Table 10, robustness sheets). T3 = EXPLORATORY (heterogeneity, alternative digital proxy, Morocco education).",
                           "Estimates are conditional associations from cross-sectional data; no causal interpretation. No 2SLS: no credible instrument exists in the files.",
                           "Stars use unadjusted two-sided p: * p<0.10, ** p<0.05, *** p<0.01. Holm-adjusted p-values are in Table 9 and the full results.",
                           "Standard errors: stratified Taylor-linearised (weights wstrict rescaled to mean 1 within country; strata = country_strata; no PSU). Unweighted runs use HC1-type robust SE.",
                           "Growth outcomes are annualised log changes x100 (percentage points per year), nominal local currency; shares are on a 0-1 scale (coefficient 0.05 = 5 percentage points).",
                           "Logit panels report log-odds coefficients and average marginal effects (AME, percentage points)."]}).to_excel(xw, sheet_name="README", index=False)
    for nm, t in [("Table1_Articles", T1), ("Table2_Variables", T2), ("Table3_Descriptives", T3), ("Table5_D1_Economic", T5), ("Table6_D2_Employment", T6), ("Table7_D3_Social", T7),
                  ("Table8_D4_Environment", T8), ("Table9_Pooled_Interact", T9), ("Table10_Robustness", T10)]:
        t.to_excel(xw, sheet_name=nm, index=False)
    for c, t in T4.items(): t.to_excel(xw, sheet_name=f"Table4_Corr_{c}")
    main.to_excel(xw, sheet_name="Main_full", index=False); m4.to_excel(xw, sheet_name="M4_country_effects", index=False)
    rob.to_excel(xw, sheet_name="Robustness_full", index=False)
    for k, t in diag.items(): t.to_excel(xw, sheet_name=k[:31], index=False)
    pd.read_csv(os.path.join(RES, "robustness_m4_effects.csv")).to_excel(xw, sheet_name="Robust_M4_effects", index=False)
    pd.read_csv(os.path.join(RES, "regressor_correlations.csv")).to_excel(xw, sheet_name="Regressor_corr", index=False)
for nm, t in [("T5", T5), ("T6", T6), ("T7", T7), ("T8", T8), ("T9", T9)]: t.to_csv(os.path.join(RES, f"table_{nm}.csv"), index=False)

# ================================================================== FIGURES
def save(fig, name): fig.savefig(os.path.join(FIG, name), dpi=200, bbox_inches="tight"); plt.close(fig)
# F1 conceptual framework (reflects feasibility audit)
fig, ax = plt.subplots(figsize=(10, 5.6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
def box(x, y, w, h, t, fc, ec, tc=INK, fs=8.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec=ec, lw=1.2)); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, color=tc, wrap=True)
box(0.1, 3.9, 2.6, 1.5, "EXPLANATORY VARIABLES\n(not components of inclusive growth)\nProduct innovation (h1)\nProcess innovation (h5)\nDigitalization proxy: website (c22b)", "#e8f0fb", BLUE)
box(0.1, 0.9, 2.6, 1.6, "Controls\nInitial/current size, age, foreign\nownership, exporter, legal form,\nsector (harmonised)", "#f1f0ec", GREY)
dims = [("D1 Economic growth\nsales growth; productivity growth\n[measured, class B]", 4.6, "#e5f4ec", "#1baf7a"), ("D2 Employment growth\npermanent FT employment growth\n[measured, class B]", 3.35, "#e5f4ec", "#1baf7a"),
        ("D3 Social inclusion\nfemale share; low-skilled share\n(composition at one date, class B)\ngrowth by category: NOT observed", 1.95, "#fdf3dc", "#eda100"),
        ("D4 Environmental\nenergy-mgmt adoption; CO2 monitoring\n(practices, class A) - GEP index and\noutcomes: NOT available", 0.45, "#fdf3dc", "#eda100")]
for t, y, fc, ec in dims: box(4.3, y, 3.4, 1.05 if "D3" not in t and "D4" not in t else 1.3, t, fc, ec, fs=8)
for y in [5.1, 3.9, 2.6, 1.1]: ax.annotate("", xy=(4.25, y), xytext=(2.75, 4.65), arrowprops=dict(arrowstyle="->", color=INK2, lw=1))
box(8.1, 2.3, 1.8, 1.8, "Not constructed:\ncomposite Inclusive\nGrowth Index\n(alpha = 0.29, KMO = 0.52)", "#fbe9e4", ORANGE, fs=8)
ax.text(5, 5.85, "Conceptual framework: associations of innovation and digitalization with separately measured dimensions (Strategy A)", ha="center", fontsize=10, color=INK)
ax.text(5, 0.05, "Cross-sectional associations only - no causal claim. Colour: green = measured and comparable; amber = partial/proxy.", ha="center", fontsize=8, color=INK2)
save(fig, "F1_conceptual_framework.png")
# F2 distributions
fig, axs = plt.subplots(2, 3, figsize=(11, 6))
for ax, (k, l, rng) in zip(axs.flat, [("g_sales", "Sales growth (pp/yr)", (-30, 45)), ("g_emp", "Employment growth (pp/yr)", (-12, 35)), ("g_lp", "Productivity growth (pp/yr)", (-40, 45)),
                                      ("female_share", "Female share of employees", (0, 1)), ("lowskill_prod_share", "Low-skilled share of production workers", (0, 1)), ("hs_share", "High-school share (descriptive; Korea at ceiling)", (0, 1))]):
    for c, col in [("MAR", BLUE), ("KOR", ORANGE)]:
        s = A.loc[A.country == c, k].dropna(); ax.hist(s, bins=30, range=rng, density=True, alpha=.55, color=col, label=f"{'Morocco' if c=='MAR' else 'Korea'} (n={len(s)})", edgecolor=SURF, linewidth=.6)
    ax.set_title(l, fontsize=9, loc="left"); ax.legend(frameon=False, fontsize=7.5)
fig.suptitle("Outcome distributions by country (growth outcomes winsorised 1/99 within country)", x=.01, ha="left", fontsize=10)
save(fig, "F2_outcome_distributions.png")
# F2b D4 bars
fig, ax = plt.subplots(figsize=(6, 3.3)); xs = np.arange(4); w = .38
vals = [(A.loc[A.country == c, k].mean()) for k in ["env_energy_mgmt", "env_co2_monitor", "prod_innov", "proc_innov"] for c in ["MAR", "KOR"]]
for i, (c, col) in enumerate([("MAR", BLUE), ("KOR", ORANGE)]):
    v = [A.loc[A.country == c, k].mean() for k in ["env_energy_mgmt", "env_co2_monitor", "prod_innov", "proc_innov"]]
    b = ax.bar(xs + (i - .5) * w, v, w - .03, color=col, label="Morocco" if c == "MAR" else "Korea")
    for xx, vv in zip(xs + (i - .5) * w, v): ax.text(xx, vv + .005, f"{vv:.0%}", ha="center", fontsize=8, color=INK2)
ax.set_xticks(xs); ax.set_xticklabels(["Energy-mgmt\nadoption (ge8d)", "CO2 monitoring\n(ge7)", "Product\ninnovation (h1)", "Process\ninnovation (h5)"]); ax.legend(frameon=False); ax.set_ylabel("Share of firms")
ax.set_title("Binary outcomes and innovation by country (unweighted)", loc="left", fontsize=9.5); save(fig, "F2b_binary_shares.png")
# F3 coefficient plot (M1, M2, pooled) per outcome
fig, axs = plt.subplots(2, 4, figsize=(14, 6.5)); axs = axs.flat
for ax, (key, (col, est, kind, dim, labx)) in zip(axs, B.OUTCOMES.items()):
    d = main[(main.outcome_key == key) & main.term.isin(B.X_MAIN)]
    for i, v in enumerate(B.X_MAIN[::-1]):
        for j, (m, colr, off) in enumerate([("M1 Morocco", BLUE, .18), ("M2 Korea", ORANGE, -.18)]):
            x = d[(d.model == m) & (d.term == v)].iloc[0]
            if est == "logit": est_, lo, hi = x.ame * 100, x.ame_ci_low * 100, x.ame_ci_high * 100
            else: est_, lo, hi = x.coef, x.ci_low, x.ci_high
            ax.plot([lo, hi], [i + off] * 2, color=colr, lw=1.6, solid_capstyle="round"); ax.plot(est_, i + off, "o", color=colr, ms=6, mec=SURF, mew=1.2)
    ax.axvline(0, color=INK2, lw=.8); ax.set_yticks(range(3)); ax.set_yticklabels([LAB[v].split(" (")[0] for v in B.X_MAIN[::-1]])
    ax.set_title(labx + ("\n(AME, pp)" if est == "logit" else ""), fontsize=8.5, loc="left")
axs_l = list(axs) if not isinstance(axs, list) else axs
ax8 = plt.gcf().axes[-1]; ax8.axis("off")
ax8.plot([], [], "o", color=BLUE, label="Morocco (M1)"); ax8.plot([], [], "o", color=ORANGE, label="Korea (M2)"); ax8.legend(frameon=False, loc="center", fontsize=9)
fig.suptitle("Model 1 and 2 coefficients with 95% CI (weighted, stratified SE). Associations, not causal effects.", x=.01, ha="left", fontsize=10)
fig.tight_layout(rect=[0, 0, 1, .95]); save(fig, "F3_coefficient_plot.png")
# F4 country comparison (Korea - Morocco differences)
fig, axs = plt.subplots(2, 4, figsize=(14, 6.5)); axs = list(axs.flat)
for ax, (key, (col, est, kind, dim, labx)) in zip(axs, B.OUTCOMES.items()):
    d = main[(main.outcome_key == key) & (main.model == "M4 Pooled x Korea")]
    for i, v in enumerate(B.X_MAIN[::-1]):
        x = d[d.term == f"{v}:Korea"].iloc[0]
        ax.plot([x.ci_low, x.ci_high], [i, i], color=GREY, lw=1.8); ax.plot(x.coef, i, "o", color=INK, ms=6, mec=SURF, mew=1.2)
    ax.axvline(0, color=INK2, lw=.8); ax.set_yticks(range(3)); ax.set_yticklabels([LAB[v].split(" (")[0] for v in B.X_MAIN[::-1]])
    ax.set_title(labx + ("\n(log-odds)" if est == "logit" else ""), fontsize=8.5, loc="left")
axs[-1].axis("off"); axs[-1].text(.5, .5, "Interaction coefficients (Korea minus Morocco)\n95% CI; zero = identical association\nin both countries", ha="center", va="center", fontsize=9, color=INK2)
fig.suptitle("Model 4: country differences in associations", x=.01, ha="left", fontsize=10); fig.tight_layout(rect=[0, 0, 1, .95]); save(fig, "F4_country_comparison.png")
# F5 predictive margins from Model 4 (with/without each regressor by country)
fig, axs = plt.subplots(3, 7, figsize=(17, 7.2))
for jj, (key, (col, est, kind, dim, labx)) in enumerate(B.OUTCOMES.items()):
    r, d, X, names = R5.fit(A, col, est, kind, True, True, True)
    w = d.w_strict_std.values; V = r.V
    for ii, v in enumerate(B.X_MAIN):
        ax = axs[ii, jj]
        for k, (c, colr) in enumerate([("MAR", BLUE), ("KOR", ORANGE)]):
            msk = (d.country == c).values
            for treat in (0, 1):
                Xs = X[msk].copy(); Xs[:, names.index(v)] = treat
                if f"{v}:Korea" in names: Xs[:, names.index(f"{v}:Korea")] = treat * (c == "KOR")
                eta = Xs @ r.b
                if est == "logit":
                    p = 1 / (1 + np.exp(-eta)); m_ = np.average(p, weights=w[msk]); gdt = ((p * (1 - p) * w[msk])[:, None] * Xs).sum(0) / w[msk].sum()
                else: m_ = np.average(eta, weights=w[msk]); gdt = (w[msk][:, None] * Xs).sum(0) / w[msk].sum()
                se = float(np.sqrt(gdt @ V @ gdt)); q = stats.t.ppf(.975, r.df); sc = 1 if est != "logit" else 1
                ax.plot([k + treat * .28 - .14] * 2, [m_ - q * se, m_ + q * se], color=colr, lw=1.6); ax.plot(k + treat * .28 - .14, m_, "o" if treat else "s", color=colr, ms=5.5, mec=SURF, mew=1)
        ax.set_xticks([0.0, 1.0]); ax.set_xticklabels(["Morocco", "Korea"], fontsize=7.5)
        if ii == 0: ax.set_title(labx.replace(" (", "\n("), fontsize=7.2, loc="left")
        if jj == 0: ax.set_ylabel(LAB[v].split(" (")[0], fontsize=8)
fig.suptitle("Predictive margins from Model 4: square = regressor 0, circle = regressor 1 (left/right marker within each country); 95% CI", x=.01, ha="left", fontsize=10)
fig.tight_layout(rect=[0, 0, 1, .95]); save(fig, "F5_interaction_margins.png")
# F6 weighted vs unweighted t-statistics
u = rob[(rob.check_id == "R01") & rob.term.isin(B.X_MAIN) & rob.model.isin(["M1 Morocco", "M2 Korea"])][["model", "outcome_key", "term", "t"]].rename(columns={"t": "t_unw"})
bb = main[main.term.isin(B.X_MAIN) & main.model.isin(["M1 Morocco", "M2 Korea"])][["model", "outcome_key", "term", "t"]].merge(u, on=["model", "outcome_key", "term"])
fig, ax = plt.subplots(figsize=(5.2, 5))
for m, colr in [("M1 Morocco", BLUE), ("M2 Korea", ORANGE)]:
    x = bb[bb.model == m]; ax.scatter(x.t, x.t_unw, color=colr, s=34, edgecolor=SURF, label=m.split(" ")[1])
lim = 7; ax.plot([-lim, lim], [-lim, lim], color=INK2, lw=.8); ax.axhline(0, color="#c9c8c2", lw=.6); ax.axvline(0, color="#c9c8c2", lw=.6)
ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_xlabel("t-statistic, weighted + stratified (main)"); ax.set_ylabel("t-statistic, unweighted (R01)"); ax.legend(frameon=False)
ax.set_title("Weighting sensitivity: 42 country x outcome x regressor cells", loc="left", fontsize=9); save(fig, "F6_weighting_sensitivity.png")
print("tables/figures done")
from report_text import write_report
write_report(A, main, m4, rob, T3, T9, T10, diag, RES, OUT)
