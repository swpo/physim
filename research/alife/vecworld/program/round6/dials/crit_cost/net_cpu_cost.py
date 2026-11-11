"""net_cpu_cost -- CPU seconds per training step of the round-5 ladder's block-view nets (one CPU thread).

Why: decision 2's research budget is counted in level-0 episode equivalents, but its enforcement is a cap on the
sandbox's total CPU. The reference policies' nets were trained on a GPU (round5/ladder progress.txt: 206 s for
the block view's nets on an A100 40GB). This times the same jitted lockstep step on one CPU thread, with zeros of
the job's shapes (the pattern of round5/ladder/check_shapes.py; no simulation, nothing of round 5 is changed or
written), and converts the declared schedules to gliders episode equivalents.

usage (one process, a few CPU-minutes):
  OMP_NUM_THREADS=1 nice -n 10 python -B net_cpu_cost.py  -> results/net_cpu_cost.json
"""
import json
import os
import sys
import time

os.environ.setdefault("XLA_FLAGS", "--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1")
HERE = os.path.dirname(os.path.abspath(__file__))
LAD = os.path.abspath(os.path.join(HERE, "..", "..", "..", "round5", "ladder"))
sys.path.insert(0, LAD)
import ladder_lib as LL  # noqa: E402
import ladder_net as NN  # noqa: E402

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

T1 = 33                 # P + H + 1, as in check_shapes.py
E = 256                 # episodes in the fake data set: the step's cost depends on BATCH x M_TRAIN, not on E
N_STEPS = 12            # timed steps after the first (which holds the compilation)
CPU_S_PER_MEMBER_TICK = 0.15   # round5/agentenv/results/summary.json [cost.value.cpu_s_per_member_tick.gliders.value]
EPISODE_TICKS = 82             # burn 50 + P 16 + H 16 (round5/ladder/results/summary.json [config])


def fake_obs(E, rng):
    obs = np.zeros((E, T1, LL.N_OBS), np.float32)
    O = np.zeros((E, T1, LL.K, LL.NF), np.float32)
    O[..., 0] = rng.random((E, T1, LL.K)) < 0.6
    O[..., 3], O[..., 5] = O[..., 0], O[..., 0]
    obs[..., LL.NC:] = O.reshape(E, T1, -1)
    obs[..., :LL.NC] = rng.normal(size=(E, T1, LL.NC)).astype(np.float32)
    return obs, rng.normal(size=(E, T1 - 1, LL.NW)).astype(np.float32)


def time_case(view, cond, n_nets, rng):
    obs, U = fake_obs(E, rng)
    th = np.zeros((E, 8), np.float32) if cond else None
    SC = {"SC1": LL.SC1, "SCF": np.ones(LL.NF), "SCO": np.ones(LL.NO), "SCP": np.ones(5), "POPM": np.zeros(5)}
    ds = NN.make_dataset(view, obs, U, SC, theta_u=th, seed=1)
    D = NN.stack_datasets([ds] * n_nets)
    vstep, _ = NN._fns(view, cond, tuple(sorted(D)))
    P = jax.vmap(lambda k: NN.init_params(view, k, cond))(jax.random.split(jax.random.key(0), n_nets))
    st = {"t": jnp.zeros((n_nets,), jnp.float32), "m": jax.tree_util.tree_map(jnp.zeros_like, P),
          "v": jax.tree_util.tree_map(jnp.zeros_like, P)}
    key = jax.random.key(1)
    t0w, t0c = time.time(), time.process_time()
    P, st, l = vstep(P, st, D, jax.random.split(key, n_nets), 1e-3)
    l.block_until_ready()
    first = (time.time() - t0w, time.process_time() - t0c)
    t0w, t0c = time.time(), time.process_time()
    for i in range(N_STEPS):
        key, sub = jax.random.split(key)
        P, st, l = vstep(P, st, D, jax.random.split(sub, n_nets), 1e-3)
    l.block_until_ready()
    wall, cpu = (time.time() - t0w) / N_STEPS, (time.process_time() - t0c) / N_STEPS
    return {"view": view, "cond": cond, "nets_in_lockstep": n_nets, "batch": NN.Cfg.BATCH, "m_train": NN.Cfg.M_TRAIN,
            "first_step_wall_s": round(first[0], 2), "first_step_cpu_s": round(first[1], 2),
            "wall_s_per_step": round(wall, 4), "cpu_s_per_step": round(cpu, 4), "timed_steps": N_STEPS,
            "finite": bool(np.isfinite(np.asarray(l)).all())}


def main():
    rng = np.random.default_rng(0)
    out = {"what": "CPU cost of one training step of the round-5 ladder nets, one thread, zeros-shaped data",
           "jax": jax.__version__, "backend": jax.default_backend(), "threads": os.environ.get("OMP_NUM_THREADS"),
           "load_average": os.getloadavg(), "cases": [], "cpu_s_per_member_tick_gliders": CPU_S_PER_MEMBER_TICK,
           "episode_ticks": EPISODE_TICKS}
    for view, cond, n in (("block", True, 1), ("pop", True, 1)):
        r = time_case(view, cond, n, rng)
        out["cases"].append(r)
        print(r, flush=True)
    ep = CPU_S_PER_MEMBER_TICK * EPISODE_TICKS
    b = out["cases"][0]["cpu_s_per_step"]
    # schedules: round5/ladder/results/summary.json [config.steps_cond, steps_p0]
    out["block_view_schedules"] = {
        name: {"steps": s, "cpu_hours": round(s * b / 3600, 2), "gliders_episode_equivalents": int(round(s * b / ep))}
        for name, s in (("conditioned net (C, P0, S), 6000 steps", 6000), ("unconditioned P0u, 3000 steps", 3000))}
    out["note"] = ("episode equivalents = steps x cpu_s_per_step / (0.15 CPU-s x 82 ticks); a shared 4-core machine, so "
                   "read the per-step time to a factor of about 1.5; validation passes are not timed")
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "results", "net_cpu_cost.json"), "w"), indent=1)
    print(json.dumps(out["block_view_schedules"], indent=1))


if __name__ == "__main__":
    main()
