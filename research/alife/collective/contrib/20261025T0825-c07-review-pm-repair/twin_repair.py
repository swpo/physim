"""Branched same-seed twin repair test for phase_membrane.
usage: python twin_repair.py seed out_prefix [frac]
Runs to T_CUT, picks mature round cells (phi>1/2 component, area within 0.7-1.5x the median, aspect < 1.3,
not touching another cell within 3 px), erases a disk centred on the wall that removes ~frac of the cell
(S=1, K=L=phi=0 = bath; matter leaves), then runs the damaged copy and an undamaged copy (deep copy of the
state at T_CUT) to T_END. The target is followed in each copy by maximal overlap frame to frame.
Reports area(damaged)/area(twin) of the same cell, the L rim/core ratio of each, and when each divides."""
import copy, json, sys
import numpy as np
from scipy import ndimage
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit.world import load_world
W = load_world("threads/autopoiesis/worlds/phase_membrane/world.py")
seed, pre = int(sys.argv[1]), sys.argv[2]
frac = float(sys.argv[3]) if len(sys.argv) > 3 else 0.35
T_CUT, T_END, DT, N = 6000, 7600, 20, 128
s = W.init(seed, (N, N))
for t in range(T_CUT):
    s = W.step(s)
lab, n = ndimage.label(s["phi"] > 0.5)
areas = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
med = np.median(areas)
cands = []
for i in range(1, n + 1):
    m = lab == i
    a = m.sum()
    if not (0.7 * med <= a <= 1.5 * med):
        continue
    ys, xs = np.nonzero(m)
    if ys.min() < 3 or xs.min() < 3 or ys.max() > N - 4 or xs.max() > N - 4:
        continue
    cov = np.cov(np.vstack([ys, xs]))
    ev = np.linalg.eigvalsh(cov)
    asp = np.sqrt(ev[1] / max(ev[0], 1e-9))
    near = ndimage.binary_dilation(m, iterations=4) & (lab > 0) & ~m
    if asp < 1.3 and not near.any():
        cands.append((asp, i, a, ys.mean(), xs.mean()))
cands.sort()
res = []
yy, xx = np.mgrid[:N, :N]


def ring(st, m):
    L = st["L"]; inner = ndimage.binary_erosion(m, iterations=4)
    rim = m & ~inner
    return float(L[rim].mean() / max(L[inner].mean(), 1e-9)) if inner.any() and rim.any() else None


for asp, i, a, cy, cx in cands[:2]:
    m0 = lab == i
    R = np.sqrt(a / np.pi)
    # disk centred on the wall (+x side), radius chosen to remove ~frac of the cell
    for rr in np.arange(2, 2 * R, 0.5):
        hole = (yy - cy) ** 2 + (xx - (cx + R)) ** 2 <= rr ** 2
        if (hole & m0).sum() >= frac * a:
            break
    sd, st = copy.deepcopy(s), copy.deepcopy(s)
    for k in ("K", "L", "phi"):
        sd[k][hole] = 0
    sd["S"][hole] = 1
    erased = float((hole & m0).sum() / a)
    traj = []
    md, mt = (sd["phi"] > 0.5) & m0, m0.copy()
    for t in range(T_CUT, T_END + 1):
        if (t - T_CUT) % DT == 0:
            row = {"t": t}
            for name, st_, mprev in (("dam", sd, md), ("twin", st, mt)):
                l2, n2 = ndimage.label(st_["phi"] > 0.5)
                ov = np.bincount(l2[mprev & (l2 > 0)], minlength=n2 + 1)
                if ov.sum() == 0:
                    row[name] = None; continue
                j = ov.argmax(); mm = l2 == j
                # count pieces of the previous mask: >= 2 large overlaps = divided
                big = (ov[1:] >= 0.2 * mprev.sum()).sum()
                row[name] = {"area": int(mm.sum()), "ring": ring(st_, mm), "pieces": int(big)}
                if name == "dam": md = mm
                else: mt = mm
            traj.append(row)
        sd = W.step(sd); st = W.step(st)
    res.append({"cell": int(i), "area0": int(a), "aspect": round(float(asp), 2), "erased": round(erased, 3), "traj": traj})
json.dump(res, open(pre + ".json", "w"))
for r in res:
    print("cell", r["cell"], "area0", r["area0"], "aspect", r["aspect"], "erased", r["erased"])
    for row in r["traj"][::10]:
        d, w = row["dam"], row["twin"]
        print("  t", row["t"], "dam", d and (d["area"], d["ring"] and round(d["ring"], 2), d["pieces"]), "twin", w and (w["area"], w["ring"] and round(w["ring"], 2), w["pieces"]),
              "ratio", d and w and round(d["area"] / w["area"], 2))
