
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility")
from sim import run, make_ic
from metrics import window_metrics

OUT = "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility"
PM = dict(lam=2.0, k1=-0.7, k3=1.0, k4=1.5, tau=5.0, theta=0.7, Du=1.0, Dv=0.65, Dw=20.0)
P = dict(k1=-0.7, Dv=0.65, tau=5.0)
N = 192; dx = 0.5
# traveler at (24,24) kicked toward +45deg; target at (60,60) with CENTERED
# v,w bump (kick_d=0) so it settles (fix for first attempt where target died).
u1, v1, w1, u0 = make_ic(N, dx, PM, center=(24.0,24.0), kick_angle=45.0)
u2, v2, w2, _  = make_ic(N, dx, PM, center=(60.0,60.0), kick_angle=0.0, kick_d=0.0)
u = u1 + (u2 - u0); v = v1 + (v2 - u0); w = w1 + (w2 - u0)
t0 = time.time()
r = run(p=P, T=1200.0, dx=0.5, stepper="imexfft", ic=(u, v, w),
        snap_times=(0.0, 100.0, 200.0, 300.0, 400.0, 450.0, 500.0, 550.0, 600.0, 700.0, 800.0, 1000.0, 1200.0))
story = []
for a in range(0, 1200, 100):
    n0 = np.searchsorted(r["t"], a); n1 = np.searchsorted(r["t"], a+100)
    if n1 > n0 and len(r["ncomp"]) > n0:
        story.append(dict(t0=a, nc_min=int(r["ncomp"][n0:n1].min()), nc_max=int(r["ncomp"][n0:n1].max()),
                          area_med=float(np.median(r["area"][n0:n1]))))
res = dict(status=r["status"], runtime_s=round(time.time()-t0,1), story=story,
           nc_end=int(r["ncomp"][-1]) if len(r["ncomp"]) else -1,
           area_end=float(r["area"][-1]) if len(r["area"]) else 0)
print(json.dumps(res, indent=1), flush=True)
json.dump(res, open(OUT + "/cert4b_collision.json", "w"), indent=1)
np.savez_compressed(OUT + "/cert4b_collision_snaps.npz",
                    **{f"snap{k}": v for k, v in r["snaps"].items()})
