"""(c34) Kind of each rod: fA = sum sA / sum (sA + sB) over the rod and a 2 px shell around it (phi > 0 dilated by 2),
A if fA > 0.8, B if fA < 0.2, mixed otherwise; counts every 10 render frames, and the purity (fraction of rods that
are A or B). usage: kinds.py frames.npz [label]"""
import sys, numpy as np
from scipy import ndimage
F = np.load(sys.argv[1]); R = F["render"].astype(np.float32); rf = list(F["render_f"])
lab0 = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]
print(f"{lab0}: frame  rods  A  B  mixed  share_A_of_pure")
for k in range(0, len(rf), 10):
    ins = R[k, 0] > 0
    lab, n = ndimage.label(ins)
    if n == 0:
        print(f"  {rf[k]:4d}  0"); continue
    big = ndimage.grey_dilation(lab, size=(5, 5))
    sizes = ndimage.sum(ins, lab, range(1, n + 1))
    a = ndimage.sum(R[k, 2], big, range(1, n + 1)); b = ndimage.sum(R[k, 3], big, range(1, n + 1))
    keep = sizes >= 12; f = a[keep] / np.maximum(a[keep] + b[keep], 1e-12)
    nA, nB = int((f > 0.8).sum()), int((f < 0.2).sum()); nm = int(keep.sum()) - nA - nB
    print(f"  {rf[k]:4d}  {int(keep.sum()):3d}  {nA:3d} {nB:3d}  {nm:3d}  {nA / max(nA + nB, 1):.2f}")
