"""Item 3a: the A_gliders World with the VW-0 ports; agent API and exam harness.

usage: python -B check_world.py   -> results/world_check.json

Coarse world (Phi_coarse observed, 192 numbers) and objects world (Phi_objects, 144 numbers):
card, reset, a legal zero-sum kick (mass per channel conserved), the four VW-0 smoke-test
violations (rejected, nothing charged), run(program, query_times), replay='initial', the
observation equals Q(P y) of the designer's level 1; then a small exam (persistence and a
linear-extrapolation agent) scored against replicate futures.
"""
import json
import time

import _paths
import jax
import numpy as np

import vw
import aworld as AW

out = {}
specs, parts = AW.build()
cfg = parts["cfg"]
BAD = [{0: 0.5}, {i: 0.1 for i in range(9)}, {0: 2.0, 1: -2.0}, {0: 0.9, 1: 0.9, 2: -0.9, 3: -0.9, 4: 0.5, 5: -0.5}]

for phi in ("coarse", "objects"):
    t_all = time.time()
    w = AW.MapWorld(specs[phi], world_seed=7)
    d = w.designer
    rec = {"card": w.card()}
    t0 = time.time()
    o0 = w.reset(seed=3)
    rec["reset_seconds"] = time.time() - t0
    st = d.state()
    A = np.asarray(st["x"])
    mass0 = A.sum((1, 2))
    inv = AW.inverse_in_map(w)
    S = A.sum(0).ravel()
    src, snk = np.argsort(-S)[:4], np.argsort(S)[:4]
    a = {int(inv[i]): -0.5 for i in src}
    a.update({int(inv[i]): 0.5 for i in snk})
    t0 = time.time()
    o1 = w.step(a)
    rec["step_seconds"] = time.time() - t0
    A1 = np.asarray(d.state()["x"])
    rec["mass_rel_change_after_kick_tick"] = float(np.abs(A1.sum((1, 2)) / mass0 - 1).max())
    rec["obs_change_l1"] = float(np.abs(o1 - o0).sum())
    # the observation is the quantised, permuted level 1
    y = d.state()["observed"]
    q = w.outport.quantum
    rec["obs_equals_QPy_max_abs"] = float(np.abs(o1 - q * np.round(y[w.out_map] / q)).max())
    errs, t_before, used_before = [], w.t, w.ticks_used
    for bad in BAD:
        try:
            w.step(bad)
            errs.append("accepted")
        except vw.InputViolation as e:
            errs.append(str(e)[:110])
    rec["violations"] = errs
    rec["nothing_charged"] = bool(w.t == t_before and w.ticks_used == used_before)
    Y = w.run([(0, a), (2, a)], query_times=[1, 3, 5])
    A2 = np.asarray(d.state()["x"])
    rec["run_shape"] = list(Y.shape)
    rec["mass_rel_change_after_run"] = float(np.abs(A2.sum((1, 2)) / mass0 - 1).max())
    oa, ob = w.reset(seed=3), w.reset(seed=3)
    rec["replay_initial_same_o0"] = bool(np.array_equal(oa, ob))
    rec["seconds"] = time.time() - t_all
    out[phi] = rec
    print(phi, json.dumps({k: v for k, v in rec.items() if k != "card"}, default=str)[:900], flush=True)

# exam on the coarse world
w = AW.MapWorld(specs["coarse"], world_seed=7)
t0 = time.time()
ex = vw.Exam(w, n_items=8, prefix=4, horizon=8, queries=(1, 2, 4, 8), rate=0.5, exam_seed=0)
t_build = time.time() - t0
items = ex.public()


def linear_agent(it):
    """Extrapolate the last observed change, damped (a trivial level-1-only predictor)."""
    o = it["past_obs"]
    return np.stack([o[-1] + 0.5 * q * (o[-1] - o[-2]) for q in it["query_times"]])


t0 = time.time()
sc = ex.score([linear_agent(it) for it in items], n_rep=8)
out["exam"] = {"n_items": len(items), "prefix": 4, "horizon": 8, "queries": sc["queries"], "n_rep": 8,
               "public_item_keys": sorted(items[0].keys()), "build_seconds": t_build, "score_seconds": time.time() - t0,
               "oracle": sc["oracle"], "mse": sc["mse"], "skill_vs_oracle": sc["skill"]}
print(json.dumps(vw.jsonable(out["exam"]), indent=1))
json.dump(vw.jsonable(out), open(f"{_paths.RESULTS}/world_check.json", "w"), indent=1)
