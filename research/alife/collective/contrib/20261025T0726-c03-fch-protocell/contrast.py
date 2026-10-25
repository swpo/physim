"""Lumen/outside solute contrast per recorded frame from a labkit pack's frames.npz.
Bilayer = (u + 1.6) > thr; lumens = enclosed components of the complement (periodic-aware:
the component touching the most area is the outside). Prints contrast every k frames,
and the fraction of frames with contrast >= 2."""
import sys, json, numpy as np
from scipy import ndimage

def wrap_label(mask):
    lab, n = ndimage.label(mask)
    # merge labels across periodic edges
    parent = list(range(n + 1))
    def f(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for a, b in list(zip(lab[0], lab[-1])) + list(zip(lab[:, 0], lab[:, -1])):
        if a and b:
            ra, rb = f(a), f(b)
            if ra != rb: parent[ra] = rb
    lut = np.array([f(i) for i in range(n + 1)])
    return lut[lab]

def analyse(path, thr=0.8, every=10):
    F = np.load(path)
    key = [k for k in F.files if F[k].ndim == 4][0]
    X = F[key]
    rows = []
    for t in range(X.shape[0]):
        u, c = X[t, 0], X[t, 1]
        lab = wrap_label(u <= thr)
        ids, cnt = np.unique(lab[lab > 0], return_counts=True)
        if len(ids) < 2:
            rows.append((t, None, 0)); continue
        out = ids[np.argmax(cnt)]
        lum = (lab > 0) & (lab != out)
        rows.append((t, float(c[lum].mean() / max(c[lab == out].mean(), 1e-9)), int(len(ids) - 1)))
    ok = [r for r in rows if r[1] is not None]
    frac = np.mean([r[1] >= 2 for r in ok]) if ok else 0
    for r in rows[::every]:
        print(r[0], None if r[1] is None else round(r[1], 2), r[2])
    print("frac frames contrast>=2:", round(float(frac), 2), "final", rows[-1])
    return rows

if __name__ == "__main__":
    analyse(sys.argv[1])
