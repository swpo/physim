
"""campC_tonguewidth.py -- 1:1 tongue edges vs coupling kc (G3b).
Bisection on R (upper edge only + measure lower edge) using locked/slip verdict.
Edge criterion: locked if n_slips==0 & exc<1 over >=8 cycles (locked metric).
"""
import sys, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
from sync_runner import eval_sync

def is_locked(R, kc, steps=200000, seed=1):
    r = eval_sync(dict(R=R, kc=kc, eps_g=2.4e-3), steps=steps, seed=seed)
    ok = r.get("verdict") == "locked"
    print("   probe R=%.4f kc=%.0e -> %s (slips=%s exc=%s rho=%s)"
          % (R, kc, r.get("verdict"), r.get("n_slips"), r.get("max_exc"), r.get("rho")), flush=True)
    return ok, r

out = {}
for kc in [1e-3, 2e-3, 4e-3, 8e-3]:
    # upper edge: bisect between locked R=1.05 and unlocked R_hi
    lo, hi = 1.02, 2.4
    ok_lo, _ = is_locked(lo, kc)
    if not ok_lo:
        out[str(kc)] = {"status": "no_lock_at_R1.02"}
        continue
    # find first unlocked
    probes = []
    R_hi = 1.3
    while R_hi <= 2.4:
        ok, r = is_locked(R_hi, kc)
        probes.append((R_hi, ok))
        if not ok:
            break
        lo = R_hi
        R_hi = round(R_hi * 1.15, 3)
    hi = R_hi
    for _ in range(4):
        mid = round(0.5 * (lo + hi), 4)
        ok, r = is_locked(mid, kc)
        probes.append((mid, ok))
        if ok: lo = mid
        else: hi = mid
    out[str(kc)] = {"R_upper_locked": lo, "R_upper_unlocked": hi,
                    "R_c_upper": round(0.5 * (lo + hi), 4), "probes": probes}
    print("kc=%.0e: R_c_upper ~ %.4f" % (kc, 0.5 * (lo + hi)), flush=True)
    with open("results_campC.json", "w") as f:
        json.dump(out, f, indent=1, default=str)
print("campC done", flush=True)
