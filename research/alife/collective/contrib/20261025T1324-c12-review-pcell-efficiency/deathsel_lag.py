"""deathsel.py, but each dying cell's yield percentile is read LAG snapshots before its last one (so a terminal
artefact of a starving cell cannot make it), and only for cells seen in >= LAG + 5 snapshots.
usage: deathsel_lag.py gen.json key lag"""
import sys, json, numpy as np
d = json.load(open(sys.argv[1])); S = d['series']; key = sys.argv[2]; lag = int(sys.argv[3])
pos = {}
for a, x in enumerate(S):
    for i, cid in enumerate(x['id']):
        pos.setdefault(cid, []).append(a)
def pct_at(cid, a):
    x = S[a]; i = x['id'].index(cid); y = x[key][i]; o = np.array([v for j, v in enumerate(x[key]) if j != i])
    return (np.sum(o < y) + 0.5 * np.sum(o == y)) / len(o)
D = []
for e in d['events']:
    if e[1] == 'death' and e[0] > 1000:
        a = pos.get(e[2][0], [])
        if len(a) >= lag + 5: D.append(pct_at(e[2][0], a[-1 - lag]))
dt = S[1]['t'] - S[0]['t']
print(json.dumps(dict(key=key, lag_snapshots=lag, lag_time=lag * dt, n_death=len(D), death_pct_mean=round(float(np.mean(D)), 3) if D else None,
                      below_median=int(sum(p < 0.5 for p in D)))))
