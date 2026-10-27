"""python freeshare.py frames.npz time_per_frame : free.py's measure on labkit frames: share of consumer bodies (q > 0.5,
>= 4 px) touching no prey (c_a > 0.5 dilated by 2 px), over rendered frames with 1000 <= t <= 2000; prey count at the end."""
import sys, json, numpy as np
from scipy import ndimage
d = np.load(sys.argv[1]); R = d['render'].astype(np.float32); t = d['render_f'] * float(sys.argv[2]); tot = fr = 0
for F, tt in zip(R, t):
    if not 1000 <= tt <= 2000: continue
    prey = ndimage.binary_dilation(F[0] > 0.5, iterations=2); lab, k = ndimage.label(F[1] > 0.5); a = np.bincount(lab.ravel())
    ids = [j for j in range(1, k + 1) if a[j] >= 4]; tot += len(ids); fr += sum(not prey[lab == j].any() for j in ids)
l, k = ndimage.label(R[-1][0] > 0.5)
print(json.dumps({'frames': sys.argv[1], 'consumer_bodies': tot, 'free': fr, 'free_share': round(fr / max(tot, 1), 3), 'prey_bodies_final': int(k), 't_final': float(t[-1])}))
