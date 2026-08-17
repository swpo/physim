
"""campA_staircase.py -- rotation number rho vs detuning R at kc=2e-3.
eps_g=2.4e-3 keeps eps1 <= 3.5e-3 up to R=2.1 (no rung-skip zone).
"""
import sys, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
from sync_runner import eval_sync
import numpy as np

Rs = [1.0, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1]
out = []
for R in Rs:
    r = eval_sync(dict(R=R, kc=2e-3, eps_g=2.4e-3), steps=250000, seed=1)
    out.append(r)
    print("R=%.2f: %s rho=%s slips=%s T_slip=%s exc=%s verdict=%s (%.0fs)"
          % (R, r["status"], r.get("rho"), r.get("n_slips"), r.get("T_slip"),
             r.get("max_exc"), r.get("verdict"), r.get("runtime_s", -1)), flush=True)
    with open("results_campA.json", "w") as f:
        json.dump(out, f, indent=1, default=str)
print("campA done", flush=True)
