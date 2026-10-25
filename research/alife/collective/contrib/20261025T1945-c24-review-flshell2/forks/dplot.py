import sys, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
pre = sys.argv[1]; fig, ax = plt.subplots(2, 7, figsize=(21, 6.4))
for r, arm in enumerate(('cut', 'fed')):
    d = np.load(f'{pre}_{arm}.npz'); X = d['X'].astype(np.float32); t = d['t']; P = d['P']; Q = d['Q']
    for j, i in enumerate(np.linspace(0, len(t)-1, 6).astype(int)):
        Y = X[i]; im = np.stack([np.clip(Y[3], 0, 1), np.clip(Y[:2].sum(0)/2, 0, 1), np.clip(Y[2]/0.2, 0, 1)], -1)
        ax[r, j].imshow(im); ax[r, j].plot(P[i][1], P[i][0], 'w+', ms=12); ax[r, j].plot(Q[i][1], Q[i][0], 'yx', ms=10)
        ax[r, j].set_title(f'{arm} t={t[i]:.0f} (+ starved daughter, x sister)', fontsize=7); ax[r, j].axis('off')
    R = d['R']; ax[r, 6].plot(R[:, 0], R[:, 1], 'r', label='starved daughter (tracked)'); ax[r, 6].plot(R[:, 0], R[:, 2], 'b', label='sister (tracked)'); ax[r, 6].legend(fontsize=7); ax[r, 6].set_title(arm)
plt.tight_layout(); plt.savefig(f'{pre}.png', dpi=60)
