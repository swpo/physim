"""Share of in-cell particles held by the largest cell, over time, from genealogy json files."""
import sys, json, gzip, numpy as np
for fn in sys.argv[1:]:
    d = json.load(gzip.open(fn) if fn.endswith('.gz') else open(fn)); S = [x for x in d['series'] if x['n']]
    sh = np.array([max(x['np']) / sum(x['np']) for x in S]); t = np.array([x['t'] for x in S])
    w = t >= 20000
    print(fn, 'largest share t>=20000: median %.2f max %.2f; frac of time > 0.3: %.2f; cells median %d' % (np.median(sh[w]), sh[w].max(), (sh[w] > 0.3).mean(), np.median([x['n'] for x in S if x['t'] >= 20000])))
