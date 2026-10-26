"""(c27) Droplet speed without merges: droplets (phi>0, >= 30 px) matched between consecutive recorded frames by
maximum overlap, kept only when the match is one-to-one and the area changes < 15%; speed = centroid shift / dt_frame.
Reports the median and 90th percentile over all such pairs after t >= 60, in px per unit time and in radii per unit time."""
import sys, json, numpy as np
from scipy import ndimage
for p in sys.argv[1:]:
    z = np.load(p + "/frames.npz"); F = z["render"].astype(float); fr = z["render_f"]
    m = json.load(open(p + "/metrics.json")); dtf = m["steps_per_frame"] * m["dt"]
    H, W = F.shape[2:]
    labs = []
    for i in range(len(F)):
        lab, n = ndimage.label(F[i, 0] > 0.5); labs.append(lab)
    sp, rad = [], []
    for i in range(len(F) - 1):
        if fr[i] * dtf < 60 or fr[i + 1] - fr[i] != 1: continue
        a, b = labs[i], labs[i + 1]
        for k in range(1, a.max() + 1):
            mk = a == k; A = mk.sum()
            if A < 30: continue
            ov = b[mk]; ov = ov[ov > 0]
            if len(ov) == 0: continue
            j = np.bincount(ov).argmax(); mj = b == j; B = mj.sum()
            back = a[mj]; back = back[back > 0]
            if np.bincount(back).argmax() != k or abs(B - A) > 0.15 * A or len(np.unique(back)) > 1 or len(np.unique(ov)) > 1: continue
            c0 = np.array(ndimage.center_of_mass(mk)); c1 = np.array(ndimage.center_of_mass(mj))
            if abs(c1 - c0).max() > H / 4: continue
            v = np.hypot(*(c1 - c0)) / dtf; sp.append(v); rad.append(v / np.sqrt(A / np.pi))
    print(json.dumps({"pack": p, "pairs": len(sp), "speed_median": round(float(np.median(sp)), 4), "speed_p90": round(float(np.percentile(sp, 90)), 4), "radii_per_t_median": round(float(np.median(rad)), 4)}))
