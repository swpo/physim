"""Diagnostic (not the frozen score): control/native energy ratios restricted to score times <= T.

Uses the frozen groups' selectors and scales from suite.json and the cached ensembles; the energy
score is blobround6_eval._energy_score (the kernel score_case uses). usage: window_check.py OUT T
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
import numpy as np  # noqa: E402
from physim.blobround6_eval import _energy_score  # noqa: E402

out, T = Path(sys.argv[1]), float(sys.argv[2])
suite = json.loads((out / "suite.json").read_text())
times = suite["cases"][0]["request"]["queries"][0]["t"]
controls = [k for k in suite["controls"] if k != "initial_persistence"]


def load(p):
    with np.load(p) as z:
        return [z[f"query{i}"] for i in range(3)]


def sel(a, g):
    keep = [(s, sc) for s, sc in zip(g["selectors"], g["scales"]) if times[s["time_index"]] <= T]
    return np.column_stack([a[s["query"]][:, s["time_index"], s["port"], s["slot"]] for s, _ in keep]) / \
        np.array([sc for _, sc in keep])


rows = {k: {g["id"]: [] for g in suite["groups"]} for k in controls}
for c in suite["cases"]:
    cid = c["request"]["id"]
    if not (out / "controls" / cid / "scores.json").exists():
        continue
    truth = load(out / c["truth"])
    for k in controls:
        p = out / "ignore_actions.npz" if k == "ignore_actions" else out / "controls" / cid / f"{k}.npz"
        pred = load(p)
        for g in suite["groups"]:
            rows[k][g["id"]].append(_energy_score(sel(pred, g), sel(truth, g)))
gids = [g["id"] for g in suite["groups"]]
ref = rows["independent_native"]
n = len(ref[gids[0]])
print(f"{suite['world']}: score times <= {T:g} tu, {n} cases; ratio of case-mean group scores to independent_native")
print(f"{'':>22} " + " ".join(f"{g:>12}" for g in gids) + f" {'equal-group mean':>17}")
agg_ref = np.mean([np.array(ref[g]) for g in gids], axis=0)
for k in controls:
    agg = np.mean([np.array(rows[k][g]) for g in gids], axis=0)
    print(f"{k:>22} " + " ".join(f"{np.mean(rows[k][g]) / np.mean(ref[g]):12.2f}" for g in gids)
          + f" {agg.mean() / agg_ref.mean():17.2f}")
