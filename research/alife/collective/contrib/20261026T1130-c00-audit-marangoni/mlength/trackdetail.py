"""Per-frame detail of chosen tracks: step, angle between step and rod axis, area, Feret, nearest other body (gap px).
usage: trackdetail.py frames.npz world.py id1,id2,..."""
import sys, importlib.util, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
from scipy.spatial import cKDTree
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32)
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True)
for tid in [int(x) for x in sys.argv[3].split(",")]:
    t = tracks[tid]; L = len(t["cy"]); print(f"track {tid} frames {t['start']}-{t['end']} birth {t['birth']} parents {t['parents']} children {t['children']}")
    sy = M._wrap(np.diff(t["cy"]), H); sx = M._wrap(np.diff(t["cx"]), Wd)
    along = 0.0; across = 0.0
    for k in range(L):
        f = t["start"] + k; lab = comps[f]["lab"]; m = lab == t["comp"][k] + 1
        ys, xs = np.nonzero(m); P = np.vstack([M._wrap(ys - t["cy"][k], H), M._wrap(xs - t["cx"][k], Wd)]).T
        w, v = np.linalg.eigh(np.cov(P.T)); ax = v[:, -1]
        other = np.argwhere((lab > 0) & ~m)
        gap = cKDTree(other, boxsize=(H, Wd)).query(np.argwhere(m))[0].min() if len(other) else np.nan
        if k < L - 1:
            s = np.array([sy[k], sx[k]]); st = np.hypot(*s); c = abs(s @ ax) / max(st, 1e-9)
            along += abs(s @ ax); across += np.sqrt(max(st**2 - (s @ ax)**2, 0))
        else:
            st, c = np.nan, np.nan
        if k % max(1, L // 25) == 0 or (k < L - 1 and st > 2.5):
            print(f"  k{k:3d} f{f:3d} area {int(m.sum()):4d} 4sqrtlam {4*np.sqrt(w[-1]):5.1f} step {st:5.2f} |cos(step,axis)| {c:4.2f} gap {gap:5.1f}")
    print(f"  summed |step . axis| {along:.1f}, summed step across axis {across:.1f}")
