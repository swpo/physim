
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
import numpy as np
from morpho_sim import simulate

base = dict(ny=8, nx=96, dx=1.0, dt=0.05, a=0.1, b=0.9, Du=1.0, Dv=25.0, Dc=0.5,
            sigma=1.0, mode="auto", eps=0.0, steps=12000, meas_every=50,
            seed=1, k_ref=0.6)
print("recalibration of band-passed S(C) at fixed C:")
for C0 in [0.8, 0.9, 1.0, 1.1, 1.2, 1.3]:
    r = simulate(dict(base, C0=C0))
    k_n2 = (2*np.pi*r["n"][-1]/96)**2
    print("C0=%.2f -> n=%2d  S=%.4f  k_n^2=%.4f  ratio=%.2f" % (C0, r["n"][-1], r["Sm"][-1], k_n2, r["Sm"][-1]/k_n2))
