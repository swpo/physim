"""K2 share of catalyst biomass inside cells (sum K2 / sum (K1+K2)) per arm and seed at t = 8000 (mutations on),
20000, 30000, 40000, and the departure of each arm from its identical-event twin at the end; also the number of
cells (phi>1/2 components from the wall channel are not available, so: components of K1+K2 > 0.05)."""
import numpy as np
from scipy import ndimage
for s in (31, 32, 33):
    out = {}
    for a in ("up", "twin", "down"):
        F = np.load(f"arm_{a}/seed{s}/frames.npz"); R = F["render"]; tf = F["render_f"] * 250
        row = []
        for T in (8000, 20000, 30000, 40000):
            i = int(np.argmin(abs(tf - T))); k1, k2 = R[i, 0].sum(), R[i, 1].sum()
            n = ndimage.label((R[i, 0] + R[i, 1]) > 0.05)[1]
            row.append((k2 / max(k1 + k2, 1e-9), n))
        out[a] = row
    print(f"seed {s}: " + " | ".join(f"{a}: " + " ".join(f"{sh:.2f}({n})" for sh, n in out[a]) for a in out))
    print(f"   end departure from twin: up {out['up'][-1][0]-out['twin'][-1][0]:+.2f}, down {out['down'][-1][0]-out['twin'][-1][0]:+.2f}")
