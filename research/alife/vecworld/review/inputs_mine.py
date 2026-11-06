"""Reviewer's own input-visibility check on A_gliders: one default-constraint input tick (k = 8,
4 sources at -0.5, 4 sinks at +0.5) applied through the agent coordinates (in_map) at the saved
test state si = 1 of trajectories 0..11, against the identical-noise twin (the base continuation,
verified bit-for-bit reproducible). Response = mean over coordinates of the squared standardised
level-1 difference, divided by the state's oracle spread (unbiased within-replicate variance of
base + 5 fresh-noise branches). Placements: cells inside tracked bodies, or uniformly random cells.
"""
import json
import sys

import numpy as np

INT = "/home/user/evalwork/vecworld/integrate"
sys.path.insert(0, INT)
import lenia_world as LW   # noqa: E402
vw = LW.vw

specs, parts = LW.make_specs("A_gliders")
l0, coarse = parts["l0"], parts["phi_coarse"]
w = vw.VectorWorld(specs["objects"], world_seed=0)
inv = LW.inverse_in_map(w)
Cn = w.spec.inputs
SI, TM = 1, 8
TAUS = [1, 2, 4, 8]
base = [np.load(f"{INT}/data/A_gliders/base_{j:03d}.npz") for j in range(24)]
br = [np.load(f"{INT}/data/A_gliders/branch_{j:03d}.npz") for j in range(24)]
out = {}
for phi, key in (("objects", "Yo"), ("coarse", "Yc")):
    sd = np.concatenate([b[key] for b in base]).std(0)
    eff = sd > 1e-6 * sd.max()
    out[phi] = {"sd": sd, "eff": eff}
res = {}
for place in ("body", "random"):
    rows = {"objects": [], "coarse": []}
    moved = []
    for j in range(12):
        d = base[j]
        t0 = int(d["st_tick"][SI]) - int(d["burn_in"])
        rng = np.random.default_rng([2026, 11, j, 0 if place == "body" else 1])
        ens = vw.Ensemble(w, d["st_h0"][SI][None], d["st_m"][SI][None], tuple(int(x) for x in d["seed"]), [0],
                          int(d["st_tick"][SI]))
        S = ens.h0[0].reshape(l0.C, -1).sum(0)
        if place == "body":
            pool = np.flatnonzero((ens.m[0, :l0.HW] > 0) & (S > 1e-3))
        else:
            pool = np.arange(l0.HW)
        cells = rng.choice(pool, 8, replace=False)
        a = {int(inv[c]): (-0.5 if k < 4 else 0.5) for k, c in enumerate(cells)}
        assert not Cn.violations(a, 0, None, 0.0)
        dense = np.zeros(w.n_in)
        for jj, v in a.items():
            dense[jj] = v
        h_before = ens.h0.copy()
        u = np.zeros((1, l0.HW))
        u[:, w.in_map] = dense
        moved.append(0.5 * float(np.abs(l0.kick(h_before, u) - h_before).sum()))
        Yi = {"objects": [], "coarse": []}
        for s in range(TM):
            ens.step(dense if s == 0 else None)
            Yi["objects"].append(ens.h1()[0])
            Yi["coarse"].append(coarse(ens.h0)[0])
        for phi, key in (("objects", "Yo"), ("coarse", "Yc")):
            sd, eff = out[phi]["sd"], out[phi]["eff"]
            twin = d[key][t0 + 1:t0 + 1 + TM]
            reps = np.concatenate([twin[None], br[j][key][SI][:, :TM]], 0)[..., eff] / sd[eff]
            Vu = ((reps - reps.mean(0)) ** 2).sum((0, 2)) / (reps.shape[0] - 1) / eff.sum()
            resp = ((((np.array(Yi[phi]) - twin) / sd)[:, eff]) ** 2).mean(1)
            rows[phi].append(resp / Vu)
    res[place] = {"moved_mass_median": float(np.median(moved)),
                  **{phi: {t: float(np.median(np.array(rows[phi])[:, t - 1])) for t in TAUS} for phi in rows}}
    print(place, json.dumps(res[place]))
json.dump(res, open("/home/user/evalwork/vecworld_integrate_review/inputs_mine.json", "w"), indent=1)
