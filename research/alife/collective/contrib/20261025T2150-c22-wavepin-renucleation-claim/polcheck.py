"""Re-run the damaged arm and record the polarity offset |d| (rho*phi centroid minus phi centroid),
the rho contrast inside the cell (p90 - p10 of rho where phi > 0.5) and the polarized area."""
import sys, json, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, tcut, T = int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
s = w.init(seed, w.META["size"])
while s["t"] < tcut - 1e-9: s = w.step(s)
s["rng"] = np.random.default_rng(seed + 1000); s = w.cut(s)
dt = w.P["dt"]; out = []
while s["t"] < T - 1e-9:
    if round(s["t"] / dt) % 100 == 0:
        A = s["phi"].sum() * s["dx"] ** 2
        if A < 1e-3: out.append([s["t"], 0, 0, 0, 0]); break
        c, d = w.polarity(s); m = s["phi"] > 0.5; r = s["rho"][m]
        out.append([round(s["t"], 2), round(A, 3), round(float(((s["rho"] > 0.5) & m).sum() * s["dx"] ** 2), 3), round(float(np.hypot(*d)), 4), round(float(np.percentile(r, 90) - np.percentile(r, 10)), 3)])
    s = w.step(s)
print("t area polarized_area |d| rho_p90-p10")
for o in out: print(*o)
