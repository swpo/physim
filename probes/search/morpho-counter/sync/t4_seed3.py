
"""t4_seed3.py -- in-tongue R=1.3 seed=3: transient or true wander?"""
import sys
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
import numpy as np
from sync_sim import simulate2
from sync_metrics import l4_analysis

BASE = dict(ny=8, nx=64, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=11.0,
            Dc=10.0, sigma=1.0, kstar2=0.2682)
R, eps_g = 1.3, 2.4e-3
p = dict(BASE, eps1=eps_g*np.sqrt(R), eps2=eps_g/np.sqrt(R), kappa_c=2e-3,
         steps=400000, meas_every=25, seed=3, noise_amp=2e-3)
r = simulate2(p)
for cut in [2000.0, 10000.0, 20000.0]:
    a = l4_analysis(r["t"], r["nz"][:, 0], r["nz"][:, 1], t_cut=cut)
    print("t_cut=%d: slips=%s exc=%s net=%s rho=%s locked=%s span_cyc=%.1f"
          % (cut, a.get("n_slips"), round(a.get("max_exc"),3), round(a.get("net_wind"),3),
             round(a.get("rho"),4), a.get("locked"),
             a["span"]/ (0.5*(a["T1"]+a["T2"]))), flush=True)
