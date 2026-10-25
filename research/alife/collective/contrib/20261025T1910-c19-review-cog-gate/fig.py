"""c19: cog matter (r < 12, relative to the fork at t=600) and core food (r < 6) for the four arms of annulus.py, seeds 4 and 5."""
import json
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(2, 2, figsize=(9, 5.5))
for c, s in enumerate((4, 5)):
    d = json.load(open(f"ann_s{s}.json"))
    for name, r in d["arms"].items():
        t = [x[0] for x in r]; ls = "--" if name == "cut_lowD" else "-"
        ax[0, c].plot(t, [x[1] for x in r], ls, label=name); ax[1, c].plot(t, [x[2] for x in r], ls, label=name)
    ax[0, c].set_title(f"seed {s}: cog matter (r<12) / fork value", fontsize=9); ax[1, c].set_title(f"seed {s}: food inside the cog (r<6)", fontsize=9)
    ax[1, c].set_xlabel("t (cut of the annulus 12<r<20 from t=600)")
ax[0, 0].legend(fontsize=7); plt.tight_layout(); plt.savefig("annulus_s4_s5.png", dpi=85)
