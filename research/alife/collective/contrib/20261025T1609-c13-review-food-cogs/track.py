"""biography of the cut cog: crops (rolled to centre) from pre<sd> (noise to t=600), then cut run and fed twin."""
import sys, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sd = int(sys.argv[1]); c = np.load(f'cut_{sd}.npz'); cy, cx = float(c['cy']), float(c['cx'])
pre = np.load(f'pre{sd}_snaps.npz'); cut = np.load(f'cutrun{sd}_snaps.npz'); fed = np.load(f'fed{sd}_snaps.npz')
def crop(X):
    Y = np.roll(X.astype(np.float32), (int(96-cy), int(96-cx)), (1, 2))
    return np.stack([Y[1], Y[0], np.clip(Y[2]/1.5, 0, 1)], -1).clip(0, 1)[66:126, 66:126]
pick = lambda d, tt: int(np.argmin(abs(d['t']-tt)))
panels = [(pre, t, 'from noise') for t in (10, 40, 80, 120, 300, 600)] + [(cut, t, 'food cut') for t in (620, 640, 650, 660)] + [(fed, t, 'fed twin') for t in (660, 900)]
fig, ax = plt.subplots(2, 6, figsize=(15, 5.6))
for a, (d, tt, lab) in zip(ax.ravel(), panels):
    i = pick(d, tt); a.imshow(crop(d['X'][i])); a.set_title(f'seed {sd} {lab} t={d["t"][i]:.0f}', fontsize=8); a.axis('off')
fig.suptitle(f'one cog (seed {sd}, centre y={cy:.0f} x={cx:.0f}); R=A1 shell, G=A0 core, B=food F/1.5; 60x60 px crops', fontsize=9)
plt.tight_layout(); plt.savefig(f'track_seed{sd}.png', dpi=70)
