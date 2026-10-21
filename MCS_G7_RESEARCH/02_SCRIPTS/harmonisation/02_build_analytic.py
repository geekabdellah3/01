"""STEP 3: analytic sample, recoding to LCA specifications A/B/C/D, covariates and outcomes."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import *
from scipy.stats import chi2_contingency
log("02_build: start")
df = load_raw()
u = df[df.r1.notna()].copy()                      # module universe
out = pd.DataFrame({"firm_key": u.cid + "_" + u.source_row.astype(str), "cid": u.cid, "year": u.source_year,
                    "wstrict": u.wstrict, "wmedian": u.wmedian, "wweak": u.wweak})
# ---- covariates -------------------------------------------------------------------
clean = lambda s: s.where(s > 0)
out["employees"] = clean(u.l1); out["ln_emp"] = np.log(out.employees)
out["age"] = (u.source_year.astype(float) - clean(u.b5)).where(lambda a: a >= 0)
out["ln_age"] = np.log(out.age.clip(lower=1))
out["sector_c"] = u.cid + "_" + u.a4a.astype(int).astype(str)      # sector codes are country-specific
out["size_class_a6a"] = u.a6a
out["ln_sales"] = np.log(clean(u.d2)); out["ln_lp"] = np.log(clean(u.d2) / clean(u.l1))
out["sales_growth3y_ann"] = np.log(clean(u.d2) / clean(u.n3)) / 3     # n3 meaning UNVERIFIED (assumed sales 3 FY ago)
out["emp_growth3y_ann"] = np.log(clean(u.l1) / clean(u.l2)) / 3        # l2 meaning UNVERIFIED
for c in ["h8", "e6", "o1"]:
    out[c + "_yes"] = u[c].map({1: 1, 2: 0})
# ---- raw item copy ---------------------------------------------------------------
for v in R: out[v] = u[v]
dk = lambda s: s.where(s > 0)           # -9,-7 -> NaN
def zb(s, lo=1):                           # substantive code -> 0-based, NaN stays NaN
    return (dk(s) - lo)
def code(frame):                           # NaN -> -1 for the LCA engine
    return frame.fillna(-1).astype(int)
A = pd.DataFrame({"r1": zb(u.r1), "r2": u.r2.map({1: 1, 2: 0}), "r4": u.r4.map({1: 1, 2: 0}),
                  "r8": u.r8.map({1: 1, 2: 0}), "r10": zb(u.r10), "r11": zb(u.r11)})
def cond(child, gate, g_no=2):
    x = pd.Series(np.nan, index=u.index)
    x[u[gate] == g_no] = 0                      # practice absent -> structural zero
    ok = u[gate] == 1
    x[ok] = dk(u.loc[ok, child])                # 1..k
    return x
B = pd.DataFrame({"r1": zb(u.r1) , "r3x": cond("r3", "r2"), "r5x": cond("r5", "r4"), "r6x": cond("r6", "r4"),
                  "r7x": cond("r7", "r4"), "r9x": cond("r9", "r8"), "r10": zb(u.r10), "r11": zb(u.r11)})
C = pd.DataFrame({"r1": zb(u.r1), "r2": u.r2.map({1: 1, 2: 0}), "r3": zb(u.r3), "r4": u.r4.map({1: 1, 2: 0}),
                  "r5": zb(u.r5), "r6": zb(u.r6), "r7": zb(u.r7), "r8": u.r8.map({1: 1, 2: 0}), "r9": zb(u.r9),
                  "r10": zb(u.r10), "r11": zb(u.r11)})
# D: as A but -7 kept as its own category (last index)
def keep7(s, k):
    x = zb(s); x[s == -7] = k; return x
D = pd.DataFrame({"r1": keep7(u.r1, 4), "r2": A.r2, "r4": A.r4, "r8": A.r8, "r10": keep7(u.r10, 4), "r11": keep7(u.r11, 3)})
for tag, fr in [("A", A), ("B", B), ("C", C), ("D", D)]:
    fr = fr.copy()
    for c in fr: out[f"{tag}_{c}"] = fr[c]
    log(f"spec {tag}: items={list(fr.columns)} categories={[int(fr[c].max())+1 for c in fr]} "
        f"n_any_obs={int(fr.notna().any(axis=1).sum())} n_complete={int(fr.notna().all(axis=1).sum())}")
# transparent aggregate scores (direction verified only for 1=yes gates and r3 bands order)
out["S_core"] = A[["r2", "r4", "r8"]].sum(axis=1, min_count=3)                 # 0..3 practices present
out["S_core_nobonus"] = A[["r2", "r4"]].sum(axis=1, min_count=2)
out["r3_level"] = B.r3x
out.to_csv(os.path.join(PROC, "mcs_analytic.csv"), index=False)
log(f"analytic file written: n={len(out)}")

# ---- harmonisation workbook -------------------------------------------------------
rec = pd.DataFrame([
 ["all","blank","not asked (outside module universe or skipped)","universe restriction / structural zero (B) / omitted (C)","structural missingness"],
 ["all","-9","don't know","NaN (FIML; excluded from complete-case)","item missing"],
 ["r1,r10,r11","-7","does-not-apply code","NaN in A,B,C; separate last category in D","comparability uncertain"],
 ["r2,r4,r8","1 / 2","yes / no (direction confirmed by skip logic)","1 / 0","binary practice present"],
 ["r1,r10,r11","1..k","substantive categories","0..k-1 (treated as NOMINAL in LCA)","order not verified"],
 ["r3,r5,r6,r7,r9","1..k (conditional)","substantive categories given gate=Yes","Spec B: gate=No -> 0, categories shifted to 1..k; Spec C: gate=No -> missing","structural"],
 ["l1","count","permanent full-time employees (label unverified)","employees; ln_emp","values<=0 -> NaN"],
 ["b5","year","establishment year (label unverified)","age = survey year - b5","negatives -> NaN"],
 ["d2,l1","LCU, count","sales / employees","ln_lp = ln(d2/l1); LCU differs by country -> only within-country comparisons (country FE)",""],
 ["d2,n3","LCU","sales now / 3 years ago (n3 label UNVERIFIED)","ln(d2/n3)/3, nominal","exploratory only"],
 ["a4a","1..15","sector code is country-specific","sector_c = country x a4a","not cross-country comparable"]],
 columns=["variables","raw_code","meaning","recode","comment"])
rows = []
for v in R:
    x = u[v]
    for c in CORDER:
        s = x[u.cid == c]; s = s[s > 0]
        vc = s.value_counts(normalize=True)
        for k, p in vc.items(): rows.append(dict(variable=v, country=c, category=int(k), share_among_substantive=round(p, 4), n=int(len(s))))
dist = pd.DataFrame(rows)
# cross-country comparability: chi2/Cramer's V, Jensen-Shannon between each country and rest
comp = []
for v in R:
    s = u[[v, "cid"]]; s = s[s[v] > 0]
    t = pd.crosstab(s.cid, s[v])
    chi, p, dof, _ = chi2_contingency(t)
    V = np.sqrt(chi / (t.values.sum() * (min(t.shape) - 1)))
    comp.append(dict(variable=v, n=int(t.values.sum()), chi2=round(chi, 1), dof=dof, p=p, cramers_V_country=round(V, 3),
                     categories_missing_in_some_country=any((t == 0).any())))
comp = pd.DataFrame(comp)
dk_rate = u.groupby("cid")[R].agg(lambda s: ((s == -9).sum() / s.notna().sum() if s.notna().sum() else np.nan)).round(4).reset_index()
m7_rate = u.groupby("cid")[["r1", "r10", "r11"]].agg(lambda s: (s == -7).mean()).round(4).reset_index()
specs = pd.DataFrame([
 ["A","r1,r2,r4,r8,r10,r11","r3,r5,r6,r7,r9 (conditional)","All six asked of every module-universe firm; no structural missingness; broadly comparable","-9,-7 -> missing (FIML)"],
 ["B","r1,r3x,r5x,r6x,r7x,r9x,r10,r11","r2,r4,r8 (absorbed into 0-categories)","Expanded: conditional items with structural-absence category","gate=No -> 0; -9,-7 -> missing"],
 ["C","all 11","none","Gate and child items together; child omitted from likelihood when skipped","FIML; skipped = missing"],
 ["D","r1,r2,r4,r8,r10,r11","r3,r5,r6,r7,r9","As A but -7 kept as separate response category","-9 -> missing"]],
 columns=["spec","included","excluded","justification","missing_data_strategy"])
for tag in "ABCD":
    cols = [c for c in out if c.startswith(tag + "_")]
    specs.loc[specs.spec == tag, "n_any_observed"] = int(out[cols].notna().any(axis=1).sum())
    specs.loc[specs.spec == tag, "n_complete_cases"] = int(out[cols].notna().all(axis=1).sum())
with pd.ExcelWriter(os.path.join(RES, "descriptive/VARIABLE_HARMONISATION.xlsx")) as w:
    rec.to_excel(w, sheet_name="recoding_rules", index=False)
    specs.to_excel(w, sheet_name="lca_specifications", index=False)
    dist.to_excel(w, sheet_name="category_shares_by_country", index=False)
    comp.to_excel(w, sheet_name="cross_country_homogeneity", index=False)
    dk_rate.to_excel(w, sheet_name="dk_rate_by_country", index=False)
    m7_rate.to_excel(w, sheet_name="m7_rate_by_country", index=False)
print(specs.to_string()); print(comp.to_string())
log("02_build: done")
