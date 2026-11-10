"""select_enriched -- a prospective test of "the weights predict the world type" (study foundry; CPU, minutes).

    python -B select_enriched.py <job1_out_dir> [--pool 16384] [--prior-seed 2027] [--n-enriched 1536]
                                 [--n-control 512] [--target movers] [--out sel_r2.json]

1. Fit, on the screened draws of job 1, an L2 logistic regression from the statistics of the weights alone
   (tnca.weight_stats: prior scalars, linear stability of the uniform state, affinity Jacobian, norms; each
   mapped to normal scores through its empirical distribution in job 1) to the target type.
2. Predict before looking: the out-of-fold yield of the target (and of the other targets) in the top
   n_enriched / pool share of job 1's draws ranked by the out-of-fold score.
3. Draw a fresh pool from the prior (another prior seed), compute its weight statistics (no simulation),
   keep the n_enriched best by the fitted score, and add n_control draws taken at random from the pool
   (the first n_control pool indices not selected: the pool is iid).
4. Write the index file for job.py (FOUNDRY_INDEX_FILE): chunks of 128 = 96 enriched + 32 control, so a
   deadline cut keeps the arms balanced.
The second GPU job then measures the yield in both arms with the same certificates.
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

import numpy as np  # noqa: E402

import analyze as AN  # noqa: E402
import criteria as CR  # noqa: E402

FEATURES = sorted({n for v in AN.FEATS.values() for n in v})


def nscore(col, ref_sorted):
    """Normal scores of `col` through the empirical distribution `ref_sorted` (mid-ranks, clipped)."""
    n = len(ref_sorted)
    r = (np.searchsorted(ref_sorted, col, side="left") + np.searchsorted(ref_sorted, col, side="right")) / 2.0
    u = np.clip((r + 0.5) / (n + 1.0), 0.5 / (n + 1.0), 1 - 0.5 / (n + 1.0))
    return np.sqrt(2) * AN._erfinv(2 * u - 1)


def design(ws, refs):
    X = np.stack([nscore(np.nan_to_num(np.asarray(ws[k], float), nan=0.0, posinf=1e30, neginf=-1e30), refs[k])
                  for k in FEATURES], 1)
    # pairwise products of the affinity terms and the instability (sign structure matters for movers)
    names = list(FEATURES)
    extra = [("lin_growth", "aff_cross_prod"), ("lin_growth", "kappa_on"), ("affx_01", "affx_10"),
             ("lin_growth", "log_dens_tot"), ("aff_self_max", "aff_cross_prod")]
    cols = [X]
    for a, b in extra:
        cols.append((X[:, names.index(a)] * X[:, names.index(b)])[:, None])
    return np.concatenate(cols + [np.ones((len(X), 1))], 1), names + [f"{a}*{b}" for a, b in extra] + ["1"]


def fit(Z, y, l2=3.0, iters=40):
    w = np.zeros(Z.shape[1])
    reg = l2 * np.eye(Z.shape[1])
    reg[-1, -1] = 0.0
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(Z @ w, -30, 30)))
        g = Z.T @ (p - y) + reg @ w
        H = (Z * (p * (1 - p))[:, None]).T @ Z + reg + 1e-9 * np.eye(Z.shape[1])
        w = w - np.linalg.solve(H, g)
    return w


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job_out")
    ap.add_argument("--pool", type=int, default=16384)
    ap.add_argument("--prior-seed", type=int, default=2027)
    ap.add_argument("--n-enriched", type=int, default=1536)
    ap.add_argument("--n-control", type=int, default=512)
    ap.add_argument("--target", default="movers")
    ap.add_argument("--out", default=os.path.join(HERE, "sel_r2.json"))
    ap.add_argument("--folds", type=int, default=5)
    a = ap.parse_args()
    D = a.job_out
    st = json.load(open(os.path.join(D, "job_state.json")))
    m, _ = AN.load_screen(D)
    idx = m["index"].astype(int)
    d = CR.derive(m, st["stages"]["screen"]["sizes"]["T"])
    t = CR.classify(d)
    g = CR.gates(d, t)
    targets = dict(structured=(t >= 3), active=(t >= 5), movers=(t == 7), closure_gate=g["closure"],
                   candidate=g["candidate"])
    ws_all = dict(np.load(os.path.join(D, "wstats.npz")))
    ids = ws_all.pop("ids", None)
    pos = {int(v): i for i, v in enumerate(ids)} if ids is not None else None
    pidx = np.array([pos[int(i)] for i in idx]) if pos else idx
    ws = {k: v[pidx] for k, v in ws_all.items()}
    refs = {k: np.sort(np.nan_to_num(np.asarray(ws[k], float), nan=0.0, posinf=1e30, neginf=-1e30)) for k in FEATURES}
    Z, names = design(ws, refs)
    y = targets[a.target].astype(float)
    n = len(y)
    share = a.n_enriched / a.pool
    # out-of-fold scores on job 1 -> the predicted yields
    rng = np.random.default_rng(0)
    perm = rng.permutation(n)
    oof = np.zeros(n)
    for f in range(a.folds):
        te = perm[f::a.folds]
        tr = np.setdiff1d(perm, te)
        oof[te] = Z[te] @ fit(Z[tr], y[tr])
    top = oof >= np.quantile(oof, 1 - share)
    pred = dict(share_selected=share, oof_auc=AN.auc(oof, y > 0.5), n_train=int(n), n_pos=int(y.sum()),
                predicted_yield={k: float(v[top].mean()) for k, v in targets.items()},
                base_rate={k: float(v.mean()) for k, v in targets.items()},
                predicted_enrichment={k: float(v[top].mean() / max(v.mean(), 1e-12)) for k, v in targets.items()})
    w = fit(Z, y)
    # the fresh pool: weight statistics only
    import jax
    import jax.numpy as jnp
    import tnca as TN
    f = jax.jit(jax.vmap(lambda th: TN.weight_stats(th)))
    step, parts, t0 = 512, [], time.time()
    for s in range(0, a.pool, step):
        ii = np.arange(s, min(a.pool, s + step))
        pad = ii if len(ii) == step else np.concatenate([ii, np.full(step - len(ii), ii[0])])
        ths = TN.draw_thetas(a.prior_seed, pad)
        r = f({k: jnp.asarray(v) for k, v in ths.items()})
        parts.append({k: np.asarray(v)[:len(ii)] for k, v in r.items()})
    wp = {k: np.concatenate([p[k] for p in parts]) for k in parts[0]}
    Zp, _ = design(wp, refs)
    sp = Zp @ w
    order = np.argsort(-sp, kind="stable")
    enr = np.sort(order[:a.n_enriched])
    chosen = set(int(i) for i in enr)
    ctl = np.array([i for i in range(a.pool) if i not in chosen][:a.n_control])
    # interleave: 96 enriched + 32 control per chunk of 128
    out_idx, e, c = [], 0, 0
    while e < len(enr) or c < len(ctl):
        out_idx += [int(i) for i in enr[e:e + 96]]
        e += 96
        out_idx += [int(i) for i in ctl[c:c + 32]]
        c += 32
    res = dict(index=out_idx, enriched=[int(i) for i in enr], control=[int(i) for i in ctl], pool=a.pool,
               prior_seed=a.prior_seed, target=a.target, model=dict(features=names, weights=[float(v) for v in w], l2=3.0),
               prediction_from_job1=pred, pool_seconds=time.time() - t0,
               pool_score_threshold=float(sp[order[a.n_enriched - 1]]),
               pool_lin_unstable_share=float((wp["lin_growth"] > 1e-4).mean()),
               enriched_kappa_on_share=float(wp["kappa_on"][enr].mean()),
               trained_on=os.path.basename(os.path.dirname(os.path.abspath(D))))
    with open(a.out, "w") as fh:
        json.dump(res, fh)
    print(json.dumps(pred, indent=1))
    print("pool", a.pool, "in", round(res["pool_seconds"], 1), "s; enriched", len(enr), "control", len(ctl),
          "index file", a.out)


if __name__ == "__main__":
    main()
