"""Phase 5 - pre-specified main models (Tier 1).

  Model 1: Morocco only      Model 2: Korea only
  Model 3: pooled, common slopes + Korea dummy
  Model 4: pooled, Korea dummy + (product, process, website) x Korea interactions

Outcomes (Strategy A, separate models): D1 sales growth, D1 productivity growth, D2 employment growth, D3 female share,
D3 low-skilled share of production workers (OLS); D4 energy-management adoption, D4 CO2 monitoring (logit; AME reported).
Design: weights = wstrict (rescaled to mean 1 within country), stratified linearised variance (svy.py).
Associations only - no causal claim.  2SLS is NOT used: no credible instrument exists in these files.
Outputs: results/main_results.csv, results/m4_country_effects.csv, results/prespecification.json
"""
import sys, os, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from scipy import stats
from common import *
import build as B, svy

RES = os.path.join(ROOT, "results"); os.makedirs(RES, exist_ok=True)

SPEC = dict(frozen_at=datetime.datetime.now().isoformat(timespec="seconds"), tier="1 - pre-specified main models",
            regressors=B.X_MAIN, controls_growth=B.CTRL_GROWTH, controls_level=B.CTRL_LEVEL, outcomes={k: v[0] for k, v in B.OUTCOMES.items()},
            estimators={k: v[1] for k, v in B.OUTCOMES.items()}, weights="wstrict rescaled to mean 1 within country", strata="country_strata (no PSU variable)",
            winsorisation="growth outcomes winsorised at 1st/99th percentile within country", causal_claims="none", iv="not used",
            multiplicity="Holm adjustment reported across the 21 regressor x outcome tests within each model")
json.dump(SPEC, open(os.path.join(RES, "prespecification.json"), "w"), indent=2)

def design(df, kind, interact=False, pooled=False, extended=False, regs=None, ctrl=None):
    regs = regs or B.X_MAIN
    cols = list(regs) + (ctrl if ctrl is not None else B.controls(kind, extended))
    names = ["const"] + cols
    X = [np.ones(len(df))] + [df[c].values for c in cols]
    if pooled:
        names.append("Korea"); X.append(df["Korea"].values)
        if interact:
            for r in regs:
                names.append(f"{r}:Korea"); X.append(df[r].values * df["Korea"].values)
    return np.column_stack(X).astype(float), names

def fit(df, col, est, kind, pooled=False, interact=False, weighted=True, extended=False, regs=None, ctrl=None, wcol="w_strict_std", model_fn=None, strata_ignore=False):
    ctrl = list(ctrl if ctrl is not None else B.controls(kind, extended))
    cols = (regs or B.X_MAIN) + ctrl + [col]
    d = df.dropna(subset=cols).copy()
    ctrl = [c for c in ctrl if d[c].nunique() > 1]          # drop all-constant dummies (e.g. Korean regions in the Morocco-only sample)
    X, names = design(d, kind, interact, pooled, extended, regs, ctrl)
    w = d[wcol].values if weighted else None
    st = (d["country"] + "_" + d["strata"].astype(str)).values if (weighted and not strata_ignore) else None
    y = d[col].values
    f = model_fn or {"ols": svy.ols, "logit": svy.logit, "frac": svy.fracit}[est]
    r = f(y, X, w=w, strata=st, names=names)
    return r, d, X, names

def tidy(r, model, key, est, d, X, names, weighted=True, tag="main", extra=None, outcomes=None, wcol="w_strict_std"):
    outcomes = outcomes or B.OUTCOMES
    t = r.table(); t["model"] = model; t["outcome_key"] = key; t["outcome"] = outcomes[key][0]; t["estimator"] = est
    t["n"] = r.n; t["df"] = r.df; t["weighted"] = weighted; t["tier"] = tag
    t["fit"] = r.extra.get("r2", r.extra.get("pseudo_r2", np.nan))
    if est == "logit":
        w = d[wcol].values if weighted else None
        for v in B.X_MAIN:
            if v in names:
                a = svy.ame_logit(r, X, names, v, w)
                for k_, val in a.items(): t.loc[t.term == v, "ame" if k_ == "ame" else "ame_" + k_] = val
        t["odds_ratio"] = np.exp(t["coef"])
    # support diagnostics for each binary regressor: number treated, and (for logit) successes among treated / untreated
    names_l = list(names)
    for v in B.X_MAIN:
        if v in names_l:
            xv = X[:, names_l.index(v)]; yv = d[outcomes[key][0]].values
            t.loc[t.term == v, "n_treated"] = int((xv == 1).sum())
            if est == "logit":
                t.loc[t.term == v, "y1_among_treated"] = int(((xv == 1) & (yv == 1)).sum())
                t.loc[t.term == v, "y1_among_untreated"] = int(((xv == 0) & (yv == 1)).sum())
                t.loc[t.term == v, "sparse_cell_flag"] = bool(((xv == 1) & (yv == 1)).sum() < 5 or ((xv == 1) & (yv == 0)).sum() < 5 or ((xv == 0) & (yv == 1)).sum() < 5)
    if extra:
        for k_, v_ in extra.items(): t[k_] = v_
    return t

def run_main(df, weighted=True, extended=False, tag="main", regs=None, ctrl_override=None, outcomes=None, wcol="w_strict_std", strata_ignore=False, only=None):
    out, m4eff = [], []
    outcomes = outcomes or B.OUTCOMES
    for key, (col, est, kind, dim, labx) in outcomes.items():
        if only and key not in only: continue
        for model, sub, pooled, inter in [("M1 Morocco", df[df.country == "MAR"], False, False), ("M2 Korea", df[df.country == "KOR"], False, False),
                                          ("M3 Pooled", df, True, False), ("M4 Pooled x Korea", df, True, True)]:
            try:
                r, d, X, names = fit(sub, col, est, kind, pooled, inter, weighted, extended, regs, ctrl_override, wcol, None, strata_ignore)
            except Exception as e:
                print("FAILED", key, model, e); continue
            extra = {}
            if model.startswith("M4"):
                ix = [names.index(f"{v}:Korea") for v in (regs or B.X_MAIN)]
                F, p, q = svy.wald(r, ix); extra = {"wald_F_interactions": F, "wald_p_interactions": p}
                # implied country-specific effects with delta-method covariance
                for v in (regs or B.X_MAIN):
                    j = names.index(v); k = names.index(f"{v}:Korea"); V = r.V
                    eM, vM = r.b[j], V[j, j]; eK = r.b[j] + r.b[k]; vK = V[j, j] + V[k, k] + 2 * V[j, k]
                    m4eff.append(dict(outcome_key=key, regressor=v, effect_MAR=eM, se_MAR=np.sqrt(vM), p_MAR=2 * stats.t.sf(abs(eM / np.sqrt(vM)), r.df),
                                      effect_KOR=eK, se_KOR=np.sqrt(vK), p_KOR=2 * stats.t.sf(abs(eK / np.sqrt(vK)), r.df),
                                      diff_KOR_minus_MAR=r.b[k], se_diff=np.sqrt(V[k, k]), p_diff=2 * stats.t.sf(abs(r.b[k] / np.sqrt(V[k, k])), r.df), n=r.n,
                                      n_MAR=int((d.country == "MAR").sum()), n_KOR=int((d.country == "KOR").sum()), tier=tag, weighted=weighted, estimator=est))
            t = tidy(r, model, key, est, d, X, names, weighted, tag, extra, outcomes, wcol)
            t["n_MAR"] = int((d.country == "MAR").sum()); t["n_KOR"] = int((d.country == "KOR").sum())
            out.append(t)
    res = pd.concat(out, ignore_index=True)
    # Holm across the regressor x outcome tests within each model
    res["p_holm"] = np.nan
    for m, g in res[res.term.isin(B.X_MAIN)].groupby("model"):
        p = g.p.values; o = np.argsort(p); adj = np.empty_like(p); run = 0
        for rank, i in enumerate(o):
            run = max(run, min(1, (len(p) - rank) * p[i])); adj[i] = run
        res.loc[g.index, "p_holm"] = adj
    # Holm across the 21 interaction tests of Model 4 (country differences)
    res["p_holm_interaction"] = np.nan
    g = res[(res.model == "M4 Pooled x Korea") & res.term.str.endswith(":Korea")]
    if len(g):
        pv = g.p.values; o = np.argsort(pv); adj = np.empty_like(pv); run_ = 0
        for rank, i in enumerate(o):
            run_ = max(run_, min(1, (len(pv) - rank) * pv[i])); adj[i] = run_
        res.loc[g.index, "p_holm_interaction"] = adj
    return res, pd.DataFrame(m4eff)

if __name__ == "__main__":
    A = B.analytic()
    res, m4 = run_main(A)
    res.to_csv(os.path.join(RES, "main_results.csv"), index=False)
    m4.to_csv(os.path.join(RES, "m4_country_effects.csv"), index=False)
    log(f"05 main models: {res.groupby(['outcome_key','model']).ngroups} model fits; N by model written", "regressions.log")
    pd.set_option("display.width", 250)
    show = res[res.term.isin(B.X_MAIN)][["model", "outcome_key", "term", "coef", "se", "p", "p_holm", "n", "n_treated"]]
    print(show.round(3).to_string())
    print(m4.round(3).to_string())
