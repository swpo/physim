"""acceptance_round4 -- the acceptance shares sigma and rho on the gliders pilot at full size, recomputed from
round 4's saved per-item fair energy scores (program/round4/sbi/results/job/scores.npz: 8 pilot truths x 64
items x 7 cells; GPU job r4-sbi-002) with evaluator/acceptance.py. No simulation.

For each predictor family (ridge, net, amort) and lab budget N (episodes): K = climatology, C = '<fam>|true',
P0 = '<fam>|prior_pred', D(N) = '<fam>|real@N', S(N) = '<fam>|post@N'. Two estimators:
  pooled     L = item mean of the fair energy score summed over the 7 cells (the roadmap's definition)
  oes_mean   the roadmap_envelope.py arithmetic: shares of the equal-weight mean of per-cell OES
Uncertainty: bootstrap over items and cluster bootstrap over the 8 hidden worlds.
usage: python acceptance_round4.py  -> results/acceptance_gliders_round4.json
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from evaluator import acceptance as ACC  # noqa: E402

SRC = os.path.abspath(os.path.join(HERE, "..", "..", "round4", "sbi", "results", "job", "scores.npz"))
BUDGETS = [2, 8, 32, 128, 512]


def main():
    z = np.load(SRC, allow_pickle=True)
    truths = sorted({k.split("|")[0] for k in z.files}, key=lambda s: int(s[1:]))

    def cat(name):
        return np.concatenate([z[f"{t}|{name}"] for t in truths])
    worlds = np.concatenate([[i] * len(z[f"{t}|oracle"]) for i, t in enumerate(truths)])
    K, O = cat("climatology"), cat("oracle")
    out = {"source": "program/round4/sbi/results/job/scores.npz (job r4-sbi-002, A100 40GB, float64, jax 0.12.0.1)",
           "n_items": int(len(K)), "n_worlds": len(truths), "cells": 7, "PILOT_NEVER_REUSE_AS_EXAM": True,
           "bars": {"sigma_min": 0.15, "rho_max": 0.7}, "families": {}}

    def oes_mean(S):
        return float(((K.mean(0) - S.mean(0)) / (K.mean(0) - O.mean(0))).mean())
    for fam in ("ridge", "net", "amort"):
        C, P0 = cat(f"{fam}|true"), cat(f"{fam}|prior_pred")
        rows = {}
        for N in BUDGETS:
            S = {"K": K, "C": C, "P0": P0, "S": cat(f"{fam}|post@{N}")}
            if f"{truths[0]}|{fam}|real@{N}" in z.files:
                S["D"] = cat(f"{fam}|real@{N}")
            r = ACC.shares(S, worlds=worlds, n_boot=2000, seed=N)
            oc, op, os_ = oes_mean(C), oes_mean(P0), oes_mean(S["S"])
            od = oes_mean(S["D"]) if "D" in S else None
            null = max(op, od) if od is not None else op
            rows[str(N)] = {"pooled": {k: r[k] for k in ("sigma", "null_is", "rho", "sigma_items", "rho_items",
                                                           "sigma_worlds", "rho_worlds", "pass_sigma", "pass_rho")},
                            "oes_mean": {"sigma": (oc - null) / oc, "rho": (os_ - op) / (oc - op)},
                            "L": r["L"]}
        out["families"][fam] = {"by_budget_episodes": rows,
                                "sigma_vs_P0_only_pooled": float((P0.sum(1).mean() - C.sum(1).mean()) / (K.sum(1).mean() - C.sum(1).mean()))}
    json.dump(out, open(os.path.join(HERE, "results", "acceptance_gliders_round4.json"), "w"), indent=1)
    for fam, d in out["families"].items():
        for N, r in d["by_budget_episodes"].items():
            p = r["pooled"]
            print(fam, N, "sigma %.3f (se_w %.3f, null %s) rho %.2f (se_w %.2f) | oes-mean sigma %.3f rho %.2f" % (
                p["sigma"], p["sigma_worlds"]["se"], p["null_is"], p["rho"], p["rho_worlds"]["se"],
                r["oes_mean"]["sigma"], r["oes_mean"]["rho"]))


if __name__ == "__main__":
    main()
