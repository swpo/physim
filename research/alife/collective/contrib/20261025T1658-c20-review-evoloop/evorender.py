"""Render evoloop grids (9 states) as full view plus a zoomed crop. usage: evorender.py out.png title1=grid1.npy ..."""
import sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
cm = ListedColormap(["#000000", "#3060ff", "#ff3030", "#30ff30", "#ffff30", "#ff30ff", "#ffffff", "#30ffff", "#ff9000"])
out, items = sys.argv[1], [a.rsplit("@", 1) for a in sys.argv[2:]]
fig, ax = plt.subplots(2, len(items), figsize=(5 * len(items), 10), squeeze=False)
for c, (lab, f) in enumerate(items):
    g = np.load(f); ax[0, c].imshow(g, cmap=cm, vmin=0, vmax=8, interpolation="nearest"); ax[0, c].set_title(lab + " (full 400^2)", fontsize=9)
    s = (g > 0).astype(float); ii, jj = np.nonzero(s)
    k = np.argmax(np.bincount((ii // 80) * 5 + jj // 80, minlength=25)); i0, j0 = (k // 5) * 80, (k % 5) * 80
    ax[1, c].imshow(g[i0:i0 + 80, j0:j0 + 80], cmap=cm, vmin=0, vmax=8, interpolation="nearest"); ax[1, c].set_title(f"{lab} crop rows {i0}-{i0+80}, cols {j0}-{j0+80}; red = sheath, blue = core", fontsize=8)
for a in ax.flat: a.axis("off")
plt.tight_layout(); plt.savefig(out, dpi=70)
