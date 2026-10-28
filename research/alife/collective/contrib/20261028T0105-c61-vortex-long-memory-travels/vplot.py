"""c61: plot vnov.py output: per window R (cloud radius), D0 (centroid distance from ancestor), new classes per 1000 t,
far share, and the diversity-normalised c30 cohort counts; waste arm solid, twin dashed. python vplot.py vnov.json out.png"""
import sys, json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = json.load(open(sys.argv[1])); labs = list(d)
keys = [('R', 'cloud radius R (trait units)'), ('D0', 'centroid distance from ancestor'), ('newcls', 'new classes / 1000 t'),
        ('far', 'share > 0.4 from every trait seen before t-1000')]
fig, ax = plt.subplots(1, 5, figsize=(20, 3.6)); cols = plt.cm.tab10.colors
for i, l in enumerate(labs):
    for arm, ls in (('spec', '-'), ('twin', '--')):
        rows = d[l][arm]; t = [r['t'] for r in rows]
        for k, (key, name) in enumerate(keys):
            ax[k].plot(t, [r[key] for r in rows], ls, color=cols[i], label=f'{l} {arm}' if k == 0 else None)
            ax[k].set_title(name, fontsize=9); ax[k].set_xlabel('t')
    x = d[l]['div_q100']; W = 33 * 30
    ax[4].plot(np.arange(len(x['spec'])) * W, x['spec'], '-o', color=cols[i], ms=3)
    ax[4].plot(np.arange(len(x['twin'])) * W, x['twin'], '--', color=cols[i])
ax[4].set_title('c30 significant new kinds per ~1000 t\n(threshold relative to an average class)', fontsize=9)
ax[0].legend(fontsize=7); plt.tight_layout(); plt.savefig(sys.argv[2], dpi=80)
