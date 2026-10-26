import sys, importlib.util, numpy as np
sys.path.insert(0, __file__.rsplit("/collective/", 1)[0])
from labkit import run as LR, metrics as M
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32)
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True)
A, V, PH = [], [], []
for t in tracks:
    L = len(t["cy"])
    if L < 15: continue
    cy, cx = np.array(t["cy"]), np.array(t["cx"]); a = np.array(t["area"])
    for i in range(0, L - 5, 5):
        d = np.hypot(M._wrap(cy[i+5]-cy[i], H), M._wrap(cx[i+5]-cx[i], Wd)) / 5
        A.append(a[i]); V.append(d); PH.append(i / L)
A, V, PH = map(np.array, (A, V, PH))
for lo_, hi_ in [(0, 40), (40, 60), (60, 80), (80, 100), (100, 300)]:
    m = (A >= lo_) & (A < hi_); print(f"area {lo_}-{hi_}: n={m.sum()}, mean px/frame {V[m].mean():.3f}" if m.sum() else "")
for lo_ in [0, .25, .5, .75]:
    m = (PH >= lo_) & (PH < lo_ + .25); print(f"life phase {lo_}: mean px/frame {V[m].mean():.3f}")
