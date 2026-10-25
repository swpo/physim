"""How many celltrack splits are re-separations of a recent collision? For each binary split whose two children
each live >= 400 t, walk its ancestry back 600 t and flag it if any ancestor in that window was a merge product.
usage: merge_then_split.py celltrack.json"""
import json, sys
d = json.load(open(sys.argv[1])); T = d["tracks"]
def merged_recently(k, window=600):
    t_split = T[k]["t1"]; stack = [k]; seen = set()
    while stack:
        c = stack.pop()
        if c in seen: continue
        seen.add(c); t = T[c]
        if len(t["parents"]) >= 2 and t["t0"] >= t_split - window: return t["t0"]
        if t["t0"] >= t_split - window: stack += [str(p) for p in t["parents"]]
    return None
for k in ("627", "696", "631"): print(f"strip row {k}: merge at t={merged_recently(k)} before its split at t={T[k]['t1']}")
sp = [k for k, t in T.items() if len(t["children"]) == 2 and all(T[str(c)]["t1"] - T[str(c)]["t0"] >= 400 for c in t["children"])]
m = [k for k in sp if merged_recently(k) is not None]
print(f"binary splits with both children >= 400 t: {len(sp)}; preceded by a merge within 600 t: {len(m)} ({len(m)/len(sp):.0%})")
