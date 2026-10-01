# -*- coding: utf-8 -*-
"""Shared logic: relationship catalogue, tag parsing, evidence aggregation, block statistics."""
from collections import defaultdict, OrderedDict
from data import F, ART, BLOCKS

REL = OrderedDict([
 # --- relationships requested by the user
 ("R1",  "Sensing -> Information quality"),
 ("R2",  "Sensing -> Predictive capability"),
 ("R3",  "Sensing -> Automation (adoption/use)"),
 ("R4",  "Sensing -> Planning (budgeting, forecasting)"),
 ("R5",  "Sensing -> Cybernetic control (performance measurement, MC effectiveness)"),
 ("R6",  "Sensing -> Controller role"),
 ("R7",  "Sensing -> Performance"),
 ("R8",  "Information quality -> Control effectiveness"),
 ("R9",  "Information quality -> Decision making"),
 ("R10", "Controller role -> Strategic involvement"),
 ("R11", "Controller role -> Decision support"),
 ("R12", "Controller role -> Interaction"),
 ("R13", "Controller role -> Performance"),
 ("R14", "Interaction -> Interpretation"),
 ("R15", "Interpretation -> Decision making"),
 ("R16", "Decision making -> Organisational action"),
 ("R17", "Organisational adaptation -> Performance"),
 ("R18", "Conditions -> AI/digital adoption"),
 ("R19", "Conditions -> Controller effectiveness"),
 ("R20", "Conditions -> Organisational translation"),
 # --- relationships that emerge from the findings (not in the user's list)
 ("E1",  "Automation -> effectiveness / workload release"),
 ("E2",  "Data volume / KPI overload -> worse outcomes (and AI as filter)"),
 ("E3",  "MCS use (interactive, beliefs) -> digital capability / innovation [reverse arrow]"),
 ("E4",  "Digitalisation -> administrative control (standardisation, process integration)"),
 ("E5",  "Digitalisation -> role strain / identity / boundary work of accountants"),
 ("E6",  "Digitalisation -> need for interpretation / contextualisation of data"),
 ("E7",  "Controller/BP orientation -> digital tool use [reverse arrow]"),
 ("E8",  "MA/MC practice quality (planning, MAS, budgeting satisfaction) -> performance/benefits"),
 ("E9",  "Digitalisation -> MA/MC tasks, instruments and practice adoption"),
 ("E10", "Digitalisation -> organisation/structure of the control function"),
 ("E11", "Digital forecasting maturity -> counter-measure effectiveness (organisational action)"),
 ("E12", "Information quality (not time saved) -> controller strategic involvement"),
 ("E13", "Conditions as moderators of digitalisation effects"),
])
COND = OrderedDict([
 ("C_TM",   "Top management support / leadership"),
 ("C_RES",  "Resources (financial, HR, time)"),
 ("C_COMP", "Competences / skills / self-efficacy"),
 ("C_CULT", "Culture / belief systems / resistance"),
 ("C_INST", "Institutional / coercive pressure"),
 ("C_SME",  "SME context / firm size"),
 ("C_OWN",  "Ownership / family control / structure"),
 ("C_TAM",  "Technology-acceptance constructs (usefulness, ease)"),
])
ALLREL = OrderedDict(list(REL.items()) + list(COND.items()))
MODE_NAME = {"Q": "quant", "D": "descriptive", "L": "qual", "U": "unverified"}


def parse(tag):
    rel, stance, mode = tag.split(".")
    assert rel in ALLREL, tag
    assert stance in ("S", "S~", "N", "X"), tag
    assert mode in MODE_NAME, tag
    return rel, stance, mode

for i, x in enumerate(F, 1):
    x["id"] = "F%02d" % i
    x["parsed"] = [parse(t) for t in x["tags"]]


def evidence():
    """rel -> dict(stance/mode -> list of (art, short, fid))"""
    out = defaultdict(lambda: defaultdict(list))
    for x in F:
        for rel, st, mode in x["parsed"]:
            out[rel][(st, mode)].append((x["art"], x["short"], x["id"]))
    return out


def arts(items):
    return sorted({a for a, _, _ in items}, key=lambda s: int(s[1:]))


def rel_row(rel, ev):
    e = ev.get(rel, {})
    def collect(pred):
        return [it for (st, m), lst in e.items() if pred(st, m) for it in lst]
    supQ = collect(lambda s, m: s == "S" and m in ("Q",))
    supD = collect(lambda s, m: s == "S" and m == "D")
    supL = collect(lambda s, m: s == "S" and m == "L")
    indQ = collect(lambda s, m: s == "S~" and m in ("Q", "D"))
    indL = collect(lambda s, m: s == "S~" and m == "L")
    unv = collect(lambda s, m: m == "U")
    nul = collect(lambda s, m: s in ("N", "X") and m != "U")
    return dict(supQ=supQ, supD=supD, supL=supL, indQ=indQ, indL=indL, unv=unv, nul=nul)


def fmt(items, limit=None):
    seen, out = set(), []
    for a, s, _ in items:
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
    return "; ".join(out) if out else "-"


# ------------------------------------------------------------ block statistics
def block_stats():
    stats = {}
    for bi, b in enumerate(BLOCKS):
        arts_q, arts_l, arts_all, n1, nh = set(), set(), set(), 0, 0
        for x in F:
            v = x["codes"][bi]
            if v >= 1:
                n1 += 1
                arts_all.add(x["art"])
                (arts_q if ART[x["art"]]["d"] in ("Q", "M") else arts_l).add(x["art"])
            elif v >= 0.5:
                nh += 1
        stats[b] = dict(f1=n1, fh=nh, aq=sorted(arts_q, key=lambda s: int(s[1:])), al=sorted(arts_l, key=lambda s: int(s[1:])))
    return stats

if __name__ == "__main__":
    ev = evidence()
    print("== RELATIONSHIPS (distinct articles) ==")
    for r in ALLREL:
        row = rel_row(r, ev)
        sq = arts(row["supQ"] + row["supD"]); sl = arts(row["supL"])
        iq = arts(row["indQ"] + row["indL"]); nu = arts(row["nul"]); un = arts(row["unv"])
        print(f"{r:7s} Q/D:{len(sq)} {sq} | L:{len(sl)} {sl} | ind:{iq} | null:{nu} | unv:{un}")
    print("\n== BLOCK STATS (findings coded 1; articles) ==")
    for b, s in block_stats().items():
        print(f"{b:16s} F1={s['f1']:3d} F.5={s['fh']:3d} | quant arts={len(s['aq']):2d} {s['aq']} | qual arts={len(s['al']):2d} {s['al']}")
