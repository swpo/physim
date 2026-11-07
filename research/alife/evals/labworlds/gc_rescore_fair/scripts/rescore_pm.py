"""phase_membrane: re-score the main suite (iteration 1, which the first-round cards quote), the refrozen main suite
(iter2) and the formation suite with both estimators, and rebuild each suite's report and specificity with the
suite's own report code pointed at a shadow folder. usage: rescore_pm.py"""
import contextlib
import dataclasses
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

W = C.GC / "phase_membrane"
for p in (W / "iter2" / "scripts", W / "formation" / "scripts", W / "scripts"):
    sys.path.insert(0, str(p))
import fm  # noqa: E402,F401  (live physim tree)
import gsuite as GS  # noqa: E402
import suite_report as SR1  # noqa: E402
import isuite  # noqa: E402
import fsuite  # noqa: E402

OUT = C.OUT_ROOT / "phase_membrane"
SUITES = {  # label -> (suite folder, report runner)
    "main_iter1": (W / "suite", lambda d: _run_iter1(d)),
    "main_iter2": (W / "iter2" / "suite",
                   lambda d: GS.report(dataclasses.replace(isuite.PLAN, out=d),
                                       "phase_membrane main suite, iteration 2 (iteration 1 + D programs)")),
    "formation": (W / "formation" / "suite",
                  lambda d: GS.report(dataclasses.replace(fsuite.PLAN, out=d),
                                      "phase_membrane formation suite (S) from the claim's noise initial condition")),
}


def _run_iter1(d):
    SR1.OUT = d
    SR1.main()


def main():
    rec = C.Recorder("phase_membrane")
    checks = {}
    for label, (sdir, runner) in SUITES.items():
        suite, dst = C.pmcips_rescore("phase_membrane", label, sdir, OUT / label, rec)
        for e in C.ESTS:
            with contextlib.redirect_stdout(io.StringIO()):
                runner(dst[e])
        checks[label] = {f: C.diff(C.jload(sdir / f), C.jload(dst["plugin"] / f)) for f in ("report.json", "specificity.json")}
    C.jdump(OUT / "rows.json", dict(rows=rec.rows, mismatches=rec.mismatches,
                                    report_checks={k: {f: [[str(x) for x in d] for d in v[:5]] for f, v in c.items()}
                                                   for k, c in checks.items()}))
    print("rows", len(rec.rows), "score mismatches", len(rec.mismatches))
    for k, c in checks.items():
        print(k, {f: len(v) for f, v in c.items()})


if __name__ == "__main__":
    main()
