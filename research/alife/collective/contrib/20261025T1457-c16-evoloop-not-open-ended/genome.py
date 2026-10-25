"""Read each evoloop loop's genome: the core ring (Chebyshev distance 2 from the loop's square hole), read clockwise,
canonicalised as the lexicographically smallest rotation (the genome circulates, so rotations are the same genotype).
Only loops whose hole is a full square with an intact sheath ring at distances 1 and 3 are read."""
import numpy as np
from evo_track import periodic_label

def ring_coords(i0, j0, n, d):
    """Clockwise square ring at Chebyshev distance d around the n x n hole with top-left (i0, j0)."""
    a, b = i0 - d, j0 - d; s = n + 2 * d
    top = [(a, b + k) for k in range(s)]; right = [(a + k, b + s - 1) for k in range(1, s)]
    bot = [(a + s - 1, b + s - 1 - k) for k in range(1, s)]; left = [(a + s - 1 - k, b) for k in range(1, s - 1)]
    return top + right + bot + left

def canon(seq):
    s = ''.join(map(str, seq)); return min(s[k:] + s[:k] for k in range(len(s)))

def genomes(g):
    L = g.shape[0]; lab = periodic_label(g == 0)
    area = np.bincount(lab.ravel()); area[0] = 0; area[np.argmax(area)] = 0
    out = []
    for h in np.nonzero(area >= 1)[0]:
        ii, jj = np.nonzero(lab == h)
        if ii.max() - ii.min() > L / 2 or jj.max() - jj.min() > L / 2: continue  # skip seam-crossing holes
        n = ii.max() - ii.min() + 1
        if jj.max() - jj.min() + 1 != n or n * n != len(ii): continue  # not a full square
        i0, j0 = ii.min(), jj.min()
        sh1 = [g[i % L, j % L] for i, j in ring_coords(i0, j0, n, 1)]
        if any(v != 2 for v in sh1): continue
        core = [g[i % L, j % L] for i, j in ring_coords(i0, j0, n, 2)]
        if any(v in (0, 2, 8) for v in core) and sum(v == 0 for v in core) > len(core): continue
        out.append({"side": int(n), "pos": (int(i0), int(j0)), "genome": canon(core)})
    return out
