"""(d) Numerics penalty at the native resolution: new ensembles for the dt-halved null band.

python dnull.py run   --world phase_membrane|fed_vortices --cases c001 ...
python dnull.py check --world ...     (one truth member re-simulated: bit-identical to the suite's)

Writes under curation/dnull/<world>/:
  null_indep/<case>.npz   dt-halved predictor, 8 members, its own seeds 61000 + i (the suite's
                          numerical_null shares the forecast seeds 81000 + i of independent_native)
  native_b/<case>.npz     fed vortices only: a second native ensemble, seeds 91000 + i (labeval's
                          band seeds; phase_membrane's band ensembles already exist in the suite)
The suite's frozen truths, groups and ensembles are read, never written.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "pkg"))            # committed HEAD copy of environments/physim/physim
import physim  # noqa: E402,F401  (pins the package before labeval inserts the live tree)
from physim import labworld as LW  # noqa: E402

sys.path.insert(0, "/home/user/swpo/residency-environments/scripts/physim/labworlds")
import labeval as E  # noqa: E402

import numpy as np  # noqa: E402

SUITE = HERE.parent / "suite"
SHORT = {"phase_membrane": "pm", "fed_vortices": "fv"}
NULL_SEED = 61000


def spec_and_suite(world):
    spec = E.WORLDS[world]()
    assert Path(LW.__file__).resolve().is_relative_to(HERE / "pkg"), LW.__file__
    suite = json.loads((SUITE / SHORT[world] / "suite.json").read_text())
    assert E._jsonable(spec.world.declaration()) == suite["declaration"], "declaration differs from the frozen suite"
    assert E.file_sha(spec.world.path) == suite["world_sha256"], "world file changed since the suite"
    return spec, suite


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "check"])
    ap.add_argument("--world", required=True)
    ap.add_argument("--cases", nargs="*", default=None)
    a = ap.parse_args()
    spec, suite = spec_and_suite(a.world)
    out = HERE / "dnull" / a.world
    cases = [(i, e) for i, e in enumerate(suite["cases"]) if not a.cases or e["request"]["id"] in a.cases]
    if a.cmd == "check":
        i, e = cases[0]
        case = e["request"]
        native = E.make_oracle(spec, "native")
        t0 = time.process_time()
        one = native.sample_truth(case["actions"], case["queries"], 1, truth_seed=E.TRUTH_SEED + i)["samples"]
        with np.load(SUITE / SHORT[a.world] / e["truth"]) as z:
            ref = [z[f"query{q}"] for q in range(len(case["queries"]))]
        same = all(np.array_equal(one[q][0], ref[q][0]) for q in range(len(ref)))
        print(json.dumps(dict(world=a.world, case=case["id"], truth_member0_bit_identical=bool(same),
                              cpu_s=round(time.process_time() - t0, 1))), flush=True)
        return
    oracles = {}
    for i, e in cases:
        case = e["request"]
        jobs = [("null_indep", "numerical_null", NULL_SEED + i)]
        if a.world == "fed_vortices":
            jobs.insert(0, ("native_b", "native", E.BAND_SEED + i))
        for sub, variant, seed in jobs:
            (out / sub).mkdir(parents=True, exist_ok=True)
            if variant not in oracles:
                oracles[variant] = E.make_oracle(spec, variant)
            o = oracles[variant]
            E.cached(out / sub / f"{case['id']}.npz", lambda: o.sample_truth(
                case["actions"], case["queries"], 8, truth_seed=seed),
                meta=dict(request=case, members=8, seed=seed, variant=variant))


if __name__ == "__main__":
    main()
