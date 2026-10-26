"""(c34) Do daughters inherit the contents? For every track born by a split (labkit tracker, as swimdivide.py),
cargo inside/outside by signed distance (inside d<=-1, outside 2<=d<=4 px, own pixels nearest to the body) at
5 frames after birth and in the middle of its life; prints the medians and the fraction >= 2.
usage: inherit.py frames.npz world.py [channel=3]"""
import sys, importlib.util, numpy as np
from scipy import ndimage
sys.path.insert(0, __file__.rsplit("/collective/", 1)[0])
from labkit import run as LR, metrics as M
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32); R = F["render"].astype(np.float32); rf = list(F["render_f"])
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
ch = int(sys.argv[3]) if len(sys.argv) > 3 else 3
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True)
ridx = {f: i for i, f in enumerate(rf)}


def ratio(f, cy, cx):
    k = ridx.get(f)
    if k is None: return np.nan
    ins = R[k, 0] > 0; lab, n = ndimage.label(ins)
    j = lab[int(round(cy)) % H, int(round(cx)) % Wd]
    if j == 0: return np.nan
    d = np.where(ins, -ndimage.distance_transform_edt(ins), ndimage.distance_transform_edt(~ins))
    _, (iy, ix) = ndimage.distance_transform_edt(lab == 0, return_indices=True); own = lab[iy, ix] == j
    a, b = own & (d <= -1), own & (d >= 2) & (d <= 4)
    if a.sum() == 0 or b.sum() == 0: return np.nan
    return R[k, ch][a].mean() / max(R[k, ch][b].mean(), 1e-9)


e5, mid = [], []
for t in tracks:
    if t["birth"] != "split" or len(t["cy"]) < 12: continue
    e5.append(ratio(t["start"] + 5, t["cy"][5], t["cx"][5])); m = len(t["cy"]) // 2
    mid.append(ratio(t["start"] + m, t["cy"][m], t["cx"][m]))
e5, mid = np.array(e5), np.array(mid)
for name, v in (("5 frames after birth", e5), ("mid-life", mid)):
    v = v[np.isfinite(v)]
    print(f"{sys.argv[1]}: daughters (born by split, >= 12 frames) {name}: n={len(v)}, median in/out {np.median(v):.2f}, fraction >= 2: {(v >= 2).mean():.2f}")
