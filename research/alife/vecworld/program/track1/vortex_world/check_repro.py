"""check_repro -- does vortex_jax.native_step reproduce the numpy source step (noise off)?

    python check_repro.py [T_end]       (default T_end = 500 time units = 25000 native steps, 128^2, seed 1)

Source: the c53 selection world.py with WORLD_P {"eps": 0.2, "mut_dt": 50} (labels at t = 300,
mutations at t = 350, 400, 450), labkit FFTs on one worker. The JAX run starts from the numpy initial
state and is fed numpy's mutation uniforms (default_rng(mut_seed) draws, one per mutation step).

Reports
  per_step   one JAX step applied to numpy's state s_n, against numpy's s_{n+1}, at every checkpoint
             (every 250 steps) and at the labelling and mutation steps: max |diff| / max |field|.
  run        the two runs side by side: max |diff| / max |field| of every field at every checkpoint.
  null       the same numpy run started from om * (1 + 1e-15 * r), r = +-1 per pixel: the chaotic
             divergence of a round-off-level perturbation, the yardstick for `run`.
  timing     numpy and JAX seconds per native step on one core.
Writes results/repro.json.
"""
import importlib.util
import json
import os
import sys
import time

import _paths
import numpy as np

os.environ["WORLD_P"] = json.dumps({"eps": 0.2, "mut_dt": 50})
sys.path.insert(0, _paths.LAB)
from labkit import ops  # noqa: E402

ops.WORKERS = 1
spec = importlib.util.spec_from_file_location("srcworld", _paths.SRC_SEL)
SW = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SW)

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import vortex_jax as VJ  # noqa: E402

T_END = float(sys.argv[1]) if len(sys.argv) > 1 else 500.0
SEED, H = 1, 128
CK = 250
FIELDS = VJ.FIELDS


class LoggedRng:
    """default_rng proxy that logs the native step index of every draw."""

    def __init__(self, rng):
        self.rng, self.log, self.step = rng, [], 0

    def random(self):
        u = self.rng.random()
        self.log.append((self.step, u))
        return u


def np_run(s, n, rec_pairs=()):
    """Advance the numpy state n steps; returns checkpoints {step: fields} and pairs {step: (s_n, s_{n+1})}."""
    cks, pairs = {}, {}
    s["mrng"] = LoggedRng(s["mrng"])
    t0 = time.process_time()
    for i in range(n):
        s["mrng"].step = i
        if i % CK == 0:
            cks[i] = {f: s[f].copy() for f in FIELDS} | {"t": s["t"]}
        if i % CK == 0 or i in rec_pairs:
            before = {f: s[f].copy() for f in FIELDS} | {"t": s["t"]}
        s = SW.step(s)
        if i % CK == 0 or i in rec_pairs:
            pairs[i] = (before, {f: s[f].copy() for f in FIELDS} | {"t": s["t"]})
    cks[n] = {f: s[f].copy() for f in FIELDS} | {"t": s["t"]}
    return cks, pairs, s["mrng"].log, (time.process_time() - t0) / n


def rel(a, b):
    return {f: float(np.abs(a[f] - b[f]).max() / max(np.abs(b[f]).max(), 1e-300)) for f in FIELDS}


def main():
    n = int(round(T_END / 0.02))
    cfg = VJ.Config(H=H, W=H)
    ns = VJ.make_native_step(cfg)
    q = {k: jnp.asarray(v, jnp.float64) for k, v in VJ.THETA.items()}
    Z = jnp.zeros((H, H))
    step1 = jax.jit(lambda x, u: ns(q, x, u, Z))

    # the special steps: labelling (t = 300) and mutations (t = 350, 400, ...)
    special = [int(round(cfg.lab_t / 0.02))] + [int(round(t / 0.02)) for t in np.arange(cfg.lab_t + 50, T_END, 50)]
    s0 = SW.init(SEED, (H, H))
    x0 = {f: jnp.asarray(s0[f]) for f in FIELDS} | {"t": jnp.asarray(0.0)}
    cks, pairs, log, np_sec = np_run(s0, n, rec_pairs=set(special))
    U = np.full(n, 0.5)
    for i, u in log:
        U[i] = u

    # per-step agreement
    per = []
    for i, (a, b) in sorted(pairs.items()):
        xa = {f: jnp.asarray(a[f]) for f in FIELDS} | {"t": jnp.asarray(a["t"])}
        y = step1(xa, U[i])
        y = {f: np.asarray(y[f]) for f in FIELDS} | {"t": float(y["t"])}
        r = rel(y, b)
        per.append({"step": i, "t": a["t"], "special": i in special, "t_equal": y["t"] == b["t"], **r})

    # full run with numpy's mutation draws
    @jax.jit
    def chunk(x, Uc):
        return jax.lax.fori_loop(0, CK, lambda j, xx: ns(q, xx, Uc[j], Z), x)
    x = x0
    run = []
    jx_sec = 0.0
    x = chunk(x, jnp.asarray(U[:CK]))                     # compile
    x = x0
    for c in range(n // CK):
        if c * CK in cks:
            xn = {f: np.asarray(x[f]) for f in FIELDS}
            run.append({"step": c * CK, "t": cks[c * CK]["t"], **rel(xn, cks[c * CK])})
        t0 = time.process_time()
        x = chunk(x, jnp.asarray(U[c * CK:(c + 1) * CK]))
        x["om"].block_until_ready()
        jx_sec += time.process_time() - t0
    xn = {f: np.asarray(x[f]) for f in FIELDS}
    run.append({"step": n, "t": cks[n]["t"], **rel(xn, cks[n])})
    jx_sec /= n

    # chaos null: numpy from a round-off perturbation
    s1 = SW.init(SEED, (H, H))
    r = np.where(np.random.default_rng(99).random((H, H)) < 0.5, -1.0, 1.0)
    s1["om"] = s1["om"] * (1 + 1e-15 * r)
    cks1, _, _, _ = np_run(s1, n)
    null = [{"step": i, "t": cks[i]["t"], **rel(cks1[i], cks[i])} for i in sorted(cks)]

    def first_above(rows, thr):
        for r_ in rows:
            if max(r_[f] for f in FIELDS) > thr:
                return r_["t"]
        return None

    out = {"config": {"H": H, "seed": SEED, "T_end": T_END, "native_steps": n, "checkpoint_every": CK,
                      "WORLD_P": os.environ["WORLD_P"], "mutation_draws": [(i, u) for i, u in log]},
           "per_step_max_rel": {f: max(p[f] for p in per) for f in FIELDS},
           "per_step_special": [p for p in per if p["special"]],
           "per_step_t_equal_all": all(p["t_equal"] for p in per),
           "run_max_rel_by_t": {str(round(r_["t"])): max(r_[f] for f in FIELDS) for r_ in run[::4]},
           "null_max_rel_by_t": {str(round(r_["t"])): max(r_[f] for f in FIELDS) for r_ in null[::4]},
           "run_first_t_above": {str(th): first_above(run, th) for th in (1e-12, 1e-9, 1e-6, 1e-3, 1e-1)},
           "null_first_t_above": {str(th): first_above(null, th) for th in (1e-12, 1e-9, 1e-6, 1e-3, 1e-1)},
           "run_final": run[-1], "null_final": null[-1],
           "per_step": per, "run": run, "null": null,
           "timing_cpu_s_per_native_step": {"numpy_labkit_1worker": np_sec, "jax": jx_sec},
           "jax_devices": str(jax.devices()), "jax_version": jax.__version__}
    json.dump(out, open(os.path.join(_paths.RESULTS, "repro.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("per_step_max_rel", "per_step_t_equal_all", "run_first_t_above",
                                           "null_first_t_above", "timing_cpu_s_per_native_step")}, indent=1))
    print("special", [(p["step"], max(p[f] for f in FIELDS)) for p in out["per_step_special"]])
    print("run", out["run_max_rel_by_t"])
    print("null", out["null_max_rel_by_t"])


if __name__ == "__main__":
    main()
