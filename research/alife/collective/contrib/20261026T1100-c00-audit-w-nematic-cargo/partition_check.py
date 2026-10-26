"""Is the held cargo a kinetic barrier effect or an equilibrium partition? Per body-frame: Boltzmann factor
B = <exp(-kappa s)>_inside / <exp(-kappa s)>_outside (what the coupling alone would give at equilibrium with no
source), and the ring maximum of kappa*s minus the inside level (the barrier height). EDT signed distance,
inside d<=-1.5 px, outside 2..5 px, ring |d|<=1. usage: partition_check.py frames.npz [kappa=20]"""
import sys, numpy as np
from scipy import ndimage
F = np.load(sys.argv[1]); R = F["render"].astype(np.float64); rf = list(F["render_f"]); kap = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
B, bar, sin, sout, sring = [], [], [], [], []
for k, f in enumerate(rf):
    if f < 20: continue
    phi, s = R[k, 0], R[k, 2]; ins = phi > 0
    t = np.tile(ins, (3, 3)); H, W = phi.shape; sl = (slice(H, 2 * H), slice(W, 2 * W))
    d = np.where(t, -(ndimage.distance_transform_edt(t) - 0.5), ndimage.distance_transform_edt(~t) - 0.5)[sl]
    lab, n = ndimage.label(t); _, (iy, ix) = ndimage.distance_transform_edt(lab == 0, return_indices=True)
    near = lab[iy, ix][sl]; labc = lab[sl]
    for j in np.unique(labc[labc > 0]):
        if (labc == j).sum() < 20: continue
        o = near == j; a, b, r = o & (d <= -1.5), o & (d >= 2) & (d <= 5), o & (np.abs(d) <= 1)
        if a.sum() < 2 or b.sum() < 6: continue
        B.append(np.exp(-kap * s[a]).mean() / np.exp(-kap * s[b]).mean())
        bar.append(kap * (np.percentile(s[r], 90) - s[a].mean())); sin.append(s[a].mean()); sout.append(s[b].mean()); sring.append(np.percentile(s[r], 90))
B = np.array(B)
print(f"{sys.argv[1].split('nematic-cargo/')[-1]}: body-frames {len(B)}; Boltzmann in/out (coupling alone, no source): median {np.median(B):.3g}, share > 1: {(B > 1).mean():.2f}; "
      f"median s inside {np.median(sin):.3f}, ring(p90) {np.median(sring):.3f}, outside {np.median(sout):.3f}; median barrier kappa*(s_ring - s_in) {np.median(bar):.2f}")
