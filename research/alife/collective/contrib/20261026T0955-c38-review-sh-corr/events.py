"""Classify molecule-count changes in a labkit run of the SH world: fission (one molecule's spots end up in >= 2
molecules that stay apart for HOLD frames), fusion, nucleation (a molecule with no spot overlap with the previous
frame) and loss. Spots = smoothed u > 0.6; molecules = spots joined within 2.2 units (dilation), periodic labels.
usage: events.py frames.npz L [HOLD=10]"""
import sys, numpy as np
from scipy import ndimage as ndi
M = np.load(sys.argv[1])["matter"].astype(np.float32); L = float(sys.argv[2]); HOLD = int(sys.argv[3]) if len(sys.argv) > 3 else 10
T, H, W = M.shape; dx = L / W; it = max(1, int(round(2.2 / dx)))
def plabel(mask):
    lab, n = ndi.label(mask)
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for x, y in zip(a, b):
            if x and y and x != y: lab[lab == y] = x
    u = np.unique(lab); u = u[u > 0]; out = np.zeros_like(lab)
    for i, k in enumerate(u): out[lab == k] = i + 1
    return out, len(u)
def mols(f):
    sp = ndi.gaussian_filter(M[f], 1.0, mode="wrap") > 0.6
    big = np.pad(sp, it, mode="wrap"); big = ndi.binary_dilation(big, iterations=it)[it:-it, it:-it]
    lab, n = plabel(big); return lab * sp, n, sp
labs = [mols(f) for f in range(T)]
fis = []; nuc = 0; fus = 0; loss = 0; nm = [l[1] for l in labs]
for f in range(T - 1):
    a, na, _ = labs[f]; b, nb, _ = labs[f + 1]
    pairs = {}
    m = (a > 0) & (b > 0)
    for x, y in zip(a[m], b[m]): pairs.setdefault(int(x), set()).add(int(y))
    hit_b = set().union(*pairs.values()) if pairs else set()
    nuc += sum(1 for y in range(1, nb + 1) if y not in hit_b)
    for x, ys in pairs.items():
        if len(ys) >= 2:
            # do the children stay apart? follow two largest children forward
            ys = sorted(ys, key=lambda y: -(b == y).sum())[:2]
            m1, m2 = (b == ys[0]), (b == ys[1]); ok = True
            for g in range(f + 2, min(T, f + 1 + HOLD)):
                c = labs[g][0]; l1 = c[m1 & (c > 0)]; l2 = c[m2 & (c > 0)]
                if len(l1) == 0 or len(l2) == 0: ok = False; break
                k1, k2 = np.bincount(l1).argmax(), np.bincount(l2).argmax()
                if k1 == k2: ok = False; break
                m1, m2 = c == k1, c == k2
            if ok and f + 1 + HOLD <= T:
                sl = labs[f + 1][2]; n1 = plabel(sl & (b == ys[0]))[1]; n2 = plabel(sl & (b == ys[1]))[1]
                fis.append((f + 1, n1, n2))
    inv = {}
    for x, ys in pairs.items():
        for y in ys: inv.setdefault(y, set()).add(x)
    fus += sum(1 for y, xs in inv.items() if len(xs) >= 2)
print(f"frames {T}; molecules first/last {nm[0]}/{nm[-1]}, frame 25 {nm[25]}; fission events (children apart >= {HOLD} frames): {len(fis)}; fusions {fus}; nucleations {nuc}")
late = [e for e in fis if e[0] >= 50]
print(f"after frame 50 (t >= 100): {len(late)} fissions; with >= 2 spots in both children: {sum(1 for e in late if min(e[1], e[2]) >= 2)}; molecules every 50 frames: {nm[::50]}")
for e in late: print("  fission at frame", e[0], "children spots", e[1], e[2])
