"""Census of loop kinds (hole side) over time from evo_track.py output; one panel per run."""
import json, sys
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
files = sys.argv[2:]
fig, axs = plt.subplots(1, len(files), figsize=(6 * len(files), 3.6), squeeze=False)
for ax, f in zip(axs[0], files):
    r = json.load(open(f)); cen = r["census"]
    t = np.array([c["t"] for c in cen])
    kinds = sorted({k for c in cen for k in c["areas"]})
    M = np.zeros((len(kinds), len(t)))
    for j, c in enumerate(cen):
        for a, n in zip(c["areas"], c["counts"]): M[kinds.index(a), j] = n
    groups = {"side 11 (founders)": [11], "side 12-13": [12, 13], "side 2-4": [2, 3, 4], "side 5-10": [5, 6, 7, 8, 9, 10], "other": [k for k in kinds if k > 13]}
    for lab, ks in groups.items():
        y = sum(M[kinds.index(k)] for k in ks if k in kinds) if any(k in kinds for k in ks) else 0 * t
        ax.plot(t / 1000, y, label=lab)
    ax.set_title(f"{f}: loops by kind (hole side)", fontsize=9); ax.set_xlabel("steps (k)"); ax.legend(fontsize=7)
fig.tight_layout(); fig.savefig(sys.argv[1], dpi=80)
