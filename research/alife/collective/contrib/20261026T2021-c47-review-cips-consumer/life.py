"""c47: lifetimes of consumer (q>0.5) and prey (c_a>0.5 render channel 0) bodies by frame-to-frame overlap
(a body continues into the next-frame body it overlaps most; at a split the larger daughter continues; a body
that overlaps nothing ends). Bodies >= 4 px. usage: python life.py frames.npz CH"""
import sys, numpy as np
from scipy import ndimage
MIN = int(sys.argv[3]) if len(sys.argv) > 3 else 4
z = np.load(sys.argv[1]); R = z["render"]; fi = z["render_f"]; ch = int(sys.argv[2]); dtf = 100.0
labs = []
for k in range(len(R)):
    l, n = ndimage.label(R[k][ch] > 0.5); sz = ndimage.sum(np.ones_like(l), l, range(1, n + 1))
    for i, s in enumerate(sz):
        if s < MIN: l[l == i + 1] = 0
    labs.append(l)
age = {}; ended = []
for k in range(len(labs)):
    cur = {i: 1 for i in np.unique(labs[k]) if i}
    if k > 0:
        prev = labs[k - 1]; claimed = {}
        for j, a in age.items():
            ov = labs[k][prev == j]; ov = ov[ov > 0]
            if len(ov) == 0: ended.append(a); continue
            v, c = np.unique(ov, return_counts=True); tgt = v[np.argmax(c)]
            if claimed.get(tgt, 0) < a: claimed[tgt] = a
        for tgt, a in claimed.items(): cur[tgt] = a + 1
    age = cur
alive = list(age.values())
L = np.array(ended + alive) * dtf
print("frame dt", dtf, "n tracks", len(L), "median life", np.median(L), "p90", np.percentile(L, 90), "max", L.max(),
      "n >= 2000 t", int((L >= 2000).sum()), "n >= 4000 t", int((L >= 4000).sum()))
