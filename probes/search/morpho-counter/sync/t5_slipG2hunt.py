
"""t5_slipG2hunt.py -- find a slip point passing BOTH r2>=0.85 (>=5 slips)
and maximal sep34. Grid: (R, noise). kc=2e-3, eps_g=2.4e-3."""
import sys
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
from sync_runner import eval_sync

for R, noise, steps in [(1.88, 1e-3, 400000), (1.95, 5e-4, 400000),
                        (2.10, 1e-3, 300000), (1.82, 2e-4, 500000),
                        (1.88, 2e-4, 400000)]:
    r = eval_sync(dict(R=R, kc=2e-3, eps_g=2.4e-3, noise_amp=noise), steps=steps, seed=1)
    print("R=%.2f ns=%.0e (%dk): v=%s slips=%s T_med=%s T3=%s sep34=%s top=%s r2=%s flips=%s alive=%s/%s (%.0fs)"
          % (R, noise, steps//1000, r.get("verdict"), r.get("n_slips"), r.get("T_slip"),
             r.get("T3"), r.get("sep34"), r.get("top_model"), r.get("top_r2"),
             (r.get("top_params") or {}).get("n_flips"),
             r.get("alive1", {}).get("alive"), r.get("alive2", {}).get("alive"),
             r.get("runtime_s", -1)), flush=True)
