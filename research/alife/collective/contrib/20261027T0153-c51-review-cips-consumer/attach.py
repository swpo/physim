"""python attach.py <pack_dir>: for each frame, consumer components (q > 0.5) and the fraction that touch a prey droplet
(prey c_a > 0.5 within 2 px); and how long each consumer band keeps the same prey partner (overlap tracking)."""
import sys, numpy as np
from scipy import ndimage
d = np.load(sys.argv[1] + '/frames.npz'); r = d['render'].astype(float); tf = d['render_f']
print('render ranges', [(round(r[:, c].min(), 2), round(r[:, c].max(), 2)) for c in range(4)])
st = np.ones((3, 3))
def lab(x):  # periodic labelling
    l, n = ndimage.label(x, st)
    for a, b in ((l[0], l[-1]), (l[:, 0], l[:, -1])):
        for i, j in zip(a, b):
            if i and j and i != j: l[l == j] = i
    return l
tot = att = free = 0; free_frames = []
for f in range(20, len(r)):
    q = r[f, 1] > 0.5; p = ndimage.binary_dilation(np.roll(r[f, 0], 0) > 0.5, st, iterations=2)
    lq = lab(q); ids = [i for i in np.unique(lq) if i and (lq == i).sum() >= 4]
    a = sum(bool((p & (lq == i)).any()) for i in ids); tot += len(ids); att += a
    free_frames.append(len(ids) - a)
print(f'consumer components (>=4 px) frames 20-{len(r)-1}: {tot}; touching prey: {att} ({att/max(tot,1):.3f}); free per frame mean {np.mean(free_frames):.2f}')
