"""Cell census around a local feed cut in pcell-mwall-b42 frames.npz (channels S, K, L, wall, yield, M).
Cells: components of (filled wall > 0.5) | (K > 0.05) with >= 20 px. Prints, per frame, the number of cells, the
target cell (component nearest (cy, cx)) area and catalyst sum, and the substrate mean inside / outside the cut disk.
usage: cells.py frames.npz T_total cy cx r frame ..."""
import sys, numpy as np
from scipy import ndimage
R = np.load(sys.argv[1])["render"]; T = float(sys.argv[2]); cy, cx, r = map(float, sys.argv[3:6])
H, W = R.shape[2:]; yy, xx = np.mgrid[0:H, 0:W]
dd = np.hypot((yy - cy + H / 2) % H - H / 2, (xx - cx + W / 2) % W - W / 2)
for i in map(int, sys.argv[6:]):
    lab, n = ndimage.label(ndimage.binary_fill_holes(R[i, 3] > 0.5) | (R[i, 1] > 0.05))
    areas = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1)); big = [j + 1 for j in range(n) if areas[j] >= 20]
    tgt = [j for j in big if dd[lab == j].min() <= 4]
    ta = sum(int((lab == j).sum()) for j in tgt); tk = sum(float(R[i, 1][lab == j].sum()) for j in tgt)
    near = [j for j in big if j not in tgt and dd[lab == j].min() <= r + 12]
    print(f"t={i * T / (len(R) - 1):.0f}: cells {len(big)}, target area {ta} K {tk:.1f}, other cells within r+12: {len(near)} (areas {[int((lab == j).sum()) for j in near]}), S in disk {R[i, 0][dd <= r].mean():.3f}, S outside {R[i, 0][dd > r + 10].mean():.3f}")
