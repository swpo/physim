import json, sys, numpy as np
from scipy.signal import find_peaks
for f in sys.argv[1:]:
    d = json.load(open(f)); R = np.array(d['rows']); t = R[:, 0]; m = t >= 1000
    a, b = R[m, 3], R[m, 4]   # prey mass, predator mass
    a0, b0 = a - a.mean(), b - b.mean()
    lags = np.arange(-30, 31); cc = [np.corrcoef(a0[max(0,-l):len(a0)-max(0,l)], b0[max(0,l):len(b0)-max(0,-l)])[0,1] for l in lags]
    lb = lags[np.argmax(cc)] * 100
    pk, _ = find_peaks(b, prominence=0.2 * (b.max() - b.min()), distance=5)
    sp = np.diff(t[m][pk])
    print(f.replace('.json',''), 'pred mass min/max %.3f/%.3f' % (b.min(), b.max()), 'best lag (pred after prey) %d t, r=%.2f' % (lb, max(cc)), 'pred peaks', len(pk), 'spacing', sp.tolist())
