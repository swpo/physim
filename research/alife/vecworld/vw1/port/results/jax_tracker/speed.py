"""Speed of the object tracker, host (VW-0 numpy + pure_callback) vs JAX, single core; vmap over 8 members.

usage: python -B speed.py   -> speed.json

(a) the memory update alone, per call, on the 300 level-0 states of the hero episode (float64 casts of
    the stored float32 states; both trackers see the same input): host Tracker.update_one (numpy) and
    the jitted JAX update; JAX also under jax.vmap over 8 members (per member).
(b) per tick and member inside the A_gliders world (MapWorld, 1 member, 20 ticks after burn-in, i.e.
    20 Flow-Lenia substeps + tracker per tick): objects world with tracker='host' and 'jax', and the
    coarse world (no tracker) as the baseline.
(c) vw.World (members batched by jax.vmap) on the JAX objects world: 8 members, init + burn-in +
    5 ticks; the tracker memory of each member equals the JAX tracker replayed on that member's
    recorded level 0, and the discrete part equals the host tracker's replay.
"""
import json
import os
import sys
import time

sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/port")
import _paths  # noqa: E402,F401
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import vw  # noqa: E402
import aworld as AW  # noqa: E402
import phi as PH  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
res = {"jax": jax.__version__, "cpu_affinity": sorted(os.sched_getaffinity(0)),
       "XLA_FLAGS": os.environ.get("XLA_FLAGS", "")}
X = np.load("/home/user/evalwork/vecworld/vw1/fresh/media/results/hero_objects_s0.npz")["x"].astype(np.float64)
trh, LW = PH.vw0_tracker()
_, trj, _ = PH.phi_objects_jax()
bt = trj.bt

# (a) update alone
mh = trh.update_one(None, X[0].ravel())
t0 = time.perf_counter()
for t in range(1, 301):
    mh = trh.update_one(mh, X[t].ravel())
host_ms = (time.perf_counter() - t0) / 300 * 1e3
upd = jax.jit(bt.update_memory)
Xj = jnp.asarray(X)
mj = jax.jit(bt.init_memory)(Xj[0])
upd(mj, Xj[1]).block_until_ready()
t0 = time.perf_counter()
for t in range(1, 301):
    mj = upd(mj, Xj[t])
mj.block_until_ready()
jax_ms = (time.perf_counter() - t0) / 300 * 1e3
vupd = jax.jit(jax.vmap(bt.update_memory))
mv = jax.jit(jax.vmap(bt.init_memory))(Xj[0:8])
vupd(mv, Xj[1:9]).block_until_ready()
t0 = time.perf_counter()
for t in range(1, 41):
    mv = vupd(mv, Xj[t:t + 8])
mv.block_until_ready()
vmap_ms = (time.perf_counter() - t0) / 40 / 8 * 1e3
res["update_ms_per_call"] = {"host_numpy": host_ms, "jax_jit": jax_ms, "jax_vmap8_per_member": vmap_ms,
                             "final_memory_equal_discrete": bool(np.array_equal(np.asarray(mj)[:16384], mh[:16384]))}
print(res, flush=True)

# (b) per tick inside the world
T = 20
tick = {}
for nm, view, kind in (("coarse_no_tracker", "coarse", "jax"), ("objects_host", "objects", "host"),
                       ("objects_jax", "objects", "jax")):
    specs, parts = AW.build(tracker=kind, with_objects=(view != "coarse"))
    w = AW.MapWorld(specs[view], world_seed=0)
    d = w.designer
    ens = d.ensemble(1, seed=(9,))
    d.rollout(ens, None, T=2, rec=("L1",))                       # compile
    ens2, _ = d.rollout(ens, None, T=T, rec=("L1",))              # compile T (same shapes after)
    t0 = time.perf_counter()
    ens2, r = d.rollout(ens, None, T=T, rec=("L1",))
    tick[nm] = (time.perf_counter() - t0) / T
    print(nm, tick[nm], flush=True)
res["world_s_per_tick_member"] = tick
res["tracker_share_of_tick"] = {k: (tick[k] - tick["coarse_no_tracker"]) / tick[k] for k in ("objects_host", "objects_jax")}

# (c) vmap over 8 members on the JAX objects world
specs, parts = AW.build(tracker="jax")
w = vw.World(specs["objects"], world_seed=0)
d = w.designer
t0 = time.perf_counter()
ens = d.ensemble(8, seed=(77,))
jax.block_until_ready(ens.carry.x)
t_init = time.perf_counter() - t0
m0 = np.asarray(ens.carry.mem[0])
t0 = time.perf_counter()
ens2, r = d.rollout(ens, None, T=5, rec=("x", "L1"))
t_roll = time.perf_counter() - t0
ok_jax, ok_host = True, True
HW0, DISC = 128 * 128, [0, 14, 15, 16]
nh = trh.n_m
for b in range(8):
    m, mhb = m0[b], m0[b][:nh]                                     # same layout: host continues from it
    for t in range(1, 6):
        m = trj.update_one(m, r["x"][b, t])
        mhb = trh.update_one(mhb, r["x"][b, t])
        ok_jax &= bool(np.array_equal(trj.phi(None, m[None])[0], r["L1"][b, t]))
        ok_host &= bool(np.array_equal(m[:HW0], mhb[:HW0]) and np.array_equal(m[nh - 5:nh], mhb[nh - 5:]) and
                        np.array_equal(trj.table(m)[:, DISC], trh.table(mhb[None])[0][:, DISC]))
    ok_jax &= bool(np.array_equal(m, np.asarray(ens2.carry.mem[0])[b]))
res["vmap_world_8_members"] = {"init_burnin_s": t_init, "rollout_5_ticks_s": t_roll,
                               "memory_shape": list(np.shape(ens2.carry.mem[0])),
                               "L1_and_memory_equal_jax_replay": ok_jax,
                               "discrete_memory_equal_host_replay": ok_host,
                               "objects_present_t5": [int(v) for v in (r["L1"][:, -1].reshape(8, 12, 12)[:, :, 0] > 0.5).sum(1)]}
json.dump(res, open(f"{OUT}/speed.json", "w"), indent=1)
print(json.dumps(res, indent=1))
