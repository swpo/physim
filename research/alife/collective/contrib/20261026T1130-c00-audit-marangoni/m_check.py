"""M check on the swim-then-divide tracks (same selection as the claim's swimdivide.py: tracks ending in a split with
>= 2 children living >= K frames). For each, net displacement in labkit body lengths (net / sqrt(mean area)) and rod
lengths (net / mean major axis, 4 sqrt(lambda_max)), the largest single-frame centroid step, the number of merges the
track went through (parents absorbed mid-life), and the path straightness (net / path length).
usage: m_check.py frames.npz world.py [K=20]"""
import sys, importlib.util, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32)
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
K = int(sys.argv[3]) if len(sys.argv) > 3 else 20
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True); byid = {t["id"]: t for t in tracks}
def rodlen(t):
    Ls = []
    for f in range(t["start"], t["end"] + 1):
        lab = comps[f]["lab"]; m = lab == t["comp"][f - t["start"]] + 1
        ys, xs = np.nonzero(m); cy, cx = t["cy"][f - t["start"]], t["cx"][f - t["start"]]
        lam = np.linalg.eigvalsh(np.cov(np.vstack([M._wrap(ys - cy, H), M._wrap(xs - cx, Wd)])))
        Ls.append(4 * np.sqrt(max(lam[-1], 0)))
    return float(np.mean(Ls))
rows = []
for t in tracks:
    kids = [c for c in t["children"] if byid[c]["birth"] == "split" and byid[c]["end"] - byid[c]["start"] + 1 >= K]
    if len(kids) < 2 or len(t["cy"]) < 5: continue
    sy = M._wrap(np.diff(t["cy"]), H); sx = M._wrap(np.diff(t["cx"]), Wd); st = np.hypot(sy, sx)
    net = float(np.hypot(sy.sum(), sx.sum())); size = float(np.sqrt(np.mean(t["area"]))); L = rodlen(t)
    mrg = sum(1 for e in ev if e.get("type") == "merge" and e.get("child", e.get("into")) == t["id"]) if isinstance(ev, list) and ev and isinstance(ev[0], dict) else -1
    rows.append((t["id"], t["birth"], t["end"] - t["start"] + 1, round(net, 1), round(net / size, 2), round(net / L, 2), round(L, 1), round(float(st.max()), 2), round(net / max(st.sum(), 1e-9), 2), len(t.get("parents", []))))
rows.sort(key=lambda r: -r[4])
print(f"{sys.argv[1]}: {len(rows)} tracks end in a split with 2 children living >= {K} frames")
print(f"  >= 3 labkit body lengths: {sum(r[4] >= 3 for r in rows)}; >= 3 rod lengths (all-frame mean major axis): {sum(r[5] >= 3 for r in rows)}; >= 2 rod lengths: {sum(r[5] >= 2 for r in rows)}")
print("  id birth life_frames net bl_labkit bl_rod rodlen max_step straightness n_parents")
for r in rows[:12]: print("  ", *r)
