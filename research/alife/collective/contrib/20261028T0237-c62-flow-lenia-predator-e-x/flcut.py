"""c62: per-predator consumption-off arm for the Flow-Lenia digestion ecology.
usage: WORLD_P=... flcut.py SEED N T0 TARM OUT.json
Runs to T0, picks up to 4 predator bodies (smoothed B > 0.2, area >= 20, >= 30 px apart), then two arms from that state:
  fed  : unchanged
  qcut : the digestion-product yield k_qy is 0 in a disk (body radius + 8 px) that follows each target (re-centred every
         2 t); eating (k_dig) is unchanged, so prey matter is still digested there. Other predators are untouched.
Targets are followed by overlap (dilated 3 px) every 2 t; a target that splits is followed by its larger part. A target is
dead when nothing overlaps it or when the peak of its smoothed predator matter falls below PEAK (default 0.6; a living body
peaks at ~1.5-2.5, a dissolving one spreads as a film below 0.4)."""
import sys, os, json, copy
sys.path.insert(0, '/home/user/physim/research/alife'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy import ndimage
import world as w
seed, N, T0, TA, out = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
FR = os.environ.get('FRAMES', ''); PEAK = float(os.environ.get('PEAK', 0.6)); dt = w.CFG['dt']; ST = np.ones((3, 3), bool)
def lab(x):
    big = np.tile(x, (3, 3)); L, n = ndimage.label(big, ST); L = L[N:2 * N, N:2 * N]
    ids, inv = np.unique(L, return_inverse=True); L = inv.reshape(L.shape)
    if ids[0] != 0: L = L + 1
    a = np.bincount(L.ravel()); small = np.where(a < 8)[0]; small = small[small > 0]
    L[np.isin(L, small)] = 0; ids, inv = np.unique(L, return_inverse=True); return inv.reshape(L.shape)
def dil(m, k):
    for _ in range(k): m = m | np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1)
    return m
def cen(m):
    ys, xs = np.nonzero(m)
    return (float(np.angle(np.exp(2j * np.pi * ys / N).mean()) * N / (2 * np.pi) % N), float(np.angle(np.exp(2j * np.pi * xs / N).mean()) * N / (2 * np.pi) % N))
yy, xx = np.mgrid[0:N, 0:N]
def disk(c, r):
    dy = (yy - c[0] + N / 2) % N - N / 2; dx = (xx - c[1] + N / 2) % N - N / 2; return dy * dy + dx * dx <= r * r
def sm(s, k): return ndimage.gaussian_filter(s[k].sum(0), 1.5, mode='wrap')
s = w.init(seed, (N, N))
for i in range(int(round(T0 / dt))): s = w.step(s)
L = lab(sm(s, 'B') > 0.2); La = lab(sm(s, 'A') > 0.2)
cands = []
for j in range(1, L.max() + 1):
    m = L == j
    if m.sum() >= 20: cands.append((m, cen(m), int(m.sum()), not bool((dil(La > 0, 2) & m).any())))
tg = []
for m, c, a, fr in sorted(cands, key=lambda x: -x[2]):
    if all(np.hypot((c[0] - t[1][0] + N / 2) % N - N / 2, (c[1] - t[1][1] + N / 2) % N - N / 2) > 30 for t in tg): tg.append((m, c, a, fr))
    if len(tg) == 4: break
state = copy.deepcopy(s); res = {}
for arm in ['fed', 'qcut']:
    s = copy.deepcopy(state); w.CFG['k_qy'] = float(json.loads(os.environ.get('WORLD_P', '{}')).get('k_qy', 1.0)); kq0 = w.CFG['k_qy']
    frs = []; masks = [t[0].copy() for t in tg]; cs = [t[1] for t in tg]; R = [np.sqrt(t[2] / np.pi) + 8 for t in tg]; alive = [True] * len(tg); rows = []
    for i in range(int(round(TA / dt)) + 1):
        if i % int(round(2 / dt)) == 0:
            SB = sm(s, 'B'); L = lab(SB > 0.2); row = dict(t=round(i * dt, 1), tg=[])
            for k in range(len(tg)):
                if alive[k]:
                    ov = L[dil(masks[k], 3)]; ov = ov[ov > 0]
                    if ov.size == 0: alive[k] = False; masks[k] = np.zeros((N, N), bool)
                    else:
                        masks[k] = L == np.bincount(ov).argmax(); cs[k] = cen(masks[k])
                        if SB[masks[k]].max() < PEAK: alive[k] = False
                row['tg'].append(dict(alive=alive[k], area=int(masks[k].sum()), peak=float(SB[masks[k]].max()) if masks[k].any() else 0.0, q=float(s['q'][masks[k]].max()) if masks[k].any() else 0.0))
            row['peak_raw'] = [float(s['B'].sum(0)[masks[k]].max()) if masks[k].any() else 0.0 for k in range(len(tg))]
            rows.append(row)
            if FR and i % int(round(20 / dt)) == 0: frs.append(np.stack([s['A'].sum(0), s['B'].sum(0)]))
            if arm == 'qcut':
                km = np.zeros((N, N), bool)
                for k in range(len(tg)):
                    if alive[k]: km |= disk(cs[k], R[k])
                w.CFG['k_qy'] = np.where(km, 0.0, kq0)
        s = w.step(s)
    res[arm] = rows
    if FR: np.savez_compressed(FR + f'_{arm}.npz', f=np.array(frs, np.float16))
w.CFG['k_qy'] = kq0
summ = {arm: [next((r['t'] for r in rows if not r['tg'][k]['alive']), None) for k in range(len(tg))] for arm, rows in res.items()}
json.dump(dict(seed=seed, T0=T0, targets=[dict(c=t[1], area=t[2], free=t[3]) for t in tg], death_t=summ, rows=res), open(out, 'w'))
print(json.dumps(dict(targets=[dict(c=[round(x) for x in t[1]], area=t[2], free=t[3]) for t in tg], death_t=summ)))
