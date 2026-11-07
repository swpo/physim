import sys, time
sys.path.insert(0, '/home/user/evalwork/vecworld/program/track1/vortex_world')
import _paths, jax, jax.numpy as jnp, numpy as np, vw, vortex_jax as VJ, vortex_world as VW
cfg = VJ.Config(H=64, W=64, G=4)
lev = VJ.make_level(cfg)
q = lev.params
x = lev.init(q, jax.random.key(0))
k = jax.random.key(1)
st = jax.jit(lambda x, t: lev.step(q, x, vw.Noise(k, t), jnp.zeros(cfg.m)))
vst = jax.jit(jax.vmap(lambda x, t: lev.step(q, x, vw.Noise(k, t), jnp.zeros(cfg.m)), in_axes=(0, None)))
def b(f, x, n=6):
    y = f(x, 0); jax.block_until_ready(y)
    t = time.process_time()
    for i in range(n): y = f(y, i)
    jax.block_until_ready(y); return (time.process_time() - t) / n
print("level step B=1", b(st, x))
xb = jax.tree_util.tree_map(lambda a: jnp.stack([a] * 4), x)
print("level step vmap B=4 per member", b(vst, xb) / 4)
p1, tr = VW.phi_vortices(cfg)
m = p1.init_memory(x)
up = jax.jit(p1.update_memory)
jax.block_until_ready(up(m, x)); t = time.process_time()
for _ in range(20): m = up(m, x)
jax.block_until_ready(m); print("tracker update", (time.process_time() - t) / 20)
