"""Timing / memory probe for the autodiff input sensitivity (coarse world, VJP through the strided level)."""
import resource
import sys
import time

import common as CM
import jax
import jax.numpy as jnp
import numpy as np

from vw.world import Carry, make_key, member_keys

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
NV = int(sys.argv[2]) if len(sys.argv) > 2 else 8
wc, parts, AW = CM.build_world("coarse")
pc = parts["phi_coarse"]
params = wc.params
st = np.load(f"{CM.RES}/states.npz")
x0 = jnp.asarray(st["x"][0])
key = member_keys(make_key(6161, 0), 1)[0]
z = jnp.zeros(wc.n_in)


def f(x):
    c = Carry(x, ((),), jnp.zeros((), jnp.int64), key)
    for _ in range(N):
        c = wc._tick(params, c, z)
    return pc.phi(c.x, ())


t0 = time.time()
y, vf = jax.jit(lambda x: jax.vjp(f, x))(x0)
y.block_until_ready()
print("forward+residuals (incl compile)", time.time() - t0, "maxrss MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e3, flush=True)
bmap = jax.jit(lambda vf, cts: jax.lax.map(lambda c: vf(c)[0], cts))
cts = jnp.eye(192)[:NV]
t0 = time.time()
G = bmap(vf, cts)
G.block_until_ready()
print("first", NV, "vjps (incl compile)", time.time() - t0, flush=True)
t0 = time.time()
G = bmap(vf, cts)
G.block_until_ready()
print(NV, "vjps", time.time() - t0, "per vjp", (time.time() - t0) / NV, "maxrss MB",
      resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e3, flush=True)
# jvp check against one VJP row
dx = jnp.zeros_like(x0).at[:, 64, 64].set(0.5)
t0 = time.time()
_, jv = jax.jit(lambda x, v: jax.jvp(f, (x,), (v,)))(x0, dx)
print("jvp (incl compile)", time.time() - t0, "row0 check", float(jv[0]), float((G[0] * dx).sum()), flush=True)
t0 = time.time()
yl, fj = jax.jit(lambda x: jax.linearize(f, x))(x0)
jl = jax.jit(lambda fj, V: jax.lax.map(fj, V))(fj, jnp.stack([dx, 2 * dx]))
print("linearize+2 jvps (incl compile)", time.time() - t0, "check", float(jl[0, 0]), float(jl[1, 0]) / 2, float(jv[0]),
      "maxrss MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e3, flush=True)
