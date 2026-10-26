# (c26 review) droplets by dominant allele over time, from a labkit pack's recorded render frames
import sys, numpy as np
from scipy import ndimage
z = np.load(sys.argv[1]); R = z["render"]; f = z["render_f"]; spf, dt = 200, 0.5
out = []
for fr, X in zip(f, R):
    phi = X[0]; A = X[2:6]
    lab, n = ndimage.label(phi > 0.0)
    cnt = [0, 0, 0, 0]
    for j in range(1, n + 1):
        m = lab == j
        if m.sum() < 20: continue
        cnt[int(np.argmax(A[:, m].sum(1)))] += 1
    out.append([fr * spf * dt] + cnt)
out = np.array(out); np.savetxt(sys.argv[2], out, fmt="%g", header="t allele0 allele1 allele2 allele3 (droplets >= 20 px by dominant allele)")
for r in out[::12]: print(*r.astype(int))
