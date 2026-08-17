
"""g4_robust2.py -- G4 certification with runner v2 on final candidates."""
import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from runner import eval_candidate

finalists = {
    "F48e24": dict(Dv=10.0, L=48, kappa=0.5, eps=2.4e-3, n_pair=(4, 5), noise=2e-3),
    "F48e34": dict(Dv=10.0, L=48, kappa=0.5, eps=3.4e-3, n_pair=(4, 5), noise=2e-3),
    "F64e34": dict(Dv=11.0, L=64, kappa=0.5, eps=3.4e-3, n_pair=(5, 6), noise=2e-3),
}
out = {"seeds": [], "jitter": []}
def gates(r):
    return bool(r.get("G1")) and bool(r.get("G2")) and bool(r.get("G5"))

for name, cand in finalists.items():
    npass = 0
    for seed in [1, 2, 3, 4]:
        r = eval_candidate(dict(cand), seed=seed)
        r.pop("_rec", None)
        r["finalist"], r["seed"] = name, seed
        out["seeds"].append(r)
        npass += gates(r)
        print("%s seed=%d: PASS=%s G1=%s G2=%s r2=%.3f flips=%s per=%s tau=%s/%s sep=%.1f/%.1f rungs=%s"
              % (name, seed, gates(r), r.get("G1"), r.get("G2"), r.get("top_r2", -1),
                 r.get("top_params", {}).get("n_flips"), r.get("tau3_period"),
                 r.get("tau1"), r.get("tau2"), r.get("sep12", -1), r.get("sep23", -1),
                 r.get("rungs_visited")), flush=True)
    print("== %s seeds: %d/4" % (name, npass), flush=True)
    with open("results_g4v2.json", "w") as f:
        json.dump(out, f, indent=1)

rng = np.random.default_rng(1234)
for name, cand in finalists.items():
    npass = 0
    for jid in range(5):
        f_ = lambda: float(rng.uniform(0.9, 1.1))
        c = dict(cand)
        c["Dv"] = round(cand["Dv"] * f_(), 3)
        c["kappa"] = round(cand["kappa"] * f_(), 3)
        c["eps"] = cand["eps"] * f_()
        c["noise"] = cand["noise"] * f_()
        r = eval_candidate(c, seed=1)
        r.pop("_rec", None)
        r["finalist"], r["jitter_id"] = name, jid
        out["jitter"].append(r)
        npass += gates(r)
        print("%s jit=%d (Dv=%.2f kap=%.3f eps=%.2e ns=%.1e): PASS=%s G1=%s G2=%s r2=%.3f flips=%s per=%s sep=%.1f/%.1f"
              % (name, jid, c["Dv"], c["kappa"], c["eps"], c["noise"], gates(r),
                 r.get("G1"), r.get("G2"), r.get("top_r2", -1),
                 r.get("top_params", {}).get("n_flips"), r.get("tau3_period"),
                 r.get("sep12", -1), r.get("sep23", -1)), flush=True)
        with open("results_g4v2.json", "w") as fj:
            json.dump(out, fj, indent=1)
    print("== %s jitter: %d/5" % (name, npass), flush=True)
print("G4 v2 done", flush=True)
