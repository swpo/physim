"""c19: count walled cells over time in labkit frames.npz of pcell-mwall-b42 runs. A cell = a connected
(periodic-agnostic) component of the labkit matter mask (frames.npz 'matter', i.e. what labkit segments) with
>= 12 px; counted in the left (x < 64) and right halves by centroid. usage: cellcount.py label=run_dir ..."""
import sys, json, numpy as np
from scipy import ndimage
for arg in sys.argv[1:]:
    lab, d = arg.split("="); F = np.load(d + "/frames.npz"); spf = json.load(open(d + "/metrics.json"))["steps_per_frame"]
    m = F["matter"]; out = []
    for i in range(0, len(m), 2):
        L, n = ndimage.label(m[i] > 0.5); a = np.bincount(L.ravel())[1:]
        cs = ndimage.center_of_mass(np.ones_like(L), L, [j + 1 for j in range(n) if a[j] >= 12]) if n else []
        left = sum(1 for c in cs if c[1] < 64); out.append((i * spf, len(cs), left, len(cs) - left))
    print(lab + ": " + ", ".join(f"t={t}: {n} ({l}L/{r}R)" for t, n, l, r in out if t >= 50000 and (t % 4000 == 0 or 59000 <= t <= 64000)))
