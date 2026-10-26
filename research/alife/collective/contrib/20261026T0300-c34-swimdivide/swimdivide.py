"""(c34) Same-individual swim-then-divide test on a labkit frames.npz, with labkit's own segmentation and
tracker (labkit.run._normalize_matter/_segment_frames, labkit.metrics.track; META threshold 0 and smooth 0.5).
For every track that ends in a split (>= 2 children that each live >= K frames), report the net displacement
over the track's life in body lengths, both labkit's (net / sqrt(mean area)) and by rod length (net / mean
major-axis length, 4 sqrt(lambda_max) of the pixel covariance). Prints the tracks that move >= 3 labkit body
lengths and then divide, and the best ones. usage: swimdivide.py frames.npz world.py [K=20] [dx=1]"""
import sys, json, importlib.util, numpy as np
sys.path.insert(0, __file__.rsplit("/collective/", 1)[0])
from labkit import run as LR, metrics as M
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32)
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
K = int(sys.argv[3]) if len(sys.argv) > 3 else 20
meta = W.META
mn, thr, lo, hi = LR._normalize_matter(mat, meta, True, meta.get("threshold"))
H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, events = M.track(comps, links, (H, Wd), True)
byid = {t["id"]: t for t in tracks}


def rodlen(t):
    Ls = []
    for f in range(t["start"], t["end"] + 1, max(1, (t["end"] - t["start"]) // 6)):
        lab = comps[f]["lab"]; cy, cx = t["cy"][f - t["start"]], t["cx"][f - t["start"]]
        j = lab[int(round(cy)) % H, int(round(cx)) % Wd]
        if j == 0: continue
        ys, xs = np.nonzero(lab == j)
        dy = M._wrap(ys - cy, H); dxx = M._wrap(xs - cx, Wd)
        lam = np.linalg.eigvalsh(np.cov(np.vstack([dy, dxx])))
        Ls.append(4 * np.sqrt(max(lam[-1], 0)))
    return float(np.mean(Ls)) if Ls else float("nan")


rows = []
for t in tracks:
    kids = [c for c in t["children"] if byid[c]["birth"] == "split" and byid[c]["end"] - byid[c]["start"] + 1 >= K]
    if len(kids) < 2 or len(t["cy"]) < 5: continue
    dy = M._wrap(np.diff(t["cy"]), H).sum(); dxx = M._wrap(np.diff(t["cx"]), Wd).sum()
    net = float(np.hypot(dy, dxx)); size = float(np.sqrt(np.mean(t["area"])))
    rows.append(dict(id=t["id"], start=t["start"], end=t["end"], birth=t["birth"], children=kids, net=round(net, 1),
                     bl_labkit=round(net / size, 2), bl_rod=round(net / rodlen(t), 2)))
rows.sort(key=lambda r: -r["bl_labkit"])
print(f"{sys.argv[1]}: {len(tracks)} tracks, {len(rows)} end in a split with 2 children living >= {K} frames")
print(f"  tracks that move >= 3 labkit body lengths, then divide: {sum(r['bl_labkit'] >= 3 for r in rows)}; by rod length >= 3: {sum(r['bl_rod'] >= 3 for r in rows)}")
for r in rows[:6]: print("  ", json.dumps(r))
