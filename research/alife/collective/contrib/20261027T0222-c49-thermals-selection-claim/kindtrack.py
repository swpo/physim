"""python kindtrack.py <pack_seed_dir> <track_id> [...] : label share a/(a+b) of a labkit-tracked cap (divmove.py's tracker)
at every rendered frame of its life, from the pack's frames.npz (render channels 2, 3 = labels a, b)."""
import sys, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as R, metrics as M
spec = importlib.util.spec_from_file_location('w', 'world.py'); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
F = np.load(f'{sys.argv[1]}/frames.npz'); mat = F['matter'].astype(np.float32); RR = F['render'].astype(np.float32); fi = list(F['render_f'])
mn, thr, lo, hi = R._normalize_matter(mat, W.META, True, W.META.get('threshold')); H, Wd = mn.shape[1:]
comps, links = R._segment_frames(mn, thr, R._default_min_area(H, Wd), True, keep_labels=True)
tracks, _ = M.track(comps, links, (H, Wd), True)
for tid in map(int, sys.argv[2:]):
    t = tracks[tid]; out = []
    for k, ci in enumerate(t['comp']):
        f = t['start'] + k
        if f in fi:
            m = comps[f]['lab'] == ci + 1; j = fi.index(f); a = RR[j, 2][m].sum(); b = RR[j, 3][m].sum(); out.append((f, round(float(a / (a + b + 1e-9)), 2)))
    print('track', tid, 'born', t['birth'], t['start'], 'ends', t['end'], 'children', t['children'], 'label share a/(a+b):', out)
