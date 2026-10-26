"""Dividing tracks measured against the kind's body length: the population median Feret (long axis) of all
components >= min area in frames >= 20% of the run, and the median Feret at birth. usage: mpop.py frames.npz world.py [K]"""
import sys, importlib.util, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32)
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
K = int(sys.argv[3]) if len(sys.argv) > 3 else 20
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True); byid = {t["id"]: t for t in tracks}
T = len(comps)
def feret(f, j, cy, cx):
    m = comps[f]["lab"] == j + 1; ys, xs = np.nonzero(m)
    dy = M._wrap(ys - cy, H); dx = M._wrap(xs - cx, Wd)
    lam, vec = np.linalg.eigh(np.cov(np.vstack([dy, dx]))); v = vec[:, -1]; q = dy * v[0] + dx * v[1]
    return q.max() - q.min() + 1, np.sqrt(len(ys))
fs, sq = [], []
for f in range(int(0.2 * T), T, 5):
    for j in range(len(comps[f]["area"])):
        a, b = feret(f, j, comps[f]["cy"][j], comps[f]["cx"][j]); fs.append(a); sq.append(b)
Lpop = float(np.median(fs)); Spop = float(np.median(sq))
rows = []
for t in tracks:
    kids = [c for c in t["children"] if byid[c]["birth"] == "split" and byid[c]["end"] - byid[c]["start"] + 1 >= K]
    if len(kids) < 2 or len(t["cy"]) < 5: continue
    sy = M._wrap(np.diff(t["cy"]), H); sx = M._wrap(np.diff(t["cx"]), Wd); net = float(np.hypot(sy.sum(), sx.sum()))
    rows.append(net)
rows = np.array(sorted(rows, reverse=True))
print(sys.argv[1]); print(f" population median long axis {Lpop:.1f} px, median sqrt(area) {Spop:.1f} px, ratio {Lpop / Spop:.2f}")
print(f" dividing tracks {len(rows)}; net >= 3 x population long axis ({3 * Lpop:.1f} px): {(rows >= 3 * Lpop).sum()}; >= 2.5x: {(rows >= 2.5 * Lpop).sum()}; best {rows[0] / Lpop:.2f}")
print(" top nets (px):", np.round(rows[:6], 1).tolist())
