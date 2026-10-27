"""c52: rebuild labkit's per-species tracking for one species from frames.npz (labkit's own functions and settings),
pick the deepest-generation track, and draw its ancestry: one row per generation, crops at the split frame.
usage: predlineage.py pack/seedN chan out.png [K=20]"""
import sys, json, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as LR, metrics as M
import importlib.util
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
pack, ch, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]; K = int(sys.argv[4]) if len(sys.argv) > 4 else 20
spec = importlib.util.spec_from_file_location('w', 'world.py'); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
R = np.load(pack + '/frames.npz')['render'].astype(np.float32); mat = R[:, ch]; T = len(mat); shape = mat.shape[1:]
mn, thr, lo, hi = LR._normalize_matter(mat, w.META, True)
comps, links = LR._segment_frames(mn, thr, 6, True, keep_labels=False)
tracks, events = M.track(comps, links, shape, True)
lin = M.lineage_stats(tracks, events, T, 100.0, shape, True, K=K)
gen = lin['generation']; ps = {c: e for e in lin['persistent_splits'] for c in e['children']}
print('tracks', len(tracks), 'persistent splits', len(lin['persistent_splits']), 'max gen', lin['max_generation'])
best = max(gen, key=lambda i: (gen[i], -tracks[i]['start']))
chain = [best]
while tracks[chain[-1]]['parents']:
    chain.append(tracks[chain[-1]]['parents'][0])
chain = chain[::-1]
info = [(i, tracks[i]['start'], tracks[i]['end'], gen[i], tracks[i]['birth']) for i in chain]
print('ancestry (id, start, end, gen, birth):', info)
splitf = [tracks[i]['start'] for i in chain[1:] if i in ps]
fig, ax = plt.subplots(len(splitf), 4, figsize=(6.4, 1.7 * len(splitf)), squeeze=False)
H = shape[0]; h = 20
for r, f in enumerate(splitf):
    tid = [i for i in chain if tracks[i]['start'] == f][0]
    cy, cx = int(tracks[tid]['cy'][0]), int(tracks[tid]['cx'][0])
    for c, d in enumerate((-2, -1, 0, 3)):
        F = R[min(T - 1, f + d)]; ys = np.arange(cy - h, cy + h) % H; xs = np.arange(cx - h, cx + h) % H
        rgb = np.stack([F[1], F[0], 0.35 * F[2]], -1)[np.ix_(ys, xs)].clip(0, 1)
        ax[r, c].imshow(rgb); ax[r, c].set_xticks([]); ax[r, c].set_yticks([])
        ax[r, c].set_title(f't={(f + d) * 100:.0f}' + (f' gen {gen[tid]}' if d == 0 else ''), fontsize=7)
plt.suptitle(f'{pack} species ch{ch}: ancestry of track {best} (gen {gen[best]}), crop centred on the daughter at its birth', fontsize=7)
plt.tight_layout(); plt.savefig(out, dpi=90)
json.dump({'ancestry': info, 'split_frames': splitf}, open(out.replace('.png', '.json'), 'w'))
