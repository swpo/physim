"""Per frame: amphiphile bodies (u+1 > 0.6, holes filled, >= 20 px), split into those that carry catalyst
(max K within the body dilated 2 px >= 0.5) and K-free ones; total amphiphile area of each group.
usage: kbodies.py pack_dir [pack_dir2 ...]"""
import sys, numpy as np
from scipy import ndimage
for d in sys.argv[1:]:
    F = np.load(d + "/frames.npz"); R = F["render"]; tf = F["render_f"]
    print(d)
    for i in list(range(0, R.shape[0], max(1, R.shape[0] // 12))) + [R.shape[0] - 1]:
        u, K = R[i, 0], R[i, 2]; body = ndimage.binary_fill_holes(u > 0.6); lab, n = ndimage.label(body)
        withK = noK = aK = a0 = 0
        for k in range(1, n + 1):
            m = lab == k
            if m.sum() < 20: continue
            if K[ndimage.binary_dilation(m, iterations=2)].max() >= 0.5: withK += 1; aK += (u[m] > 0.6).sum()
            else: noK += 1; a0 += (u[m] > 0.6).sum()
        print(f"  t={tf[i] * 3:5.0f}  bodies with K {withK:2d} (bilayer px {aK:5d})   K-free {noK:2d} (px {a0:5d})   total K {K.sum():8.1f}")
