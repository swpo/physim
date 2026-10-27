"""python findtrack.py <pack_seed_dir> : labkit's own segmentation, tracker and merge-aware lineage (K=20) on |omega|; label
share a/(a+b) of each track read from the rendered label channels (render ch 2, 3) at rendered frames inside its life. Lists
kind-b tracks (share < 0.5) that are born by a persistent split from a kind-b parent and themselves end in a persistent
split into kind-b daughters (a named lineage for the claim), with their generation."""
import sys, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as R, metrics as M
spec = importlib.util.spec_from_file_location('w', 'world.py'); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
F = np.load(f'{sys.argv[1]}/frames.npz'); mat = F['matter'].astype(np.float32); RR = F['render'].astype(np.float32); fi = list(F['render_f'])
mn, thr, lo, hi = R._normalize_matter(mat, W.META, True, W.META.get('threshold')); H, Wd = mn.shape[1:]
comps, links = R._segment_frames(mn, thr, R._default_min_area(H, Wd), True, keep_labels=True)
tracks, events = M.track(comps, links, (H, Wd), True)
lin = M.lineage_stats(tracks, events, len(mn), 3.0, (H, Wd), True, 20); gen = lin['generation']
def share(tid):
    t = tracks[tid]; out = []
    for k, ci in enumerate(t['comp']):
        f = t['start'] + k
        if f in fi:
            m = comps[f]['lab'] == ci + 1; a = RR[fi.index(f), 2][m].sum(); b = RR[fi.index(f), 3][m].sum()
            if a + b > 0: out.append(a / (a + b))
    return float(np.mean(out)) if out else np.nan
ps = lin['persistent_splits']; born = {c: e for e in ps for c in e['surviving_children']}; ends = {e['parent']: e for e in ps}
n = 0
for tid, e in born.items():
    if tid not in ends: continue
    sp, st = share(e['parent']), share(tid); kids = ends[tid]['surviving_children']; sk = [share(c) for c in kids]
    if all(np.isfinite(x) and x < 0.5 for x in [sp, st] + sk):
        print(f"track {tid}: kind b (share {st:.2f}), born t={e['frame'] * 3:.0f} from parent {e['parent']} (share {sp:.2f}), divides t={ends[tid]['frame'] * 3:.0f} into {kids} (shares {[round(x, 2) for x in sk]}), generation {gen[tid]}")
        n += 1
print(n, 'such tracks;', len(ps), 'persistent splits; max generation', lin['max_generation'])
