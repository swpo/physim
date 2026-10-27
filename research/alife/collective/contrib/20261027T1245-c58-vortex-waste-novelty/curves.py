"""c58: novelty curves: cumulative number of trait classes (round(theta/0.4)) ever held by >= 3 vortices at once, and the
range of classes held by >= 3 vortices, against t. python curves.py out.png run.json ..."""
import sys, json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(11, 3.6)); dm = 0.4
for f in sys.argv[2:]:
    r = json.load(open(f)); ever = set(); T = []; C = []; LO = []; HI = []
    for t, th in r['traits_by_frame']:
        u, n = np.unique(np.round(np.array(th) / dm).astype(int), return_counts=True); held = [int(c) for c, k in zip(u, n) if k >= 3]
        ever |= set(held); T.append(t); C.append(len(ever)); LO.append(min(held) if held else np.nan); HI.append(max(held) if held else np.nan)
    ls = '-' if 'spec' in f else '--'; lab = f.replace('.json', '')
    l, = ax[0].plot(T, C, ls, label=lab); ax[1].plot(T, HI, ls, color=l.get_color(), label=lab); ax[1].plot(T, LO, ls, color=l.get_color())
    k = np.searchsorted(T, [3000, 6000, 9000]); print(f, 'cumulative classes at t=3000/6000/9000/end', [C[i] for i in k if i < len(C)] + [C[-1]])
ax[0].set_xlabel('t'); ax[0].set_ylabel('classes ever held by >= 3 vortices'); ax[1].set_xlabel('t'); ax[1].set_ylabel('highest / lowest class held by >= 3')
ax[0].legend(fontsize=7); fig.tight_layout(); fig.savefig(sys.argv[1], dpi=80)
