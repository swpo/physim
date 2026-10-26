"""Where is the catalyst made, and do bodies without catalyst persist? (c30 review of the FCH chemoton)
For each recorded frame of a labkit re-run: bodies = 8-connected components of (u+1) > 0.6 dilated by 2 px;
K production a K^2 P (a = 1) inside bodies vs in the bath; per body, its K content; bodies with K content
< 1% of the largest body's K are 'K-free'. Reports the share of K production on bodies and the share of
amphiphile held by K-free bodies, at t ~ 150, 300, 450, 600.
python kshare.py RERUN_DIR SEEDS..."""
import sys, numpy as np
from scipy import ndimage
R = sys.argv[1]
for s in sys.argv[2:]:
    d = np.load(f"{R}/seed{s}/frames.npz"); X = d["render"]; f = d["render_f"]
    for fr in [len(f) * k // 4 - 1 for k in (1, 2, 3, 4)]:
        u1, P, K = X[fr]; t = f[fr] * 3.0
        body = ndimage.binary_dilation(u1 > 0.6, iterations=2); lab, n = ndimage.label(body, structure=np.ones((3, 3)))
        prod = K * K * P; share = prod[body].sum() / prod.sum()
        kc = ndimage.sum(K, lab, range(1, n + 1)); uc = ndimage.sum(u1, lab, range(1, n + 1))
        kfree = kc < 0.01 * kc.max()
        print(f"seed {s} t={t:.0f}: bodies {n}, K-free {kfree.sum()}; K production on bodies {share:.3f}; amphiphile in K-free bodies {uc[kfree].sum() / uc.sum():.2f}")
