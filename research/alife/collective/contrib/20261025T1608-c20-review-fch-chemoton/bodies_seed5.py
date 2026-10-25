"""Per-body table for a labkit FCH pack: area (u>0.6), enclosed hole area, max catalyst K within 3 px. usage: bodies_seed5.py frames.npz"""
import sys, numpy as np
from scipy import ndimage
F = np.load(sys.argv[1]); R = F["render"]; fr = F["render_f"]
for i in [30, 59, 60, 75, 90, 105, 119]:
    u, P, K = R[i]; lab, n = ndimage.label(u > 0.6); out = []
    for j in range(1, n + 1):
        m = lab == j
        if m.sum() < 6: continue
        out.append((int(m.sum()), int((ndimage.binary_fill_holes(m) & ~m).sum()), round(float(K[ndimage.binary_dilation(m, iterations=3)].max()), 3)))
    print("t", fr[i] * 3, "K total %.1f" % K.sum(), "u total %.0f" % u.sum(), "bodies (area, hole, maxK):", sorted(out, reverse=True))
