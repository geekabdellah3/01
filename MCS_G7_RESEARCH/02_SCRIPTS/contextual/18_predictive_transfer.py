"""Competing models M1 (universal), M2 (organisational contingency), national-slope models, evaluated out of sample (same folds, score rebuilt inside folds),
and an international transferability matrix. Associations/prediction only; no causal claim.
M3 (institutional Z_c x MCS) cannot be estimated with 7 countries; it is nested in the national-slope model, which is the upper bound for any Z_c interaction."""
import os, sys, pickle, warnings
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
from lca_core import *
from scipy import stats
from scipy.special import softmax
warnings.filterwarnings("ignore")
OUTD = os.path.join(ROOT, "08_CONTEXTUAL_FIT"); K_F, REP = 10, 3
d = load_analytic(); store = pickle.load(open(os.path.join(RES, "lca/lca_store.pkl"), "rb"))
raw = load_raw(); raw = raw[raw.r1.notna()].copy(); raw["firm_key"] = raw.cid + "_" + raw.source_row.astype(str)
dd = d[store["A"]["keep"]].reset_index(drop=True).join(raw.set_index("firm_key")[["b2b", "d3b", "d3c", "b7", "b7a"]], on="firm_key")
dd["foreign10"] = np.where(dd.b2b >= 10, 1.0, np.where(dd.b2b >= 0, 0.0, np.nan))
dd["exporter"] = np.where((dd.d3b.fillna(-1) >= 0) & (dd.d3c.fillna(-1) >= 0), ((dd.d3b + dd.d3c) > 0).astype(float), np.nan)
dd["ln_mgr_exp"] = np.log(dd.b7.where(dd.b7 > 0)); dd["female_mgr"] = dd.b7a.map({1: 1.0, 2: 0.0})
w = lambda s: s.clip(s.quantile(.01), s.quantile(.99))
dd["sales_growth3y_ann"] = w(dd.sales_growth3y_ann); dd["emp_growth3y_ann"] = w(dd.emp_growth3y_ann); dd["ln_lp"] = dd.groupby("cid").ln_lp.transform(lambda s: s.clip(s.quantile(.005), s.quantile(.995)))
MODS = ["ln_emp", "ln_age", "foreign10", "exporter", "ln_mgr_exp", "female_mgr"]
OUT = {"ln_lp": "Log sales per employee", "sales_growth3y_ann": "Sales growth (ann.)", "emp_growth3y_ann": "Employment growth (ann.)"}
ITEMS = [c for c in d if c.startswith("A_")]; Xit = dd[ITEMS].fillna(-1).astype(int).values; ncat = [int(Xit[:, j].max()) + 1 for j in range(Xit.shape[1])]
Zall = onehot(Xit, ncat); z15, wq15 = gh_nodes(15)

def train_score(tr):
    """item parameters estimated on TRAINING firms only (outcome-free); returns scoring function for any firm index"""
    p = fit_param(Xit[tr], ncat, "nrm1", n_starts=1, max_iter=120); Bs = p["Beta"]; Xs = p["Xs"]
    logT = [np.log(softmax(np.c_[np.zeros(len(Xs)), Xs @ B], 1) + EPS) for B in Bs]
    def score(idx):
        L = sum(Zall[j][idx] @ logT[j].T for j in range(len(ncat))) + np.log(wq15)[None, :]; L -= L.max(1, keepdims=True); P = np.exp(L); P /= P.sum(1, keepdims=True); return P @ Xs[:, 1]
    s_tr = score(tr); sgn = 1.0 if np.corrcoef(s_tr, dd.S_core.fillna(dd.S_core.mean()).values[tr])[0, 1] > 0 else -1.0
    return lambda idx: sgn * score(idx)

def build(df, theta, kind, q1=None, q2=None):
    """design blocks for model families; theta oriented; moderators standardised using training stats passed in df attrs"""
    return None

def design(sub, th, spec, cuts, mu_sd):
    S = pd.get_dummies(sub.sector_c.astype(str), dtype=float).reindex(columns=SECT, fill_value=0.0).values
    t = th
    mods = np.c_[[(sub[m].values - mu_sd[m][0]) / mu_sd[m][1] for m in MODS]].T
    base = np.c_[S, sub.ln_emp.values, sub.ln_age.values, mods[:, 2:]]     # SAME main effects (incl. non-control moderators) in every model, so that differences isolate the MCS terms
    C = pd.get_dummies(sub.cid, dtype=float).reindex(columns=CORDER, fill_value=0.0).values
    t1 = np.minimum(t, cuts[0]); t2 = np.clip(t, cuts[0], cuts[1]) - cuts[0]; t3 = np.maximum(t, cuts[1]) - cuts[1]
    if spec == "U0": return base
    if spec == "U1": return np.c_[base, t]
    if spec == "U2": return np.c_[base, t1, t2, t3]
    if spec == "C1": return np.c_[base, t1, t2, t3, mods * t[:, None]]          # contingency: score x organisational moderators (+ main effects of non-control moderators)
    if spec == "N1": return np.c_[base, C * t[:, None]]
    if spec == "N2": return np.c_[base, t1, t2, t3, C[:, :-1] * t[:, None]]
    if spec == "X": return np.c_[base, t1, t2, t3, mods * t[:, None], mods[:, 2:], C[:, :-1] * t[:, None]]
SPECS = ["U0", "U1", "U2", "C1", "N1", "N2", "X"]
res_rows, pair_rows, cty_rows = [], [], []
for y, lab in OUT.items():
    sub = dd.dropna(subset=[y] + MODS + ["S_core"]).reset_index(drop=True); idx_global = sub.index.values
    # rows of dd for scoring: align via firm_key
    pos = pd.Series(np.arange(len(dd)), index=dd.firm_key).loc[sub.firm_key].values
    SECT = sorted(sub.sector_c.unique()); yv = sub[y].values; n = len(sub)
    sse = {s: np.zeros(n) for s in SPECS}; sse_by_rep = {s: [] for s in SPECS}
    for rep in range(REP):
        rng = np.random.default_rng(SEED + rep); fold = np.zeros(n, int)
        for c in CORDER:
            ii = np.where(sub.cid.values == c)[0]; ii = rng.permutation(ii); fold[ii] = np.arange(len(ii)) % K_F
        pred = {s: np.zeros(n) for s in SPECS}
        for f in range(K_F):
            te = np.where(fold == f)[0]; tr = np.where(fold != f)[0]
            sc = train_score(pos[tr]); th_all = np.zeros(n); th_all[tr] = sc(pos[tr]); th_all[te] = sc(pos[te])
            mu = th_all[tr].mean(); sdv = th_all[tr].std(); th_all = (th_all - mu) / sdv
            cuts = np.quantile(th_all[tr], [1 / 3, 2 / 3]); mu_sd = {m: (sub[m].values[tr].mean(), sub[m].values[tr].std()) for m in MODS}
            for s in SPECS:
                Xd = design(sub, th_all, s, cuts, mu_sd); b = np.linalg.lstsq(Xd[tr], yv[tr], rcond=None)[0]; pred[s][te] = Xd[te] @ b
        for s in SPECS: e2 = (yv - pred[s]) ** 2; sse[s] += e2 / REP; sse_by_rep[s].append(np.sqrt(e2.mean()))
    for s in SPECS:
        res_rows.append(dict(outcome=lab, model=s, N=n, rmse_oos=float(np.mean(sse_by_rep[s])), rmse_sd_across_repeats=float(np.std(sse_by_rep[s])), incr_R2_oos_vs_U0=1 - sse[s].sum() / sse["U0"].sum()))
    for ref, mdl in [("U0", "U1"), ("U1", "U2"), ("U2", "C1"), ("U1", "N1"), ("U2", "N2"), ("C1", "X"), ("N2", "X"), ("U1", "C1")]:
        dlt = sse[ref] - sse[mdl]; m_, se = dlt.mean(), dlt.std(ddof=1) / np.sqrt(n)
        pair_rows.append(dict(outcome=lab, reference=ref, model=mdl, mean_sq_error_reduction=m_, ci_lo=m_ - 1.96 * se, ci_hi=m_ + 1.96 * se, z=m_ / se, rel_reduction_pct=100 * m_ / sse[ref].mean()))
    for c in CORDER:
        mk = (sub.cid == c).values
        for s in SPECS: cty_rows.append(dict(outcome=lab, country=c, model=s, N=int(mk.sum()), rmse_oos=float(np.sqrt(sse[s][mk].mean())), incr_R2_vs_U0=1 - sse[s][mk].sum() / sse["U0"][mk].sum()))
    print(lab, pd.DataFrame([r for r in res_rows if r["outcome"] == lab]).round(4).to_string(), flush=True)
res = pd.DataFrame(res_rows); pr = pd.DataFrame(pair_rows); cr = pd.DataFrame(cty_rows)
print(pr.round(4).to_string()); log("18 predictive: CV done")
# ---------------- transferability matrix ----------------
nr = store["A"]["models"]["nrm1_1"]; th_full = nr["post"] @ nr["Xs"][:, 1]; th_full = th_full if np.corrcoef(th_full, dd.S_core.fillna(dd.S_core.mean()))[0, 1] > 0 else -th_full
dd["th"] = (th_full - th_full.mean()) / th_full.std(); q1, q2 = dd.th.quantile([1 / 3, 2 / 3])
def demean(df, cols):
    out = df.copy()
    for c in cols: out[c] = df[c] - df.groupby("sector_c")[c].transform("mean")
    return out
def feats(df, shape):
    if shape == "linear": return np.c_[df.th.values, df.ln_emp.values, df.ln_age.values]
    t = df.th.values; return np.c_[np.minimum(t, q1), np.clip(t, q1, q2) - q1, np.maximum(t, q2) - q2, df.ln_emp.values, df.ln_age.values]
trows = []; B = 200
for y, lab in OUT.items():
    sub = dd.dropna(subset=[y, "ln_emp", "ln_age", "th"]).copy(); sub = demean(sub, [y, "th", "ln_emp", "ln_age"])
    for shape in ["linear", "level-dependent"]:
        G = {c: (feats(sub[sub.cid == c], shape), sub[sub.cid == c][y].values) for c in CORDER}
        def fitb(Xs_, ys_): return np.linalg.lstsq(Xs_, ys_, rcond=None)[0]
        def r2(Xt, yt, b): return 1 - ((yt - Xt @ b) ** 2).sum() / (yt ** 2).sum()
        for t_ in CORDER:
            Xt, yt = G[t_]
            # local benchmark: repeated 10-fold CV within target
            rng = np.random.default_rng(SEED); loc = []
            for rep in range(5):
                f = rng.permutation(len(yt)) % 10; pr_ = np.zeros(len(yt))
                for k in range(10): pr_[f == k] = Xt[f == k] @ fitb(Xt[f != k], yt[f != k])
                loc.append(1 - ((yt - pr_) ** 2).sum() / (yt ** 2).sum())
            r_loc = float(np.mean(loc))
            srcs = [s_ for s_ in CORDER if s_ != t_]
            for s_ in srcs + ["LOCO (other 6 pooled)"]:
                Xs_, ys_ = (np.vstack([G[k][0] for k in srcs]), np.concatenate([G[k][1] for k in srcs])) if s_.startswith("LOCO") else G[s_]
                b = fitb(Xs_, ys_); r_tr = r2(Xt, yt, b)
                bs = []; rg = np.random.default_rng(SEED + 7)
                for _ in range(B):
                    ii = rg.integers(0, len(ys_), len(ys_)); jj = rg.integers(0, len(yt), len(yt)); bb = fitb(Xs_[ii], ys_[ii]); bs.append(r2(Xt[jj], yt[jj], bb))
                trows.append(dict(outcome=lab, shape=shape, source=s_, target=t_, n_source=len(ys_), n_target=len(yt), R2_transfer=r_tr, R2_local_cv=r_loc, gap_local_minus_transfer=r_loc - r_tr, R2_transfer_ci_lo=np.percentile(bs, 2.5), R2_transfer_ci_hi=np.percentile(bs, 97.5)))
tr_ = pd.DataFrame(trows)
with pd.ExcelWriter(os.path.join(OUTD, "PREDICTIVE_COMPARISON_AND_TRANSFER.xlsx")) as wx:
    res.to_excel(wx, sheet_name="oos_by_model", index=False); pr.to_excel(wx, sheet_name="paired_comparisons", index=False); cr.to_excel(wx, sheet_name="oos_by_country", index=False); tr_.to_excel(wx, sheet_name="transfer_matrix_long", index=False)
    for (o, sh), g in tr_.groupby(["outcome", "shape"]): g.pivot(index="source", columns="target", values="R2_transfer").reindex(columns=CORDER).round(4).to_excel(wx, sheet_name=f"T_{o[:6]}_{sh[:4]}")
print(tr_[(tr_.outcome == "Log sales per employee") & (tr_.shape == "linear")].pivot(index="source", columns="target", values="R2_transfer").round(4).to_string())
print(tr_[(tr_.source.str.startswith("LOCO"))].round(4).to_string())
log("18 predictive+transfer: done")
