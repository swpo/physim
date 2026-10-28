"""c58: trait.py (20261027T1245-c58-vortex-waste-novelty) for a trait vector. Runs world.py (WORLD_P honoured), records |omega|,
c, z every 3 t, segments and tracks the vortices with labkit's segmentation and tracker on |omega| (K=20 frames). A vortex's
trait is sum(z_i)/sum(c) over its mask (nan if mean c < 0.2); its class is the tuple round(theta_i/dm). Reports daughter
fidelity (|theta_daughter - theta_parent| < dm/2) at persistent splits, the within-vortex spread, trait jumps of living
vortices at / away from a mutation, and per 30 t the labelled vortices' traits; novelty: dominance spells (>= 3 samples),
distinct dominant classes, first-time dominants, classes ever held by >= 3 vortices (cumulative, at t=1500/3000/4500/end).
python trait3.py out_prefix seed T"""
import sys, os, json, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as R, metrics as M, ops as _ops; _ops.WORKERS = int(os.environ.get('OMP_NUM_THREADS', '2'))
here = os.environ.get('WORLD_DIR', '/home/user/physim/research/alife/collective/contrib/20261027T1401-c58-vortex-trait3d')
spec = importlib.util.spec_from_file_location('w', os.path.join(here, 'world.py')); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
out, seed, Tend = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
FR = 3.0
NN = int(os.environ.get('SIZE', '128')); s = w.init(seed, (NN, NN)); dt = w.P['dt']; dm = w.P['dm']; per = int(round(FR / dt)); n = int(Tend / dt)
TT, CC, ZZ = [], [], []; SNAP = []; snap_i = set(int(x) for x in np.linspace(int(w.P['lab_t'] / dt) + 1, n, 8))
# checkpoint/resume (c59): every CK steps the state and the frames recorded since the last checkpoint go to out_ck/
import pickle
CKD = out + '_ck'; os.makedirs(CKD, exist_ok=True); CK = int(round(250.0 / dt)); i0 = 0; nch = 0
if os.path.exists(CKD + '/state.pkl'):
    st = pickle.load(open(CKD + '/state.pkl', 'rb')); s, i0, nch, SNAP = st['s'], st['i'], st['nch'], st['snap']
    for k in range(nch):
        d = np.load(f'{CKD}/ch{k:04d}.npz'); TT += list(d['T']); CC += list(d['C']); ZZ += list(d['Z'])
    print('resumed at step', i0, 'chunks', nch, flush=True)
bt, bc, bz = [], [], []
for i in range(i0, n + 1):
    if i % per == 0:
        bt.append(np.abs(s['om']).astype(np.float32)); bc.append(s['c'].astype(np.float32)); bz.append(s['z'].astype(np.float32))
    if i in snap_i: SNAP.append((round(s['t']), np.abs(s['om']).copy(), s['c'].copy(), s['z'][:3].copy()))
    if i < n: s = w.step(s)
    if (i + 1) % CK == 0 or i == n:
        np.savez(f'{CKD}/ch{nch:04d}.npz', T=np.array(bt), C=np.array(bc), Z=np.array(bz)); nch += 1
        TT += bt; CC += bc; ZZ += bz; bt, bc, bz = [], [], []
        pickle.dump({'s': s, 'i': i + 1, 'nch': nch, 'snap': SNAP}, open(CKD + '/state.tmp', 'wb')); os.replace(CKD + '/state.tmp', CKD + '/state.pkl')
mat = np.stack(TT); del TT
mn, thr, lo, hi = R._normalize_matter(mat, w.META, True, w.META.get('threshold'))
H, W = mat.shape[1:]
comps, links = R._segment_frames(mn, thr, R._default_min_area(H, W), True, keep_labels=True)
tracks, events = M.track(comps, links, (H, W), True)
lin = M.lineage_stats(tracks, events, len(mn), FR, (H, W), True, 20)
lab_f = int(w.P['lab_t'] / FR)
def trait(f, ci):
    m = comps[f]['lab'] == ci + 1; c = CC[f][m]
    if c.size == 0 or c.mean() < 0.2: return None, np.nan
    z = ZZ[f][:, m]; th = z.sum(1) / c.sum(); g = c > 0.2
    sp = float(np.sqrt((c[g] * ((z[:, g] / c[g] - th[:, None]) ** 2).sum(0)).sum() / c[g].sum())) if g.sum() > 2 else np.nan
    return th, sp
tid = {}
for k_, t_ in enumerate(tracks):
    for j_, ci_ in enumerate(t_['comp']): tid[(t_['start'] + j_, ci_)] = k_
vort = []
tbf = []; spreads = []
for f in range(lab_f + 2, len(mn), 10):
    tv = [trait(f, ci) for ci in range(comps[f]['n'])]
    vort.append((round(f * FR), [[round(float(v), 3) for v in x[0]] + [round(float(comps[f]['cy'][ci]), 1), round(float(comps[f]['cx'][ci]), 1), tid.get((f, ci), -1)] for ci, x in enumerate(tv) if x[0] is not None]))
    spreads += [x[1] for x in tv if np.isfinite(x[1])]
    tbf.append((round(f * FR), [[round(float(v), 2) for v in x[0]] for x in tv if x[0] is not None]))
rows = []
for e in lin['persistent_splits']:
    if e['frame'] <= lab_f + 2: continue
    p = tracks[e['parent']]; tp, _ = trait(p['end'], p['comp'][-1])
    for ch in e['surviving_children']:
        t = tracks[ch]; tc, _ = trait(t['start'], t['comp'][0])
        if tp is not None and tc is not None: rows.append((e['frame'] * FR, float(np.linalg.norm(tc - tp))))
muts = s.get('mutations', [])
jm = jo = 0
for t in tracks:
    if t['start'] <= lab_f + 2 or t['end'] - t['start'] < 10: continue
    ks = [trait(t['start'] + k, ci)[0] for k, ci in enumerate(t['comp'])]
    k = 5
    while k < len(ks):
        if ks[k] is not None and ks[k - 5] is not None and np.linalg.norm(ks[k] - ks[k - 5]) > dm / 2:
            tm = (t['start'] + k) * FR
            if any(-3 <= tm - m[0] <= 18 for m in muts): jm += 1
            else: jo += 1
            k += 10
        else: k += 1
# novelty
dom = []; ever = set(); cum = []
for tt, th in tbf:
    cl = [tuple(int(round(v / dm)) for v in x) for x in th]
    u = {}
    for c in cl: u[c] = u.get(c, 0) + 1
    dom.append(max(u, key=u.get) if u else None); ever |= {c for c, k in u.items() if k >= 3}; cum.append(len(ever))
spells = []; k = 0
while k < len(dom):
    j = k
    while j < len(dom) and dom[j] == dom[k]: j += 1
    if j - k >= 3 and dom[k] is not None and (not spells or spells[-1][1] != dom[k]): spells.append((tbf[k][0], dom[k]))
    k = j
seen = set(); new_t = []; ret = 0
for ts, c in spells:
    if c in seen: ret += 1
    else: seen.add(c); new_t.append(ts)
tts = np.array([a for a, _ in tbf]); idx = np.searchsorted(tts, [1500, 3000, 4500])
d = np.array([r_[1] for r_ in rows])
res = {'seed': seed, 'WORLD_P': os.environ.get('WORLD_P', '{}'), 'T': Tend, 'nt': w.P['nt'], 'mutations': len(muts),
       'persistent_splits_after_label': len(rows), 'daughter_keep_class': int((d < dm / 2).sum()), 'daughter_dist_median': float(np.median(d)) if d.size else None,
       'within_spread_median': float(np.median(spreads)) if spreads else None, 'jumps_at_mutation': jm, 'jumps_elsewhere': jo,
       'max_generation': lin.get('max_generation'), 'spells': len(spells), 'distinct_dominant': len(seen),
       'first_time_dominant_t<3000': int(sum(1 for x in new_t[1:] if x < 3000)), 'first_time_dominant_t>=3000': int(sum(1 for x in new_t[1:] if x >= 3000)), 'returns': ret,
       'classes_ever_ge3_at_1500_3000_4500_end': [cum[i] for i in idx if i < len(cum)] + [cum[-1]],
       'mean_n_vortices': float(np.mean([len(th) for _, th in tbf])), 'cum_classes': list(zip(tts.tolist(), cum)), 'spells_list': [(a, list(b)) for a, b in spells], 'traits_by_frame': tbf, 'vort': vort, 'size': NN, 'splits': [(e['frame'] * FR, e['parent'], list(e['surviving_children'])) for e in lin['persistent_splits']], 'track_span': [(t['start'] * FR, t['end'] * FR) for t in tracks]}
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, len(SNAP), figsize=(2.3 * len(SNAP), 2.6))
for a, (tt, om, c, z) in zip(ax, SNAP):
    th = z / np.maximum(c, 0.05)[None]; img = np.clip(0.5 + th.transpose(1, 2, 0) / 3.0, 0, 1)
    img[~((om > 0.06) & (c > 0.2))] = 1.0
    a.imshow(img); a.set_xticks([]); a.set_yticks([]); a.set_title(f't={tt}', fontsize=8)
fig.suptitle(f"{os.path.basename(out)} seed {seed} {os.environ.get('WORLD_P', '')}: RGB = 0.5 + theta_1..3 / 3 (grey = ancestral 0)", fontsize=8)
fig.savefig(out + '_maps.png', dpi=70)
json.dump(res, open(out + '.json', 'w'), default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
print({k: v for k, v in res.items() if k not in ('traits_by_frame', 'cum_classes', 'spells_list', 'vort', 'splits', 'track_span')})
