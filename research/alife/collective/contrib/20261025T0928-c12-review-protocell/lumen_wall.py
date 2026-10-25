"""Lumen / wall / outside solute per frame: wall = (u+1.6) > thr, lumens = enclosed components of the complement
(the author's contrast.py wrap_label), outside = the largest complement component. A barrier gives lumen > wall;
a source in the wall with slow diffusion gives wall > lumen. Usage: lumen_wall.py frames.npz"""
import sys, numpy as np
sys.path.insert(0, "collective/contrib/20261025T0726-c03-fch-protocell")
from contrast import wrap_label
F = np.load(sys.argv[1]); X = F["render"]; tf = F["render_f"]
print("frame  lumen/outside  wall/outside  lumen/wall  n_lumens")
for i in list(range(10, X.shape[0], 15)) + [X.shape[0] - 1]:
    u, c = X[i, 0], X[i, 1]; wall = u > 0.8; lab = wrap_label(~wall)
    ids, cnt = np.unique(lab[lab > 0], return_counts=True); out = ids[np.argmax(cnt)]
    lum = (lab > 0) & (lab != out); o = lab == out
    if not lum.any(): continue
    print(f"{tf[i]:5d}  {c[lum].mean()/c[o].mean():8.2f}  {c[wall].mean()/c[o].mean():8.2f}  {c[lum].mean()/c[wall].mean():8.2f}  {len(ids)-1}")
