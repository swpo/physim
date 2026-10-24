"""Branch-point test of mutation operators on mca-MIRd (committee r2 design).

python branch_test.py world.py STATE.npz OUT_PREFIX OP EFF [STEPS]
  OP = whole : flip the cell's whole territory (all matter assigned to its A0 core, dilated 2 px)
  OP = old   : sprint-2 operator (A0 > 0.3 component of that cell, dilated 4 px)
Territories: A0 cores (A0 > 0.3, area >= 30) inside M > 0.03; every matter pixel goes to its nearest core
(Voronoi within matter); a territory counts if >= 100 px. The target is the most isolated mature territory.
Mutation is off during the run. Readouts every 50 steps (5 t) on territories:
  p = allele-1 mass fraction of each territory; carriers p > 0.5; pure1 p >= 0.9; mixed 0.1 < p < 0.9.
Writes OUT_PREFIX.json.
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from labkit.world import load_world  # noqa: E402


def territories(A):
    M = A.sum(0)
    core_lab, n = ndimage.label(A[0] > 0.3)
    if n == 0:
        return np.zeros(M.shape, int), 0
    areas = ndimage.sum(np.ones_like(M), core_lab, range(1, n + 1))
    keep = np.zeros(n + 1, bool)
    keep[1:] = areas >= 30
    core_lab = np.where(keep[core_lab], core_lab, 0)
    _, (iy, ix) = ndimage.distance_transform_edt(core_lab == 0, return_indices=True)
    terr = core_lab[iy, ix] * (M > 0.03)
    ids = np.unique(terr[terr > 0])
    out = np.zeros_like(terr)
    k = 0
    for i in ids:
        m = terr == i
        if m.sum() >= 100:
            k += 1
            out[m] = k
    return out, k


def readout(s):
    terr, n = territories(s["A"])
    M = s["A"].sum(0)
    ps = []
    for i in range(1, n + 1):
        m = terr == i
        ps.append(float((s["a"][m] * M[m]).sum() / max(M[m].sum(), 1e-9)))
    ps = np.array(ps) if ps else np.zeros(0)
    tot1 = float((s["a"] * M).sum())
    return dict(n=int(n), carriers=int((ps > 0.5).sum()), pure1=int((ps >= 0.9).sum()),
                mixed=int(((ps > 0.1) & (ps < 0.9)).sum()), mass1=tot1, frac1=tot1 / max(float(M.sum()), 1e-9),
                carrier_purity=float(ps[ps > 0.5].mean()) if (ps > 0.5).any() else None)


if __name__ == "__main__":
    W = load_world(sys.argv[1]); st = np.load(sys.argv[2]); pre = sys.argv[3]; op = sys.argv[4]; W.EFF = float(sys.argv[5])
    steps = int(sys.argv[6]) if len(sys.argv) > 6 else 5000
    W.MU_CELL = 0.0
    H, Wd = st["F"].shape
    s = W.init(0, (H, Wd))
    s["A"], s["F"], s["a"] = st["A"].copy(), st["F"].copy(), np.zeros_like(st["a"])
    terr, n = territories(s["A"])
    # most isolated mature territory: largest distance to any other territory
    best, bestd = None, -1
    for i in range(1, n + 1):
        m = terr == i
        d = ndimage.distance_transform_edt(~m)
        others = (terr > 0) & ~m
        dmin = float(d[others].min()) if others.any() else 1e9
        if dmin > bestd:
            best, bestd = i, dmin
    if best is None:
        print(json.dumps(dict(error="no territory"))); sys.exit()
    tm = terr == best
    M = s["A"].sum(0)
    if op == "whole":
        mask = ndimage.binary_dilation(tm, iterations=2)
    else:
        lab, _ = ndimage.label(s["A"][0] > 0.3)
        ids = np.unique(lab[tm & (lab > 0)])
        k = ids[np.argmax([((lab == j) & tm).sum() for j in ids])]
        mask = ndimage.binary_dilation(lab == k, iterations=4)
    s["a"] = np.where(mask, 1.0, s["a"])
    flipped = float((M * s["a"] * tm).sum() / max((M * tm).sum(), 1e-9))
    series = []
    for t in range(steps + 1):
        if t % 50 == 0:
            r = readout(s); r["t"] = t; series.append(r)
        if t < steps:
            s = W.step(s)
    out = dict(state=sys.argv[2], op=op, eff=W.EFF, target_area=int(tm.sum()), isolation=bestd,
               flipped_mass_fraction=flipped, n_territories0=n, series=series)
    json.dump(out, open(pre + ".json", "w"))
    fin = series[-1]
    print(json.dumps(dict(op=op, eff=W.EFF, flipped=round(flipped, 3), area=int(tm.sum()), iso=round(bestd, 1),
                          final_pure1=fin["pure1"], final_carriers=fin["carriers"], final_mixed=fin["mixed"],
                          max_pure1=max(x["pure1"] for x in series), final_frac1=round(fin["frac1"], 4), n=fin["n"])))
