"""For each clean prey split (as in splitstrip.py), was predator matter (> 0.3) within R px of the parent's centroid
in any saved frame from t-W to t? usage: contact.py TRACK.json FRAMES.npz [R=10] [W=20]"""
import sys, json, numpy as np
d = json.load(open(sys.argv[1])); F = np.load(sys.argv[2]); fr, ft = F['f'].astype(np.float32), F['t']
R = float(sys.argv[3]) if len(sys.argv) > 3 else 10; W = float(sys.argv[4]) if len(sys.argv) > 4 else 20
tr = d['tracks']; N = fr.shape[-1]; yy, xx = np.mgrid[0:N, 0:N]
def clean(k):
    x = tr[k]; return (x['end'] - x['start'] >= 100) or (x['fate'] == 'split' and x['end'] - x['start'] >= 25)
ev = [e for e in d['events'] if e['kind'] == 'split' and sum(clean(k) for k in e['kids']) >= 2]
allsp = [e for e in d['events'] if e['kind'] == 'split']
def touched(e):
    dy = (yy - e['c'][0] + N / 2) % N - N / 2; dx = (xx - e['c'][1] + N / 2) % N - N / 2; m = dy * dy + dx * dx <= R * R
    idx = np.where((ft >= e['t'] - W) & (ft <= e['t']))[0]
    return bool(any((fr[i][1][m] > 0.3).any() for i in idx))
res = [touched(e) for e in ev]; ra = [touched(e) for e in allsp]
print(json.dumps(dict(clean=len(ev), clean_touched=int(sum(res)), all_splits=len(allsp), all_touched=int(sum(ra)), times=[e['t'] for e in ev], touched=res)))
