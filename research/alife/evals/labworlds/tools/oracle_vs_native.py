"""Zero-simulation diagnostic: the 2-member true-simulator forecasts against the suites' cached native ensembles.

Per bundle, equal group and case means of: A = distance of a forecast to the truths (the energy's cross term, which
does not depend on the member count), S = mean distance between distinct members (spread), and the cross distance
between the 2 oracle members and the native members. If the oracle draws come from the native world, cross ~ A_native
and A_oracle ~ A_native, while S_oracle (one pair, the same predictor seed on every case) scatters.
    python oracle_vs_native.py OUT_JSON
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim import blobround6_eval as scoring  # noqa: E402
from physim import labbundle as LB  # noqa: E402

B = Path("/home/user/evalwork/bundles")
G = Path("/home/user/evalwork/gc_suites")
KEYS = ["fedvortex", "vortex_main", "vortex_formation", "pm_main", "pm_formation", "cips_main", "cips_formation",
        "rods_main", "rods_formation"]


def native_file(key, bundle, rec):
    cid = rec["request"]["id"]
    if key == "fedvortex":
        return Path("/home/user/evalwork/vortex_eval/suite/work/controls") / f"reference_{cid}.npz"
    if key == "vortex_main":
        return G / "vortex/suite/ens" / rec["family"] / "native.npz"
    if key == "vortex_formation":
        return G / "vortex/formation/controls" / cid / "independent_native.npz"
    return Path(bundle.suite["source"]["suite_dir"]) / "controls" / cid / "independent_native.npz"


def main(out):
    res = {}
    for key in KEYS:
        root = Path("/home/user/evalwork/vortex_eval/suite/bundle") if key == "fedvortex" else B / key
        grade = B / "work/prove" / key / "oracle_grade_m2" / "grading_predictions"
        if not (B / "work/prove" / key / "oracle_m2.json").exists():
            continue
        bundle = LB.open_bundle(root, profile="evaluation")
        rows = []
        for rec in bundle.suite["cases"]:
            case = rec["request"]
            nq = len(case["queries"])
            with np.load(grade / f"{case['id']}.npz") as z:
                orc = [z[f"query{i}"] for i in range(nq)]
            with np.load(native_file(key, bundle, rec)) as z:
                nat = [z[f"query{i}"][:4] for i in range(nq)]
            truth = bundle.truth(rec)["samples"]
            vals = []
            for g in rec["groups"]:
                def sel(a):
                    return np.column_stack([a[s["query"]][:, s["time_index"], s["port"], s["slot"]]
                                            for s in g["selectors"]]) / np.asarray(g["scales"])
                o, n, t = sel(orc), sel(nat), sel(truth)
                vals.append((scoring._mean_rms_distance(o, t), scoring._mean_rms_distance(o, o) * 2,
                             scoring._mean_rms_distance(n, t), scoring._mean_rms_distance(n, n) * 4 / 3,
                             scoring._mean_rms_distance(o, n)))
            rows.append(np.mean(np.asarray(vals), axis=0))
        m = np.mean(np.asarray(rows), axis=0)
        res[key] = dict(A_oracle=m[0], S_oracle=m[1], A_native=m[2], S_native=m[3], cross_oracle_native=m[4],
                        A_ratio=m[0] / m[2], S_ratio=m[1] / m[3], cross_over_A_native=m[4] / m[2],
                        e4_oracle=m[0] - 0.375 * m[1], e4_native=m[2] - 0.375 * m[3])
        print(key, {k: round(float(v), 3) for k, v in res[key].items()})
    Path(out).write_text(json.dumps({k: {a: float(b) for a, b in v.items()} for k, v in res.items()}, indent=1) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
