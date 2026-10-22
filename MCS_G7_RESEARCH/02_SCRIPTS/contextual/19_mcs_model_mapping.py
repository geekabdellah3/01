"""Formal specification of management control (MCS) frameworks and their mapping to WBES items (coverage matrix).
Constructs named only as far as the verified records support (see 05_THEORY/literature_review); mapping strength reflects BOTH conceptual fit and wording verification."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); from common import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
ITEMS = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11"]
# status: O observed (items map with adequate wording), P partial/proxy, N not observed.  strength per item: 2 strong, 1 weak/proxy, 0 none
C = [
 # model, construct, role/formal spec, {item: strength}, status, comment
 ("Malmi & Brown (2008)", "Planning controls", "latent C1; first-order construct of the package", {"r5": 1}, "P", "only the time frame of targets (r5) is a proxy; no long-range or action planning items"),
 ("Malmi & Brown (2008)", "Cybernetic controls", "latent C2", {"r2": 2, "r3": 2, "r4": 2, "r1": 1, "r5": 1}, "O", "monitoring indicators, targets, feedback reaction; no budgets or financial/non-financial split"),
 ("Malmi & Brown (2008)", "Reward and compensation", "latent C3", {"r8": 2, "r9": 2}, "O", "bonuses tied to targets and their basis; nothing on non-monetary rewards"),
 ("Malmi & Brown (2008)", "Administrative controls", "latent C4", {}, "N", "no verified item (r10, r11 wording unknown)"),
 ("Malmi & Brown (2008)", "Cultural controls", "latent C5", {}, "N", "none"),
 ("Simons (1995)", "Belief systems", "system S1", {}, "N", "none"),
 ("Simons (1995)", "Boundary systems", "system S2", {}, "N", "none"),
 ("Simons (1995)", "Diagnostic use", "use mode of a technical system (feedback against targets)", {"r2": 1, "r3": 1, "r4": 1}, "P", "presence of monitoring and targets is compatible with diagnostic use; use itself is not observed"),
 ("Simons (1995)", "Interactive use", "use mode (strategic uncertainties, dialogue)", {}, "N", "not observable from presence items"),
 ("Otley (1999) / Ferreira & Otley (2009)", "Objectives and key success factors", "area A1", {}, "N", "none"),
 ("Otley (1999) / Ferreira & Otley (2009)", "Strategies and plans", "area A2", {"r5": 1}, "P", "time frame of targets only"),
 ("Otley (1999) / Ferreira & Otley (2009)", "Performance targets", "area A3", {"r4": 2, "r5": 2, "r6": 1, "r7": 1}, "O", "r6, r7 wording unverified"),
 ("Otley (1999) / Ferreira & Otley (2009)", "Rewards", "area A4", {"r8": 2, "r9": 2}, "O", "target-linked bonuses"),
 ("Otley (1999) / Ferreira & Otley (2009)", "Information flows for monitoring", "area A5", {"r1": 1, "r2": 2, "r3": 2}, "O", "indicators monitored and reaction to problems"),
 ("Merchant & Van der Stede", "Results controls", "set targets, measure results, reward", {"r2": 2, "r3": 2, "r4": 2, "r5": 1, "r8": 2, "r9": 2}, "O", "closest family to WBES"),
 ("Merchant & Van der Stede", "Action controls", "constrain or prescribe actions", {"r1": 1}, "P", "reaction to production problems is a weak proxy (wording partly verified)"),
 ("Merchant & Van der Stede", "Personnel controls", "selection, training, resources", {"r10": 1, "r11": 1}, "P", "mapping speculative: r10, r11 wording unverified; do not interpret"),
 ("Merchant & Van der Stede", "Cultural controls", "values, group norms", {}, "N", "none"),
 ("Ouchi (1979)", "Market-type control", "measure and reward individual contribution precisely", {"r2": 1, "r3": 1, "r4": 1, "r8": 1, "r9": 1}, "P", "individual versus unit measurement not observed"),
 ("Ouchi (1979)", "Bureaucratic control", "close evaluation plus shared objectives", {"r2": 1, "r4": 1}, "P", "shared acceptance of objectives not observed"),
 ("Ouchi (1979)", "Clan control", "socialisation, goal congruence", {}, "N", "none"),
 ("Grabner & Moers (2013)", "System (internal consistency)", "package + consistency function over controls", {}, "N", "presence data cannot identify consistency"),
 ("Chenhall (2003) / Otley (2016)", "Contingency variables", "context moderates design/effects", {}, "P", "size, age, ownership, exports observed (outside r1-r11); environment, technology, strategy not observed"),
 ("Bloom & Van Reenen (2007) WMS tradition", "Monitoring", "score component", {"r1": 2, "r2": 2, "r3": 2}, "O", "WBES module follows this tradition"),
 ("Bloom & Van Reenen (2007) WMS tradition", "Target setting", "score component", {"r4": 2, "r5": 2, "r6": 1, "r7": 1}, "O", ""),
 ("Bloom & Van Reenen (2007) WMS tradition", "Incentives", "score component", {"r8": 2, "r9": 2, "r10": 1, "r11": 1}, "O", "r10, r11 grouping unverified"),
]
mp = pd.DataFrame([dict(model=m, construct=c, formal_role=f, status=s, comment=cm, **{it: st.get(it, 0) for it in ITEMS}) for m, c, f, st, s, cm in C])
cov = mp.groupby("model", sort=False).apply(lambda g: pd.Series(dict(n_constructs=len(g), observed=int((g.status == "O").sum()), partial=int((g.status == "P").sum()), not_observed=int((g.status == "N").sum()), coverage_score=((g.status == "O").sum() + 0.5 * (g.status == "P").sum()) / len(g)))).reset_index()
cov["scoring_rule"] = "coverage = (observed + 0.5 x partial) / constructs; 'observed' needs at least one strongly mapped item with verified or partly verified wording"
spec = pd.DataFrame([
 ["Malmi & Brown (2008)", "Package of five control types", "x_ij = λ_jk C_ik + ε_ij (items j, control type k, firm i); package = joint distribution of (C_i1..C_i5); configuration = region of that space; Performance_i = f(C_i)", "Five categories verified (planning, cybernetic, reward & compensation, administrative, cultural)", "WBES covers cybernetic and reward only"],
 ["Simons (1995); Tessier & Otley (2012)", "Four systems; modes of use", "x_ij = λ_jk S_ik + μ_jk U_ik; U_ik ∈ {diagnostic, interactive}; effects depend on U (interaction), not on presence", "Four systems and diagnostic/interactive use verified (Tessier & Otley abstract)", "Use not observed"],
 ["Otley (1999); Ferreira & Otley (2009)", "Five areas extended to twelve questions", "Performance management system as a set of areas A1..A5 (objectives, strategies and plans, targets, rewards, information flows); coherence across areas", "Five areas and twelve-question extension verified (abstract/summary); twelve questions not itemised here", "Targets, rewards, information flows partly observed"],
 ["Merchant & Van der Stede", "Four control types", "Results, action, personnel, cultural controls; tightness of each", "Four types verified (course-material listing of the book; edition-level details not checked)", "Results controls observed; others weakly or not"],
 ["Ouchi (1979)", "Market, bureaucracy, clan", "Mechanism choice determined by ability to measure outputs/behaviours and goal congruence", "Three mechanisms and two preconditions verified (abstract)", "Output measurement partly; congruence not observed"],
 ["Grabner & Moers (2013)", "System versus package", "System = package + internal consistency (formal definition per abstract)", "Verified (abstract)", "Not identifiable from presence"],
 ["Bloom & Van Reenen (2007)", "Scored practices", "Score_i = Σ_j s_ij (monitoring, targets, incentives); Productivity = f(Score)", "Verified (abstract)", "Direct counterpart of WBES module"],
 ["Contingency (Chenhall, 2003; Otley, 2016)", "Contingent design/effects", "Effect = β + δ'Context (interaction/fit)", "Verified (summaries)", "Organisational context partly observed; national institutions not"]],
 columns=["model", "unit / structure", "formal specification (our notation)", "verification", "WBES observability"])
with pd.ExcelWriter(os.path.join(ROOT, "08_CONTEXTUAL_FIT/MCS_MODEL_SPECIFICATIONS.xlsx")) as w:
    spec.to_excel(w, sheet_name="formal_specifications", index=False); mp.to_excel(w, sheet_name="construct_item_mapping", index=False); cov.to_excel(w, sheet_name="coverage", index=False)
print(cov.round(2).to_string())
# figure: coverage heatmap
fig, ax = plt.subplots(figsize=(10.5, 9.2)); M = mp[ITEMS].values; cmap = plt.matplotlib.colors.ListedColormap(["#F5F5F5", "#9ECAE1", "#08519C"])
ax.imshow(M, cmap=cmap, vmin=0, vmax=2, aspect="auto")
ax.set_xticks(range(len(ITEMS))); ax.set_xticklabels(ITEMS); ax.xaxis.tick_top()
ax.set_yticks(range(len(mp))); ax.set_yticklabels([f"{r.construct}" for r in mp.itertuples()], fontsize=7.5)
for i, r in enumerate(mp.itertuples()): ax.text(len(ITEMS) - .35, i, {"O": "observed", "P": "partial", "N": "not observed"}[r.status], va="center", fontsize=7, color={"O": "#08519C", "P": "#B8860B", "N": "#A00000"}[r.status])
prev = None
for i, r in enumerate(mp.itertuples()):
    if r.model != prev: ax.axhline(i - .5, color="k", lw=1.2); ax.text(-0.55, i - .1, r.model, ha="right", va="bottom", fontsize=7.2, fontweight="bold", transform=ax.transData); prev = r.model
ax.set_xlim(-.5, len(ITEMS) + 1.6); ax.set_title("Coverage of management-control frameworks by WBES items (dark = strong mapping, light blue = proxy, grey = none)", fontsize=9, pad=24)
plt.subplots_adjust(left=0.43); plt.savefig(os.path.join(FIG, "Fig_MCS_models_WBES_coverage.png"), dpi=300, bbox_inches="tight"); plt.savefig(os.path.join(FIG, "Fig_MCS_models_WBES_coverage.pdf"), bbox_inches="tight"); log("19 mapping: done")
