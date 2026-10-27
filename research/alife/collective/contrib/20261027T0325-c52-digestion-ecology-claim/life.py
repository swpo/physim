"""Predator (c_b>0.5) body lifetimes by overlap tracking on labkit frames, and how much of each body lies inside prey (c_a>0.5).
usage: life.py frames.npz [chan 1] -> prints lifetime stats; line continues through the largest-overlap successor."""
import sys, numpy as np
from scipy import ndimage
R = np.load(sys.argv[1])['render']; ch = int(sys.argv[2]) if len(sys.argv) > 2 else 1
t0 = int(sys.argv[3]) if len(sys.argv) > 3 else 25
labs = []; inside = []
for f in R:
    L, n = ndimage.label(f[ch] > 0.5); a = np.bincount(L.ravel(), minlength=n + 1)
    keep = [i for i in range(1, n + 1) if a[i] >= 4]
    labs.append((L, set(keep)))
    for i in keep:
        inside.append(((f[1 - ch][L == i]) > 0.5).mean())
# lines: follow from each body at frame t0 through max-overlap successor (merges/splits allowed), count frames survived
T = len(R); L0, k0 = labs[t0]; lives = []
for i in k0:
    m = L0 == i; t = t0
    while t + 1 < T:
        L1, k1 = labs[t + 1]; ov = L1[m]; ov = ov[np.isin(ov, list(k1))]
        if ov.size == 0: break
        j = np.bincount(ov).argmax(); m = L1 == j; t += 1
    lives.append(t - t0)
lives = np.array(lives)
print(f'bodies at frame {t0}: {len(lives)}; frames survived median {np.median(lives):.0f}, to end {(t0+lives==T-1).sum()}, >=20 frames {(lives>=20).sum()}')
ins = np.array(inside); print(f'fraction of body inside other species: median {np.median(ins):.2f}, share mostly inside (>0.5) {(ins>0.5).mean():.2f}')
