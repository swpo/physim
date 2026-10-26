"""c47: where do new oscillons come from? Run world.py (WORLD_P honoured) and every DT_S time units find envelope
peaks (A local max over 5x5, A > 0.8). A peak with no previous peak within 3 px is new: 'split' if a previous peak
is within RS px (it budded off a neighbour), 'nucleation' otherwise; a previous peak with no current peak within 3 px
is a death. usage: python births.py SEED T OUT.json [DT_S=5] [RS=9]"""
import sys, os, json, importlib.util, numpy as np
from scipy.ndimage import maximum_filter
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py"))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, T, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
DS = float(sys.argv[4]) if len(sys.argv) > 4 else 5.0; RS = float(sys.argv[5]) if len(sys.argv) > 5 else 9.0
s = w.init(seed, w.META["size"]); H, W = w.META["size"]
def peaks(s):
    A = w.fields(s)[0]; m = (A == maximum_filter(A, 5, mode="wrap")) & (A > 0.8); return np.argwhere(m)
def dmin(p, Q):
    if len(Q) == 0: return 1e9
    d = np.abs(Q - p); d = np.minimum(d, [H, W] - d); return float(np.sqrt((d ** 2).sum(1)).min())
prev = None; ev = []; counts = []; nxt = 300.0
while s["t"] < T:
    w.step(s)
    if s["t"] >= nxt:
        nxt += DS; cur = peaks(s); counts.append((round(s["t"]), len(cur)))
        if prev is not None:
            for p in cur:
                if dmin(p, prev) > 3:
                    ev.append({"t": round(s["t"]), "kind": "split" if dmin(p, prev) <= RS else "nucleation", "y": int(p[0]), "x": int(p[1])})
            for p in prev:
                if dmin(p, cur) > 3: ev.append({"t": round(s["t"]), "kind": "death", "y": int(p[0]), "x": int(p[1])})
        prev = cur
k = {x: sum(1 for e in ev if e["kind"] == x) for x in ("split", "nucleation", "death")}
json.dump({"counts": counts, "events": ev, "totals": k}, open(out, "w"))
print(seed, k, "n at 300/end", counts[0][1], counts[-1][1])
