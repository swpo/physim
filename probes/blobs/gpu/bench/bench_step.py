"""bench/bench_step.py — per-step timing battery for the roofline analysis.

Measures ms/step for the batched stepper across:
  * batch size sweep at 256^2 (fields 12 .. 2048 via B worlds x nf fields)
  * grid sweep single world (128/256/512/1024)
  * f32 vs f64
  * fused vs unfused reaction (optimization_barrier)
  * precomputed-E vs on-the-fly exp
  * chunked fori_loop vs python-loop single steps (launch overhead)
Method: median of R repeats of a K-step chunk, after a warmup chunk (jit
compile excluded); block_until_ready for honest timing. Appends rows to
results/gpu_bench.json. Usage: python bench_step.py [quick|full]
"""
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
GPU = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, GPU)
sys.path.insert(0, os.path.join(HERE))          # pod: flat layout fallback

import jax
import jax.numpy as jnp
from blobgpu import pack_genomes, pack_states, make_stepper, diffusion_E
from blobgpu.core import batch_keys, make_single_step, enable_x64
from tests.gt_worlds import world, NAMES

OUT = os.path.join(GPU, "results", "gpu_bench.json")


def append(row):
    try:
        data = json.load(open(OUT))
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    row = dict(row)
    row.setdefault("ts", time.strftime("%Y-%m-%d %H:%M:%S"))
    row.setdefault("backend", str(jax.devices()[0]))
    data.append(row)
    tmp = OUT + ".tmp"
    json.dump(data, open(tmp, "w"), indent=1)
    os.replace(tmp, OUT)


def setup(B, N, dtype=np.float32, noise=2e-3, world_name="pred",
          precompute_E=True, unfused=False):
    """B copies of one GT world (pred: 9 fields, tanh+bilin — the rich case)."""
    if dtype is np.float64:
        enable_x64()          # else f64 arrays silently degrade to f32
    gens = [world(world_name) for _ in range(B)]
    params, struct, aux = pack_genomes(gens, dtype=dtype)
    rng = np.random.default_rng(0)
    nf = struct["nf_max"]
    F = rng.standard_normal((B, nf, N, N)).astype(dtype) * 0.1
    p = {k: jnp.asarray(v) for k, v in params.items()}
    if precompute_E:
        p["E"] = diffusion_E(params["D"], N, 0.5, 0.02, dtype)
    else:
        from blobgpu.core import k2_grid
        p["k2"] = jnp.asarray(k2_grid(N, 0.5).astype(dtype))
        p["D"] = jnp.asarray(params["D"].astype(dtype))
    step = make_stepper(struct, N, 0.5, 0.02, noise=noise,
                        precompute_E=precompute_E, unfused=unfused)
    keys = batch_keys(list(range(B)))
    return jnp.asarray(F), p, keys, step, struct


def time_chunk(F, p, keys, step, K=250, R=5):
    F = step(F, p, keys, 0, K)          # warmup + compile
    F.block_until_ready()
    ts = []
    t = K
    for _ in range(R):
        t0 = time.perf_counter()
        F = step(F, p, keys, t, K)
        F.block_until_ready()
        ts.append((time.perf_counter() - t0) / K)
        t += K
    return float(np.median(ts) * 1e3), F    # ms/step


def bench_batch_sweep(dtype=np.float32, K=250, R=5, world_name="pred",
                      Bs=(1, 2, 4, 8, 16, 32, 64, 96, 128, 224), N=256,
                      tag="batch_sweep"):
    name = {np.float32: "f32", np.float64: "f64"}[dtype]
    for B in Bs:
        try:
            F, p, keys, step, struct = setup(B, N, dtype, world_name=world_name)
            ms, F = time_chunk(F, p, keys, step, K, R)
        except Exception as e:
            append(dict(kind=tag, B=B, N=N, dtype=name, world=world_name,
                        error=str(e)[:200]))
            print(f"B={B}: ERROR {e}", flush=True)
            continue
        nf = struct["nf_max"]
        row = dict(kind=tag, B=B, N=N, nf=nf, fields=B * nf, dtype=name,
                   world=world_name, ms_per_step=ms,
                   us_per_field_step=1e3 * ms / (B * nf))
        append(row)
        print(f"B={B:4d} ({B*nf:5d} fields) {ms:8.3f} ms/step "
              f"{row['us_per_field_step']:7.2f} us/field-step", flush=True)


def bench_grid_sweep(dtype=np.float32, K=100, R=5, Ns=(128, 256, 512, 1024),
                     world_name="pred"):
    name = {np.float32: "f32", np.float64: "f64"}[dtype]
    for N in Ns:
        F, p, keys, step, struct = setup(1, N, dtype, world_name=world_name)
        ms, F = time_chunk(F, p, keys, step, K, R)
        append(dict(kind="grid_sweep", B=1, N=N, nf=struct["nf_max"],
                    dtype=name, world=world_name, ms_per_step=ms,
                    us_per_field_step=1e3 * ms / struct["nf_max"]))
        print(f"N={N:5d} {ms:8.3f} ms/step", flush=True)


def bench_ablations(N=256, B=96, K=250, R=5, world_name="pred"):
    """fused vs unfused; precomputed E vs exp-on-the-fly; fori vs python loop;
    noise on/off."""
    base = dict(kind="ablation", B=B, N=N, world=world_name, dtype="f32")
    for tag, kw in (("fused+E", dict()),
                    ("unfused", dict(unfused=True)),
                    ("expfly", dict(precompute_E=False))):
        F, p, keys, step, struct = setup(B, N, np.float32, world_name=world_name,
                                         **kw)
        ms, F = time_chunk(F, p, keys, step, K, R)
        append(dict(base, variant=tag, ms_per_step=ms))
        print(f"{tag:10s} {ms:8.3f} ms/step", flush=True)
    # noise off
    F, p, keys, step, struct = setup(B, N, np.float32, noise=0.0,
                                     world_name=world_name)
    ms, F = time_chunk(F, p, keys, step, K, R)
    append(dict(base, variant="nonoise", ms_per_step=ms))
    print(f"{'nonoise':10s} {ms:8.3f} ms/step", flush=True)
    # python-loop single steps (launch overhead)
    F, p, keys, step1, struct = setup(B, N, np.float32, world_name=world_name)
    sstep = make_single_step(struct, N, 0.5, 0.02, noise=2e-3)
    F = sstep(F, p, keys, 0)
    F.block_until_ready()
    t0 = time.perf_counter()
    KK = 50
    for i in range(KK):
        F = sstep(F, p, keys, i + 1)
    F.block_until_ready()
    ms = (time.perf_counter() - t0) / KK * 1e3
    append(dict(base, variant="python-loop", ms_per_step=ms))
    print(f"{'py-loop':10s} {ms:8.3f} ms/step", flush=True)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "quick"
    print("backend:", jax.devices(), flush=True)
    if mode == "quick":
        bench_batch_sweep(Bs=(1, 4, 16), K=100, R=3)
        return
    # full battery
    bench_batch_sweep(np.float32)
    bench_batch_sweep(np.float64, Bs=(1, 4, 16, 64, 96))
    bench_grid_sweep(np.float32)
    bench_grid_sweep(np.float64, Ns=(256, 512, 1024))
    bench_ablations()


if __name__ == "__main__":
    main()
