"""check_shapes -- compile-level size check of the nets at the FULL job's shapes (CPU, no simulation).

The smoke pass cannot see full-size arrays, so this traces the jitted training step, the validation pass and
the sampler of every view with data sets of the full job's shapes (zeros) and reports the largest
intermediate array of each traced program (jax.make_jaxpr, sub-programs included). The job is refused by
review if any device array passes 2^31 elements; ladder_net.Cfg.MAX_ELEMS (2^30) is the limit here. The
block view's validation pass (the largest case) is also executed once and its peak memory recorded.
usage: python -B check_shapes.py  -> results/check_shapes.json
"""
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ladder_lib as LL  # noqa: E402
import ladder_net as NN  # noqa: E402

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

# the full job's sizes (run_ladder.FULL): largest design 768 thetas x 8 mix episodes, 8 truths, P + H + 1 = 33
T1, N_ITEMS, M = 33, 48, 32
CASES = {"cond": dict(n_nets=1, E=768 * 8, cond=True), "P0u": dict(n_nets=1, E=768 * 8, cond=False),
         "D_small": dict(n_nets=NN.Cfg.MAX_LOCK, E=32, cond=False), "D_large": dict(n_nets=NN.Cfg.MAX_LOCK, E=512, cond=False)}


def largest(jaxpr, best=None):
    best = best if best is not None else [0, None]
    for eqn in jaxpr.eqns:
        for v in eqn.outvars:
            sh = tuple(getattr(v.aval, "shape", ()))
            n = int(np.prod(sh)) if sh else 1
            if n > best[0]:
                best[:] = [n, f"{eqn.primitive.name} {v.aval.dtype}{list(sh)}"]
        for val in eqn.params.values():
            for sub in (val if isinstance(val, (list, tuple)) else [val]):
                j = getattr(sub, "jaxpr", sub)
                if hasattr(j, "eqns"):
                    largest(j, best)
    return best


def fake_obs(E, rng):
    obs = np.zeros((E, T1, LL.N_OBS), np.float32)
    O = np.zeros((E, T1, LL.K, LL.NF), np.float32)
    O[..., 0] = rng.random((E, T1, LL.K)) < 0.6
    O[..., 3], O[..., 5] = O[..., 0], O[..., 0]
    obs[..., LL.NC:] = O.reshape(E, T1, -1)
    return obs, np.zeros((E, T1 - 1, LL.NW), np.float32)


out = {"limit_elems": NN.Cfg.MAX_ELEMS, "two_pow_31": 2 ** 31, "cases": {}, "jax": jax.__version__,
       "sizes": {"T1": T1, "items": N_ITEMS, "m": M, "max_lock": NN.Cfg.MAX_LOCK, "batch": NN.Cfg.BATCH,
                 "m_train": NN.Cfg.M_TRAIN, "eval_rows": NN.Cfg.EVAL_ROWS, "eval_draws": NN.Cfg.EVAL_DRAWS}}
rng = np.random.default_rng(0)
SC = {"SC1": LL.SC1, "SCF": np.ones(LL.NF), "SCO": np.ones(LL.NO), "SCP": np.ones(5), "POPM": np.zeros(5)}
worst = 0
for view in LL.VIEWS:
    for name, c in CASES.items():
        obs, U = fake_obs(c["E"], rng)
        th = np.zeros((c["E"], 8), np.float32) if c["cond"] else None
        ds = NN.make_dataset(view, obs, U, SC, theta_u=th, seed=1)
        D = NN.stack_datasets([ds] * c["n_nets"])
        Kn = c["n_nets"]
        NN.check_elems(view, c["cond"], Kn, NN.Cfg.BATCH * NN.Cfg.M_TRAIN, "training step")
        vstep, veval = NN._fns(view, c["cond"], tuple(sorted(D)))
        P = jax.vmap(lambda k: NN.init_params(view, k, c["cond"]))(jax.random.split(jax.random.key(0), Kn))
        st = {"t": jnp.zeros((Kn,), jnp.float32), "m": jax.tree_util.tree_map(jnp.zeros_like, P),
              "v": jax.tree_util.tree_map(jnp.zeros_like, P)}
        js = jax.make_jaxpr(vstep)(P, st, D, jax.random.split(jax.random.key(1), Kn), 1e-3)
        je = jax.make_jaxpr(veval)(P, D)
        ls, le = largest(js.jaxpr), largest(je.jaxpr)
        data = max(int(v.size) for v in D.values())
        row = {"n_nets": Kn, "episodes": c["E"], "train_examples": int(len(ds["tr"])), "val_rows_padded": int(D["va"].shape[1]),
               "largest_in_step": ls, "largest_in_validation": le, "largest_dataset_array": data,
               "model_step": NN.widest(view, c["cond"]) * Kn * NN.Cfg.BATCH * NN.Cfg.M_TRAIN}
        if view == "block" and name == "D_large":          # the case the review flagged: run it once
            t0 = time.time()
            v = np.asarray(veval(P, D))
            row["validation_executed"] = {"seconds": round(time.time() - t0, 1), "finite": bool(np.isfinite(v).all()),
                                          "peak_rss_gb": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 20, 2)}
        out["cases"][f"{view}|{name}"] = row
        worst = max(worst, ls[0], le[0], data)
        print(view, name, row, flush=True)
        del D, ds, obs, U
    # the sampler at the exam's shapes, both modes
    for cond, per_sample in ((True, False), (True, True), (False, False)):
        n = N_ITEMS * (M if per_sample else 1)
        m_inner = 1 if per_sample else M
        obs, U = fake_obs(N_ITEMS, rng)
        items = [{"id": i, "history": obs[i, :17], "program": []} for i in range(N_ITEMS)]
        D, Pt, _ = NN.item_arrays(view, items, max(NN.Cfg.HS), SC)
        e = jnp.asarray(np.repeat(np.arange(N_ITEMS), M)) if per_sample else jnp.arange(N_ITEMS)
        th = jnp.zeros((n, 8), jnp.float32) if cond else None
        p1 = NN.init_params(view, jax.random.key(0), cond)
        jsx = jax.make_jaxpr(NN._sampler(view, cond, m_inner))(p1, D, e, jnp.full(e.shape, Pt), jnp.full(e.shape, 0),
                                                              jax.random.key(1), th)
        lg = largest(jsx.jaxpr)
        out["cases"][f"{view}|sampler cond={cond} per_sample={per_sample}"] = {"largest": lg}
        worst = max(worst, lg[0])
        print(view, "sampler", cond, per_sample, lg, flush=True)
out["largest_elems_overall"] = worst
out["fraction_of_2_pow_31"] = worst / 2 ** 31
out["ok"] = bool(worst < NN.Cfg.MAX_ELEMS)
os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "results", "check_shapes.json"), "w"), indent=1)
print("largest", worst, "=", round(worst / 2 ** 31, 4), "x 2^31")
assert out["ok"], "an intermediate array passes the limit"
print("check_shapes PASSED")
