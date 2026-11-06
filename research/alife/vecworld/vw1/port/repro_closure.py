"""Item 3b: reproduce VW-0 closure ceilings of A_gliders through the VW-1 world and designer API.

usage: python -B repro_closure.py J T R      -> results/closure_repro.json (+ closure_data.npz)

Data, as integrate/run_base.py + run_branches.py but with the VW-1 types: J designer trajectories
(init + 50-tick burn-in) of the <Phi_coarse, Phi_objects> world, T free ticks each; at test ticks
(60, 140, 220) R-1 fresh-noise branches from the privileged state (x, m) for 8 ticks (the base
continuation is replicate 0). Estimator: integrate/analyze.closure (the VW-0 code, unchanged; its
HORIZONS set to 1, 2, 4, 8 and the MLP off): standardised units, level-1-only predictors (mean,
persistence, AR(1), ridge on 1/2/4/8 lags, kNN; for objects also kinematic and kinematic+ridge)
fitted on folds by trajectory, scored against the replicate futures; ceiling
c = (V0 - V_best) / (V0 - V_oracle), bootstrap SE over trajectories.
VW-0 reference: J = 24, T = 300, 72 test states, R = 6 (integrate/results/A_gliders_certificates.json).
"""
import json
import sys
import time

import _paths
import numpy as np

import vw
import aworld as AW

J = int(sys.argv[1]) if len(sys.argv) > 1 else 16
T = int(sys.argv[2]) if len(sys.argv) > 2 else 240
R = int(sys.argv[3]) if len(sys.argv) > 3 else 6
TEST = (60, 140, 220)
TB, CH = 8, 20
assert T % CH == 0 and all(t % CH == 0 for t in TEST) and max(TEST) + TB <= T

specs, parts = AW.build()
w = AW.MapWorld(specs["both"], world_seed=0)
d = w.designer
n_c = 192
t0 = time.time()
ens = d.ensemble(J, seed=(101,))
print("init + burn-in", J, "members:", round(time.time() - t0, 1), "s", flush=True)
Y = [ens.level(1)[:, None]]                                    # (J, 1, 336)
B = np.zeros((J, len(TEST), R - 1, TB, Y[0].shape[-1]))
t = 0
while t < T:
    if t in TEST:
        br = ens.clone(rep=R - 1, fresh=True)
        _, rb = d.rollout(br, None, T=TB, rec=("L1",))
        B[:, TEST.index(t)] = rb["L1"][:, 1:].reshape(J, R - 1, TB, -1)
    ens, r = d.rollout(ens, None, T=CH, rec=("L1",))
    Y.append(r["L1"][:, 1:])
    t += CH
    print("tick", t, round(time.time() - t0, 1), "s", flush=True)
Y = np.concatenate(Y, 1)                                       # (J, T+1, 336)
np.savez_compressed(f"{_paths.RESULTS}/closure_data.npz", Y=Y.astype(np.float32), B=B.astype(np.float32))
sim_seconds = time.time() - t0

import analyze as AN  # noqa: E402   (VW-0 estimator, read only)
assert AN.__file__.startswith(_paths.INT_DIR), AN.__file__
AN.HORIZONS = [1, 2, 4, 8]
D = {"Yc": [Y[j, :, :n_c] for j in range(J)], "Bc": [B[j, ..., :n_c] for j in range(J)],
     "Yo": [Y[j, :, n_c:] for j in range(J)], "Bo": [B[j, ..., n_c:] for j in range(J)],
     "st_tick": [np.array(TEST) for _ in range(J)], "j": list(range(J))}
ref = json.load(open(f"{_paths.INT_DIR}/results/A_gliders_certificates.json"))
out = {"J": J, "T": T, "R": R, "test_ticks": TEST, "n_test_states": J * len(TEST), "branch_ticks": TB,
       "member_ticks_simulated": J * (AW.BURN_TICKS + T) + J * len(TEST) * (R - 1) * TB,
       "simulation_seconds": sim_seconds, "vw0_sample": {"J": ref["n_traj"], "T": ref["ticks_per_traj"],
                                                          "n_test_states": ref["closure_coarse"]["n_test_states"],
                                                          "R": ref["closure_coarse"]["replicates"]}}
for phi, K in (("coarse", None), ("objects", 12)):
    c, eff, sd = AN.closure(D, phi, K=K, mlp=False)
    r0 = ref[f"closure_{phi}"]
    out[phi] = {"horizons": c["horizons_ticks"], "ceiling": c["ceiling"], "ceiling_se": c["ceiling_se"],
                "best_name": c["best_name"], "V0": c["V0_mean_predictor"], "V_oracle": c["V_oracle"],
                "V_best": c["best_level1"], "n_eff_coords": c["n_eff_coords"],
                "vw0_ceiling": r0["ceiling"][:4], "vw0_ceiling_se": r0["ceiling_se"][:4], "vw0_best_name": r0["best_name"][:4],
                "vw0_V_oracle": r0["V_oracle"][:4],
                "z_vs_vw0": [(a - b) / np.hypot(s1, s2) for a, b, s1, s2 in
                             zip(c["ceiling"], r0["ceiling"][:4], c["ceiling_se"], r0["ceiling_se"][:4])]}
    print(phi, json.dumps(vw.jsonable(out[phi])), flush=True)
json.dump(vw.jsonable(out), open(f"{_paths.RESULTS}/closure_repro.json", "w"), indent=1)
