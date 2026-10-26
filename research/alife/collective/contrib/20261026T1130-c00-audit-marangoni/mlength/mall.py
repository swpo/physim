"""All tracks living >= K frames: net in labkit BL and in median-Feret rod lengths, with birth and fate (split with
>= 2 lasting children, merge, other split, run end). usage: mall.py frames.npz world.py [K=20]"""
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
rows = []
for t in tracks:
    n = len(t["cy"])
    if n < K: continue
    sy = M._wrap(np.diff(t["cy"]), H); sx = M._wrap(np.diff(t["cx"]), Wd)
    net = float(np.hypot(sy.sum(), sx.sum())); size = np.sqrt(np.mean(t["area"]))
    fer = []
    for k in range(0, n, max(1, n // 25)):
        m = comps[t["start"] + k]["lab"] == t["comp"][k] + 1
        ys, xs = np.nonzero(m); dy = M._wrap(ys - t["cy"][k], H); dx = M._wrap(xs - t["cx"][k], Wd)
        lam, vec = np.linalg.eigh(np.cov(np.vstack([dy, dx]))); v = vec[:, -1]; q = dy * v[0] + dx * v[1]
        fer.append(q.max() - q.min() + 1)
    fm = float(np.median(fer))
    kids = t["children"]
    lasting = [c for c in kids if byid[c]["birth"] == "split" and byid[c]["end"] - byid[c]["start"] + 1 >= K]
    if t["end"] == T - 1: fate = "run-end"
    elif len(lasting) >= 2: fate = "divides"
    elif kids and byid[kids[0]]["birth"] == "merge": fate = "merges"
    elif kids: fate = "split-other"
    else: fate = "vanishes"
    rows.append((net / fm, net / size, t["id"], t["birth"], fate, n, round(net, 1), round(fm, 1)))
rows.sort(key=lambda r: -r[0])
print(sys.argv[1], "tracks >= K frames:", len(rows))
from collections import Counter
print(" >=3 rod lengths (median Feret):", sum(r[0] >= 3 for r in rows), Counter(r[4] for r in rows if r[0] >= 3), Counter(r[3] for r in rows if r[0] >= 3))
print(" >=3 labkit BL:", sum(r[1] >= 3 for r in rows), Counter(r[4] for r in rows if r[1] >= 3))
for r in rows[:10]: print(f"  id {r[2]} birth {r[3]} fate {r[4]} life {r[5]} net {r[6]} Fmed {r[7]} rodL {r[0]:.2f} labkitBL {r[1]:.2f}")
