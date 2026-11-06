"""Checker: re-run cheap cases end to end through the VW-1 world and compare with the media key's saved outputs.

 (a) objects hero episode, agent API: MapWorld(specs['objects'], world_seed=0).reset(0), step(None) x T;
     compare o(t), designer L1, tracker table/globals with results/hero_objects_s0.npz (bit for bit).
 (b) coarse world, same seed: level 0 vs the saved objects-episode level 0 (cross-view identity claim),
     and in_map equality.
 (c) designer.ensemble(2, seed=(7,)) of the 'both' world, rollout one tick per call for T2 ticks; compare
     L1 with members 0 and 1 of results/stats_both_J24_T300.npz (float32), and mass invariants.

usage: python -B rerun.py T T2 -> check/rerun.json
"""
import json
import sys
import time

sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/port")
import _paths  # noqa: F401,E402
import jax  # noqa: E402
import numpy as np  # noqa: E402

import aworld as AW  # noqa: E402

R = "/home/user/evalwork/vecworld/vw1/fresh/media/results"
T, T2 = int(sys.argv[1]), int(sys.argv[2])
t0, c0 = time.time(), time.process_time()
out = {"T": T, "T2": T2}
specs, parts = AW.build()
tr, LW = parts["tracker"], parts["LW"]
K, NS, NF, HW = tr.K, LW.NS, LW.NF, 128 * 128

# (a)
w = AW.MapWorld(specs["objects"], world_seed=0)
d = w.designer
O, Y, X, TB, GL = [], [], [], [], []


def rec(o):
    st = d.state()
    ms = [np.asarray(m) for m in jax.tree_util.tree_leaves(st["mem"]) if np.size(m) == tr.n_m]
    m = ms[0]
    O.append(np.asarray(o, float))
    Y.append(np.asarray(st["observed"], float))
    X.append(np.asarray(st["x"], np.float32))
    TB.append(m[HW:HW + K * NS].reshape(K, NS)[:, NF:].copy())
    GL.append(m[HW + K * NS:].copy())


rec(w.reset(0))
for t in range(T):
    rec(w.step(None))
h = np.load(f"{R}/hero_objects_s0.npz")
O, Y, X, TB, GL = map(np.array, (O, Y, X, TB, GL))
out["a_objects_hero"] = {
    "obs_bitwise_equal_saved": bool(np.array_equal(O, h["obs64"][:T + 1])),
    "L1_bitwise_equal_saved": bool(np.array_equal(Y, h["L1"][:T + 1])),
    "x_float32_equal_saved": bool(np.array_equal(X, h["x"][:T + 1])),
    "tab_equal_saved": bool(np.array_equal(TB, h["tab"][:T + 1])),
    "glob_equal_saved": bool(np.array_equal(GL, h["glob"][:T + 1])),
    "obs_max_abs_diff": float(np.abs(O - h["obs64"][:T + 1]).max()),
    "in_map_equal_saved": bool(np.array_equal(w.in_map, h["in_map"])),
    "out_map_equal_saved": bool(np.array_equal(w.out_map, h["out_map"])),
    "wall_s": time.time() - t0}
print(json.dumps(out["a_objects_hero"]), flush=True)

# (b)
wc = AW.MapWorld(specs["coarse"], world_seed=0)
wc.reset(0)
Xc = [np.asarray(wc.designer.state()["x"], np.float32)]
for t in range(T):
    wc.step(None)
    Xc.append(np.asarray(wc.designer.state()["x"], np.float32))
Xc = np.array(Xc)
out["b_coarse_vs_objects_level0"] = {"max_abs_diff": float(np.abs(Xc - X).max()),
                                     "in_map_equal_objects": bool(np.array_equal(wc.in_map, w.in_map)),
                                     "out_maps_differ_in_size": [int(w.n_obs), int(wc.n_obs)]}
# control: a different world seed gives a different trajectory and in_map
w1 = AW.MapWorld(specs["coarse"], world_seed=1)
w1.reset(0)
x1 = np.asarray(w1.designer.state()["x"], np.float32)
out["b_coarse_vs_objects_level0"]["control_world_seed1_level0_t0_max_abs_diff"] = float(np.abs(x1 - X[0]).max())
out["b_coarse_vs_objects_level0"]["control_world_seed1_in_map_equal"] = bool(np.array_equal(w1.in_map, w.in_map))
print(json.dumps(out["b_coarse_vs_objects_level0"]), flush=True)

# (c)
wb = AW.MapWorld(specs["both"], world_seed=0)
db = wb.designer
ens = db.ensemble(2, seed=(7,))
L = [ens.level(1)]
M = [np.stack([ens.invariants()["mass_c0"], ens.invariants()["mass_c1"]], -1)]
for t in range(T2):
    ens, r = db.rollout(ens, None, T=1, rec=("L1",))
    L.append(r["L1"][:, 1])
    inv = ens.invariants()
    M.append(np.stack([inv["mass_c0"], inv["mass_c1"]], -1))
L = np.swapaxes(np.array(L), 0, 1).astype(np.float32)
M = np.swapaxes(np.array(M), 0, 1)
z = np.load(f"{R}/stats_both_J24_T300.npz")
dL = np.abs(L - z["L1"][:2, :T2 + 1]).reshape(2, T2 + 1, -1).max(-1)
out["c_ensemble_seed7_members_0_1"] = {"L1_float32_max_abs_diff_per_tick": dL.max(0).tolist(),
                                       "L1_float32_equal_all": bool((dL == 0).all()),
                                       "mass_max_abs_diff": float(np.abs(M - z["mass"][:2, :T2 + 1]).max())}
out["wall_s"], out["cpu_s"] = time.time() - t0, time.process_time() - c0
print(json.dumps(out["c_ensemble_seed7_members_0_1"]), flush=True)
json.dump(out, open("/home/user/evalwork/vecworld/vw1/fresh/media/check/rerun.json", "w"), indent=1)
