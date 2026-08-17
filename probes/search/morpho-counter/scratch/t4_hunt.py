
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
import numpy as np
from morpho_sim import simulate
from hier_metrics import compact_top_fit

base = dict(ny=8, nx=96, dx=1.0, dt=0.05, a=0.1, b=0.9, Du=1.0, Dv=25.0, Dc=0.5,
            sigma=1.0, mode="auto", steps=40000, meas_every=50, seed=1,
            k_ref=0.6, C0=1.0, t_on=250.0)
# hunting window guess from calibration: branch7 S in [0.23,0.34], branch8 min ~0.44?
for eps, kstar2 in [(3e-4, 0.38), (1e-3, 0.38), (3e-3, 0.38), (1e-3, 0.30), (1e-3, 0.45), (3e-3, 0.55)]:
    t0=time.time()
    r = simulate(dict(base, eps=eps, kstar2=kstar2))
    el = time.time()-t0
    m = r["t"] >= 500  # post-transient
    n = r["n"][m]
    ft = compact_top_fit(n, dt=2.5)
    flips = int((np.diff(n)!=0).sum())
    print("eps=%.0e k*2=%.2f: n uniq=%s flips=%d Cm range=[%.2f,%.2f] top=%s r2=%.3f %s (%.0fs)"
          % (eps, kstar2, np.unique(n).astype(int), flips, r["Cm"][m].min(), r["Cm"][m].max(),
             ft["model"], ft["r2"], ft["params"], el))
