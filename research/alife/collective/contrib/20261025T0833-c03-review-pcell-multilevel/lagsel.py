"""Lagged death selection: the yield percentile of each dying cell among the living cells at a
snapshot LAG time units BEFORE its death (the cell must already exist then). If low yield causes
death, the percentile stays low at long lags; if yield collapses only while the cell dies, it
returns towards 0.5. Same for the marker zm.
usage: lagsel.py gen.json [lags...]"""
import sys, json, numpy as np

d = json.load(open(sys.argv[1])); S = d["series"]
lags = [int(x) for x in sys.argv[2:]] or [0, 1000, 2500, 5000, 10000]
pos = {}
for a, x in enumerate(S):
    for i, cid in enumerate(x["id"]):
        pos.setdefault(cid, []).append(a)

def pct(cid, tmax, key):
    a = [k for k in pos.get(cid, []) if S[k]["t"] < tmax]
    if not a:
        return None
    x = S[a[-1]]; i = x["id"].index(cid); y = x[key][i]
    o = np.array([v for j, v in enumerate(x[key]) if j != i])
    return None if len(o) == 0 else (np.sum(o < y) + 0.5 * np.sum(o == y)) / len(o)

deaths = [e for e in d["events"] if e[1] == "death" and e[0] > 1000]
for lag in lags:
    for key in ("ym", "zm"):
        p = [pct(e[2][0], e[0] - lag, key) for e in deaths]
        p = [v for v in p if v is not None]
        if p:
            print(f"lag {lag:6d} {key}: n={len(p):3d} mean pct {np.mean(p):.3f}  below median {np.sum(np.array(p) < 0.5)}/{len(p)}")
