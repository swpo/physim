"""c58: trait heredity and selection in the continuous-trait fed vortices. Adapted from c53's heredity.py
(20261027T0845-c53-fed-vortex-selection-claim): runs world.py (WORLD_P honoured), records |omega|, c, z every 3 t,
segments and tracks the vortices with labkit's own segmentation and tracker on |omega| (merge-aware lineage, K=20 frames).
For each vortex: trait = sum(z)/sum(c) over its mask, within-vortex spread = c-weighted std of z/c (pixels with c > 0.2).
Reports: at every persistent split after lab_t the parent's trait at its last frame and each surviving daughter's at its
first frame; trait jumps of living vortices (|change| > dm/2 over 15 t) at or away from a logged mutation; the vortex-mean
trait and the dominant trait class (round(theta/dm)) over time; births per trait class.
python trait.py out_prefix seed T"""
import sys, os, json, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as R, metrics as M
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('w', os.path.join(here, 'world.py')); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
out, seed, Tend = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
FR = 3.0
s = w.init(seed, (128, 128)); dt = w.P['dt']; dm = w.P['dm']; per = int(round(FR / dt)); n = int(Tend / dt)
TT, CC, ZZ = [], [], []
for i in range(n + 1):
    if i % per == 0:
        TT.append(np.abs(s['om']).astype(np.float32)); CC.append(s['c'].astype(np.float32)); ZZ.append(s['z'].astype(np.float32))
    if i < n: s = w.step(s)
mat = np.stack(TT); del TT
mn, thr, lo, hi = R._normalize_matter(mat, w.META, True, w.META.get('threshold'))
H, W = mat.shape[1:]
comps, links = R._segment_frames(mn, thr, R._default_min_area(H, W), True, keep_labels=True)
tracks, events = M.track(comps, links, (H, W), True)
lin = M.lineage_stats(tracks, events, len(mn), FR, (H, W), True, 20)
lab_f = int(w.P['lab_t'] / FR)
def trait(f, ci):
    m = comps[f]['lab'] == ci + 1; c = CC[f][m]; z = ZZ[f][m]; sc = c.sum()
    if c.mean() < 0.2: return np.nan, np.nan      # unlabelled vortex (not eating at lab_t, or label lost)
    th = z.sum() / sc; g = c > 0.2
    sp = float(np.sqrt((c[g] * (z[g] / c[g] - th) ** 2).sum() / c[g].sum())) if g.sum() > 2 else np.nan
    return float(th), sp
pop = []; spreads = []; tbf = []
for f in range(lab_f + 2, len(mn), 10):
    tv = [trait(f, ci) for ci in range(comps[f]['n'])]; th = np.array([x[0] for x in tv if np.isfinite(x[0])])
    spreads += [x[1] for x in tv if np.isfinite(x[1])]
    tbf.append((round(f * FR), [round(float(x), 2) for x in th]))
    if th.size:
        cls, cnt = np.unique(np.round(th / dm).astype(int), return_counts=True)
        pop.append((round(f * FR), int(th.size), round(float(th.mean()), 3), round(float(th.std()), 3), int(cls[cnt.argmax()]), round(float(cnt.max() / th.size), 2),
                    int(cls.min()), int(cls.max())))
rows = []
for e in lin['persistent_splits']:
    if e['frame'] <= lab_f + 2: continue
    p = tracks[e['parent']]; tp, _ = trait(p['end'], p['comp'][-1])
    for c in e['surviving_children']:
        t = tracks[c]; tc, _ = trait(t['start'], t['comp'][0])
        if np.isfinite(tp) and np.isfinite(tc): rows.append((e['frame'] * FR, round(tp, 3), round(tc, 3)))
rows_a = np.array(rows) if rows else np.zeros((0, 3))
muts = s.get('mutations', [])
def near_mut(f, cy, cx):
    # a whole-vortex mutation shifts a vortex anywhere on it: match by time only (the jump window spans 15 t)
    for (tm, my, mx, sg) in muts:
        if -3 <= f * FR - tm <= 18: return True
    return False
jm = jo = 0; jo_sizes = []
for t in tracks:
    if t['start'] <= lab_f + 2 or t['end'] - t['start'] < 10: continue
    ks = [trait(t['start'] + k, ci)[0] for k, ci in enumerate(t['comp'])]
    k = 5
    while k < len(ks):
        if np.isfinite(ks[k]) and np.isfinite(ks[k - 5]) and abs(ks[k] - ks[k - 5]) > dm / 2:
            if near_mut(t['start'] + k, t['cy'][k], t['cx'][k]): jm += 1
            else: jo += 1; jo_sizes.append(round(ks[k] - ks[k - 5], 3))
            k += 10
        else: k += 1
d = rows_a[:, 2] - rows_a[:, 1] if len(rows_a) else np.zeros(0)
res = {'seed': seed, 'WORLD_P': os.environ.get('WORLD_P', '{}'), 'T': Tend, 'mutations': len(muts), 'mut_signs_sum': float(sum(m[3] for m in muts)),
       'persistent_splits_after_label': len(rows), 'daughter_keep_class': int((np.abs(d) < dm / 2).sum()), 'daughter_absdiff_median': float(np.median(np.abs(d))) if d.size else None,
       'parent_daughter_corr': float(np.corrcoef(rows_a[:, 1], rows_a[:, 2])[0, 1]) if len(rows_a) > 3 else None,
       'within_spread_median': float(np.median(spreads)) if spreads else None, 'within_spread_p90': float(np.percentile(spreads, 90)) if spreads else None,
       'jumps_at_mutation': jm, 'jumps_elsewhere': jo, 'jumps_elsewhere_sizes': jo_sizes[:60],
       'lineage': {k: lin[k] for k in lin if k not in ('persistent_splits',) and isinstance(lin[k], (int, float, str))},
       'pop_t_n_mean_std_domclass_domshare_min_max': pop, 'split_rows': rows, 'traits_by_frame': tbf}
json.dump(res, open(out + '.json', 'w'), indent=0, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
print({k: v for k, v in res.items() if k not in ('split_rows', 'traits_by_frame', 'pop_t_n_mean_std_domclass_domshare_min_max', 'jumps_elsewhere_sizes')})
print(pop[::10])
