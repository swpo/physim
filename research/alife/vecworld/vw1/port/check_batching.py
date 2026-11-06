"""Batching and pathwise reproducibility on the chaotic A_gliders level (coarse world).

usage: python -B check_batching.py   -> results/batching_check.json

From one common post-burn-in ensemble (same states, same member keys), compare the level-0 states
reached by (i) MapWorld (lax.map), (ii) vw.World (vmap, B = 4) and (iii) vw.World with the same
members inside a larger batch (B = 8), after 1, 2, 5, 10 and 20 ticks. Noise draws are identical
(counter-based keys); any difference is floating-point rounding from different compiled batch
layouts, amplified by the dynamics (finite-time Lyapunov rate ~0.23 per substep, check_level0).
"""
import json

import _paths
import jax
import jax.numpy as jnp
import numpy as np

import vw
import aworld as AW

specs, parts = AW.build(with_objects=False)
wm = AW.MapWorld(specs["coarse"], world_seed=0)
wv = vw.World(specs["coarse"], world_seed=0)
ens = wm.designer.ensemble(4, seed=(9,))
x0, keys = ens.carry.x, ens.carry.key
x8 = jnp.concatenate([x0, x0[::-1] * 1.0])
k8 = jnp.concatenate([keys, keys[::-1]])
marks = (1, 2, 5, 10, 20)
res = {"ticks": list(marks)}
em = wm.designer.from_states(x0, keys=keys)
ev = wv.designer.from_states(x0, keys=keys)
e8 = wv.designer.from_states(x8, keys=k8)
d_mv, d_v8, t = [], [], 0
for m in marks:
    em, _ = wm.designer.rollout(em, None, T=m - t, rec=())
    ev, _ = wv.designer.rollout(ev, None, T=m - t, rec=())
    e8, _ = wv.designer.rollout(e8, None, T=m - t, rec=())
    t = m
    a, b, c = np.asarray(em.carry.x), np.asarray(ev.carry.x), np.asarray(e8.carry.x)[:4]
    d_mv.append(float(np.abs(a - b).max()))
    d_v8.append(float(np.abs(b - c).max()))
    print(m, d_mv[-1], d_v8[-1], flush=True)
res["max_abs_laxmap_vs_vmap4"] = d_mv
res["max_abs_vmap4_vs_vmap8_same_members"] = d_v8
# a single unbatched member (jit of the tick) against lax.map member 0, one tick
c0 = jax.tree_util.tree_map(lambda q: q[0], ens.carry)
one = jax.jit(lambda c: wm._tick(wm.params, c, jnp.zeros(wm.n_in)))(c0)
em1, _ = wm.designer.rollout(wm.designer.from_states(x0, keys=keys), None, T=1, rec=())
res["unbatched_vs_laxmap_1tick_max_abs"] = float(np.abs(np.asarray(one.x) - np.asarray(em1.carry.x)[0]).max())
json.dump(res, open(f"{_paths.RESULTS}/batching_check.json", "w"), indent=1)
print(json.dumps(res, indent=1))
