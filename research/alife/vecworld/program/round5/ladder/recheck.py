"""recheck -- plain-numpy recomputation of the headline skills and shares from results/job/n*/scores.npz
(no vw.scoring, no acceptance.py), compared with results/summary.json. CPU, a few seconds.
usage: python -B recheck.py  -> results/recheck.json
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "results", "summary.json")))
out, worst = {}, 0.0
for n in (1, 4, 8):
    z = np.load(os.path.join(HERE, "results", "job", f"n{n}", "scores.npz"), allow_pickle=True)
    for v in ("block", "object", "pop"):
        def g(a):
            return np.concatenate([z[f"t{i}|{v}|{a}"] for i in range(8)])          # (items, horizons)

        def oes(a):
            return float(((g("K").mean(0) - g(a).mean(0)) / (g("K").mean(0) - g("O").mean(0))).mean())

        def L(a):
            return float(g(a).sum(1).mean())
        c = S["cells"][f"n{n}|{v}"]
        row = {a: oes(a) for a in ("C", "P0", "P0u", "PM", "plugPM", "S@2", "D@512", "Dr@512")}
        for a, x in row.items():
            worst = max(worst, abs(x - c["oes"][a]["mean"]))
        for b in ("32", "512"):
            null = min(L("P0"), L(f"D@{b}"), L(f"Dr@{b}"))
            row[f"sigma@{b}"] = (null - L("C")) / (L("K") - L("C"))
            worst = max(worst, abs(row[f"sigma@{b}"] - c["acceptance"]["P0"][b]["sigma"]))
        row["rho@2"] = (L("P0") - L("S@2")) / (L("P0") - L("C"))
        if v != "object":                                    # rho is ill-conditioned where C - P0 is about zero
            worst = max(worst, abs(row["rho@2"] - c["acceptance"]["P0"]["2"]["rho"]))
        out[f"n{n}|{v}"] = {k: round(x, 5) for k, x in row.items()}
res = {"largest_abs_difference_from_summary_json": worst, "tolerance": 1e-4, "ok": bool(worst < 1e-4), "cells": out,
       "note": "summary.json rounds to 4 decimals; OES = mean over the 5 horizons of (K - X) / (K - O) on item means; "
               "sigma, rho from pooled L (sum over horizons, mean over items)"}
json.dump(res, open(os.path.join(HERE, "results", "recheck.json"), "w"), indent=1)
print("largest difference", worst)
assert res["ok"]
print("recheck PASSED")
