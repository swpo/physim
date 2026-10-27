"""c57: labkit's own segmentation and tracking for one channel; reports track lifetimes (time units), birth modes and
the K=20 lineage, and the fraction of consumer mass that sits inside prey (c_a > 0.5). usage: consumer_tracks.py pack world.py chan"""
import sys, json, numpy as np, importlib.util
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as LR, metrics as M
pack, wp, ch = sys.argv[1], sys.argv[2], int(sys.argv[3])
spec = importlib.util.spec_from_file_location('w', wp); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
R = np.load(pack + '/frames.npz')['render'].astype(np.float32); mat = R[:, ch]; T = len(mat); shape = mat.shape[1:]
mn, thr, lo, hi = LR._normalize_matter(mat, w.META, True)
comps, links = LR._segment_frames(mn, thr, 6, True, keep_labels=False)
tracks, events = M.track(comps, links, shape, True)
life = np.array([(t['end'] - t['start'] + 1) * 100 for t in tracks]); births = {}
for t in tracks: births[t['birth']] = births.get(t['birth'], 0) + 1
out = {"tracks": len(tracks), "life_median": float(np.median(life)), "life_p90": float(np.percentile(life, 90)),
       "frac_life_ge_2000": float((life >= 2000).mean()), "n_life_ge_2000": int((life >= 2000).sum()), "births": births}
for K in (5, 20):
    lin = M.lineage_stats(tracks, events, T, 100.0, shape, True, K=K)
    out[f"K{K}"] = {"persistent_splits": len(lin['persistent_splits']), "max_gen": lin['max_generation']}
late = R[40:]; q = late[:, ch]; inside = (late[:, 0] > 0.5)
out["mass_inside_prey"] = float((q * inside).sum() / q.sum())
print(json.dumps(out))
