"""Per-lumen solute contrast (each enclosed lumen's mean c / mean c outside), per recorded frame.
Same segmentation as the claim's contrast.py: bilayer = (u + 1.6) > 0.8, lumens = enclosed
components of the complement on the torus, outside = the largest component."""
import sys, numpy as np
from scipy import ndimage
def wrap_label(mask):
    lab, n = ndimage.label(mask); parent = list(range(n + 1))
    def f(a):
        while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for a, b in list(zip(lab[0], lab[-1])) + list(zip(lab[:, 0], lab[:, -1])):
        if a and b:
            ra, rb = f(a), f(b)
            if ra != rb: parent[ra] = rb
    return np.array([f(i) for i in range(n + 1)])[lab]
F = np.load(sys.argv[1]); X = F[[k for k in F.files if F[k].ndim == 4][0]]
for t in range(0, X.shape[0], 10):
    u, c = X[t, 0], X[t, 1]; lab = wrap_label(u <= 0.8)
    ids, cnt = np.unique(lab[lab > 0], return_counts=True); out = ids[np.argmax(cnt)]
    co = c[lab == out].mean()
    per = sorted(round(float(c[lab == i].mean() / co), 1) for i, n in zip(ids, cnt) if i != out and n >= 4)
    print(t, 'lumens (>=4 px):', per, 'min', min(per) if per else None)
