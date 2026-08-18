
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility")
from sim import run, M0
from metrics import certify_point

OUT = "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility"
P = dict(k1=-0.7, Dv=0.65)   # M1 operating line (rest = M0)

jobs = []
for tau in (4.0, 4.2, 4.4):                 jobs.append((tau, 900.0))
for tau in (4.5, 4.6):                      jobs.append((tau, 1800.0))
for tau in (4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4): jobs.append((tau, 900.0))

res = {}
tracks = {}
t00 = time.time()
for tau, T in jobs:
    t0 = time.time()
    r = run(p=dict(P, tau=tau), T=T, dx=0.5, stepper="imexfft", kick_angle=30.0)
    m = certify_point(r, T)
    rt = time.time() - t0
    res[f"tau{tau}"] = dict(tau=tau, T=T, runtime_s=round(rt,1), **m)
    tracks[f"tau{tau}_t"] = r["t"]; tracks[f"tau{tau}_com"] = r["com"]
    print(f"tau={tau} T={T}: {m}  [{rt:.0f}s]", flush=True)
    json.dump(res, open(OUT + "/cert1_curve.json", "w"), indent=1)
np.savez_compressed(OUT + "/cert1_tracks.npz", **tracks)

# M0 control reruns on the certification integrator (document integrator change)
for dx in (1.0, 0.5):
    t0 = time.time()
    r = run(p={}, T=900.0, dx=dx, stepper="imexfft")   # pure M0 params, Dv=1
    m = certify_point(r, 900.0)
    res[f"M0_imexfft_dx{dx}"] = dict(T=900.0, runtime_s=round(time.time()-t0,1), **m)
    print(f"M0 control imexfft dx={dx}: {m}", flush=True)
json.dump(res, open(OUT + "/cert1_curve.json", "w"), indent=1)
print("TOTAL %.0fs" % (time.time()-t00))
