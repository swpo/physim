"""Per-body amphiphile and catalyst ledger from a labkit frames.npz of the FCH chemoton.
Bodies: u+1 > 0.6 components; u and K summed over each body dilated by 3 px.
usage: bodies.py frames.npz [frame ...]"""
import sys, numpy as np
from scipy import ndimage
R = np.load(sys.argv[1])["render"]
fr = [int(x) for x in sys.argv[2:]] or [59, 70, 80, 90, 100, 110, 119]
for i in fr:
    u, P, K = R[i]
    lab, n = ndimage.label(u > 0.6)
    rows = []
    for j in range(1, n + 1):
        m = lab == j; md = ndimage.binary_dilation(m, iterations=3); ys, xs = np.nonzero(m)
        rows.append((int(m.sum()), round(float(u[md].sum())), round(float(K[md].sum()), 1), int(ys.mean()), int(xs.mean())))
    rows.sort(key=lambda r: -r[1])
    print(f"frame {i} (t~{i * 600 / 119:.0f}): total u+1 {u.sum():.0f}, total K {K.sum():.0f}, mean P {P.mean():.3f}; bodies (area, u, K, y, x): {rows}")
