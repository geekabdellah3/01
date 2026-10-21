"""Conceptual figure: empirically grounded model of observable management-control practices (4 layers).
Solid = statistical association/structure estimated in this study; dashed = theoretical relation NOT tested; no causal arrows."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(14, 10.5)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
C = dict(l1="#E8F1F8", l2="#FBF0DA", l3="#EFE6F2", l4="#E4F2EA", edge="#333333")
def band(y0, y1, col, title):
    ax.add_patch(FancyBboxPatch((0.5, y0), 99, y1 - y0, boxstyle="round,pad=0.2,rounding_size=1", fc=col, ec="none", zorder=0))
    ax.text(3.2, y1 - 1.3, title, fontsize=10.5, fontweight="bold", va="top", color="#222")
def box(x, y, w, h, txt, fc="white", fs=8.2, ls="-", bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15,rounding_size=0.8", fc=fc, ec=C["edge"], lw=1.1, ls=ls, zorder=2))
    ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=fs, zorder=3, fontweight="bold" if bold else "normal", linespacing=1.25)
def arrow(p, q, ls="-", txt=None, dx=0, dy=0, style="-", col="#333", rad=0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=11, lw=1.3, ls=ls, color=col, zorder=1, connectionstyle=f"arc3,rad={rad}"))
    if txt: ax.text((p[0] + q[0]) / 2 + dx, (p[1] + q[1]) / 2 + dy, txt, fontsize=7.2, ha="center", va="center", bbox=dict(fc="white", ec="none", pad=0.8, alpha=.9), zorder=4)
ax.text(50, 99.2, "Empirically grounded model of observable management-control practices (WBES, G7, 2024-2025)", ha="center", va="top", fontsize=13, fontweight="bold")
ax.text(50, 96.4, "Exploratory, cross-sectional, firms with the management module (n = 6,316; mostly 20+ employees). Associations only - no causal claims.", ha="center", va="top", fontsize=8.5, style="italic")
# Layer 1
band(72, 94.5, C["l1"], "LAYER 1 - Observable practices (WBES r1-r11)")
box(3, 75, 21, 14.5, "MONITORING\nr2  performance indicators tracked (y/n)\nr3  number of indicators (given r2)\nr1  reaction to production problems", fs=7.6)
box(27, 75, 21, 14.5, "TARGETS\nr4  targets exist (y/n)\nr5  time frame of targets (given r4)\nr6, r7  other target features\n(wording NOT verified)", fs=7.6)
box(51, 75, 21, 14.5, "INCENTIVES\nr8  bonuses tied to targets (y/n)\nr9  basis of bonuses (given r8)", fs=7.6)
box(75, 75, 22, 14.5, "PEOPLE-RELATED ITEMS\nr10, r11  (wording NOT verified;\nincl. 'does-not-apply' codes;\ncomparability across countries doubtful)", fs=7.6, ls="--")
arrow((24.3, 82), (26.7, 82), txt="V=.41\n(r2-r4)", dy=3.2, style="-", col="#0072B2"); arrow((48.3, 82), (50.7, 82), txt="V=.22-.27", dy=3.2, col="#0072B2"); arrow((72.3, 82), (74.7, 82), txt="V=.15-.26", dy=3.2, col="#0072B2")
# Layer 2
band(40, 70, C["l2"], "LAYER 2 - Empirical structure (statistically identified)")
box(3, 47, 30, 17, "ONE DOMINANT CONTINUOUS DIMENSION\n'breadth of formalised practice'\n\nParallel analysis retains 1 factor (6 items:\neigenvalue 2.54 vs 1.09)\nMarginal reliability of the trait = 0.60\nTucker congruence across countries .93-.99", fc="#FFF9EC", fs=7.8, bold=False)
box(36, 47, 30, 17, "DISCRETE PROFILES: WEAK\nLCA entropy .53-.60 (spec A, K=3-4); min. AvePP .64-.70\nBIC flat for K = 3-5; class order = gradient (K=3)\nK=4: small class (5-7%) with targets but fewer\nbonuses - unstable across subsamples", fc="#FFF9EC", fs=7.8)
box(69, 47, 28, 17, "COMBINATIONS\nAll-three gates present: 43% (1.35x expected)\nNone present: 10% (3.7x expected)\nMost partial combinations rarer than expected\nCountry composition differs (e.g. none: ITA 27%)\nSome items non-invariant across countries", fc="#FFF9EC", fs=7.8)
arrow((18, 74.8), (18, 64.3), col="#0072B2")
arrow((51, 74.8), (51, 64.3), col="#0072B2"); arrow((84, 74.8), (84, 64.3), col="#0072B2")
box(14, 41.2, 72, 4.0, "BIC across families: hybrid (3 classes x 1 trait) < 2-D continuous < 1-D continuous < LCA (spec A)  |  2-D continuous best in B, C, D  ->  'hybrid'/multi-dimensional, NOT pure typology", fc="white", fs=7.4)
# Layer 3
band(19, 38, C["l3"], "LAYER 3 - Theoretical interpretation (dashed = not tested here)")
box(3, 21, 29, 13.5, "MALMI & BROWN (2008)\nObserved items mainly map to cybernetic\n(monitoring, targets) and reward controls;\ncultural, planning, administrative largely\nunobserved. Package coexistence: supported\nas co-occurrence only", fc="white", fs=7.6, ls="--")
box(35.5, 21, 29, 13.5, "SIMONS (1995)\nMonitoring/targets are COMPATIBLE with\ndiagnostic control. Interactive use, belief\nand boundary systems are NOT observable\nin WBES -> classes are not labelled\n'diagnostic' or 'interactive'", fc="white", fs=7.6, ls="--")
box(68, 21, 29, 13.5, "BLOOM & VAN REENEN (2007)\nAn aggregate score captures most structure\nin the data (gradient); configurations add\nlittle once the score is controlled in the\noutcome models examined", fc="white", fs=7.6, ls="--")
for x in (18, 50, 82): arrow((x, 41.0), (x, 38.2), ls="--", col="#7A4B8A")
# Layer 4
band(1, 17, C["l4"], "LAYER 4 - Organisational associations (cross-sectional)")
box(3.5, 3, 30, 9.5, "FIRM CHARACTERISTICS\nLarger firms: higher mean core score\n(1.86 -> 2.51, <50 to 250+ staff)\nCountry gaps: ITA lowest, GBR highest", fs=7.4)
box(36.5, 3, 33, 9.5, "PERFORMANCE (associational)\nlog sales/employee: +0.13 per SD of score (within country)\n3y sales growth: +0.003 per SD; employment growth: +0.002\nClasses add nothing once the continuous score is controlled\n(pseudo-class F tests, all outcomes)", fs=7.4)
box(72, 3, 25, 9.5, "NONLINEARITY / INTERACTION\nProductivity: mild non-linearity (Holm p<.05)\nNo robust interactions among monitoring,\ntargets, bonuses (Holm)", fs=7.4)
ax.plot([1.8, 1.8], [56, 8], color="#2E7D32", lw=1.3, zorder=1); ax.plot([1.8, 1.8], [56, 56], color="#2E7D32"); ax.plot([1.8, 2.9], [56, 56], color="#2E7D32", lw=1.3); arrow((1.8, 8), (2.9, 8), col="#2E7D32", style="-|>")
ax.text(1.2, 32, "associations with the continuous score", rotation=90, fontsize=7, va="center", ha="center", color="#2E7D32")
ax.text(99, 0.2, "Solid: estimated structure/association. Dashed: theoretical reading, not tested. No arrow implies causation.", fontsize=7.5, ha="right", style="italic")
for ext in ("png", "svg", "pdf"):
    for dest in (os.path.join(ROOT, "05_THEORY/model_development"), FIG):
        plt.savefig(os.path.join(dest, f"MANAGEMENT_CONTROL_MODEL.{ext}"), dpi=300, bbox_inches="tight")
log("11_model_figure: done")
