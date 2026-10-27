"""python strip.py <pack_seed_dir> <track_id> <out.png> : heat-field crops (40x40, centred on the track's centroid) of one
dividing track from 10 t before its birth to 10 t after its division, from frames.npz (rendered frames, every ~5 t)."""
import sys, json, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = json.load(open(f'{sys.argv[1]}/divmove.json')); tid = int(sys.argv[2])
r = next(x for x in d['rows'] if x['id'] == tid)
F = np.load(f'{sys.argv[1]}/frames.npz'); R = F['render'].astype(np.float32); fi = F['render_f']
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as Rn, metrics as M
import importlib.util
spec = importlib.util.spec_from_file_location('w', 'world.py'); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
mat = F['matter'].astype(np.float32); mn, thr, lo, hi = Rn._normalize_matter(mat, W.META, True, W.META.get('threshold'))
H, Wd = mn.shape[1:]; comps, links = Rn._segment_frames(mn, thr, Rn._default_min_area(H, Wd), True, keep_labels=False)
tracks, _ = M.track(comps, links, (H, Wd), True); t = tracks[tid]
cand = [int(x) for x in fi if t['start'] - 10 <= x <= t['end'] + 12]
ts = [cand[i] for i in np.unique(np.linspace(0, len(cand) - 1, 10).round().astype(int))]
idx = {int(x): i for i, x in enumerate(fi)}
fig, ax = plt.subplots(1, len(ts), figsize=(16, 1.9))
for j, f in enumerate(ts):
    k = min(max(f - t['start'], 0), len(t['cy']) - 1); cy, cx = int(round(t['cy'][k])), int(round(t['cx'][k]))
    img = np.roll(np.roll(R[idx[f], 0], H // 2 - cy, 0), Wd // 2 - cx, 1)[H // 2 - 20:H // 2 + 20, Wd // 2 - 20:Wd // 2 + 20]
    ax[j].imshow(img, origin='lower', cmap='inferno', vmin=0, vmax=0.7); ax[j].axis('off')
    ax[j].set_title(f"t={f}" + (' <birth' if f < t['start'] else '') + (' >div' if f > t['end'] else ''), fontsize=8)
fig.suptitle(f"{sys.argv[1]} track {tid}: born {r['birth_t']:.0f} (split), divides {r['div_t']:.0f}; net {r['net']:.0f} px = {r['BL_sqrtA']:.1f} sqrt(area), {r['BL_long']:.1f} long axes; crops follow the centroid", fontsize=8)
plt.tight_layout(); plt.savefig(sys.argv[3], dpi=80)
