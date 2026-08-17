
"""g3_final.py -- G3 response curves with metric-locked runner (v3):
(1) counter period vs eps (micro price: control-field gain), 5 values
(2) duty cycle vs kappa (micro price: setpoint position), 5 values
Both at 120k ticks for >= 6-cycle statistics. Also (3) staircase-position
response: mean C on rung-5 plateau vs sigma is implicit in hysteresis loops.
"""
import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from runner import eval_candidate

base = dict(Dv=11.0, L=64, kappa=0.5, eps=2.8e-3, n_pair=(5, 6), noise=2e-3)
out = {"metric_version": "v3-locked", "eps_curve": [], "kappa_curve": []}

for eps in [1.4e-3, 2.0e-3, 2.8e-3, 4.0e-3, 5.6e-3]:
    r = eval_candidate(dict(base, eps=eps), steps=120000, seed=1)
    r.pop("_rec", None)
    row = dict(eps=eps, period=r.get("tau3_period"), n_cycles=r.get("n_cycles"),
               n_flips=r.get("n_flips"), dwell_lo=r.get("dwell_lo"),
               dwell_hi=r.get("dwell_hi"), rungs=r.get("rungs_visited"),
               frac2=r.get("frac_2level"),
               eps_x_period=(eps * r["tau3_period"] if r.get("tau3_period") else None))
    out["eps_curve"].append(row)
    print(row, flush=True)
    with open("results_g3final.json", "w") as f:
        json.dump(out, f, indent=1)

for kap in [0.3, 0.4, 0.5, 0.6, 0.7]:
    r = eval_candidate(dict(base, kappa=kap), steps=120000, seed=1)
    r.pop("_rec", None)
    dl, dh = r.get("dwell_lo"), r.get("dwell_hi")
    duty = dh / (dh + dl) if (dh and dl) else None
    row = dict(kappa=kap, period=r.get("tau3_period"),
               duty=round(duty, 4) if duty else None, dwell_lo=dl, dwell_hi=dh,
               n_flips=r.get("n_flips"), rungs=r.get("rungs_visited"))
    out["kappa_curve"].append(row)
    print(row, flush=True)
    with open("results_g3final.json", "w") as f:
        json.dump(out, f, indent=1)
print("g3 final done", flush=True)
