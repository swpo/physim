"""python divmove.py <pack_seed_dir> <world.py> : labkit's own segmentation/tracking of frames.npz; for every track that is
born in a split and ends in a persistent split (a dividing individual), the net displacement between its own birth and
its own division, in sqrt(area) and in its long-axis length (4 sqrt(largest covariance eigenvalue), conservative),
plus the travel direction and the largest frame-to-frame area jump. Writes divmove.json next to frames.npz."""
import sys, json, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as R, metrics as M
pack, wpath = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location('w', wpath); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
m = json.load(open(f'{pack}/metrics.json')); spf, dt = m['steps_per_frame'], m['dt']; dtf = spf * dt
mat = np.load(f'{pack}/frames.npz')['matter'].astype(np.float32)
mn, thr, lo, hi = R._normalize_matter(mat, W.META, True, W.META.get('threshold'))
H, Wd = mn.shape[1:]
comps, links = R._segment_frames(mn, thr, R._default_min_area(H, Wd), True)
tracks, events = M.track(comps, links, (H, Wd), True)
K, _ = R._lineage_k(W.META, None)
lin = M.lineage_stats(tracks, events, len(mn), dtf, (H, Wd), True, K)
ps = lin['persistent_splits']; ps_parent = {e['parent']: e for e in ps}; ps_children = {c for e in ps for c in e['children']}

def longaxis(f, ci):
    lab = comps[f]['lab']; yy, xx = np.nonzero(lab == ci + 1)
    if len(yy) < 3: return 1.0
    cy, cx = comps[f]['cy'][ci], comps[f]['cx'][ci]
    dy = (yy - cy + H / 2) % H - H / 2; dx = (xx - cx + Wd / 2) % Wd - Wd / 2
    ev = np.linalg.eigvalsh(np.cov(np.stack([dy, dx])))
    return float(4 * np.sqrt(max(ev[-1], 1e-9)))

rows = []
for t in tracks:
    if t['birth'] != 'split' or t['id'] not in ps_children or t['id'] not in ps_parent: continue
    dy = M._wrap(np.diff(t['cy']), H); dx = M._wrap(np.diff(t['cx']), Wd)
    net = float(np.hypot(dy.sum(), dx.sum())); size = float(np.sqrt(np.mean(t['area'])))
    la = float(np.median([longaxis(t['start'] + k, ci) for k, ci in enumerate(t['comp'])]))
    a = np.array(t['area'], float); jump = float(np.max(np.maximum(a[1:] / a[:-1], a[:-1] / a[1:]))) if len(a) > 1 else 1.0
    rows.append({'id': t['id'], 'birth_t': t['start'] * dtf, 'div_t': t['end'] * dtf, 'net': net, 'sqrt_area': size,
                 'long_axis': la, 'BL_sqrtA': net / size, 'BL_long': net / la, 'dir_deg': float(np.degrees(np.arctan2(dy.sum(), dx.sum()))),
                 'max_area_jump': jump})
n = len(rows); p3a = sum(r['BL_sqrtA'] >= 3 for r in rows); p3l = sum(r['BL_long'] >= 3 for r in rows)
up = sum(45 <= r['dir_deg'] <= 135 for r in rows)
out = {'pack': pack, 'persistent_splits': len(ps), 'max_generation': int(max(lin['generation'].values()) if isinstance(lin.get('generation'), dict) else -1),
       'dividing_tracks_born_by_split': n, 'pass_3BL_sqrtA': p3a, 'pass_3BL_longaxis': p3l, 'moving_up_45deg': up, 'rows': rows}
json.dump(out, open(f'{pack}/divmove.json', 'w'), indent=1)
print(pack, f"persistent splits {len(ps)}; dividing tracks born by split {n}; >=3 BL: {p3a}/{n} (sqrt area), {p3l}/{n} (long axis); travelling up (+-45deg) {up}/{n}")
for r in sorted(rows, key=lambda r: -r['BL_long'])[:5]:
    print('  track %d born %.0f divides %.0f net %.1f px, sqrtA %.1f, long axis %.1f -> %.1f / %.1f BL, dir %.0f deg, max area jump %.2f' % (r['id'], r['birth_t'], r['div_t'], r['net'], r['sqrt_area'], r['long_axis'], r['BL_sqrtA'], r['BL_long'], r['dir_deg'], r['max_area_jump']))
