"""Side-by-side phi and fuel crops of several labkit runs at chosen frames. usage: compare.py out.png label=dir ..."""
import sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out = sys.argv[1]; runs = [a.split("=", 1) for a in sys.argv[2:]]
fr = [30, 60, 90, 119]
fig, ax = plt.subplots(2 * len(runs), len(fr), figsize=(2.2 * len(fr), 2.2 * 2 * len(runs)))
for r, (lab, d) in enumerate(runs):
    R = np.load(d + "/frames.npz")["render"]
    for c, i in enumerate(fr):
        i = min(i, len(R) - 1)
        ax[2 * r, c].imshow(R[i, 0], cmap="gray", vmin=-1, vmax=1); ax[2 * r, c].set_title(f"{lab} phi t={round(i*1000/119)}", fontsize=7)
        ax[2 * r + 1, c].imshow(R[i, 3], cmap="viridis", vmin=0, vmax=1.2); ax[2 * r + 1, c].set_title(f"{lab} fuel f", fontsize=7)
for a in ax.flat: a.axis("off")
plt.tight_layout(); plt.savefig(out, dpi=80)
