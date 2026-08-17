
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
import numpy as np
from sync_sim import simulate2

# uncoupled check: two rings, eps1=3.2e-3, eps2=2.4e-3 -> T1~1190, T2~1580 by law
p = dict(ny=8, nx=64, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=11.0, Dc=10.0,
         sigma=1.0, kstar2=0.2682, eps1=3.2e-3, eps2=2.4e-3, kappa_c=0.0,
         steps=60000, meas_every=25, seed=1, noise_amp=2e-3)
t0 = time.time()
r = simulate2(p)
el = time.time() - t0
print("60k ticks 2 rings in %.1fs" % el)
for i in (0, 1):
    n = r["nz"][:, i]
    m = r["t"] >= 1000
    lev = (n[m] >= 5.5).astype(int)
    ch = np.where(np.diff(lev) != 0)[0]
    ups = r["t"][m][ch][np.array([lev[c+1] == 1 for c in ch])] if len(ch) else []
    per = np.median(np.diff(ups)) if len(ups) >= 2 else None
    print("ring %d: rungs %s, flips %d, period %s" % (i, np.unique(n[m]).astype(int), len(ch), per))
