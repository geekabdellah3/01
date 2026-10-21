"""Shared paths, constants and loaders for the MCS_G7 project (all scripts import this)."""
import os, sys, json, logging, datetime
import numpy as np, pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW = os.path.join(ROOT, "01_DATA/raw/WBES_G7_2024_2025_merged.csv")
PROC = os.path.join(ROOT, "01_DATA/processed")
META = os.path.join(ROOT, "01_DATA/metadata")
RES = os.path.join(ROOT, "03_RESULTS")
FIG = os.path.join(ROOT, "04_FIGURES/publication_ready")
SEED = 20260101
sys.path.insert(0, os.path.join(ROOT, "02_SCRIPTS/lca"))

CMAP = {"Canada": "CAN", "France": "FRA", "Germany": "DEU", "Italy": "ITA",
        "Japan": "JPN", "United-Kingdom": "GBR", "United-States": "USA"}
CORDER = ["CAN", "FRA", "DEU", "ITA", "JPN", "GBR", "USA"]
R = [f"r{i}" for i in range(1, 12)]

def log(msg):
    line = f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    print(line, flush=True)
    with open(os.path.join(ROOT, "07_REPRODUCIBILITY/execution_log.txt"), "a") as f:
        f.write(line + "\n")

def load_raw():
    df = pd.read_csv(RAW, low_memory=False).copy()
    df.insert(0, "cid", df["source_country"].map(CMAP))
    return df

def load_analytic():
    return pd.read_csv(os.path.join(PROC, "mcs_analytic.csv"))
