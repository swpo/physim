"""Checker re-run (core 1): stage A into a scratch folder, then world 0 end to end at the small passive
budget (Lab -> agent data -> B0/B1/B2/B2x, plus B3 and B2@zero) on the 128-item, 16-truth exam,
compared item by item with results/d2_scores.npz."""
import json
import os
import sys
import time

import numpy as np

H = "/home/user/evalwork/vecworld/program/track2/harness"
sys.path.insert(0, H)
SCR = sys.argv[1]
t0 = time.process_time()
import run_toy as RT  # noqa: E402
import toy as T  # noqa: E402
from vw.harness import Lab  # noqa: E402

RT.OUT = SCR
out = {}
# ---- stage A, rerun
c = time.process_time()
RT.stage_A()
a_new = json.load(open(os.path.join(SCR, "stageA.json")))
a_old = json.load(open(os.path.join(H, "results/stageA.json")))
diffs = []
for k, v in a_old["programs"].items():
    for kk in ("charge_nats", "kl_obs_level1_given_history", "efficiency_level1_given_history",
               "max_mean_shift_sd_level1_given_history"):
        diffs.append(abs(v[kk] - a_new["programs"][k][kk]))
    diffs.append(abs(v["mc_llr"]["mc_nats"] - a_new["programs"][k]["mc_llr"]["mc_nats"]))
out["stageA_max_abs_diff"] = max(diffs)
out["stageA_rejections_equal"] = a_old["rejections"] == a_new["rejections"]
out["stageA_cpu_s"] = time.process_time() - c

# ---- world 0, small passive, end to end
c = time.process_time()
W, b = 0, "small_passive"
E, L, active = RT.BUDGETS[b]
th = RT.theta(W)
ex = RT.make_exam(W)
refs = ex.references()
sim = T.Simulator()
lab = Lab(T.world(th), RT.SEC.child("agent", W, b), nats=T.nats_budget(total=0.0), max_ticks=E * (L + 1))
eps = T.collect(lab, E, L, active, seed=W * 100 + len(b))
rng = np.random.default_rng([W, len(b), 2])
THs, lws, _ = T.pmc(T.synthetic_loglik(sim, eps, n_rep=RT.NREP_SL, seed=W * 10 + len(b)), rng, M=RT.M_PMC, rounds=RT.ROUNDS)
THx, lwx, _ = T.pmc(T.exact_loglik(eps), np.random.default_rng([W, len(b), 3]), M=RT.M_PMC, rounds=RT.ROUNDS)
P = {f"B0@{b}": T.climatology_from_data(eps), f"B1@{b}": T.fit_arx(eps),
     f"B2@{b}": T.filter_predictor(T.posterior_draws(THs, lws, RT.J_POST, rng)),
     f"B2x@{b}": T.filter_predictor(T.posterior_draws(THx, lwx, RT.J_POST, rng)),
     "B3_true_theta": T.filter_predictor(th)}
rng0 = np.random.default_rng([W, 1])
P["B2@zero"] = T.filter_predictor(np.stack([T.draw_theta(rng0) for _ in range(RT.J_POST)]))
Z = np.load(os.path.join(H, "results/d2_scores.npz"))
S = {"climatology": refs["climatology"]["es"], "oracle": refs["oracle"]["es"]}
out["ref_max_abs_diff"] = {k: float(np.abs(S[k] - Z[f"n128R16/{k}"]).max()) for k in S}
out["pred_max_abs_diff"] = {}
for k, f in P.items():
    S[k] = ex.score(ex.collect(f, 64, 0))["es"]
    out["pred_max_abs_diff"][k] = float(np.abs(S[k] - Z[f"n128R16/{k}"]).max())
out["usage"] = lab.usage()
out["world0_small_passive_cpu_s"] = time.process_time() - c
np.savez(os.path.join(SCR, "rerun_scores.npz"), **S)
out["total_cpu_s"] = time.process_time() - t0
json.dump(out, open(os.path.join(SCR, "rerun.json"), "w"), indent=1, default=float)
print(json.dumps(out, indent=1, default=float))
