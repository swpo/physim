"""Per cell and frame: L rim/core (rim = wall channel 4phi(1-phi) > 0.5 inside the cell's dilated mask; core = cell
pixels >= 3 px from its edge with wall < 0.2) and speed (centroid shift to the max-overlap cell in the next frame,
periodic). Prints rim/core by speed tercile and the share of cell-frames with rim/core >= 1.5.
Usage: ring_vs_speed.py pack_dir"""
import sys, numpy as np
from scipy import ndimage
F = np.load(sys.argv[1] + "/frames.npz"); R = F["render"]; tf = F["render_f"]
H, W = R.shape[2:]
def cells(f):
    m = R[f, 1] + R[f, 2] + R[f, 3]; body = ndimage.binary_fill_holes(m > 0.35 * np.percentile(m, 99.5))
    lab, n = ndimage.label(body); return lab, n
rows = []
for f in range(20, R.shape[0] - 1):
    lab, n = cells(f); lab2, n2 = cells(f + 1); L, wall = R[f, 2], R[f, 3]
    for k in range(1, n + 1):
        m = lab == k
        if m.sum() < 30: continue
        core = ndimage.binary_erosion(m, iterations=3) & (wall < 0.2)
        rim = ndimage.binary_dilation(m, iterations=1) & (wall > 0.5)
        if core.sum() < 5 or rim.sum() < 5: continue
        ov = np.bincount(lab2[m], minlength=n2 + 1); ov[0] = 0
        if ov.max() < 0.5 * m.sum(): continue
        j = int(np.argmax(ov)); ys, xs = np.nonzero(m); ys2, xs2 = np.nonzero(lab2 == j)
        def cen(a, P): th = 2 * np.pi * a / P; return np.arctan2(np.sin(th).mean(), np.cos(th).mean()) * P / (2 * np.pi)
        dy = (cen(ys2, H) - cen(ys, H) + H / 2) % H - H / 2; dx = (cen(xs2, W) - cen(xs, W) + W / 2) % W - W / 2
        v = np.hypot(dy, dx) / (tf[f + 1] - tf[f]) / np.sqrt(m.sum())  # body lengths per frame-interval unit
        rows.append((v, L[rim].mean() / max(L[core].mean(), 1e-9)))
rows = np.array(rows); q = np.quantile(rows[:, 0], [1 / 3, 2 / 3])
print(f"{sys.argv[1]}: {len(rows)} cell-frames; share rim/core >= 1.5: {np.mean(rows[:, 1] >= 1.5):.2f}; median rim/core {np.median(rows[:, 1]):.2f}")
for name, sel in (("slowest third", rows[:, 0] <= q[0]), ("middle third", (rows[:, 0] > q[0]) & (rows[:, 0] <= q[1])), ("fastest third", rows[:, 0] > q[1])):
    print(f"  {name}: speed {np.median(rows[sel, 0]):.4f} BL/t, median rim/core {np.median(rows[sel, 1]):.2f}, share >= 1.5 {np.mean(rows[sel, 1] >= 1.5):.2f}")
