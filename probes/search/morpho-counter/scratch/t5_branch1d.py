
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
import numpy as np
from morpho_sim import simulate

base = dict(ny=1, nx=96, dx=1.0, dt=0.05, a=0.1, b=0.9, Du=1.0, Dv=25.0, Dc=10.0,
            sigma=1.0, mode="auto", eps=0.0, steps=12000, meas_every=50, seed=1, k_ref=0.6)
print("1D fixed-C branch S levels:")
t0=time.time()
for C0 in [0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4]:
    r = simulate(dict(base, C0=C0))
    k_n2 = (2*np.pi*r["n"][-1]/96)**2
    print("C0=%.2f -> n=%2d nz=%2d  S=%.4f k_n^2=%.4f ratio=%.2f amp=%.3f" %
          (C0, r["n"][-1], r["nz"][-1], r["Sm"][-1], k_n2, r["Sm"][-1]/k_n2, r["amp"][-1]))
print("%.1fs total" % (time.time()-t0))

# hysteresis: adiabatic slow triangle ramp of C via ramp mode, record n(C) up vs down
p = dict(base, mode="ramp", ramp=(0.7, 1.45, 4000.0, 20.0), C0=0.7, steps=120000, meas_every=100)
t0=time.time(); r = simulate(p); el=time.time()-t0
print("ramp 120k ticks in %.1fs" % el)
n = r["nz"].astype(int); Cm = r["Cm"]; t = r["t"]
half = 2000.0
up = (t % 4000) < half
print("up-sweep jumps:")
for i in range(1, len(n)):
    if n[i] != n[i-1]:
        print("  t=%7.0f C=%.3f  n %d->%d  (%s)" % (t[i], Cm[i], n[i-1], n[i], "up" if up[i] else "down"))
