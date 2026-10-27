"""python counts.py : persistent splits after t=12000 (frame 120, 100 t per frame) and body counts at t=12000/21000/30000."""
import json
for p in ['W800s2', 'nowash_s2']:
    m = json.load(open(p + '/metrics.json')); ps = [e['frame'] for e in m['persistent_splits']]; n = m['series']['n_comp']
    print(p, 'persistent splits', len(ps), 'after t=12000', sum(f > 120 for f in ps), 'last split t', max(ps) * 100 if ps else None, 'bodies t=12000/21000/30000', n[120], n[210], n[300])
