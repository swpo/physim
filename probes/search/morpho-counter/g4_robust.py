
"""g4_robust.py -- seeds + jitter for the two finalists."""
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from runner import eval_candidate

finalists = {
    "F48": dict(Dv=10.0, L=48, kappa=0.5, eps=2.4e-3, n_pair=(4, 5), noise=2e-3),
    "F64": dict(Dv=11.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6), noise=2e-3),
}
out = {"seeds": [], "jitter": []}

def gates(r):
    return bool(r.get("G1")) and bool(r.get("G2")) and bool(r.get("G5"))

for name, cand in finalists.items():
    for seed in [1, 2, 3, 4]:
        r = eval_candidate(dict(cand), seed=seed)
        r.pop("_rec", None)
        r["finalist"], r["seed"] = name, seed
        out["seeds"].append(r)
        print("%s seed=%d: PASS=%s G1=%s G2=%s r2=%.3f flips=%s per=%s rungs=%s sep=%.1f/%.1f ev=%s"
              % (name, seed, gates(r), r.get("G1"), r.get("G2"), r.get("top_r2", -1),
                 r.get("top_params", {}).get("n_flips"), r.get("tau3_period"),
                 r.get("rungs_visited"), r.get("sep12", -1), r.get("sep23", -1),
                 r.get("n_events")), flush=True)

rng = np.random.default_rng(99)
for name, cand in finalists.items():
    for jid in range(5):
        f = lambda: float(rng.uniform(0.9, 1.1))
        c = dict(cand)
        c["Dv"] = round(cand["Dv"] * f(), 3)
        c["kappa"] = round(cand["kappa"] * f(), 3)
        c["eps"] = cand["eps"] * f()
        c["noise"] = cand["noise"] * f()
        r = eval_candidate(c, seed=1)
        r.pop("_rec", None)
        r["finalist"], r["jitter_id"] = name, jid
        out["jitter"].append(r)
        print("%s jit=%d (Dv=%.2f kap=%.3f eps=%.2e): PASS=%s G1=%s G2=%s r2=%.3f flips=%s per=%s rungs=%s sep=%.1f/%.1f"
              % (name, jid, c["Dv"], c["kappa"], c["eps"], gates(r), r.get("G1"), r.get("G2"),
                 r.get("top_r2", -1), r.get("top_params", {}).get("n_flips"),
                 r.get("tau3_period"), r.get("rungs_visited"),
                 r.get("sep12", -1), r.get("sep23", -1)), flush=True)
        with open("results_g4.json", "w") as fjson:
            json.dump(out, fjson, indent=1)
with open("results_g4.json", "w") as fjson:
    json.dump(out, fjson, indent=1)
print("G4 done")
