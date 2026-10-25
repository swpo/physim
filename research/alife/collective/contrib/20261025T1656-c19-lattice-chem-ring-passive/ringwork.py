"""c19: does the M ring of lattice-chem do work? Per run (labkit frames.npz; render ch0 A, ch1 M, ch2 X), averaged over
the last 100 recorded frames: number of cells (components of box-smoothed A > 5, >= 6 px), total A, A per cell,
leak = mean A in the bath (smoothed A < 1, >= 3 px from any cell), and X inside cells vs in the bath.
usage: ringwork.py label=run_dir ..."""
import sys, numpy as np
from scipy import ndimage
for arg in sys.argv[1:]:
    lab, d = arg.split("="); R = np.load(d + "/frames.npz")["render"].astype(np.float64)
    rows = []
    for i in range(len(R) - 100, len(R), 5):
        A, M, X = R[i, 0], R[i, 1], R[i, 2]
        As = ndimage.uniform_filter(A, 3, mode="wrap"); cell = As > 5
        L, n = ndimage.label(cell); a = np.bincount(L.ravel())[1:]; nc = int((a >= 6).sum())
        bath = ~ndimage.binary_dilation(cell, iterations=3) & (As < 1)
        rows.append((nc, A.sum(), A.sum() / max(nc, 1), A[bath].mean(), X[cell].mean(), X[bath].mean(), M[cell].sum() / max(M.sum(), 1)))
    r = np.mean(rows, 0)
    print(f"{lab}: cells {r[0]:.1f}, total A {r[1]:.0f}, A per cell {r[2]:.0f}, bath A {r[3]:.3f}, X in cells {r[4]:.2f} vs bath {r[5]:.2f}, M fraction inside cell masks {r[6]:.2f}")
