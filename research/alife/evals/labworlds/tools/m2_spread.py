"""How noisy is a 2-member true-simulator score? Zero-simulation check from the suites' cached 4-member native ensembles.

For each of the 6 member pairs (i, j) of the suite's independent-native ensembles (seeds 81000 + case), the pair is
used as a 2-member forecast on every case, and the suite energy debiased to 4 members (A - 0.375 S, as
prove_bundle.py debias) is computed against the bundle's truths and groups. The spread of these 6 values over the
4-member reference shows the sampling noise of a 2-member estimate.
    python m2_spread.py BUNDLE_KEY OUT_JSON
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim import blobround6_eval as scoring  # noqa: E402
from physim import labbundle as LB  # noqa: E402

B = Path("/home/user/evalwork/bundles")
G = Path("/home/user/evalwork/gc_suites")
NATIVE = {  # bundle key -> function(case record) -> path of the suite's 4-member independent native
    "vortex_main": lambda rec, src: G / "vortex/suite/ens" / rec["family"] / "native.npz",
    "vortex_formation": lambda rec, src: G / "vortex/formation/controls" / rec["request"]["id"] / "independent_native.npz",
}


def native_path(key, rec, src):
    if key in NATIVE:
        return NATIVE[key](rec, src)
    return Path(src) / "controls" / rec["request"]["id"] / "independent_native.npz"


def main(key, out):
    bundle = LB.open_bundle(B / key, profile="evaluation")
    src = bundle.suite["source"]["suite_dir"]
    per_pair = {p: [] for p in itertools.combinations(range(4), 2)}
    ref4 = []
    for rec in bundle.suite["cases"]:
        case = rec["request"]
        path = native_path(key, rec, src)
        with np.load(path, allow_pickle=False) as z:
            nat = [z[f"query{i}"][:4] for i in range(len(case["queries"]))]
        truth = bundle.truth(rec)["samples"]
        sel = []
        for g in rec["groups"]:
            def select(arrays):
                return np.column_stack([arrays[s["query"]][:, s["time_index"], s["port"], s["slot"]]
                                        for s in g["selectors"]]) / np.asarray(g["scales"])
            sel.append((select(nat), select(truth)))
        ref4.append(np.mean([scoring._energy_score(x, y) for x, y in sel]))
        for (i, j) in per_pair:
            vals = []
            for x, y in sel:
                xx = x[[i, j]]
                A = scoring._mean_rms_distance(xx, y)
                S = scoring._mean_rms_distance(xx, xx) * 2
                vals.append(A - 0.375 * S)
            per_pair[(i, j)].append(np.mean(vals))
    ref = float(np.mean(ref4))
    pairs = {f"{i}{j}": float(np.mean(v)) for (i, j), v in per_pair.items()}
    res = dict(bundle=key, native4=ref, pair_e4=pairs, pair_ratio_min=min(pairs.values()) / ref,
               pair_ratio_max=max(pairs.values()) / ref)
    Path(out).write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
