"""Where does rollout time go? rec variants and burn-in (scan with constant zero input)."""
import sys, time
sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/port")
import _paths  # noqa
import jax, jax.numpy as jnp, numpy as np
import aworld as AW
specs, parts = AW.build()
w = AW.MapWorld(specs["both"], world_seed=0)
d = w.designer
ens = d.ensemble(4, seed=(5,))
for rec in [(), ("L1",), ()]:
    for rep in range(2):
        t0 = time.time(); e2, r = d.rollout(ens, None, T=10, rec=rec); jax.block_until_ready(e2.carry.x)
        print(rec, rep, round(time.time() - t0, 2), "s per 40 member-ticks", flush=True)
# constant-zero-input scan (as in burn-in) on the same carry
z = jnp.zeros(w.n_in)
f = jax.jit(lambda c: jax.lax.map(lambda cb: jax.lax.scan(lambda cc, _: (w._tick(w.params, cc, z), None), cb, None, length=10)[0], c))
for rep in range(2):
    t0 = time.time(); c2 = f(ens.carry); jax.block_until_ready(c2.x)
    print("const-zero scan", rep, round(time.time() - t0, 2), flush=True)
# coarse-only world (no tracker callback)
specs2, _ = AW.build(with_objects=False)
wc = AW.MapWorld(specs2["coarse"], world_seed=0)
ec = wc.designer.from_states(ens.carry.x, keys=ens.carry.key)
for rep in range(2):
    t0 = time.time(); e3, r = wc.designer.rollout(ec, None, T=10, rec=()); jax.block_until_ready(e3.carry.x)
    print("coarse-only world", rep, round(time.time() - t0, 2), flush=True)
