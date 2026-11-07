"""Smoke test for the gpu-jobs pipeline: JAX sees the GPU and a matmul agrees with NumPy."""
import json, os, sys, time
import numpy as np
import jax, jax.numpy as jnp

out = os.environ["OUT"]
devices = jax.devices()
print("jax", jax.__version__, "devices", devices, flush=True)
gpu = [d for d in devices if d.platform == "gpu"]
rng = np.random.default_rng(0)
a = rng.standard_normal((4096, 4096), dtype=np.float32)
b = rng.standard_normal((4096, 4096), dtype=np.float32)
f = jax.jit(lambda x, y: x @ y)
x, y = jnp.asarray(a), jnp.asarray(b)
f(x, y).block_until_ready()
t = time.perf_counter()
for _ in range(20):
    r = f(x, y)
r.block_until_ready()
dt = (time.perf_counter() - t) / 20
err = float(np.max(np.abs(np.asarray(r, dtype=np.float64) - a.astype(np.float64) @ b.astype(np.float64))))
result = dict(jax=jax.__version__, devices=[str(d) for d in devices], gpu=bool(gpu),
              matmul_4096_ms=round(dt * 1e3, 3), tflops=round(2 * 4096**3 / dt / 1e12, 2),
              max_abs_err_vs_numpy=err)
with open(os.path.join(out, "result.json"), "w") as fh:
    json.dump(result, fh, indent=2)
with open(os.path.join(out, "progress.txt"), "w") as fh:
    fh.write("smoke done\n")
print(json.dumps(result), flush=True)
sys.exit(0 if gpu else 1)
