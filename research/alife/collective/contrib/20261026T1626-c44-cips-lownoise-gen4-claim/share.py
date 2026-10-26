"""Share of catalysis (the only source of the amphiphile s) inside the bodies (e>0.5) over time, from a labkit frames.npz.
usage: python share.py pack/seedK/frames.npz"""
import sys, numpy as np
z = np.load(sys.argv[1]); f = z["render"]; fi = z["render_f"]
print("t  cat_share_in_bodies  s_share_in_bodies+4px  n_px_bodies")
from scipy.ndimage import binary_dilation
for k in np.linspace(5, len(fi) - 1, 10).astype(int):
    e, p, F, s = f[k].astype(float); cat = 2 * F * np.clip(e, 0, None) ** 2 * (1 - p); b = e > 0.5
    if b.sum() == 0: print(int(fi[k]) * 100, "no bodies"); continue
    print(int(fi[k]) * 100, round(cat[b].sum() / cat.sum(), 2), round(s[binary_dilation(b, iterations=4)].sum() / s.sum(), 2), int(b.sum()))
