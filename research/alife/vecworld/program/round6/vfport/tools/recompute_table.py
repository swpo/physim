"""recompute_table -- the reference table again, from the committed per-item scores, with numpy only.

results/proof_ring_items.npz holds, for every hidden world of the proof, the fair energy score of every policy
and of K and O per (item, cell) (tools/prove.py writes it). This script recomputes the pooled loss L, the skills
on the K-to-C and K-to-O scales and the two acceptance shares WITHOUT the store, without the vw library and
without evaluator.grader, and compares them with results/proof_ring.json. The one input taken from the proof
file is the list of valid cells (decided on K and O before any agent, vw.scoring.cells_ok).

usage: python tools/recompute_table.py [--proof results/proof_ring.json] [--out results/recomputed_table.json]
"""
import argparse
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--proof", default=os.path.join(ROOT, "results", "proof_ring.json"))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    proof = json.load(open(a.proof))
    z = np.load(os.path.join(os.path.dirname(os.path.abspath(a.proof)), proof["per_item_scores_file"]), allow_pickle=False)
    valid = np.array(proof["pooled"]["valid_cells"], bool)
    pols = [str(p) for p in z["policies"]]
    L = {k: float(z[k].reshape(-1, len(valid))[:, valid].sum(1).mean()) for k in ("K", "O")}
    for p in pols:
        L[p] = float(z[f"es_{p}"].reshape(-1, len(valid))[:, valid].sum(1).mean())
    table = {k: {"L": v, "vs_C": (L["K"] - v) / (L["K"] - L["C"]) if "C" in L else None, "vs_O": (L["K"] - v) / (L["K"] - L["O"])} for k, v in L.items()}
    acc = {}
    if all(k in L for k in ("P0", "C")):
        null = min(L["D"], L["P0"]) if "D" in L else L["P0"]
        acc["sigma"] = (null - L["C"]) / (L["K"] - L["C"])
        if "S" in L:
            acc["rho"] = (L["P0"] - L["S"]) / (L["P0"] - L["C"])
    ref, racc = proof["pooled"]["policies"], proof["pooled"].get("acceptance", {})
    diffs = [abs(table[k][f] - ref[k][f]) for k in table for f in ("L", "vs_C", "vs_O") if k in ref and ref[k].get(f) is not None and table[k][f] is not None]
    diffs += [abs(acc[k] - racc[k]) for k in acc if racc.get(k) is not None]
    out = {"source": os.path.relpath(a.proof, ROOT), "items_file": proof["per_item_scores_file"], "n_worlds": int(z["K"].shape[0]),
           "n_items": int(z["K"].shape[0] * z["K"].shape[1]), "n_cells": int(len(valid)), "n_valid_cells": int(valid.sum()),
           "failed_items": {p: int(z[f"failed_{p}"].sum()) for p in pols}, "table": table, "acceptance": acc,
           "numbers_compared": len(diffs), "max_abs_difference_to_the_proof_file": float(max(diffs)) if diffs else None}
    if a.out:
        json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps({"numbers_compared": out["numbers_compared"], "max_abs_difference": out["max_abs_difference_to_the_proof_file"],
                      "vs_C": {k: round(v["vs_C"], 4) for k, v in table.items() if v["vs_C"] is not None}, "acceptance": acc}))


if __name__ == "__main__":
    main()
