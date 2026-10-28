"""c63: strips of labkit's persistent predator splits, deepest generation first, from record.py's frames (labkit's frames.npz has no per-species fields).
Re-runs labkit's own species pipeline (normalize, segment, track, lineage_stats, K=20) on the predator channel of the
render array, reports every persistent split (frame, generation of the daughters, whether prey matter touches the parent in
the frame before), and draws strips (red prey, green predator, crop 48 px on the parent) for the deepest-generation splits.
usage: predstrip.py FRAMES.npz OUT.png OUT.json [rows=8]"""
import sys, json, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as R, metrics as M
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy import ndimage
pk, outp, outj = sys.argv[1], sys.argv[2], sys.argv[3]; rows = int(sys.argv[4]) if len(sys.argv) > 4 else 8
F = np.load(pk); A, B = F['A'].astype(np.float32), F['B'].astype(np.float32)   # record.py output, frames 5 t apart
meta = {"threshold": 0.15, "smooth": 1.0}
T, H, W = B.shape; dtf = 5.0
mn, thr, lo, hi = R._normalize_matter(B, meta, True)
comps, links = R._segment_frames(mn, thr, R._default_min_area(H, W), True, keep_labels=True)
tracks, events = M.track(comps, links, (H, W), True)
lin = M.lineage_stats(tracks, events, T, dtf, (H, W), True, K=20)
gen = lin['generation']; res = []
for e in lin['persistent_splits']:
    f = e['frame']; p = tracks[e['parent']]; ci = p['comp'][-1]; fp = p['end']
    m = comps[fp]['lab'] == ci + 1
    near = ndimage.binary_dilation(m, iterations=2)
    prey_touch = bool((A[fp][near] > 0.3 * A.max()).any())
    g = max(gen[c] for c in e['surviving_children'])
    res.append({'frame': int(f), 't': f * dtf, 'gen': int(g), 'parent_free': not prey_touch,
                'cy': float(comps[fp]['cy'][ci]), 'cx': float(comps[fp]['cx'][ci])})
print('persistent predator splits', len(res), 'max gen', lin['max_generation'], 'free parents', sum(r['parent_free'] for r in res))
json.dump({'splits': res, 'max_generation': int(lin['max_generation']),
           'merges': sum(e['type'] == 'merge' for e in events), 'splits_all': sum(e['type'] == 'split' for e in events)}, open(outj, 'w'), indent=1)
sel = sorted(res, key=lambda r: (-r['gen'], r['t']))[:rows]
offs = [-4, -2, 0, 2, 6, 12]; C = 24
fig, ax = plt.subplots(max(1, len(sel)), len(offs), figsize=(1.5 * len(offs), 1.6 * max(1, len(sel))), squeeze=False)
amax, bmax = np.percentile(A, 99.9), np.percentile(B, 99.9)
for r, e in enumerate(sel):
    cy, cx = int(e['cy']), int(e['cx'])
    for j, o in enumerate(offs):
        f = min(max(e['frame'] + o, 0), T - 1)
        ys = (np.arange(cy - C, cy + C)) % H; xs = (np.arange(cx - C, cx + C)) % W
        img = np.zeros((2 * C, 2 * C, 3)); img[..., 0] = np.clip(A[f][np.ix_(ys, xs)] / amax, 0, 1); img[..., 1] = np.clip(B[f][np.ix_(ys, xs)] / bmax, 0, 1)
        a = ax[r, j]; a.imshow(img); a.set_xticks([]); a.set_yticks([]); a.set_title(f"t={f * dtf:.0f}", fontsize=7)
        if j == 0: a.set_ylabel(f"gen {e['gen']}\n{'free' if e['parent_free'] else 'on prey'}", fontsize=7)
fig.suptitle(f"{pk}: labkit persistent predator splits, deepest generation first (red prey, green predator)", fontsize=7)
fig.tight_layout(); fig.savefig(outp, dpi=80)
