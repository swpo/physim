"""Persistent fissions with a strict window: a split counts when >= 2 daughters each live >= KS snapshots
(DT=50 -> KS=200 is 10000 steps, labkit's K) and neither merges back within that window.
Generation = parent's generation + 1 over strict splits only (cells existing at the first snapshot = 0).
Also: daughter size relative to parent (particles), and how many strict splits occur after t=20000."""
import sys, json, gzip
import numpy as np
fn = sys.argv[1]; KS = int(sys.argv[2]) if len(sys.argv) > 2 else 200
d = json.load(gzip.open(fn)); S = d['series']
life = {}; npart = {}
for a, x in enumerate(S):
    for i, cid in enumerate(x['id']):
        life.setdefault(cid, []).append(x['t']); npart.setdefault(cid, []).append(x['np'][i])
merged_at = {}
for t, ty, p, ch in d['events']:
    if ty == 'merge':
        for q in p: merged_at[q] = t
gen = {}; strict = []
for t, ty, p, ch in d['events']:
    if ty != 'split' or len(ch) < 2: continue
    good = []
    for c in ch:
        L = life.get(c, [])
        span = len(L)
        if span >= KS and not (c in merged_at and merged_at[c] - L[0] < KS * 50):
            good.append(c)
    if len(good) >= 2:
        g = gen.get(p[0], 0) + 1
        for c in good: gen[c] = g
        par_n = npart[p[0]][-1] if p[0] in npart else None
        strict.append(dict(t=t, parent=p[0], kids=good, gen=g, kid_frac=[round(npart[c][0] / max(1, sum(npart[k][0] for k in good)), 2) for c in good]))
nm = sum(1 for e in d['events'] if e[1] == 'merge')
print(json.dumps(dict(file=fn.split('/')[-1], KS_steps=KS * 50, strict_splits=len(strict), max_gen=max([s['gen'] for s in strict], default=0),
      after_20000=sum(1 for s in strict if s['t'] > 20000), merges=nm, gens=[s['gen'] for s in strict], times=[s['t'] for s in strict])))
