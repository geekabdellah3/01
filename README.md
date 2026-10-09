# Innovation, Digitalization and Inclusive Firm Growth: Morocco (WBES 2023) vs South Korea (WBES 2024)

Reproducible Python project. `python run_all.py` runs everything (~2 min) and rebuilds `outputs/`, `results/`, `logs/`.

## Layout
| Path | Content |
|---|---|
| `data/raw/` | Original WBES `.dta` files and the three source PDFs (never modified) |
| `data/processed/analytic_dataset.csv` | Derived indicators (built by `scripts/build.py`) |
| `scripts/01_extract_articles.py` | Article extraction; page numbers machine-verified against PDF text |
| `scripts/02_audit_datasets.py` | Dictionaries and missing-data report |
| `scripts/03_harmonize_variables.py` | Variable crosswalk (classes A-E) |
| `scripts/04_construct_indicators.py` | Indicators, sample flow, measurement decision (Strategy A/B/C) |
| `scripts/05_run_regressions.py` | Pre-specified Models 1-4 (`results/prespecification.json`) |
| `scripts/06_robustness.py` | Robustness checks R01-R12, diagnostics, exploratory (T3) analyses |
| `scripts/07_generate_tables.py`, `report_text.py` | Tables 1-10, figures, `07_RESEARCH_REPORT.md` |
| `scripts/svy.py`, `tests/test_svy.py` | Survey-design OLS/logit/Firth estimators and their validation |
| `outputs/` | Deliverables 01-07; `outputs/06_FIGURES/` figures |
| `logs/` | Every transformation, exclusion and data-quality rule applied |

## Requirements
Python 3.10+, packages in `requirements.txt` (pandas 3 syntax is used), and `pdftotext` (poppler) for script 01.

## Key conventions
* WBES special codes (-9, -8, -7, -6) are never recoded to 0. System-missing = question not asked.
* Growth outcomes = annualised log change x100 (pp/yr), nominal, winsorised 1/99 within country. Shares are 0-1.
* Weights `wstrict` (rescaled to mean 1 within country), stratified linearised SE (no PSU in the files).
* Results are associations; no causal claims; no 2SLS (no credible instrument).
* Korea `.dta` is read with `latin1` (not valid UTF-8).
