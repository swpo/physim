
"""campD_32tongue.py -- is there a 3:2 plateau? fine rho(R) scan past the 1:1 edge."""
import sys, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
from sync_runner import eval_sync

out = []
for R in [1.85, 1.90, 1.95, 2.00, 2.05, 2.10, 2.20]:
    r = eval_sync(dict(R=R, kc=2e-3, eps_g=2.4e-3), steps=300000, seed=1)
    out.append(r)
    print("R=%.2f: rho=%s slips=%s v=%s cyc=%s/%s" % (R, r.get("rho"), r.get("n_slips"),
          r.get("verdict"), r.get("cyc1"), r.get("cyc2")), flush=True)
    with open("results_campD.json", "w") as f:
        json.dump(out, f, indent=1, default=str)
print("campD done", flush=True)
