"""make_sel -- study foundrylong: fresh draws of the screened prior for P0's training worlds (CPU, minutes).

    python -B make_sel.py --wstats DIR/wstats.npz [--prior-seed 2028] [--pool 160000] [--check 4096]

The hidden worlds of the pilot's arm P are "enriched" candidates of prior seed 2027: draws whose weight
statistics pass round 5's weights-only pre-screen (round5/foundry/select_enriched.py, model and threshold in
round5/foundry/sel_r2.json, fitted on job r5-foundry-001), which then pass the four gates of the screen and
the exam-time gate. This script applies the SAME pre-screen to a fresh pool (prior seed 2028): the stored
logistic model on the normal scores of the weight statistics (reference distribution: job r5-foundry-001's
wstats.npz), and the stored score threshold of the seed-2027 pool (its top 9.375%). No simulation.
--check N recomputes the seed-2027 selection on its first N pool indices and compares it with sel_r2.json.
Writes inputs/sel_2028.json (the selected indices, in index order). The GPU job screens them.

PILOT ONLY: every theta is a public function of (prior_seed, index); never reuse as an exam.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
FOUNDRY = os.path.abspath(os.path.join(HERE, "..", "..", "round5", "foundry"))
sys.path.insert(0, FOUNDRY)

import numpy as np  # noqa: E402

import select_enriched as SE  # noqa: E402  (design, FEATURES; imports analyze and criteria)


def scores(prior_seed, lo, hi, refs, w, step=512):
    import jax
    import jax.numpy as jnp
    import tnca as TN
    f = jax.jit(jax.vmap(lambda th: TN.weight_stats(th)))
    out = []
    for s in range(lo, hi, step):
        ii = np.arange(s, min(hi, s + step))
        pad = ii if len(ii) == step else np.concatenate([ii, np.full(step - len(ii), ii[0])])
        ths = TN.draw_thetas(prior_seed, pad)
        r = f({k: jnp.asarray(v) for k, v in ths.items()})
        wp = {k: np.asarray(v)[:len(ii)] for k, v in r.items()}
        Z, _ = SE.design(wp, refs)
        out.append(Z @ w)
    return np.concatenate(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wstats", required=True)
    ap.add_argument("--prior-seed", type=int, default=2028)
    ap.add_argument("--pool", type=int, default=160000)
    ap.add_argument("--check", type=int, default=4096)
    ap.add_argument("--out", default=os.path.join(HERE, "inputs", "sel_2028.json"))
    a = ap.parse_args()
    sel = json.load(open(os.path.join(FOUNDRY, "sel_r2.json")))
    ws = dict(np.load(a.wstats))
    ws.pop("ids", None)
    refs = {k: np.sort(np.nan_to_num(np.asarray(ws[k], float), nan=0.0, posinf=1e30, neginf=-1e30)) for k in SE.FEATURES}
    w = np.asarray(sel["model"]["weights"], float)
    thr = float(sel["pool_score_threshold"])
    t0 = time.time()
    chk = None
    if a.check:
        sc = scores(sel["prior_seed"], 0, a.check, refs, w)
        mine = set(np.flatnonzero(sc >= thr).tolist())
        theirs = {i for i in sel["enriched"] if i < a.check}
        chk = dict(n=a.check, mine=len(mine), sel_r2=len(theirs), same=mine == theirs, only_mine=sorted(mine - theirs)[:8],
                   only_sel_r2=sorted(theirs - mine)[:8])
        print("check on prior seed", sel["prior_seed"], chk, flush=True)
        if not chk["same"]:
            raise SystemExit("the pre-screen does not reproduce sel_r2.json")
    sc = scores(a.prior_seed, 0, a.pool, refs, w)
    idx = np.flatnonzero(sc >= thr)
    out = dict(PILOT_NEVER_REUSE_AS_EXAM=True,
               what="fresh draws of the prior that pass round 5's weights-only pre-screen (same model, same score threshold "
                    "as the seed-2027 enriched arm); candidates for P0's training worlds of study foundrylong",
               prior_seed=a.prior_seed, pool=a.pool, score_threshold=thr, n_selected=int(len(idx)),
               share_selected=float(len(idx) / a.pool), share_selected_seed2027=sel["prediction_from_job1"]["share_selected"],
               model="round5/foundry/sel_r2.json [model]", reference="origin/gpu-jobs:jobs/r5-foundry-001/out/wstats.npz",
               check_on_seed2027=chk, seconds=time.time() - t0, index=[int(i) for i in idx])
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w") as f:
        json.dump(out, f)
    print("pool", a.pool, "selected", len(idx), f"({len(idx) / a.pool:.4f})", "in", round(time.time() - t0), "s ->", a.out)


if __name__ == "__main__":
    main()
