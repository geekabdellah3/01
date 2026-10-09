"""Phase 2 - automated WBES data audit.

Reads the ORIGINAL .dta files (never modified) and writes
  outputs/02_MOROCCO_DICTIONARY.xlsx
  outputs/02_KOREA_DICTIONARY.xlsx
  outputs/02_MISSING_DATA_REPORT.xlsx

WBES special codes (negative integers) are NOT valid answers:
  -9 don't know, -8 refused, -7 not applicable / not in business, -6 still in process
They are counted separately from system-missing (question not asked / skipped by
the questionnaire routing or by the split-sample design) and are never recoded to 0.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from common import *

SPECIAL = {-9: "DK", -8: "Refused", -7: "N/A", -6: "Other special", -5: "Other special"}

# Variable-name prefix -> questionnaire section. INFERRED from prefixes + labels; the questionnaire
# PDF is not in the project, so these names are descriptive, not official section titles.
SECTION = {"a": "A. Control/sampling/general", "b": "B. Firm characteristics/ownership/management",
           "c": "C. Infrastructure & services", "d": "D. Sales & supplies/trade", "e": "E. Competition/market",
           "f": "F. Capacity", "g": "G. Land & permits", "ge": "GE. Green-economy items (partial)",
           "h": "H. Innovation & technology", "i": "I. Crime", "j": "J. Business-government relations",
           "k": "K. Finance", "l": "L. Labour", "m": "M. Main obstacle", "n": "N. Costs/assets/taxes",
           "o": "O. Disputes", "r": "R. Management practices/performance",
           "w": "Survey weights", "s": "Stratification"}

# Topic assignment (A-I of the project brief). Curated by reading every label (see 02 dictionaries).
TOPICS = {
 "A": "Sales & financial performance", "B": "Employment", "C": "Female employment",
 "D": "Skilled/unskilled workers", "E": "Innovation", "F": "Digitalization & ICT",
 "G": "Environmental practices", "H": "Education & training", "I": "Firm characteristics"}
TOPIC_VARS = {
 "A": ["d2", "d2x", "d2a1", "d2a1x", "n3", "n3x", "n2a", "n2a1", "n2a2", "n2b", "n2e", "n2e1", "n2i", "n2k", "n5a", "n5b", "n5c", "n5d",
       "n7a", "d3a", "d3b", "d3c", "d1a3", "f1", "k3a", "k3bc", "k3e", "k3f", "k3hd", "k4", "k4b", "k5a", "k5bc", "k5e", "k5f", "k5i",
       "k6", "k7", "k82", "k15b", "k15c", "k162", "k21", "n11", "n12"],
 "B": ["l1", "l1a", "l2", "l3a", "l3b", "l6", "l6a", "l8", "l31", "l32", "l33", "l34", "b6"],
 "C": ["l5", "l5a", "l5b", "l6a", "l12a", "l12a1", "b4", "b4a", "b7a"],
 "D": ["l4a1", "l4a2", "l4b", "l3a", "l3b", "l9b", "l9b1", "l30b", "m1a_workforce_pos"],
 "E": ["h1", "h2", "h3x", "h4x", "h32x", "h5", "h6x", "h62x", "h7x", "h8", "h9", "e6", "b8"],
 "F": ["c22b", "k33", "k34", "k342", "k35", "k36", "k37", "k38", "k39", "k392", "k40", "j36", "j37", "c36", "c37", "c38", "c39",
       "c40a", "c40b", "c41a", "c41b", "c42", "n2l", "d37"],
 "G": ["ge3", "ge3a", "ge7", "ge8d"],
 "H": ["l10", "l11a", "l11a1", "l11b", "l11b1", "l12a", "l12a1", "l9b", "l9b1", "l30b", "b7"],
 "I": ["a1", "a2", "a3", "a3a", "a4a", "a6a", "a6c", "a7", "a7a", "a7b", "b1", "b2a", "b2b", "b2c", "b2d", "b3a", "b5", "b7", "b8",
       "a14y", "a20y", "d1a2_v4", "e6"],
}
VAR2TOPICS = {}
for t, vs in TOPIC_VARS.items():
    for v in vs:
        VAR2TOPICS.setdefault(v, []).append(t)

def section_of(v):
    if v.startswith("ge") and v[2:3].isdigit(): return SECTION["ge"]
    if v.startswith("strat") or v == "strata": return SECTION["s"]
    if v.startswith(("wmedian", "wstrict", "wweak")): return SECTION["w"]
    return SECTION.get(v[0], "Other/derived")

def num(s):
    """Coerce pyreadstat 'object' columns holding ints (module-routed items) to numeric."""
    if s.dtype == object:
        return pd.to_numeric(s, errors="coerce")
    return s

def dictionary(c):
    df, meta = load(c)
    rows, vl_rows = [], []
    n = len(df)
    orig_types = dict(zip(meta.column_names, meta.original_variable_types.values())) if isinstance(meta.original_variable_types, dict) else {}
    for v in df.columns:
        s_raw = df[v]
        s = num(s_raw)
        is_num = s.dtype.kind in "fiu"
        lab = meta.column_names_to_labels.get(v)
        vls = meta.variable_value_labels.get(v, {})
        sysmiss = int(s.isna().sum())
        if is_num:
            spec = {k: int((s == k).sum()) for k in SPECIAL}
            n_spec = sum(spec.values())
            valid = s[(~s.isna()) & (~s.isin(list(SPECIAL)))]
            other_neg = int((valid < 0).sum())
        else:
            spec = {k: 0 for k in SPECIAL}; n_spec = 0
            valid = s_raw.dropna().astype(str).str.strip(); valid = valid[valid != ""]
            other_neg = 0
        row = dict(variable=v, label=lab, section_inferred=section_of(v),
                   topics=",".join(VAR2TOPICS.get(v, [])), stata_type=orig_types.get(v), pandas_dtype=str(s_raw.dtype),
                   kind="numeric" if is_num else "string", has_value_labels=bool(vls),
                   n_obs=n, n_system_missing=sysmiss, n_DK_m9=spec[-9], n_refused_m8=spec[-8], n_NA_m7=spec[-7],
                   n_other_special=spec[-6] + spec[-5], n_special_total=n_spec, n_valid=int(len(valid)),
                   pct_valid=round(100 * len(valid) / n, 1), n_unique_valid=int(valid.nunique()),
                   other_negative_values=other_neg)
        if is_num and len(valid):
            row.update(min=float(valid.min()), p01=float(valid.quantile(.01)), p50=float(valid.median()), p99=float(valid.quantile(.99)),
                       max=float(valid.max()), mean=float(valid.mean()), sd=float(valid.std()))
        rows.append(row)
        for k, t in vls.items():
            try: cnt = int((s == k).sum()) if is_num else None
            except Exception: cnt = None
            vl_rows.append(dict(variable=v, code=k, value_label=t, n=cnt))
    d = pd.DataFrame(rows); vl = pd.DataFrame(vl_rows)
    return df, meta, d, vl

def design_sheets(c, df, meta):
    out = {}
    lab = lambda v: meta.variable_value_labels.get(v, {})
    for v in ["a4a", "a6a", "a2", "a1c", "a3", "a7", "b1"]:
        if v in df:
            t = df[v].value_counts(dropna=False).sort_index().rename("n").reset_index().rename(columns={v: "code", "index": "code"})
            t.insert(0, "variable", v); t["label"] = t["code"].map(lab(v)); t["pct"] = (100 * t["n"] / len(df)).round(1)
            out[v] = t
    des = pd.concat(out.values(), ignore_index=True)
    w = pd.DataFrame({k: df[k].describe() for k in ["wstrict", "wmedian", "wweak"]}).T.reset_index().rename(columns={"index": "weight"})
    w["sum_weights"] = [df[k].sum() for k in ["wstrict", "wmedian", "wweak"]]
    sm = pd.DataFrame({"strata_n": [df.strata.nunique()], "min_firms_per_stratum": [df.strata.value_counts().min()],
                       "max_firms_per_stratum": [df.strata.value_counts().max()],
                       "strata_with_one_firm": [(df.strata.value_counts() == 1).sum()],
                       "psu_variable": ["NONE in file (no cluster/PSU id; firm id only)"]})
    return des, w, sm

def main():
    miss_tabs, summaries = {}, []
    for c, name in [("MAR", "MOROCCO"), ("KOR", "KOREA")]:
        df, meta, d, vl = dictionary(c)
        des, w, sm = design_sheets(c, df, meta)
        info = pd.DataFrame({"item": ["country", "source file", "n observations", "n variables", "stata file label", "read encoding",
                                       "interview year range (a14y)", "fiscal-year close range (a20y)", "note"],
                             "value": [name, FILES[c], len(df), df.shape[1], meta.file_label, ENC,
                                       f"{df.a14y.min()}-{df.a14y.max()}", f"{df.a20y.min()}-{df.a20y.max()}",
                                       "Special codes are counted separately; 'object' columns hold integer answers of routed modules and were coerced to numeric."]})
        topics_df = pd.DataFrame([(k, TOPICS[k], ", ".join(v)) for k, v in TOPIC_VARS.items()], columns=["topic", "name", "variables_flagged"])
        path = os.path.join(OUT, f"02_{name}_DICTIONARY.xlsx")
        with pd.ExcelWriter(path, engine="openpyxl") as xw:
            info.to_excel(xw, sheet_name="README", index=False)
            d.to_excel(xw, sheet_name="Variables", index=False)
            vl.to_excel(xw, sheet_name="ValueLabels", index=False)
            d[d.topics != ""].sort_values(["topics", "variable"]).to_excel(xw, sheet_name="Topic_candidates_A-I", index=False)
            topics_df.to_excel(xw, sheet_name="Topic_definitions", index=False)
            des.to_excel(xw, sheet_name="Design_strata_size_industry", index=False)
            w.to_excel(xw, sheet_name="Weights", index=False)
            sm.to_excel(xw, sheet_name="Strata_summary", index=False)
        log(f"{c}: dictionary written {path}; {df.shape}; vars with other negative values: {d[d.other_negative_values>0].variable.tolist()}", "audit.log")
        d["country"] = c
        summaries.append(d)

        # missing-data per topic
        t = d[d.topics != ""].assign(topic=lambda x: x.topics.str.split(",")).explode("topic")
        g = t.groupby("topic").agg(n_vars=("variable", "count"), mean_pct_valid=("pct_valid", "mean"),
                                   n_vars_lt50_valid=("pct_valid", lambda x: int((x < 50).sum()))).round(1).reset_index()
        g["topic_name"] = g.topic.map(TOPICS); g.insert(0, "country", c)
        miss_tabs.setdefault("By_topic", []).append(g)

        # KEY variables: structural missingness by sector and size
        keyv = ["d2", "n3", "l1", "l2", "l3a", "l5", "l5a", "l4a1", "l4b", "l9b", "l9b1", "h1", "h5", "h8", "c22b", "k33", "k38", "j36", "j37", "ge3", "ge7", "ge8d", "k82"]
        recs = []
        for v in keyv:
            s = num(df[v])
            st = pd.Series(np.where(s.isna(), "system-missing (not asked)", np.where(s.isin(list(SPECIAL)), "special code", "valid")), index=df.index)
            for by, lab_ in [("a4a", "sector"), ("a6a", "size")]:
                ct = pd.crosstab(df[by].map(meta.variable_value_labels[by]), st)
                for lv, r in ct.iterrows():
                    recs.append(dict(country=c, variable=v, by=lab_, level=lv, n=int(r.sum()),
                                     pct_valid=round(100 * r.get("valid", 0) / r.sum(), 1),
                                     pct_special=round(100 * r.get("special code", 0) / r.sum(), 1),
                                     pct_not_asked=round(100 * r.get("system-missing (not asked)", 0) / r.sum(), 1)))
        miss_tabs.setdefault("Key_vars_by_sector_size", []).append(pd.DataFrame(recs))

        # DK mechanics: is -9 on l4 / k33 correlated with size/sector?  (reported, not corrected)
        miss_tabs.setdefault("Complete_case_counts", []).append(pd.DataFrame({
            "country": c,
            "set": ["sales growth (d2,n3)", "employment growth (l1,l2)", "female share via l5 (l5,l1)", "female share via l5a+l5b",
                    "female share (either route)", "low-skill share of production (l4b,l3a)", "high-school share (l9b)",
                    "h1 valid", "h5 valid", "website c22b valid", "ge8d valid"],
            "n_valid": [
                int(((df.d2 > 0) & (num(df.n3) > 0)).sum()), int(((df.l1 > 0) & (df.l2 > 0)).sum()),
                int(((num(df.l5) >= 0) & (df.l1 > 0)).sum()),
                int(((num(df.l5a) >= 0) & (num(df.l5b) >= 0) & (df.l1 > 0)).sum()),
                int((((num(df.l5) >= 0) | ((num(df.l5a) >= 0) & (num(df.l5b) >= 0))) & (df.l1 > 0)).sum()),
                int(((df.l4b >= 0) & (num(df.l3a) > 0)).sum()), int((num(df.l9b) >= 0).sum()),
                int((df.h1 > 0).sum()), int((df.h5 > 0).sum()), int((df.c22b > 0).sum()), int((df.ge8d > 0).sum())]}))
    full = pd.concat(summaries, ignore_index=True)
    cmp_ = full.pivot(index="variable", columns="country", values=["label", "n_valid", "pct_valid"])
    cmp_.columns = [f"{a}_{b}" for a, b in cmp_.columns]
    cmp_ = cmp_.reset_index()
    cmp_["in_both"] = cmp_.label_MAR.notna() & cmp_.label_KOR.notna()
    cmp_["same_label"] = cmp_.label_MAR == cmp_.label_KOR
    with pd.ExcelWriter(os.path.join(OUT, "02_MISSING_DATA_REPORT.xlsx"), engine="openpyxl") as xw:
        readme = pd.DataFrame({"note": [
            "System-missing = item not asked (questionnaire routing or split-sample module design). It is NOT a zero.",
            "Special codes -9 (DK), -8 (refused), -7 (not applicable / not in business), -6 (in process) are never treated as zero or as valid values.",
            "Complete_case_counts: raw counts before any outlier rule; analytic samples are defined in 04_construct_indicators.",
            "Key_vars_by_sector_size shows whether missingness is structural (not asked) or item non-response (DK).",
            "Cross_country_label_compare: identical variable names do NOT imply identical constructs; see 03_VARIABLE_CROSSWALK."]})
        readme.to_excel(xw, sheet_name="README", index=False)
        pd.concat(miss_tabs["Complete_case_counts"]).to_excel(xw, sheet_name="Complete_case_counts", index=False)
        pd.concat(miss_tabs["By_topic"]).to_excel(xw, sheet_name="By_topic", index=False)
        pd.concat(miss_tabs["Key_vars_by_sector_size"]).to_excel(xw, sheet_name="Key_vars_by_sector_size", index=False)
        full[["country", "variable", "label", "topics", "n_obs", "n_system_missing", "n_DK_m9", "n_refused_m8", "n_NA_m7",
              "n_other_special", "n_valid", "pct_valid"]].to_excel(xw, sheet_name="All_variables", index=False)
        cmp_.to_excel(xw, sheet_name="Cross_country_label_compare", index=False)
    print("audit done")

if __name__ == "__main__":
    main()
