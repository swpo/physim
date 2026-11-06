"""Item 2: Phi_coarse (JAX) and Phi_objects (opaque VW-0 tracker) as CoarseGrain modules.

usage: python -B check_phi.py   -> results/phi_check.json

(a) Phi_coarse against integrate/lenia_world.make_phi_coarse on stored and simulated states;
(b) Phi_objects inside a running VW-1 world (memory carried by the World, host callback per tick)
    against the numpy Tracker replayed on the same level-0 states: memory and output identical;
(c) vmap versus lax.map batching: see check_batching.py (chaos amplifies their rounding difference);
(d) the opaque block refuses derivatives: jax.grad raises, certificates.fisher raises
    NotDifferentiable; Phi_coarse is differentiable (finite gradient);
(e) cost per tick of the tracker callback.
"""
import json
import time

import _paths
import jax
import jax.numpy as jnp
import numpy as np

import vw
import aworld as AW
import phi as PH

out = {}
specs, parts = AW.build()
cfg, tr, LW = parts["cfg"], parts["tracker"], parts["LW"]
l0 = LW.Level0("A_gliders", 20, 0.0)
coarse_np, n1c, _ = LW.make_phi_coarse(l0, AW.G)

# (a)
A0 = np.load(f"{_paths.L0_DIR}/worlds/A_gliders/init.npz")["A0"]
A4 = np.load(f"{_paths.L0_DIR}/worlds/A_gliders/state_t4000.npz")["A"]
pc = jax.jit(lambda A: parts["phi_coarse"].phi(A, ()))
diffs = [float(np.abs(np.asarray(pc(jnp.asarray(A))) - coarse_np(A.ravel()[None])[0]).max()) for A in (A0, A4)]
out["phi_coarse"] = {"n_out": int(n1c), "max_abs_diff_vs_vw0": max(diffs)}

# (b) + (c): objects world, recorded level 0 and level 1
T = 30
res = {}
for nm, cls in (("laxmap", AW.MapWorld),):
    w = cls(specs["objects"], world_seed=0)
    d = w.designer
    t0 = time.time()
    ens = d.ensemble(2, seed=(5,))
    jax.block_until_ready(ens.carry.x)
    t_init = time.time() - t0
    t0 = time.time()
    ens2, rec = d.rollout(ens, None, T=T, rec=("x", "L1"))
    t_roll = time.time() - t0
    res[nm] = {"x": rec["x"], "L1": rec["L1"], "mem": np.asarray(ens2.carry.mem[0]), "mem0": np.asarray(ens.carry.mem[0]),
               "t_init": t_init, "t_roll": t_roll}
    print(nm, "init+burn-in", round(t_init, 1), "s; rollout", T, "ticks", round(t_roll, 1), "s", flush=True)
b = res["laxmap"]
# replay the numpy tracker on the recorded level-0 states, starting from the world's memory at t = 0
X, Y = b["x"], b["L1"]
rep_err, mem_err = 0.0, 0.0
for i in range(X.shape[0]):
    m = b["mem0"][i]
    for t in range(1, T + 1):
        m = tr.update_one(m, X[i, t])
        rep_err = max(rep_err, float(np.abs(tr.phi(None, m[None])[0] - Y[i, t]).max()))
    mem_err = max(mem_err, float(np.abs(m - b["mem"][i]).max()))
out["phi_objects"] = {"memory_size": int(tr.n_m), "n_out": int(tr.K * LW.NF), "ticks": T, "members": int(X.shape[0]),
                      "replay_output_max_abs_diff": rep_err, "replay_final_memory_max_abs_diff": mem_err,
                      "objects_present_t30": [int((Y[i, -1].reshape(tr.K, LW.NF)[:, 0] > 0.5).sum()) for i in range(X.shape[0])]}

# (d) derivatives
po = parts["phi_objects"]
x0 = jnp.asarray(A0)
try:
    jax.grad(lambda A: po.update_memory(po.init_memory(A), A).sum())(x0)
    out["grad_through_tracker"] = "no error (unexpected)"
except Exception as e:  # noqa: BLE001
    out["grad_through_tracker"] = f"raises {type(e).__name__}"
try:
    vw.fisher(AW.MapWorld(specs["objects"], 0), wrt=["R"], n=4)
    out["fisher_on_objects_world"] = "no error (unexpected)"
except vw.NotDifferentiable as e:
    out["fisher_on_objects_world"] = f"NotDifferentiable: {str(e)[:90]}"
g = jax.grad(lambda A: parts["phi_coarse"].phi(A, ())[5])(x0)
out["phi_coarse_grad_finite"] = bool(np.isfinite(np.asarray(g)).all())

# (e) tracker cost per call
t0 = time.time()
m = tr.update_one(None, A4.ravel())
for _ in range(20):
    m = tr.update_one(m, A4.ravel())
out["tracker_ms_per_call"] = 1e3 * (time.time() - t0) / 21
out["rollout_seconds"] = {k: {"init_burnin_2_members": v["t_init"], f"rollout_{T}_ticks_2_members": v["t_roll"]} for k, v in res.items()}
print(json.dumps(out, indent=1))
json.dump(out, open(f"{_paths.RESULTS}/phi_check.json", "w"), indent=1)
