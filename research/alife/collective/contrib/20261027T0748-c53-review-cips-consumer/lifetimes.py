"""python lifetimes.py <pack_seed_dir> : per-species tracking rebuilt from the rendered channels (as c52's predlineage.py),
lifetimes of prey (ch 0) and consumer (ch 1) tracks in time units, how each consumer track begins and ends"""
import sys, importlib.util, collections, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as LR, metrics as M
spec = importlib.util.spec_from_file_location('w', '../20261026T1700-c43-cips-consumer/world.py'); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
F = np.load(sys.argv[1] + '/frames.npz'); R = F['render'].astype(np.float32); rf = F['render_f']; dtf = 100.0 * (rf[1] - rf[0])
for ch, name in ((0, 'prey'), (1, 'consumer')):
    mat = R[:, ch]; mn, thr, lo, hi = LR._normalize_matter(mat, w.META, True)
    comps, links = LR._segment_frames(mn, thr, 6, True, keep_labels=False)
    tracks, events = M.track(comps, links, mat.shape[1:], True)
    L = np.array([(t['end'] - t['start'] + 1) * dtf for t in tracks if t['start'] > 5])
    births = collections.Counter(t['birth'] for t in tracks if t['start'] > 5)
    print(f"{name}: {len(L)} tracks after t=500; lifetime median {np.median(L):.0f} t, p75 {np.percentile(L, 75):.0f}, p90 {np.percentile(L, 90):.0f}, max {L.max():.0f}; births {dict(births)}")
