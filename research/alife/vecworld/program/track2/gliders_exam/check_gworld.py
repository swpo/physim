"""check_gworld -- gworld.tick at default theta vs actuation/wind.WindWorld.tick_x (u_kick = 0), and timing.

From 2 saved states (fresh/inputs/results/states.npz), 3 ticks at sigma_w = 0.05 with the same noise
keys: max |A_gworld - A_wind|. Then the per-member Runner at default theta and at a perturbed theta:
compile and per-member-tick time. Output: results/check_gworld.json.
"""
import json
import time

import jax
import jax.numpy as jnp
import numpy as np

import gworld as GW
from vw.core import Noise
from vw.world import make_key, member_keys

out = {}
z = np.load("/home/user/evalwork/vecworld/vw1/fresh/inputs/results/states.npz")
X = jnp.asarray(z["x"][:2])
WW = GW.WD.WindWorld()
p_def = GW.theta_to_params({})
kp = jax.random.fold_in(make_key(4242, 0), GW._ST_PROC)
f_w = jax.jit(lambda A, t: WW.tick_x(WW.params, A, Noise(kp, t), jnp.zeros((GW.H * GW.W,)), jnp.zeros((GW.NW,)), 0.05))
f_g = jax.jit(lambda A, t: GW.tick(p_def, A, Noise(kp, t), jnp.zeros((GW.NW,)), 0.05))
rows = []
for b in range(2):
    Aw, Ag = X[b], X[b]
    for t in range(3):
        Aw, Ag = f_w(Aw, t), f_g(Ag, t)
        rows.append(float(jnp.abs(Aw - Ag).max()))
out["equivalence_default_theta"] = {"max_abs_level0_per_tick": rows, "states": 2, "ticks": 3, "sigma_w": 0.05,
                                    "note": "gworld traces theta_A, n, gw; alpha uses x ** n with a traced n"}
print(out, flush=True)

R = GW.Runner()
B, T = 3, 10
th = [{}, {"lh": 1.15, "lR": 0.9}, {"dm": 0.2, "lA": 1.2, "n": 2.5, "gw": 1.3}]
P = GW.stack_params([GW.theta_to_params(t) for t in th])
k = member_keys(make_key(77, 1), B)
sig = jnp.full((B,), 0.05)
A0 = jnp.asarray(z["x"][2:2 + B])
m0 = jax.vmap(R.bt.init_memory)(A0)
t0 = time.time()
res = R.run(P, A0, m0, GW.dyn_keys(k), jnp.zeros((B,), jnp.int64), jnp.zeros((B, T, GW.NW)), sig)
jax.block_until_ready(res)
t1 = time.time()
res = R.run(P, A0, m0, GW.dyn_keys(k), jnp.zeros((B,), jnp.int64), jnp.zeros((B, T, GW.NW)), sig)
jax.block_until_ready(res)
t2 = time.time()
y = np.asarray(res[0])
pop = GW.population(y)
out["timing"] = {"compile_plus_first_s": t1 - t0, "second_call_s": t2 - t1,
                 "s_per_member_tick": (t2 - t1) / (B * T), "B": B, "T": T}
out["population_last_tick"] = pop[:, -1].tolist()
out["finite"] = bool(np.isfinite(y).all())
print(out, flush=True)
json.dump(out, open(f"{GW.RES}/check_gworld.json", "w"), indent=1)
