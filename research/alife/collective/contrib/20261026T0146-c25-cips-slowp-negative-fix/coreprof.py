"""Final-frame body profiles: for bodies (e > 0.5, >= 40 px), mean e, p and F in the core (eroded 3 px) and in the
1 px inner rim. Tests whether starved cores lose product (p rim/core) and whether the enzyme could thin there (e)."""
import sys, numpy as np
from scipy import ndimage
for d in sys.argv[1:]:
    R = np.load(d + "/frames.npz")["render"][-1]; e, p, F = R[0], R[1], R[2]
    lab, n = ndimage.label(e > 0.5); out = []
    for j in range(1, n + 1):
        m = lab == j
        if m.sum() < 40: continue
        core = ndimage.binary_erosion(m, iterations=3); rim = m & ~ndimage.binary_erosion(m)
        if core.sum() < 3: continue
        out.append((e[core].mean(), e[rim].mean(), p[core].mean(), p[rim].mean(), F[core].mean(), F[rim].mean()))
    o = np.array(out)
    print(d, "bodies", len(o), "e core/rim %.2f/%.2f  p core/rim %.3f/%.3f  F core/rim %.3f/%.3f" % tuple(o.mean(0)) if len(o) else "none")
