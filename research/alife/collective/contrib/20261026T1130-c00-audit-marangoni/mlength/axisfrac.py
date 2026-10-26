"""For dividing tracks: step-weighted mean |cos(step, long axis)| and fraction of path along the axis. usage: axisfrac.py frames.npz world.py"""
import sys, importlib.util, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32)
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True); byid = {t["id"]: t for t in tracks}
out = []
for t in tracks:
    kids = [c for c in t["children"] if byid[c]["birth"] == "split" and byid[c]["end"] - byid[c]["start"] + 1 >= 20]
    L = len(t["cy"])
    if len(kids) < 2 or L < 5: continue
    sy = M._wrap(np.diff(t["cy"]), H); sx = M._wrap(np.diff(t["cx"]), Wd); st = np.hypot(sy, sx)
    net = np.hypot(sy.sum(), sx.sum()); size = np.sqrt(np.mean(t["area"]))
    al = 0.0
    for k in range(L - 1):
        f = t["start"] + k; m = comps[f]["lab"] == t["comp"][k] + 1; ys, xs = np.nonzero(m)
        P = np.vstack([M._wrap(ys - t["cy"][k], H), M._wrap(xs - t["cx"][k], Wd)])
        ax = np.linalg.eigh(np.cov(P))[1][:, -1]; al += abs(sy[k] * ax[0] + sx[k] * ax[1])
    out.append((net / size, al / st.sum()))
out = np.array(out)
for lo_ in (0, 3):
    s = out[out[:, 0] >= lo_]
    print(f"{sys.argv[1].split('/')[-2]}: tracks with labkit BL >= {lo_}: n={len(s)}, path fraction along the long axis: median {np.median(s[:,1]):.2f}, min {s[:,1].min():.2f}")
