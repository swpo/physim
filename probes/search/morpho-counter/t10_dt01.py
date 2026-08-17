
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
import numpy as np
from morpho_sim import simulate

# 1) dt=0.1 equivalence check on the flip-flop
base = dict(ny=8, nx=64, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=11.0, Dc=10.0,
            sigma=1.0, mode="auto", steps=60000, meas_every=25, seed=1,
            k_ref=0.62, C0=0.9, t_on=250.0, kstar2=0.268, noise_amp=2e-3,
            Cmin=0.5, Cmax=1.8)
t0=time.time(); r = simulate(dict(base, eps=2.4e-3)); el=time.time()-t0
m = r["t"] >= 300
n = r["nz"][m]; t = r["t"][m]
flips = np.where(np.diff(n)!=0)[0]
print("dt=0.1 60k ticks (t=6000) in %.0fs: uniq=%s flips at t=%s -> n=%s"
      % (el, np.unique(n).astype(int), [int(t[i]) for i in flips], [int(n[i+1]) for i in flips]))
print("  amp range [%.3f,%.3f], any blowup: %s" % (r["amp"].min(), r["amp"].max(), "blown" in r))

# 2) branch calibration via seed_mode at fixed C=1.0 (does branch persist + S plateau?)
cal = dict(ny=8, nx=64, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=11.0, Dc=10.0,
           sigma=1.0, mode="auto", eps=0.0, steps=6000, meas_every=100, seed=1,
           k_ref=0.62, noise_amp=2e-3)
print("\nseeded-branch S plateaus at fixed C0=1.0 (Dv=11):")
for nm in [3,4,5,6,7,8,9]:
    r = simulate(dict(cal, C0=1.0, seed_mode=nm))
    print("  seed n=%d -> final n=%2d  S=%.4f amp=%.3f" % (nm, r["nz"][-1], r["Sm"][-1], r["amp"][-1]))
