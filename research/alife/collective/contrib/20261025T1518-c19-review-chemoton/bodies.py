"""c19: per-body amphiphile mass and catalyst content in the fed run and its starved fork (seed 13).
Bodies = connected components of u+1 > 0.6 (labkit's threshold), periodic; a body's mass is the sum of
u+1 over its component dilated by 3 px. Prints, at selected times, each body >= 30 px with centroid,
mass and total K. usage: bodies.py frames.npz [frames.npz ...]"""
import sys, numpy as np
from scipy import ndimage
for fn in sys.argv[1:]:
    d = np.load(fn); R = d["render"].astype(np.float32); f = d["render_f"]
    print("==", fn)
    for i in [int(np.argmin(np.abs(f * 3 - T))) for T in (150, 300, 330, 390, 450, 520, 600)]:
        u, K = R[i, 0], R[i, 2]
        lab, n = ndimage.label(np.pad(u > 0.6, 0), structure=np.ones((3, 3)))
        rows = []
        for j in range(1, n + 1):
            m = lab == j
            if m.sum() < 30: continue
            dm = ndimage.binary_dilation(m, iterations=3)
            cy, cx = ndimage.center_of_mass(m)
            rows.append(f"({cy:.0f},{cx:.0f}) area {m.sum()} mass {u[dm].sum():.0f} K {K[dm].sum():.1f}")
        print(f"t={f[i] * 3:.0f}: total u {u.sum():.0f}, total K {K.sum():.1f}; " + "; ".join(rows))
