"""The VW-0 closure estimator on a VW-0 data subsample matched to the VW-1 run (sample-size control).

usage: python -B closure_vw0_subsample.py J T     -> results/closure_vw0_subsample.json

Reads integrate/data/A_gliders/base_*.npz and branch_*.npz (read only), keeps trajectories j < J,
truncates them to T ticks and the branches to 8 ticks, and runs integrate/analyze.closure with
HORIZONS = 1, 2, 4, 8 and the MLP off: the same estimator and the same sample size as
repro_closure.py, on the VW-0 simulator's data.
"""
import json
import os
import sys

import _paths
import numpy as np

import vw

J = int(sys.argv[1]) if len(sys.argv) > 1 else 16
T = int(sys.argv[2]) if len(sys.argv) > 2 else 240
cwd = os.getcwd()
os.chdir(_paths.INT_DIR)                     # analyze.load reads data/<name>/ relative to integrate/
import analyze as AN  # noqa: E402
assert AN.__file__.startswith(_paths.INT_DIR)
D = AN.load("A_gliders")
os.chdir(cwd)
keep = [i for i, j in enumerate(D["j"]) if j < J]
Ds = {"j": [D["j"][i] for i in keep], "st_tick": [D["st_tick"][i] for i in keep],
      "Yc": [D["Yc"][i][:T + 1] for i in keep], "Yo": [D["Yo"][i][:T + 1] for i in keep],
      "Bc": [D["Bc"][i][:, :, :8] for i in keep], "Bo": [D["Bo"][i][:, :, :8] for i in keep]}
assert all(int(t.max()) + 8 <= T for t in Ds["st_tick"])
AN.HORIZONS = [1, 2, 4, 8]
out = {"J": len(keep), "T": T, "n_test_states": int(sum(len(t) for t in Ds["st_tick"]))}
for phi, K in (("coarse", None), ("objects", 12)):
    c, _, _ = AN.closure(Ds, phi, K=K, mlp=False)
    out[phi] = {"ceiling": c["ceiling"], "ceiling_se": c["ceiling_se"], "best_name": c["best_name"],
                "V0": c["V0_mean_predictor"], "V_oracle": c["V_oracle"], "V_best": c["best_level1"]}
    print(phi, json.dumps(vw.jsonable(out[phi])), flush=True)
json.dump(vw.jsonable(out), open(f"{_paths.RESULTS}/closure_vw0_subsample.json", "w"), indent=1)
