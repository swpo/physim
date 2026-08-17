
"""campB_slipscaling.py -- G3a: T_slip vs detuning beyond the 1:1 tongue edge.
kc=2e-3 (edge R_c ~ 1.727 from campC). Longer runs near the edge for stats.
"""
import sys, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
from sync_runner import eval_sync

pts = [(1.76, 400000), (1.80, 400000), (1.85, 300000), (1.92, 300000),
       (2.00, 250000), (2.10, 250000), (2.25, 250000)]
out = []
for R, steps in pts:
    r = eval_sync(dict(R=R, kc=2e-3, eps_g=2.4e-3), steps=steps, seed=1)
    out.append(r)
    print("R=%.2f (%dk): %s verdict=%s slips=%s T_slip=%s T_rate=%s rho=%s r2=%s (%.0fs)"
          % (R, steps//1000, r["status"], r.get("verdict"), r.get("n_slips"),
             r.get("T_slip"), r.get("T_slip_rate"), r.get("rho"),
             r.get("top_r2"), r.get("runtime_s", -1)), flush=True)
    with open("results_campB.json", "w") as f:
        json.dump(out, f, indent=1, default=str)
print("campB done", flush=True)
