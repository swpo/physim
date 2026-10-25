"""Absolute yield of dying mature cells at birth and at death, against the mean of living cells at the same times."""
import sys, json, gzip, numpy as np
fn = sys.argv[1]; d = json.load(gzip.open(fn) if fn.endswith('.gz') else open(fn)); S = d['series']
pos = {}
for a, x in enumerate(S):
    for i, cid in enumerate(x['id']): pos.setdefault(cid, []).append((a, i))
rows = []
for t, ty, p, ch in d['events']:
    if ty != 'death' or t <= 1000: continue
    a = pos.get(p[0], [])
    if len(a) < 20: continue
    (a0, i0), (a1, i1) = a[0], a[-1]
    rows.append((S[a0]['ym'][i0], S[a1]['ym'][i1], np.mean(S[a0]['ym']), np.mean(S[a1]['ym'])))
R = np.array(rows)
print(json.dumps(dict(file=fn, n=len(R), y_birth=round(float(R[:, 0].mean()), 3), y_death=round(float(R[:, 1].mean()), 3),
      pop_at_birth=round(float(R[:, 2].mean()), 3), pop_at_death=round(float(R[:, 3].mean()), 3),
      share_declined=round(float(np.mean(R[:, 1] < R[:, 0])), 2))))
