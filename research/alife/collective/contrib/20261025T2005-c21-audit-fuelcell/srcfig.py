"""(c21) Claimed world vs rod-only surfactant source, same seed and frame: phi, surfactant s, fuel f
(fixed colour scales across arms). usage: srcfig.py out.png frame dirA labelA dirB labelB [dirC labelC]"""
import sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, fr = sys.argv[1], int(sys.argv[2]); arms = list(zip(sys.argv[3::2], sys.argv[4::2]))
fig, ax = plt.subplots(len(arms), 3, figsize=(9, 3.1 * len(arms)), squeeze=False)
for r, (d, lab) in enumerate(arms):
    R = np.load(d + "/frames.npz")["render"]; f = min(fr, len(R) - 1)
    for c, (k, cm, vmax, nm) in enumerate(((0, "gray", 1, "phi"), (2, "viridis", 0.7, "surfactant s (gate midpoint 0.45)"), (3, "inferno", 0.8, "fuel f"))):
        im = ax[r, c].imshow(R[f, k], cmap=cm, vmin=-1 if k == 0 else 0, vmax=vmax); ax[r, c].axis("off")
        ax[r, c].set_title(f"{lab}: {nm}", fontsize=7); plt.colorbar(im, ax=ax[r, c], fraction=0.046)
fig.suptitle(f"render frame {fr}", fontsize=8); fig.tight_layout(); fig.savefig(out, dpi=75)
