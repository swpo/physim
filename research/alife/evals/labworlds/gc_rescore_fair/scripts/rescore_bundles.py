"""Saved reference forecasts outside the suite folders: the LabBundle proofs' 2-member true-simulator forecasts
(oracle_grade_m2) and 64-member initial-persistence forecasts (naive_grade) of the eight bundled GC suites in use.
Each is re-scored against the bundle's truths and groups (checked identical to the suite's) with both estimators, and
the plugin result is checked against the stored grade.json. usage: rescore_bundles.py"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

B = Path("/home/user/evalwork/bundles")
OUT = C.OUT_ROOT / "bundles"
MAP = {  # bundle -> (world, suite label, suite folder)
    "vortex_main": ("vortex", "main", C.GC / "vortex" / "suite"),
    "vortex_formation": ("vortex", "formation", C.GC / "vortex" / "formation"),
    "pm_main": ("phase_membrane", "main_iter2", C.GC / "phase_membrane" / "iter2" / "suite"),
    "pm_formation": ("phase_membrane", "formation", C.GC / "phase_membrane" / "formation" / "suite"),
    "cips_main": ("cips", "main_iter2", C.GC / "cips" / "iter2" / "suite"),
    "cips_formation": ("cips", "formation", C.GC / "cips" / "formation" / "suite"),
    "rods_main": ("rods", "main_iter2", C.GC / "rods" / "iter2" / "suite"),
    "rods_formation": ("rods", "formation", C.GC / "rods" / "formation" / "suite"),
}
KEYS = ("marginal_crps", "joint_energy", "joint_energy_equal_group_mean")


def suite_groups(gs, entry):
    return gs["groups_by_horizon"][str(entry["horizon"])] if "groups_by_horizon" in gs else gs["groups"]


def same_groups(a, b):
    key = lambda gg: [(g["id"], g["selectors"], [float(x) for x in g["scales"]]) for g in gg]  # noqa: E731
    return key(a) == key(b)


def main():
    rows, mismatches, truth_checks = [], [], {}
    for bundle, (world, label, sdir) in MAP.items():
        bs = C.jload(B / bundle / "suite.json")
        gs = C.jload(sdir / "suite.json")
        gcases = {c["request"]["id"] if "request" in c else c["id"]: c for c in gs["cases"]}
        same = []
        for kind, folder in (("true_simulator_m2", "oracle_grade_m2"), ("initial_persistence_m64", "naive_grade")):
            grade = C.jload(B / "work" / "prove" / bundle / folder / "grade.json")
            stored = {r["case_id"]: r["score"] for r in grade["results"]}
            for c in bs["cases"]:
                case, cid = c["request"], c["request"]["id"]
                truth, _ = C.load_npz(B / bundle / c["truth"])
                if kind == "true_simulator_m2":
                    st, _ = C.load_npz(sdir / gcases[cid]["truth"])
                    same.append(all(np.array_equal(a, b) for a, b in zip(truth, st)))
                pred, _ = C.load_npz(B / "work" / "prove" / bundle / folder / "grading_predictions" / f"{cid}.npz")
                m = len(pred[0])
                rost = C.roster_for(truth)
                sc = {e: C.score(case, pred, truth, c["groups"], m, len(truth[0]), rost, e) for e in C.ESTS}
                d = C.diff({k: stored[cid][k] for k in KEYS}, {k: sc["plugin"][k] for k in KEYS})
                if d:
                    mismatches.append(dict(bundle=bundle, kind=kind, case=cid, n=len(d), max_rel=C.max_rel(d)))
                rows.append(dict(world=world, suite=label, bundle=bundle, case=cid, program=c["family"], control=kind,
                                 members=m, agg_plugin=sc["plugin"]["joint_energy_equal_group_mean"],
                                 agg_fair=sc["fair"]["joint_energy_equal_group_mean"],
                                 groups_plugin={x["id"]: x["energy_score"] for x in sc["plugin"]["joint_energy"]},
                                 groups_fair={x["id"]: x["energy_score"] for x in sc["fair"]["joint_energy"]},
                                 stored_checked=True, plugin_matches_stored=not d,
                                 source=str(B / "work" / "prove" / bundle / folder / "grading_predictions" / f"{cid}.npz"),
                                 spread=C.spread_terms(pred, truth, c["groups"]) if m > 1 else None,
                                 groups_same_as_suite=same_groups(c["groups"], suite_groups(gs, gcases[cid]))))
        truth_checks[bundle] = dict(truths_identical_to_suite=all(same), cases=len(same))
    C.jdump(OUT / "rows.json", dict(rows=rows, mismatches=mismatches, truth_checks=truth_checks))
    print("rows", len(rows), "mismatches", len(mismatches), truth_checks)


if __name__ == "__main__":
    main()
