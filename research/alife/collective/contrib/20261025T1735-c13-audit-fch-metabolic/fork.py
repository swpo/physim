"""Fork analysis for metabolic micelles: bodies = components of (u + 1.6) > thr with >= 6 px.
For each pack: per recorded frame, body count and total body amphiphile. Then follow every body
present at frame f0 forward by maximal overlap (through its own splits: any overlapping child keeps
it alive) and report the fraction of those bodies whose lineage is gone at later frames.
usage: fork.py f0 pack_dir [pack_dir ...]"""
import sys, numpy as np
from scipy import ndimage

f0 = int(sys.argv[1]); thr = 0.8
for d in sys.argv[2:]:
    F = np.load(d + "/frames.npz"); R, rf = F["render"], list(F["render_f"])
    def lab(i):
        l, n = ndimage.label(R[i, 0] > thr)
        sz = np.bincount(l.ravel(), minlength=n + 1)
        keep = np.nonzero(sz >= 6)[0]; keep = keep[keep > 0]
        return l, keep
    i0 = min(range(len(rf)), key=lambda i: abs(rf[i] - f0))
    l0, k0 = lab(i0)
    alive = {int(k): (l0 == k) for k in k0}
    out = []
    for i in range(i0, len(rf)):
        li, ki = lab(i)
        body = np.isin(li, ki)
        mass = float((R[i, 0] * body).sum())
        new = {}
        for k, m in alive.items():
            ov = np.unique(li[m & body])
            ov = ov[ov > 0]
            if len(ov):
                new[k] = np.isin(li, ov)
        alive = new
        if (i - i0) % max(1, (len(rf) - i0) // 8) == 0 or i == len(rf) - 1:
            out.append(f"f{rf[i]}: bodies {len(ki)}, mass {mass:.0f}, founders alive {len(alive)}/{len(k0)}")
    print(d.split("/")[-2], " | ".join(out))
