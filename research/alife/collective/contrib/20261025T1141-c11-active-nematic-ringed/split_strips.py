"""Find fission events in a labkit frames.npz (one body whose pixels overlap exactly two bodies
k frames later, each >= amin px, with no other body touching) and plot crops of the matter channel
around each, over 8 frames. Usage: split_strips.py frames.npz out.png [thr] [nrows] [k]"""
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
sel = ev[:: max(1, len(ev) // nrows)][:nrows]
print(len(ev), "fission events; showing", [(int(rf[e[0]]), e[1], e[2]) for e in sel])
H, W = R.shape[2:]; h = 20
fig, ax = plt.subplots(len(sel), 8, figsize=(12, 1.6 * len(sel)), squeeze=False)
for r, (i, cy, cx) in enumerate(sel):
    for c in range(8):
        f = min(max(i - 3 + c, 0), len(R) - 1)
        img = np.roll(np.roll(R[f, 0], H // 2 - cy, 0), W // 2 - cx, 1)[H // 2 - h:H // 2 + h, W // 2 - h:W // 2 + h]
        ax[r, c].imshow(img, cmap="gray", vmin=-1.1, vmax=1.1); ax[r, c].axis("off")
        ax[r, c].set_title(f"frame {int(rf[f])}", fontsize=7)
plt.suptitle("fission events (phi, crops centred on the parent)", fontsize=9); plt.tight_layout()
plt.savefig(out, dpi=80)
