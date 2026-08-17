
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
import numpy as np
from morpho_sim import turing_info, simulate, steady_state

# dispersion sanity for a Schnakenberg stripe regime
for (a,b,Du,Dv) in [(0.05,1.0,1.0,25.0),(0.1,0.9,1.0,25.0),(0.1,0.9,1.0,40.0),(0.05,1.4,1.0,25.0)]:
    ti = turing_info(a,b,Du,Dv)
    print(f"a={a} b={b} Dv={Dv}: growth={ti['growth']:.4f} k_max={ti['k_max']:.3f} band=({ti['k_lo']},{ti['k_hi']}) hom_stable={ti['hom_stable']}")

# quick fixed-C run: does a stripe pattern form and get counted?
p = dict(ny=4, nx=96, dx=1.0, dt=0.05, a=0.1, b=0.9, Du=1.0, Dv=25.0, Dc=0.5,
         sigma=1.0, eps=0.0, kstar2=0.0, mode="auto", C0=1.0, steps=8000,
         meas_every=25, seed=1, k_ref=0.6)
t0=time.time()
r = simulate(p)
print("8k steps in %.2fs" % (time.time()-t0))
print("final n=%d purity=%.3f amp=%.4f Sm=%.4f (k_meas=%.3f)" % (r["n"][-1], r["purity"][-1], r["amp"][-1], r["Sm"][-1], np.sqrt(max(r["Sm"][-1],0))))
print("n(t) tail:", r["n"][-20:].astype(int))
print("expected n = k_max*L/2pi =", 0.62*96/(2*np.pi))
