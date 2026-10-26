"""kbudget.py <frames.npz> [more]: from labkit's saved fields (u+1, P, K) compute, per recorded frame, the share
of catalyst autocatalysis (a K^2 P) and of amphiphile production (r K P) that happens on bilayer matter
(u+1 > 0.6, labkit's threshold), plus per-body K content of each connected body at the last frame."""
import sys, numpy as np
from scipy import ndimage
a, r = 1.0, 0.04
for p in sys.argv[1:]:
    d = np.load(p); key = [k for k in d.files if d[k].ndim == 4][0]; F = d[key]  # (T, C, H, W)
    print(p, F.shape)
    for t in (len(F) // 4, len(F) // 2, len(F) - 1):
        u1, P, K = F[t, 0], F[t, 1], F[t, 2]; on = u1 > 0.6
        auto = a * K * K * P; prod = r * K * P
        print(f"  frame {t}: bilayer share of K autocatalysis {auto[on].sum() / auto.sum():.2f}, of amphiphile production {prod[on].sum() / prod.sum():.2f}, of K {K[on].sum() / K.sum():.2f}, bilayer area frac {on.mean():.3f}")
    u1, K = F[-1, 0], F[-1, 2]; lab, n = ndimage.label(ndimage.binary_fill_holes(u1 > 0.6))
    Ks = ndimage.sum(K, lab, range(1, n + 1)); A = ndimage.sum(np.ones_like(K), lab, range(1, n + 1))
    print("  bodies at last frame (area, K content):", [(int(x), round(float(y), 1)) for x, y in zip(A, Ks)])
