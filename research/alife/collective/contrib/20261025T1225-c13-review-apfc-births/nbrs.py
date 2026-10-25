"""c13: for each peak birth (births.py rule), count the earlier peaks within 12 px (one lattice spacing ~9.2 px + slack).
Triangle completion predicts >= 2 parents; a single-peak division would show births with exactly 1 earlier peak nearby."""
import sys, os, json, importlib.util, numpy as np
from scipy import ndimage
N = int(os.environ.get("NGRID", "128")); os.environ["WORLD_P"] = sys.argv[1]; T = int(sys.argv[2]); seed = int(sys.argv[3])
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py"))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, (N, N)); prev = None; nn = []
def peaks(p):
    return np.argwhere((p == ndimage.maximum_filter(p, size=7, mode="wrap")) & (p > 0.0))
def dists(a, B):
    d = np.abs(B - a); d = np.minimum(d, N - d); return np.hypot(d[:, 0], d[:, 1])
for n in range(1, T + 1):
    w.step(s)
    if n % 20 == 0 and n * w.P["dt"] >= 60:
        pk = peaks(s["phi"])
        if prev is not None:
            for a in pk:
                d = dists(a, prev)
                if d.min() > 3: nn.append(int((d <= 12).sum()))
        prev = pk
nn = np.array(nn)
print(json.dumps({"P": sys.argv[1], "seed": seed, "N": N, "births": len(nn), "parents_within_12px_hist": {int(k): int((nn == k).sum()) for k in np.unique(nn)}}))
