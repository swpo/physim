"""K2 biomass share K2/(K1+K2) over time, and cells carrying mostly K2, from a labkit pack's frames.npz
(render channels: 0 K1, 1 K2, 2 L, 3 wall). Usage: share.py pack_dir [pack_dir ...]"""
import sys, numpy as np
from scipy import ndimage

for d in sys.argv[1:]:
    F = np.load(d + "/frames.npz")
    R, rf = F["render"], list(F["render_f"])
    row = []
    for i in range(0, len(rf), max(1, len(rf) // 8)):
        k1, k2 = R[i, 0], R[i, 1]
        tot = k1.sum() + k2.sum()
        lab, n = ndimage.label(k1 + k2 > 0.05)
        s1 = ndimage.sum(k1, lab, range(1, n + 1)); s2 = ndimage.sum(k2, lab, range(1, n + 1))
        n2 = int(np.sum(s2 > s1)); n1 = int(np.sum(s1 >= s2))
        row.append(f"f{rf[i]}:{k2.sum() / max(tot, 1e-9):.2f}({n1}/{n2})")
    k1, k2 = R[-1, 0], R[-1, 1]
    lab, n = ndimage.label(k1 + k2 > 0.05)
    s1 = ndimage.sum(k1, lab, range(1, n + 1)); s2 = ndimage.sum(k2, lab, range(1, n + 1))
    mixed = int(np.sum((np.minimum(s1, s2) / np.maximum(np.maximum(s1, s2), 1e-9)) > 0.1))
    print(d.split("evo/")[-1], "share(K1cells/K2cells):", " ".join(row),
          f"| final share {k2.sum() / max((k1 + k2).sum(), 1e-9):.2f}, cells {n}, mixed(>10% minority) {mixed}")
