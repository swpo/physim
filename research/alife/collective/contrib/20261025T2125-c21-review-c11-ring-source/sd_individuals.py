"""(c21) Per-individual signed-distance ring test (the question's rim |d|<=0.5 px, core d<=-1.5, outside
2<=d<=4, distances to the phi=0 contour, periodic), for each s channel, on every 5th render frame from frame
20: each body (phi>0 component >= 20 px, with >= 3 core px) gets rim/core and rim/out from pixels within 4 px
of it that are nearer to it than to any other body. Prints, per channel, the fraction of body-frames with
both ratios >= 1.5 and the medians. usage: sd_individuals.py frames.npz [channels, default 2,3,4]"""
import sys, numpy as np
from scipy import ndimage
F = np.load(sys.argv[1]); R = F["render"].astype(np.float32); rf = list(F["render_f"])
chs = [int(c) for c in sys.argv[2].split(",")] if len(sys.argv) > 2 else [2, 3, 4]
H, W = R.shape[2:]; sl = (slice(H, 2 * H), slice(W, 2 * W))
res = {c: [] for c in chs}
for k, f in enumerate(rf):
    if f < 20 or k % 5: continue
    phi = R[k, 0]; ins = phi > 0
    t = np.tile(ins, (3, 3))
    d = np.where(t, -(ndimage.distance_transform_edt(t) - 0.5), ndimage.distance_transform_edt(~t) - 0.5)[sl]
    lab, n = ndimage.label(t)
    # nearest-body label for every pixel (periodic via tiling)
    _, (iy, ix) = ndimage.distance_transform_edt(lab == 0, return_indices=True)
    near = lab[iy, ix][sl]; labc = lab[sl]
    for j in np.unique(labc[labc > 0]):
        body = labc == j
        if body.sum() < 20: continue
        own = near == j
        rim, core, out = own & (np.abs(d) <= 0.5), own & (d <= -1.5), own & (d >= 2) & (d <= 4)
        if core.sum() < 3 or rim.sum() < 4 or out.sum() < 4: continue
        for c in chs:
            x = R[k, c]; a = x[rim].mean() / max(x[core].mean(), 1e-9); b = x[rim].mean() / max(x[out].mean(), 1e-9)
            res[c].append((a, b))
for c in chs:
    v = np.array(res[c]); ok = ((v[:, 0] >= 1.5) & (v[:, 1] >= 1.5)).mean() if len(v) else float("nan")
    print(f"{sys.argv[1]} ch{c}: body-frames {len(v)}, both >= 1.5: {ok:.2f}, median rim/core {np.median(v[:, 0]):.2f}, median rim/out {np.median(v[:, 1]):.2f}")
