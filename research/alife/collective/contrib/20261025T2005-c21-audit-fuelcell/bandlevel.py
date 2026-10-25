"""(c21) Surfactant level in each body's interface band (|phi| < 0.3 within 2 px of the body) against the gate
midpoint sh = 0.45, and the fuel permeability there, D/Df = 1/(1 + 5 (s/0.45)^12). usage: bandlevel.py frames.npz"""
import sys, numpy as np
from scipy import ndimage
R = np.load(sys.argv[1])["render"]; lv, perm = [], []
for i in range(20, len(R), 10):
    phi, s = R[i, 0], R[i, 2]
    lab, n = ndimage.label(phi > 0, structure=np.ones((3, 3)))
    for j in range(1, n + 1):
        m = lab == j
        if m.sum() < 12: continue
        band = ndimage.binary_dilation(m, iterations=2) & (np.abs(phi) < 0.3)
        if band.sum() < 4: continue
        b = s[band]; lv.append(np.percentile(b, 90)); perm.append(np.median(1 / (1 + 5 * (b / 0.45) ** 12)))
print(f"{sys.argv[1]}: band s (90th pct per body) median {np.median(lv):.3f} [{np.percentile(lv, 10):.3f}-{np.percentile(lv, 90):.3f}]; median band permeability D/Df {np.median(perm):.3f}")
