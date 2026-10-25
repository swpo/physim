"""Share of the surfactant in the ring (|d| <= 0.5 px from phi = 0), core (d <= -1.5) and outside (2 <= d <= 4)
that each source region made (three-way split world; channels 2, 3, 4). usage: rimshare.py frames.npz"""
import sys, numpy as np
from scipy import ndimage
F = np.load(sys.argv[1]); R = F["render"].astype(np.float32); rf = list(F["render_f"])
H, W = R.shape[2:]
acc = {k: np.zeros(3) for k in ("rim", "core", "out")}
for k, f in enumerate(rf):
    if f < 20:
        continue
    phi = R[k, 0]; ins = phi > 0
    t = np.tile(ins, (3, 3)); sl = (slice(H, 2 * H), slice(W, 2 * W))
    d = np.where(t, -(ndimage.distance_transform_edt(t) - 0.5), ndimage.distance_transform_edt(~t) - 0.5)[sl]
    for name, m in (("rim", np.abs(d) <= 0.5), ("core", d <= -1.5), ("out", (d >= 2) & (d <= 4))):
        acc[name] += [R[k, c][m].sum() for c in (2, 3, 4)]
for name, v in acc.items():
    print(f"{name:5s}: rod-made {v[0]/v.sum():.2f}, interface-made {v[1]/v.sum():.2f}, far-bath-made {v[2]/v.sum():.2f}")
