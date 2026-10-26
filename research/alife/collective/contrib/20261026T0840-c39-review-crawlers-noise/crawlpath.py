"""(c39) For every labkit track (same segmentation/tracker as labkit.run) alive >= 10 frames: net displacement,
path length and the largest displacement over any window, in body diameters (2 sqrt(area/pi)); also the mean
polarity asymmetry is not used. usage: crawlpath.py frames.npz world.py"""
import sys, importlib.util, numpy as np
sys.path.insert(0, __file__.rsplit("/collective/", 1)[0])
from labkit import run as LR, metrics as M
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32)
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True)
rows = []
for t in tracks:
    n = t["end"] - t["start"] + 1
    if n < 10: continue
    cy = np.unwrap(np.array(t["cy"]) * 2 * np.pi / H) * H / (2 * np.pi); cx = np.unwrap(np.array(t["cx"]) * 2 * np.pi / Wd) * Wd / (2 * np.pi)
    D = 2 * np.sqrt(np.mean(t["area"]) / np.pi)
    net = np.hypot(cy[-1] - cy[0], cx[-1] - cx[0]); path = np.hypot(np.diff(cy), np.diff(cx)).sum()
    mx = max(np.hypot(cy[j] - cy[i], cx[j] - cx[i]) for i in range(n) for j in range(i, n))
    rows.append((mx / D, t["id"], t["start"], t["end"], t.get("birth"), D, net / D, path / D))
for r in sorted(rows, reverse=True)[:6]:
    print(f"track {r[1]} frames {r[2]}-{r[3]} birth {r[4]} diameter {r[5]:.1f}px: net {r[6]:.2f} D, path {r[7]:.2f} D, max excursion {r[0]:.2f} D")
