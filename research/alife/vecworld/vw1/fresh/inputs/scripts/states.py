"""Fresh test states for the input analyses: one designer ensemble of the VW-1 <Phi_coarse,
Phi_objects> world (aworld.build()['both'], MapWorld, world_seed 0), N members (seed (7001,)), init +
50-tick burn-in, then T0 free ticks. Saves the level-0 states (float64, exact restart) and the
tracker memories -> results/states.npz.

usage: python -B states.py N T0"""
import json
import sys
import time

import common as CM
import numpy as np

N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
T0 = int(sys.argv[2]) if len(sys.argv) > 2 else 60
t0 = time.time()
w, parts, AW = CM.build_world("both")
d = w.designer
ens = d.ensemble(N, seed=(7001,))
print("init + burn-in", N, round(time.time() - t0, 1), "s", flush=True)
done = 0
while done < T0:
    ens, _ = d.rollout(ens, None, T=20, rec=())
    done += 20
    print("tick", done, round(time.time() - t0, 1), "s", flush=True)
x = np.asarray(ens.x)
m = CM.tracker_mem(ens)
L1 = ens.level(1)
np.savez(f"{CM.RES}/states.npz", x=x, m=m, L1=L1, t=ens.t)
lab, tab = CM.mem_parts(m)
info = {"N": N, "seed": [7001], "world_seed": 0, "ticks_after_burn_in": T0, "burn_in_ticks": AW.BURN_TICKS,
        "seconds": time.time() - t0, "objects_present_median": float(np.median(tab[:, :, 0].sum(1))),
        "mass_total_mean": float(x.sum((1, 2, 3)).mean())}
json.dump(info, open(f"{CM.RES}/states.json", "w"), indent=1)
print(json.dumps(info), flush=True)
