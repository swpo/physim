"""recheck_cpu -- the screen's certificates of a few draws on this platform (CPU), with the GPU job's keys.

    python -B recheck_cpu.py --draws 12,345 [--prior-seed 2026] [--run-seed 5150] [--out results/recheck_cpu.json]

Same code, sizes, thetas and noise keys as the screen stage of job.py. Float64 runs on a GPU and on a CPU
differ in rounding and the worlds amplify it, so trajectories differ; what should agree is the world type and
the descriptors within their sampling error. Writes the CPU descriptors (analyze.py's world_row) per draw.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import analyze as AN  # noqa: E402
import criteria as CR  # noqa: E402
import screen as SC  # noqa: E402
import tnca as TN  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draws", required=True)
    ap.add_argument("--prior-seed", type=int, default=2026)
    ap.add_argument("--run-seed", type=int, default=5150)
    ap.add_argument("--eps", type=float, default=0.1)
    ap.add_argument("--out", default=os.path.join(HERE, "results", "recheck_cpu.json"))
    a = ap.parse_args()
    idx = np.array([int(v) for v in a.draws.split(",")])
    sz = SC.Sizes(M=6, M_fit=4, M_trk=2, burn=50, T=240, n_snap=4, R=4, R2=2, HB=32)
    ths = TN.draw_thetas(a.prior_seed, idx)
    ths2 = [TN.perturb_theta({k: v[i] for k, v in ths.items()}, a.prior_seed, int(j), a.eps) for i, j in enumerate(idx)]
    ths2 = {k: np.stack([o[k] for o in ths2]) for k in ths2[0]}
    base = jax.random.key(a.run_seed)
    keys = jax.vmap(lambda i: jax.random.fold_in(base, i))(jnp.asarray(idx, jnp.uint32))
    fn = SC.make_chunk_fn(SC.tnca_world(), sz, map_batch=4)
    t = time.time()
    res = SC.to_host(fn({k: jnp.asarray(v) for k, v in ths.items()}, {k: jnp.asarray(v) for k, v in ths2.items()}, keys))
    dt = time.time() - t
    d = CR.derive(res, sz.T)
    ty = CR.classify(d)
    g = CR.gates(d, ty)
    s = CR.score(d, ty)
    out = dict(platform=dict(backend=jax.default_backend(), jax=jax.__version__, numpy=np.__version__, dtype="float64"),
               sizes=vars(sz), seconds=dt, prior_seed=a.prior_seed, run_seed=a.run_seed,
               worlds=[dict(draw=int(i), **AN.world_row(d, j, ty, g, s)) for j, i in enumerate(idx)])
    with open(a.out, "w") as f:
        json.dump(out, f, indent=1, default=float)
    for w in out["worlds"]:
        print(w["draw"], w["type"], "score %.3f" % w["score"], "ceil8 %.3f" % w["ceil"][3], "nb %.1f" % w["nb_mean"],
              "v_net %.3f" % w["v_net"], "events %.1f" % w["events100"])


if __name__ == "__main__":
    main()
