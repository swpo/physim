
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility")
from sim import run
from metrics import certify_point, window_metrics

OUT = "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility"
P = dict(k1=-0.7, Dv=0.65, tau=5.0)

# B1 at the M1 traveling point: lifetime 1e4 tu with noise, dx=0.5 imexfft.
t0 = time.time()
r = run(p=P, T=10000.0, dx=0.5, stepper="imexfft", kick_angle=30.0,
        noise=2e-3, seed=3, rec_tu=5.0)
m = certify_point(r, 10000.0)
segs = []
for a in range(0, 10000, 1000):
    wm = window_metrics(r, a, a+1000)
    if wm.get("ok"):
        segs.append(dict(t0=a, c=round(wm["c_med"],4), ang=round(wm["ang"],1),
                         nc=wm["nc_max"], A=round(wm["area_med"],1)))
res = dict(runtime_s=round(time.time()-t0,1), final=m, segments=segs,
           status=r["status"], t_end=float(r["t"][-1]) if len(r["t"]) else 0)
print(json.dumps(res, indent=1), flush=True)
json.dump(res, open(OUT + "/cert5_lifetime.json", "w"), indent=1)
np.savez_compressed(OUT + "/cert5_track.npz", t=r["t"], com=r["com"], area=r["area"])
