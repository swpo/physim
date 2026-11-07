"""GPU benchmark for the VW-1 gliders world (job vw1-bench-001).

usage: python bench_gpu.py --out DIR [--quick]

A. Throughput of the gliders world (one tick = 20 Flow-Lenia substeps, 2 x 128 x 128, float64, noise on):
   member-ticks per second with vw.World (members batched by jax.vmap) for B = 1, 8, 64, 256, for the
   'both' world (block view + JAX object tracker) and the 'coarse' world (block view only). Inputs are
   zero device arrays passed straight to the compiled rollout, so host-side input building is not timed.
B. The JAX object tracker alone: memory updates per second under vmap.
C. GPU vs CPU agreement in float64 on the same pod: the same members (same keys) initialised and run on
   the GPU and on the CPU backend; max relative differences of level 0 and level 1 after 0, 1 and 10 ticks
   (chaos amplifies rounding; both are reported). Matmul precision is set to 'highest'.
D. A conv autoencoder training step in float32 on 2 x 128 x 128 inputs (batch 64 and 256), Adam written
   out, steps per second.
Writes DIR/results.json and DIR/progress.txt. Exits non-zero if a section fails.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _paths  # noqa: E402,F401
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

jax.config.update("jax_default_matmul_precision", "highest")

import vw  # noqa: E402
import aworld as AW  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--quick", action="store_true", help="tiny sizes for a CPU smoke test")
args = ap.parse_args()
os.makedirs(args.out, exist_ok=True)
PROG = os.path.join(args.out, "progress.txt")
RES = {"versions": {"python": platform.python_version(), "jax": jax.__version__, "numpy": np.__version__},
       "devices": [str(d) for d in jax.devices()], "backend": jax.default_backend(), "quick": args.quick}
FAILED = []


def log(msg):
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    with open(PROG, "a") as f:
        f.write(line + "\n")


def save():
    with open(os.path.join(args.out, "results.json"), "w") as f:
        json.dump(RES, f, indent=1, default=str)


def block(tree):
    jax.tree_util.tree_map(lambda a: a.block_until_ready() if hasattr(a, "block_until_ready") else a, tree)
    return tree


log(f"devices {RES['devices']}  jax {jax.__version__}")
specs, parts = AW.build()  # default tracker='jax'
RES["tracker_kind"] = parts.get("tracker_kind")

# ---------------------------------------------------------------- A. world throughput
SIZES = [1, 2] if args.quick else [1, 8, 64, 256]
T = 2 if args.quick else 10
REPS = 1 if args.quick else 3
RES["throughput"] = {}
for view in ("both", "coarse"):
    for B in SIZES:
        key = f"{view}_B{B}"
        try:
            w = vw.World(specs[view], world_seed=0)
            d = w.designer
            t0 = time.perf_counter()
            ens = d.ensemble(B, seed=(11,))
            block(ens.carry)
            t_init = time.perf_counter() - t0
            A = jnp.zeros((T, B, w.n_in))
            t0 = time.perf_counter()
            c, out = w._rollout(w.params, ens.carry, A, rec=("L1",))
            block((c, out))
            t_compile = time.perf_counter() - t0
            times = []
            for _ in range(REPS):
                t0 = time.perf_counter()
                c, out = w._rollout(w.params, c, A, rec=("L1",))
                block((c, out))
                times.append(time.perf_counter() - t0)
            best = min(times)
            mem = None
            try:
                st = jax.devices()[0].memory_stats() or {}
                mem = {k: st.get(k) for k in ("peak_bytes_in_use", "bytes_in_use", "bytes_limit")}
            except Exception:
                pass
            RES["throughput"][key] = dict(B=B, T=T, init_s_incl_burn_in_and_compile=t_init,
                                          first_rollout_s_incl_compile=t_compile, rollout_s=times,
                                          member_ticks_per_s=B * T / best, s_per_member_tick=best / (B * T),
                                          memory=mem)
            log(f"A {key}: {B * T / best:.1f} member-ticks/s (init {t_init:.1f}s, compile+first {t_compile:.1f}s)")
        except Exception as exc:
            RES["throughput"][key] = {"error": repr(exc), "trace": traceback.format_exc()[-2000:]}
            FAILED.append(f"A {key}")
            log(f"A {key} FAILED: {exc!r}")
        save()

# ---------------------------------------------------------------- B. tracker alone
try:
    po = parts["phi_objects"]
    lev = parts["level"]
    Bt = 2 if args.quick else 256
    w = vw.World(specs["coarse"], world_seed=0)
    ens = w.designer.ensemble(Bt, seed=(12,))
    X = block(ens.carry.x)
    init_m = jax.jit(jax.vmap(po.init_memory))
    upd = jax.jit(jax.vmap(po.update_memory))
    m = block(init_m(X))
    t0 = time.perf_counter()
    m = block(upd(m, X))
    t_c = time.perf_counter() - t0
    times = []
    for _ in range(3):
        t0 = time.perf_counter()
        m = block(upd(m, X))
        times.append(time.perf_counter() - t0)
    RES["tracker"] = dict(B=Bt, first_s_incl_compile=t_c, update_s=times, updates_per_s=Bt / min(times))
    log(f"B tracker: {Bt / min(times):.1f} member-updates/s")
except Exception as exc:
    RES["tracker"] = {"error": repr(exc), "trace": traceback.format_exc()[-2000:]}
    FAILED.append("B tracker")
    log(f"B FAILED: {exc!r}")
save()

# ---------------------------------------------------------------- C. GPU vs CPU agreement
try:
    cpu = jax.devices("cpu")[0]
    acc = jax.devices()[0]
    res = {}
    if acc.platform == "cpu":
        res["note"] = "no accelerator: CPU against CPU (sanity only)"

    def run_on(dev):
        with jax.default_device(dev):
            w = vw.World(specs["both"], world_seed=0)
            ens = w.designer.ensemble(2, seed=(13,))
            x0, l0 = np.asarray(jax.vmap(vw.flat)(ens.carry.x)), np.asarray(ens.level(1))
            A1 = jnp.zeros((1, 2, w.n_in))
            c1, _ = w._rollout(w.params, ens.carry, A1, rec=())
            e1 = vw.world.Ensemble(w, c1, 1)
            x1, l1 = np.asarray(jax.vmap(vw.flat)(c1.x)), np.asarray(e1.level(1))
            A9 = jnp.zeros((9, 2, w.n_in))
            c10, _ = w._rollout(w.params, c1, A9, rec=())
            e10 = vw.world.Ensemble(w, c10, 10)
            x10, l10 = np.asarray(jax.vmap(vw.flat)(c10.x)), np.asarray(e10.level(1))
        return dict(x0=x0, l0=l0, x1=x1, l1=l1, x10=x10, l10=l10)

    g = run_on(acc)
    h = run_on(cpu)
    for k in g:
        a, b = g[k], h[k]
        den = np.maximum(np.abs(b), 1e-300)
        res[k] = dict(max_abs=float(np.max(np.abs(a - b))), max_rel=float(np.max(np.abs(a - b) / np.maximum(den, 1e-12))),
                      equal=bool(np.array_equal(a, b)))
    RES["agreement"] = res
    log("C agreement: " + ", ".join(f"{k} max_abs {v['max_abs']:.2e}" for k, v in res.items() if isinstance(v, dict)))
except Exception as exc:
    RES["agreement"] = {"error": repr(exc), "trace": traceback.format_exc()[-2000:]}
    FAILED.append("C agreement")
    log(f"C FAILED: {exc!r}")
save()

# ---------------------------------------------------------------- D. conv autoencoder training step (float32)
try:
    def conv(x, w, stride):
        return jax.lax.conv_general_dilated(x, w, (stride, stride), "SAME", dimension_numbers=("NCHW", "OIHW", "NCHW"))

    def deconv(x, w, stride):
        return jax.lax.conv_transpose(x, w, (stride, stride), "SAME", dimension_numbers=("NCHW", "OIHW", "NCHW"))

    def init(key):
        ks = jax.random.split(key, 6)
        f = lambda k, o, i, s: (jax.random.normal(k, (o, i, s, s), jnp.float32) / np.sqrt(i * s * s)).astype(jnp.float32)
        return dict(e1=f(ks[0], 32, 2, 4), e2=f(ks[1], 64, 32, 4), e3=f(ks[2], 8, 64, 3),
                    d1=f(ks[3], 64, 8, 3), d2=f(ks[4], 32, 64, 4), d3=f(ks[5], 2, 32, 4))

    def model(p, x):
        h = jax.nn.gelu(conv(x, p["e1"], 4))
        h = jax.nn.gelu(conv(h, p["e2"], 2))
        z = conv(h, p["e3"], 1)
        h = jax.nn.gelu(deconv(z, p["d1"], 1))
        h = jax.nn.gelu(deconv(h, p["d2"], 2))
        return deconv(h, p["d3"], 4)

    def loss(p, x):
        return jnp.mean((model(p, x) - x) ** 2)

    @jax.jit
    def step(p, m, v, t, x):
        g = jax.grad(loss)(p, x)
        m = jax.tree_util.tree_map(lambda a, b: 0.9 * a + 0.1 * b, m, g)
        v = jax.tree_util.tree_map(lambda a, b: 0.999 * a + 0.001 * b * b, v, g)
        p = jax.tree_util.tree_map(lambda a, b, c: (a - 1e-3 * (b / (1 - 0.9 ** t)) / (jnp.sqrt(c / (1 - 0.999 ** t)) + 1e-8)).astype(jnp.float32), p, m, v)
        return p, m, v

    RES["conv_ae"] = {}
    for Bc in ([4] if args.quick else [64, 256]):
        p = init(jax.random.key(0))
        m = jax.tree_util.tree_map(jnp.zeros_like, p)
        v = jax.tree_util.tree_map(jnp.zeros_like, p)
        x = jax.random.normal(jax.random.key(1), (Bc, 2, 128, 128), jnp.float32)
        t0 = time.perf_counter()
        p, m, v = block(step(p, m, v, 1.0, x))
        t_c = time.perf_counter() - t0
        n = 3 if args.quick else 50
        t0 = time.perf_counter()
        for i in range(n):
            p, m, v = step(p, m, v, float(i + 2), x)
        block(p)
        dt = time.perf_counter() - t0
        RES["conv_ae"][f"B{Bc}"] = dict(batch=Bc, first_step_s_incl_compile=t_c, steps=n, steps_per_s=n / dt,
                                        samples_per_s=n * Bc / dt)
        log(f"D conv AE B{Bc}: {n / dt:.1f} steps/s")
except Exception as exc:
    RES["conv_ae"] = {"error": repr(exc), "trace": traceback.format_exc()[-2000:]}
    FAILED.append("D conv_ae")
    log(f"D FAILED: {exc!r}")
save()

RES["failed_sections"] = FAILED
save()
log("done" + (f" with failures: {FAILED}" if FAILED else ""))
sys.exit(1 if FAILED else 0)
