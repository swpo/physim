"""Centroid paths of every cell (phi > 0.5 components, periodic) in a labkit frames.npz; displacement in cell diameters.
usage: motion.py <frames.npz> <out.png>"""
import sys, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
d = np.load(sys.argv[1]); F = d[d.files[0]] if "frames" not in d.files else d["frames"]
print("keys", d.files, F.shape)
phi = F[:, 0]; T, H, W = phi.shape
def comps(f):
    lab, n = ndimage.label(phi[f] > 0.5)
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):   # periodic merge
        for x, y in zip(a, b):
            if x and y and x != y: lab[lab == y] = x
    out = []
    for k in np.unique(lab)[1:]:
        yy, xx = np.nonzero(lab == k); A = len(yy)
        if A < 30: continue
        cy = np.angle(np.exp(2j * np.pi * yy / H).mean()) / (2 * np.pi) * H % H
        cx = np.angle(np.exp(2j * np.pi * xx / W).mean()) / (2 * np.pi) * W % W
        out.append((cy, cx, A))
    return out
tracks = []  # list of [(f, cy, cx, A)]
for f in range(T):
    cs = comps(f); used = set()
    for tr in tracks:
        if tr[-1][0] != f - 1: continue
        _, py, px, pA = tr[-1]; best = None; bd = 1e9
        for i, (cy, cx, A) in enumerate(cs):
            dy = (cy - py + H / 2) % H - H / 2; dx = (cx - px + W / 2) % W - W / 2; dd = np.hypot(dy, dx)
            if i not in used and dd < bd and 0.6 < A / pA < 1.6: bd, best = dd, i
        if best is not None and bd < 20: used.add(best); tr.append((f, *cs[best]))
    for i, c in enumerate(cs):
        if i not in used: tracks.append([(f, *c)])
fig, ax = plt.subplots(figsize=(6, 6))
for k, tr in enumerate(tracks):
    if len(tr) < 20: continue
    tr = np.array(tr); dy = (np.diff(tr[:, 1]) + H / 2) % H - H / 2; dx = (np.diff(tr[:, 2]) + W / 2) % W - W / 2
    D = 2 * np.sqrt(np.median(tr[:, 3]) / np.pi); net = np.hypot(dy.sum(), dx.sum()); path = np.hypot(dy, dx).sum()
    print(f"track {k}: frames {int(tr[0,0])}-{int(tr[-1,0])}, area {int(tr[:,3].min())}-{int(tr[:,3].max())}, diameter {D:.1f}px, net {net/D:.2f} diameters, path {path/D:.2f}")
    y = tr[0, 1] + np.r_[0, np.cumsum(dy)]; x = tr[0, 2] + np.r_[0, np.cumsum(dx)]; ax.plot(x, y, "-", label=f"{k}: {net/D:.1f} D"); ax.plot(x[0], y[0], "o", c="k", ms=3)
ax.set_aspect(1); ax.invert_yaxis(); ax.legend(fontsize=7); ax.set_title("unwrapped centroid paths (phi>0.5), dot = start", fontsize=9)
fig.savefig(sys.argv[2], dpi=80)
