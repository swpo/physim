#!/usr/bin/env python3
"""reblend_archive.py — continuation restore step.
Re-blends archive entry interests under the new W9 using C9 from results.json
(join by cand incl. _s2/_s3 confirm rows: use the BASE cand's best ok row).
Entries with no C9 anywhere (g0-imported v2 seeds) keep their old interest —
mixed currency documented in HARVEST.md. Also backfills C9 fields into entries.
Usage: reblend_archive.py <out_dir> <W9>
"""
import json, sys, collections

out, w9 = sys.argv[1], float(sys.argv[2])
rows = json.load(open(f"{out}/results.json"))
best = {}
for r in rows:
    if r.get("status") != "ok" or r.get("C9") is None: continue
    base = r["cand"].split("_s2")[0].split("_s3")[0].split("_c9")[0]
    if base not in best or (r.get("interest") or 0) > (best[base].get("interest") or 0):
        best[base] = r
arch = json.load(open(f"{out}/archive.json"))
n_re, n_keep = 0, 0
for k, c in arch.items():
    r = best.get(c["cand"]) or best.get(str(c["cand"]).split("_s2")[0].split("_s3")[0])
    if r is None:
        n_keep += 1; continue
    iv2 = r.get("interest_v2")
    c9 = r.get("C9")
    if iv2 is None or c9 is None:
        n_keep += 1; continue
    c["interest"] = (1.0 - w9) * float(iv2) + w9 * 100.0 * float(c9)
    c["C9"] = c9; c["C9_factors"] = r.get("C9_factors")
    c["spatial_class"] = r.get("spatial_class"); c["c9_partial"] = r.get("c9_partial")
    c["interest_v2"] = iv2
    c["_reblended_w9"] = w9
    n_re += 1
json.dump(arch, open(f"{out}/archive.json", "w"))
print(f"reblended {n_re} entries at W9={w9}; kept {n_keep} (no C9 join — g0 imports)")
