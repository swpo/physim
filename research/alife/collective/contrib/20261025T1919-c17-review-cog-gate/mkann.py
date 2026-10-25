"""Pick the most isolated mature cog in pre<seed>_ckpt.npz (as the food-cog claim's mkcut.py) and write ann_<seed>.npz
with mask = annulus 12 < r < 20 around it (food removed there every step: the cog's outside supply).
usage: mkann.py seed"""
import sys, numpy as np
from scipy import ndimage
sd = int(sys.argv[1]); c = np.load(f'pre{sd}_ckpt.npz'); A = c['A']; H, W = A.shape[1:]; yy, xx = np.mgrid[:H, :W]
lab, k = ndimage.label(ndimage.gaussian_filter(A[0], 1) > 0.3)
cs = ndimage.center_of_mass(A[0], lab, range(1, k + 1)); sz = ndimage.sum(np.ones_like(A[0]), lab, range(1, k + 1))
def pd(a, b): return np.hypot(min(abs(a[0]-b[0]), H-abs(a[0]-b[0])), min(abs(a[1]-b[1]), W-abs(a[1]-b[1])))
best = max((min([pd(cs[i], cs[j]) for j in range(k) if j != i and sz[j] >= 20] or [999]), i) for i in range(k) if sz[i] >= 20)
dmin, i = best; cy, cx = cs[i]
d = np.hypot(np.minimum(abs(yy-cy), H-abs(yy-cy)), np.minimum(abs(xx-cx), W-abs(xx-cx)))
np.savez_compressed(f'ann_{sd}.npz', A=c['A'], F=c['F'], W=c['W'], t=c['t'], mask=(d > 12) & (d < 20), cy=cy, cx=cx, dmin=dmin)
print(sd, 'cog at', round(cy), round(cx), 'nearest other core', round(dmin))
