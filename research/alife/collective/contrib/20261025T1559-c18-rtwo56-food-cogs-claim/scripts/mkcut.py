"""pick the most isolated mature cog in pre<seed>_ckpt.npz and write cut_<seed>.npz (disk r=RAD around it)"""
import sys, numpy as np
from scipy import ndimage
RAD = 18
H = W = 192; yy, xx = np.mgrid[:H, :W]
for sd in map(int, sys.argv[1:]):
    c = np.load(f'pre{sd}_ckpt.npz'); A = c['A']
    lab, k = ndimage.label(ndimage.gaussian_filter(A[0], 1) > 0.3)
    cs = ndimage.center_of_mass(A[0], lab, range(1, k+1)); sz = ndimage.sum(np.ones_like(A[0]), lab, range(1, k+1))
    def pd(a, b): return np.hypot(min(abs(a[0]-b[0]), H-abs(a[0]-b[0])), min(abs(a[1]-b[1]), W-abs(a[1]-b[1])))
    best = None
    for i in range(k):
        if sz[i] < 20: continue
        dmin = min([pd(cs[i], cs[j]) for j in range(k) if j != i and sz[j] >= 20] or [999])
        if best is None or dmin > best[0]: best = (dmin, i)
    dmin, i = best; cy, cx = cs[i]
    dy = np.minimum(abs(yy-cy), H-abs(yy-cy)); dx = np.minimum(abs(xx-cx), W-abs(xx-cx))
    mask = np.hypot(dy, dx) < RAD
    np.savez_compressed(f'cut_{sd}.npz', A=c['A'], F=c['F'], W=c['W'], t=c['t'], mask=mask, cy=cy, cx=cx, rad=RAD, dmin=dmin)
    print(sd, 'cog at', round(cy), round(cx), 'nearest other core', round(dmin), 'cores', k)
