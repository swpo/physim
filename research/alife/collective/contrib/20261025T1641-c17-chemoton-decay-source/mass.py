"""Body mass vs bath level for FCH chemoton runs: per recorded frame, number of bodies (u+1 > 0.6, >= 6 px),
amphiphile held in bodies (sum of u+1 over bodies dilated 3 px), bath mean u+1 (outside), and total K.
usage: mass.py frames.npz T_total"""
import sys, numpy as np
from scipy import ndimage
R = np.load(sys.argv[1])["render"]; T = float(sys.argv[2]); n = len(R) - 1
for i in np.linspace(0, n, 9).astype(int):
    u, P, K = R[i]
    lab, nb = ndimage.label(u > 0.6); a = ndimage.sum(np.ones_like(u), lab, range(1, nb + 1))
    keep = np.isin(lab, [j + 1 for j in range(nb) if a[j] >= 6]); md = ndimage.binary_dilation(keep, iterations=3)
    print(f"t={i * T / n:6.0f}: bodies {int((a >= 6).sum()):3d}, body amphiphile {u[md].sum():8.1f}, bath mean u+1 {u[~md].mean():+.4f}, bath min {u[~md].min():+.3f}, total u+1 {u.sum():8.1f}, K {K.sum():.0f}")
