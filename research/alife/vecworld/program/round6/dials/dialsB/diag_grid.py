"""diag_grid -- AFTER THE FACT (written after r6-dialsb-002's results were read; in no verdict): is the hidden
field X of the carrier smooth, or does it hold grid-scale (checkerboard) structure, at the pilot centre?

    python -B diag_grid.py            (CPU, about 3 minutes; writes results/diag_grid.json)

Why: scan C found the gap without input at the floor for D_X <= 0.35 (0.005-0.006) and at 0.13 for D_X = 0.5, no
cells at all for rho >= 0.04 at D_X = 0.5, and the told-form recipe (whose D_X is below 0.5) lost most of the
32-tick gap. `sublevel.py` steps X by explicit Euler with the 5-point Laplacian at dt = 0.5: the checkerboard mode
is multiplied each native step by 1 - 8 dt D_X - dt rho (K / 0.25) = -(1 + 0.5 rho K / 0.25) at D_X = 0.5, of
modulus above 1 wherever there is catalyst. This script measures it: the hidden world forms cells for 150 ticks
(the gate's and scan C's set-up, ensemble seed (77, 2), 2 members), and the same members are run on to tick 182
without input; reported at ticks 150 and 182: the largest |X|, the largest grid-scale part of X (|X - mean of its
4 neighbours| / 2, which is the amplitude of a checkerboard), and their ratio. PILOT values, never an exam.
"""
import json
import os
import sys

sys.dont_write_bytecode = True
os.environ.setdefault("OUT", "/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/dialsB/out_diag")
import numpy as np  # noqa: E402

import s0  # noqa: E402

M = 2
rows = []
cfg, K, pub, hid = s0.make_worlds(dict(lam=1.0, cat=1.0, **s0.CENTRE))


def grid_part(X):
    nb = 0.25 * (np.roll(X, 1, -1) + np.roll(X, -1, -1) + np.roll(X, 1, -2) + np.roll(X, -1, -2))
    return np.abs(X - nb) / 2.0


for cat, rho, DX in ((1.0, 0.02, 0.5), (1.0, 0.02, 0.35), (1.0, 0.01, 0.5), (1.0, 0.04, 0.5), (0.0, 0.02, 0.5)):
    hid.set(cat=cat, rho=rho, DX=DX)
    row = {"cat": cat, "rho": rho, "DX": DX, "a0": s0.CENTRE["a0"], "lam": 1.0,
           "checkerboard_factor_per_native_step_inside_cells": -(1 - 8 * 0.5 * DX - 0.5 * rho * (1.08 if cat else 1.0))}
    for T in (150, 182):
        x, L1 = hid.form(M, (77, 2), T=T)
        X = x["X"]
        n, _ = s0.n_and_area(np.nan_to_num(L1[:, -1]), K, s0.PX)
        g = grid_part(X)
        row[f"tick_{T}"] = {"finite": bool(np.isfinite(X).all()), "max_abs_X": float(np.nanmax(np.abs(X))),
                            "max_grid_scale_part": float(np.nanmax(g)), "ratio": float(np.nanmax(g) / max(np.nanmax(np.abs(X)), 1e-300)),
                            "max_grid_scale_part_per_member": np.nanmax(g, axis=(1, 2)).tolist(), "cells": n.tolist(),
                            "S_min": float(np.nanmin(x["S"])), "S_max": float(np.nanmax(x["S"]))}
    rows.append(row)
    print(json.dumps(row), flush=True)
# the gate's own start states: seeds 31 and 36, main arm, all 16 members (ensemble seed (78, seed) as in the gate)
gate_rows = []
for seed in (31, 36):
    hid.set(cat=1.0, **s0.CENTRE)
    row = {"seed": seed, "arm": "main", "hidden_pilot": dict(lam=1.0, cat=1.0, **s0.CENTRE)}
    for T in (150, 182):
        x, L1 = hid.form(16, (78, seed), T=T)
        g = grid_part(x["X"])
        row[f"tick_{T}"] = {"finite_members": int(np.isfinite(x["X"]).all((1, 2)).sum()),
                            "max_abs_X_per_member": np.nanmax(np.abs(x["X"]), axis=(1, 2)).tolist(),
                            "max_grid_scale_part_per_member": np.nanmax(g, axis=(1, 2)).tolist(),
                            "S_min_per_member": np.nanmin(x["S"], axis=(1, 2)).tolist()}
    gate_rows.append(row)
    print(json.dumps({"seed": seed, "tick_150_grid": np.round(row["tick_150"]["max_grid_scale_part_per_member"], 4).tolist(),
                      "tick_182_grid": np.round(row["tick_182"]["max_grid_scale_part_per_member"], 3).tolist(),
                      "tick_182_S_min": np.round(row["tick_182"]["S_min_per_member"], 3).tolist()}), flush=True)
hid.set()
out = {s0.PILOT: True, "gate_start_states": gate_rows, "AFTER_THE_FACT": "written after the job's results were read; a diagnostic, in no verdict",
       "what": "grid-scale (checkerboard) content of the carrier field X after 150 and 182 ticks without input, 64 px, 2 members, "
               "ensemble seed (77, 2)", "rows": rows}
json.dump(out, open(os.path.join(s0.HERE, "results", "diag_grid.json"), "w"), indent=1)
