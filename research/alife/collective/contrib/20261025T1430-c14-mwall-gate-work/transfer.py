"""Horizontal transfer of heritable particles between cells.
Every DT steps: cells = periodic components of phi > 1/2; each particle's cell. A move A -> B (both cells)
counts as a transfer unless B is a successor of A (receives >= 20% of A's particles: a split/persistence)
and A is B's main predecessor. Escapes = particles in a cell that are outside any cell DT later.
usage: python transfer.py world.py seed T [key=val ...]  -> prints transfer and escape rates per in-cell particle per 1000 t"""
import sys, json, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit.world import load_world
from genealogy import plabel
world, seed, T = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
W = load_world(world)
for a in sys.argv[4:]:
    k, v = a.split('='); W.P[k] = float(v)
s = W.init(seed, (128, 128)); DT = 50; T0 = 5000
prev = None; tr = esc = incell = 0
for t in range(T + 1):
    if t % DT == 0 and t >= T0:
        lab, n = plabel(s['phi'] > 0.5); H, Wd = lab.shape
        c = lab[s['py'].astype(int) % H, s['px'].astype(int) % Wd]
        cur = dict(zip(s['uid'].tolist(), c.tolist()))
        if prev is not None:
            u = np.array([x for x in s['uid'].tolist() if x in prev])
            a = np.array([prev[x] for x in u]); b = np.array([cur[x] for x in u])
            m = (a > 0) & (b > 0)
            pairs = {}
            for x, y in zip(a[m], b[m]): pairs[(x, y)] = pairs.get((x, y), 0) + 1
            outA = {}; inB = {}
            for (x, y), k in pairs.items(): outA[x] = outA.get(x, 0) + k; inB[y] = inB.get(y, 0) + k
            for (x, y), k in pairs.items():
                succ = k >= 0.2 * outA[x]
                main = k == max(v for (p, q), v in pairs.items() if q == y)
                if not (succ and main): tr += k
            esc += int(((a > 0) & (b == 0)).sum()); incell += int((a > 0).sum())
        prev = cur
    s = W.step(s)
r = 1000 / DT
print(json.dumps(dict(world=world, seed=seed, T=T, params=sys.argv[4:], transfer_per_1000t=round(tr / max(incell, 1) * r, 6), escape_per_1000t=round(esc / max(incell, 1) * r, 5), cells_end=int(plabel(s['phi'] > 0.5)[1]), N=len(s['py']))))
