"""bench -- CPU cost per native step, per tick and per tracker update (one core).

    python bench.py

Native step (jit, B = 1) at dt 0.5; a tick (20 native steps + channel draw); a tick under vmap for B = 4 and
B = 16 (per member); the level-1 tracker update and the level-2 update; one full World tick through
vw.World rollout (level 0 + level 1 + level 2) per member at B = 1, 4 and 16. process_time, best of 3.
Writes results/timing.json.
"""
import json
import os
import time

import _paths
import jax
import jax.numpy as jnp
import numpy as np

import vw
import membrane_jax as MJ
import membrane_world as MW


def best(f, x, n, reps=3):
    y = f(x)
    jax.block_until_ready(y)
    out = []
    for _ in range(reps):
        t = time.process_time()
        y = x
        for _ in range(n):
            y = f(y)
        jax.block_until_ready(y)
        out.append((time.process_time() - t) / n)
    return min(out)


def main():
    cfg = MJ.Config()
    lev = MJ.make_level(cfg)
    q = lev.params
    x = lev.init(q, jax.random.key(0))
    ns = MJ.make_native_step(cfg)
    Z = jnp.zeros((cfg.H, cfg.W))
    res = {}
    res["native_step_s"] = best(jax.jit(lambda x: ns(q, x, Z)), x, 200)
    k = jax.random.key(1)
    tick = jax.jit(lambda x: lev.step(q, x, vw.Noise(k, 0), jnp.zeros(cfg.m)))
    res["tick_level0_s"] = best(tick, x, 30)
    for B in (4, 16):
        xb = jax.tree_util.tree_map(lambda a: jnp.stack([a] * B), x)
        vt = jax.jit(jax.vmap(lambda x: lev.step(q, x, vw.Noise(k, 0), jnp.zeros(cfg.m))))
        res[f"tick_level0_vmap{B}_per_member_s"] = best(vt, xb, 10) / B
    # run the state forward so the tracker sees cells
    run = jax.jit(lambda x: jax.lax.fori_loop(0, 300, lambda i, xx: lev.step(q, xx, vw.Noise(k, i), jnp.zeros(cfg.m)), x))
    x = run(x)
    p1, tr = MW.phi_cells(cfg)
    m = p1.init_memory(x)
    up = jax.jit(p1.update_memory)
    res["tracker_update_s"] = best(lambda mm: up(mm, x), m, 30)
    p2 = MW.phi_population(tr.K, cfg.tick_time)
    y1 = p1.phi(x, m)
    m2 = p2.init_memory(y1)
    up2 = jax.jit(p2.update_memory)
    res["level2_update_s"] = best(lambda mm: up2(mm, y1), m2, 100)
    specs, parts = MW.build(cfg)
    w = vw.World(specs["population"], world_seed=0)
    d = w.designer
    for B in (1, 4, 16):
        ens = d.ensemble(B, seed=0)
        ens, _ = d.rollout(ens, T=2, rec=("L1", "L2"))
        ts = []
        for _ in range(2):
            t = time.process_time()
            ens, r = d.rollout(ens, T=10, rec=("L1", "L2"))
            ts.append((time.process_time() - t) / (10 * B))
        res[f"world_tick_L0_L1_L2_B{B}_per_member_s"] = min(ts)
    res["config"] = {"H": cfg.H, "dt": cfg.dt, "n_sub": cfg.n_sub, "tick_time": cfg.tick_time, "m": cfg.m,
                     "tracker": dict(MW.TRACK, **MW.slots_for(cfg)), "cpu": "one core (taskset), OMP 1, XLA single thread"}
    json.dump(res, open(os.path.join(_paths.RESULTS, "timing.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
