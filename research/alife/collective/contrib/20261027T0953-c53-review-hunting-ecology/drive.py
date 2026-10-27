"""python drive.py world.py out_prefix --size N --T T --seed s : counts prey (e>0.5) and predator (c_b>0.5) bodies, snapshots."""
import sys, json, argparse, importlib.util, time, os
sys.path.insert(0, '/home/user/physim/research/alife')
import numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ap = argparse.ArgumentParser(); ap.add_argument('world'); ap.add_argument('out')
ap.add_argument('--size', type=int, default=128); ap.add_argument('--T', type=float, default=6000)
ap.add_argument('--seed', type=int, default=0); ap.add_argument('--every', type=float, default=50)
ap.add_argument('--snaps', type=int, default=16); ap.add_argument('--s0', type=float, default=0); ap.add_argument('--s1', type=float, default=-1)
a = ap.parse_args()
spec = importlib.util.spec_from_file_location('w', a.world); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
dt = w.P['dt']; s = w.init(a.seed, (a.size, a.size))
nsteps = int(round(a.T / dt)); ev = max(1, int(round(a.every / dt)))
snap_t = set(int(x) for x in np.linspace(int(a.s0/dt), nsteps if a.s1 < 0 else int(a.s1/dt), a.snaps).astype(int))
rec = []; snaps = []; t0 = time.time(); prevL = [None, None]; nsplit = [0, 0]
def splits(k, x, th=0.3, amin=4):
    l, n = ndimage.label(x > th)
    if n:
        ar = ndimage.sum(np.ones_like(x), l, range(1, n + 1)); small = np.where(ar < amin)[0] + 1; l[np.isin(l, small)] = 0
    pl = prevL[k]; prevL[k] = l
    if pl is None: return
    for c in np.unique(pl[pl > 0]):
        kids = np.unique(l[(pl == c) & (l > 0)])
        if len(kids) >= 2: nsplit[k] += len(kids) - 1
def lab(x, th, amin=4):
    l, n = ndimage.label(x > th)
    if n == 0: return 0
    ar = ndimage.sum(np.ones_like(x), l, range(1, n + 1)); return int((ar >= amin).sum())
for i in range(nsteps + 1):
    if i % ev == 0 or i in snap_t:
        F = w.fields(s)
        if i % ev == 0:
            rec.append([i * dt, lab(F[0], 0.5), lab(F[1], 0.5), float(F[0].mean()), float(F[1].mean()), float(F[2].mean()), float(F[3].mean()), float(F[0].max()), float(F[1].max()), float(np.median(F[0]))])
            splits(0, F[0]); splits(1, F[1])
            if not np.isfinite(F).all(): print('NaN'); break
        if i in snap_t: snaps.append((i * dt, F.copy()))
    if i < nsteps: s = w.step(s)
R = np.array(rec)
json.dump(dict(cols=['t', 'n_prey', 'n_pred', 'm_e', 'm_cb', 'F', 'w', 'emax', 'cbmax', 'e_med'], rows=R.tolist(), splits=nsplit, P=w.P, size=a.size, seed=a.seed, wall=time.time() - t0), open(a.out + '.json', 'w'))
fig = plt.figure(figsize=(1.6 * len(snaps), 4.2))
for k, (t, F) in enumerate(snaps):
    ax = fig.add_subplot(2, len(snaps), k + 1)
    rgb = np.zeros(F.shape[1:] + (3,))
    rgb[..., 0] = np.clip(F[1], 0, 1)
    rgb[..., 1] = np.clip(F[0], 0, 1)
    rgb[..., 2] = 0.35 * np.clip(F[2], 0, 1)
    ax.imshow(np.clip(rgb, 0, 1)); ax.set_title(f't={t:.0f}', fontsize=7); ax.axis('off')
ax = fig.add_subplot(2, 1, 2)
ax.plot(R[:, 0], R[:, 1], 'g', label='prey bodies'); ax.plot(R[:, 0], R[:, 2], 'r', label='predator bodies')
ax2 = ax.twinx(); ax2.plot(R[:, 0], R[:, 4], 'r:', lw=0.8); ax2.plot(R[:, 0], R[:, 3], 'g:', lw=0.8); ax2.set_ylabel('mean e, c_b (dotted)', fontsize=7)
ax.legend(fontsize=7, loc='upper left'); ax.set_xlabel('t')
ax.set_title(a.out.split('/')[-1] + ' ' + os.environ.get('WORLD_P', ''), fontsize=7)
plt.tight_layout(); plt.savefig(a.out + '.png', dpi=70)
print(a.out, 'splits prey/pred', nsplit, "emed %.3f" % R[-1, 9], 'wall %.0fs' % (time.time() - t0), 'final prey/pred', R[-1, 1:3], 'max prey', R[:, 1].max(), 'max pred', R[:, 2].max(), 'cbmax %.2f emax %.2f' % (R[-1, 8], R[-1, 7]))
