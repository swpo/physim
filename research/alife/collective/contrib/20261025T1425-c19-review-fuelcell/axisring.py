"""c19: rim vs medial-axis contrast of shell s, per body. For each body (phi > 0, >= 12 px) every 10th
frame from 40: axis = body pixels on its distance ridge (edt >= 0.8 max edt), rim = pixels within 1 px
of the phi = 0 contour on either side, outside = pixels 4-7 px outside. Reports the fraction of bodies
with rim/axis >= 1.5 and rim/outside >= 1.5, medians, and mean fuel on the axis.
usage: axisring.py frames.npz"""
import sys, numpy as np
from scipy import ndimage
R = np.load(sys.argv[1])["render"].astype(np.float32)
ra, ro, fa, ok = [], [], [], 0
for i in range(40, len(R), 10):
    phi, s, f = R[i, 0], R[i, 2], R[i, 3]
    lab, n = ndimage.label(phi > 0, structure=np.ones((3, 3)))
    ein = ndimage.distance_transform_edt(phi > 0); eout = ndimage.distance_transform_edt(phi <= 0)
    for j in range(1, n + 1):
        m = lab == j
        if m.sum() < 12: continue
        ax = m & (ein >= 0.8 * ein[m].max())
        near = ndimage.binary_dilation(m, iterations=2)
        rim = (m & (ein <= 1)) | (near & ~m & (eout <= 1))
        out = ndimage.binary_dilation(m, iterations=7) & ~ndimage.binary_dilation(m, iterations=3) & (lab == 0)
        if out.sum() < 4: continue
        a, b = s[rim].mean() / max(s[ax].mean(), 1e-6), s[rim].mean() / max(s[out].mean(), 1e-6)
        ra.append(a); ro.append(b); fa.append(f[ax].mean()); ok += (a >= 1.5) & (b >= 1.5)
print(f"{sys.argv[1]}: bodies {len(ra)}, ring-like {ok} ({ok / max(len(ra), 1):.0%}), median rim/axis {np.median(ra):.2f}, median rim/outside {np.median(ro):.2f}, mean axis fuel {np.mean(fa):.3f}")
