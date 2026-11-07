"""declare -- the design, program mix and decision rules, written before any simulation.

usage: python -B declare.py   -> results/declaration.json (refuses to overwrite)
"""
import json
import os
import time

import wr

fn = f"{wr.RES}/declaration.json"
assert not os.path.exists(fn), "declaration exists; it is frozen"
D = {
    "written": time.strftime("%Y-%m-%d %H:%M:%S"),
    "world": "A_gliders + wind channel (actuation/wind.py, unchanged): 8 x 8 x 2 block forces, Gaussian blur 8 px, "
             "held for the 20 substeps of a tick, background a~ = u + sigma_w eta once per tick",
    "sigma_w_main": wr.SIGMA,
    "level1": "Phi_coarse (192) and Phi_objects (144), as vw1/fresh/closure",
    "a_viability": {
        "sigmas": wr.V_SIGMAS, "members": wr.V_J, "seed": wr.V_SEED,
        "design": "init + 50 burn-in + 250 ticks, no input; keys shared across sigma_w (paired); pooled with the 3 "
                  "actuation members (seed 9001, same design) for 9 per sigma_w",
        "statistics": "actuation/viability.traj_stats (objects present, speed median/p90, mass and rg median, "
                      "births/deaths/fusions/fissions per 100 ticks, track life median, share of tracks >= 50 ticks)",
        "native_band": "2.5-97.5% of means of n trajectories resampled from the 36 wind-free closure trajectories "
                       "(sim_A/sim_B, ticks 0..250), n = number of members compared",
        "rule": "sigma_w passes if every statistic's member mean lies in the native band for that n AND no paired "
                "difference to sigma_w = 0 (same keys) exceeds 3 SE",
        "oracle_cost": "12 sigma_w = 0 states (6 members x ticks 100, 200), R = 6 branches x 16 ticks at each sigma_w "
                       "with keys shared across sigma_w; dV(sigma) = V_oracle(sigma) - V_oracle(0) in closure-sd units, "
                       "relative to the fresh closure V_best (h = 1, 2, 4, 8, 16), both views",
        "decision": "0.1 replaces 0.05 only if 0.1 passes the viability rule and its measured dV is <= 0.10 V_best at "
                    "every horizon in both views; otherwise 0.05 stands if it passes",
    },
    "b_closure": {
        "horizons": wr.HORIZONS,
        "estimator": "closure_lib.closure_ext (the checked line-for-line copy of integrate/analyze.closure, with its "
                     "'extra' hook): mean, persistence, AR(1), ridge on 1/2/4/8 lags, kNN, VW-0 MLP (+ kinematic and "
                     "kin+ridge_p4 for objects); 4 folds by trajectory; errors against the base + 5 branch replicates; "
                     "unmodified analyze.closure (MLP off) must agree exactly; JAX rmlp/patchnet/slotnet if CPU allows",
        "set_F": {"J": wr.F_J, "T": wr.F_T, "test_ticks": wr.F_TEST, "branches": wr.R_BR, "branch_ticks": wr.TB,
                  "seed": wr.F_SEED, "input": "none"},
        "set_P": {"J": wr.P_J, "T": wr.P_T, "episodes": wr.P_EPISODES, "test_ticks": wr.P_TEST,
                  "branches": wr.R_BR, "twins_no_input": wr.R_TWIN, "branch_ticks": wr.TB, "seed": wr.P_SEED,
                  "test_classes": "balanced quotas over the 96 test items (24 per class), shuffled (seed 9204); "
                                  "non-test episodes iid with equal shares"},
        "program_mix": {"classes": wr.CLASSES, "shares": "equal", "length_ticks": wr.T_IN,
                        "budget_nats": {"blind": [wr.C_LO, wr.C_HI, "log-uniform"],
                                        "aimed": [wr.C_LO, wr.C_HI, "log-uniform"], "regional": wr.C_REG},
                        "definitions": wr.__doc__},
        "matched_reference": "the same estimator on the wind-free closure data cut to 16 trajectories (8 from sim_A, "
                             "8 from sim_B), ticks 0..236, test ticks 40/100/160/220, branches cut to 16 ticks",
        "inputs": "level-1 predictors with inputs: ridge on 1/2/4 lags plus input features of the declared future "
                  "commands in [t, t+h): the cumulative block command (128), the block-averaged displacement field "
                  "4 * sum E(u) (128), and for coarse the central-difference advection of the block means and m2 by "
                  "that displacement (192); for objects the displacement at each slot's extrapolated centroid "
                  "(dx, dy, and the induced change of the 4 position coordinates, 6 per slot) and a "
                  "kinematic+wind predictor with a ridge residual; the input-blind twins use the same lags and "
                  "data without the input features",
        "exam_effect": "per item d = err(best input-blind) - err(best input-aware), by class and pooled, relative to "
                       "V_best (input-aware best-of); detectability z = mean(d) / (sd(d) / sqrt(n)) at n = 64, 128 "
                       "for R = 1, 6 and (extrapolated) 16 replicate truths; also the true mean effect of each "
                       "program from the no-input twins (unbiased squared shift and the paired CRN version)",
    },
    "cpu": "core 0 only, one heavy process at a time; about 3 CPU-hours in all",
}
json.dump(D, open(fn, "w"), indent=1, default=list)
print("declared", fn)
