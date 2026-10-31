"""Item 4: frozen suites. usage: suite.py pm|cips freeze|run [controls...]|report"""
import sys, json
sys.path.insert(0, "/home/user/evalwork/pm_cips_eval/scripts")
from common import PC, E, LW, OUT
from pathlib import Path

world, cmd = sys.argv[1], sys.argv[2]
if world == "pm":
    spec = PC.pm_spec(0.01, 0.5, 0.25)
    progs = PC.pm_programs()
    subsets = {"band_native": ["sham", "K_d0", "L_d0", "Sm_d0", "Sp_d1", "K_d1", "two_sources"],
               "ablate_a2": ["sham", "L_d0", "L_rim", "L_d1"], "ablate_chi0": ["sham", "L_d0", "L_rim"],
               "ablate_DS2": ["sham", "Sp_d0", "Sm_d1", "Sp_d1"], "numerical_null": ["sham", "K_d0", "Sm_d0"]}
else:
    g = json.loads(Path(f"{OUT}/cips_gains.json").read_text())
    spec = PC.cips_spec(g["intensity"], gains=g["gains"])
    progs = PC.cips_programs()
    subsets = json.loads(Path(f"{OUT}/cips_subsets.json").read_text())
plan = PC.SuitePlan(spec=spec, programs=progs, subsets=subsets, members=4)
out = Path(OUT) / f"suite_{world}"
if cmd == "freeze":
    s = PC.freeze(plan, out)
    print(json.dumps({k: v["scale"] for k, v in s["calibration"]["scales"].items()}, indent=0))
elif cmd == "run":
    args = sys.argv[3:]
    ctrl = [a for a in args if not a.startswith("case:")] or None
    cases = [a[5:] for a in args if a.startswith("case:")] or None
    PC.run_suite(plan, out, controls=ctrl, cases=cases)
    PC.report(out)
elif cmd == "report":
    PC.report(out)
    print((out / "report.md").read_text())
