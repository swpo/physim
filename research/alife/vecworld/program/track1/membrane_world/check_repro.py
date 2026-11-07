"""check_repro -- does membrane_jax.native_step reproduce the numpy source step (noise off)?

    python check_repro.py [dt] [T_end] [seed]     (defaults 0.5, 5000 time units, seed 1; 128^2)

Source: threads/autopoiesis/worlds/phase_membrane/world.py with P['dt'] = dt (its defaults otherwise). The JAX
run starts from numpy's initial state (init(seed, (128, 128))); the channel is off (f = 0).

Reports
  per_step  one JAX step applied to numpy's state s_n against numpy's s_{n+1}, at every checkpoint (every
            CK = 100 / dt steps, i.e. every 100 time units): max |diff| / max |field| per field.
  run       the two runs side by side: max |diff| / max |field| of every field at every checkpoint, and the
            number of phi > 0.5 cells (8-connected, periodic labelling by scipy on a 3x3 tiling) in each.
  null      the numpy run restarted from phi (1 + 1e-15 r), r = +-1 per pixel: how fast a round-off-level
            difference grows in this law, the yardstick for `run`.
  timing    numpy and JAX CPU seconds per native step on one core.
Writes results/repro_dt{dt}.json.
"""
import json
import os
import sys
import time

import _paths
import numpy as np
from scipy import ndimage

DT = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
T_END = float(sys.argv[2]) if len(sys.argv) > 2 else 5000.0
SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 1
H = 128
SW = _paths.load_source()
SW.P["dt"] = DT

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import membrane_jax as MJ  # noqa: E402

FIELDS = MJ.FIELDS
CK = int(round(100 / DT))
N = int(round(T_END / DT))


def cells(phi):
    """Number of 8-connected phi > 0.5 components on the torus."""
    m = phi > 0.5
    lab, n = ndimage.label(np.tile(m, (3, 3)), structure=np.ones((3, 3)))
    c = lab[H:2 * H, H:2 * H]
    return int(len(np.unique(c[c > 0])))


def np_run(s, n):
    cks = {}
    t0 = time.process_time()
    for i in range(n):
        if i % CK == 0:
            cks[i] = {f: s[f].copy() for f in FIELDS}
        s = SW.step(s)
    cks[n] = {f: s[f].copy() for f in FIELDS}
    return cks, (time.process_time() - t0) / n


def rel(a, b):
    return {f: float(np.abs(a[f] - b[f]).max() / max(np.abs(b[f]).max(), 1e-300)) for f in FIELDS}


def main():
    cfg = MJ.Config(dt=DT)
    q = {k: jnp.asarray(v, jnp.float64) for k, v in MJ.THETA.items()}
    ns = MJ.make_native_step(cfg)
    Z = jnp.zeros((H, H))
    one = jax.jit(lambda x: ns(q, x, Z))
    chunk = jax.jit(lambda x: jax.lax.fori_loop(0, CK, lambda i, xx: ns(q, xx, Z), x))

    s0 = SW.init(SEED, (H, H))
    x0 = {f: s0[f].copy() for f in FIELDS}
    cks, np_sec = np_run({f: s0[f].copy() for f in FIELDS}, N)

    # per step: JAX step on numpy's state vs numpy's next state (numpy step from the same checkpoint)
    per_step = {}
    for i, st in cks.items():
        if i == N:
            continue
        nxt = SW.step({f: st[f].copy() for f in FIELDS})
        y = {f: np.asarray(v) for f, v in one({f: jnp.asarray(st[f]) for f in FIELDS}).items()}
        per_step[i] = rel(y, nxt)
    ps_max = {f: max(v[f] for v in per_step.values()) for f in FIELDS}

    # run side by side
    x = {f: jnp.asarray(x0[f]) for f in FIELDS}
    jax.block_until_ready(chunk(x))
    run, cells_np, cells_jax = {}, {}, {}
    t0 = time.process_time()
    jsec = 0.0
    for i in range(0, N + 1, CK):
        xn = {f: np.asarray(v) for f, v in x.items()}
        run[i] = rel(xn, cks[i])
        cells_np[i], cells_jax[i] = cells(cks[i]["phi"]), cells(xn["phi"])
        if i < N:
            tj = time.process_time()
            x = chunk(x)
            jax.block_until_ready(x)
            jsec += time.process_time() - tj
    jax_sec = jsec / N

    # null: numpy vs numpy from a round-off-level perturbation of phi
    r = np.random.default_rng(0).choice([-1.0, 1.0], size=(H, H))
    s1 = {f: x0[f].copy() for f in FIELDS}
    s1["phi"] = s1["phi"] * (1 + 1e-15 * r)
    ck2, _ = np_run(s1, N)
    null = {i: rel(ck2[i], cks[i]) for i in cks}
    cells_null = {i: cells(ck2[i]["phi"]) for i in cks}

    def by_t(d):
        return {str(int(round(i * DT))): max(v.values()) for i, v in sorted(d.items())}

    out = {"dt": DT, "T_end": T_END, "seed": SEED, "H": H, "checkpoint_every_t": CK * DT,
           "per_step_max_rel_diff": ps_max,
           "run_max_rel_by_t": by_t(run), "null_max_rel_by_t": by_t(null),
           "run_max_rel_end": max(run[N].values()), "null_max_rel_end": max(null[N].values()),
           "cells_numpy_by_t": {str(int(round(i * DT))): c for i, c in sorted(cells_np.items())},
           "cells_jax_by_t": {str(int(round(i * DT))): c for i, c in sorted(cells_jax.items())},
           "cells_null_by_t": {str(int(round(i * DT))): c for i, c in sorted(cells_null.items())},
           "cells_jax_eq_numpy_all": all(cells_np[i] == cells_jax[i] for i in cells_np),
           "cpu_s_per_native_step_128": {"numpy_source": np_sec, "jax": jax_sec}}
    json.dump(out, open(os.path.join(_paths.RESULTS, f"repro_dt{DT:g}.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if not k.endswith("_by_t")}, indent=1))
    print("run", {k: f"{v:.1e}" for k, v in out["run_max_rel_by_t"].items()})
    print("null", {k: f"{v:.1e}" for k, v in out["null_max_rel_by_t"].items()})


if __name__ == "__main__":
    main()
