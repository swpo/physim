"""bench/bench_headline.py — headline throughput battery (worlds/hour).

(i)   v2 main-run shape: pop-96 batch (96 x pred world ~9 fields, 256^2),
      T=2500tu, full locked record pipeline (blob tracking on host).
(ii)  512^2 single world, T=10000tu, records every 5tu (fields-only pulls).
(iii) 1024^2 single world, T=10000tu.
Each row: wall time, worlds/hour, and the step-only rate for comparison.
Writes rows into results/gpu_bench.json. Usage:
  python bench_headline.py popbatch|pop96|big512|big1024|steponly
pop96 uses actual T=2500; popbatch is a T=250 dress rehearsal (x10 scale).
"""
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
GPU = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, GPU)
import jax
from bench.bench_step import append          # noqa: E402
from tests.gt_worlds import world, KICKS     # noqa: E402


def pop96(T=2500.0, B=96, tag="headline_pop96", world_name="pred"):
    import blobgpu.soup as BS
    jobs = [(world(world_name), 100 + i) for i in range(B)]
    t0 = time.time()
    SS = BS.init_soup_gpu_batch(jobs, L=128.0, dtype="f32", kicks_map=KICKS)
    t_init = time.time() - t0
    t0 = time.time()
    BS.advance_gpu_batch(SS, T, progress=lambda t: print(f"t={t:.0f}",
                                                         flush=True))
    wall = time.time() - t0
    wph = B / (wall / 3600.0)
    row = dict(kind=tag, B=B, world=world_name, T=T, L=128.0,
               t_init_s=round(t_init, 1), wall_s=round(wall, 1),
               worlds_per_hour=round(wph, 1),
               statuses={s: sum(1 for w in SS["worlds"] if w["status"] == s)
                         for s in set(w["status"] for w in SS["worlds"])})
    append(row)
    print(json.dumps(row), flush=True)


def big(N, T=10000.0, world_name="pred", rec_pull=True):
    """Single world at N^2 with genome fields; records via the v2 pipeline
    (L = N*dx). Measures the large-world mode."""
    import blobgpu.soup as BS
    L = N * 0.5
    g = world(world_name)
    t0 = time.time()
    S = BS.init_soup_gpu(g, L=L, seed=1, dtype="f32")
    # scale n_soup with area? protocol is 12 pokes at L=128; for the large-world
    # bench keep 12 (this is a throughput bench, not an assay).
    t_init = time.time() - t0
    t0 = time.time()
    BS.advance_gpu(S, T)
    wall = time.time() - t0
    steps = int(round(T / 0.02))
    row = dict(kind=f"headline_big{N}", N=N, world=world_name, T=T,
               t_init_s=round(t_init, 1), wall_s=round(wall, 1),
               ms_per_step_with_records=round(1e3 * wall / steps, 4),
               status=S["status"])
    append(row)
    print(json.dumps(row), flush=True)


def steponly(N, B, world_name="pred", T=500.0):
    """Pure stepping rate at the headline shapes (no records)."""
    from bench.bench_step import setup, time_chunk
    F, p, keys, step, struct = setup(B, N, np.float32, world_name=world_name)
    ms, F = time_chunk(F, p, keys, step, K=250, R=5)
    row = dict(kind="headline_steponly", B=B, N=N, nf=struct["nf_max"],
               ms_per_step=ms)
    append(row)
    print(json.dumps(row), flush=True)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "popbatch"
    print("backend:", jax.devices(), flush=True)
    if mode == "popbatch":
        pop96(T=250.0, tag="headline_pop96_dress")
    elif mode == "pop96":
        pop96(T=2500.0)
    elif mode == "big512":
        big(512)
    elif mode == "big1024":
        big(1024)
    elif mode == "steponly":
        for N, B in ((256, 96), (512, 1), (1024, 1)):
            steponly(N, B)
