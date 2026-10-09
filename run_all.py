"""Runs the full pipeline in order. Raw data are never modified. Usage: python run_all.py"""
import subprocess, sys, os, time
ROOT = os.path.dirname(os.path.abspath(__file__))
STEPS = ["tests/test_svy.py", "scripts/01_extract_articles.py", "scripts/02_audit_datasets.py", "scripts/03_harmonize_variables.py",
         "scripts/04_construct_indicators.py", "scripts/05_run_regressions.py", "scripts/06_robustness.py", "scripts/07_generate_tables.py"]
if os.path.isdir(os.path.join(ROOT, "logs")):
    for f in os.listdir(os.path.join(ROOT, "logs")):
        if f.endswith(".log"): os.remove(os.path.join(ROOT, "logs", f))      # logs are rebuilt on every run
for s in STEPS:
    t = time.time(); print(f"== {s}", flush=True)
    r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, s)], cwd=ROOT)
    if r.returncode: sys.exit(f"FAILED: {s}")
    print(f"   done in {time.time()-t:.0f}s", flush=True)
