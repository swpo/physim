
"""campB3_scaling_seeds.py -- G3a headline: T_slip_rate vs (R-Rc), 3 seeds each.
kc=2e-3, Rc=1.7271 (measured). Median over seeds kills slip-clustering noise.
"""
import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
from sync_runner import eval_sync

pts = [(1.76, 500000), (1.80, 400000), (1.85, 400000), (1.92, 300000),
       (2.00, 300000), (2.15, 300000), (2.30, 250000)]
out = []
for R, steps in pts:
    rates, meds, slips = [], [], []
    for seed in [1, 2, 3]:
        r = eval_sync(dict(R=R, kc=2e-3, eps_g=2.4e-3), steps=steps, seed=seed)
        out.append(r)
        if r.get("T_slip_rate"): rates.append(r["T_slip_rate"])
        if r.get("T_slip"): meds.append(r["T_slip"])
        slips.append(r.get("n_slips", 0))
        with open("results_campB3.json", "w") as f:
            json.dump(out, f, indent=1, default=str)
    print("R=%.2f: T_rate seeds=%s -> med=%.0f | T_med med=%s | slips=%s"
          % (R, [round(x) for x in rates], np.median(rates),
             round(np.median(meds)) if meds else None, slips), flush=True)
print("campB3 done", flush=True)
