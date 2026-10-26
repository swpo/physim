"""(c39) From a labkit frames.npz of the layered CIPS world (channels e, p, F, s): every 10th render frame from frame 5,
(1) per body (e > 0.5 component >= 20 px) s rim/core and rim/out by signed distance (rim |d| <= 1.5 px, core d <= -3,
outside 4 <= d <= 7, own pixels), and (2) the share of catalysis kc F e^n (1-p) (the s source) on body pixels.
usage: layer_share.py frames.npz [n=2]"""
import sys, numpy as np
from scipy import ndimage
F = np.load(sys.argv[1]); R = F["render"].astype(np.float32); rf = list(F["render_f"]); n = float(sys.argv[2]) if len(sys.argv) > 2 else 2
H, W = R.shape[2:]; sl = (slice(H, 2 * H), slice(W, 2 * W)); res = []
for k in range(5, len(rf), 10):
    e, p, Fu, s = R[k]; ins = e > 0.5
    cat = Fu * np.clip(e, 0, None) ** n * (1 - p); share = cat[ins].sum() / cat.sum()
    t = np.tile(ins, (3, 3)); d = np.where(t, -(ndimage.distance_transform_edt(t) - 0.5), ndimage.distance_transform_edt(~t) - 0.5)[sl]
    lab, nb = ndimage.label(t); _, (iy, ix) = ndimage.distance_transform_edt(lab == 0, return_indices=True); near = lab[iy, ix][sl]; labc = lab[sl]
    ok = tot = 0; rc = []
    for j in np.unique(labc[labc > 0]):
        if (labc == j).sum() < 20: continue
        own = near == j; rim, core, out = s[own & (np.abs(d) <= 1.5)], s[own & (d <= -3)], s[own & (d >= 4) & (d <= 7)]
        if len(core) < 3 or len(out) < 4: continue
        a, b = rim.mean() / max(core.mean(), 1e-9), rim.mean() / max(out.mean(), 1e-9); rc.append((a, b)); tot += 1; ok += (a >= 1.5) and (b >= 1.5)
    rc = np.array(rc) if rc else np.zeros((1, 2))
    print(f"frame {rf[k]}: bodies {tot}, layer pass {ok}/{tot}, median rim/core {np.median(rc[:,0]):.2f} rim/out {np.median(rc[:,1]):.2f}, catalysis share on bodies {share:.2f}")
