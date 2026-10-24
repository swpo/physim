"""Damage ONE swimmer (not the largest clump): run to t_dmg, pick the median-size body, erase a disk
covering FRAC of its area through its centroid, then follow it. Also follows the same run undamaged.
usage: python damage1.py world.py out.png seed t_dmg frac
"""
import copy
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, ".")
from labkit.world import load_world  # noqa: E402

W = load_world(sys.argv[1]); out = sys.argv[2]; seed = int(sys.argv[3])
t_dmg, frac = float(sys.argv[4]), float(sys.argv[5])
dt = W.P["dt"]; H, Wd = W.META["size"]
s = W.init(seed, (H, Wd))
for _ in range(int(t_dmg / dt)):
    s = W.step(s)
rho = W.fields(s)[0]
lab, n = ndimage.label(rho > 0.35 * rho.max())
areas = ndimage.sum(np.ones_like(rho), lab, range(1, n + 1))
ok = [i for i in range(n) if 60 < areas[i] < 250]
k = ok[int(np.argsort(areas[ok])[len(ok) // 2])] + 1
cy, cx = ndimage.center_of_mass(rho, lab, k)
r = np.sqrt(frac * areas[k - 1] / np.pi)
y, x = np.mgrid[:H, :Wd]
mask = (np.hypot(y - cy, x - cx) <= r) & (lab == k)
ctrl = copy.deepcopy(s)
mass0 = rho[lab == k].sum()
s = W.damage(s, mask)
print(f"body area {areas[k-1]:.0f}px, erased {mask.sum()} px ({rho[mask].sum()/mass0:.0%} of its mass)")
rows = []
for st in (s, ctrl):
    tiles, c = [], (cy, cx)
    for j in range(10):
        f = W.fields(st)[0]
        # follow: nearest body centroid to previous
        lb, nn = ndimage.label(f > 0.35 * rho.max())
        if nn:
            cs = np.array(ndimage.center_of_mass(f, lb, range(1, nn + 1)))
            dd = np.abs(cs - np.array(c)); dd = np.minimum(dd, np.array([H, Wd]) - dd)
            c = tuple(cs[np.argmin(np.hypot(*dd.T))])
        crop = np.roll(np.roll(f, H // 2 - int(c[0]), 0), Wd // 2 - int(c[1]), 1)[H // 2 - 24:H // 2 + 24, Wd // 2 - 24:Wd // 2 + 24]
        tiles.append(np.pad(crop / rho.max(), 1, constant_values=1))
        for _ in range(int(6 / dt)):
            st = W.step(st)
    rows.append(np.concatenate(tiles, 1))
img = np.clip(np.concatenate(rows, 0), 0, 1)
Image.fromarray((img * 255).astype(np.uint8)).resize((img.shape[1] * 3, img.shape[0] * 3), Image.NEAREST).save(out)
print("rows: damaged (top), undamaged control (bottom); 6 t between tiles")
