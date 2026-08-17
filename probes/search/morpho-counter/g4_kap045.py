
"""g4_kap045.py -- jitter robustness of re-centered flagship kap=0.45, eps=3.0e-3.
4 seeds at 60k (G5-real cert) + 12 jitter draws at 120k (statistics)."""
import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from runner import eval_candidate

cand0 = dict(Dv=11.0, L=64, kappa=0.45, eps=3.0e-3, n_pair=(5, 6), noise=2e-3)
def gates(r):
    return bool(r.get("G1")) and bool(r.get("G2")) and bool(r.get("G5"))

out = {"seeds": [], "jitter": []}
npass = 0
for seed in [1, 2, 3, 4]:
    r = eval_candidate(dict(cand0), seed=seed)
    r.pop("_rec", None); r["seed"] = seed
    out["seeds"].append(r)
    npass += gates(r)
    print("seed=%d: PASS=%s G1=%s G2=%s r2=%.3f fl=%s per=%s tau=%s/%s sep=%.1f/%.1f rungs=%s"
          % (seed, gates(r), r.get("G1"), r.get("G2"), r.get("top_r2", -1),
             r.get("top_params", {}).get("n_flips"), r.get("tau3_period"),
             r.get("tau1"), round(r["tau2"],1) if r.get("tau2") else None,
             r.get("sep12", -1), r.get("sep23", -1), r.get("rungs_visited")), flush=True)
print("== seeds: %d/4" % npass, flush=True)

rng = np.random.default_rng(777)
npass = 0
for jid in range(12):
    f_ = lambda: float(rng.uniform(0.9, 1.1))
    c = dict(cand0)
    c["Dv"] = round(cand0["Dv"] * f_(), 3)
    c["kappa"] = round(cand0["kappa"] * f_(), 3)
    c["eps"] = cand0["eps"] * f_()
    c["noise"] = cand0["noise"] * f_()
    r = eval_candidate(c, steps=120000, seed=jid + 20)
    r.pop("_rec", None); r["jitter_id"] = jid
    ok = bool(r.get("G1")) and bool(r.get("G2"))
    r["pass_g1g2"] = ok
    out["jitter"].append(r)
    npass += ok
    print("jit=%02d (Dv=%.2f kap=%.3f eps=%.2e): PASS=%s G1=%s G2=%s r2=%.3f fl=%s per=%s sep=%.1f/%.1f rungs=%s"
          % (jid, c["Dv"], c["kappa"], c["eps"], ok, r.get("G1"), r.get("G2"),
             r.get("top_r2", -1), r.get("top_params", {}).get("n_flips"),
             r.get("tau3_period"), r.get("sep12", -1), r.get("sep23", -1),
             r.get("rungs_visited")), flush=True)
    with open("results_kap045.json", "w") as f:
        json.dump(out, f, indent=1)
print("== jitter: %d/12" % npass, flush=True)
