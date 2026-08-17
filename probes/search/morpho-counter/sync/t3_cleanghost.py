
"""t3_cleanghost.py -- hunt a slip window that is BOTH slow (sep34>=5) and
regular (r2>=0.85): stronger coupling => deterministic drift dominates noise.
Edges: kc=4e-3 -> Rc~2.285; kc=8e-3 -> Rc~2.519.
"""
import sys
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
from sync_runner import eval_sync

for R, kc, steps in [(2.32, 4e-3, 500000), (2.36, 4e-3, 400000), (2.42, 4e-3, 400000),
                     (2.56, 8e-3, 500000), (2.62, 8e-3, 400000), (2.72, 8e-3, 400000)]:
    r = eval_sync(dict(R=R, kc=kc, eps_g=2.4e-3), steps=steps, seed=1)
    print("R=%.2f kc=%.0e (%dk): v=%s slips=%s T_med=%s T_rate=%s sep34=%s top=%s r2=%s flips=%s rho=%s (%.0fs)"
          % (R, kc, steps//1000, r.get("verdict"), r.get("n_slips"), r.get("T_slip"),
             r.get("T_slip_rate"), r.get("sep34"), r.get("top_model"), r.get("top_r2"),
             (r.get("top_params") or {}).get("n_flips"), r.get("rho"),
             r.get("runtime_s", -1)), flush=True)
