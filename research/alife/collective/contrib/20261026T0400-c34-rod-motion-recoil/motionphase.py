"""(c34) When in a rod's life does it move? For every labkit track (labkit tracker, as swimdivide.py) that lives
>= 40 frames, the displacement from its first position as a function of time since birth (frames), split by birth
type (split vs nucleation), and the net displacement over the first 10 / 20 / 40 frames and over the whole life;
also the mean frame-to-frame step in each decile of life. usage: motionphase.py frames.npz world.py [label]"""
import sys, importlib.util, numpy as np
sys.path.insert(0, __file__.rsplit("/collective/", 1)[0])
from labkit import run as LR, metrics as M
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32)
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True)
lab = sys.argv[3] if len(sys.argv) > 3 else sys.argv[1]
for birth in ["split", "nucleation"]:
    D = {10: [], 20: [], 40: [], "life": []}; dec = [[] for _ in range(10)]; n = 0
    for t in tracks:
        L = len(t["cy"])
        if L < 41 or t["birth"] != birth: continue
        n += 1
        y = np.concatenate([[0], np.cumsum(M._wrap(np.diff(t["cy"]), H))]); x = np.concatenate([[0], np.cumsum(M._wrap(np.diff(t["cx"]), Wd))])
        for k in (10, 20, 40): D[k].append(np.hypot(y[k], x[k]))
        D["life"].append(np.hypot(y[-1], x[-1]))
        st = np.hypot(np.diff(y), np.diff(x))
        for i in range(10): dec[i].append(st[int(i * (L - 1) / 10):int((i + 1) * (L - 1) / 10)].mean())
    if n == 0: continue
    print(f"{lab} birth={birth}: {n} tracks >= 40 frames; median net px after 10/20/40 frames and whole life: " + " / ".join(f"{np.median(D[k]):.1f}" for k in (10, 20, 40, "life")))
    print(f"   mean step px/frame by life decile: " + " ".join(f"{np.mean(d):.3f}" for d in dec))
