"""Body turnover from a labkit pack: bodies = components of (u + 1.6) > thr with >= 6 px.
Between consecutive recorded frames, a body with no overlapping body in the next frame is a death,
a body overlapping >= 2 bodies of the next frame is a split, a body with no overlapping body in the
previous frame is a nucleation. Reports counts in windows of the run.
usage: turnover.py pack_dir [nwin]"""
import sys, numpy as np
from scipy import ndimage

d = sys.argv[1]; nwin = int(sys.argv[2]) if len(sys.argv) > 2 else 5; thr = 0.8
F = np.load(d + "/frames.npz"); R, rf = F["render"], list(F["render_f"])
def lab(i):
    l, n = ndimage.label(R[i, 0] > thr)
    sz = np.bincount(l.ravel(), minlength=n + 1); sz[0] = 0
    return np.where(sz[l] >= 6, l, 0)
L = [lab(i) for i in range(len(rf))]
ev = []
for i in range(len(rf) - 1):
    a, b = L[i], L[i + 1]
    ids_a = np.unique(a[a > 0]); ids_b = np.unique(b[b > 0])
    deaths = sum(1 for k in ids_a if not np.any(b[a == k] > 0))
    splits = sum(1 for k in ids_a if len(np.unique(b[(a == k) & (b > 0)])) >= 2)
    nucl = sum(1 for k in ids_b if not np.any(a[b == k] > 0))
    ev.append((rf[i + 1], len(ids_b), deaths, splits, nucl))
ev = np.array(ev)
for w in np.array_split(ev, nwin):
    print(f"frames {int(w[0,0])}-{int(w[-1,0])}: bodies {int(w[0,1])}->{int(w[-1,1])}, deaths {int(w[:,2].sum())}, splits {int(w[:,3].sum())}, nucleations {int(w[:,4].sum())}")
