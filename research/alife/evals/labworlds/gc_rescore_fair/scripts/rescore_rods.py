"""Marangoni rods: re-score the main suite (iteration 1, quoted by the first-round cards), the iteration-2 main suite
and the formation suite (plus fband.py's 70 four-member subsets of the 8 no-action natives) with both estimators;
rebuild reports with the suites' own report code on shadow folders. usage: rescore_rods.py"""
import contextlib
import io
import itertools
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

W = C.GC / "rods"
for p in (W / "scripts2", W / "scripts"):
    sys.path.insert(0, str(p))
import gcf  # noqa: E402,F401
import gcrods as G  # noqa: E402
import programs as P1  # noqa: E402
import programs2 as P2  # noqa: E402
import fprograms as FP  # noqa: E402
import suite_report as R  # noqa: E402

OUT = C.OUT_ROOT / "rods"
SENSORS = ("device0", "device1", "global")
CAPS = dict(G.CAP_CONTROLS)


def runner(pf, caps):
    def run(d):
        R.OUT, R.PF = d, pf
        G.CAP_CONTROLS = caps
        try:
            R.main()
        finally:
            G.CAP_CONTROLS = CAPS
    return run


SUITES = {"main_iter1": (W / "suite", runner(P1, CAPS)), "main_iter2": (W / "iter2" / "suite", runner(P2, CAPS)),
          "formation": (W / "formation" / "suite", runner(FP, {"S": ["a0"]}))}


def fband(rec, dst):
    """fband.py: every 4-member subset of the no-action case's 8 independent natives, ratio to independent_native."""
    sdir = W / "formation" / "suite"
    suite = C.jload(sdir / "suite.json")
    entry = next(c for c in suite["cases"] if c["family"] == "sham")
    case, cid = entry["request"], entry["request"]["id"]
    groups = suite["groups_by_horizon"][str(entry["horizon"])]
    truth, _ = C.load_npz(sdir / entry["truth"])
    nt = truth[0].shape[1]
    rost = C.roster_for(truth)
    ind, _ = C.load_npz(sdir / "controls" / cid / "independent_native.npz")
    ign = [a[:, :nt] for a in C.load_npz(sdir / "ignore_actions.npz")[0]]
    pool = [np.concatenate([a, b]) for a, b in zip(ind, ign)]
    res = {}
    for e in C.ESTS:
        def sc(pred):
            r = C.score(case, pred, truth, groups, 4, 2, rost, e)
            g = {x["id"]: x["energy_score"] for x in r["joint_energy"]}
            return r["joint_energy_equal_group_mean"], {s: float(np.mean([v for k, v in g.items() if k.startswith(s + "/")]))
                                                        for s in SENSORS}
        ref, refs = sc(ind)
        rat, rats = [], {s: [] for s in SENSORS}
        for sub in itertools.combinations(range(8), 4):
            a, b = sc([p[list(sub)] for p in pool])
            rat.append(a / ref)
            for s in SENSORS:
                rats[s].append(b[s] / refs[s])
        null = C.jload(dst[e] / "controls" / cid / "scores.json").get("numerical_null")
        out = dict(case=cid, subsets=len(rat), band_aggregate=[round(float(np.quantile(rat, q)), 3) for q in (0.05, 0.5, 0.95)],
                   band_by_sensor={s: [round(float(np.quantile(v, q)), 3) for q in (0.05, 0.5, 0.95)] for s, v in rats.items()})
        if null:
            g = {x["id"]: x["energy_score"] for x in null["joint_energy"]}
            out["null_aggregate"] = round(null["joint_energy_equal_group_mean"] / ref, 3)
            out["null_by_sensor"] = {s: round(float(np.mean([v for k, v in g.items() if k.startswith(s + "/")])) / refs[s], 3)
                                     for s in SENSORS}
            out["null_inside_band"] = bool(out["band_aggregate"][0] <= out["null_aggregate"] <= out["band_aggregate"][2])
        res[e] = out
        C.jdump(dst[e] / "band.json", out)
    return C.diff(C.jload(sdir / "band.json"), res["plugin"])


def main():
    rec = C.Recorder("rods")
    checks, dsts = {}, {}
    for label, (sdir, run) in SUITES.items():
        suite, dst = C.pmcips_rescore("rods", label, sdir, OUT / label, rec)
        dsts[label] = dst
        for e in C.ESTS:
            with contextlib.redirect_stdout(io.StringIO()):
                run(dst[e])
        checks[label] = {"report.json": C.diff(C.jload(sdir / "report.json"), C.jload(dst["plugin"] / "report.json"))}
    checks["formation"]["band.json"] = fband(rec, dsts["formation"])
    C.jdump(OUT / "rows.json", dict(rows=rec.rows, mismatches=rec.mismatches,
                                    report_checks={k: {f: [[str(x) for x in d] for d in v[:5]] for f, v in c.items()}
                                                   for k, c in checks.items()}))
    print("rows", len(rec.rows), "score mismatches", len(rec.mismatches))
    for k, c in checks.items():
        print(k, {f: len(v) for f, v in c.items()})


if __name__ == "__main__":
    main()
