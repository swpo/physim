"""Per-individual interface boundary score for elongated rods (radial rho around a centroid mixes
the two rails of a thin rod). For every body (phi > 0, >= 12 px) at every 10th frame: rim = mean s
on the interface band |phi| < 0.3 touching the body, core = mean s where phi > 0.6, outside = mean s
in the ring 3-6 px outside the body. Prints the fraction of bodies with rim/core >= 1.5 and
rim/outside >= 1.5, the medians, and the mean fuel f in cores.
usage: ringstat.py frames.npz [frame_step]"""
import sys, numpy as np
from scipy import ndimage
R = np.load(sys.argv[1])["render"]; step = int(sys.argv[2]) if len(sys.argv) > 2 else 10
rc, ro, fc, ok = [], [], [], 0
for i in range(10, len(R), step):
    phi, s, f = R[i, 0], R[i, 2], R[i, 3]
    lab, n = ndimage.label(phi > 0, structure=np.ones((3, 3)))
    for j in range(1, n + 1):
        m = lab == j
        if m.sum() < 12: continue
        d2 = ndimage.binary_dilation(m, iterations=2)
        band = d2 & (np.abs(phi) < 0.3); core = m & (phi > 0.6)
        out = ndimage.binary_dilation(m, iterations=6) & ~ndimage.binary_dilation(m, iterations=3) & (phi < -0.3)
        if band.sum() < 4 or core.sum() < 2 or out.sum() < 4: continue
        a, b = s[band].mean() / max(s[core].mean(), 1e-6), s[band].mean() / max(s[out].mean(), 1e-6)
        rc.append(a); ro.append(b); fc.append(f[core].mean()); ok += (a >= 1.5) & (b >= 1.5)
print(f"{sys.argv[1]}: bodies {len(rc)}, membrane-like {ok} ({ok / max(len(rc), 1):.0%}), median rim/core {np.median(rc):.2f}, median rim/outside {np.median(ro):.2f}, mean core fuel {np.mean(fc):.3f}")
