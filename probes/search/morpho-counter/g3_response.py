
"""g3_response.py -- response curves: does the emergent period/duty move
smoothly+monotonically with micro prices (eps = C drive gain; kappa = setpoint)?
Longer runs (120k ticks) for accurate period stats; not the G5 cert runs.
"""
import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from runner import eval_candidate

base = dict(Dv=11.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6), noise=2e-3)
out = {"eps_curve": [], "kappa_curve": []}

print("--- eps curve (expect period ~ 1/eps, monotone decreasing) ---")
for eps in [1.2e-3, 1.7e-3, 2.4e-3, 3.4e-3, 4.8e-3]:
    r = eval_candidate(dict(base, eps=eps), steps=120000, seed=1)
    r.pop("_rec", None)
    row = dict(eps=eps, period=r.get("tau3_period"), n_cycles=r.get("n_cycles"),
               dwell_lo=r.get("dwell_lo"), dwell_hi=r.get("dwell_hi"),
               n_flips=r.get("n_flips"), rungs=r.get("rungs_visited"),
               eps_x_period=(eps * r["tau3_period"] if r.get("tau3_period") else None))
    out["eps_curve"].append(row)
    print(row, flush=True)

print("--- kappa curve (expect duty cycle = dwell_hi/(hi+lo) increasing) ---")
for kap in [0.25, 0.375, 0.5, 0.625, 0.75]:
    r = eval_candidate(dict(base, kappa=kap), steps=120000, seed=1)
    r.pop("_rec", None)
    dl, dh = r.get("dwell_lo"), r.get("dwell_hi")
    duty = dh / (dh + dl) if (dh and dl) else None
    row = dict(kappa=kap, period=r.get("tau3_period"), duty=duty,
               dwell_lo=dl, dwell_hi=dh, n_flips=r.get("n_flips"),
               rungs=r.get("rungs_visited"))
    out["kappa_curve"].append(row)
    print(row, flush=True)

with open("results_g3.json", "w") as f:
    json.dump(out, f, indent=1)
print("G3 done")
