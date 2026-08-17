
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
import numpy as np
from morpho_sim import simulate, turing_info

for Dv in [9.0, 10.0, 11.0, 12.0, 15.0, 25.0]:
    ti = turing_info(0.1, 0.9, 1.0, Dv)
    L = 64
    print("Dv=%4.1f growth=%.4f k_c=%.3f band=[%.3f,%.3f] ratio=%.2f  n range on L=64: [%.1f, %.1f]"
          % (Dv, ti["growth"], ti["k_max"], ti["k_lo"], ti["k_hi"], ti["k_hi"]/ti["k_lo"],
             ti["k_lo"]*L/(2*np.pi), ti["k_hi"]*L/(2*np.pi)))

# 1D branch scan at Dv=11, L=64: which n at which fixed C, S levels
base = dict(ny=1, nx=64, dx=1.0, dt=0.05, a=0.1, b=0.9, Du=1.0, Dv=11.0, Dc=10.0,
            sigma=1.0, mode="auto", eps=0.0, steps=16000, meas_every=100, seed=1, k_ref=0.62)
print("\n1D fixed-C branches (Dv=11, L=64), from random init:")
t0=time.time()
for C0 in np.arange(0.70, 1.55, 0.1):
    r = simulate(dict(base, C0=C0))
    k_n2 = (2*np.pi*r["nz"][-1]/64)**2
    print("C0=%.2f -> n=%2d  S=%.4f k_n^2=%.4f ratio=%.2f amp=%.3f" %
          (C0, r["nz"][-1], r["Sm"][-1], k_n2, r["Sm"][-1]/max(k_n2,1e-9), r["amp"][-1]))
print("%.1fs" % (time.time()-t0))
