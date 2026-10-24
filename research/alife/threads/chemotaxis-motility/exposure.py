"""Predator exposure per allele in evopursuit packs (render channels: preyA, preyB, predator, n).

exposure_k = sum(k * q) / sum(k) over frames where both alleles hold >= 5% of prey mass:
the predator density an average unit of allele k sits in. If the evasion allele works, exposure_B < exposure_A.
usage: python exposure.py pack_seed_dir [...]
"""
import sys

import numpy as np

for d in sys.argv[1:]:
    F = np.load(f"{d}/frames.npz")["render"].astype(np.float32)
    eA, eB, nf = [], [], 0
    for A, B, q, _ in F:
        sA, sB = A.sum(), B.sum()
        if min(sA, sB) < 0.05 * (sA + sB) or q.sum() == 0:
            continue
        eA.append((A * q).sum() / sA)
        eB.append((B * q).sum() / sB)
        nf += 1
    if nf:
        print(f"{d}: {nf} frames with both alleles; exposure A {np.mean(eA):.4f}, B {np.mean(eB):.4f}, "
              f"B/A {np.mean(eB) / np.mean(eA):.2f}, B<A in {np.mean(np.array(eB) < np.array(eA)):.0%} of frames")
    else:
        print(f"{d}: no frames with both alleles")
