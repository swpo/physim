"""python onprey.py frames.npz : per rendered frame from t>=2000, consumer bodies (q > 0.5, >= 4 px) and the share of them
that touch prey (c_a > 0.5 within 1 px) and the mean fraction of their area inside prey; plus free consumer bodies
(touching no prey) per frame."""
import sys, json, numpy as np
from scipy import ndimage
d = np.load(sys.argv[1]); R = d['render'].astype(np.float32); f = d['render_f']; dtf = float(sys.argv[2]) if len(sys.argv) > 2 else 100.0
tot = touch = 0; inside = []; free = []
for k, F in enumerate(R):
    if f[k] * dtf < 2000: continue
    prey = F[0] > 0.5; l, n = ndimage.label(F[1] > 0.5); nf = 0
    for i in range(1, n + 1):
        m = l == i
        if m.sum() < 4: continue
        tot += 1; t = bool((ndimage.binary_dilation(m) & prey).any()); touch += t; inside.append(float((m & prey).sum() / m.sum())); nf += (not t)
    free.append(nf)
out = {'consumer_bodies': tot, 'touch_prey': touch, 'share_touching': touch / max(tot, 1), 'mean_area_inside_prey': float(np.mean(inside)) if inside else None, 'free_per_frame_mean': float(np.mean(free)), 'free_per_frame_max': int(np.max(free))}
print(json.dumps(out))
