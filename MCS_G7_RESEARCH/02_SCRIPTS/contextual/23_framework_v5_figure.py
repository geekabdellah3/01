import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(14, 7.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 74); ax.axis("off")
def box(x, y, w, h, t, fc="white", ls="-", fs=8, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=0.8", fc=fc, ec="#333", lw=1.1, ls=ls)); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, linespacing=1.28, fontweight="bold" if bold else "normal")
def arr(p, q, ls="-", col="#333", rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11, lw=1.3, ls=ls, color=col, connectionstyle=f"arc3,rad={rad}"))
ax.text(50, 73, "From structured management practices to control mechanisms, performance, heterogeneity and transferability", ha="center", va="top", fontsize=12.5, fontweight="bold")
ax.text(50, 69.6, "Starting point: Bloom & Van Reenen's three practice families; control-literature concepts are then used to interpret them", ha="center", va="top", fontsize=9, style="italic")
# header row
for x, t in [(2, "Observable practices\n(Bloom & Van Reenen; WBES items)"), (28, "Control mechanisms\n(interpretation)"), (54, "Association with performance"), (78, "Context: stability and transfer")]:
    ax.text(x + 10, 64.5, t, ha="center", va="center", fontsize=9, fontweight="bold")
rows = [(51, "#E8F1F8", "MONITORING\nr2 indicators tracked (y/n)\nr3 number of indicators", "#EAF3E4", "Cybernetic / diagnostic\ncontrol: measure and track results"),
        (35.5, "#E8F1F8", "TARGETS\nr4 targets exist (y/n)\nr5 time frame of targets", "#EAF3E4", "Planning and results control:\nset objectives, orient behaviour"),
        (20, "#E8F1F8", "INCENTIVES\nr8 target-linked bonuses (y/n)\nr9 basis of bonuses", "#EAF3E4", "Reward control:\nalign effort and rewards")]
for y, c1, t1, c2, t2 in rows:
    box(2, y, 22, 11, t1, fc=c1, fs=7.8); box(28, y, 22, 11, t2, fc=c2, fs=7.8); arr((24.2, y + 5.5), (27.8, y + 5.5)); arr((50.2, y + 5.5), (53.8, y + 5.5), ls="-", col="#2E7D32")
box(54, 20, 22, 42, "LEVEL 1 - individual\nassociations\nβ_M, β_T, β_I\n\nLEVEL 2 - combinations\nM×T, M×I, T×I\n(statistical interaction;\nnot yet complementarity)\n\nOutcomes: productivity,\nsales and employment growth\n(associations only)", fc="#FBF0DA", fs=8)
box(78, 36, 20, 26, "LEVEL 3 - contexts\nOrganisation: size, age,\nownership, exports, managers\nCountry: stability of β_M, β_T, β_I;\nout-of-sample prediction;\ntransferability across countries\n(country effects ≠ culture)", fc="#EFE6F2", fs=7.8)
box(78, 20, 20, 12.5, "NOT OBSERVED\nuse (diagnostic / interactive),\nintegration, consistency,\nmanagerial ownership", ls=":", fc="#F2F2F2", fs=7.8)
arr((76.2, 50), (77.8, 50), col="#7A4B8A"); arr((88, 32.8), (88, 35.8), ls=":", col="#777")
ax.text(50, 12.5, "Mapping used for interpretation only: Bloom & Van Reenen practices are not a complete management control system (Malmi & Brown, 2008). Presence of several practices does not show that they form a coherent system (Grabner & Moers, 2013);", ha="center", fontsize=7.8, style="italic")
ax.text(50, 9.8, "their integration and use (Simons, 1995) would require additional variables. Solid arrows: observed or estimated; dotted: unobserved; no arrow implies causation.", ha="center", fontsize=7.8, style="italic")
plt.savefig(os.path.join(FIG, "Fig_Framework_v5_practices_to_transferability.png"), dpi=300, bbox_inches="tight"); plt.savefig(os.path.join(FIG, "Fig_Framework_v5_practices_to_transferability.pdf"), bbox_inches="tight")
