"""bench/bench_cudagraph.py — launch-overhead experiments: XLA command buffers
(CUDA graphs) on/off for the small-batch and single-world shapes.
XLA custom calls (cuFFT) historically break graph capture; measure, don't guess.
Usage: run twice with different XLA_FLAGS (set by pod/run_cudagraph.sh).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
GPU = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, GPU)
import numpy as np
import jax
from bench.bench_step import setup, time_chunk, append

tag = sys.argv[1] if len(sys.argv) > 1 else "default"
print("backend:", jax.devices(), "flags:", os.environ.get("XLA_FLAGS", ""),
      flush=True)
for B, N in ((1, 256), (4, 256), (96, 256), (1, 512), (1, 1024)):
    F, p, keys, step, struct = setup(B, N, np.float32)
    ms, F = time_chunk(F, p, keys, step, K=250, R=5)
    append(dict(kind="cudagraph_exp", variant=tag, B=B, N=N,
                xla_flags=os.environ.get("XLA_FLAGS", ""),
                ms_per_step=ms))
    print(f"{tag} B={B} N={N}: {ms:.4f} ms/step", flush=True)
