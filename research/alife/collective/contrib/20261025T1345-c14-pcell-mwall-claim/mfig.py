"""M-wall figure from a labkit pack: M channel over the domain, and M around the deepest persistent splits.
usage: python mfig.py pack_dir out.png"""
import sys, json, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
pk, out = sys.argv[1], sys.argv[2]
f = np.load(f"{pk}/frames.npz"); R, RF, MT = f["render"], f["render_f"], f["matter"]
m = json.load(open(f"{pk}/metrics.json")); spf = m["steps_per_frame"]
ps = m["persistent_splits"]
gen = {}
for e in ps:  # generation of children = parent's + 1 (founders 0)
    g = gen.get(e["parent"], 0) + 1
    for c in e["surviving_children"]: gen[c] = g
deep = sorted(ps, key=lambda e: -gen[e["surviving_children"][0]])[:3]
thr = 0.5 * MT.max()
def loc(fr):  # centroid of the frame-(fr-2) component that overlaps >= 2 components at fr+2
    a, na = ndimage.label(MT[max(fr - 2, 0)] > thr * 0.5); b, nb = ndimage.label(MT[min(fr + 2, len(MT) - 1)] > thr * 0.5)
    best = None
    for i in range(1, na + 1):
        k = np.unique(b[(a == i) & (b > 0)])
        if len(k) >= 2:
            ar = (a == i).sum()
            if best is None or ar > best[0]: best = (ar, ndimage.center_of_mass(a == i))
    return best[1] if best else (64, 64)
nr = 1 + len(deep)
fig, ax = plt.subplots(nr, 5, figsize=(13, 2.7 * nr))
idx = np.linspace(0, len(RF) - 1, 5).astype(int)
for j, i in enumerate(idx):
    ax[0, j].imshow(R[i, 5], cmap="magma", vmin=0, vmax=1); ax[0, j].contour(R[i, 3] > 0.5, [0.5], colors="c", linewidths=0.4)
    ax[0, j].set_title(f"M, t={RF[i] * spf}", fontsize=8)
for r, e in enumerate(deep, 1):
    fr = e["frame"]; cy, cx = loc(fr)
    near = np.argsort(np.abs(RF - fr))[0]
    for j, d in enumerate([-6, -3, 0, 3, 6]):
        i = int(np.clip(near + d, 0, len(RF) - 1))
        img = np.roll(np.roll(R[i, 5], 64 - int(cy), 0), 64 - int(cx), 1)[28:100, 28:100]
        ax[r, j].imshow(img, cmap="magma", vmin=0, vmax=1)
        ax[r, j].set_title(f"split {e['parent']}->{e['surviving_children']} (gen {gen[e['surviving_children'][0]]}) t={RF[i] * spf}", fontsize=6)
for a in ax.flat: a.set_xticks([]); a.set_yticks([])
fig.suptitle(f"{pk}: wall material M (magma; cyan = wall contour) and M around the deepest persistent splits", fontsize=9)
fig.tight_layout(); fig.savefig(out, dpi=90)
