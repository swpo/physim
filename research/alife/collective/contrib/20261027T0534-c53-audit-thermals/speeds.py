"""python speeds.py <seed_dir> <world.py> t0 t1 : labkit's own segmentation and tracker; for every track alive in frames
[t0, t1), its mean vertical and horizontal velocity there (px per frame), its sqrt(area), and the number of bodies per
frame. Used to compare the fed world with the passive-thermal and burn-off forks."""
import sys, json, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as R, metrics as M
pack, wpath, t0, t1 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
spec = importlib.util.spec_from_file_location('w', wpath); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
mat = np.load(f'{pack}/frames.npz')['matter'].astype(np.float32)
mn, thr, lo, hi = R._normalize_matter(mat, W.META, True, W.META.get('threshold'))
H, Wd = mn.shape[1:]
comps, links = R._segment_frames(mn, thr, R._default_min_area(H, Wd), True)
tracks, events = M.track(comps, links, (H, Wd), True)
vy, vx, sa = [], [], []
for t in tracks:
    idx = [k for k in range(len(t['cy'])) if t0 <= t['start'] + k < t1]
    if len(idx) < 5: continue
    cy = np.array(t['cy'])[idx]; cx = np.array(t['cx'])[idx]
    dy = M._wrap(np.diff(cy), H); dx = M._wrap(np.diff(cx), Wd)
    vy.append(dy.mean()); vx.append(dx.mean()); sa.append(np.sqrt(np.mean(np.array(t['area'])[idx])))
vy, vx, sa = map(np.array, (vy, vx, sa))
n = [len(comps[f]['cy']) for f in range(t0, min(t1, len(comps)))]
out = {'pack': pack, 'window': [t0, t1], 'tracks': int(len(vy)), 'median_vy': float(np.median(vy)) if len(vy) else None,
       'median_speed': float(np.median(np.hypot(vy, vx))) if len(vy) else None, 'median_sqrtA': float(np.median(sa)) if len(sa) else None,
       'frac_up': float(np.mean(vy > 0)) if len(vy) else None, 'bodies_first_last': [n[0], n[-1]] if n else None}
print(json.dumps(out))
