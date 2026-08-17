
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
import numpy as np
from morpho_sim import simulate
from hier_metrics import compact_top_fit

L = 96
k2 = lambda n: (2*np.pi*n/L)**2
kap = 0.4
kstar2 = (1-kap)*k2(7) + kap*k2(8)
base = dict(ny=4, nx=L, dx=1.0, dt=0.05, a=0.1, b=0.9, Du=1.0, Dv=25.0, Dc=10.0,
            sigma=1.0, mode="auto", steps=60000, meas_every=50, seed=1,
            k_ref=0.6, C0=1.0, t_on=250.0, kstar2=kstar2, noise_amp=2e-3)
for eps in [0.004, 0.008, 0.016, 0.032]:
    t0=time.time(); r = simulate(dict(base, eps=eps)); el=time.time()-t0
    m = r["t"] >= 300
    n = r["nz"][m]; t = r["t"][m]
    flips = np.where(np.diff(n)!=0)[0]
    ft = compact_top_fit(n, dt=2.5)
    print("eps=%.3f: uniq=%s nflips=%d Cm=[%.2f,%.2f] top=%s r2=%.3f %s (%.0fs)"
          % (eps, np.unique(n).astype(int), len(flips), r["Cm"][m].min(), r["Cm"][m].max(),
             ft["model"], ft["r2"], ft["params"], el))
    print("   flips t:", [int(t[i]) for i in flips[:16]], "-> n:", [int(n[i+1]) for i in flips[:16]])
