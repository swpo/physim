"""Figure: cohort new activity and replacement for each knob (runs/*.json) and the baseline (parent results.json)."""
import os, json, glob
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
base = json.load(open(os.path.join(HERE, "..", "20261026T0009-c30-hash-chemistry-o-calibration", "results.json")))
groups = [("baseline sigma .15 mu .01", None), ("sigma .05", "sig05"), ("sigma .02, n0 2000", "sig02n"), ("mu .001", "mu001"),
          ("mu .05", "mu05"), ("crowding 0.3, n0 2000", "crowd03n"), ("moving landscape (resalt every 2000)", "resalt2k")]
fig, ax = plt.subplots(2, len(groups), figsize=(3.1 * len(groups), 6.2), sharey="row")
tb = np.arange(20) * 1000 + 500
for i, (lab, tag) in enumerate(groups):
    runs = [v for k, v in base.items() if k.startswith("long/m0") and "cohort_new" in v] if tag is None else \
           [json.load(open(f)) for f in sorted(glob.glob(f"{HERE}/runs/{tag}_s*.json"))]
    for j, r in enumerate(runs):
        c = r.get("cohort_new", r.get("cohort")); s = r.get("shadow_cohort_new", r.get("sh_cohort"))
        ov = r.get("top20_overlap_with_first_window", r.get("ov"))
        ax[0, i].plot(tb, np.array(c) + 0.5, c=f"C{j}", marker="o", ms=2); ax[0, i].plot(tb, np.array(s) + 0.5, c=f"C{j}", ls=":", lw=1)
        ax[1, i].plot(tb, ov, c=f"C{j}")
    late = [sum(r.get("cohort_new", r.get("cohort"))[2:]) for r in runs]; lsh = [sum(r.get("shadow_cohort_new", r.get("sh_cohort"))[2:]) for r in runs]
    ax[0, i].set_title(f"{lab}\nlate (t>=2000) new kinds {late}\nshadow {lsh}", fontsize=8); ax[0, i].set_yscale("log")
    ax[1, i].set_ylim(-0.05, 1.05); ax[1, i].set_xlabel("step")
ax[0, 0].set_ylabel("cohort new kinds per 1000-step window (+0.5)\nsolid real, dotted RB shadow")
ax[1, 0].set_ylabel("top-20 overlap with steps 0-1000")
plt.tight_layout(); plt.savefig(f"{HERE}/knobs.png", dpi=70)
