"""python fate.py <pack_dir> [threshold, default 0.5]: predator (channel 1 > threshold) splits by overlap tracking on labkit's saved render frames
(100 t apart); for each split into >= 2 daughters of >= 6 px, follow every daughter by maximal overlap and report how
long it stays a separate body (until it vanishes, merges or the run ends) and whether it later grows to >= 1.5x its
birth area (a meal) or divides again."""
import sys, json, numpy as np
from scipy import ndimage
d = np.load(sys.argv[1] + '/frames.npz'); r = d['render'][:, 1].astype(float)
st = np.ones((3, 3)); AMIN = 6; TH = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
def lab(x):
    l, n = ndimage.label(x > TH, st)
    H, W = l.shape
    for i in range(H):
        if l[i, 0] and l[i, -1] and l[i, 0] != l[i, -1]: l[l == l[i, -1]] = l[i, 0]
    for j in range(W):
        if l[0, j] and l[-1, j] and l[0, j] != l[-1, j]: l[l == l[-1, j]] = l[0, j]
    ids = [i for i in np.unique(l) if i and (l == i).sum() >= AMIN]
    return l, ids
L = [lab(r[f]) for f in range(len(r))]
def nxt(f, cid):
    """components of frame f+1 overlapping component cid of frame f"""
    l0, _ = L[f]; l1, ids1 = L[f + 1]
    ov = np.unique(l1[(l0 == cid) & (l1 > 0)]); return [i for i in ov if i in ids1]
def follow(f, cid):
    a0 = (L[f][0] == cid).sum(); amax = a0; life = 0; fate = 'end'; redivide = False
    while f + 1 < len(L):
        k = nxt(f, cid)
        if not k: fate = 'vanished'; break
        if len(k) >= 2: redivide = True; fate = 'divided'; life += 1; break
        c1 = k[0]; back = np.unique(L[f][0][(L[f + 1][0] == c1) & (L[f][0] > 0)])
        if len([b for b in back if b in L[f][1]]) >= 2: fate = 'merged'; life += 1; break
        f, cid = f + 1, c1; life += 1; amax = max(amax, (L[f][0] == cid).sum())
    return dict(life_frames=life, fate=fate, grew=bool(amax >= 1.5 * a0), birth_area=int(a0))
ev = []
for f in range(len(L) - 1):
    for cid in L[f][1]:
        k = nxt(f, cid)
        if len(k) >= 2:
            ev.append(dict(t=(f + 1) * 100, daughters=[follow(f + 1, c) for c in k]))
n = len(ev); both5 = sum(all(x['life_frames'] >= 5 or x['fate'] == 'divided' for x in e['daughters']) for e in ev)
dau = [x for e in ev for x in e['daughters']]
out = dict(splits=n, splits_both_daughters_5frames_or_divide=both5, daughters=len(dau),
           daughters_vanished=sum(x['fate'] == 'vanished' for x in dau), daughters_merged=sum(x['fate'] == 'merged' for x in dau),
           daughters_divided_again=sum(x['fate'] == 'divided' for x in dau), daughters_reach_end=sum(x['fate'] == 'end' for x in dau),
           daughters_grew_1p5=sum(x['grew'] for x in dau), median_life_frames=float(np.median([x['life_frames'] for x in dau])) if dau else 0, events=ev)
json.dump(out, open(sys.argv[1] + '/fate_' + str(TH) + '.json', 'w'), indent=1)
print({k: v for k, v in out.items() if k != 'events'})
