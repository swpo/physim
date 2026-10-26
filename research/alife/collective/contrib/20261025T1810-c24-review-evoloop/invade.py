"""Invasion assay for evoloop: from a side-11 population at t0, plant ONE loop of core side m_inv
(hole side m_inv-4) in an empty window and continue; the unplanted twin continues the same state.
Census of hole sides every `every` steps. Usage: invade.py <world.py> <base_seed> <m_inv> <n_rep> <out.json>"""
import sys, json, copy, importlib.util, numpy as np
from scipy import ndimage
world, base, m_inv, nrep, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
T0, T1, EVERY, L = 30000, 90000, 3000, 300
spec = importlib.util.spec_from_file_location("w", world); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)

def census(g):
    lab, n = ndimage.label(np.pad(g == 0, 0))
    area = np.bincount(lab.ravel()); area[0] = 0; area[np.argmax(area)] = 0
    sides = [int(round(np.sqrt(a))) for a in area if a >= 4]
    return dict(zip(*np.unique(sides, return_counts=True))) if sides else {}

def run(s, t_end, rec):
    while s["t"] < t_end:
        for _ in range(EVERY): s = w.step(s)
        rec.append([s["t"], {int(k): int(v) for k, v in census(s["g"]).items()}])
    return s

s = w.init(base, (L, L))
for _ in range(T0): s = w.step(s)
c0 = census(s["g"])
if sum(c0.values()) < 20:
    json.dump({"base": base, "skipped": "population extinct or < 20 loops at t0", "census_t0": {int(k): int(v) for k, v in c0.items()}}, open(out, "w")); print(base, "skipped", c0); sys.exit(0)
res = {"base": base, "m_inv": m_inv, "t0": T0, "census_t0": {int(k): int(v) for k, v in c0.items()}, "twin": [], "reps": []}
twin = copy.deepcopy(s); run(twin, T1, res["twin"])
rng = np.random.default_rng(1000 + base)
lp0 = w.make_loop(m_inv)
for r in range(nrep):
    st = copy.deepcopy(s); g = st["g"]
    lp = np.rot90(lp0, r % 4); h, wd = lp.shape
    occ = ndimage.binary_dilation(g > 0, iterations=6)
    for _ in range(20000):
        i0, j0 = rng.integers(L), rng.integers(L)
        ii = (i0 + np.arange(h))[:, None] % L; jj = (j0 + np.arange(wd))[None, :] % L
        if not occ[ii, jj].any(): break
    else:
        res["reps"].append({"rep": r, "planted": False}); continue
    g[ii, jj] = lp
    rec = []; run(st, T1, rec)
    res["reps"].append({"rep": r, "planted": True, "at": [int(i0), int(j0)], "census": rec})
    print(base, m_inv, r, rec[-1], flush=True)
json.dump(res, open(out, "w"))
