"""Per-species droplet counts per frame (prey a > 0.5, predator b > 0.5, components >= 6 px, periodic-agnostic)."""
import sys, numpy as np
from scipy import ndimage
for path in sys.argv[1:]:
    z = np.load(path); F = z["render"]
    t = z["render_f"] * 100.0
    print(path, F.shape)
    for i in range(0, len(F), 10):
        out = []
        for c in (0, 1):
            lab, n = ndimage.label(F[i, c] > 0.5)
            sz = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
            out.append(int((sz >= 6).sum()))
        print(f"  t={t[i]:.0f} prey {out[0]} pred {out[1]}")
