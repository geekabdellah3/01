"""STEP 1-2: file inventory, variable audit, harmonisation map, missingness diagnostics."""
import os, sys, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import *

log("01_audit: start")
# ---- STEP 1: the seven source .dta files named in the brief (Mac paths) -------------
paths = {
 "CAN": "/Users/abdellah/Downloads/Canada-2024-full-data.dta",
 "FRA": "/Users/abdellah/Downloads/France-2025-full data.dta",
 "USA": "/Users/abdellah/Downloads/United-States-2024-full-data.dta",
 "GBR": "/Users/abdellah/Downloads/United-Kingdom-2024-full-data.dta",
 "DEU": "/Users/abdellah/Downloads/Germany-2025-full-data.dta",
 "JPN": "/Users/abdellah/Downloads/Japan-2025-full data.dta",
 "ITA": "(no path given in brief: 'locate Italy 2024')"}
df = load_raw()
inv = []
for c in CORDER:
    p = paths[c]
    sub = df[df.cid == c]
    inv.append(dict(country=c, brief_path=p, dta_exists_in_this_environment=os.path.exists(p),
        rows_in_merged_csv=len(sub), survey_year_in_csv=int(sub.source_year.iloc[0]),
        n_columns_in_merged_csv=df.shape[1],
        note="Original .dta not accessible (files are on the user's Mac). Analysis uses the user-supplied merged CSV only; "
             "no other dataset was substituted. Value labels are NOT present in the CSV."))
inv = pd.DataFrame(inv)
h = hashlib.sha256(open(RAW, "rb").read()).hexdigest()
log(f"merged CSV sha256={h} rows={len(df)} cols={df.shape[1]}")

# ---- structural audit of r1..r11 ----------------------------------------------------
df["asked"] = df["r1"].notna()
gate = {"r3": "r2", "r5": "r4", "r6": "r4", "r7": "r4", "r9": "r8"}
status = {  # (functional description, verification status, source)
 "r1": ("Actions taken after a problem in the production/service process (4 response categories + code -7)",
        "PARTIAL", "Enterprise Surveys Questionnaire Manual 2019 (read via search summary): r1 = reaction to production-process problems. Category labels NOT seen."),
 "r2": ("Monitoring of production/service performance indicators (yes/no)", "PARTIAL",
        "ES Questionnaire Manual 2019 + microdata-library variable page (Gambia 2018) via search summary; 1=yes confirmed empirically by skip pattern into r3."),
 "r3": ("Number of performance indicators monitored (asked only if r2=yes; 3 bands)", "PARTIAL",
        "Gambia 2018 variable page (bands 1-2, 3-9, 10+) via search summary; skip pattern r2=1 confirmed in data. 2024 wording not seen."),
 "r4": ("Existence of production/service targets (yes/no) - gate for r5-r7", "INFERRED",
        "Not seen verbatim. Inferred: r5 label is about targets and r5-r7 are asked iff r4=1 (verified in data)."),
 "r5": ("Time frame of production/service provision targets (3 categories; conditional on r4)", "VERIFIED-LABEL",
        "Microdata-library Italy 2024 page V127: 'What best describes the time frame of production/service provision targets?'; 381 valid = our Italy count (381). Category labels NOT seen."),
 "r6": ("Unknown - 6 categories, conditional on r4", "UNVERIFIED", "Wording not retrieved. Treated as nominal; no substantive label assigned."),
 "r7": ("Unknown - 4 categories, conditional on r4", "UNVERIFIED", "Wording not retrieved. Treated as nominal; no substantive label assigned."),
 "r8": ("Performance bonuses tied to production/service targets (yes/no)", "PARTIAL",
        "Italy 2024 catalogue (r8) via search summary: bonuses tied to production/service targets. Population of bonus recipients not verified."),
 "r9": ("Basis on which (managers') bonuses are usually paid (4 categories; conditional on r8)", "PARTIAL",
        "Italy 2024 catalogue (r9) via search summary; category labels NOT seen."),
 "r10": ("Unknown - 4 categories + code -7 (people-management item, not verified)", "UNVERIFIED", "Wording not retrieved."),
 "r11": ("Unknown - 3 categories + code -7 (people-management item, not verified)", "UNVERIFIED", "Wording not retrieved."),
}
rows = []
for v in R:
    s = df[v]
    cats = sorted(s.dropna().unique())
    valid = s[s > 0]
    row = dict(variable=v, functional_description=status[v][0], verification_status=status[v][1],
               verification_source=status[v][2], universe_gate=("module universe (r1 asked)" if v not in gate else f"{gate[v]}=1 within module universe"),
               n_total=len(df), n_asked=int(s.notna().sum()), pct_asked_total=round(100 * s.notna().mean(), 1),
               n_dk_m9=int((s == -9).sum()), n_not_applicable_m7=int((s == -7).sum()),
               n_valid_substantive=int((s > 0).sum()), substantive_codes=str([int(c) for c in cats if c > 0]),
               n_substantive_categories=len([c for c in cats if c > 0]),
               missing_code_scheme="-9=don't know; -7=does-not-apply (only r1,r10,r11); blank=not asked (skip/universe)")
    for c in CORDER:
        sc = df[df.cid == c][v]
        row[f"codes_{c}"] = str([int(x) for x in sorted(sc.dropna().unique())])
    rows.append(row)
audit = pd.DataFrame(rows)

# empirical skip-pattern verification
sk = []
for child, parent in gate.items():
    ct = pd.crosstab(df[parent].fillna(-999), df[child].notna())
    ok = (df.loc[df[child].notna(), parent] == 1).all() and (df.loc[df[parent] == 1, child].notna().all())
    sk.append(dict(child=child, parent=parent, child_asked_iff_parent_equals_1=bool(ok),
                   n_child_asked=int(df[child].notna().sum()), n_parent_yes=int((df[parent] == 1).sum())))
sk.append(dict(child="r1,r2,r4,r8,r10,r11", parent="module universe", child_asked_iff_parent_equals_1=bool(
    all((df[v].notna() == df.asked).all() for v in ["r1", "r2", "r4", "r8", "r10", "r11"])),
    n_child_asked=int(df.asked.sum()), n_parent_yes=int(df.asked.sum())))
skip = pd.DataFrame(sk)

# module universe by size (l1 = permanent full-time employees, label unverified)
l1 = df.l1.where(df.l1 > 0)
uni = pd.DataFrame({"cid": df.cid, "asked": df.asked, "size_band": pd.cut(l1, [0, 4, 9, 19, 99, 1e9], labels=["1-4", "5-9", "10-19", "20-99", "100+"])})
uni_t = pd.crosstab(uni.size_band, uni.asked, normalize="index").round(3).reset_index()
uni_c = df.groupby("cid").asked.agg(["sum", "size", "mean"]).reindex(CORDER).reset_index()

with pd.ExcelWriter(os.path.join(RES, "descriptive/VARIABLE_AUDIT.xlsx")) as w:
    inv.to_excel(w, sheet_name="file_inventory", index=False)
    audit.to_excel(w, sheet_name="variable_audit", index=False)
    skip.to_excel(w, sheet_name="skip_pattern_check", index=False)
    uni_t.to_excel(w, sheet_name="module_universe_by_size", index=False)
    uni_c.to_excel(w, sheet_name="module_universe_by_country", index=False)
    pd.DataFrame({"note": [
      "All 7 country-year blocks are present in the merged CSV (Italy 2024 included), but the original .dta files cannot be verified here.",
      "The merged CSV contains codes only; question wording/value labels were NOT available. Verification status column states what could be confirmed.",
      "The World Bank microdata site was unreachable from this environment (network policy), so wording was checked only via search-engine summaries.",
      "Management module universe = establishments with the module asked (r1 non-blank): n=6316 of 10968; strongly concentrated in 20+ employees, consistent with the ES management index being defined for medium/large firms."]}).to_excel(w, sheet_name="notes", index=False)
log("01_audit: VARIABLE_AUDIT.xlsx written")

# ---- missingness diagnostics -------------------------------------------------------
def tab(v, sub):
    s = sub[v]
    return dict(n=len(s), not_asked_blank=int(s.isna().sum()), dk_m9=int((s == -9).sum()), na_m7=int((s == -7).sum()), valid=int((s > 0).sum()))
mrows = []
for c in CORDER + ["ALL"]:
    sub = df if c == "ALL" else df[df.cid == c]
    for v in R:
        d = tab(v, sub); d.update(country=c, variable=v)
        asked = d["n"] - d["not_asked_blank"]
        d["pct_dk_among_asked"] = round(100 * d["dk_m9"] / asked, 2) if asked else np.nan
        d["pct_m7_among_asked"] = round(100 * d["na_m7"] / asked, 2) if asked else np.nan
        mrows.append(d)
miss = pd.DataFrame(mrows)[["country", "variable", "n", "not_asked_blank", "dk_m9", "na_m7", "valid", "pct_dk_among_asked", "pct_m7_among_asked"]]
# within-universe: who gives DK? predictors of DK/-7 (logit) done in EDA; here simple size gradient
u = df[df.asked].copy()
u["size"] = pd.cut(u.l1.where(u.l1 > 0), [0, 49, 99, 249, 1e9], labels=["20-49(<50)", "50-99", "100-249", "250+"])
dkrows = []
for v in ["r1", "r2", "r4", "r8", "r10", "r11"]:
    t = u.groupby("size", observed=True)[v].apply(lambda s: ((s == -9) | (s == -7)).mean()).round(3)
    for k, val in t.items(): dkrows.append(dict(variable=v, size=k, share_dk_or_m7=val))
# complete-case counts under alternative rules
cc = []
sets = {"all 11 (complete-case deletion)": R, "universal 6 (r1,r2,r4,r8,r10,r11)": ["r1", "r2", "r4", "r8", "r10", "r11"],
        "universal 6 excluding -7 and -9 as missing": ["r1", "r2", "r4", "r8", "r10", "r11"]}
for k, vs in sets.items():
    if "all 11" in k: m = df[vs].notna().all(axis=1) & (df[vs] > 0).all(axis=1)
    elif "excluding" in k: m = (df[vs] > 0).all(axis=1)
    else: m = df[vs].notna().all(axis=1)
    cc.append(dict(rule=k, n=int(m.sum()), pct_of_total=round(100 * m.mean(), 1), pct_of_module_universe=round(100 * m.sum() / df.asked.sum(), 1)))
cc = pd.DataFrame(cc)
strat = pd.DataFrame([dict(strategy="Universe restriction", detail="Analytic universe = module-asked establishments (r1 non-blank). Blank in r1,r2,r4,r8,r10,r11 is a sampling-frame/filter exclusion, NOT item missingness.", use="all specs"),
 dict(strategy="Conditional items (r3,r5,r6,r7,r9)", detail="Blank iff gate=No (verified). Spec B: structural-absence category 0. Spec C: gate retained, child observed only when gate=Yes; FIML-type likelihood (blank items omitted).", use="B,C"),
 dict(strategy="Don't know (-9)", detail="Treated as missing; handled by FIML in LCA (items omitted from the likelihood). Assumes MAR given class; sensitivity: complete-case.", use="all"),
 dict(strategy="Does-not-apply (-7)", detail="Primary: set to missing (comparability across countries is doubtful: r11 -7 share 33% in Japan vs <5% UK). Sensitivity: retained as a separate response category.", use="A,B (primary); robustness"),
 dict(strategy="Complete-case deletion across all 11", detail="Rejected: would delete firms by design (skip patterns) and leave only firms with every practice present.", use="none")])
with pd.ExcelWriter(os.path.join(RES, "descriptive/MISSINGNESS_DIAGNOSTICS.xlsx")) as w:
    miss.to_excel(w, sheet_name="by_variable_country", index=False)
    pd.DataFrame(dkrows).to_excel(w, sheet_name="dk_m7_by_size_in_universe", index=False)
    cc.to_excel(w, sheet_name="complete_case_counts", index=False)
    strat.to_excel(w, sheet_name="handling_strategy", index=False)
log("01_audit: MISSINGNESS_DIAGNOSTICS.xlsx written")
print(inv[["country", "dta_exists_in_this_environment", "rows_in_merged_csv"]])
print(cc)
print(skip)
