"""Surfactant by phi band (pooled over recorded frames from frame f0): interface |phi|<0.5, interior phi>0.6,
near outside phi<-0.8 within 4*scale px of a droplet. Prints interface/interior and interface/outside.
usage: bandring.py frames.npz [f0=100] [scale=1]"""
import sys, numpy as np
from scipy import ndimage
F = np.load(sys.argv[1]); R = F["render"]; f0 = int(sys.argv[2]) if len(sys.argv) > 2 else 100
sc = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; rf = list(F["render_f"])
I = J = O = 0.0; nI = nJ = nO = 0
for i in range(len(R)):
    if rf[i] < f0: continue
    phi, s = R[i, 0], R[i, 2]
    band = np.abs(phi) < 0.5; core = phi > 0.6
    near = ndimage.binary_dilation(phi > 0, iterations=int(round(4 * sc))) & (phi < -0.8)
    I += s[band].sum(); nI += band.sum(); J += s[core].sum(); nJ += core.sum(); O += s[near].sum(); nO += near.sum()
print(f"{sys.argv[1]}: interface {I/nI:.3f}, interior {J/max(nJ,1):.3f}, near outside {O/nO:.3f}; interface/interior {I/nI/(J/max(nJ,1)):.2f}, interface/outside {I/nI/(O/nO):.2f}")
