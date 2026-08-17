
"""cert_grid.py -- pick the flagship: small grid x 4 seeds, v2 gates."""
import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from runner import eval_candidate

grid = []
for eps in [2.4e-3, 2.8e-3, 3.2e-3]:
    for kap in [0.42, 0.5]:
        grid.append(dict(Dv=11.0, L=64, kappa=kap, eps=eps, n_pair=(5, 6), noise=2e-3))
grid.append(dict(Dv=11.0, L=64, kappa=0.5, eps=2.8e-3, n_pair=(5, 6), noise=8e-3))
grid.append(dict(Dv=10.5, L=64, kappa=0.5, eps=2.8e-3, n_pair=(5, 6), noise=2e-3))

out = []
def gates(r):
    return bool(r.get("G1")) and bool(r.get("G2")) and bool(r.get("G5"))

for gi, cand in enumerate(grid):
    ok = 0
    rows = []
    for seed in [1, 2, 3, 4]:
        r = eval_candidate(dict(cand), seed=seed)
        r.pop("_rec", None)
        r["grid_id"], r["seed"] = gi, seed
        out.append(r)
        ok += gates(r)
        rows.append("s%d:%s(r2=%.2f fl=%s sep=%.0f/%.0f per=%s)" % (
            seed, "P" if gates(r) else "f", r.get("top_r2", -1),
            r.get("n_flips"), r.get("sep12", -1), r.get("sep23", -1),
            r.get("tau3_period")))
    print("grid%02d eps=%.1e kap=%.2f ns=%.0e Dv=%.1f -> %d/4 | %s"
          % (gi, cand["eps"], cand["kappa"], cand["noise"], cand["Dv"], ok, " ".join(rows)), flush=True)
    with open("results_grid.json", "w") as f:
        json.dump(out, f, indent=1)
print("grid done", flush=True)
