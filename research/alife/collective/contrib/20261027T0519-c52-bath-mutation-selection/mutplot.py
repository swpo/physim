import json, glob, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
sty = {'sel': ('C3', 'selective (e hunts, b no taxis), gated'), 'sel3': ('C1', 'selective, gated, 3x conversion'), 'neu': ('C0', 'neutral (both hunt), gated'),
       'nogate': ('k', 'selective, conversion everywhere'), 'half': ('C2', 'b half taxis, gated')}
for f in sorted(glob.glob('mut/*.json')):
    n = f.split('/')[-1][:-5]; arm, seed = n.rsplit('_', 1); c, lab = sty[arm]
    R = np.array(json.load(open(f))['rows']); m = R[:, 0] > 2000
    ax[0].plot(R[m, 0], R[m, 2] / R[m, 1], color=c, ls='-' if seed == 's0' else '--', label=f'{lab} {seed}')
    ax[1].plot(R[m, 0], R[m, 5] / np.maximum(R[m, 4] + R[m, 5], 1), color=c, ls='-' if seed == 's0' else '--')
ax[0].set_yscale('log'); ax[0].set_ylabel('total material e / b'); ax[0].axhline(1, color='gray', lw=0.5); ax[0].legend(fontsize=6)
ax[1].set_ylabel('share of predator bodies that are kind e'); [a.set_xlabel('t') for a in ax]
plt.tight_layout(); plt.savefig('mut/selection.png', dpi=80)
