"""(c45) Body count (labkit segmentation of the matter field) and occupancy per frame, printed around each famine
(season start 6000, period 2000; famine = last season_frac of each period). usage: series.py frames.npz world.py frac"""
import sys, importlib.util, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32)
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
frac = float(sys.argv[3]); FT = W.META["steps_per_frame"] * W.P["dt"]
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
n = [len(c["area"]) for c in comps]; occ = [float((m > thr).mean()) for m in mn]
print("frame t bodies occupancy")
for f in range(0, len(n), 5): print(f, int(f * FT), n[f], round(occ[f], 3))
print("before first famine (t 5900): bodies", n[59], "; at end:", n[-1], "; min bodies after t=6000:", min(n[60:]), "; max:", max(n[60:]))
