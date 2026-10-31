"""Dry run of the group format through score_case on calibration samples only (no truths)."""
import sys
from pathlib import Path

sys.path.insert(0, "/home/user/swpo/residency-environments/scripts/physim/labworlds")
import labeval as E  # noqa: E402
import numpy as np  # noqa: E402

world, out = sys.argv[1], Path(sys.argv[2])
spec = E.WORLDS[world]()
programs = E.build_programs(spec)
cal, plan = E.calibrate(spec, out, programs)
scales = E.frozen_scales(spec, cal)
groups = E.score_groups(spec, scales)
case = dict(programs[0], id="dry")
pred, tru = cal[0], [a[:2] for a in cal[0]]
r = E.scoring.score_case(case, {"samples": [a for a in pred]}, {"samples": tru}, groups=groups,
                         n_samples=len(pred[0]), n_truth=2, roster=E.roster(spec))
print("groups", len(groups), [len(g["selectors"]) for g in groups])
print("aggregate", r["joint_energy_equal_group_mean"])
for g in r["joint_energy"]:
    print(f"  {g['id']:>16} {g['energy_score']:.4f} dims {g['dimensions']}")
for k, v in scales.items():
    print(f"  {k:>22} raw {v['raw_std']:.4g} floor {v['floor']:.4g} scale {v['scale']:.4g}")
