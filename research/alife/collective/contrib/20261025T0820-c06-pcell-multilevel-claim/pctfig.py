import sys, json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.argv = sys.argv
f, ax = plt.subplots(1, 2, figsize=(9, 3.5))
for k, (lab, fn) in enumerate(a.split('=') for a in sys.argv[2:]):
    key = lab.split(':')[-1] if ':' in lab else 'ym'
    d = json.load(open(fn)); S = d['series']; pos = {}
    for a_, x in enumerate(S):
        for cid in x['id']: pos.setdefault(cid, []).append(a_)
    def pct(cid, tb):
        a_ = [q for q in pos.get(cid, []) if S[q]['t'] < tb]
        if not a_: return None
        x = S[a_[-1]]; i = x['id'].index(cid); y = x[key][i]; o = np.array([v for j, v in enumerate(x[key]) if j != i])
        return None if not len(o) else (np.sum(o < y) + 0.5 * np.sum(o == y)) / len(o)
    D = [p for p in (pct(e[2][0], e[0]) for e in d['events'] if e[1] == 'death' and e[0] > 1000) if p is not None]
    B = [p for p in (pct(e[2][0], e[0]) for e in d['events'] if e[1] == 'split' and len(e[3]) >= 2 and e[0] > 1000) if p is not None]
    ax[0].hist(D, bins=np.linspace(0, 1, 11), histtype='step', lw=2, label=f'{lab} (n={len(D)})')
    ax[1].hist(B, bins=np.linspace(0, 1, 6), histtype='step', lw=2, label=f'{lab} (n={len(B)})')
ax[0].set_title('dying cells: yield percentile among living cells'); ax[1].set_title('splitting cells: yield percentile')
for a in ax: a.set_xlabel('percentile'); a.legend(fontsize=7)
plt.tight_layout(); plt.savefig(sys.argv[1], dpi=85)
