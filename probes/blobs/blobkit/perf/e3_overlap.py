"""e3_overlap.py — E3: can a blob-stats jit call overlap the stepping jit?

Question: XLA/jax dispatches are async; do two INDEPENDENT jitted calls
(step_chunk on tensor A; ccl+stats on tensor B) actually overlap on one
CUDA stream, or serialize? jax uses ONE compute stream per device — the
expectation is SERIALIZATION of kernels, but stats kernels are small and
the practical question is the WALL of interleaved [step; stats] vs
[step] + [stats] run separately.

Also measures the D2H pull overlap: pulling the (tiny) stats rows while
the next step chunk runs (different stream for D2H in XLA) — the real
pipeline shape: step k+1 dispatched, then stats(k) pulled.

Setup: b14-class batch B=32 (nf 13) N=256 step chunk of 250 steps
(realistic REC chunk) + ccl(4,8)+stats on a (112, 256, 256) acts block.
Rows -> experiments.jsonl.
"""
import json, os, time
import numpy as np

import jax
import jax.numpy as jnp

from blobkit import worlds as W
from blobkit import genome as G
from blobkit.soup import sim_cpu as SC
from blobkit.soup import sim_gpu as SG

import e1c_scattermin as E1C
import e1b_pointerjump as E1B

OUT = os.path.expanduser("~/perf/results/experiments.jsonl")


def emit(row):
    row["ts"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(OUT, "a") as f:
        f.write(json.dumps(row, default=str) + "\n")
    print("[row]", json.dumps(row, default=str)[:500], flush=True)


def main():
    # --- realistic stepping batch: 32 lanes of ds3_014 (b14 class)
    B = 32
    g = W.load("ds3_014")
    jobs = [(g, 1 + i) for i in range(B)]
    master = SG.init_soup_gpu_batch(jobs, L=128.0, dtype="f32")
    Gd = master["worlds"][0]["_gpu"]
    step, params, keys = Gd["step"], Gd["params"], Gd["keys"]
    F = Gd["F"]
    N = Gd["N"]
    na_max = Gd["struct"]["na_max"]
    NSTEP = 250

    # --- stats input: real advanced acts block (B*na fields)
    S = SC.init_soup(g, L=128.0, seed=1, workers=4)
    SC.advance(S, 1000.0)
    acts1 = np.asarray(S["F"][:S["na"]], np.float32)      # (na, N, N)
    thr1 = np.asarray(S["thr_a"], np.float32)
    nf = B * S["na"]
    acts = np.tile(acts1, (B, 1, 1))[:nf]                 # (112, N, N)
    thrs = np.tile(thr1, B)[:nf]
    mask = jnp.asarray(acts > thrs[:, None, None])
    u32 = jnp.asarray(acts)
    t32 = jnp.asarray(thrs)

    ccl = E1C.make_ccl(N, 4, 8)
    stats = E1B.make_blobstats(N, 256)

    # compile everything
    F1 = step(F, params, keys, 0, NSTEP); F1.block_until_ready()
    lab, conv = ccl(mask)
    rs = stats(lab, u32, t32)
    jax.block_until_ready(rs)

    reps = 10
    # A) step alone
    t0 = time.perf_counter()
    Fs = F1
    for r in range(reps):
        Fs = step(Fs, params, keys, (r + 1) * NSTEP, NSTEP)
    Fs.block_until_ready()
    step_s = (time.perf_counter() - t0) / reps

    # B) stats alone (ccl + stats + tiny pull)
    t0 = time.perf_counter()
    for r in range(reps):
        lab, conv = ccl(mask)
        rs = stats(lab, u32, t32)
        pulled = [np.asarray(x) for x in rs[:7]]
    stats_s = (time.perf_counter() - t0) / reps

    # C) interleaved: dispatch step k+1, THEN run stats(k) + pull
    t0 = time.perf_counter()
    Fs2 = Fs
    for r in range(reps):
        Fs2 = step(Fs2, params, keys, (r + 100) * NSTEP, NSTEP)  # async
        lab, conv = ccl(mask)
        rs = stats(lab, u32, t32)
        pulled = [np.asarray(x) for x in rs[:7]]
    Fs2.block_until_ready()
    inter_s = (time.perf_counter() - t0) / reps

    overlap_ratio = (step_s + stats_s) / inter_s
    emit(dict(question="E3 step/stats jit overlap", B=B, nf_fields=nf, N=N,
              nstep=NSTEP,
              step_ms=round(1e3 * step_s, 2),
              stats_ms=round(1e3 * stats_s, 2),
              interleaved_ms=round(1e3 * inter_s, 2),
              serial_sum_ms=round(1e3 * (step_s + stats_s), 2),
              overlap_ratio=round(overlap_ratio, 3),
              verdict=("OVERLAPS" if overlap_ratio > 1.15 else
                       "SERIALIZES (single stream)")))

    # D) D2H pull overlap while stepping: pull FULL acts (the current
    # record path's transfer) vs tiny stats rows, both after async step
    Fh = None
    t0 = time.perf_counter()
    Fs3 = Fs2
    for r in range(reps):
        Fs3 = step(Fs3, params, keys, (r + 200) * NSTEP, NSTEP)
        Fh = np.asarray(Fs3[:, :na_max])       # full acts pull (blocks)
    step_fullpull_s = (time.perf_counter() - t0) / reps
    emit(dict(question="E3d full-acts pull after async step",
              step_ms=round(1e3 * step_s, 2),
              step_plus_fullpull_ms=round(1e3 * step_fullpull_s, 2),
              pull_overhead_ms=round(1e3 * (step_fullpull_s - step_s), 2),
              acts_shape=list(np.asarray(Fs3[:, :na_max]).shape)))


if __name__ == "__main__":
    main()
