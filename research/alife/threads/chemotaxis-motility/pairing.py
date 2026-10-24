"""Pursuit-pair statistic from a pack's frames.npz (render channels: prey, predator, ...).

For each recorded frame: segment predator bodies (q > 0.3 of max) and count the fraction
whose 4-px dilation touches prey (p > 0.3 of max). Null: the same with the prey field
rolled by a random offset (chance contact at the observed densities).
usage: python pairing.py pack_dir [pack_dir ...]
"""
import sys

import numpy as np
from scipy import ndimage

rng = np.random.default_rng(0)
st = ndimage.generate_binary_structure(2, 1)
for d in sys.argv[1:]:
    F = np.load(f"{d}/frames.npz")["render"].astype(np.float32)
    T = len(F)
    fr, nul, nq = [], [], []
    for f in range(T // 2, T):
        p, q = F[f, 0], F[f, 1]
        pm = p > 0.3 * max(p.max(), 1e-9)
        lab, n = ndimage.label(q > 0.3 * max(q.max(), 1e-9))
        if n == 0:
            continue
        dil = ndimage.binary_dilation(lab > 0, st, iterations=4)
        lab_d = ndimage.label(dil)[0]
        ids = np.unique(lab_d[lab > 0])
        touch = [pm[lab_d == i].any() for i in ids]
        pr = np.roll(pm, (rng.integers(p.shape[0]), rng.integers(p.shape[1])), (0, 1))
        touch0 = [pr[lab_d == i].any() for i in ids]
        fr.append(np.mean(touch)); nul.append(np.mean(touch0)); nq.append(len(ids))
    print(f"{d}: late-half predator bodies ~{np.mean(nq):.1f}; touching prey {np.mean(fr):.2f} "
          f"(shuffled-prey null {np.mean(nul):.2f})")
