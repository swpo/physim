"""cpu_part -- study foundrylong: what an exam profile on this setting would need in the agent environment (CPU).

    taskset -c 0,1 python -B cpu_part.py --dtype float64 --out results/cpu_float64.json
    taskset -c 0,1 python -B cpu_part.py --dtype float32 --out results/cpu_float32.json --no-nets

Measured on 2 cores of this container (the caller pins them with taskset; JAX's CPU backend then has 2 threads):
  speed     member-ticks per second of the 64 x 64 automaton for batches of 1, 8, 32, 128 members (one jitted
            scan of 32 ticks per call, compilation excluded, best of 3 calls), a full episode of 348 ticks
  nets      (float64 process only; the nets are float32 either way) ms per training step of ONE net of the reference
            family at batch 64 and 256, and seconds for 32 samples at 3 horizons for one item
  bundle    bytes of one instance bundle's parts from a small simulated sample: raw float32 and npz-compressed
PILOT ONLY: the world used is a public pilot world (seed2027-46).
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ap = argparse.ArgumentParser()
ap.add_argument("--dtype", default="float64", choices=("float64", "float32"))
ap.add_argument("--out", required=True)
ap.add_argument("--no-nets", action="store_true")
a = ap.parse_args()

import fl_lib as LL  # noqa: E402

FL, NN = LL.FL, LL.NN
import jax  # noqa: E402

if a.dtype == "float32":
    jax.config.update("jax_enable_x64", False)
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from jax import lax  # noqa: E402

import tnca as TN  # noqa: E402
from vw.core import Noise  # noqa: E402

FAM = TN.FAM
DT = jnp.float64 if a.dtype == "float64" else jnp.float32
th = {k: jnp.asarray(v, DT) for k, v in TN.draw_theta(2027, 46).items()}
out = dict(PILOT_NEVER_REUSE_AS_EXAM=True, dtype=a.dtype, affinity=sorted(os.sched_getaffinity(0)), jax=jax.__version__,
           what="foundry automaton 64 x 64, 2 kinds, 4 substeps per tick; world seed2027-46")
EP_TICKS = 300 + LL.P + LL.H


def roll(B, T):
    def one(x, k):
        def body(x, t):
            xn = TN.tick(th, x, Noise(k, t), jnp.zeros((FAM.NW,), DT), FAM)
            return xn, TN.block_view(xn).reshape(-1)
        return lax.scan(body, x, jnp.arange(T))
    f = jax.jit(jax.vmap(one))
    keys = jax.vmap(lambda i: jax.random.fold_in(jax.random.key(7), i))(jnp.arange(B))
    x0 = jax.vmap(lambda k: TN.init(th, k, FAM))(keys).astype(DT)
    return f, x0, keys


speed = {}
obs_sample = None
for B in (1, 8, 32, 128):
    T = 32
    f, x, keys = roll(B, T)
    x, y = f(x, keys)
    y.block_until_ready()                                # compilation
    best = 1e9
    for _ in range(3):
        t = time.time()
        x, y = f(x, keys)
        y.block_until_ready()
        best = min(best, time.time() - t)
    speed[str(B)] = dict(member_ticks_per_s=B * T / best, seconds_per_call=best, ticks=T, dtype=str(y.dtype))
    print("speed", B, speed[str(B)], flush=True)
    if B == 32:
        obs_sample = np.asarray(y, np.float32)           # (32, 32, 192)
out["speed"] = speed
bestB = max(speed, key=lambda k: speed[k]["member_ticks_per_s"])
r = speed[bestB]["member_ticks_per_s"]
out["episode"] = dict(ticks=EP_TICKS, burn_in=300, history=LL.P, test=LL.H, best_batch=int(bestB), member_ticks_per_s=r,
                      cpu_seconds_per_full_episode_on_2_cores=EP_TICKS / r, core_seconds_per_full_episode=2 * EP_TICKS / r,
                      question=dict(members=32, ticks=LL.H, member_ticks=32 * LL.H, seconds_on_2_cores=32 * LL.H / speed["32"]["member_ticks_per_s"]))

# ---- instance bundle: sizes of the parts (float32), compression measured on the simulated sample
def nbytes(*shape):
    return int(np.prod(shape)) * 4


def ratio(arr):
    b = io.BytesIO()
    np.savez_compressed(b, a=arr)
    return b.getbuffer().nbytes / arr.nbytes


cr = ratio(obs_sample)
parts = dict(lab_obs_32_episodes=nbytes(32, LL.T1, LL.NOBS), lab_programs_32_episodes=nbytes(32, LL.P + LL.H, LL.NW),
             item_histories_96=nbytes(96, LL.P + 1, LL.NOBS), item_programs_96=nbytes(96, LL.H, LL.NW),
             replicate_futures_96x12x3=nbytes(96, 12, LL.NH, LL.NOBS), climatology_96x3=nbytes(96, LL.NH, LL.NOBS),
             replicate_futures_all_32_ticks_96x12=nbytes(96, 12, LL.H, LL.NOBS))
pub = parts["lab_obs_32_episodes"] + parts["lab_programs_32_episodes"] + parts["item_histories_96"] + parts["item_programs_96"]
sealed = parts["replicate_futures_96x12x3"] + parts["climatology_96x3"]
out["bundle"] = dict(parts_bytes_float32=parts, block_view_npz_ratio=cr, public_bytes=pub, sealed_bytes=sealed, total_bytes=pub + sealed,
                     total_bytes_compressed_estimate=int(cr * (pub + sealed - parts["lab_programs_32_episodes"] - parts["item_programs_96"])
                                                         + 0.05 * (parts["lab_programs_32_episodes"] + parts["item_programs_96"])),
                     note="programs are sparse (zero outside 4 ticks) and compress to a few percent; block views are dense floats",
                     build_member_ticks=dict(lab=32 * EP_TICKS, items_history=96 * (300 + LL.P), futures=96 * 12 * LL.H, climatology=96 * EP_TICKS))
out["bundle"]["build_member_ticks"]["total"] = sum(out["bundle"]["build_member_ticks"].values())
out["bundle"]["build_seconds_on_2_cores"] = out["bundle"]["build_member_ticks"]["total"] / r

# ---- nets on CPU
if not a.no_nets:
    NN.Cfg.CHUNK = 10
    rng = np.random.default_rng(0)
    E = 64
    obs = np.abs(rng.standard_normal((E, LL.T1, LL.NOBS), np.float32)) + 0.1
    U = np.zeros((E, LL.P + LL.H, LL.NW), np.float32)
    CN = json.load(open(os.path.join(HERE, "inputs", "code_norm.json")))
    smu, ssd = np.asarray(CN["mean"], np.float32), np.asarray(CN["sd"], np.float32)
    ds = LL.make_ds(obs, U, smu, ssd, seed=0)
    nets = {}
    best = None
    for batch in (64, 256):
        best, inf = LL.train(ds, 40, [0], batch=batch, eval_every=40)
        nets[f"ms_per_step_one_net_batch{batch}"] = inf["ms_per_step"]
        print("net", batch, inf["ms_per_step"], flush=True)
    D0 = NN.item_dataset(obs[:1, : LL.P + 1], np.zeros((1, LL.H, LL.NW)), smu, ssd)
    bk = LL.tree_at(best, slice(None), 0)
    LL.samples_h(bk, D0, 32, 1)
    t = time.time()
    for _ in range(5):
        LL.samples_h(bk, D0, 32, 1)
    nets["seconds_per_item_32_samples_3_horizons"] = (time.time() - t) / 5
    out["nets"] = nets
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
with open(a.out, "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out["episode"], indent=1))
print("wrote", a.out)
