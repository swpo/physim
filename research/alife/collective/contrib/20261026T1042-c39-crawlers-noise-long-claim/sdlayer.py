"""(c39) Signed-distance layer test for the crawler world: every 5th render frame from frame 40 (t >= 8, when one large
crawler dominates), for each body (phi > 0.5 component >= 400 px), mean s in the rim band |d| <= 3 px, the core
d <= -10 px and the outside band 6 <= d <= 15 px (own pixels: nearer to this body than to any other), periodic.
Prints per-frame ratios and the fraction of body-frames with rim/core and rim/out both >= 1.5. usage: sdlayer.py frames.npz"""
import sys, numpy as np
from scipy import ndimage
F = np.load(sys.argv[1]); Rr = F["render"].astype(np.float32); rf = list(F["render_f"])
H, W = Rr.shape[2:]; sl = (slice(H, 2 * H), slice(W, 2 * W)); out = []
for k, f in enumerate(rf):
    if f < 40 or k % 5: continue
    t = np.tile(Rr[k, 0] > 0.5, (3, 3))
    d = np.where(t, -(ndimage.distance_transform_edt(t) - 0.5), ndimage.distance_transform_edt(~t) - 0.5)[sl]
    lab, n = ndimage.label(t); _, (iy, ix) = ndimage.distance_transform_edt(lab == 0, return_indices=True)
    near = lab[iy, ix][sl]; labc = lab[sl]; s = Rr[k, 3]
    for j in np.unique(labc[labc > 0]):
        if (labc == j).sum() < 400: continue
        own = near == j
        rim, core, o = s[own & (np.abs(d) <= 3)].mean(), s[own & (d <= -10)].mean(), s[own & (d >= 6) & (d <= 15)].mean()
        out.append((f, rim / max(core, 1e-9), rim / max(o, 1e-9)))
a = np.array(out)
print(sys.argv[1], "body-frames", len(a), "both >= 1.5:", round(float(((a[:, 1] >= 1.5) & (a[:, 2] >= 1.5)).mean()), 2),
      "median rim/core", round(float(np.median(a[:, 1])), 2), "median rim/out", round(float(np.median(a[:, 2])), 2))
