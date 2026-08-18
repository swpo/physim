
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility")
from sim import run
from metrics import certify_point, lattice_cluster_verdict
seed = int(sys.argv[1])
OUT = "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility"
P = dict(k1=-0.7, Dv=0.65, tau=5.0)
# AMENDED protocol (2026-02-18, logged): noise-seeded direction runs use the
# direction-neutral symmetric IC (centered v,w bump, kick_d=0) because the
# plain u-only Gaussian does not settle at tau=5 (all 8 died; honest negative
# in cert3_angles.json). noise=1e-3, T=2000 to let direction lock in.
t0 = time.time()
r = run(p=P, T=2000.0, dx=0.5, stepper="imexfft", kick_angle=0.0, kick_d=0.0,
        noise=1e-3, seed=seed)
m = certify_point(r, 2000.0)
m["seed"] = seed; m["runtime_s"] = round(time.time()-t0,1)
json.dump(m, open(OUT + f"/cert6_seed{seed}.json", "w"))
np.savez_compressed(OUT + f"/cert6_track_seed{seed}.npz", t=r["t"], com=r["com"])
print(seed, m, flush=True)
