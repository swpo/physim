"""(c20: c15 split_strips.py with neural-field labels.) (c15: adapted from c11 20261025T1141 split_strips.py; adds the shell channel row and random selection.) Find fission events in a labkit frames.npz (one body whose pixels overlap exactly two bodies
k frames later, each >= amin px, with no other body touching) and plot crops of the matter channel
around each, over 8 frames. Usage: split_strips.py frames.npz out.png [thr] [nrows] [k] [frames: keep events within 4 frames of these, e.g. the deepest-generation births from metrics.json]"""
import sys, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
path, out = sys.argv[1], sys.argv[2]
thr = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
nrows = int(sys.argv[4]) if len(sys.argv) > 4 else 4
k = int(sys.argv[5]) if len(sys.argv) > 5 else 2
F = np.load(path); R, rf = F["render"], F["render_f"]
amin = 15
ev = []
for i in range(len(R) - k):
    a, na = ndimage.label(R[i, 0] > thr); b, nb = ndimage.label(R[i + k, 0] > thr)
    for j in range(1, na + 1):
        m = a == j
        if m.sum() < 2 * amin: continue
        ids, cnt = np.unique(b[m & (b > 0)], return_counts=True)
        if len(ids) != 2: continue
        sizes = [(b == x).sum() for x in ids]
        if min(sizes) < amin: continue
        # each daughter must overlap only this parent
        if all(len(np.unique(a[(b == x) & (a > 0)])) == 1 for x in ids):
            cy, cx = ndimage.center_of_mass(m); ev.append((i, int(cy), int(cx)))
ded = []
for e in ev:
    if not any(abs(e[0] - d[0]) <= 6 and abs(e[1] - d[1]) % 128 < 8 and abs(e[2] - d[2]) % 128 < 8 for d in ded): ded.append(e)
ev = ded  # one entry per fission (the same pinch is detected on consecutive frames)
only = [int(x) for x in sys.argv[6].split(",")] if len(sys.argv) > 6 else None
if only: ev = [e for e in ev if any(abs(int(rf[e[0]]) - o) <= 4 for o in only)]
sel = [ev[i] for i in sorted(np.random.default_rng(0).choice(len(ev), min(nrows, len(ev)), replace=False))]
print(len(ev), "fission events; showing", [(int(rf[e[0]]), e[1], e[2]) for e in sel])
H, W = R.shape[2:]; h = 20
fig, ax = plt.subplots(2 * len(sel), 8, figsize=(12, 3.2 * len(sel)), squeeze=False); smax = float(R[:, 2].max())
for r, (i, cy, cx) in enumerate(sel):
    for c in range(8):
        f = min(max(i - 3 + c, 0), len(R) - 1)
        crop = lambda g: np.roll(np.roll(g, H // 2 - cy, 0), W // 2 - cx, 1)[H // 2 - h:H // 2 + h, W // 2 - h:W // 2 + h]; img = crop(R[f, 0])
        ax[2 * r, c].imshow(img, cmap="gray", vmin=-1.1, vmax=1.1); ax[2 * r, c].axis("off")
        ax[2 * r + 1, c].imshow(crop(R[f, 2]), cmap="magma", vmin=0, vmax=smax); ax[2 * r + 1, c].contour(img, [0], colors="c", linewidths=0.5); ax[2 * r + 1, c].axis("off")
        ax[2 * r, c].set_title(f"frame {int(rf[f])} u", fontsize=7); ax[2 * r + 1, c].set_title("firing f(u)", fontsize=7)
plt.suptitle("fission events (activity u and firing f(u), crops centred on the parent; random selection, seed 0 of numpy)", fontsize=9); plt.tight_layout()
plt.savefig(out, dpi=80)
