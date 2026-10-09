"""Phase 3 - variable crosswalk (Morocco 2023 vs South Korea 2024) -> outputs/03_VARIABLE_CROSSWALK.xlsx

Two compatibility classes are reported for every construct:
  class_cross_country : can MAR and KOR be compared/pooled?   (A exact, B harmonizable, C proxy only, D not comparable, E unavailable)
  class_vs_article    : how faithfully does the construct replicate the SOURCE ARTICLE's variable?  (same scale)
Only constructs with class_cross_country in {A,B} enter pooled models; C is used only as clearly labelled proxies/robustness;
D and E are NOT used (listed for transparency).  Labels, response categories and valid N are read from the data, not typed.
"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from common import *
from build import build_all

spec = importlib.util.spec_from_file_location("ext", os.path.join(os.path.dirname(os.path.abspath(__file__)), "01_extract_articles.py"))
ext = importlib.util.module_from_spec(spec); spec.loader.exec_module(ext)
P = ext.P

D = {c: load(c) for c in FILES}
B = build_all()

def lab(c, v):
    if v in (None, "", "-"): return "(absent)"
    df, m = D[c]
    return m.column_names_to_labels.get(v, "(absent)") if v in df.columns else "(absent)"

def cats(c, v):
    if v in (None, "", "-"): return "(absent)"
    df, m = D[c]
    if v not in df.columns: return "(absent)"
    vl = m.variable_value_labels.get(v)
    return "; ".join(f"{k}={t}" for k, t in vl.items()) if vl else "numeric / free entry"

def nvalid(col, c):
    if col is None: return None
    return int(B.loc[B.country == c, col].notna().sum())

rows = []
def row(construct, dim, article, orig_def, mar, kor, derived, transform, missing, cls, cls_art, why, use, comparable):
    mv = mar.split("+")[0] if mar else None; kv = kor.split("+")[0] if kor else None
    rows.append(dict(construct=construct, dimension=dim, article_source=article, original_definition=orig_def,
                     MAR_variable=mar, KOR_variable=kor, MAR_label=lab("MAR", mv), KOR_label=lab("KOR", kv),
                     MAR_response_categories=cats("MAR", mv), KOR_response_categories=cats("KOR", kv),
                     derived_column=derived, proposed_transformation=transform, missing_data_treatment=missing,
                     comparable_across_countries=comparable, class_cross_country=cls, class_vs_article=cls_art,
                     justification_limitations=why, role_in_study=use,
                     n_valid_MAR=nvalid(derived, "MAR") if derived else None, n_valid_KOR=nvalid(derived, "KOR") if derived else None))

MISS_YN = "Yes=1, No=0; DK(-9)/refused -> missing (listwise in main models; DK-as-category in sensitivity)"
MISS_NUM = "Negative special codes -> missing; never recoded to 0"

# ---------------- explanatory variables
row("Product innovation", "Explanatory", f"Phan (2026) PRODUCT = h1 ({P('PHAN','Table 1 Variable description')}); Sime & Tadesse (2025) new product item h1 ({P('SIME','one of the indicators of innovation, h1 (new product)')})",
    "Firm introduced new or significantly improved products/services in last 3 years", "h1", "h1", "prod_innov", "1 if h1=Yes", MISS_YN, "A", "A",
    "Identical code, label, categories and 3-year reference period in both files; Phan prints the same code h1.", "Main regressor", "Yes")
row("Process innovation", "Explanatory", f"Phan (2026) PROCESS = h5 ({P('PHAN','Table 1 Variable description')})",
    "Firm introduced new or significantly improved production/service-delivery process in last 3 years", "h5", "h5", "proc_innov", "1 if h5=Yes", MISS_YN, "A", "A",
    "Identical code and label; Phan prints h5. Note: Korea has few process innovators (about 3%), limiting power.", "Main regressor", "Yes")
row("R&D spending (any)", "Explanatory/robustness", f"Sime & Tadesse (2025) R&D innovation ({P('SIME','R&D innovation looks at employee time spent')}); Adewumi & Zhang (2026) rd_std instrument ({P('ADEW','region-standardized R&D intensity instrument')})",
    "Spent on R&D (excl. market research) in last fiscal year", "h8", "h8", "rd_spend", "1 if h8=Yes", MISS_YN, "A", "C",
    "Binary item identical across files. Articles use R&D intensity/time and, for Adewumi & Zhang, a region-standardised amount used as an instrument: not replicated.", "Robustness only", "Yes")
row("R&D expenditure amount", "Explanatory", f"Adewumi & Zhang (2026) rd_std ({P('ADEW','region-standardized R&D intensity instrument')})",
    "Amount spent on R&D", "h9", "h9", None, "None", "-", "D", "E",
    "Amount in local currency units (MAD vs KRW); only 45 (MAR) / 173 (KOR) valid positive amounts among the firms that report R&D (25 MAR / 23 KOR answered DK). Not comparable and not used.", "Not used", "No")
row("Digitalization proxy 1: own website", "Explanatory", f"Sime & Tadesse (2025) own_web ({P('SIME','Possible covariate variables')})",
    "Establishment has its own website", "c22b", "c22b", "web", "1 if Yes", MISS_YN, "A", "C",
    "Same wording and coding. A website is a weak proxy for digital technology adoption/digital transformation (no information on ERP, automation, cloud, etc.). Sime & Tadesse use it only as a covariate.", "Main regressor (digitalization proxy)", "Yes")
row("Digitalization proxy 2: e-filing of taxes", "Explanatory/robustness", "None (own proposal)",
    "Filed taxes electronically in last FY (fully / partially / no)", "j36", "j36", "etax_file", "1 if fully or partially; 0 if No", MISS_YN + " (DK -> missing)", "B", "E",
    "Identical question, but e-filing may be mandated (Korea median = 'fully', Morocco median = 'no'): reflects government e-services as much as firm digital capability. Robustness proxy only.", "Robustness only", "Partial")
row("Digitalization proxy 3: share of payments received electronically", "Explanatory/robustness", "None (own proposal)",
    "% of payments received via e-payments", "k33", "k33", "epay_recv_share", "Continuous 0-100", "Special codes -> missing (51% DK in Morocco)", "C", "E",
    "Identical wording but 51% DK in Morocco (vs 2% in Korea) -> differential non-response; usable only on a small, self-selected Morocco subsample. Proxy only; excluded from pooled main models.", "Not used in main models", "Partial")
row("Digitalization (technology adoption, ICT use, e-commerce, automation)", "Explanatory", "Task brief (Digitalization_i)",
    "Digital technology adoption / ICT intensity", None, None, None, "-", "-", "E", "E",
    "No item on e-mail, software, ERP, cloud, automation, online sales or digital skills in either file (only website, e-payments, e-tax, broadband connection/disruption items).", "Not available", "No")
# ---------------- D1 / D2
row("Sales growth (3-year, annualised log)", "D1 Economic growth", f"Adewumi & Zhang (2026) sales growth ({P('ADEW','Sales growth is expressed as the proportional change in sales over the past three years')})",
    "(S_t - S_t-3)/S_t", "d2 + n3", "d2 + n3", "g_sales_raw", "100*ln(d2/n3)/3 (winsorised 1/99 within country = g_sales); alt: (S_t-S_t-3)/S_t", "Require d2>0 and n3>0; -9, -7 (not in business) -> missing", "B", "B",
    "Same items in both files. Nominal LCU growth; window FY2019->FY2022 (MAR, fiscal-year close 2022 for 90%) vs FY2020->FY2023 (KOR); no deflator in data (country-wide inflation enters the country intercept only because growth is in logs). Korea has unit-entry outliers (ratio up to 10,500x) -> winsorising + trimming sensitivity. Authors' own formula computed as g_sales_adew for comparison.", "Main outcome", "Yes (with caveats)")
row("Real sales growth", "D1 Economic growth", "Task brief", "Sales growth deflated by sector/country price index", None, None, None, "-", "-", "E", "E",
    "No sector deflator in either dataset and none is invented. Common country-level deflation would change only the country intercept of log growth, not slopes, provided fiscal-year timing is common within a country.", "Not available (see note)", "No")
row("Labour productivity growth", "D1 Economic growth", f"Sime & Tadesse (2025) labour productivity = sales/employment ({P('SIME','Computed productivity from employment and sales')})",
    "Total annual sales / number of employees", "d2+n3+l1+l2", "d2+n3+l1+l2", "g_lp_raw", "g_lp = g_sales - g_emp (exact identity of dln(S/L)); winsorised 1/99", MISS_NUM, "B", "B",
    "Sales per permanent full-time employee, not value added; shares the sales/employment components of D1 and D2, so models are not independent. Productivity LEVEL (lnlp_level) is in MAD vs KRW and not pooled.", "Main outcome", "Yes (growth); No (level)")
row("Employment growth (3-year, annualised log)", "D2 Employment growth", f"Sime & Tadesse (2025) employment ({P('SIME','Variable choice and definitions')}); Phan (2026) SIZE = ln(l1)",
    "Number of permanent full-time employees", "l1 + l2", "l1 + l2", "g_emp_raw", "100*ln(l1/l2)/3 (winsorised); alt: DHS arc growth, CAGR", "Require l1>0, l2>0; l2=-7 (not in business 3y ago: 11 MAR, 40 KOR) excluded", "B", "C",
    "Permanent full-time employees only (temporary workers not observed 3 years ago). Sample = surviving firms. Sime & Tadesse analyse employment LEVELS by category; we analyse growth in total.", "Main outcome", "Yes")
row("Employment growth by worker category (female / skilled / low-skilled / production)", "D2/D3", "Task brief; Sime & Tadesse (2025) disaggregate levels only",
    "Employment growth by category", None, None, None, "-", "-", "E", "E",
    "l2 (employment 3 years ago) exists only for total permanent full-time employment; category composition is observed only at the last fiscal year, so category-specific growth cannot be measured.", "Not available", "No")
# ---------------- D3
row("Female employment share", "D3 Social inclusion", "Task brief (no source article estimates it)",
    "Female full-time employees / permanent full-time employees", "l5 | l5a+l5b", "l5 | l5a+l5b", "female_share", "female_n / l1 where female_n = l5, or l5a+l5b when l5 not asked (split-sample routes)", "Both routes are random halves of the sample (structural missingness); DK -> missing", "B", "E",
    "Level share at one point in time. NOT growth of female employment. Denominator l1 equals l3a+l3b in all checked cases. Two questionnaire routes pooled; Morocco n=462, route-specific robustness provided.", "Main outcome (composition)", "Yes")
row("Female employment growth", "D3 Social inclusion", "Task brief", "Change in female employment", None, None, None, "-", "-", "E", "E",
    "Female employment observed only for the last fiscal year; growth cannot be measured.", "Not available", "No")
row("Low-skilled share of production workers", "D3 Social inclusion", f"Phan (2026) SKILL uses l4a1, l4a2, l4b ({P('PHAN','Table 1 Variable description')})",
    "Low-skilled production workers / (skilled+semi-skilled+low-skilled production workers)", "l4a1+l4a2+l4b", "l4a1+l4a2+l4b", "lowskill_prod_share", "l4b/(l4a1+l4a2+l4b)", "Any component DK (-9) -> missing (22% of Morocco, 2% of Korea)", "B", "B",
    "Skill categories exist for PRODUCTION workers only (sum equals l3a in 100% of checked cases); non-production workers' skills unobserved. Higher share is a composition fact, not necessarily 'more inclusive'. Morocco DK 22% -> selection risk.", "Main outcome (composition)", "Yes")
row("Skilled share of production workers (Phan SKILL)", "Control/D3", f"Phan (2026) SKILL ({P('PHAN','Table 1 Variable description')})",
    "Skilled / (skilled+semi+unskilled)", "l4a1", "l4a1", "skilled_prod_share", "l4a1/(l4a1+l4a2+l4b)", MISS_NUM, "B", "A",
    "Phan's text says 'ratio of skilled workers to total employment' but prints only production-worker items; we reproduce the printed items. Reciprocal complement of low-skilled share only partly (semi-skilled in between).", "Robustness", "Yes")
row("Production-worker share of employment", "D3 Social inclusion", "Sime & Tadesse (2025) production vs non-production workers",
    "Production workers / permanent FT employees", "l3a|l4*", "l3a|l4*", "prod_share_emp", "(l4a1+l4a2+l4b)/l1", MISS_NUM, "B", "C", "Level at last FY only; descriptive.", "Descriptive", "Yes")
row("Workforce education: share with completed high school", "D3 Social inclusion/control", f"Adewumi & Zhang (2026) Education index with edu1 (secondary) and edu2 (university) ({P('ADEW','we assigned a weight of 0.5 to secondary education')})",
    "% of full-time workers who completed high school", "l9b (l9b1 = number)", "l9b (l9b1 = number)", "hs_share", "l9b/100", "Two routes (percent or number); only percent route used in main (number route as alternative)", "C", "C",
    "No university-share item -> the Adewumi & Zhang education index (0.5*secondary + 1*university) cannot be built. Korea is at ceiling (mean 98%, median 100%): almost no variation to identify effects; Morocco mean ~41%. Not pooled as an outcome; descriptive/Morocco-only.", "Descriptive / Morocco exploratory", "Partial")
row("University-educated workforce share", "D3", f"Adewumi & Zhang (2026) edu2 ({P('ADEW','we assigned a weight of 0.5 to secondary education')})", "Share with university degree", None, None, None, "-", "-", "E", "E",
    "No such item in either file.", "Not available", "No")
row("Formal training", "H/control", f"Sime & Tadesse (2025) training_pfemp ({P('SIME','Possible covariate variables')})", "Formal training programme for permanent FT employees", "l10", "l10", None, "1 if Yes", MISS_YN, "A", "B",
    "Identical coding; mapping to the article's training_pfemp is by label (the article prints no WBES code). Not used (post-treatment mediator candidate).", "Not used", "Yes")
# ---------------- D4
row("Green Economy Practices index (10 items)", "D4 Environmental", f"Phan (2026) GEP1-GEP10 = BMGc23a-j ({P('PHAN','Table 1 Variable description')}); Adewumi & Zhang (2026) GI count ({P('ADEW','ecofriendly investments over the past three years')})",
    "Count of ten green practices adopted", "BMGc23a-j", "BMGc23a-j", None, "-", "-", "E", "E",
    "Variables BMGc23a-j (and any ten-item green-investment module) are ABSENT from both files; only ge3, ge7, ge8d exist. Phan's GEP index and Adewumi & Zhang's GI score cannot be reproduced.", "Not available", "No")
row("Energy management measures adopted (3 years)", "D4 Environmental", f"Phan (2026) GEP4 'Energy management systems' = BMGc23d ({P('PHAN','Table 1 Variable description')}) [equivalence inferred from suffix/ordering, NOT verifiable without the questionnaire]",
    "Over last 3 years establishment adopted energy management measures", "ge8d", "ge8d", "env_energy_mgmt", "1 if Yes", MISS_YN + "; -7 (not in business) -> missing", "A", "C",
    "Identical variable and wording in both files, so cross-country comparison is sound; it is ONE practice-adoption item, not an index, and not a sustainability OUTCOME (no emissions, energy use or efficiency measured).", "D4 outcome (practice adoption)", "Yes")
row("Monitors CO2 emissions (3 years)", "D4 Environmental", "None", "Over last 3 years establishment monitored its CO2 emissions", "ge7", "ge7", "env_co2_monitor", "1 if Yes", MISS_YN, "A", "E",
    "Identical in both files; a management-practice indicator, not an environmental outcome.", "D4 outcome (practice adoption)", "Yes")
row("Extreme-weather damage to assets", "D4 Environmental", "None", "Experienced damage of physical assets due to extreme weather", "ge3", "ge3", "weather_damage", "1 if Yes", MISS_YN, "A", "E",
    "Exposure to climate shocks, not environmental performance; descriptive only.", "Descriptive", "Yes")
row("Environmental investment / energy efficiency / waste management", "D4 Environmental", "Task brief", "Investment in energy efficiency, waste, etc.", "n2b, c32 (electricity cost/use only)", "n2b, c32", None, "-", "-", "D", "E",
    "No environmental-investment or waste items. Electricity cost (n2b, currency units) and consumption (c32, kWh) mix price and quantity and cover electricity only: they do not measure energy efficiency. Not used.", "Not used", "No")
# ---------------- controls
row("Firm size (initial / current)", "Control", f"Phan (2026) SIZE = ln(l1) ({P('PHAN','Table 1 Variable description')})", "ln(permanent FT employees)", "l1, l2", "l1, l2", "ln_size_init", "ln(l2) for growth models (avoids mechanical size-growth correlation); ln(l1) for composition models", MISS_NUM, "A", "B",
    "Same items. Phan uses current ln(l1); we use initial size in growth models (documented deviation). Source files use different sampling-size classes (3 vs 4), so size classes are rebuilt from l1/l2 (<20, 20-99, 100+).", "Control", "Yes")
row("Firm age", "Control", f"Phan (2026) AGE = ln(years) ({P('PHAN','Table 1 Variable description')}); Adewumi & Zhang ln firm age", "ln(1 + survey year - year began operations)", "b5, a14y", "b5, a14y", "ln_age", "ln(1+(a14y-b5))", MISS_NUM, "A", "B", "Phan uses ln(years) (a14y; b5); ln(1+age) used to keep age 0.", "Control", "Yes")
row("Foreign ownership", "Control", f"Phan (2026) FO (b2b %) ({P('PHAN','Table 1 Variable description')}); Adewumi & Zhang dummy", "% owned by foreign individuals/companies", "b2b", "b2b", "foreign_own", "1 if b2b>=10", MISS_NUM, "A", "B", "Phan uses % ; we use the standard 10% threshold dummy.", "Control", "Yes")
row("Exporter", "Control", f"Adewumi & Zhang (2026) exporter ({P('ADEW','Measurement details of all variables')})", "Direct + indirect export share of sales >= 10%", "d3b+d3c", "d3b+d3c", "exporter", "1 if d3b+d3c>=10", "If either component DK, exporter=1 only if the known one >=10", "A", "B", "Authors' exporter definition not printed; 10% convention used.", "Control", "Yes")
row("Corporation (legal form)", "Control", "Adewumi & Zhang (2026) firm legal status", "Shareholding company vs sole proprietorship/partnership", "b1", "b1", "corporation", "1 if b1 in {1,2}", "-", "A", "B", "Category definitions identical in both files; collapsed to corporation vs other.", "Control", "Yes")
row("Credit access (loan or line of credit)", "Control", f"Phan (2026) DEBT = k8 ({P('PHAN','Table 1 Variable description')})", "Has a line of credit or loan from a financial institution", "k82", "k82", "credit_access", "1 if k82 in {1,2,3}", MISS_NUM, "A", "B", "Phan cites code k8; the files carry k82 with a matching label (code drift across waves: not assumed identical).", "Control", "Yes")
row("Checking/savings account", "Control", f"Phan (2026) CFL = k6 ({P('PHAN','Table 1 Variable description')})", "Has a checking and/or savings account", "k6", "k6", None, "-", "-", "A", "A", "Nearly universal; low variance; not used.", "Not used", "Yes")
row("Large-shareholder ownership", "Control", f"Phan (2026) LARGE = b3 ({P('PHAN','Table 1 Variable description')})", "% owned by large owners", "b3a (different item)", "b3a (different item)", None, "-", "-", "D", "E", "In these files b3a = 'largest owner is also top manager' - NOT the item Phan describes. Not used.", "Not used", "No")
row("Female top manager", "Control", "None", "Top manager is female", "b7a", "b7a", "female_top_mgr", "1 if Yes", MISS_YN, "A", "E", "Same item in both files; included in extended-control robustness.", "Robustness control", "Yes")
row("Sector (harmonised 3 groups)", "Control/heterogeneity", "Phan (2026) industry FE; Adewumi & Zhang sector", "Sampling sector", "a4a (5 categories)", "a4a (10 categories)", "sector3", "Manufacturing / Retail / Other services (Korea construction, professional, other services -> Other services)", "-", "B", "B",
    "Different sector schemes (Morocco: Food, Garments, Other mfg, Retail, Other services; Korea: 6 manufacturing groups, Retail, Construction, Professional activities, Other services): only the 3-group aggregate is comparable. ISIC rev.4 division from d1a2_v4 used as a sensitivity.", "Control / heterogeneity", "Yes (aggregated)")
row("Sampling region", "Control", "Phan (2026) country FE", "Sampling region (a2)", "a2 (4 regions)", "a2 (10 regions)", None, "Country-specific region FE only", "-", "D", "E", "Regional classifications are country-specific; not comparable.", "Within-country FE only", "No")
row("Survey weights and strata", "Design", "None (WBES design); Phan (2026) does not report weights", "wstrict / wmedian / wweak; strata", "wstrict, strata", "wstrict, strata", "w_strict_std", "Weights rescaled to mean 1 within country; stratified linearised variance (strata=strata; no PSU variable)", "-", "A", "E",
    "Identical variables. No cluster/PSU variable in the files; firm treated as its own PSU. 14 (MAR) and 46 (KOR) single-firm strata handled by centred lonely-PSU adjustment.", "Design", "Yes")

cw = pd.DataFrame(rows)
cw["pooled_models_allowed"] = np.where(cw.class_cross_country.isin(["A", "B"]) & cw.role_in_study.str.contains("Main|Control|Robustness|Design|Descriptive|D4", regex=True), "Yes", "No")
legend = pd.DataFrame({"class": list("ABCDE"), "meaning": ["EXACT MATCH", "HARMONIZABLE (documented transformation)", "PROXY ONLY (limitations explicit; never presented as exact replication)",
                                                                "NOT COMPARABLE (not used)", "UNAVAILABLE (not used)"]})
with pd.ExcelWriter(os.path.join(OUT, "03_VARIABLE_CROSSWALK.xlsx"), engine="openpyxl") as xw:
    legend.to_excel(xw, sheet_name="Legend", index=False)
    cw.to_excel(xw, sheet_name="Crosswalk", index=False)
    cw.groupby("class_cross_country").size().rename("n_constructs").reset_index().to_excel(xw, sheet_name="Class_counts", index=False)
log(f"03 crosswalk written: {len(cw)} constructs; class counts {cw.class_cross_country.value_counts().to_dict()}", "harmonization.log")
print(cw[["construct", "class_cross_country", "class_vs_article", "n_valid_MAR", "n_valid_KOR", "role_in_study"]].to_string())
