"""Compare gene trajectories: selection vs neutral runs.

python threads/flow-lenia/scripts/gene_plot.py OUT.png SEL.json NEU.json [LABEL1 LABEL2]
"""
import json, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

out, files = sys.argv[1], sys.argv[2:4]
labels = sys.argv[4:6] or ["gene active (selection)", "neutral marker (control)"]
cols = ["tab:red", "tab:gray"]
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
for f, lab, c in zip(files, labels, cols):
    d = json.load(open(f))["runs"]
    for k, (sd, r) in enumerate(d.items()):
        t = np.array(r["t"]) * 0.2
        m, s = np.array(r["mean"]), np.array(r["sd"])
        ax[0].plot(t, m, color=c, lw=1.5, label=lab if k == 0 else None)
        ax[0].fill_between(t, m - s, m + s, color=c, alpha=0.08)
        ax[1].plot(t, r["bodies"], color=c, lw=1, label=lab if k == 0 else None)
        bg = [x for row in r["body_g"][-5:] for x in row]
        ax[2].hist(bg, bins=np.linspace(-1, 1.5, 26), color=c, alpha=0.35, label=f"{lab} seed {sd}" if k == 0 else None)
ax[0].axhline(0, color="k", lw=0.5); ax[0].set_title("matter-weighted mean log g (band = sd)"); ax[0].set_xlabel("time"); ax[0].legend(fontsize=8)
ax[1].set_title("bodies"); ax[1].set_xlabel("time"); ax[1].legend(fontsize=8)
ax[2].set_title("body mean log g, last 5 samples, all seeds"); ax[2].legend(fontsize=7)
fig.tight_layout(); fig.savefig(out, dpi=80)
