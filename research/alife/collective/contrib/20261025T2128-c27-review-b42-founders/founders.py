"""(c21) Which cells die in pcell genealogies? Counts deaths of cells seen as one id for >= 10000 steps
(200 snapshots) and how many of them were born by a split (vs founders that appeared at t~500).
usage: founders.py gen.json.gz [...]"""
import sys, json, gzip
for fn in sys.argv[1:]:
    d = json.load(gzip.open(fn)); S, E = d["series"], d["events"]; pos = {}
    for a, x in enumerate(S):
        for i, c in enumerate(x["id"]): pos.setdefault(c, []).append(a)
    sb = set(c for t, ty, p, ch in E if ty == "split" for c in ch)
    mat = [c for t, ty, p, ch in E if ty == "death" and t > 1000 and p[0] in pos and len(pos[p[0]]) >= 200 for c in p]
    alive_founders = sum(1 for c in S[-1]["id"] if c not in sb)
    print(json.dumps(dict(file=fn, mature_deaths=len(mat), split_born_among_them=sum(c in sb for c in mat), split_born_cells=len(sb), final_cells=len(S[-1]["id"]), founders_alive_at_end=alive_founders)))
