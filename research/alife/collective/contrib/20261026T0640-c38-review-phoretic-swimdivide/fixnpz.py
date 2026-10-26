"""Wrap float32 positions that rounded up to exactly L back into [0, L) (cKDTree rejects x == L); writes <in>_w.npz."""
import sys, numpy as np
d = dict(np.load(sys.argv[1])); L = float(d["L"]); x = d["x"].astype(np.float64) % L
x[x >= L] = 0.0; d["x"] = x; n = sys.argv[1].replace(".npz", "_w.npz"); np.savez_compressed(n, **d); print(n, "wrapped")
