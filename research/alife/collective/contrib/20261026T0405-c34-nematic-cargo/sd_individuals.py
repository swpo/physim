"""(c21; c34 adds a cargo inside/outside ratio, inside d<=-1, outside 2<=d<=4) Per-individual signed-distance ring test (the question's rim |d|<=0.5 px, core d<=-1.5, outside
2<=d<=4, distances to the phi=0 contour, periodic), for each s channel, on every 5th render frame from frame
20: each body (phi>0 component >= 20 px, with >= 3 core px) gets rim/core and rim/out from pixels within 4 px
of it that are nearer to it than to any other body. Prints, per channel, the fraction of body-frames with
both ratios >= 1.5 and the medians. usage: sd_individuals.py frames.npz [channels, default 2,3,4] [dx]
(c34: optional dx converts pixel distances to world units, so the shells are the same physical widths on a finer grid;
the body-size floor 20 px is scaled by 1/dx^2.)"""
import sys, numpy as np
from scipy import ndimage
F = np.load(sys.argv[1]); R = F["render"].astype(np.float32); rf = list(F["render_f"])
chs = [int(c) for c in sys.argv[2].split(",")] if len(sys.argv) > 2 else [2, 3, 4]
dx = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
H, W = R.shape[2:]; sl = (slice(H, 2 * H), slice(W, 2 * W))
res = {c: [] for c in chs}
for k, f in enumerate(rf):
    if f < 20 or k % 5: continue
    phi = R[k, 0]; ins = phi > 0
    t = np.tile(ins, (3, 3))
    d = dx * np.where(t, -(ndimage.distance_transform_edt(t) - 0.5), ndimage.distance_transform_edt(~t) - 0.5)[sl]
    lab, n = ndimage.label(t)
    # nearest-body label for every pixel (periodic via tiling)
    _, (iy, ix) = ndimage.distance_transform_edt(lab == 0, return_indices=True)
    near = lab[iy, ix][sl]; labc = lab[sl]
    for j in np.unique(labc[labc > 0]):
        body = labc == j
        if body.sum() < 20 / dx ** 2: continue
        own = near == j
        rim, core, out = own & (np.abs(d) <= 0.5), own & (d <= -1.5), own & (d >= 2) & (d <= 4)
        if core.sum() < 3 or rim.sum() < 4 or out.sum() < 4: continue
        for c in chs:
            x = R[k, c]; a = x[rim].mean() / max(x[core].mean(), 1e-9); b = x[rim].mean() / max(x[out].mean(), 1e-9)
            ins = own & (d <= -1)
            res[c].append((a, b, x[ins].mean() / max(x[out].mean(), 1e-9) if ins.sum() else np.nan))
for c in chs:
    v = np.array([r[:2] for r in res[c]]); w = np.array([r[2] for r in res[c]])
    print(f"{sys.argv[1]} ch{c}: inside/outside (d<=-1 vs 2<=d<=4) median {np.median(w):.2f}, fraction >= 2: {(w >= 2).mean():.2f}"); ok = ((v[:, 0] >= 1.5) & (v[:, 1] >= 1.5)).mean() if len(v) else float("nan")
    print(f"{sys.argv[1]} ch{c}: body-frames {len(v)}, both >= 1.5: {ok:.2f}, median rim/core {np.median(v[:, 0]):.2f}, median rim/out {np.median(v[:, 1]):.2f}")
