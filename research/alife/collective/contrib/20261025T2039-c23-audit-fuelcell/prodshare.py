"""Who makes the surfactant, and how much ring does it give. For labkit frames.npz of the fuel-cell world:
share of the s source ks(1+phi)/2 that lies in bodies (phi>0) and within 3 px of them; median s on the
interface band; bath s; and the fuel gate factor D/Df = 1/(1+5 (s/0.45)^12) at the rim."""
import sys, numpy as np
from scipy import ndimage
for fn in sys.argv[1:]:
    z = np.load(fn); R = z['render']; sh, rim, bath, gate = [], [], [], []
    for i in range(30, len(R), 10):
        phi, sf = R[i, 0].astype(float), R[i, 2].astype(float); body = phi > 0
        src = 0.5 * (1 + np.clip(phi, -1, 1)); near = ndimage.binary_dilation(body, iterations=3)
        sh.append((src[body].sum() / src.sum(), src[near].sum() / src.sum()))
        band = ndimage.binary_dilation(body, iterations=2) & (np.abs(phi) < 0.3)
        rim.append(np.median(sf[band])); bath.append(np.median(sf[~ndimage.binary_dilation(body, iterations=6)]))
        gate.append(np.median(1 / (1 + 5 * (sf[band] / 0.45) ** 12)))
    sh = np.array(sh)
    print(f"{fn}: share of a ks(1+phi)/2 source in bodies {sh[:,0].mean():.2f}, within 3 px {sh[:,1].mean():.2f}; rim s {np.mean(rim):.3f}; bath s {np.mean(bath):.3f}; rim gate D/Df {np.mean(gate):.3f}")
