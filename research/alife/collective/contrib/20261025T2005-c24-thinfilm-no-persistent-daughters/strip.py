"""Save height snapshots of world.py runs for figures. usage: strip.py world.py out.npz json seed nsteps t_first every"""
import sys, os, json, importlib.util, numpy as np
wp, out, pj, seed, N, t0, ev = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]); L = int(sys.argv[8]) if len(sys.argv) > 8 else 128
os.environ["WORLD_P"] = pj
spec = importlib.util.spec_from_file_location("w", wp); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, (L, L)); H, Pm, ts = [], [], []
for i in range(1, N + 1):
    s = w.step(s)
    if i >= t0 and (i - t0) % ev == 0:
        f = w.fields(s); H.append(f[0]); Pm.append(f[1]); ts.append(i * w.P["dt"])
np.savez_compressed(out, h=np.array(H, np.float32), p=np.array(Pm, np.float32), t=np.array(ts), mass=float(s["h"].mean()))
print(out, "final mass", s["h"].mean(), "hmax", s["h"].max(), np.isfinite(s["h"]).all())
