"""One fresh VW-1 agent episode of the A_gliders world, with the designer side of the SAME episode.

usage: python -B hero_run.py VIEW SEED T     VIEW in {objects, coarse, both}
  -> results/hero_VIEW_sSEED.npz   obs (T+1, n_obs)  what World.reset / World.step returned (agent basis)
                                   L1 (T+1, n1)     designer.state()['observed'] each tick (designer basis)
                                   x  (T+1, 2, 128, 128) float32  designer.state()['x'] (level 0)
                                   tab (T+1, K, 5)  tracker slot extras (cy, cx, age, event, uid)  [objects/both]
                                   glob (T+1, 5)    tracker globals (next uid, births, deaths, fusions, fissions)
                                   out_map, in_map  hidden maps (designer side; used for scoring only)
     results/hero_VIEW_sSEED.json  card, timing, checks
The agent loop is exactly: o = w.reset(SEED); for t < T: o = w.step(None). After every call the
designer reads designer.state() of the same episode (no second simulation). Check: every observation
equals the quantised, permuted designer level (o[j] == q * round(y[out_map[j]] / q), bit for bit).
"""
import json
import os
import sys
import time

sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/port")
import _paths  # noqa: F401,E402
import jax  # noqa: E402
import numpy as np  # noqa: E402

import vw  # noqa: E402
import aworld as AW  # noqa: E402

OUT = "/home/user/evalwork/vecworld/vw1/fresh/media/results"
view, seed, T = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
t_wall, t_cpu = time.time(), time.process_time()
specs, parts = AW.build(with_objects=(view != "coarse"))
w = AW.MapWorld(specs[view], world_seed=0)
d = w.designer
card = w.card()
HW = 128 * 128
if view != "coarse":
    tr, LW = parts["tracker"], parts["LW"]
    K, NS, NF = tr.K, LW.NS, LW.NF


def tracker_mem(st):
    if view == "coarse":
        return None
    ms = [np.asarray(m) for m in jax.tree_util.tree_leaves(st["mem"]) if np.size(m) == tr.n_m]
    assert len(ms) == 1
    return ms[0]


obs, L1, X, TAB, GLOB = [], [], [], [], []


def record(o, st):
    obs.append(np.asarray(o, float))
    L1.append(np.asarray(st["observed"], float))
    X.append(np.asarray(st["x"], np.float32))
    m = tracker_mem(st)
    if m is not None:
        TAB.append(m[HW:HW + K * NS].reshape(K, NS)[:, NF:].copy())
        GLOB.append(m[HW + K * NS:].copy())


o = w.reset(seed)
record(o, d.state())
t_reset = time.time() - t_wall
log = open(f"{OUT}/hero_{view}_s{seed}.log", "w")
for t in range(T):
    o = w.step(None)
    record(o, d.state())
    if (t + 1) % 25 == 0:
        print(f"tick {t + 1} wall {time.time() - t_wall:.1f}s", file=log, flush=True)
obs, L1 = np.array(obs), np.array(L1)
om = w.out_map
q = OBSQ = AW.OBS.quantum
expect = q * np.round(L1[:, om] / q)
exact = bool(np.array_equal(obs, expect))
res = {"view": view, "seed": seed, "T": T, "world_seed": 0, "card": card,
       "n_obs": int(w.n_obs), "n_in": int(w.n_in), "ticks_used": int(w.ticks_used),
       "obs_equal_quantised_permuted_designer_level_bitwise": exact,
       "obs_max_abs_diff": float(np.abs(obs - expect).max()),
       "out_sign_all_plus": bool((w.out_sign == 1).all()),
       "reset_plus_burnin_wall_s": t_reset, "wall_s": time.time() - t_wall, "cpu_s": time.process_time() - t_cpu}
sv = dict(obs=obs.astype(np.float32), obs64=obs, L1=L1, x=np.array(X, np.float32), out_map=om, in_map=w.in_map)
if TAB:
    TAB, GLOB = np.array(TAB), np.array(GLOB)
    sv.update(tab=TAB, glob=GLOB)
    pres = L1[:, -K * NF:].reshape(len(L1), K, NF)[:, :, 0] > 0.5
    ev = GLOB[-1, 1:] - GLOB[0, 1:]
    res["tracker_events_over_episode"] = dict(zip(["births", "deaths", "fusions", "fissions"], ev.tolist()))
    res["objects_present"] = {"median": float(np.median(pres.sum(1))), "min": int(pres.sum(1).min()),
                              "max": int(pres.sum(1).max())}
    res["fusion_ticks"] = [int(t) for t in np.flatnonzero(np.diff(GLOB[:, 3]) > 0) + 1]
    res["fission_ticks"] = [int(t) for t in np.flatnonzero(np.diff(GLOB[:, 4]) > 0) + 1]
np.savez_compressed(f"{OUT}/hero_{view}_s{seed}.npz", **sv)
json.dump(vw.jsonable(res), open(f"{OUT}/hero_{view}_s{seed}.json", "w"), indent=1)
print(json.dumps(vw.jsonable({k: v for k, v in res.items() if k not in ("card", "fusion_ticks", "fission_ticks")})))
