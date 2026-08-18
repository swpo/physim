import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/binding")
import numpy as np
from sim import run, pair_sep

WP = dict(Dv=6.0, tau=4.0, k3=1.5, k4=1.0)   # working point candidate
d0 = float(sys.argv[1])
L = 96.0
bumps = [(48.0, 48.0 - d0/2), (48.0, 48.0 + d0/2)]
seps = []
def cb(t, u, v, w, blobs):
    if len(blobs) == 2:
        s, _ = pair_sep(blobs[0], blobs[1], L)
        seps.append((t, s))
    else:
        seps.append((t, -len(blobs)))
t0=time.time()
r = run(L=L, dx=1.0, T=3000.0, bumps=bumps, rec_tu=25.0, callback=cb, **WP)
out = dict(d0=d0, status=r["status"], seps=seps, runtime=round(time.time()-t0,1))
json.dump(out, open(f"/tmp/explore_d{d0}.json","w"))
print(json.dumps({k:out[k] for k in ("d0","status","runtime")}))
