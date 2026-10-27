"""c55: for every persistent predator track (labkit per-species tracking, as coinc.py), which prey tracks does it touch
(prey label inside the predator mask dilated 2 px) over its life? Reports how many predators touch >= 2 distinct prey
tracks that are not related by a prey split during the predator's life (i.e. the predator changes partner), and how many
frames each predator spends touching no prey.
usage: partners.py pack world.py out.json"""
import sys, json, numpy as np, importlib.util
from scipy import ndimage
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as LR, metrics as M
pack, wpath, out = sys.argv[1:4]
spec = importlib.util.spec_from_file_location('w', wpath); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
R = np.load(pack + '/frames.npz')['render'].astype(np.float32); T = len(R); shape = R.shape[2:]
def trk(ch):
    mn, thr, lo, hi = LR._normalize_matter(R[:, ch], w.META, True)
    comps, links = LR._segment_frames(mn, thr, 6, True, keep_labels=True)
    tracks, events = M.track(comps, links, shape, True)
    lin = M.lineage_stats(tracks, events, T, 100.0, shape, True, K=20)
    return comps, tracks, lin
pc, pt, pl = trk(0); qc, qt, ql = trk(1)
tid = {}
for t in pt:
    for k, ci in enumerate(t['comp']): tid[(t['start'] + k, ci)] = t['id']
def anc(i):  # prey root along split parents
    s = {i}; st = [i]
    while st:
        j = st.pop()
        for p in pt[j]['parents']:
            if p not in s: s.add(p); st.append(p)
    return s
pers = [t for t in qt if t['end'] - t['start'] >= 20]
rows = []
for t in pers:
    seen = []; alone = 0
    for k, ci in enumerate(t['comp']):
        f = t['start'] + k; m = ndimage.binary_dilation(qc[f]['lab'] == ci + 1, iterations=2)
        ls = np.unique(pc[f]['lab'][m]); ls = [l - 1 for l in ls if l > 0]
        ids = {tid[(f, l)] for l in ls if (f, l) in tid}
        if not ids: alone += 1
        for i in ids:
            if i not in seen: seen.append(i)
    # partners unrelated by prey ancestry (neither is an ancestor of the other)
    roots = []
    for i in seen:
        a = anc(i)
        if not any(r in a or i in anc(r) for r in roots): roots.append(i)
    rows.append({'id': t['id'], 'life': t['end'] - t['start'], 'prey_partners': len(seen), 'unrelated_partners': len(roots), 'frames_alone': alone})
n = len(rows); sw = sum(r['unrelated_partners'] >= 2 for r in rows)
res = {'persistent_predators_ge20': n, 'touch_ge2_unrelated_prey': sw, 'median_partners': float(np.median([r['prey_partners'] for r in rows])),
       'median_frac_alone': float(np.median([r['frames_alone'] / r['life'] for r in rows])), 'rows': rows}
json.dump(res, open(out, 'w'), indent=0)
print({k: v for k, v in res.items() if k != 'rows'})
