"""(c21) Fission events in labkit matter frames (f(u) > thr), k=1 frame apart: one parent component whose
pixels overlap exactly two daughters (each >= amin px) that overlap only that parent. For each event,
report the parent's distance (px, periodic) to the nearest other component in the 3 frames before,
to separate break-ups of isolated comets from collision-driven ones. Plots a crop strip of the
most isolated events. Usage: fission_isolation.py frames.npz out.png [thr]"""
import sys, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
M = np.load(sys.argv[1])["matter"]; out = sys.argv[2]; thr = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
T, H, W = M.shape; amin = 10
def lab(x):
    l, n = ndimage.label(np.pad(x, 0) > thr)
    # periodic merge of labels across edges
    for a, b in list(zip(l[0], l[-1])) + list(zip(l[:, 0], l[:, -1])):
        if a and b and a != b: l[l == b] = a
    return l
L = [lab(M[t]) for t in range(T)]
ev = []
for t in range(5, T - 1):
    a, b = L[t], L[t + 1]
    for j in np.unique(a[a > 0]):
        m = a == j
        ids = np.unique(b[m & (b > 0)])
        if len(ids) != 2: continue
        if min((b == x).sum() for x in ids) < amin: continue
        if not all(len(np.unique(a[(b == x) & (a > 0)])) == 1 for x in ids): continue
        # isolation: min distance from parent to any other component over frames t-3..t (track parent by overlap)
        dmin = 1e9; cur = m
        for s in range(t, t - 4, -1):
            others = (L[s] > 0) & ~cur
            dt = ndimage.distance_transform_edt(~np.tile(others, (3, 3)))[H:2 * H, W:2 * W]
            dmin = min(dmin, dt[cur].min() if cur.any() else 1e9)
            prev = L[s - 1][cur & (L[s - 1] > 0)]
            if prev.size == 0: break
            ids2, c = np.unique(prev, return_counts=True); cur = L[s - 1] == ids2[c.argmax()]
        cy, cx = ndimage.center_of_mass(m)
        ev.append((t, int(cy), int(cx), float(dmin), int(m.sum())))
d = np.array([e[3] for e in ev])
print(len(ev), "fission events; parent distance to nearest other body over 3 frames before (px): median %.1f" % np.median(d),
      "; >=4 px: %d, >=6 px: %d, >=8 px: %d" % ((d >= 4).sum(), (d >= 6).sum(), (d >= 8).sum()))
sel = sorted(ev, key=lambda e: -e[3])[:4]
print("most isolated:", sel)
h = 20; fig, ax = plt.subplots(len(sel), 8, figsize=(12, 1.6 * len(sel)), squeeze=False)
for r, (t, cy, cx, dm, area) in enumerate(sel):
    for c in range(8):
        f = min(max(t - 5 + c, 0), T - 1)
        g = np.roll(np.roll(M[f], H // 2 - cy, 0), W // 2 - cx, 1)[H // 2 - h:H // 2 + h, W // 2 - h:W // 2 + h]
        ax[r, c].imshow(g, cmap="magma", vmin=0, vmax=1); ax[r, c].axis("off")
        ax[r, c].set_title("frame %d%s" % (f, " (parent)" if f == t else ""), fontsize=7)
    ax[r, 0].text(-4, h, "gap %.0f px" % dm, fontsize=7, rotation=90, va="center", ha="right")
fig.suptitle("most isolated fission events, firing f(u), crops 40x40 px centred on the parent; " + sys.argv[1], fontsize=8)
fig.tight_layout(); fig.savefig(out, dpi=90)
