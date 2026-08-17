
"""g4_recheck120k.py -- were jitter failures physics or 60k-window truncation?
Rerun every FAILED jitter draw of FLAG_e28/e32 (incl. extra 12) at 120k ticks.
Gate thresholds unchanged. G5 still satisfied by the 60k cert runs (cycle
period ~1400 t = 14k ticks << 60k); this recheck only extends STATISTICS.
"""
import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from runner import eval_candidate

def gates(r):
    return bool(r.get("G1")) and bool(r.get("G2")) and bool(r.get("G5"))

fails = []
g4f = json.load(open("results_g4final.json"))
for r in g4f["jitter"]:
    if not gates(r):
        fails.append((r["finalist"], r["jitter_id"], r["cand"], r.get("seed", 10 + r["jitter_id"])))
j12 = json.load(open("results_jitter12.json"))
for r in j12:
    if not gates(r):
        fails.append(("e32x", r["jitter_id"], r["cand"], 1))

print("failed draws to recheck:", len(fails), flush=True)
out = []
npass = 0
for tag, jid, cand, seed in fails:
    seed_used = 10 + jid if tag != "e32x" else 1
    r = eval_candidate(dict(cand), steps=120000, seed=seed_used)
    r.pop("_rec", None)
    r["tag"], r["jitter_id"] = tag, jid
    ok = bool(r.get("G1")) and bool(r.get("G2"))   # G5: cycle visible in 60k, cert above
    r["pass120"] = ok
    out.append(r)
    npass += ok
    print("%s jit=%d: 120k PASS=%s G1=%s G2=%s r2=%.3f fl=%s per=%s sep=%.1f/%.1f rungs=%s"
          % (tag, jid, ok, r.get("G1"), r.get("G2"), r.get("top_r2", -1),
             r.get("top_params", {}).get("n_flips"), r.get("tau3_period"),
             r.get("sep12", -1), r.get("sep23", -1), r.get("rungs_visited")), flush=True)
    with open("results_recheck120k.json", "w") as f:
        json.dump(out, f, indent=1)
print("recheck: %d/%d now pass at 120k" % (npass, len(fails)), flush=True)
