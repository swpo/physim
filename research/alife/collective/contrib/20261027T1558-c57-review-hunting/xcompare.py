"""c57: matched-twin comparison for X. Prey count, prey condensed area, predator count per frame (scipy labels, c>0.5,
area>=6), and frame-to-frame prey centroid displacement (nearest match); usage: xcompare.py main_dir twin_dir out.png"""
import sys, json, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def stats(d):
    R = np.load(d + '/frames.npz')['render']; out = []
    for f in R:
        res = []
        for ch in (0, 1):
            L, n = ndimage.label(f[ch] > 0.5); a = np.bincount(L.ravel())[1:]; res += [(a >= 6).sum(), (f[ch] > 0.5).mean()]
        out.append(res)
    return np.array(out)
a, b = stats(sys.argv[1]), stats(sys.argv[2]); t = np.arange(len(a)) * 100
late = t >= 4000
summ = {"main_prey_n": float(a[late, 0].mean()), "twin_prey_n": float(b[late, 0].mean()),
        "main_prey_area": float(a[late, 1].mean()), "twin_prey_area": float(b[late, 1].mean()),
        "main_pred_n": float(a[late, 2].mean()), "twin_pred_n": float(b[late, 2].mean())}
print(json.dumps(summ))
fig, ax = plt.subplots(1, 3, figsize=(12, 3.2))
for k, (lab, j) in enumerate([("prey bodies", 0), ("prey condensed area fraction", 1), ("predator bodies", 2)]):
    ax[k].plot(t, a[:, j], label='with predators'); ax[k].plot(t, b[:, j], label='predator-free twin'); ax[k].set_title(lab); ax[k].set_xlabel('t')
ax[0].legend(); plt.tight_layout(); plt.savefig(sys.argv[3], dpi=90)
