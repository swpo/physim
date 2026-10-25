"""Invasion test with a matched neutral arm. Identical worlds (same seed) run to t_ins; then the SAME 40x40 patch
(seed-dependent position) is cleared in every arm and one planted loop of core side m_inv (hole side m_inv - 4) is placed
in it with the same orientation: m_inv=8 (side 4, the kind that swept in the claim) or m_inv=15 (side 11, the residents'
own kind = neutral arm). Census of hole sides every 1000 steps after insertion."""
import sys, os, json, importlib.util, numpy as np
from evo_track import holes
seed, t_ins, m_inv, T_after, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
L = 400; s = w.init(seed, (L, L))
for t in range(t_ins): w.step(s)
rng = np.random.default_rng(seed + 1000); i0, j0 = rng.integers(L, size=2); rot = rng.integers(4)
ii = (i0 + np.arange(40)) % L; jj = (j0 + np.arange(40)) % L
s["g"][np.ix_(ii, jj)] = 0
lp = np.rot90(w.make_loop(m_inv), rot); a, b = lp.shape
s["g"][np.ix_((i0 + 20 - a // 2 + np.arange(a)) % L, (j0 + 20 - b // 2 + np.arange(b)) % L)] = lp
rec = []
for t in range(1, T_after + 1):
    w.step(s)
    if t % 1000 == 0:
        lab, ids, area = holes(s["g"]); sz = np.round(np.sqrt(area[ids])).astype(int)
        h = np.bincount(sz, minlength=16)
        rec.append({"t": t_ins + t, "n": int(len(ids)), "hist": h.tolist()})
json.dump({"seed": seed, "t_ins": t_ins, "m_inv": m_inv, "patch": [int(i0), int(j0)], "rot": int(rot), "census": rec}, open(out, "w"))
f4 = rec[-1]["hist"][4] / max(rec[-1]["n"], 1)
print(seed, m_inv, "final n", rec[-1]["n"], "side-4 share", round(f4, 2), "side-11", rec[-1]["hist"][11], flush=True)
