"""K2 biomass share and K2-majority cell count per recorded frame, from labkit frames.npz of membrane_evo arms.
Cells = connected components of (K1+K2) > thr (periodic not merged; screening only)."""
import sys, numpy as np
from scipy import ndimage
def run(path, thr=0.05):
    F = np.load(path); R, rf = F["render"], F["render_f"]
    out = []
    for i in range(len(R)):
        k1, k2 = R[i, 0], R[i, 1]
        tot = k1.sum() + k2.sum()
        lab, n = ndimage.label((k1 + k2) > thr)
        if n:
            s1 = np.array(ndimage.sum(k1, lab, range(1, n + 1))); s2 = np.array(ndimage.sum(k2, lab, range(1, n + 1)))
            nk2 = int((s2 > s1).sum())
        else: nk2 = 0
        out.append((int(rf[i]), float(k2.sum() / tot) if tot > 0 else np.nan, n, nk2))
    return out
if __name__ == "__main__":
    for p in sys.argv[1:]:
        o = run(p)
        sh = np.array([x[1] for x in o])
        late = sh[-len(sh)//4:]
        print(p.split('/')[-2], "K2 share at frames", [round(x[1], 2) for x in o[::20]], "final", round(sh[-1], 3), "late mean", round(float(np.nanmean(late)), 3), "cells final", o[-1][2], "K2 cells", o[-1][3])
