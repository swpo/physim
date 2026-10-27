"""c56: do prey daughters regrow after a division?  python regrow.py frames.npz [chan] [A]
For each strict division (splits3 rule) report parent area at t, daughters' areas at t+1 and, following each daughter by
largest overlap, at t+5 and t+10 (None if it ended)."""
import sys, json, numpy as np
from scipy import ndimage
R = np.load(sys.argv[1])['render'].astype(np.float32); CH = int(sys.argv[2]) if len(sys.argv) > 2 else 0
A = int(sys.argv[3]) if len(sys.argv) > 3 else 30; T = len(R)
labs = [ndimage.label(f[CH] > 0.5)[0] for f in R]
def follow(t, m, n):
    for k in range(t + 1, t + n + 1):
        if k >= T: return None
        ov = labs[k][m]; ov = ov[ov > 0]
        if not ov.size: return None
        j = np.bincount(ov).argmax(); m = labs[k] == j
    return int(m.sum())
out = []
NF = int(sys.argv[4]) if len(sys.argv) > 4 else 10
for t in range(5, T - NF - 1):
    L0, L1 = labs[t], labs[t + 1]; ar0 = np.bincount(L0.ravel()); ar1 = np.bincount(L1.ravel())
    for i in range(1, len(ar0)):
        if ar0[i] < A: continue
        m = L0 == i; kids = [j for j in np.unique(L1[m]) if j > 0 and ar1[j] >= A and (L1[m] == j).sum() >= 10]
        if len(kids) < 2: continue
        if not all(np.bincount(L0[L1 == j][L0[L1 == j] > 0]).argmax() == i for j in kids): continue
        k5 = [follow(t + 1, L1 == j, 5) for j in kids]; k10 = [follow(t + 1, L1 == j, NF) for j in kids]
        if any(v is None for v in k5): continue
        out.append(dict(t=t, parent=int(ar0[i]), kids1=[int(ar1[j]) for j in kids], kids5=k5, kids10=k10))
ok = [o for o in out if all(v is not None for v in o['kids10'])]
r1 = [np.mean(o['kids1']) / o['parent'] for o in ok]; r10 = [np.mean(o['kids10']) / o['parent'] for o in ok]
print(json.dumps(dict(divisions=len(out), followed10=len(ok), kid_over_parent_t1=float(np.median(r1)) if ok else None,
                      kid_over_parent_t10=float(np.median(r10)) if ok else None,
                      regrown_to_half_or_more=int(sum(x >= 0.5 for x in r10)), regrown_to_075=int(sum(x >= 0.75 for x in r10)))))
