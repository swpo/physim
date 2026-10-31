"""Compact tables from labeval report.json files: aggregate and per-group ratios to independent_native."""
import json
import sys
from pathlib import Path

for d in sys.argv[1:]:
    r = json.loads((Path(d) / "report.json").read_text())
    print(f"== {r['world']}: {r['n_cases']} cases, {r['forecast_members']} members, {r['truth_members']} truths;"
          f" null like reference: {r['null_like_reference']}")
    for k, a in r["aggregate"].items():
        print(f"  {k:>22} agg {a['mean']:.4f} ratio {a['ratio']:6.2f} [{a['ratio_ci90'][0]:.2f}, {a['ratio_ci90'][1]:.2f}]"
              f" worse {a['cases_worse']}/{r['n_cases']} sep {a['separated']}")
    gids = list(r["groups"]["independent_native"])
    print("  " + " " * 22 + " ".join(f"{g:>12}" for g in gids))
    for k, gr in r["groups"].items():
        if k == "independent_native":
            print(f"  {'native score':>22} " + " ".join(f"{gr[g]['mean']:12.4f}" for g in gids))
        else:
            print(f"  {k:>22} " + " ".join(f"{gr[g]['ratio']:11.2f}{'*' if gr[g]['separated'] else ' '}" for g in gids))
    print(f"  simulation cpu h: {r['cpu']['simulation_cpu_s'] / 3600:.2f}")
