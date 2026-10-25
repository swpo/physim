"""c08's arms.py readout (late droplet count, CV of area, polar order of psi-offset polarity),
applied to my packs. usage: arms_review.py pack_dir [pack_dir ...]"""
import sys, numpy as np
from scipy import ndimage

for d in sys.argv[1:]:
    z = np.load(d + "/frames.npz"); F = z["matter"]; R = z["render"]; rf = z["render_f"]
    pol = []
    for rr in R:
        phi, psi = rr[0], rr[1]; lab, k = ndimage.label(phi > 0); us = []
        for q in range(1, k + 1):
            m = lab == q
            if m.sum() < 20:
                continue
            yy, xx = np.nonzero(m); w = psi[m] - psi[m].min() + 1e-9
            v = np.array([(xx * w).sum() / w.sum() - xx.mean(), (yy * w).sum() / w.sum() - yy.mean()])
            if np.hypot(*v) > 0.3:
                us.append(v / np.hypot(*v))
        pol.append(np.hypot(*np.mean(us, 0)) if len(us) > 1 else np.nan)
    pol = np.array(pol)
    n, cv = [], []
    for fr in F:
        lab, k = ndimage.label(fr > 0); ar = np.bincount(lab.ravel())[1:]; ar = ar[ar >= 20]
        n.append(len(ar)); cv.append(ar.std() / ar.mean() if len(ar) > 1 else np.nan)
    n = np.array(n); cv = np.array(cv); late = slice(len(F) // 2, None)
    print(d, "n late mean %.1f sd %.1f" % (n[late].mean(), n[late].std()), "CV late %.2f" % np.nanmean(cv[late]),
          "polar order late %.2f" % np.nanmean(pol[len(pol) // 2:]))
