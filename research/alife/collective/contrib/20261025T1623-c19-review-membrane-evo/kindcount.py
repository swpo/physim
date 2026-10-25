"""c19: number and mean area of K1-majority and K2-majority cells at t=40000 (cells = components of K1+K2 > 0.2,
>= 12 px). usage: kindcount.py <review dir>"""
import sys, glob, numpy as np
from scipy import ndimage
for arm in ("up", "twin"):
    for d in sorted(glob.glob(f"{sys.argv[1]}/{arm}/seed*")):
        R = np.load(d + "/frames.npz")["render"][-1].astype(np.float64); k1, k2 = R[0], R[1]
        lab, n = ndimage.label(k1 + k2 > 0.2); c = {1: [], 2: []}
        for j in range(1, n + 1):
            m = lab == j
            if m.sum() < 12: continue
            c[2 if k2[m].sum() > k1[m].sum() else 1].append(int(m.sum()))
        print(f"{arm}/{d.split('seed')[-1]}: K1 cells {len(c[1])} (mean area {np.mean(c[1]) if c[1] else 0:.0f}), K2 cells {len(c[2])} (mean area {np.mean(c[2]) if c[2] else 0:.0f})")
