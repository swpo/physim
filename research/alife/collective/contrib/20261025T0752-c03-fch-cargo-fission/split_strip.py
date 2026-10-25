"""Find body fissions (one body at frame i overlapped by two bodies at frame i+k) and draw crops of
u (amphiphile) and c (cargo, log scale) around a few of them, with the cargo held by each body.
Usage: split_strip.py pack_dir out.png [n_events] [seed for random choice]"""
import sys, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

d, out = sys.argv[1], sys.argv[2]
nev = int(sys.argv[3]) if len(sys.argv) > 3 else 3
rng = np.random.default_rng(int(sys.argv[4]) if len(sys.argv) > 4 else 0)
F = np.load(d + "/frames.npz"); R, rf = F["render"], list(F["render_f"])
thr, k = 0.8, 3
labs = [ndimage.label(R[i, 0] > thr) for i in range(len(rf))]
events = []
for i in range(2, len(rf) - k):
    la, na = labs[i]; lb, nb = labs[i + k]
    for j in range(1, na + 1):
        m = la == j
        kids = np.unique(lb[m & (lb > 0)])
        if len(kids) == 2 and m.sum() > 20:
            sizes = [np.sum(lb == q) for q in kids]
            if min(sizes) > 0.3 * max(sizes):
                events.append((i, j, kids))
print("fission events found:", len(events))
# one event per fission (consecutive frames see the same one): keep the earliest per location
picked, seen = [], []
for e in events:
    cy, cx = ndimage.center_of_mass(labs[e[0]][0] == e[1])
    if any(abs(cy - y) < 6 and abs(cx - x) < 6 and abs(e[0] - t) < 8 for t, y, x in seen):
        continue
    seen.append((e[0], cy, cx)); picked.append((e, cy, cx))
print("distinct fissions:", len(picked))
sel = [picked[q] for q in sorted(rng.choice(len(picked), size=min(nev, len(picked)), replace=False))]
offs = [-3, -1, 0, 1, 2, 3, 5, 8]
fig, ax = plt.subplots(2 * len(sel), len(offs), figsize=(1.6 * len(offs), 3.3 * len(sel)), squeeze=False)
H, W = R.shape[2:]
for r, ((i, j, kids), cy, cx) in enumerate(sel):
    for q, o in enumerate(offs):
        t = min(max(i + o, 0), len(rf) - 1)
        yy = (np.arange(-14, 15) + int(cy)) % H; xx = (np.arange(-14, 15) + int(cx)) % W
        u = R[t, 0][np.ix_(yy, xx)]; c = R[t, 1][np.ix_(yy, xx)]
        far = ~ndimage.binary_dilation(R[t, 0] > thr, iterations=3)
        cout = R[t, 1][far].mean()
        lab, n = ndimage.label(u > thr)
        held = [R[t, 1][np.ix_(yy, xx)][lab == b].mean() / cout for b in range(1, n + 1)]
        ax[2 * r, q].imshow(u, cmap="magma", vmin=0, vmax=2.2); ax[2 * r, q].set_title(f"t={rf[t] * 4}", fontsize=7)
        ax[2 * r + 1, q].imshow(np.log10(c + 1e-6), cmap="viridis", vmin=np.log10(cout) - 0.5, vmax=np.log10(cout) + 3.2)
        ax[2 * r + 1, q].set_title("cargo x" + ",".join(f"{h:.0f}" for h in held), fontsize=6)
for a in ax.flat: a.axis("off")
fig.suptitle("fissions (random picks): top u (amphiphile), bottom log cargo; 'cargo xN' = mean cargo in each body / outside", fontsize=8)
plt.tight_layout(); plt.savefig(out, dpi=80)
