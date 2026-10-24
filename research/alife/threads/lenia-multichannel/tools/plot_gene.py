"""Plot trait trajectories: selection vs neutral runs from quick_gene.py JSON series.

python plot_gene.py OUT.png "label1:glob1" "label2:glob2" ...
"""
import glob
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

out = sys.argv[1]
groups = [a.split(":", 1) for a in sys.argv[2:]]
colors = ["#d95f02", "#7570b3", "#1b9e77", "#e7298a"]
fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
for gi, (lab, pat) in enumerate(groups):
    for k, f in enumerate(sorted(glob.glob(pat))):
        d = json.load(open(f))
        t = [x["t"] for x in d]
        kw = dict(color=colors[gi], alpha=0.85, lw=1.5, label=lab if k == 0 else None)
        ax[0].plot(t, [x["mean"] for x in d], **kw)
        ax[0].fill_between(t, [x["mn"] for x in d], [x["mx"] for x in d], color=colors[gi], alpha=0.08)
        ax[1].plot(t, [x["n"] for x in d], **kw)
        ax[2].plot(t, [x["F"] for x in d], **kw)
for a, ttl in zip(ax, ["population mean trait g (band: per-cell min-max)", "cells", "mean food"]):
    a.set_title(ttl, fontsize=10)
    a.set_xlabel("step")
    a.grid(alpha=0.3)
ax[0].legend(fontsize=9)
fig.tight_layout()
fig.savefig(out, dpi=90)
