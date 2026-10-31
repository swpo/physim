"""How long each variant tracks the native trajectory from the same initial state (light; no simulation).
Relative RMS difference of the 128^2 matter frames, variant vs native, against two seeds (decorrelated level)."""
import json
import numpy as np
out = {}
for w, ts, fdt in (("pm", (100, 250, 500, 1000, 2000, 4000, 8000), 50.0), ("fv", (15, 30, 60, 90, 150, 300, 600, 1500), 3.0)):
    def mat(p):
        z = np.load(p); r = z["rec"]
        return np.abs(r).astype(np.float64) if w == "fv" else r[:, 0].astype(np.float64)
    dt0 = "dtdef"
    vs = {"pm": ["N128_dt0.5", "N192_dt0.5", "N256_dt0.25"], "fv": ["N128_dt0.01", "N192_dtdef"]}[w]
    res = {}
    for s in (11, 12):
        a = mat(f"runs/{w}_s{s}_N128_{dt0}_rot0.npz")
        other = mat(f"runs/{w}_s{23 - s}_N128_{dt0}_rot0.npz")
        rel = lambda b, f: float(np.sqrt(((a[f] - b[f]) ** 2).mean() / (0.5 * (a[f] ** 2).mean() + 0.5 * (b[f] ** 2).mean())))
        for v in vs:
            b = mat(f"runs/{w}_s{s}_{v}_rot0.npz")
            res[f"s{s} {v}"] = {str(t): round(rel(b, int(round(t / fdt))), 3) for t in ts}
        res[f"s{s} other seed"] = {str(t): round(rel(other, int(round(t / fdt))), 3) for t in ts}
    out[w] = res
    print(w)
    for k, v in res.items():
        print(f"  {k:18s}", v)
json.dump(out, open("tracking.json", "w"), indent=1)
