"""c62: per-prey E arms on c52's world (the world of 20261027T1100-c56-prey-ixde-claim).
usage: preyarms.py SEED OUTDIR   (spins 128^2 to t=6000 once, then runs arms from that state for 2000 t)
Targets: 3 prey bodies of median-ish area (30-80 px), >= 35 px apart. Arms:
  fed     : unchanged
  fcut    : fuel regrowth kF=0 in a disk of radius R (body radius + 6 px) around the target, from t0 (c56's lcut)
  kc0     : catalysis rate kc=0 in a disk following the target (re-centred every 50 t), fuel supply kept (the L4c
            consumption-off arm: the fuel stays, the body cannot consume it or make its product)
Each arm cuts all 3 targets at once (they are far apart). Target tracked by overlap with c_a > 0.5."""
import sys, os, json, time
sys.path.insert(0, '/home/user/physim/research/alife')
WD = '/home/user/physim/research/alife/collective/contrib/20261027T0325-c52-digestion-ecology-claim'
import importlib.util
spec = importlib.util.spec_from_file_location('w', WD + '/world.py'); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
import numpy as np
from scipy import ndimage
seed, out = int(sys.argv[1]), sys.argv[2]; os.makedirs(out, exist_ok=True)
KEYS = ["pa", "pb", "p", "F", "w", "q"]; N = 128
stf = f'{out}/state_{seed}.npz'
if not os.path.exists(stf):
    s = w.init(seed, (N, N)); n = int(round(6000 / s['par']['dt']))
    for i in range(n): s = w.step(s)
    np.savez(stf, t=s['t'], **{k: s[k] for k in KEYS})

def pdist(cy, cx):
    yy, xx = np.mgrid[0:N, 0:N]; dy = (yy - cy + N / 2) % N - N / 2; dx = (xx - cx + N / 2) % N - N / 2
    return np.sqrt(dy * dy + dx * dx)

def label(x):
    big = np.tile(x > 0.5, (3, 3)); L, n = ndimage.label(big); L = L[N:2 * N, N:2 * N]
    ids = np.unique(L[L > 0]); return L, ids

def cent(m):
    ys, xs = np.nonzero(m)
    return (float(np.angle(np.exp(2j * np.pi * ys / N).mean()) * N / (2 * np.pi) % N), float(np.angle(np.exp(2j * np.pi * xs / N).mean()) * N / (2 * np.pi) % N))

def load():
    s = w.init(seed, (N, N)); d = np.load(stf)
    for k in KEYS: s[k] = d[k].copy()
    s['t'] = float(d['t']); s['par'] = dict(s['par']); return s

s = load(); F = w.fields(s); L, ids = label(F[0])
cand = []
for i in ids:
    m = L == i; a = int(m.sum())
    if 30 <= a <= 80: cand.append((abs(a - 50), i, a, cent(m)))
cand.sort(); tg = []
for _, i, a, c in cand:
    if all(pdist(*c)[int(round(t['c'][0])) % N, int(round(t['c'][1])) % N] > 35 for t in tg): tg.append(dict(id=int(i), area=a, c=c))
    if len(tg) == 3: break
res = {}
for arm in ['fed', 'fcut', 'kc0']:
    s = load(); dt = s['par']['dt']; t0 = s['t']
    kF0 = s['par']['kF']; kc0 = s['par']['kc']
    F = w.fields(s); L, _ = label(F[0]); masks = [L == t['id'] for t in tg]; alive = [True] * 3
    cen = [t['c'] for t in tg]; R = [float(np.sqrt(t['area'] / np.pi)) + 6 for t in tg]
    if arm == 'fcut':
        cutm = np.zeros((N, N), bool)
        for c, r in zip(cen, R): cutm |= pdist(*c) <= r
        s['par']['kF'] = np.where(cutm, 0.0, kF0)
    rows = []; frames = []
    for i in range(int(2000 / dt) + 1):
        if i % int(50 / dt) == 0:
            F = w.fields(s); L, _ = label(F[0]); Lb, _ = label(F[1]); row = dict(t=round(s['t'] - t0), tg=[])
            for k in range(3):
                if alive[k]:
                    ov = L[masks[k]]; ov = ov[ov > 0]
                    if ov.size == 0: alive[k] = False; masks[k] = np.zeros((N, N), bool)
                    else:
                        lab = np.bincount(ov).argmax(); masks[k] = L == lab; cen[k] = cent(masks[k])
                m = masks[k]
                dm = ndimage.binary_dilation(m, iterations=2) if m.any() else m
                row['tg'].append(dict(alive=alive[k], area=int(m.sum()), F_in=float(F[2][m].mean()) if m.any() else None,
                                      p_in=float(F[3][m].mean()) if m.any() else None, pred_touch=bool((Lb[dm] > 0).any()) if m.any() else False))
            rows.append(row)
            if arm == 'kc0':
                km = np.zeros((N, N), bool)
                for k in range(3): km |= pdist(*cen[k]) <= R[k] + (0 if alive[k] else 0)
                s['par']['kc'] = np.where(km, 0.0, kc0)
        if i % int(250 / dt) == 0: frames.append(np.asarray(w.fields(s)[[0, 1, 2]], np.float32))
        s = w.step(s)
    res[arm] = rows
    np.savez_compressed(f'{out}/frames_{arm}_{seed}.npz', f=np.array(frames))
json.dump(dict(seed=seed, targets=tg, arms=res), open(f'{out}/preyarms_{seed}.json', 'w'))
for arm in res:
    print(arm, [[(r['t'], r['tg'][k]['area']) for r in res[arm][::8]] for k in range(3)])
