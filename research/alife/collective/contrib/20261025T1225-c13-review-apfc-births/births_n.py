"""Peak births: local maxima of phi (> 0, 7-px window) every 2 t; a peak with no peak within 3 px in the previous
snapshot is a birth; report its distance to the nearest peak present in the previous snapshot (lattice spacing ~9 px)."""
import sys, os, json, importlib.util, numpy as np
from scipy import ndimage
N = int(os.environ.get("NGRID", "128")); os.environ["WORLD_P"] = sys.argv[1]; T = int(sys.argv[2]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, (N, N)); prev = None; dists = []; deaths = 0; counts = []
def peaks(p):
    m = (p == ndimage.maximum_filter(p, size=7, mode="wrap")) & (p > 0.0)
    return np.argwhere(m)
def dmin(a, B):
    d = np.abs(B - a); d = np.minimum(d, N - d); return np.hypot(d[:, 0], d[:, 1]).min() if len(B) else 1e9
for n in range(1, T + 1):
    w.step(s)
    if n % 20 == 0 and n * w.P["dt"] >= 60:
        pk = peaks(s["phi"]); counts.append((round(n * w.P["dt"]), len(pk)))
        if prev is not None:
            for a in pk:
                if dmin(a, prev) > 3: dists.append(round(float(dmin(a, prev)), 1))
            deaths += sum(1 for b in prev if dmin(b, pk) > 3)
        prev = pk
d = np.array(dists)
print(json.dumps({"P": sys.argv[1], "births": len(d), "deaths_or_lost": deaths, "birth_dist_median": float(np.median(d)) if len(d) else None,
  "share_births_within_12px_of_a_peak": round(float((d <= 12).mean()), 2) if len(d) else None, "counts": counts[::max(1, len(counts) // 8)]}))
