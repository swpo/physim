"""When does a dying cell's yield become low? (c01, review of c06 pcell-multilevel)
For each mature cell that dies (>= 20 snapshots), its yield percentile among the living cells at
fractions 0.1, 0.25, 0.5, 0.75 and 1.0 of its observed life (first to last snapshot).
Usage: python lifecourse.py gen.json [key]"""
import json
import sys

import numpy as np

d = json.load(open(sys.argv[1])); S = d["series"]; key = sys.argv[2] if len(sys.argv) > 2 else "ym"
pos = {}
for a, x in enumerate(S):
    for i, cid in enumerate(x["id"]):
        pos.setdefault(cid, []).append(a)


def pct_at(cid, a):
    x = S[a]; i = x["id"].index(cid); y = x[key][i]
    o = np.array([v for j, v in enumerate(x[key]) if j != i])
    return (np.sum(o < y) + 0.5 * np.sum(o == y)) / len(o) if len(o) else None


fr = [0.1, 0.25, 0.5, 0.75, 1.0]
rows = []
for e in d["events"]:
    if e[1] != "death" or e[0] <= 1000:
        continue
    cid = e[2][0]; a = pos.get(cid, [])
    if len(a) < 20:
        continue
    rows.append([pct_at(cid, a[min(len(a) - 1, int(f * (len(a) - 1)))]) for f in fr])
R = np.array([[np.nan if v is None else v for v in r] for r in rows])
print(json.dumps({"file": sys.argv[1], "key": key, "n_deaths": len(rows),
                  "mean_pct_at_life_fraction": {str(f): round(float(np.nanmean(R[:, k])), 3) for k, f in enumerate(fr)},
                  "below_median_at_life_fraction": {str(f): int(np.nansum(R[:, k] < 0.5)) for k, f in enumerate(fr)}}))
