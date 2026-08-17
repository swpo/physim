
"""campB2_slipscaling.py -- refined G3a: winding rate vs detuning past the edge.
Primary observable: T_slip_rate = span / |net winding| (asymptotic inter-slip
time; robust for few-slip runs). Longer runs near the edge.
Also symmetry check R -> 1/R (ring swap) at two points.
"""
import sys, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
from sync_runner import eval_sync

pts = [(1.74, 800000), (1.76, 800000), (1.78, 600000), (1.82, 500000),
       (1.88, 400000), (1.96, 300000), (2.10, 300000), (2.30, 300000)]
out = []
for R, steps in pts:
    r = eval_sync(dict(R=R, kc=2e-3, eps_g=2.4e-3), steps=steps, seed=1)
    out.append(r)
    print("R=%.2f (%dk): %s v=%s slips=%s T_med=%s T_rate=%s rho=%s alive=%s/%s (%.0fs)"
          % (R, steps//1000, r["status"], r.get("verdict"), r.get("n_slips"),
             r.get("T_slip"), r.get("T_slip_rate"), r.get("rho"),
             r.get("alive1", {}).get("alive"), r.get("alive2", {}).get("alive"),
             r.get("runtime_s", -1)), flush=True)
    with open("results_campB2.json", "w") as f:
        json.dump(out, f, indent=1, default=str)
# symmetry checks
for R, steps in [(0.6, 250000), (0.5, 250000)]:
    r = eval_sync(dict(R=R, kc=2e-3, eps_g=2.4e-3), steps=steps, seed=1)
    out.append(r)
    print("SYM R=%.3f: v=%s slips=%s rho=%s" % (R, r.get("verdict"), r.get("n_slips"), r.get("rho")), flush=True)
    with open("results_campB2.json", "w") as f:
        json.dump(out, f, indent=1, default=str)
print("campB2 done", flush=True)
