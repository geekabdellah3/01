"""Shared helpers: paths, loading, logging. Raw data is read-only."""
import os, json, datetime
import pandas as pd, pyreadstat
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
OUT = os.path.join(ROOT, "outputs")
LOGDIR = os.path.join(ROOT, "logs")
FILES = {"MAR": "Morocco-2023-full-data.dta", "KOR": "Korea-Republic-2024-full-data.dta"}
ENC = "latin1"   # Korea file is not valid UTF-8; latin1 reads all bytes (labels with Korean text may be garbled)
os.makedirs(OUT, exist_ok=True); os.makedirs(LOGDIR, exist_ok=True)

def load(c, formats=False):
    df, meta = pyreadstat.read_dta(os.path.join(RAW, FILES[c]), apply_value_formats=formats, encoding=ENC)
    return df, meta

def log(msg, fname="transformations.log"):
    with open(os.path.join(LOGDIR, fname), "a") as f:
        f.write(f"{datetime.datetime.now().isoformat(timespec='seconds')} | {msg}\n")
