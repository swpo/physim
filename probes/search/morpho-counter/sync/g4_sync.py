
"""g4_sync.py -- G4 for coupled counters. In-tongue: R=1.3, kc=2e-3.
Slip: R=2.0, kc=2e-3. 4 seeds each; jitter +-10% on R, kc, eps_g, noise (4 draws each).
"""
import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
from sync_runner import eval_sync

out = {"tongue_seeds": [], "slip_seeds": [], "tongue_jit": [], "slip_jit": []}
IN = dict(R=1.3, kc=2e-3, eps_g=2.4e-3)
SL = dict(R=2.0, kc=2e-3, eps_g=2.4e-3)

def ok_tongue(r):
    return r.get("verdict") == "locked" and r.get("G1") and r.get("G5")
def ok_slip(r):
    return (r.get("verdict") == "slip" and r.get("n_slips", 0) >= 3
            and r.get("sep34", 0) and r.get("sep34") >= 2 and r.get("G5"))

for seed in [1, 2, 3, 4]:
    r = eval_sync(dict(IN), steps=200000, seed=seed)
    out["tongue_seeds"].append(r)
    print("TONGUE seed=%d: v=%s slips=%s exc=%s rho=%s sep=%s/%s PASS=%s (%.0fs)"
          % (seed, r.get("verdict"), r.get("n_slips"), r.get("max_exc"), r.get("rho"),
             r.get("sep12"), r.get("sep23"), ok_tongue(r), r.get("runtime_s", -1)), flush=True)
for seed in [1, 2, 3, 4]:
    r = eval_sync(dict(SL), steps=300000, seed=seed)
    out["slip_seeds"].append(r)
    print("SLIP seed=%d: v=%s slips=%s T_slip=%s rho=%s sep34=%s r2=%s PASS=%s (%.0fs)"
          % (seed, r.get("verdict"), r.get("n_slips"), r.get("T_slip"), r.get("rho"),
             r.get("sep34"), r.get("top_r2"), ok_slip(r), r.get("runtime_s", -1)), flush=True)
    with open("results_g4sync.json", "w") as f:
        json.dump(out, f, indent=1, default=str)

rng = np.random.default_rng(4242)
for jid in range(4):
    f_ = lambda: float(rng.uniform(0.9, 1.1))
    c = dict(R=round(IN["R"] * f_(), 3), kc=IN["kc"] * f_(),
             eps_g=IN["eps_g"] * f_(), noise_amp=2e-3 * f_())
    r = eval_sync(c, steps=200000, seed=jid + 10)
    out["tongue_jit"].append(r)
    print("TONGUE jit=%d (R=%.2f kc=%.1e): v=%s slips=%s PASS=%s"
          % (jid, c["R"], c["kc"], r.get("verdict"), r.get("n_slips"), ok_tongue(r)), flush=True)
for jid in range(4):
    f_ = lambda: float(rng.uniform(0.9, 1.1))
    c = dict(R=round(SL["R"] * f_(), 3), kc=SL["kc"] * f_(),
             eps_g=SL["eps_g"] * f_(), noise_amp=2e-3 * f_())
    r = eval_sync(c, steps=300000, seed=jid + 20)
    out["slip_jit"].append(r)
    print("SLIP jit=%d (R=%.2f kc=%.1e): v=%s slips=%s T_slip=%s sep34=%s PASS=%s"
          % (jid, c["R"], c["kc"], r.get("verdict"), r.get("n_slips"),
             r.get("T_slip"), r.get("sep34"), ok_slip(r)), flush=True)
    with open("results_g4sync.json", "w") as f:
        json.dump(out, f, indent=1, default=str)
print("g4 sync done", flush=True)
