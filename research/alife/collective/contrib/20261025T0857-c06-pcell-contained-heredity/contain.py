"""Containment of catalyst particles by the self-made wall, per cell and over time.

Every 250 steps, for each cell (periodic component of phi > 1/2 with >= 20 particles):
inside density = particles per px inside the cell; outside density = particles per px in
the shell 2-6 px (x scale) beyond the cell boundary (excluding other cells). Reports the
per-cell ratio in/out (inf when the shell is empty), the share of cells with ratio >= 2,
and the share of all particles inside cells.
usage: python contain.py world.py seed T out.json [key=val ...]
"""
import sys, json
import numpy as np
from scipy import ndimage
sys.path.insert(0, '/home/user/physim/research/alife')
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from labkit.world import load_world
from genealogy import plabel

world, seed, T, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
W = load_world(world)
for kv in sys.argv[5:]:
    k, v = kv.split('='); W.P[k] = float(v)
sc = W.P.get('scale', 1.0)
H = Wd = int(round(128 * sc))
s = W.init(seed, (H, Wd))
rec = []
for t in range(T + 1):
    if t % 250 == 0 and t >= 1000:
        inside = s['phi'] > 0.5
        lab, n = plabel(inside)
        cnt = np.bincount((s['py'].astype(int) % H) * Wd + (s['px'].astype(int) % Wd), minlength=H * Wd).reshape(H, Wd)
        cells = []
        for i in range(1, n + 1):
            m = lab == i
            nin = cnt[m].sum()
            if nin < 20:
                continue
            d6 = ndimage.binary_dilation(m, iterations=int(round(6 * sc)))
            d2 = ndimage.binary_dilation(m, iterations=int(round(2 * sc)))
            shell = d6 & ~d2 & ~inside
            rin = nin / m.sum(); rout = cnt[shell].sum() / max(1, shell.sum())
            cells.append(dict(n=int(nin), area=int(m.sum()), din=float(rin), dout=float(rout), ratio=float(rin / rout) if rout > 0 else 1e9))
        tot = len(s['py'])
        frac_in = float(cnt[inside].sum() / max(1, tot))
        r = [c['ratio'] for c in cells]
        rec.append(dict(t=t, ncell=len(cells), frac_in=frac_in, share_ratio_ge2=float(np.mean([x >= 2 for x in r])) if r else 0,
                        median_ratio=float(np.median(r)) if r else 0, min_ratio=float(min(r)) if r else 0,
                        median_din=float(np.median([c['din'] for c in cells])) if cells else 0,
                        median_dout=float(np.median([c['dout'] for c in cells])) if cells else 0))
        if t % 2000 == 0:
            print(json.dumps(rec[-1]), flush=True)
    s = W.step(s)
json.dump(rec, open(out, 'w'))
