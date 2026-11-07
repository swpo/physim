"""GPU vs CPU numerical agreement for the VW-1 gliders world from ONE shared state (job vw1-agree-001).

usage: python agree_gpu.py --out DIR [--ticks N]

The carry (level-0 state, tracker memory, time, member keys) of 2 members is built once on the CPU (init + burn-in),
copied to the accelerator with jax.device_put, and both copies are advanced one tick at a time with zero input.
After every tick: max absolute and max relative difference of level 0 and of the block view (the first 192 level-1
numbers), and whether the object view (tracker slots) still agrees exactly. Also the difference after a single
Flow-Lenia substep (stride 1 world) from the shared state, the size of one rounding step. Matmul precision 'highest'.
Writes DIR/agreement.json and DIR/progress.txt.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

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
ap.add_argument("--ticks", type=int, default=20)
args = ap.parse_args()
os.makedirs(args.out, exist_ok=True)
PROG = os.path.join(args.out, "progress.txt")


def log(msg):
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    with open(PROG, "a") as f:
        f.write(line + "\n")


cpu = jax.devices("cpu")[0]
acc = jax.devices()[0]
log(f"accelerator {acc}, cpu {cpu}")
RES = {"accelerator": str(acc), "jax": jax.__version__, "numpy": np.__version__}


def diff(a, b):
    a, b = np.asarray(a, np.float64), np.asarray(b, np.float64)
    d = np.abs(a - b)
    scale = np.maximum(np.abs(b), 1e-12)
    return dict(max_abs=float(d.max()), max_rel=float((d / scale).max()), rms=float(np.sqrt(np.mean(d * d))),
                ref_rms=float(np.sqrt(np.mean(b * b))), equal=bool(np.array_equal(a, b)))


def run(spec_key, stride=None, ticks=args.ticks):
    specs, parts = AW.build() if stride is None else AW.build(stride=stride)
    spec = specs[spec_key]
    with jax.default_device(cpu):
        w_cpu = vw.World(spec, world_seed=0)
        ens = w_cpu.designer.ensemble(2, seed=(21,))
        carry_cpu = ens.carry
    with jax.default_device(acc):
        w_acc = vw.World(spec, world_seed=0)
    carry_acc = jax.device_put(carry_cpu, acc)
    out = []
    zeros_c = jax.device_put(jnp.zeros((1, 2, w_cpu.n_in)), cpu)
    zeros_a = jax.device_put(jnp.zeros((1, 2, w_acc.n_in)), acc)
    for t in range(1, ticks + 1):
        with jax.default_device(cpu):
            carry_cpu, _ = w_cpu._rollout(w_cpu.params, carry_cpu, zeros_c, rec=())
            L_c = np.asarray(vw.world.Ensemble(w_cpu, carry_cpu, t).level(1))
            X_c = np.asarray(jax.vmap(vw.flat)(carry_cpu.x))
        with jax.default_device(acc):
            carry_acc, _ = w_acc._rollout(w_acc.params, carry_acc, zeros_a, rec=())
            L_a = np.asarray(vw.world.Ensemble(w_acc, carry_acc, t).level(1))
            X_a = np.asarray(jax.vmap(vw.flat)(carry_acc.x))
        rec = {"tick": t, "level0": diff(X_a, X_c), "block_view": diff(L_a[:, :192], L_c[:, :192])}
        if L_c.shape[1] > 192:
            rec["object_view"] = diff(L_a[:, 192:], L_c[:, 192:])
        out.append(rec)
        log(f"{spec_key} stride={stride or 20} tick {t}: level0 max_abs {rec['level0']['max_abs']:.3e}, "
            f"block max_rel {rec['block_view']['max_rel']:.3e}"
            + (f", objects equal {rec['object_view']['equal']}" if "object_view" in rec else ""))
    return out


try:
    RES["substep"] = run("coarse", stride=1, ticks=5)
    RES["both_ticks"] = run("both")
    RES["ok"] = True
except Exception as exc:
    import traceback
    RES["error"] = repr(exc)
    RES["trace"] = traceback.format_exc()[-3000:]
    RES["ok"] = False
    log(f"FAILED {exc!r}")
with open(os.path.join(args.out, "agreement.json"), "w") as f:
    json.dump(RES, f, indent=1)
sys.exit(0 if RES["ok"] else 1)
