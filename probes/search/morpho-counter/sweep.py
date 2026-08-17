
"""sweep.py -- theory-coordinate sweep for the morpho-counter.

Theory coordinates:
  Dv     -> Turing band ratio r=k_hi/k_lo (how many rungs fit in the band;
            hysteresis lever). r must be big enough for 2 stable rungs but
            small enough to forbid rung-skipping.
  (L, n_pair) -> rung ladder position: k_n = 2 pi n / L relative to band.
  kappa  -> setpoint position inside the measured S-gap (duty-cycle lever).
  eps    -> C drive gain; slow timescale (period ~ hysteresis width / eps).
  noise  -> kinetic noise (barrier-crossing lever).
"""
import sys, json, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from runner import eval_candidate

cands = []
cid = 0
def add(**kw):
    global cid
    kw.setdefault("noise", 2e-3)
    cands.append(dict(id=cid, **kw))
    cid += 1

# --- stage A: band ratio x domain ladder (kappa=0.5, eps=2.4e-3) ---
pair_for_L = {48: (4, 5), 64: (5, 6), 80: (6, 7), 96: (7, 8)}
for Dv in [10.0, 11.0, 12.0, 15.0]:
    for L in [48, 64, 80]:
        add(Dv=Dv, L=L, kappa=0.5, eps=2.4e-3, n_pair=pair_for_L[L])
# --- stage A2: eps variation on promising ladder points ---
for Dv in [11.0, 12.0]:
    for L in [64, 80]:
        for eps in [1.2e-3, 4.8e-3]:
            add(Dv=Dv, L=L, kappa=0.5, eps=eps, n_pair=pair_for_L[L])
# --- stage B: kappa scan (duty cycle) on the L=64, Dv=11 point ---
for kap in [0.2, 0.35, 0.65, 0.8]:
    add(Dv=11.0, L=64, kappa=kap, eps=2.4e-3, n_pair=(5, 6))
# --- stage C: noise scan ---
for noise in [5e-4, 1e-3, 4e-3, 8e-3]:
    add(Dv=11.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6), noise=noise)
# --- stage D: known-bad wide-band region (expected rung skipping; log it) ---
for eps in [2.4e-3, 8e-3]:
    add(Dv=25.0, L=96, kappa=0.5, eps=eps, n_pair=(7, 8))
add(Dv=25.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6))
# --- stage E: narrow band edge (expect calib fail / weak growth) ---
add(Dv=9.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6))
add(Dv=9.5, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6))

print("total candidates:", len(cands))
results = []
t00 = time.time()
for c in cands:
    t0 = time.time()
    try:
        r = eval_candidate({k: v for k, v in c.items() if k != "id"})
        r["id"] = c["id"]
    except Exception as e:
        r = {"id": c["id"], "cand": c, "status": "error: %r" % e}
    r.pop("_rec", None)
    results.append(r)
    with open("results_sweep.json", "w") as f:
        json.dump(results, f, indent=1)
    s = r.get("status", "?")
    msg = ("id=%02d Dv=%.1f L=%d kap=%.2f eps=%.1e noise=%.0e -> %s"
           % (c["id"], c["Dv"], c["L"], c["kappa"], c["eps"], c["noise"], s))
    if s == "ok":
        msg += (" | G1=%s G2=%s G5=%s r2=%.3f flips=%s per=%s rungs=%s 2lv=%.2f sep=%.1f/%.1f"
                % (r["G1"], r["G2"], r["G5"], r["top_r2"], r["top_params"].get("n_flips"),
                   r["tau3_period"], r["rungs_visited"], r["frac_2level"],
                   r["sep12"], r["sep23"]))
    print(msg, flush=True)
print("sweep done in %.0fs" % (time.time() - t00))
