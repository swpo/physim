"""Established fusions vs clean splits in a fltrack_m.py output. usage: fusion.py TRACK.json [AGE=100]
clean split: as splitstrip.py (both daughters last >= 100 t, or split again cleanly after >= 25 t).
established fusion: a merge whose parents include >= 2 bodies that each existed unchanged >= AGE t (since their own
last split/merge/nucleation) and each have >= 25% of the largest parent's area."""
import sys, json
d = json.load(open(sys.argv[1])); AGE = float(sys.argv[2]) if len(sys.argv) > 2 else 100
tr = d['tracks']; ev = d['events']
def clean(k):
    x = tr[k]; return (x['end'] - x['start'] >= 100) or (x['fate'] == 'split' and x['end'] - x['start'] >= 25)
cs = [e for e in ev if e['kind'] == 'split' and sum(clean(k) for k in e['kids']) >= 2]
mg = [e for e in ev if e['kind'] == 'merge']
def est(e):
    big = max(e['areas']); return sum(a >= AGE and ar >= 0.25 * big for a, ar in zip(e['ages'], e['areas'])) >= 2
fu = [e for e in mg if est(e)]
print(json.dumps(dict(splits=sum(e['kind'] == 'split' for e in ev), merges=len(mg), clean_splits=len(cs), established_fusions=len(fu),
                      fusions_free=sum(all(e['free']) for e in fu), fusion_times=[e['t'] for e in fu], age=AGE)))
