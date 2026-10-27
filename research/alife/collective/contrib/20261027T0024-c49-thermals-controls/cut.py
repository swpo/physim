"""python cut.py seed : run world.py to t=400, pick the cap (T>0.25 component, >= 6 px) with the widest horizontal clearance
to the other caps, then branch: fed twin vs a local cut (fuel held at 0 in a vertical strip spanning the target's width
+ 4 px). Follow both to t=480 and count caps whose centroid lies inside / outside the strip. Writes cut_s<seed>.png/.json."""
import sys, os, json, copy, importlib, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy import ndimage
sys.path.insert(0, '/home/user/physim/research/alife'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import world as w
seed = int(sys.argv[1]); N = 128; dt = w.P['dt']; t0, t1 = 400.0, 480.0

def caps(T):
    l, k = ndimage.label(T > 0.25, structure=np.ones((3, 3)))
    out = []
    for i in range(1, k + 1):
        yy, xx = np.nonzero(l == i)
        if len(yy) < 6: continue
        # periodic-safe x extent and centroid
        ang = 2 * np.pi * xx / N; cx = (np.angle(np.exp(1j * ang).mean()) % (2 * np.pi)) * N / (2 * np.pi)
        dxs = (xx - cx + N / 2) % N - N / 2
        angy = 2 * np.pi * yy / N; cy = (np.angle(np.exp(1j * angy).mean()) % (2 * np.pi)) * N / (2 * np.pi)
        out.append({'cx': cx, 'cy': cy, 'x0': dxs.min(), 'x1': dxs.max(), 'area': len(yy)})
    return out

s = w.init(seed, (N, N))
for i in range(int(round(t0 / dt))): s = w.step(s)
C = caps(s['T'])
def clearance(c):
    lo, hi = c['cx'] + c['x0'], c['cx'] + c['x1']
    g = []
    for o in C:
        if o is c: continue
        olo, ohi = o['cx'] + o['x0'], o['cx'] + o['x1']
        d = min(abs((olo - hi + N / 2) % N - N / 2), abs((lo - ohi + N / 2) % N - N / 2))
        g.append(d)
    return min(g) if g else N
tgt = max(C, key=clearance); width = tgt['x1'] - tgt['x0'] + 4; cxs = tgt['cx'] + (tgt['x0'] + tgt['x1']) / 2
print('seed', seed, 'caps at t=400', len(C), 'target cx %.1f cy %.1f width %.1f clearance %.1f' % (cxs, tgt['cy'], width, clearance(tgt)))
res = {}; snaps = {}
for arm in ('fed', 'cut'):
    st = copy.deepcopy(s)
    if arm == 'cut':
        st['par'] = dict(st['par'], cut_t=t0, cut_x=cxs, cut_w=width)
        xx = np.broadcast_to(np.arange(N)[None, :], (N, N)); st['strip'] = np.abs((xx - cxs + N / 2) % N - N / 2) < width / 2
    rows = []; snaps[arm] = []
    for i in range(int(round((t1 - t0) / dt)) + 1):
        if i % int(round(2 / dt)) == 0:
            cc = caps(st['T']); ins = [c for c in cc if abs((c['cx'] - cxs + N / 2) % N - N / 2) < width / 2]
            rows.append((t0 + i * dt, len(ins), len(cc) - len(ins)))
        if i % int(round(16 / dt)) == 0: snaps[arm].append((t0 + i * dt, st['T'].copy(), st['Y'].copy()))
        st = w.step(st)
    res[arm] = rows
json.dump({'seed': seed, 'target': {'cx': cxs, 'cy': tgt['cy'], 'width': width}, 'rows': res}, open(f'cut_s{seed}.json', 'w'))
fig = plt.figure(figsize=(14, 6))
for r, arm in enumerate(('fed', 'cut')):
    for j, (t, T, Y) in enumerate(snaps[arm][:6]):
        ax = fig.add_subplot(3, 6, r * 6 + j + 1)
        rgb = np.stack([np.clip(T / 0.7, 0, 1), 0.45 * np.clip(Y, 0, 1), 0.25 * np.clip(Y, 0, 1)], -1)
        ax.imshow(rgb, origin='lower'); ax.axvline(cxs - width / 2, color='w', lw=0.5); ax.axvline(cxs + width / 2, color='w', lw=0.5)
        ax.set_title(f'{arm} t={t:.0f}', fontsize=8); ax.axis('off')
ax = fig.add_subplot(3, 1, 3)
for arm, c in (('fed', 'r'), ('cut', 'k')):
    R = np.array(res[arm]); ax.plot(R[:, 0], R[:, 1], c, label=f'{arm}: caps inside strip'); ax.plot(R[:, 0], R[:, 2] / max(R[0, 2], 1), c + ':', label=f'{arm}: caps outside / start')
ax.legend(fontsize=7, ncol=2); ax.set_xlabel('t')
plt.tight_layout(); plt.savefig(f'cut_s{seed}.png', dpi=70)
for arm in res: print(arm, 'inside/outside at t=400,410,420,440,480:', [(r[1], r[2]) for r in res[arm] if r[0] in (400, 410, 420, 440, 480)])
