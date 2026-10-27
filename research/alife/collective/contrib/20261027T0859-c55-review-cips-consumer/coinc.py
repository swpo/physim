"""c55: per-species labkit tracking (as in c52's predlineage.py: render channel, labkit normalisation, min area 6, K=int(__import__('os').environ.get('K', 20)))
for prey (ch0) and predator (ch1). For every persistent predator split, is there a prey split (any split, persistent or not)
within +-1 frame and 20 px? And for every persistent prey split, a predator within 8 px of the parent at the split frame?
Also: share of predator bodies touching prey (c_a render > 0.5 within 2 px) at every 10th frame after t=3000.
usage: coinc.py pack/seedN world.py out.json"""
import sys, json, numpy as np, importlib.util
from scipy import ndimage
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as LR, metrics as M
pack, wpath, out = sys.argv[1:4]
spec = importlib.util.spec_from_file_location('w', wpath); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
R = np.load(pack + '/frames.npz')['render'].astype(np.float32); T = len(R); shape = R.shape[2:]; H, W = shape
def trk(ch):
    mn, thr, lo, hi = LR._normalize_matter(R[:, ch], w.META, True)
    comps, links = LR._segment_frames(mn, thr, 6, True, keep_labels=True)
    tracks, events = M.track(comps, links, shape, True)
    lin = M.lineage_stats(tracks, events, T, 100.0, shape, True, K=int(__import__('os').environ.get('K', 20)))
    return comps, tracks, events, lin
pc, pt, pe, pl = trk(0); qc, qt, qe, ql = trk(1)
def wd(a, b, L): return (a - b + L / 2) % L - L / 2
prey_split_pts = []
for t in pt:
    if t['birth'] == 'split': prey_split_pts.append((t['start'], t['cy'][0], t['cx'][0]))
res = {'pred_persistent_splits': len(ql['persistent_splits']), 'pred_max_gen': ql['max_generation'],
       'prey_persistent_splits': len(pl['persistent_splits']), 'prey_max_gen': pl['max_generation']}
co = 0; rows = []
for e in ql['persistent_splits']:
    f = e['frame']; ch = [qt[c] for c in e['children']]
    cy = np.mean([c['cy'][0] for c in ch]); cx = np.mean([c['cx'][0] for c in ch])
    hit = any(abs(fp - f) <= 1 and np.hypot(wd(y, cy, H), wd(x, cx, W)) <= 20 for fp, y, x in prey_split_pts)
    co += hit; rows.append((f, round(float(cy)), round(float(cx)), bool(hit)))
res['pred_splits_with_prey_split_pm1frame_20px'] = co; res['pred_split_rows'] = rows
near = 0
for e in pl['persistent_splits']:
    f = e['frame']; p = pt[e['parent']]; m = pc[p['end']]['lab'] == p['comp'][-1] + 1
    md = ndimage.binary_dilation(m, iterations=8)
    near += bool((R[p['end'], 1][md] > 0.5).any())
res['prey_splits_with_predator_within_8px'] = near
tf = []
for f in range(30, T, 10):
    L, n = ndimage.label(R[f, 1] > 0.5); prey = ndimage.binary_dilation(R[f, 0] > 0.5, iterations=2)
    if n == 0: continue
    touch = ndimage.maximum(prey.astype(int), L, index=np.arange(1, n + 1))
    tf.append((f, n, float(np.mean(touch))))
res['pred_touching_prey_frac'] = tf
# predator tracks that survive >= 20 frames: how many ever exist without touching prey for >= 3 consecutive frames
json.dump(res, open(out, 'w'), indent=0, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print({k: v for k, v in res.items() if k not in ('pred_split_rows', 'pred_touching_prey_frac')}, 'touch frac', [round(x[2], 2) for x in tf])
