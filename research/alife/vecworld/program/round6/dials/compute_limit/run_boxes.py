"""run_boxes -- level-2 trajectories (N, s_b) of the fed-vortex world at a given box side (CPU, tiny).

Round 6, dials/compute_limit (study c). Uses round5/vortexexam/vxlib.Runner unchanged. All members share the
public default parameters except the overrides given here (NOT hidden values: every run of this folder is a
design check at declared parameters, PILOT_NEVER_REUSE_AS_EXAM).

  python -B run_boxes.py --H 32 --B 24 --T 380 --seed 1 --eps 0.4 --mut128 25 --out <scratch>/b32_s1.npz

Output npz: l2 (B, T, 2) = (N, s_b) after each tick; s1 (B, T, 12) level-1 summaries; meta json string.
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "round5", "vortexexam"))
import jax  # noqa: E402

jax.config.update("jax_enable_x64", True)
import numpy as np  # noqa: E402
import vxlib as VX  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--H", type=int, required=True)
    ap.add_argument("--B", type=int, required=True)
    ap.add_argument("--T", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--eps", type=float, default=0.4)
    ap.add_argument("--mut128", type=float, default=25.0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    t0 = time.time()
    c0 = time.process_time()
    r = VX.Runner(H=a.H)
    Q = VX.theta_batch(a.B, eps=a.eps, mut128=a.mut128)
    keys = jax.random.split(jax.random.key(a.seed * 1000 + a.H), a.B)
    X, M, Y = r.rollout(Q, keys, a.T, chunk=20, log=lambda s: print(s, round(time.time() - t0), "s", flush=True)
                        if "0/" in s else None)
    l2 = VX.level2(Y, r.K)
    s1 = VX.summaries(Y, r.K)
    meta = dict(H=a.H, B=a.B, T=a.T, seed=a.seed, eps=a.eps, mut128=a.mut128, K=r.K, wall_s=round(time.time() - t0, 1),
                cpu_s=round(time.process_time() - c0, 1),
                overflow_ticks_raw_kept=np.asarray(r.overflow(M))[:, :2].sum(0).astype(int).tolist(),
                peak_raw_kept=np.asarray(r.overflow(M))[:, 2:].max(0).astype(int).tolist(),
                marker="PILOT_NEVER_REUSE_AS_EXAM; parameters are declared, not hidden")
    np.savez_compressed(a.out, l2=l2.astype(np.float32), s1=s1, meta=json.dumps(meta))
    print(json.dumps(meta), flush=True)
    sb = l2[..., 1]
    n = l2[..., 0]
    for t in range(59, a.T, 40):
        print("tick", t + 1, "N mean", round(float(n[:, t].mean()), 2), "s_b mean", round(float(sb[:, t].mean()), 3),
              "sd", round(float(sb[:, t].std()), 3), flush=True)


if __name__ == "__main__":
    main()
