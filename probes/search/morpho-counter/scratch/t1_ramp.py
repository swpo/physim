
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
import numpy as np
from morpho_sim import simulate
from hier_metrics import save_strip

# ramp mode: triangle-wave C setpoint, watch n(C) staircase
p = dict(ny=64, nx=96, dx=1.0, dt=0.05, a=0.1, b=0.9, Du=1.0, Dv=25.0, Dc=0.5,
         sigma=1.0, mode="ramp", ramp=(0.7, 1.4, 2000.0, 30.0), C0=1.0,
         steps=50000, meas_every=50, seed=1, k_ref=0.6,
         snap_at=[2000, 10000, 20000, 30000, 40000, 49999])
t0=time.time()
r = simulate(p)
print("50k steps @64x96 in %.1fs" % (time.time()-t0))
n = r["n"].astype(int); nz = r["nz"].astype(int)
print("FFT n unique:", np.unique(n))
print("zc  n unique:", np.unique(nz))
# print staircase: C vs n along the ramp
for i in range(0, len(n), len(n)//25):
    print("t=%7.0f Cm=%.3f n=%2d nz=%2d amp=%.3f pur=%.2f" % (r["t"][i], r["Cm"][i], n[i], nz[i], r["amp"][i], r["purity"][i]))
snaps = r["snaps"]
ks = sorted(snaps)
save_strip([snaps[k][0] for k in ks], "strips/ramp_u.png", titles=["u t=%d"%k for k in ks])
save_strip([snaps[k][1] for k in ks], "strips/ramp_C.png", titles=["C t=%d"%k for k in ks], cmap="viridis")
np.savez("logs/ramp_test.npz", **{k:v for k,v in r.items() if k!="snaps"})
print("saved strips")
