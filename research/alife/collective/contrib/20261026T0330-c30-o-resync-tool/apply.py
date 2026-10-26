"""Re-score evoloop (c16 census) and the seeded BFF soup (c30 functional census) with o_resync.new_adaptive."""
import sys, os, json, gzip, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from o_resync import new_adaptive
C = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
out = {}
for s in (1, 2, 3):
    d = json.load(gzip.open(f"{C}/20261025T1457-c16-evoloop-not-open-ended/census/geno_s{s}.json.gz", "rt"))
    rows = [c["full"] for c in d["census"]]
    for g in (1, 5, 20):
        r = new_adaptive(rows, g=g, win=25); out[f"evoloop_s{s}_g{g}"] = r
        print(f"evoloop s{s} g={g}: a0={r['a0']:.0f} new adaptive {r['n_new']} by crossing window (50k steps) {r['by_cross']}", flush=True)
fr = json.load(gzip.open(f"{C}/20261026T0204-c30-bff-soup-o/data/func_census_s0.json.gz", "rt"))
rows = [r["census"] for r in fr]
for g in (10, 25, 50):
    r = new_adaptive(rows, g=g, win=20); out[f"bff_functional_g{g}"] = r
    print(f"bff functional g={g}: a0={r['a0']:.0f} new adaptive {r['n_new']} by crossing window (1000 epochs) {r['by_cross']}", flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resync_results.json"), "w"), indent=1)
