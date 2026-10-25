"""Follow the damaged target and the same cell in the undamaged same-seed twin.
matter = K + L + wall (phase_membrane matter()); threshold 0.54 (0.35 of labkit's range ~1.54).
Target = twin component at frame 120 overlapping the cut (where dmg and twin differ).
Follow by max overlap with the previous mask (largest piece); report area, and L ring contrast
(mean L on the outer 2-px band of the component / mean L in its core)."""
import sys, numpy as np
from scipy import ndimage

def load(p):
    F = np.load(p); return F["matter"], F["render"], list(F["render_f"])

def follow(Xs, mask0, t0, t1):
    X, R, rf = Xs
    out, m = [], mask0
    for t in range(t0, t1):
        M = X[t] > 0.54
        lab, n = ndimage.label(M)
        ov = np.bincount(lab[m & (lab > 0)].ravel(), minlength=n + 1)
        if ov.sum() == 0:
            out.append((t, 0, None)); continue
        k = int(np.argmax(ov[1:]) + 1); m = lab == k
        inner = ndimage.binary_erosion(m, iterations=2)
        core = ndimage.binary_erosion(m, iterations=5)
        if t not in rf or not core.any():
            ring = None
        else:
            L = R[rf.index(t), 2]
            ring = L[m & ~inner].mean() / max(L[core].mean(), 1e-9)
        out.append((t, int(m.sum()), None if ring is None else round(float(ring), 2)))
    return out

D, T = load(sys.argv[1]), load(sys.argv[2])
diff = np.abs(D[0][120] - T[0][120]) > 1e-6
M = T[0][120] > 0.54
lab, n = ndimage.label(M)
k = np.bincount(lab[diff & (lab > 0)].ravel(), minlength=n + 1)[1:].argmax() + 1
m0 = lab == k
a0 = m0.sum()
fd, ft = follow(D, m0, 120, D[0].shape[0]), follow(T, m0, 120, T[0].shape[0])
print("pre-cut area", a0)
for (t, ad, rd), (_, at, rt) in list(zip(fd, ft))[::4]:
    print(f"frame {t}: damaged a={ad/a0:.2f} ring={rd} | twin a={at/a0:.2f} ring={rt} | ratio {ad/max(at,1):.2f}")
