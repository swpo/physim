"""Share of (body, frame) pairs whose mean solute is >= 2x the outside (beyond a 3-px band around all
bodies; body = (u+1.6) > thr), frames 5..end, plus aggregate contrast. Usage: contrast.py pack_seed_dir [thr]"""
import sys, numpy as np
from scipy import ndimage
d = sys.argv[1]; thr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8
F = np.load(d + "/frames.npz"); R = F["render"]
n_ok = n_all = 0; agg = {}
for i in range(5, len(R)):
    u, c = R[i, 0], R[i, 1]
    body = u > thr; lab, n = ndimage.label(body)
    far = ~ndimage.binary_dilation(body, iterations=3)
    if n == 0 or not far.any(): continue
    cout = max(c[far].mean(), 1e-12)
    per = np.array(ndimage.mean(c, lab, range(1, n + 1))) / cout
    n_ok += int((per >= 2).sum()); n_all += n
    agg[i] = (c[body].mean() / cout, n, per.min())
ks = sorted(agg)
print(f"{d}: {n_ok/max(n_all,1):.3f} of {n_all} body-frames >= 2x; aggregate t-index {ks[0]} {agg[ks[0]][0]:.1f}, final {agg[ks[-1]][0]:.1f}; weakest body final {agg[ks[-1]][2]:.1f}x")
