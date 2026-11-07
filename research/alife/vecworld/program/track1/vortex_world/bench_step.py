import time, numpy as np, jax, jax.numpy as jnp, sys
sys.path.insert(0, '/home/user/evalwork/vecworld/program/track1/vortex_world')
import vortex_jax as VJ, dataclasses
def bench(cfg, n=250, reps=4):
    ns = VJ.make_native_step(cfg)
    q = {k: jnp.asarray(v, jnp.float64) for k, v in VJ.THETA.items()}
    Z = jnp.zeros((cfg.H, cfg.W))
    x = VJ.make_init(cfg)(q, jax.random.key(0))
    f = jax.jit(lambda x: jax.lax.fori_loop(0, n, lambda i, xx: ns(q, xx, 0.3, Z), x))
    jax.block_until_ready(f(x))
    t = time.process_time()
    for _ in range(reps): x = f(x)
    jax.block_until_ready(x)
    return (time.process_time() - t) / (n * reps) * 1e3
for H in (64, 96, 128):
    print(H, "ms/step", bench(VJ.Config(H=H, W=H)), "nomut", bench(VJ.Config(H=H, W=H, mut_dt=-1)))
