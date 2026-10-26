"""(c34) Selection or contagion? Follows every labkit track (labkit tracker on phi) and reads its kind (fA over the
rod and a 2 px shell, A > 0.8, B < 0.2) at each render frame of its life. Reports tracks that switch kind
(A->B or B->A) between their first and last pure reading, persistent splits by parent kind, and merges by kind
of the merging tracks. usage: switches.py frames.npz world.py"""
import sys, importlib.util, numpy as np
from scipy import ndimage
sys.path.insert(0, __file__.rsplit("/collective/", 1)[0])
from labkit import run as LR, metrics as M
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32); R = F["render"].astype(np.float32); rf = list(F["render_f"])
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True)
lin = M.lineage_stats(tracks, ev, len(mat), 1.0, (H, Wd), True, K=20)
ridx = {f: i for i, f in enumerate(rf)}
cache = {}


def kindmap(k):
    if k not in cache:
        ins = R[k, 0] > 0; lab, n = ndimage.label(ins); big = ndimage.grey_dilation(lab, size=(5, 5))
        a = ndimage.sum(R[k, 2], big, range(1, n + 1)); b = ndimage.sum(R[k, 3], big, range(1, n + 1))
        cache[k] = (lab, a / np.maximum(a + b, 1e-12))
    return cache[k]


def kind(t, f):
    k = ridx.get(f)
    if k is None: return None
    lab, fa = kindmap(k); i = f - t["start"]
    j = lab[int(round(t["cy"][i])) % H, int(round(t["cx"][i])) % Wd]
    if j == 0: return None
    v = fa[j - 1]
    return "A" if v > 0.8 else "B" if v < 0.2 else "m"


K = {}; sw = []
for t in tracks:
    ks = [kind(t, f) for f in range(t["start"], t["end"] + 1)]
    pure = [x for x in ks if x in ("A", "B")]
    if not pure: continue
    K[t["id"]] = pure[-1]
    if pure[0] != pure[-1]: sw.append((t["id"], pure[0], pure[-1], t["start"], t["end"]))
ps = {"A": 0, "B": 0}
for e in lin["persistent_splits"] if isinstance(lin, dict) and "persistent_splits" in lin else []:
    p = K.get(e["parent"])
    if p in ps: ps[p] += 1
mg = {"AA": 0, "BB": 0, "AB": 0}
byid = {t["id"]: t for t in tracks}
for t in tracks:
    if t["birth"] == "merge" and len(t["parents"]) >= 2:
        kk = sorted(K.get(p, "?") for p in t["parents"])
        key = "".join(kk[:2])
        if key in ("AA", "BB"): mg[key] += 1
        elif set(kk) >= {"A", "B"}: mg["AB"] += 1
print(f"{sys.argv[1]}: {len(K)} tracks with a pure kind; kind switches along a track: {len(sw)} {sw[:8]}")
print(f"  persistent splits by parent kind: {ps}; merges by kinds of the merging tracks: {mg}")
