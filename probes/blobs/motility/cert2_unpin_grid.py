
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility")
from sim import run
from metrics import certify_point, unpin_speed_verdict

OUT = "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility"
P = dict(k1=-0.7, Dv=0.65, tau=5.0)
res = {}

# grid-refinement chain at fixed physical params, fixed dt=0.02, T=900, kick30
for dx in (1.0, 0.5, 0.25):
    t0 = time.time()
    r = run(p=P, T=900.0, dx=dx, stepper="imexfft", kick_angle=30.0)
    m = certify_point(r, 900.0)
    res[f"dx{dx}"] = dict(dx=dx, runtime_s=round(time.time()-t0,1), **m)
    print(f"dx={dx}: {m}  [{res[f'dx{dx}']['runtime_s']}s]", flush=True)
    json.dump(res, open(OUT + "/cert2_grid.json", "w"), indent=1)

if res["dx0.5"].get("c_med") and res["dx0.25"].get("c_med"):
    v = unpin_speed_verdict(res["dx0.5"]["c_med"], res["dx0.25"]["c_med"])
    res["verdict_dx05_vs_dx025"] = v
    print("grid-convergence verdict (0.5 vs 0.25):", v, flush=True)
if res["dx1.0"].get("c_med") and res["dx0.5"].get("c_med"):
    v2 = unpin_speed_verdict(res["dx1.0"]["c_med"], res["dx0.5"]["c_med"])
    res["info_dx1_vs_dx05"] = v2
    print("info (1.0 vs 0.5):", v2, flush=True)
json.dump(res, open(OUT + "/cert2_grid.json", "w"), indent=1)
