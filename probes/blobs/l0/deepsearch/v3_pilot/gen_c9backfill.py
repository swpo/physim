#!/usr/bin/env python3
"""gen_c9backfill.py — emit eval jobs for archive entries lacking C9 (g0 imports)
so the whole archive can be reblended in one currency. Run BEFORE reblend.
Usage: gen_c9backfill.py <out_dir> [island_seed]   -> writes out/jobs/c9fill_w0.json
"""
import json, sys, os
out = sys.argv[1]
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
arch = json.load(open(f"{out}/archive.json"))
rows = json.load(open(f"{out}/results.json"))
have = set()
for r in rows:
    if r.get("C9") is not None and r.get("status") == "ok":
        have.add(r["cand"].split("_s2")[0].split("_s3")[0].split("_c9")[0])
jobs = []
for k, c in arch.items():
    if c.get("C9") is not None or c["cand"] in have:
        continue
    g = c["genome"]
    if isinstance(g, str):
        g = json.loads(g)
    jobs.append(dict(cand=c["cand"] + "_c9", gen=c.get("gen", 0), op="c9fill",
                     kind="c9fill", parents=[c["cand"]], seed=seed,
                     genome=g))
os.makedirs(f"{out}/jobs", exist_ok=True)
json.dump(jobs, open(f"{out}/jobs/c9fill_w0.json", "w"))
print(f"c9fill jobs: {len(jobs)} -> {out}/jobs/c9fill_w0.json")
