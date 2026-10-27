"""c56: are the predators free individuals?  python freepred.py frames.npz out.json [dt_per_frame] [t_start]
Per frame: predator bodies (c_b > 0.5, area >= 4) and their gap to the nearest prey body (c_a > 0.5, area >= 4), measured
as the minimum Euclidean distance transform of the prey-free region over the predator's pixels (0 = overlapping or
touching). A predator is FREE when its gap is > 2 px.
Tracks: predator bodies linked frame to frame by largest overlap (one parent, one child; splits and merges end tracks).
Per track: fraction of frames free; detach events (contact -> free); 'hops' (a free spell bounded by contacts whose
prey contact points are > 10 px apart).
Divisions (splits3.py rule, predator channel, min area A=10): the parent's gap at t and both daughters' gaps at t+1 and
t+5 (any daughter free at t+5 = the daughters separated from prey).
"""
import sys, json, numpy as np
from scipy import ndimage
R = np.load(sys.argv[1])['render'].astype(np.float32)
import os
if os.environ.get('SWAP'): R = R[:, [1, 0]]   # focal kind = prey
DTF = float(sys.argv[3]) if len(sys.argv) > 3 else 100.0
T0 = float(sys.argv[4]) if len(sys.argv) > 4 else 2500.0
T = len(R); A = 10; H, W = R.shape[-2:]


def labels(x, amin):
    l, n = ndimage.label(x > 0.5, structure=np.ones((3, 3)))
    if n:
        ar = np.bincount(l.ravel()); l[ar[l] < amin] = 0
    return l


def tile_edt(prey):
    # periodic distance to prey: transform a 3x3 tiling, take the centre
    big = np.tile(~prey, (3, 3))
    d = ndimage.distance_transform_edt(big)
    return d[H:2 * H, W:2 * W]


LB = [labels(f[1], 4) for f in R]
LA = [labels(f[0], 4) for f in R]
DP = [tile_edt(la > 0) for la in LA]


def gaps(t):
    l = LB[t]; ids = np.unique(l[l > 0])
    if not len(ids): return {}
    g = ndimage.minimum(DP[t], l, ids)
    return {int(i): float(v) for i, v in zip(ids, g)}


G = [gaps(t) for t in range(T)]
t_start = int(round(T0 / DTF))
nf = [sum(v > 2 for v in G[t].values()) for t in range(t_start, T)]
nt = [len(G[t]) for t in range(t_start, T)]
# tracks
tracks = []; cur = {}
for t in range(t_start, T):
    l = LB[t]; nxt = {}
    if t > t_start:
        lp = LB[t - 1]
        for i in G[t - 1]:
            ov = l[lp == i]; ov = ov[ov > 0]
            if not ov.size: continue
            kids = np.unique(ov)
            if len(kids) != 1: continue
            j = int(kids[0])
            back = lp[l == j]; back = np.unique(back[back > 0])
            if len(back) != 1: continue
            if i in cur: nxt[j] = cur[i]
    for j in G[t]:
        if j not in nxt:
            nxt[j] = len(tracks); tracks.append([])
        com = ndimage.center_of_mass(LB[t] == j)
        tracks[nxt[j]].append((t, G[t][j], com, j))
    cur = nxt
L = [tr for tr in tracks if len(tr) >= 10]
ffree = [np.mean([x[1] > 2 for x in tr]) for tr in L]
detach = 0; hops = 0; hop_tr = []
for k, tr in enumerate(L):
    st = [x[1] > 2 for x in tr]
    for a in range(1, len(st)):
        if st[a] and not st[a - 1]: detach += 1
    # hops: contact at a, free a+1..b-1, contact at b, with centre moved > 10 px
    a = None
    for b in range(len(st)):
        if not st[b]:
            if a is not None and b - a > 1:
                (y0, x0), (y1, x1) = tr[a][2], tr[b][2]
                d = np.hypot((y1 - y0 + H / 2) % H - H / 2, (x1 - x0 + W / 2) % W - W / 2)
                if d > 10: hops += 1; hop_tr.append((k, tr[a][0], tr[b][0], float(d)))
            a = b
# free spells: length and fate (reattach within the track, or the track ends while free)
spells = []; area_free = []; area_touch = []
for tr in L:
    st = [x[1] > 2 for x in tr]; a = None
    for b in range(len(st) + 1):
        if b < len(st) and st[b]:
            if a is None: a = b
        elif a is not None:
            fate = 'reattach' if b < len(st) else ('end' if tr[-1][0] < T - 1 else 'alive_at_end')
            if a > 0 or True: spells.append((b - a, fate, a == 0))
            a = None
sp_len = [x[0] for x in spells if not x[2]]
def endkind(tr):
    t, j = tr[-1][0], tr[-1][3]
    if t >= T - 1: return 'alive'
    m = LB[t] == j; ov = LB[t + 1][m]; ov = ov[ov > 0]
    if not ov.size: return 'dissolved'
    return 'split' if len(np.unique(ov)) > 1 else 'merged'
endk = {}
for tr in L:
    st = [x[1] > 2 for x in tr]
    if st[-1] and any(not v for v in st):
        e = endkind(tr); endk[e] = endk.get(e, 0) + 1
fates = {f: sum(1 for x in spells if x[1] == f and not x[2]) for f in ('reattach', 'end', 'alive_at_end')}
# divisions
LBA = [labels(f[1], A) for f in R]


def persists(t, i, n=5):
    m = LBA[t] == i
    for k in range(t + 1, min(T, t + n)):
        ov = LBA[k][m]; ov = ov[ov > 0]
        if not ov.size: return None
        j = np.bincount(ov).argmax(); m = LBA[k] == j
    return m if t + n <= T else None


div = []
for t in range(max(5, t_start), T - 6):
    L0, L1 = LBA[t], LBA[t + 1]
    for i in np.unique(L0[L0 > 0]):
        m = L0 == i; kids = [j for j in np.unique(L1[m]) if j > 0 and (L1[m] == j).sum() >= 10]
        if len(kids) < 2: continue
        if not all(np.bincount(L0[L1 == j][L0[L1 == j] > 0]).argmax() == i for j in kids): continue
        ends = [persists(t + 1, j) for j in kids]
        if any(e is None for e in ends): continue
        gp = float(DP[t][m].min())
        g1 = [float(DP[t + 1][L1 == j].min()) for j in kids]
        g5 = [float(DP[t + 5][e].min()) for e in ends]
        cy, cx = ndimage.center_of_mass(m)
        div.append(dict(t=t * DTF, y=int(cy), x=int(cx), parent_gap=gp, kid_gap1=g1, kid_gap5=g5))
out = dict(frames_from=t_start, mean_pred=float(np.mean(nt)), mean_free=float(np.mean(nf)),
           free_frac=float(np.sum(nf) / max(1, np.sum(nt))),
           tracks10=len(L), track_free_frac_median=float(np.median(ffree)) if ffree else 0,
           tracks_ever_free=int(sum(f > 0 for f in ffree)), tracks_mostly_free=int(sum(f > 0.5 for f in ffree)),
           detach_events=detach, free_spells_after_contact=len(sp_len), spell_frames_median=float(np.median(sp_len)) if sp_len else 0, spell_frames_max=int(max(sp_len)) if sp_len else 0, spell_fates=fates, free_end_kind=endk, born_free_spells=sum(1 for x in spells if x[2]), hops=hops, hop_examples=hop_tr[:20],
           divisions=len(div), div_parent_free=int(sum(d['parent_gap'] > 2 for d in div)),
           div_parent_gap_gt6=int(sum(d['parent_gap'] > 6 for d in div)),
           div_any_kid_free_t5=int(sum(max(d['kid_gap5']) > 2 for d in div)),
           div_all_kids_free_t5=int(sum(min(d['kid_gap5']) > 2 for d in div)), div_list=div)
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ('div_list', 'hop_examples')}))
