"""Inter-coder reliability for the MCS x DC x OIPT coding.

Usage: python kappa.py coder1_codes.csv coder2_codes.csv

Both files use the same long format: one row per code
(sentence_id, control, capability, face); a sentence may have several rows.
For each dimension, every (sentence, category) pair is scored as present/absent
for each coder, and Cohen's kappa is computed on these binary judgements
(pooled over categories, then per category). Only sentences coded by both
coders are compared over all sentences coded by either coder: a sentence left
uncoded by one coder counts as 'absent' for every category (a disagreement).
"""
import csv, sys
from collections import defaultdict

DIMS = {
    "control": ["Planning", "Cybernetic", "Administrative", "Cultural", "Reward", "Unspecified MC"],
    "capability": ["Sensing", "Seizing", "Transforming"],
    "face": ["IPC", "IPR"],
}

def load(path):
    codes = defaultdict(lambda: defaultdict(set))
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            sid = r["sentence_id"].strip()
            for d in DIMS:
                v = (r.get(d) or "").strip()
                if v:
                    codes[sid][d].add(v)
    return codes

def kappa(pairs):
    n = len(pairs)
    if n == 0:
        return float("nan")
    po = sum(a == b for a, b in pairs) / n
    pa, pb = sum(a for a, _ in pairs) / n, sum(b for _, b in pairs) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)

def main(f1, f2):
    c1, c2 = load(f1), load(f2)
    common = sorted(set(c1) | set(c2))
    only1, only2 = sorted(set(c1) - set(c2)), sorted(set(c2) - set(c1))
    print(f"Sentences compared: {len(common)} | coder 1 only: {len(only1)} | coder 2 only: {len(only2)}")
    for d, cats in DIMS.items():
        pooled = []
        per = {}
        for cat in cats:
            pairs = [(cat in c1[s][d], cat in c2[s][d]) for s in common]
            pooled += pairs
            per[cat] = kappa(pairs)
        exact = sum(c1[s][d] == c2[s][d] for s in common) / len(common) if common else float("nan")
        print(f"\n{d.upper()}: pooled kappa = {kappa(pooled):.3f} | exact agreement on label sets = {exact:.1%}")
        for cat, k in per.items():
            print(f"  {cat:15s} kappa = {k:.3f}")
    if only1:
        print("\nCoded by coder 1 only:", ", ".join(only1))
    if only2:
        print("Coded by coder 2 only:", ", ".join(only2))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
