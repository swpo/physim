"""(c50) Consumer bodies (q > 0.5, area >= 6) vs prey (prey channel > 0.5): share touching prey (within 1 px), share of
consumer area inside prey, free consumers (not within 2 px of prey), per rendered frame t >= 2000; and in the fork run
the consumer count by time. usage: attach.py frames.npz [fork.npz]"""
import sys, numpy as np
from scipy import ndimage as ndi
R = np.load(sys.argv[1])["render"].astype(np.float32); T = len(R)
tch, ins, free, n = [], [], [], []
for i in range(T // 6, T):
    prey = R[i, 0] > 0.5; q = R[i, 1] > 0.5
    lab, k = ndi.label(q); a = np.bincount(lab.ravel())
    near1 = ndi.binary_dilation(prey, iterations=1); near2 = ndi.binary_dilation(prey, iterations=2)
    for j in range(1, k + 1):
        if a[j] < 6: continue
        m = lab == j; n.append(1)
        tch.append((m & near1).any()); ins.append((m & prey).sum() / m.sum()); free.append(not (m & near2).any())
print(f"consumer bodies counted over frames {T // 6}..{T - 1}: {len(n)} body-frames; touching prey {np.mean(tch):.2f}; "
      f"mean share of area inside prey {np.mean(ins):.2f}; free (>2 px from prey) {np.mean(free):.3f}")
if len(sys.argv) > 2:
    F = np.load(sys.argv[2])["render"].astype(np.float32); ts = np.linspace(0, 8000, len(F))
    for i in range(len(F)):
        if 2700 <= ts[i] <= 3500:
            lab, k = ndi.label(F[i, 1] > 0.5); a = np.bincount(lab.ravel())
            print(f"  fork t={ts[i]:.0f}: consumers {int((a[1:] >= 6).sum())}, prey bodies {ndi.label(F[i,0] > 0.5)[1]}, max q {F[i,1].max():.2f}")
