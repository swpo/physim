"""stage2/merge_shards.py — combine pod shards into l0 results/archive.

Usage: merge_shards.py shard_*.json [--results merged_results.json]
                                    [--archive merged_archive.json]
Dedup by ghash (identical physics content across shards keeps the first).
Archive: MAP-Elites over descriptor cells, exemplar = most negative g0a margin
(V3 same rule as stage 1); counts accumulate.
"""
import argparse, glob, json, sys
from collections import defaultdict

ap = argparse.ArgumentParser()
ap.add_argument("shards", nargs="+")
ap.add_argument("--results", default="merged_results.json")
ap.add_argument("--archive", default="merged_archive.json")
args = ap.parse_args()

paths = []
for p in args.shards:
    paths += glob.glob(p)
paths = sorted(set(paths))
print(f"merging {len(paths)} shards")

seen = set()
merged = []
arch = {}
dups = 0
shard_meta = []
for p in paths:
    try:
        sh = json.load(open(p))
    except Exception as e:
        print(f"  SKIP {p}: {e}")
        continue
    shard_meta.append(dict(path=p, seed=sh.get("shard_seed"), n=len(sh.get("records", [])),
                           wall_s=sh.get("wall_s")))
    for rec in sh.get("records", []):
        h = rec.get("ghash")
        if h and h in seen:
            dups += 1
            continue
        if h:
            seen.add(h)
        merged.append(rec)
        if rec.get("stage") == "assayed" and rec.get("desc"):
            key = "|".join(rec["desc"])
            m = rec.get("g0a_margin", 0.0)
            cell = arch.get(key)
            if cell is None:
                arch[key] = dict(margin=m, genome=rec["genome"], cand=rec["cand"],
                                 count=1)
            else:
                cell["count"] += 1
                if m < cell["margin"]:
                    cell.update(margin=m, genome=rec["genome"], cand=rec["cand"])

json.dump(merged, open(args.results, "w"))
json.dump(arch, open(args.archive, "w"))
print(f"merged {len(merged)} candidates ({dups} ghash dups dropped)")
print(f"archive cells: {len(arch)}")
alive = [r for r in merged if r.get("a1") and
         any(v.get("cls") in ("persist", "travel") for v in r["a1"].values())]
onsets = [r for r in merged if r.get("desc") and r["desc"][7] == "onset"]
bonds = [r for r in merged if r.get("a2") and
         any(a["cls"] == "bond" for a in r["a2"])]
print(f"alive: {len(alive)}  bonds: {len(bonds)}  motility onsets: {len(onsets)}")
for m in shard_meta:
    print(f"  {m['path']}: seed={m['seed']} n={m['n']} wall={m['wall_s']}")
