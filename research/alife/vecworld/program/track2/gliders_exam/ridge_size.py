"""ridge_size -- does the behaviour-level control pair separate with more training data?

The pilot's ridge pair (pilot.py; 4 training members x 60 ticks per theta) did not separate on the exam.
Here, for one truth theta_k of the pilot (the largest plug-in gap among the truths where the ridge pair did
not separate, z < 2), with fresh simulations:
  train   theta_k: the pilot's 4 members + 12 new; theta_0 (box centre): the pilot's 4 + 12 new
  test    8 new theta_k members (init + burn-in + 60 ticks, programs of classes b/c/d every 10 ticks, as
          the training runs), windows at t = 16, 24, 32, 40 (history o(t-16..t), the following 16 ticks'
          wind as the open-loop program), one realised future per window
Predictors: ridge_true / ridge_prior trained on 4 or 16 members (same features and residual sampling as
the pilot). Score: fair energy score (m = 32) per (level, h) cell against the realised future, paired over
the 32 windows; level-1 differences also in OES units (divided by D_h of refs_closure.json).
Output: results/ridge_size.json.
"""
import json
import os

import numpy as np

import gworld as GW
import pilot as PL
from vw.harness import program_dense
from vw.scoring import energy_fair

T_WIN = [16, 24, 32, 40]


def items_from(Y, U):
    out = []
    for j in range(Y.shape[0]):
        for t in T_WIN:
            prog = [(int(k), {int(i): float(U[j, t + k, i]) for i in np.flatnonzero(U[j, t + k])})
                    for k in range(PL.HMAX) if t + k < U.shape[1] and np.any(U[j, t + k])]
            out.append(({"id": j * 1000 + t, "history": Y[j, t - PL.P_PRE:t + 1], "program": prog,
                         "queries": {1: PL.QUERIES[1], 2: PL.QUERIES[2]}}, Y[j, t:t + PL.HMAX + 1]))
    return out


def main():
    pj = json.load(open(os.path.join(GW.RES, "pilot.json")))
    names = pj["hidden"]
    gaps = {int(i): r["gaps"]["plugin_true-plugin_prior"]["gap"] for i, r in pj["per_truth"].items()
            if r["gaps"]["ridge_true-ridge_prior"]["z"] < 2.0}
    k = max(gaps, key=gaps.get)          # largest plug-in gap among truths where the ridge pair did not separate
    th_k = PL.theta_dict(names, pj["truths"][k])
    th_0 = PL.theta_dict(names, pj["prior_mean"])
    z = np.load(os.path.join(GW.RES, "pilot_train.npz"))
    Yp, Up = z["Y"].astype(float), z["U"].astype(float)
    sec = PL.secret().child("ridge-size")
    Y, U = PL.train_sims([th_k] * 3 + [th_0] * 3 + [th_k] * 2, sec)
    Ytr_k = np.concatenate([Yp[1 + k], Y[:3].reshape(-1, *Y.shape[2:])])
    Utr_k = np.concatenate([Up[1 + k], U[:3].reshape(-1, *U.shape[2:])])
    Ytr_0 = np.concatenate([Yp[0], Y[3:6].reshape(-1, *Y.shape[2:])])
    Utr_0 = np.concatenate([Up[0], U[3:6].reshape(-1, *U.shape[2:])])
    Yte, Ute = Y[6:].reshape(-1, *Y.shape[2:]), U[6:].reshape(-1, *U.shape[2:])
    hs = sorted(set(PL.QUERIES[1]) | set(PL.QUERIES[2]))
    preds = {}
    for n in (4, 16):
        preds[f"ridge_true_{n}"] = PL.ridge_predictor(PL.fit_ridge(Ytr_k[:n], Utr_k[:n], hs))
        preds[f"ridge_prior_{n}"] = PL.ridge_predictor(PL.fit_ridge(Ytr_0[:n], Utr_0[:n], hs))
    its = items_from(Yte, Ute)
    refs = json.load(open(os.path.join(GW.RES, "refs_closure.json")))
    cells = [(1, h) for h in PL.QUERIES[1]] + [(2, h) for h in PL.QUERIES[2]]
    S = {nm: np.zeros((len(its), len(cells))) for nm in preds}
    for nm, f in preds.items():
        for i, (it, fut) in enumerate(its):
            s = f(it, PL.M_RIDGE, 0)
            for c, (l, h) in enumerate(cells):
                j = PL.QUERIES[l].index(h)
                fn, sc = (GW.coarse, PL.SC["level1"]) if l == 1 else (GW.population, PL.SC2)
                S[nm][i, c] = float(energy_fair(s[l][:, j][None], fn(fut[h])[None, None], sc)[0])
    out = {"truth_index": k, "theta_true": th_k, "theta_prior": th_0, "n_windows": len(its), "cells": cells,
           "member_ticks": int(np.prod(Y.shape[:2]) * (GW.BURN + PL.CH_TR * PL.N_CH)),
           "mean_es": {nm: v.mean(0).tolist() for nm, v in S.items()}, "gap_prior_minus_true": {}}
    for n in (4, 16):
        d = S[f"ridge_prior_{n}"] - S[f"ridge_true_{n}"]
        den = np.array([refs[f"level{l}"][str(h)]["D"] for l, h in cells])
        out["gap_prior_minus_true"][str(n)] = {"es_gap": d.mean(0).tolist(),
                                               "es_gap_se": (d.std(0, ddof=1) / np.sqrt(len(d))).tolist(),
                                               "oes_gap": (d.mean(0) / den).tolist(),
                                               "z": (d.mean(0) / (d.std(0, ddof=1) / np.sqrt(len(d)))).tolist()}
        print(n, {f"L{l}h{h}": (round(g, 3), round(zz, 1)) for (l, h), g, zz in
                  zip(cells, out["gap_prior_minus_true"][str(n)]["oes_gap"], out["gap_prior_minus_true"][str(n)]["z"])},
              flush=True)
    d16 = S["ridge_true_4"] - S["ridge_true_16"]
    out["true_4_minus_true_16_es"] = d16.mean(0).tolist()
    json.dump(out, open(os.path.join(GW.RES, "ridge_size.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
