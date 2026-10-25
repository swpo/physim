"""c19: persistent splits and interior fuel for c15's nematic fuel-cell (ringed), its chi_s=0 ablation and two
ringless chi_s=0 twins with uniformly lowered fuel diffusivity (Df 0.5, 0.2; default 2.0), seeds 0-2 and 11.
Numbers: ringed/chis0 seeds 0-2 from c15's packs (FACTS.md) and ringstat.txt; seed 11 and all slow-D arms from
c19's runs (20261025T1425-c19-review-fuelcell, this directory; fuel_rings.txt)."""
import json
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, numpy as np
D = {"ringed (Df 2)": {"splits": [14, 5, 11, 15], "gen": [3, 3, 3, 3], "core_fuel": [0.576, 0.593, 0.583, 0.580]},
     "no ring, Df 2": {"splits": [5, 2, 7, 10], "gen": [2, 1, 2, 3], "core_fuel": [0.353, 0.348, 0.351, 0.351]},
     "no ring, Df 0.5": {"splits": [12, 4, 6, 12], "gen": [3, 2, 2, 3], "core_fuel": [0.535, 0.561, 0.544, 0.546]},
     "no ring, Df 0.2": {"splits": [8, 5, 8, 17], "gen": [3, 2, 2, 4], "core_fuel": [0.787, 0.871, 0.771, 0.793]}}
json.dump({"seeds": [0, 1, 2, 11], "arms": D}, open("summary.json", "w"), indent=1)
fig, ax = plt.subplots(1, 2, figsize=(10, 3.6)); x = np.arange(4); w = 0.2
for k, (lab, d) in enumerate(D.items()):
    ax[0].bar(x + (k - 1.5) * w, d["splits"], w, label=lab)
    for xi, (sp, g) in enumerate(zip(d["splits"], d["gen"])): ax[0].text(xi + (k - 1.5) * w, sp + 0.3, f"g{g}", ha="center", fontsize=6)
    cf = [c if c is not None else np.nan for c in d["core_fuel"]]; ax[1].bar(x + (k - 1.5) * w, cf, w, label=lab)
for a, t in zip(ax, ["persistent splits (g = max generation)", "mean core fuel (ringstat.py)"]):
    a.set_xticks(x); a.set_xticklabels(["seed 0", "seed 1", "seed 2", "seed 11"]); a.set_title(t, fontsize=9)
ax[0].legend(fontsize=7); plt.tight_layout(); plt.savefig("slowD_summary.png", dpi=90)
for lab, d in D.items(): print(lab, "total splits", sum(d["splits"]), "gen>=3 on", sum(g >= 3 for g in d["gen"]), "of 4")
