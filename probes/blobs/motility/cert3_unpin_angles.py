
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility")
from sim import run
from metrics import certify_point, angle_follow_verdict, lattice_cluster_verdict

OUT = "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility"
P = dict(k1=-0.7, Dv=0.65, tau=5.0)
res = {"kick_runs": {}, "noise_runs": {}}

# A) 9 non-lattice kick angles: does final direction follow the kick?
kicks = [12.0, 30.0, 57.0, 78.0, 105.0, 141.0, 203.0, 289.0, 330.0]
finals = []
tracks = {}
for a in kicks:
    t0 = time.time()
    r = run(p=P, T=600.0, dx=0.5, stepper="imexfft", kick_angle=a)
    m = certify_point(r, 600.0)
    res["kick_runs"][str(a)] = dict(kick=a, runtime_s=round(time.time()-t0,1), **m)
    finals.append(m.get("ang"))
    tracks[f"kick{a}_t"] = r["t"]; tracks[f"kick{a}_com"] = r["com"]
    print(f"kick={a}: {m}", flush=True)
    json.dump(res, open(OUT + "/cert3_angles.json", "w"), indent=1)
ok = [i for i,(f) in enumerate(finals) if f is not None and res["kick_runs"][str(kicks[i])]["cls"]=="traveling"]
v = angle_follow_verdict([kicks[i] for i in ok], [finals[i] for i in ok])
res["angle_follow_verdict"] = v
print("ANGLE-FOLLOW:", v, flush=True)

# B) 8 noise-seeded runs, NO kick: spontaneous direction choice
finals2 = []
for seed in range(8):
    t0 = time.time()
    r = run(p=P, T=600.0, dx=0.5, stepper="imexfft", noise=2e-3, seed=seed)
    m = certify_point(r, 600.0)
    res["noise_runs"][str(seed)] = dict(seed=seed, runtime_s=round(time.time()-t0,1), **m)
    if m.get("cls") == "traveling":
        finals2.append(m["ang"])
    tracks[f"noise{seed}_t"] = r["t"]; tracks[f"noise{seed}_com"] = r["com"]
    print(f"seed={seed}: {m}", flush=True)
    json.dump(res, open(OUT + "/cert3_angles.json", "w"), indent=1)
v2 = lattice_cluster_verdict(finals2)
res["lattice_cluster_verdict"] = v2
print("LATTICE-CLUSTER:", v2, flush=True)
json.dump(res, open(OUT + "/cert3_angles.json", "w"), indent=1)
np.savez_compressed(OUT + "/cert3_tracks.npz", **tracks)
