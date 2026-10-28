"""c62: predator individuals in the Flow-Lenia digestion ecology, tracked every EV time units during the run.
usage: WORLD_P=... fltrack.py SEED N T OUT.json [EV=2]
Bodies: periodic components of predator matter B_sum > 0.3 (prey A_sum > 0.3), area >= 8 px.
Linking: each body's parent is the previous-frame body with which it overlaps most after dilating the previous mask by
D px (D = 3, gliders move <= ~2 px per EV); a parent with >= 2 children each >= 25% of its area is a SPLIT (children
start new tracks); a body with >= 2 parents each >= 25% of its area is a MERGE; else the largest child continues the track.
Free: no prey pixel within 2 px. Hop: within one track, a contact, a free spell of >= 10 t, and a new contact whose prey
contact point is > 10 px from the last one. Clean split: both daughters' tracks last >= 100 t without merging.
Also records per-frame counts (predators, prey, free predators) and digestion total."""
import sys, os, json
sys.path.insert(0, '/home/user/physim/research/alife'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy import ndimage
import world as w
seed, N, T, out = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
EV = float(sys.argv[5]) if len(sys.argv) > 5 else 2.0
s = w.init(seed, (N, N)); dt = w.CFG['dt']; ev = int(round(EV / dt)); nst = int(round(T / dt))
ST = np.ones((3, 3), bool)

def lab(x):
    big = np.tile(x, (3, 3)); L, n = ndimage.label(big, ST); L = L[N:2 * N, N:2 * N]
    ids, inv = np.unique(L, return_inverse=True); L = inv.reshape(L.shape)
    if ids[0] != 0: L = L + 1
    a = np.bincount(L.ravel()); small = np.where(a < 8)[0]; small = small[small > 0]
    L[np.isin(L, small)] = 0; ids, inv = np.unique(L, return_inverse=True); L = inv.reshape(L.shape)
    return L, int(L.max())

def dil(m, k):
    for _ in range(k): m = m | np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1)
    return m

def cen(m):
    ys, xs = np.nonzero(m)
    return (float(np.angle(np.exp(2j * np.pi * ys / N).mean()) * N / (2 * np.pi) % N), float(np.angle(np.exp(2j * np.pi * xs / N).mean()) * N / (2 * np.pi) % N))

def pd(a, b):
    dy = (a[0] - b[0] + N / 2) % N - N / 2; dx = (a[1] - b[1] + N / 2) % N - N / 2
    return float(np.hypot(dy, dx))

tracks = []; prev = None; prevL = None; series = []; events = []
for i in range(nst + 1):
    if i % ev == 0 and s['t'] * dt >= w.CFG['t_pred']:
        t = round(s['t'] * dt, 2)
        A = s['A'].sum(0); B = s['B'].sum(0)
        La, na = lab(A > 0.3); Lb, nb = lab(B > 0.3)
        near = dil(La > 0, 2)
        cur = []
        for j in range(1, nb + 1):
            m = Lb == j; free = not bool((near & m).any())
            cp = cen(m & near) if not free else None
            cur.append(dict(m=m, area=int(m.sum()), free=free, cp=cp, c=cen(m)))
        # link
        if prev is not None:
            pdl = [dil(p['m'], 3) for p in prev]
            ov = np.zeros((len(prev), len(cur)))
            for a_, pm in enumerate(pdl):
                for b_, c in enumerate(cur): ov[a_, b_] = (pm & c['m']).sum()
            parents = [[a_ for a_ in range(len(prev)) if ov[a_, b_] >= 0.25 * cur[b_]['area']] for b_ in range(len(cur))]
            children = [[b_ for b_ in range(len(cur)) if ov[a_, b_] >= 0.25 * min(prev[a_]['area'], cur[b_]['area']) and ov[a_, b_] > 0] for a_ in range(len(prev))]
            for b_, c in enumerate(cur):
                c['tid'] = None
            for a_, p in enumerate(prev):
                kids = [b_ for b_ in children[a_] if len(parents[b_]) <= 1]
                tr = tracks[p['tid']]
                if len(kids) >= 2 and sum(cur[b_]['area'] >= 0.25 * p['area'] for b_ in kids) >= 2:
                    tr['end'] = t; tr['fate'] = 'split'; events.append(dict(kind='split', t=t, parent=p['tid'], free=p['free'], kids=[]))
                    for b_ in kids:
                        tracks.append(dict(start=t, end=t, birth='split', parent=p['tid'], fate='alive', life_free=0, frames=0, hops=0, last_cp=None, free_since=None, contacts=0))
                        cur[b_]['tid'] = len(tracks) - 1; events[-1]['kids'].append(len(tracks) - 1)
                elif len(kids) >= 1:
                    b_ = max(kids, key=lambda b: ov[a_, b]); cur[b_]['tid'] = p['tid']
                elif not children[a_]:
                    tr['end'] = t; tr['fate'] = 'dissolved'
            for b_, c in enumerate(cur):
                if len(parents[b_]) >= 2:
                    for a_ in parents[b_]:
                        if tracks[prev[a_]['tid']]['fate'] == 'alive': tracks[prev[a_]['tid']]['fate'] = 'merge'; tracks[prev[a_]['tid']]['end'] = t
                    tracks.append(dict(start=t, end=t, birth='merge', parent=None, fate='alive', life_free=0, frames=0, hops=0, last_cp=None, free_since=None, contacts=0)); c['tid'] = len(tracks) - 1
            for a_, p in enumerate(prev):
                tr = tracks[p['tid']]
                if tr['fate'] == 'alive' and not any(c.get('tid') == p['tid'] for c in cur):
                    tr['fate'] = 'absorbed'; tr['end'] = t
        for c in cur:
            if c.get('tid') is None:
                tracks.append(dict(start=t, end=t, birth='nucleation' if prev is not None else 'initial', parent=None, fate='alive', life_free=0, frames=0, hops=0, last_cp=None, free_since=None, contacts=0)); c['tid'] = len(tracks) - 1
            tr = tracks[c['tid']]; tr['end'] = t; tr['frames'] += 1; tr['life_free'] += int(c['free'])
            if c['free']:
                if tr['free_since'] is None: tr['free_since'] = t
            else:
                if tr['free_since'] is not None and tr['last_cp'] is not None and t - tr['free_since'] >= 10 and pd(c['cp'], tr['last_cp']) > 10: tr['hops'] += 1
                tr['free_since'] = None; tr['last_cp'] = c['cp']; tr['contacts'] += 1
        series.append(dict(t=t, n_pred=nb, n_prey=na, n_free=sum(c['free'] for c in cur), q=float(s['q'].sum()), Bmass=float(B.sum())))
        prev = cur
    if i < nst: s = w.step(s)
# summaries
for tr in tracks: tr.pop('last_cp', None)
life = [tr['end'] - tr['start'] for tr in tracks]
splits = [e for e in events if e['kind'] == 'split']
def clean(k):
    tr = tracks[k]; return (tr['end'] - tr['start'] >= 100) or (tr['fate'] == 'split' and tr['end'] - tr['start'] >= 25)
cl = [e for e in splits if sum(clean(k) for k in e['kids']) >= 2]
gen = {}
for k, tr in enumerate(tracks):
    gen[k] = 0 if tr['parent'] is None else gen[tr['parent']] + 1 if tr['birth'] == 'split' else 0
summ = dict(seed=seed, N=N, T=T, n_tracks=len(tracks), life_median=float(np.median(life)) if life else 0,
            life_ge100=int(sum(l >= 100 for l in life)), life_ge300=int(sum(l >= 300 for l in life)),
            births={b: sum(tr['birth'] == b for tr in tracks) for b in ['initial', 'nucleation', 'split', 'merge']},
            fates={f: sum(tr['fate'] == f for tr in tracks) for f in ['alive', 'dissolved', 'split', 'merge', 'absorbed']},
            splits=len(splits), clean_splits=len(cl), clean_split_parent_free=sum(e['free'] for e in cl), max_gen=max(gen.values()) if gen else 0,
            hops=int(sum(tr['hops'] for tr in tracks)), tracks_with_hop=int(sum(tr['hops'] > 0 for tr in tracks)),
            free_frac=float(np.sum([r['n_free'] for r in series]) / max(1, np.sum([r['n_pred'] for r in series]))),
            n_pred_mean=float(np.mean([r['n_pred'] for r in series])), n_prey_mean=float(np.mean([r['n_prey'] for r in series])))
json.dump(dict(summary=summ, series=series, tracks=tracks, events=events), open(out, 'w'))
print(json.dumps(summ))
