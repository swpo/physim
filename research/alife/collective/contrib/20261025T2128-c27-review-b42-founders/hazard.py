"""(c27) Death hazard of MATURE cells (one id for >= 200 snapshots) per unit exposure, founders vs split-born,
from genealogy.py output. Exposure counts each snapshot a mature cell is alive (snapshot spacing from the series).
Also the hazard after t=50000 only (when founders and born cells coexist as adults).
usage: hazard.py gen.json.gz [...]"""
import sys, json, gzip
tot = {}
for fn in sys.argv[1:]:
    d = json.load(gzip.open(fn)); S, E = d["series"], d["events"]
    dt = S[1]["t"] - S[0]["t"]
    sb = set(c for t, ty, p, ch in E if ty == "split" for c in ch)
    first = {}
    for a, x in enumerate(S):
        for c in x["id"]: first.setdefault(c, a)
    dead = {}
    for t, ty, p, ch in E:
        if ty == "death":
            for c in p: dead[c] = t
    row = {}
    for late in (0, 50000):
        ex = {"founder": 0, "born": 0}; dd = {"founder": 0, "born": 0}
        for a, x in enumerate(S):
            if x["t"] < late: continue
            for c in x["id"]:
                if a - first[c] >= 200: ex["born" if c in sb else "founder"] += dt
        for c, t in dead.items():
            if t >= late and c in first and t - S[first[c]]["t"] >= 200 * dt:
                dd["born" if c in sb else "founder"] += 1
        row[f"from_t{late}"] = {k: {"deaths": dd[k], "exposure_cell_steps": ex[k], "hazard_per_1e5": round(1e5 * dd[k] / ex[k], 3) if ex[k] else None} for k in ex}
        for k in ex:
            tt = tot.setdefault(f"from_t{late}", {}).setdefault(k, [0, 0]); tt[0] += dd[k]; tt[1] += ex[k]
    print(json.dumps({"file": fn, **row}))
print(json.dumps({"pooled": {w: {k: {"deaths": v[0], "exposure": v[1], "hazard_per_1e5": round(1e5 * v[0] / v[1], 3) if v[1] else None} for k, v in r.items()} for w, r in tot.items()}}))
