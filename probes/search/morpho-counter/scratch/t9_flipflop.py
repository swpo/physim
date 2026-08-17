
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
import numpy as np
from morpho_sim import simulate
from hier_metrics import compact_top_fit, macro_period_quality

# Flip-flop counter: kstar2 between measured S plateaus of n=5 (0.227) and n=6 (0.309)
base = dict(ny=8, nx=64, dx=1.0, dt=0.05, a=0.1, b=0.9, Du=1.0, Dv=11.0, Dc=10.0,
            sigma=1.0, mode="auto", steps=60000, meas_every=50, seed=1,
            k_ref=0.62, C0=0.9, t_on=250.0, kstar2=0.268, noise_amp=2e-3,
            Cmin=0.5, Cmax=1.8)
for eps in [6e-4, 1.2e-3, 2.4e-3]:
    t0=time.time(); r = simulate(dict(base, eps=eps)); el=time.time()-t0
    m = r["t"] >= 300
    n = r["nz"][m]; t = r["t"][m]
    flips = np.where(np.diff(n)!=0)[0]
    ft = compact_top_fit(n, dt=2.5)
    pq = macro_period_quality(r["Cm"][m], dt=2.5)
    print("eps=%.1e: uniq=%s flips=%d Cm=[%.2f,%.2f] top=%s r2=%.3f params=%s | C-osc period=%s q=%.2f (%.0fs)"
          % (eps, np.unique(n).astype(int), len(flips), r["Cm"][m].min(), r["Cm"][m].max(),
             ft["model"], ft["r2"], ft["params"], pq["period"], pq["q"], el))
    print("   flip t:", [int(t[i]) for i in flips[:18]], "-> n:", [int(n[i+1]) for i in flips[:18]])
