
"""campC2_weakedge.py -- add kc=5e-4 and kc=1.5e-3 tongue edges (weak-coupling
linearity of width) via the same locked/slip bisection as campC."""
import sys, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
from sync_runner import eval_sync

def is_locked(R, kc, steps=200000, seed=1):
    r = eval_sync(dict(R=R, kc=kc, eps_g=2.4e-3), steps=steps, seed=seed)
    ok = r.get("verdict") == "locked"
    print("   probe R=%.4f kc=%.1e -> %s (slips=%s exc=%s rho=%s)"
          % (R, kc, r.get("verdict"), r.get("n_slips"), r.get("max_exc"), r.get("rho")), flush=True)
    return ok, r

out = json.load(open("results_campC.json"))
for kc, R_grid in [(5e-4, [1.05, 1.1, 1.15, 1.2, 1.25]),
                   (1.5e-3, [1.3, 1.45, 1.55, 1.65])]:
    lo, hi = None, None
    probes = []
    prev_ok_R = 1.0
    for R in R_grid:
        ok, r = is_locked(R, kc)
        probes.append((R, ok))
        if ok:
            prev_ok_R = R
        else:
            lo, hi = prev_ok_R, R
            break
    if lo is None:
        lo, hi = R_grid[-1], R_grid[-1] * 1.2
        ok, _ = is_locked(hi, kc)
        probes.append((hi, ok))
        if ok:
            out[str(kc)] = {"status": "edge_beyond_grid"}
            continue
    for _ in range(3):
        mid = round(0.5 * (lo + hi), 4)
        ok, r = is_locked(mid, kc)
        probes.append((mid, ok))
        if ok: lo = mid
        else: hi = mid
    out[str(kc)] = {"R_upper_locked": lo, "R_upper_unlocked": hi,
                    "R_c_upper": round(0.5 * (lo + hi), 4), "probes": probes}
    print("kc=%.1e: R_c_upper ~ %.4f" % (kc, 0.5 * (lo + hi)), flush=True)
    with open("results_campC.json", "w") as f:
        json.dump(out, f, indent=1, default=str)
print("campC2 done", flush=True)
