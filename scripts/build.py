"""Single source of truth for all derived variables (used by scripts 03-07).

Rules
 * WBES negative codes (-9 DK, -8 refused, -7 N/A / not in business, -6 in process) become NaN, never 0.
 * Routing/split-sample 'object' columns are coerced to numeric.
 * Growth is computed over the WBES 3-fiscal-year window (value at last FY vs value 3 FY ago).
 * Raw files are read-only; nothing here writes back to data/raw.
Scale convention: growth outcomes are ANNUALISED LOG growth x 100 (percentage points per year).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from common import load, FILES

# Harmonised 3-group sector (country-specific a4a codes -> common groups)
SECTOR3 = {"MAR": {1: "Manufacturing", 2: "Manufacturing", 3: "Manufacturing", 4: "Retail", 5: "Other services"},
           "KOR": {1: "Manufacturing", 2: "Manufacturing", 3: "Manufacturing", 4: "Manufacturing", 5: "Manufacturing", 6: "Manufacturing",
                   7: "Retail", 8: "Other services", 9: "Other services", 10: "Other services"}}
WIN = (0.01, 0.99)   # winsorisation percentiles (within country) for growth outcomes

def clean(df, k):
    s = pd.to_numeric(df[k], errors="coerce")
    return s.where(s >= 0)

def yn(df, k):
    s = pd.to_numeric(df[k], errors="coerce")
    return s.map({1: 1.0, 2: 0.0})

def winsor(s, lo=WIN[0], hi=WIN[1]):
    a, b = s.quantile(lo), s.quantile(hi)
    return s.clip(a, b)

def build_country(c):
    raw, meta = load(c)
    n = lambda k: clean(raw, k)
    d = pd.DataFrame(index=raw.index)
    d["country"] = c
    d["firm_id"] = raw["idstd"]
    d["strata"] = raw["strata"]
    d["region"] = raw["a2"]
    d["w_strict"] = raw["wstrict"]; d["w_median"] = raw["wmedian"]; d["w_weak"] = raw["wweak"]
    for w in ["w_strict", "w_median", "w_weak"]:
        d[w + "_std"] = d[w] / d[w].mean()           # mean 1 within country => each country weighted by its sample size when pooled
    d["fy_close"] = raw["a20y"]; d["svy_year"] = raw["a14y"]
    d["sector_code"] = raw["a4a"]
    d["sector3"] = raw["a4a"].map(SECTOR3[c])
    # ---- levels
    S1, S0 = n("d2"), n("n3")
    L1, L2 = n("l1"), n("l2")
    S1 = S1.where(S1 > 0); S0 = S0.where(S0 > 0); L1 = L1.where(L1 > 0); L2 = L2.where(L2 > 0)
    d["sales_t"], d["sales_t3"], d["emp_t"], d["emp_t3"] = S1, S0, L1, L2
    d["entrant_l2_m7"] = (raw["l2"] == -7)
    # ---- D1/D2 growth (annualised log x100) ; 3-year window
    d["g_sales_raw"] = 100 * np.log(S1 / S0) / 3
    d["g_emp_raw"] = 100 * np.log(L1 / L2) / 3
    d["g_lp_raw"] = d["g_sales_raw"] - d["g_emp_raw"]                      # exact identity: dln(S/L) = dlnS - dlnL
    for k in ["g_sales", "g_emp", "g_lp"]:
        d[k] = d.groupby("country")[k + "_raw"].transform(winsor)         # main (winsorised 1/99 within country)
    d["g_sales_adew"] = (S1 - S0) / S1                                     # Adewumi & Zhang (2026) definition, upper-bounded by 1
    d["g_sales_cagr"] = 100 * ((S1 / S0) ** (1 / 3) - 1)
    d["g_emp_dhs"] = 100 * ((L1 - L2) / (0.5 * (L1 + L2))) / 3             # Davis-Haltiwanger arc growth /3
    d["g_emp_cagr"] = 100 * ((L1 / L2) ** (1 / 3) - 1)
    d["lnlp_level"] = np.log(S1 / L1)                                       # ln(sales per permanent FT employee), LCU - not comparable across countries
    # ---- D3 social composition
    l5, l5a, l5b = n("l5"), n("l5a"), n("l5b")
    fem = l5.copy()
    routeB = l5a + l5b
    fem = fem.where(fem.notna(), routeB)
    d["female_n"] = fem
    d["female_share"] = (fem / L1).where(fem <= L1)                          # share of permanent FT employees (x1 scale 0-1)
    d["female_route"] = np.where(l5.notna(), "l5", np.where(routeB.notna(), "l5a+l5b", ""))
    l4a1, l4a2, l4b = n("l4a1"), n("l4a2"), n("l4b")
    prod = (l4a1 + l4a2 + l4b)
    d["prod_n"] = prod
    d["lowskill_prod_share"] = (l4b / prod).where(prod > 0)                 # low-skilled among PRODUCTION workers only
    d["skilled_prod_share"] = (l4a1 / prod).where(prod > 0)
    d["prod_share_emp"] = (prod / L1).where(prod <= L1)
    d["lowskill_total_share"] = (l4b / L1).where(prod <= L1)                # low-skilled production / all permanent FT (lower bound)
    d["hs_share"] = n("l9b") / 100                                          # % FT workers completed high school
    d["hs_share_alt"] = d["hs_share"].where(d["hs_share"].notna(), n("l9b1") / L1)   # number/l1 (denominator assumed = l1)
    d["female_top_mgr"] = yn(raw, "b7a")
    # ---- explanatory: innovation & digitalization
    d["prod_innov"] = yn(raw, "h1"); d["proc_innov"] = yn(raw, "h5"); d["rd_spend"] = yn(raw, "h8")
    d["any_innov"] = np.where(d.prod_innov.isna() | d.proc_innov.isna(), np.nan, ((d.prod_innov + d.proc_innov) > 0).astype(float))
    d["web"] = yn(raw, "c22b")
    j36, j37 = n("j36"), n("j37")
    d["etax_file"] = j36.map({1: 1.0, 2: 1.0, 3: 0.0}); d["etax_pay"] = j37.map({1: 1.0, 2: 1.0, 3: 0.0})
    d["epay_recv_share"] = n("k33"); d["epay_made_share"] = n("k38")
    d["epay_any"] = np.where(d.epay_recv_share.isna() | d.epay_made_share.isna(), np.nan, ((d.epay_recv_share > 0) | (d.epay_made_share > 0)).astype(float))
    # ---- D4 environmental practice items (practice adoption, NOT outcomes such as emissions)
    d["env_energy_mgmt"] = yn(raw, "ge8d"); d["env_co2_monitor"] = yn(raw, "ge7"); d["weather_damage"] = yn(raw, "ge3")
    # ---- controls
    d["ln_size_init"] = np.log(L2); d["ln_size_cur"] = np.log(L1)
    age = raw["a14y"] - n("b5")
    d["age"] = age; d["ln_age"] = np.log1p(age)
    b2b = n("b2b"); d["foreign_own"] = (b2b >= 10).astype(float).where(b2b.notna())
    e1, e2 = n("d3b"), n("d3c"); es = e1 + e2
    d["exporter"] = np.where(es.notna(), (es >= 10).astype(float), np.where((e1 >= 10) | (e2 >= 10), 1.0, np.nan))
    d["corporation"] = raw["b1"].map({1: 1.0, 2: 1.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0})
    d["credit_access"] = pd.to_numeric(raw["k82"], errors="coerce").map({1: 1.0, 2: 1.0, 3: 1.0, 4: 0.0})
    d["mgr_exp"] = n("b7")
    d["size_class_init"] = pd.cut(L2, [0, 19, 99, np.inf], labels=["Small (<20)", "Medium (20-99)", "Large (100+)"])
    d["size_class_cur"] = pd.cut(L1, [0, 19, 99, np.inf], labels=["Small (<20)", "Medium (20-99)", "Large (100+)"])
    d["sampling_size"] = raw["a6a"]
    d["isic4_div"] = pd.to_numeric(raw["d1a2_v4"], errors="coerce") // 100
    d["Korea"] = float(c == "KOR")
    return d

def build_all():
    return pd.concat([build_country(c) for c in FILES], ignore_index=True)

if __name__ == "__main__":
    x = build_all()
    print(x.groupby("country")[["g_sales", "g_emp", "female_share", "prod_innov", "proc_innov", "web", "env_energy_mgmt"]].describe().T.to_string()[:3000])


# ------------------------------------------------------------------------------------------------------------------
# PRE-SPECIFIED model components (fixed BEFORE estimation; see 05_run_regressions / README)
# ------------------------------------------------------------------------------------------------------------------
X_MAIN = ["prod_innov", "proc_innov", "web"]                    # product innovation, process innovation, digitalization proxy (website)
SECTOR_DUMMIES = ["sec_Retail", "sec_Other services"]           # base = Manufacturing
CTRL_GROWTH = ["ln_size_init", "ln_age", "foreign_own", "exporter", "corporation"] + SECTOR_DUMMIES
CTRL_LEVEL = ["ln_size_cur", "ln_age", "foreign_own", "exporter", "corporation"] + SECTOR_DUMMIES
CTRL_EXTRA = ["credit_access", "female_top_mgr"]                # added in 'extended controls' robustness
# outcome key -> (column, estimator, control set, dimension, label)
OUTCOMES = {
    "D1_sales":    ("g_sales", "ols", "growth", "D1 Economic growth", "Sales growth (annualised log, pp)"),
    "D1_lp":       ("g_lp", "ols", "growth", "D1 Economic growth", "Labour-productivity growth (annualised log, pp)"),
    "D2_emp":      ("g_emp", "ols", "growth", "D2 Employment growth", "Employment growth (annualised log, pp)"),
    "D3_female":   ("female_share", "ols", "level", "D3 Social inclusion", "Female share of permanent FT employees"),
    "D3_lowskill": ("lowskill_prod_share", "ols", "level", "D3 Social inclusion", "Low-skilled share of production workers"),
    "D4_energy":   ("env_energy_mgmt", "logit", "level", "D4 Environmental practice", "Adopted energy-management measures (ge8d)"),
    "D4_co2":      ("env_co2_monitor", "logit", "level", "D4 Environmental practice", "Monitors CO2 emissions (ge7)"),
}

def add_dummies(d):
    d = d.copy()
    for s in ["Retail", "Other services"]:
        d["sec_" + s] = (d["sector3"] == s).astype(float).where(d["sector3"].notna())
    return d

def analytic():
    return add_dummies(build_all())

def controls(kind, extended=False):
    return (CTRL_GROWTH if kind == "growth" else CTRL_LEVEL) + (CTRL_EXTRA if extended else [])
