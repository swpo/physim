"""CIPS-iso: re-score the main suite (iteration 1, quoted by the first-round cards), the refrozen main suite (iter2,
with moat_C4), the formation suite and the formation diagnostics (null on steer_p, band on keep_empty) with both
estimators; rebuild reports with the suites' own report code on shadow folders. usage: rescore_cips.py"""
import contextlib
import io
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

W = C.GC / "cips"
for p in (W / "scripts2", W / "scripts"):
    sys.path.insert(0, str(p))
import gccips  # noqa: E402,F401
import suite_report as SR1  # noqa: E402
import iter2 as I2  # noqa: E402
import formation as FM  # noqa: E402

OUT = C.OUT_ROOT / "cips"
SENSORS = ("device0", "device1", "global")


def run_iter1(d):
    SR1.OUT = d
    SR1.main()


def run_iter2(d):
    I2.OUT = d
    I2.report()


def run_formation(d):
    FM.OUT = d
    FM.report()


SUITES = {"main_iter1": (W / "suite", run_iter1), "main_iter2": (W / "iter2" / "suite", run_iter2),
          "formation": (W / "formation" / "suite", run_formation)}


def diagnostics(rec, dst):
    """formation_diag.py's two forecasts, scored as it did (ratio to the case's independent_native, by sensor)."""
    sdir = W / "formation" / "suite"
    suite = C.jload(sdir / "suite.json")
    stored = C.jload(sdir / "diagnostics" / "scores.json")
    out = {e: {} for e in C.ESTS}
    for prog, name in (("steer_p", "numerical_null"), ("keep_empty", "band_native")):
        entry = next(c for c in suite["cases"] if c["family"] == prog)
        case, cid = entry["request"], entry["request"]["id"]
        truth, _ = C.load_npz(sdir / entry["truth"])
        rost = C.roster_for(truth)
        pred, _ = C.load_npz(sdir / "diagnostics" / f"{cid}_{name}.npz")
        sc = {e: C.score(case, pred, truth, suite["groups"], 4, 2, rost, e) for e in C.ESTS}
        rec.add("formation_diagnostics", cid, prog, name, 4, sc["plugin"], sc["fair"], None,
                sdir / "diagnostics" / f"{cid}_{name}.npz", spread=C.spread_terms(pred, truth, suite["groups"]),
                note="formation_diag.py: outside the frozen suite; no per-score file was saved, so the plugin check "
                     "is on the stored ratios")
        for e in C.ESTS:
            ref = C.jload(dst[e] / "controls" / cid / "scores.json")["independent_native"]
            g = lambda s: {x["id"]: x["energy_score"] for x in s["joint_energy"]}  # noqa: E731
            gs, gr = g(sc[e]), g(ref)
            out[e][f"{prog}:{name}"] = dict(
                case=cid, ratio=round(sc[e]["joint_energy_equal_group_mean"] / ref["joint_energy_equal_group_mean"], 3),
                by_sensor={s: round(float(np.mean([gs[k] for k in gs if k.startswith(s + "/")]) /
                                          np.mean([gr[k] for k in gr if k.startswith(s + "/")])), 3) for s in SENSORS})
    for e in C.ESTS:
        C.jdump(dst[e] / "diagnostics" / "scores.json", out[e])
    return C.diff(stored, out["plugin"])


def main():
    rec = C.Recorder("cips")
    checks, dsts = {}, {}
    for label, (sdir, runner) in SUITES.items():
        suite, dst = C.pmcips_rescore("cips", label, sdir, OUT / label, rec)
        dsts[label] = dst
        for e in C.ESTS:
            with contextlib.redirect_stdout(io.StringIO()):
                runner(dst[e])
        checks[label] = {f: C.diff(C.jload(sdir / f), C.jload(dst["plugin"] / f)) for f in ("report.json", "specificity.json")}
    checks["formation_diagnostics"] = {"diagnostics/scores.json": diagnostics(rec, dsts["formation"])}
    C.jdump(OUT / "rows.json", dict(rows=rec.rows, mismatches=rec.mismatches,
                                    report_checks={k: {f: [[str(x) for x in d] for d in v[:5]] for f, v in c.items()}
                                                   for k, c in checks.items()}))
    print("rows", len(rec.rows), "score mismatches", len(rec.mismatches))
    for k, c in checks.items():
        print(k, {f: len(v) for f, v in c.items()})


if __name__ == "__main__":
    main()
