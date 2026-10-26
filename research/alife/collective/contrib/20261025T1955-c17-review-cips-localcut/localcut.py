"""c19: area of the target body (component of labkit's matter mask nearest the cut centre (128.5, 129.5)) and of bodies
inside / outside the cut disk, for the fed run and the two local-cut runs of seed 3. usage: localcut.py fed_dir label=dir r ..."""
import sys, json, numpy as np
from scipy import ndimage
cy, cx = 122.4, 129.5  # c17: seed 4 target (target_s4.json)
def load(d):
    F = np.load(d + "/frames.npz"); M = json.load(open(d + "/metrics.json")); return F["matter"], M["steps_per_frame"] * M["dt"]
def at(m, tf, t, r):
    i = int(round(t / tf)); L, n = ndimage.label(m[i] > 0.5); H, W = L.shape; a = np.bincount(L.ravel())
    yy, xx = np.mgrid[0:H, 0:W]; dd = np.hypot((yy - cy + H / 2) % H - H / 2, (xx - cx + W / 2) % W - W / 2)
    tgt = L[int(cy), int(cx)]; tgt_area = int(a[tgt]) if tgt > 0 else 0
    ins = out = 0
    for j in range(1, n + 1):
        if a[j] < 6: continue
        dj = dd[L == j].mean(); ins += dj < r - 3; out += dj >= r + 3
    return tgt_area, ins, out
fed = sys.argv[1]; mf, tff = load(fed)
for arg in sys.argv[2:]:
    lab, d, r = arg.split("="); r = float(r); m, tf = load(d)
    for t in (1500, 1700, 2000, 2500):
        a1, i1, o1 = at(m, tf, t, r); a0, i0, o0 = at(mf, tff, t, r)
        print(f"{lab} t={t}: target area {a1} (fed {a0}); bodies inside disk {i1} (fed {i0}); outside {o1} (fed {o0})")
