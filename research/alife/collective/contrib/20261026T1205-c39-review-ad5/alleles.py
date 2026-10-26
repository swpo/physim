"""(c39) Dominant catalyst allele of every droplet (phi > 0 component >= 20 px) at render frames; prints counts per allele
over time. usage: alleles.py frames.npz"""
import sys, numpy as np
from scipy import ndimage
F = np.load(sys.argv[1]); R = F["render"].astype(np.float32); rf = list(F["render_f"])
for k in range(0, len(rf), max(1, len(rf) // 8)):
    lab, n = ndimage.label(R[k, 0] > 0); cnt = [0, 0, 0, 0]
    for j in range(1, n + 1):
        m = lab == j
        if m.sum() < 20: continue
        cnt[int(np.argmax([R[k, 2 + a][m].mean() for a in range(4)]))] += 1
    print("frame", rf[k], "droplets by dominant allele a0..a3:", cnt)
