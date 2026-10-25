"""Mean particle yield, cell count and cumulative cell deaths from genealogy JSONs. usage: yfig.py out.png label=file ..."""
import sys, json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
f, ax = plt.subplots(1, 3, figsize=(14, 3.8))
ci = -1
for i, a in enumerate(sys.argv[2:]):
    ci += 0 if 'twin' in a.split('=')[0] else 1
    lab, fn = a.split('='); d = json.load(open(fn)); S = d['series']
    t = [x['t'] for x in S]
    ym = [np.dot(x['np'], x['ym']) / max(1, sum(x['np'])) for x in S]
    dt = sorted(e[0] for e in d['events'] if e[1] == 'death')
    ls = '--' if 'twin' in lab else '-'
    c = plt.cm.tab10(ci)
    ax[0].plot(t, ym, ls, color=c, label=lab); ax[1].plot(t, [x['n'] for x in S], ls, color=c, label=lab)
    ax[2].step([0] + dt + [t[-1]], list(range(len(dt) + 1)) + [len(dt)], ls, color=c, where='post', label=lab)
ax[0].set_ylabel('mean link yield of particles in cells'); ax[1].set_ylabel('cells'); ax[2].set_ylabel('cumulative whole-cell deaths')
for a in ax: a.set_xlabel('t'); a.legend(fontsize=7)
plt.tight_layout(); plt.savefig(sys.argv[1], dpi=85)
