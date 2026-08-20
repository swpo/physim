"""yield_curves.py — stage-1 primary deliverable: funnel pass-rates, assay
outcomes per 100 candidates by strategy, wall-clock per stage.

Usage: yield_curves.py [tag]   (default s1v3). Writes data/yield_<tag>.json and
prints a human table.
"""
import sys, os, json
from collections import Counter, defaultdict
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
TAG = sys.argv[1] if len(sys.argv) > 1 else "s1v3"

res = json.load(open(os.path.join(BASE, "results.json")))
cands = [r for r in res if r.get("kind") == "candidate" and r.get("tag") == TAG]

out = dict(tag=TAG, n=len(cands))
tbl = {}
for strat in ("uniform", "jitter"):
    rows = [r for r in cands if r["strategy"] == strat]
    n = len(rows)
    if n == 0:
        continue
    st = Counter(r["stage"] for r in rows)
    # funnel stage rates
    g0b_pass = sum(1 for r in rows if r["stage"] not in ("fail_g0b", "invalid", "error"))
    g0a_pass = sum(1 for r in rows if r["stage"] in ("pass", "assayed"))
    osc = sum(1 for r in rows if r.get("g0c_any_osc"))
    chem = sum(1 for r in rows if r.get("g0c_any_chem"))
    shelf = sum(1 for r in rows if r.get("excitable_shelf"))
    # assay outcome counts (per-act best class)
    a1 = Counter()
    pairs = Counter()
    mot = Counter()
    for r in rows:
        if r.get("a1"):
            best = min((v["cls"] for v in r["a1"].values()),
                       key=lambda c: {"travel":0,"persist":1,"multi":2,"domain":3,
                                      "replicate":4,"die":5,"blowup":6}.get(c, 9))
            a1[best] += 1
        if r.get("desc"):
            pairs[r["desc"][6]] += 1
            mot[r["desc"][7]] += 1
    # wall-clock
    def med(key):
        v = [r[key] for r in rows if r.get(key) is not None]
        return float(np.median(v)) if v else None
    tbl[strat] = dict(
        n=n, stages=dict(st),
        rate_g0b=g0b_pass / n, rate_g0a=g0a_pass / n,
        rate_osc=osc / n, rate_chem=chem / n, rate_shelf=shelf / n,
        a1_per100={k: 100.0 * v / n for k, v in a1.items()},
        alive_per100=100.0 * (a1["persist"] + a1["travel"]) / n,
        pair_per100={k: 100.0 * v / n for k, v in pairs.items()},
        motility_per100={k: 100.0 * v / n for k, v in mot.items()},
        wall_med_funnel_s=med("funnel_s"), wall_med_assay_s=med("assay_s"),
        wall_med_total_s=med("total_s"),
        wall_sum_s=sum(r.get("total_s", 0) for r in rows))
out["by_strategy"] = tbl

# archive census
try:
    arch = json.load(open(os.path.join(BASE, "archive.json")))
    out["archive_cells"] = len(arch)
    out["archive_keys"] = sorted(arch.keys())
except FileNotFoundError:
    out["archive_cells"] = 0

os.makedirs(os.path.join(BASE, "data"), exist_ok=True)
with open(os.path.join(BASE, "data", f"yield_{TAG}.json"), "w") as f:
    json.dump(out, f, indent=1)

print(f"== YIELD {TAG} (n={out['n']}) ==")
for strat, d in tbl.items():
    print(f"-- {strat} n={d['n']} --")
    print(f"  G0b {100*d['rate_g0b']:.0f}%  G0a {100*d['rate_g0a']:.0f}%  "
          f"osc-tails {100*d['rate_osc']:.0f}%  chem-box {100*d['rate_chem']:.0f}%  "
          f"shelf {100*d['rate_shelf']:.0f}%")
    print(f"  A1/100: {dict((k, round(v)) for k, v in d['a1_per100'].items())}")
    print(f"  ALIVE/100: {d['alive_per100']:.1f}   pair: "
          f"{dict((k, round(v)) for k, v in d['pair_per100'].items())}")
    print(f"  motility: {dict((k, round(v)) for k, v in d['motility_per100'].items())}")
    print(f"  wall med: funnel {d['wall_med_funnel_s']}s assay {d['wall_med_assay_s']}s "
          f"total {d['wall_med_total_s']}s; sum {d['wall_sum_s']/60:.1f} min")
print("archive cells:", out.get("archive_cells"))
