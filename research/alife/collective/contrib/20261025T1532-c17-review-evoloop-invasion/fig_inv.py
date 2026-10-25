"""Side-4 share vs time after insertion, per seed: invader arm (side-4 plant, red) and neutral arm (side-11 plant, grey)."""
import json, glob
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
seeds = sorted(int(f.split("_s")[1].split(".")[0]) for f in glob.glob("census/inv8_s*.json"))
fig, ax = plt.subplots(2, 5, figsize=(13, 5), sharex=True, sharey=True)
for a, s in zip(ax.ravel(), seeds):
    for m, col, lab in ((8, "tab:red", "side-4 plant"), (15, "0.4", "side-11 plant (neutral)")):
        d = json.load(open(f"census/inv{m}_s{s}.json"))
        a.plot([(r["t"] - d["t_ins"]) / 1000 for r in d["census"]], [r["hist"][4] / max(r["n"], 1) for r in d["census"]], color=col, label=lab)
    a.set_title(f"seed {s}" + (" (swept before plant: excluded)" if s == 42 else ""), fontsize=8); a.axhline(0.5, ls=":", c="k", lw=0.6)
ax[0, 0].legend(fontsize=7); fig.supxlabel("thousand steps after planting (t_ins = 20000)"); fig.supylabel("side-4 share of loops")
fig.tight_layout(); fig.savefig("invasion.png", dpi=100)
