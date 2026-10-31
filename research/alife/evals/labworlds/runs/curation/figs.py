"""Snapshot sheets of the behaviour runs (python figs.py pm|fv)."""
import glob
import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

w = sys.argv[1]
runs = sorted(glob.glob(f"runs/{w}_s*_N*.npz"))
order = lambda p: (int(p.split("_s")[1].split("_")[0]), "rot45" in p, int(p.split("_N")[1].split("_")[0]), p)
runs = sorted(runs, key=order)
n = len(runs)
cols = 4
rows = int(np.ceil(n / cols))
fig, ax = plt.subplots(rows, cols, figsize=(3.2 * cols, 3.3 * rows), squeeze=False)
for k, p in enumerate(runs):
    z = np.load(p)
    meta = json.loads(str(z["meta"]))
    a = ax[k // cols, k % cols]
    if w == "pm":
        f = meta["frames"]
        img = z[f"L_{f}"]
        a.imshow(img, origin="lower", cmap="viridis", vmin=0, vmax=np.percentile(img, 99.5), extent=(0, 128, 0, 128))
        a.contour(np.linspace(0, 128, img.shape[0]), np.linspace(0, 128, img.shape[0]), z[f"phi_{f}"], [0.5],
                  colors="w", linewidths=0.4)
        lab = f"L (phi=0.5 white), t={meta['T']:.0f}"
    else:
        f = meta["frames"]
        img = z[f"om_{f}"]
        a.imshow(img, origin="lower", cmap="RdBu_r", vmin=-0.25, vmax=0.25, extent=(0, 128, 0, 128))
        lab = f"omega, t={meta['T']:.0f}"
    j = p.replace(".npz", ".json")
    try:
        r = json.load(open(j))
        extra = f"ps {r['persistent_splits']} gen {r['max_generation']}"
    except FileNotFoundError:
        extra = ""
    a.set_title(f"s{meta['seed']} N{meta['N']} dt{meta['dt']} rot{meta['rot']:.0f}\n{extra}", fontsize=8)
    a.set_xticks([]); a.set_yticks([])
for k in range(n, rows * cols):
    ax[k // cols, k % cols].axis("off")
fig.suptitle(f"{w}: final frames ({lab}); 128-unit box at every grid", fontsize=9)
plt.tight_layout()
plt.savefig(f"{w}_final_frames.png", dpi=90)
print(f"{w}_final_frames.png", n)
