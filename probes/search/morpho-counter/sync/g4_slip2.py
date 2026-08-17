
"""g4_slip2.py -- G4 battery at the G2-capable slip point: R=1.85, noise=5e-4.
4 seeds (400k) + 4 jitter draws (+-10% R, kc, eps_g, noise)."""
import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
from sync_runner import eval_sync

SL = dict(R=1.85, kc=2e-3, eps_g=2.4e-3, noise_amp=5e-4)
def ok_slip(r):
    return (r.get("verdict") == "slip" and r.get("n_slips", 0) >= 5
            and (r.get("top_r2") or 0) >= 0.85 and r.get("G5"))
out = {"seeds": [], "jit": []}
for seed in [1, 2, 3, 4]:
    r = eval_sync(dict(SL), steps=400000, seed=seed)
    out["seeds"].append(r)
    print("seed=%d: v=%s slips=%s T_med=%s T3=%s sep34=%s r2=%s flips=%s PASS=%s (%.0fs)"
          % (seed, r.get("verdict"), r.get("n_slips"), r.get("T_slip"), r.get("T3"),
             r.get("sep34"), r.get("top_r2"), (r.get("top_params") or {}).get("n_flips"),
             ok_slip(r), r.get("runtime_s", -1)), flush=True)
    with open("results_g4slip2.json", "w") as f:
        json.dump(out, f, indent=1, default=str)
rng = np.random.default_rng(31337)
for jid in range(4):
    f_ = lambda: float(rng.uniform(0.9, 1.1))
    c = dict(R=round(SL["R"] * f_(), 3), kc=SL["kc"] * f_(),
             eps_g=SL["eps_g"] * f_(), noise_amp=SL["noise_amp"] * f_())
    r = eval_sync(c, steps=400000, seed=jid + 30)
    out["jit"].append(r)
    print("jit=%d (R=%.2f kc=%.1e ns=%.1e): v=%s slips=%s r2=%s sep34=%s PASS=%s"
          % (jid, c["R"], c["kc"], c["noise_amp"], r.get("verdict"), r.get("n_slips"),
             r.get("top_r2"), r.get("sep34"), ok_slip(r)), flush=True)
    with open("results_g4slip2.json", "w") as f:
        json.dump(out, f, indent=1, default=str)
print("g4_slip2 done", flush=True)
