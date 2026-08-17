
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
import numpy as np
from morpho_sim import simulate, turing_info

base = dict(ny=8, nx=96, dx=1.0, dt=0.05, a=0.1, b=0.9, Du=1.0, Dv=25.0, Dc=0.5,
            sigma=1.0, mode="auto", eps=0.0, kstar2=0.0, steps=12000,
            meas_every=50, seed=1, k_ref=0.6)
ti = turing_info(0.1, 0.9, 1.0, 25.0)
print("k_c=%.3f -> n_c(L=96)=%.2f" % (ti["k_max"], ti["k_max"]*96/(2*np.pi)))
# calibrate S(n): fixed C (eps=0) at several C values
for C0 in [0.8, 0.9, 1.0, 1.1, 1.2, 1.3]:
    p = dict(base, C0=C0)
    t0=time.time(); r = simulate(p); el=time.time()-t0
    k_n = 2*np.pi*r["n"][-1]/96
    print("C0=%.2f -> n=%2d nz=%2d  S=%.4f  k_n^2=%.4f  bias=%.2fx  amp=%.3f  (%.1fs)"
          % (C0, r["n"][-1], r["nz"][-1], r["Sm"][-1], k_n**2, r["Sm"][-1]/k_n**2, r["amp"][-1], el))
