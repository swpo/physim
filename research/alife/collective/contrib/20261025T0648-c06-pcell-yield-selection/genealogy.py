"""Exact cell genealogy for pcell worlds, carried by particle identity.

Cells = 8-connected components of phi > 1/2 holding >= MINP particles. Every DT steps, a
cell j's parents are the earlier cells that hold >= FR of j's surviving particles (uids
present at both times). Splits (one parent, >= 2 children), merges (>= 2 parents), births
(cells created by a split), deaths (a cell with no child). A cell's kind = majority kind;
it is pure if >= 0.95 of its particles share the kind.

usage: python genealogy.py world.py seed T out.json [key=val ...]
"""
import sys, json
import numpy as np
from scipy import ndimage
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit.world import load_world

MINP, FR, DT = 20, 0.2, 50


def plabel(mask):
    """Connected components on the periodic torus (4-connectivity), labels 1..n."""
    lab, n = ndimage.label(mask)
    par = list(range(n + 1))
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for a, b in ((lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])):
        for u, v in zip(a, b):
            if u and v:
                ru, rv = f(u), f(v)
                if ru != rv:
                    par[ru] = rv
    roots = np.array([f(x) for x in range(n + 1)])
    uniq, inv = np.unique(roots, return_inverse=True)
    out = inv.reshape(-1)[lab]
    if uniq[0] != 0:
        out = out + 1
    return out, len(uniq) - 1


def cells_of(s):
    lab, n = plabel(s["phi"] > 0.5)
    H, W = lab.shape
    c = lab[s['py'].astype(int) % H, s['px'].astype(int) % W]
    out = []
    for i in range(1, n + 1):
        m = c == i
        if m.sum() < MINP:
            continue
        k = s['kind'][m]
        f1 = float((k == 1).mean())
        out.append(dict(uids=s['uid'][m], n=int(m.sum()), f1=f1,
                        area=int((lab == i).sum()),
                        cy=float(np.median(s['py'][m])), cx=float(np.median(s['px'][m]))))
    return out


def run(world, seed, T, kv):
    W = load_world(world)
    for k, v in kv.items():
        W.P[k] = float(v)
    s = W.init(seed, (128, 128))
    snaps = []
    for t in range(T + 1):
        if t % DT == 0 and t >= 500:
            snaps.append((t, cells_of(s)))
        s = W.step(s)
    return snaps, s


def link(snaps):
    """Assign persistent cell ids; return per-snapshot ids and the event list."""
    nid = 0
    ids = []
    cid = []
    for c in snaps[0][1]:
        cid.append(nid); nid += 1
    ids.append(cid)
    events = []  # (t, type, parents, children)
    parent_of = {}
    gen = {i: 0 for i in cid}
    kindinfo = {i: c['f1'] for i, c in zip(cid, snaps[0][1])}
    for a in range(1, len(snaps)):
        t0, C0 = snaps[a - 1]; t1, C1 = snaps[a]
        own = {}
        for i, c in enumerate(C0):
            for u in c['uids']:
                own[int(u)] = i
        # overlap matrix
        M = np.zeros((len(C0), len(C1)), int)
        for j, c in enumerate(C1):
            for u in c['uids']:
                i = own.get(int(u))
                if i is not None:
                    M[i, j] += 1
        par = [[i for i in range(len(C0)) if M[i, j] >= 3 and M[i, j] >= FR * max(1, M[:, j].sum())] for j in range(len(C1))]
        chi = [[j for j in range(len(C1)) if M[i, j] >= 3 and M[i, j] >= FR * max(1, M[i, :].sum())] for i in range(len(C0))]
        new = [None] * len(C1)
        for j in range(len(C1)):
            p = par[j]
            if len(p) == 1 and chi[p[0]] == [j]:
                new[j] = ids[a - 1][p[0]]  # continuation
        for i in range(len(C0)):
            if len(chi[i]) >= 2:
                kids = []
                for j in chi[i]:
                    if len(par[j]) == 1:
                        new[j] = nid; parent_of[nid] = ids[a - 1][i]
                        gen[nid] = gen[ids[a - 1][i]] + 1; nid += 1; kids.append(new[j])
                events.append((t1, 'split', [ids[a - 1][i]], kids))
            if len(chi[i]) == 0:
                events.append((t1, 'death', [ids[a - 1][i]], []))
        for j in range(len(C1)):
            if len(par[j]) >= 2:
                new[j] = nid; gen[nid] = max(gen[ids[a - 1][i]] for i in par[j]); nid += 1
                events.append((t1, 'merge', [ids[a - 1][i] for i in par[j]], [new[j]]))
            elif new[j] is None:
                new[j] = nid; gen[nid] = 0 if not par[j] else gen[ids[a - 1][par[j][0]]]; nid += 1
                if not par[j]:
                    events.append((t1, 'appear', [], [new[j]]))
        ids.append(new)
    return ids, events, gen, parent_of


def summarize(snaps, ids, events, gen, parent_of, K=10):
    """Persistent splits: both daughters exist >= K snapshots and do not merge back into each other."""
    life = {}
    for a, (t, C) in enumerate(snaps):
        for i, c in zip(ids[a], C):
            life.setdefault(i, []).append((t, c['f1'], c['n']))
    merged = {}
    for t, ty, p, ch in events:
        if ty == 'merge':
            for x in p:
                merged[x] = (t, ch[0], p)
    def ok(d):
        return len(life.get(d, [])) >= K
    psplits = []
    for t, ty, p, ch in events:
        if ty == 'split' and len(ch) >= 2:
            good = [d for d in ch if ok(d)]
            if len(good) >= 2:
                psplits.append((t, p[0], good))
    def kind(f):
        return 1 if f >= 0.95 else (0 if f <= 0.05 else -1)
    # per-kind divisions (parent pure) and offspring kinds
    pk = {0: 0, 1: 0, -1: 0}; offkind = 0; dk = {0: 0, 1: 0, -1: 0}
    for t, p, good in psplits:
        f = [x for x in life[p] if x[0] < t][-1][1]
        kp = kind(f); pk[kp] += 1
        for d in good:
            if kp >= 0 and kind(life[d][0][1]) != kp:
                offkind += 1
    for t, ty, p, ch in events:
        if ty == 'death':
            f = life[p[0]][-1][1]; dk[kind(f)] += 1
    # conversions: a pure cell that becomes pure of the other kind without a merge in between
    conv = 0
    for i, L in life.items():
        ks = [kind(f) for _, f, _ in L]
        pure = [k for k in ks if k >= 0]
        if len(set(pure)) > 1:
            conv += 1
    pg = {}
    for t, p, good in psplits:
        for d in good:
            pg[d] = pg.get(p, 0) + 1
    maxgen = max(pg.values()) if pg else 0
    nmerge = sum(1 for e in events if e[1] == 'merge')
    return dict(persistent_splits=len(psplits), max_generation_persistent=maxgen, merges=nmerge,
                deaths=sum(1 for e in events if e[1] == 'death'),
                splits_by_parent_kind={str(k): v for k, v in pk.items()}, deaths_by_kind={str(k): v for k, v in dk.items()},
                off_kind_daughters=offkind, conversions_of_pure_cells=conv,
                final_cells=len(snaps[-1][1]),
                final_pure={str(k): sum(1 for c in snaps[-1][1] if kind(c['f1']) == k) for k in (0, 1, -1)})


if __name__ == '__main__':
    world, seed, T, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    kv = dict(a.split('=') for a in sys.argv[5:])
    snaps, s = run(world, seed, T, kv)
    ids, events, gen, parent_of = link(snaps)
    summ = summarize(snaps, ids, events, gen, parent_of)
    summ.update(world=world, seed=seed, T=T, params=kv,
                particle_births=s['births'].tolist(), particle_deaths=s['deaths'].tolist(), flips=s['flips'])
    series = [dict(t=t, n=len(C), f1=[round(c['f1'], 3) for c in C], np=[c['n'] for c in C], id=ids[a]) for a, (t, C) in enumerate(snaps)]
    json.dump(dict(summary=summ, events=events, series=series), open(out, 'w'))
    print(json.dumps(summ))
