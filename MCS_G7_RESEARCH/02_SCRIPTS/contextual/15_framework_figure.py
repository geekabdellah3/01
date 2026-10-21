import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(13, 6.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 66); ax.axis("off")
def box(x, y, w, h, t, ls="-", fc="white", fs=8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=0.8", fc=fc, ec="#333", lw=1.2, ls=ls)); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, linespacing=1.3)
def arr(p, q, ls="-", col="#333", txt=None):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12, lw=1.4, ls=ls, color=col))
    if txt: ax.text((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + 2.2, txt, ha="center", fontsize=7, bbox=dict(fc="white", ec="none", pad=.5))
ax.text(50, 65.5, "Conceptual framework: from observed practices to contextual effectiveness", ha="center", va="top", fontsize=12.5, fontweight="bold")
box(2, 30, 20, 20, "PRACTICES\n(observed in WBES)\nmonitoring, targets,\nincentives\n\nUniversality of practices:\ndescribed", fc="#E8F1F8")
box(27, 30, 20, 20, "STRUCTURE\n(estimated)\ncommon dimension,\nweak classes\n\nUniversality of structure:\ntested, partly supported", fc="#E8F1F8")
box(52, 30, 20, 20, "IMPLEMENTATION /\nINTEGRATION\n(NOT observed)\nuse, articulation,\nmanagerial ownership", ls=":", fc="#F2F2F2")
box(77, 30, 21, 20, "OUTCOMES\n(observed, associational)\nproductivity, growth\n\nUniversality of effectiveness:\ntested, mixed", fc="#E4F2EA")
box(27, 4, 45, 16, "CONTEXT\nNational institutions, culture, governance (NOT measured)\nOrganisational: size, age, ownership, exports, managers (measured, partly)\nContextual fit = alignment of practice and context (NOT directly identifiable)", ls="--", fc="#FBF0DA", fs=8)
arr((22.4, 40), (26.6, 40), txt="co-occurrence"); arr((47.4, 40), (51.6, 40), ls=":", col="#7A4B8A"); arr((72.4, 40), (76.6, 40), ls=":", col="#7A4B8A")
ax.add_patch(FancyArrowPatch((37, 50.6), (87.5, 50.6), arrowstyle="-|>", mutation_scale=12, lw=1.5, color="#2E7D32", connectionstyle="arc3,rad=-0.15")); ax.text(62, 57.2, "association tested: stability across countries", ha="center", fontsize=7.5, color="#2E7D32")
arr((49.5, 20.4), (62, 29.6), ls="--", col="#B8860B", txt=""); arr((49.5, 20.4), (87, 29.6), ls="--", col="#B8860B")
ax.text(50, 24.5, "moderates (theoretical; firm-level partly tested)", ha="center", fontsize=7.5, color="#B8860B")
ax.text(2, 1.2, "Solid = observed/estimated; dotted = unobserved mechanism; dashed = contextual moderation (theory; firm-level moderators partly tested). No arrow implies causation.", fontsize=7.8, style="italic")
plt.savefig(os.path.join(FIG, "Fig_Framework_contextual_fit.png"), dpi=300, bbox_inches="tight"); plt.savefig(os.path.join(FIG, "Fig_Framework_contextual_fit.pdf"), bbox_inches="tight")
