#!/usr/bin/env bash
# Run from MCS_G7_RESEARCH/. Seeds fixed in 02_SCRIPTS/common.py (SEED=20260101). Approx. 45 min on one CPU.
set -e
S=02_SCRIPTS
python3 -I $S/audit/01_audit.py
python3 -I $S/harmonisation/02_build_analytic.py
python3 -I $S/eda/03_eda.py
python3 -I $S/lca/04_lca_select.py            # ~30 min
python3 -I $S/lca/05_profiles_gradient.py A 3 A 4 B 4
python3 -I $S/lca/06_outcomes_incremental.py
python3 -I $S/robustness/07_robustness.py     # ~12 min
python3 -I $S/dimensionality/08_dimensionality.py
python3 -I $S/nonlinear/09_nonlinear.py
python3 -I $S/audit/10_theory_matrices.py
python3 -I $S/audit/11_model_figure.py
python3 -I $S/robustness/12_crosscheck_stepmix.py
