
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility")
from sim import run, make_ic, uniform_state
from metrics import certify_point, window_metrics

OUT = "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility"
P = dict(k1=-0.7, Dv=0.65, tau=5.0)
res = {}

# R1: no-flux boundary — launch blob at 30deg from center, watch wall encounter
t0 = time.time()
r = run(p=P, T=900.0, dx=0.5, stepper="euler", boundary="neumann", kick_angle=30.0,
        snap_times=(0.0, 200.0, 400.0, 600.0, 900.0))
m = certify_point(r, 900.0)
res["noflux_wall"] = dict(runtime_s=round(time.time()-t0,1), **m)
# also log the raw (wrapped=unwrapped here) track summary in 100tu windows
segs = []
for a in range(0, 900, 100):
    wm = window_metrics(r, a, a+100)
    if wm.get("ok"): segs.append(dict(t0=a, c=round(wm["c_med"],4), ang=round(wm["ang"],1)))
res["noflux_wall"]["segments"] = segs
print("noflux:", m, flush=True)
print("segments:", segs, flush=True)
np.savez_compressed(OUT + "/cert4_noflux_track.npz", t=r["t"], com=r["com"],
                    **{f"snap{k}": v for k, v in r["snaps"].items()})
json.dump(res, open(OUT + "/cert4_reflex.json", "w"), indent=1)

# R2: collision traveler -> stationary blob (both seeded, then autonomous).
# Build IC: traveling blob at (24,24) kicked toward 45deg aiming at a stationary
# blob at (60,60) (distance ~51). Same params for both (tau=5 => the "stationary"
# one will also start moving if perturbed — log whatever happens; M2 terrain).
p = dict(P)
N = 192; dx = 0.5
u1, v1, w1, u0 = make_ic(N, dx, dict(lam=2.0,k1=-0.7,k3=1.0,k4=1.5,tau=5.0,theta=0.7,Du=1.0,Dv=0.65,Dw=20.0),
                          center=(24.0,24.0), kick_angle=45.0)
u2, v2, w2, _  = make_ic(N, dx, dict(lam=2.0,k1=-0.7,k3=1.0,k4=1.5,tau=5.0,theta=0.7,Du=1.0,Dv=0.65,Dw=20.0),
                          center=(60.0,60.0))
u = u1 + (u2 - u0); v = v1 + (v2 - u0); w = w1 + (w2 - u0)
t0 = time.time()
r = run(p=P, T=900.0, dx=0.5, stepper="imexfft", ic=(u, v, w),
        snap_times=(0.0, 100.0, 200.0, 300.0, 400.0, 500.0, 700.0, 900.0))
# per-window ncomp + total area tells the story (COM of multi-blob = not meaningful)
story = []
for a in range(0, 900, 100):
    n0 = np.searchsorted(r["t"], a); n1 = np.searchsorted(r["t"], a+100)
    if n1 > n0 and len(r["ncomp"]) > n0:
        story.append(dict(t0=a, nc_min=int(r["ncomp"][n0:n1].min()), nc_max=int(r["ncomp"][n0:n1].max()),
                          area_med=float(np.median(r["area"][n0:n1]))))
res["collision"] = dict(status=r["status"], runtime_s=round(time.time()-t0,1), story=story,
                        nc_end=int(r["ncomp"][-1]) if len(r["ncomp"]) else -1,
                        area_end=float(r["area"][-1]) if len(r["area"]) else 0)
print("collision:", res["collision"], flush=True)
np.savez_compressed(OUT + "/cert4_collision_snaps.npz",
                    **{f"snap{k}": v for k, v in r["snaps"].items()})
json.dump(res, open(OUT + "/cert4_reflex.json", "w"), indent=1)
