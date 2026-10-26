"""Cells per kind in a labkit frames.npz of sporecell2: components of (C0 + M + C1) density > thr (periodic), kind by the
larger of the summed C0 and C1 inside the component; prints counts at a few render frames. usage: cellkinds.py frames.npz"""
import sys, numpy as np
from scipy import ndimage as ndi
F = np.load(sys.argv[1]); R = F["render"].astype(np.float32); rf = list(F["render_f"])
for k in sorted(set([0, len(rf) // 4, len(rf) // 2, 3 * len(rf) // 4, len(rf) - 1])):
    m = R[k, 1] + R[k, 2] + R[k, 3]; thr = 0.25 * m.max()
    lab, n = ndi.label(ndi.gaussian_filter(m, 1.0, mode="wrap") > thr)
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for x, y in zip(a, b):
            if x and y and x != y: lab[lab == y] = x
    ids = [i for i in np.unique(lab) if i and (lab == i).sum() >= 12]
    c0 = [R[k, 1][lab == i].sum() for i in ids]; c1 = [R[k, 3][lab == i].sum() for i in ids]
    k1 = sum(1 for a, b in zip(c0, c1) if b > a)
    print(f"render frame {rf[k]}: cells {len(ids)}, kind-1 (predator) cells {k1}, kind-0 {len(ids) - k1}")
