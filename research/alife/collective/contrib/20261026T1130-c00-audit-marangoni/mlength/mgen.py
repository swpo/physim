"""Generic: for tracks living >= Kmin frames, net displacement in labkit BL (net/sqrt(mean area)), in own long axes
(net / median Feret along the principal axis), in extents along the travel direction; aspect; dividing flag.
usage: mgen.py frames.npz world.py [K=20] [Kmin=20]"""
import sys, importlib.util, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32)
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
K = int(sys.argv[3]) if len(sys.argv) > 3 else 20; Kmin = int(sys.argv[4]) if len(sys.argv) > 4 else 20
meta = getattr(W, "META", {})
mn, thr, lo, hi = LR._normalize_matter(mat, meta, True, meta.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True); byid = {t["id"]: t for t in tracks}
rows = []
for t in tracks:
    n = len(t["cy"])
    if n < Kmin: continue
    sy = M._wrap(np.diff(t["cy"]), H); sx = M._wrap(np.diff(t["cx"]), Wd)
    net = float(np.hypot(sy.sum(), sx.sum())); size = np.sqrt(np.mean(t["area"]))
    u = np.array([sy.sum(), sx.sum()]) / max(net, 1e-9)
    fe, wi, ext = [], [], []
    for k in range(0, n, max(1, n // 25)):
        m = comps[t["start"] + k]["lab"] == t["comp"][k] + 1
        ys, xs = np.nonzero(m); dy = M._wrap(ys - t["cy"][k], H); dx = M._wrap(xs - t["cx"][k], Wd)
        lam, vec = np.linalg.eigh(np.cov(np.vstack([dy, dx]))); v = vec[:, -1]; w = vec[:, 0]
        q = dy * v[0] + dx * v[1]; r = dy * w[0] + dx * w[1]; p = dy * u[0] + dx * u[1]
        fe.append(q.max() - q.min() + 1); wi.append(r.max() - r.min() + 1); ext.append(p.max() - p.min() + 1)
    fm = float(np.median(fe))
    lasting = [c for c in t["children"] if byid[c]["birth"] == "split" and byid[c]["end"] - byid[c]["start"] + 1 >= K]
    rows.append(dict(id=t["id"], n=n, birth=t["birth"], div=len(lasting) >= 2, net=net, bl=net / size, bl_long=net / fm,
                     bl_travel=net / float(np.median(ext)), aspect=float(np.median(np.array(fe) / np.array(wi))), long_over_sqrtA=fm / size))
rows.sort(key=lambda r: -r["bl"])
print(sys.argv[1], f"tracks >= {Kmin} frames: {len(rows)}; dividing: {sum(r['div'] for r in rows)}")
if rows:
    print(f" median aspect {np.median([r['aspect'] for r in rows]):.2f}; median long/sqrt(area) {np.median([r['long_over_sqrtA'] for r in rows]):.2f}")
    for key in ["bl", "bl_long", "bl_travel"]:
        print(f" >=3 by {key}: all {sum(r[key] >= 3 for r in rows)}, dividing {sum(r[key] >= 3 and r['div'] for r in rows)}; best all {max(r[key] for r in rows):.2f}, best dividing {max([r[key] for r in rows if r['div']] or [0]):.2f}")
    for r in rows[:6]:
        print(f"  id {r['id']} life {r['n']} birth {r['birth']} div {r['div']} net {r['net']:.1f} BL {r['bl']:.2f} long {r['bl_long']:.2f} travel {r['bl_travel']:.2f} aspect {r['aspect']:.2f}")
