"""python dipmove.py <pack_seed_dir> <world.py> : labkit's own segmentation, tracker and merge-aware lineage (K=20) on |omega|,
each track's sign from the rendered signed-vorticity channel. For every frame step of every track: its speed and whether
its nearest other body is an opposite-sign vortex (a dipole partner) or a same-sign one, within 2.5 sqrt(own area).
For dividing vortices (born by a persistent split, ending in one): net travel between birth and division in sqrt(area)
and in long axes (4 sqrt of the largest covariance eigenvalue), and the share of their life spent with a dipole partner.
Writes the json to argv[3] (default dipmove.json in the current directory)."""
import sys, json, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as R, metrics as M
pack, wpath = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location('w', wpath); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
F = np.load(f'{pack}/frames.npz'); mat = F['matter'].astype(np.float32); RR = F['render'].astype(np.float32); rf = list(F['render_f'])
m = json.load(open(f'{pack}/metrics.json')); dtf = m['steps_per_frame'] * m['dt']
mn, thr, lo, hi = R._normalize_matter(mat, W.META, True, W.META.get('threshold')); H, Wd = mn.shape[1:]
comps, links = R._segment_frames(mn, thr, R._default_min_area(H, Wd), True, keep_labels=True)
tracks, events = M.track(comps, links, (H, Wd), True)
lin = M.lineage_stats(tracks, events, len(mn), dtf, (H, Wd), True, 20)
owner = {}
for t in tracks:
    for k, ci in enumerate(t['comp']): owner[(t['start'] + k, ci)] = t['id']
sgn = {}
for t in tracks:
    s = 0
    for k, ci in enumerate(t['comp']):
        f = t['start'] + k
        if f in rf:
            s = int(np.sign(RR[rf.index(f), 2][comps[f]['lab'] == ci + 1].sum())); break
    sgn[t['id']] = s
def wrap(d, L): return (d + L / 2) % L - L / 2
def partner(f, ci, tid):
    cy, cx = comps[f]['cy'], comps[f]['cx']; a = comps[f]['area'] if 'area' in comps[f] else None
    me_area = float((comps[f]['lab'] == ci + 1).sum()); best = (1e9, 0)
    for cj in range(len(cy)):
        if cj == ci: continue
        d = np.hypot(wrap(cy[cj] - cy[ci], H), wrap(cx[cj] - cx[ci], Wd))
        if d < best[0]: best = (d, sgn.get(owner.get((f, cj)), 0))
    if best[0] < 2.5 * np.sqrt(me_area): return 'opp' if best[1] == -sgn[tid] and best[1] != 0 else ('same' if best[1] == sgn[tid] else 'none')
    return 'none'
steps = {'opp': [], 'same': [], 'none': []}
pstate = {}
for t in tracks:
    if sgn[t['id']] == 0: continue
    st = [partner(t['start'] + k, ci, t['id']) for k, ci in enumerate(t['comp'])]; pstate[t['id']] = st
    for k in range(1, len(t['comp'])):
        a = np.array(t['area'][k - 1:k + 1], float)
        if max(a) / max(min(a), 1) > 1.5: continue           # skip area jumps (splits, merges, threshold flicker)
        v = np.hypot(wrap(t['cy'][k] - t['cy'][k - 1], H), wrap(t['cx'][k] - t['cx'][k - 1], Wd)) / dtf / np.sqrt(a.mean())
        steps[st[k]].append(v)
def longaxis(f, ci):
    yy, xx = np.nonzero(comps[f]['lab'] == ci + 1)
    if len(yy) < 3: return 1.0
    dy = wrap(yy - comps[f]['cy'][ci], H); dx = wrap(xx - comps[f]['cx'][ci], Wd)
    return float(4 * np.sqrt(max(np.linalg.eigvalsh(np.cov(np.stack([dy, dx])))[-1], 1e-9)))
ps = lin['persistent_splits']; born = {c for e in ps for c in e['surviving_children']}; ends = {e['parent'] for e in ps}
rows = []
for t in tracks:
    if t['id'] not in born or t['id'] not in ends or t['id'] not in pstate: continue
    dy = wrap(np.diff(t['cy']), H).sum(); dx = wrap(np.diff(t['cx']), Wd).sum(); net = float(np.hypot(dy, dx))
    sa = float(np.sqrt(np.mean(t['area']))); la = float(np.median([longaxis(t['start'] + k, ci) for k, ci in enumerate(t['comp'])][::3]))
    st = pstate[t['id']]
    rows.append({'id': t['id'], 'birth_t': t['start'] * dtf, 'div_t': t['end'] * dtf, 'net': net, 'BL_sqrtA': net / sa, 'BL_long': net / la,
                 'frac_dipole': float(np.mean([x == 'opp' for x in st])), 'frac_same': float(np.mean([x == 'same' for x in st]))})
out = {'pack': pack, 'speed_per_t_in_sqrtA': {k: {'n': len(v), 'median': float(np.median(v)) if v else None, 'mean': float(np.mean(v)) if v else None} for k, v in steps.items()},
       'dividing': len(rows), 'pass3_sqrtA': sum(r['BL_sqrtA'] >= 3 for r in rows), 'pass3_long': sum(r['BL_long'] >= 3 for r in rows),
       'pass3_long_mostly_dipole': sum(r['BL_long'] >= 3 and r['frac_dipole'] > 0.5 for r in rows),
       'median_frac_dipole_of_dividing': float(np.median([r['frac_dipole'] for r in rows])) if rows else None, 'rows': rows}
json.dump(out, open(sys.argv[3] if len(sys.argv) > 3 else 'dipmove.json', 'w'), indent=0)
print({k: v for k, v in out.items() if k != 'rows'})
