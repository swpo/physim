"""quick driver: python drive.py world.py out_prefix --size N --T T --seed s
records prey/predator droplet counts (channel>0.5) every 'every' time units and a snapshot strip."""
import sys, json, argparse, importlib.util, time
sys.path.insert(0, '/home/user/physim/research/alife')
import numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ap = argparse.ArgumentParser(); ap.add_argument('world'); ap.add_argument('out')
ap.add_argument('--size', type=int, default=128); ap.add_argument('--T', type=float, default=6000)
ap.add_argument('--seed', type=int, default=0); ap.add_argument('--every', type=float, default=100)
ap.add_argument('--snaps', type=int, default=12)
a = ap.parse_args()
spec = importlib.util.spec_from_file_location('w', a.world); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
dt = w.P['dt']; s = w.init(a.seed, (a.size, a.size))
nsteps = int(a.T / dt); ev = max(1, int(a.every / dt))
snap_t = set(int(x) for x in np.linspace(0, nsteps, a.snaps).astype(int))
rec = []; snaps = []; t0 = time.time()
for i in range(nsteps + 1):
    if i % ev == 0 or i in snap_t:
        F = w.fields(s)
        if i % ev == 0:
            na = ndimage.label(F[0] > 0.4)[1]; nb = ndimage.label(F[3] > 0.3)[1]
            rec.append([i * dt, na, nb, float(F[0].mean()), float(F[3].mean()), float(F[2].mean()), float(F[3].max()), float(F[0].max()), 0.0])
            if not np.isfinite(F).all(): print('NaN'); break
        if i in snap_t:
            snaps.append((i * dt, F.copy()))
    if i < nsteps: s = w.step(s)
R = np.array(rec)
json.dump(dict(cols=['t', 'n_prey', 'n_pred', 'm_prey', 'm_pred', 'u', 'w', 'eat_droplet', 'eat_dilute'], rows=R.tolist(), P=w.P, size=a.size, seed=a.seed, wall=time.time() - t0), open(a.out + '.json', 'w'))
fig = plt.figure(figsize=(2 * len(snaps), 4.6))
for k, (t, F) in enumerate(snaps):
    ax = fig.add_subplot(2, len(snaps), k + 1)
    rgb = np.zeros(F.shape[1:] + (3,))
    rgb[..., 0] = np.clip(F[3], 0, 1)
    rgb[..., 1] = np.clip(F[0], 0, 1) * 0.9
    rgb[..., 2] = np.clip(F[0], 0, 1) * 0.6 + 0.4 * np.clip(F[2], 0, 1)
    ax.imshow(np.clip(rgb, 0, 1)); ax.set_title(f't={t:.0f}', fontsize=7); ax.axis('off')
ax = fig.add_subplot(2, 1, 2)
ax.plot(R[:, 0], R[:, 1], label='prey droplets'); ax.plot(R[:, 0], R[:, 2], label='predator droplets')
ax2 = ax.twinx(); ax2.plot(R[:, 0], R[:, 4], 'r:', lw=0.8, label='pred mass'); ax2.set_ylabel('mean pred c', fontsize=7)
ax.legend(fontsize=7, loc='upper right'); ax.set_xlabel('t')
ax.set_title(a.out.split('/')[-1] + ' ' + json.dumps({k: v for k, v in w.P.items() if k in json.loads(__import__('os').environ.get('WORLD_P', '{}'))}), fontsize=7)
plt.tight_layout(); plt.savefig(a.out + '.png', dpi=70)
fr = R[-1, 6]
print(a.out, 'final qmax %.2f emax %.2f' % (fr, R[-1, 7]), 'wall %.0fs' % (time.time() - t0), 'last pred>0 t=', R[R[:, 2] > 0, 0].max() if (R[:, 2] > 0).any() else -1, 'final', R[-1, 1:3])
