"""c28: per-track ring/motion/division report from ringtrack.py output; finds tracks showing B, M and D together."""
import json, sys, numpy as np
d = json.load(open(sys.argv[1])); T = d["tracks"]; S = d["summary"]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 256
ps = {}
# recompute persistent splits from events with the same rule as celltrack (children survive HOLD without merging)
HOLD = 400
def survives(i, until):
    tr = T[str(i)]
    if tr["t1"] >= until: return True
    return any(len(T[str(c)]["parents"]) == 1 and survives(c, until) for c in tr["children"])
for e in d["events"]:
    if e[0] == "split":
        ok = [c for c in e[3] if survives(c, e[1] + HOLD)]
        if len(ok) >= 2: ps[int(e[2])] = (e[1], ok)
born = {c for v in ps.values() for c in v[1]}
def stats(i):
    tr = T[str(i)]; P = tr["path"]
    r = [x for x in tr.get("ring", []) if x is not None]
    if len(P) < 2: return None
    cy = np.array([p[1] for p in P]); cx = np.array([p[2] for p in P])
    dy = (np.diff(cy) + N / 2) % N - N / 2; dx = (np.diff(cx) + N / 2) % N - N / 2
    BL = float(np.hypot(dy.sum(), dx.sum()) / np.sqrt(np.mean(tr["area"])))
    return dict(id=i, t0=tr["t0"], t1=tr["t1"], BL=round(BL, 2), ring_med=round(float(np.median(r)), 2) if r else None,
                ring_frac=round(float(np.mean(np.array(r) >= 1.5)), 2) if r else None, nring=len(r), nframes=len(P),
                born_by_split=i in born, divides=i in ps, children=ps[i][1] if i in ps else [])
allr = [x for tr in T.values() for x in tr.get("ring", []) if x is not None]
print("cells-frames scored:", len(allr), "median ring", round(float(np.median(allr)), 3), "frac >= 1.5:", round(float(np.mean(np.array(allr) >= 1.5)), 3))
rows = [s for s in (stats(int(k)) for k in T) if s]
full = [r for r in rows if r["divides"] and r["BL"] >= 3 and r["ring_frac"] is not None and r["ring_frac"] >= 0.5]
print("persistent splits", len(ps), "| tracks that swim >= 3 BL, ring >= 1.5 in >= half their frames, and divide:", len(full))
for r in sorted(full, key=lambda r: -r["BL"])[:10]:
    kids = [stats(c) for c in r["children"]]
    print(r, "-> children", [(k["id"], k["ring_med"], k["ring_frac"], k["BL"]) for k in kids if k])
mov = [r for r in rows if r["BL"] >= 3 and r["ring_frac"] is not None]
print("swimmers >= 3 BL:", len(mov), "with ring >= 1.5 in >= half frames:", sum(r["ring_frac"] >= 0.5 for r in mov))
