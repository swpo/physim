"""pick the most isolated mature cog in pre<seed>_ckpt.npz and write cut_<seed>.npz (disk r=RAD around it)"""
import sys, numpy as np
from scipy import ndimage
import os
RAD = float(os.environ.get("RAD", "18")); PRE = os.environ.get("PRE", "pre"); OUT = os.environ.get("OUT", "cut_")
for sd in map(int, sys.argv[1:]):
    c = np.load(f'{PRE}{sd}_ckpt.npz'); A = c['A']; H, W = A.shape[1:]; yy, xx = np.mgrid[:H, :W]
    lab, k = ndimage.label(ndimage.gaussian_filter(A[0], 1) > 0.3)
    minsz = 20 * (RAD / 18) ** 2
    cs = ndimage.center_of_mass(A[0], lab, range(1, k+1)); sz = ndimage.sum(np.ones_like(A[0]), lab, range(1, k+1))
    def pd(a, b): return np.hypot(min(abs(a[0]-b[0]), H-abs(a[0]-b[0])), min(abs(a[1]-b[1]), W-abs(a[1]-b[1])))
    best = None
    for i in range(k):
        if sz[i] < minsz: continue
        dmin = min([pd(cs[i], cs[j]) for j in range(k) if j != i and sz[j] >= minsz] or [999])
        if best is None or dmin > best[0]: best = (dmin, i)
    dmin, i = best; cy, cx = cs[i]
    dy = np.minimum(abs(yy-cy), H-abs(yy-cy)); dx = np.minimum(abs(xx-cx), W-abs(xx-cx))
    mask = np.hypot(dy, dx) < RAD
    np.savez_compressed(f'{OUT}{sd}.npz', A=c['A'], F=c['F'], W=c['W'], t=c['t'], mask=mask, cy=cy, cx=cx, rad=RAD, dmin=dmin)
    print(sd, 'cog at', round(cy), round(cx), 'nearest other core', round(dmin), 'cores', k)
