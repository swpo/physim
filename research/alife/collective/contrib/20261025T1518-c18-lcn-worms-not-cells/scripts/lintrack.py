"""labkit lineage on a snapshot npz (channel 0 = A0 core), same normalization rules as labkit.run with META threshold 0.3."""
import sys, json, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import metrics as M
from scipy import ndimage
f = sys.argv[1]; K = int(sys.argv[2]) if len(sys.argv) > 2 else 20
d = np.load(f); X = d['X'][:, 0].astype(np.float32); t = d['t']
mn = np.stack([ndimage.gaussian_filter(x, 1.0, mode='wrap') for x in X])
thr = 0.3; H, W = X.shape[1:]
comps, links, prev = [], [None], None
for fr in range(len(mn)):
    seg = M.segment(mn[fr], thr, 20, True)
    if prev is not None: links.append(M.overlaps(prev['lab'], prev['n'], seg['lab'], seg['n']))
    comps.append(seg); prev = seg
tracks, events = M.track(comps, links, (H, W), True)
lin = M.lineage_stats(tracks, events, len(mn), float(t[1]-t[0]), (H, W), True, K=K)
print(f, {k: lin[k] for k in lin if isinstance(lin[k], (int, float))})
