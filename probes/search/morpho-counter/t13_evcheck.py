
import sys, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
import runner
from runner import eval_candidate

# re-evaluate the 3 formerly-failing F48 jitter cases + base with new event anchor
cases = [
    ("F48 base   ", dict(Dv=10.0,  L=48, kappa=0.5,   eps=2.4e-3,  n_pair=(4,5), noise=2e-3)),
    ("F48 jit2   ", dict(Dv=9.94,  L=48, kappa=0.511, eps=2.61e-3, n_pair=(4,5), noise=2e-3)),
    ("F48 jit3   ", dict(Dv=9.62,  L=48, kappa=0.489, eps=2.29e-3, n_pair=(4,5), noise=2e-3)),
    ("F48 jit4   ", dict(Dv=10.87, L=48, kappa=0.488, eps=2.53e-3, n_pair=(4,5), noise=2e-3)),
    ("F64 base   ", dict(Dv=11.0,  L=64, kappa=0.5,   eps=2.4e-3,  n_pair=(5,6), noise=2e-3)),
]
for name, c in cases:
    r = eval_candidate(c, seed=1)
    r.pop("_rec", None)
    print("%s: G1=%s G2=%s r2=%.3f flips=%s per=%s n_ev=%s tau2=%s sep=%.1f/%.1f healthy=%.2f"
          % (name, r.get("G1"), r.get("G2"), r.get("top_r2",-1),
             r.get("top_params",{}).get("n_flips"), r.get("tau3_period"),
             r.get("n_events"), r.get("tau2"), r.get("sep12",-1), r.get("sep23",-1),
             r.get("healthy_env",-1)), flush=True)
