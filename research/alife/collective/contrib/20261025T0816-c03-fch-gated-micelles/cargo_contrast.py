"""Cargo held in micelles: mean c inside bodies ((u+1.6) > thr) / mean c outside (beyond a 3-px band),
per recorded frame; fraction of bodies whose own mean c is >= 2x the outside (so every daughter keeps cargo).
Usage: cargo_contrast.py pack_dir [thr]"""
import sys, numpy as np
from scipy import ndimage

d = sys.argv[1]; thr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8
F = np.load(d + "/frames.npz")
R, rf = F["render"], list(F["render_f"])
lines = []
for i in range(0, len(rf)):
    u, c = R[i, 0], R[i, 1]
    body = u > thr
    lab, n = ndimage.label(body)
    far = ~ndimage.binary_dilation(body, iterations=3)
    if n == 0 or not far.any():
        continue
    cout = c[far].mean()
    per = ndimage.mean(c, lab, range(1, n + 1)) / max(cout, 1e-12)
    lines.append((rf[i], c[body].mean() / max(cout, 1e-12), n, float(np.mean(per >= 2)), float(per.min())))
for l in lines[:: max(1, len(lines) // 10)] + [lines[-1]]:
    print(f"frame {l[0]}: contrast {l[1]:.1f}, bodies {l[2]}, share of bodies >=2x {l[3]:.2f}, weakest body {l[4]:.1f}x")
