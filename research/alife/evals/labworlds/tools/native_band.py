"""The suites' own native band (no simulation): equal-case means of their 4-member independent native ensembles
(the suites' reference) and of their second independent native ensembles, from each suite's report.json."""
import json
import sys
from pathlib import Path

import numpy as np

G = Path("/home/user/evalwork/gc_suites")
SUITES = {"vortex_main": "vortex/suite", "vortex_formation": "vortex/formation", "pm_main": "phase_membrane/iter2/suite",
          "pm_formation": "phase_membrane/formation/suite", "cips_main": "cips/iter2/suite",
          "cips_formation": "cips/formation/suite", "rods_main": "rods/iter2/suite", "rods_formation": "rods/formation/suite"}
out = {}
for k, p in SUITES.items():
    r = json.loads((G / p / "report.json").read_text())
    ref, band = [], []
    for row in r["per_case"].values():
        e = row.get("reference", row.get("ref_score", row.get("ref")))
        b = row.get("native_b", row.get("band_native"))
        ref.append(e)
        if b is not None:
            band.append(b * e)
    if "band" in r and r["band"]:                        # gc_vortex: native_b over independent native
        ratio, ci = r["band"]["native_b_over_native"], r["band"]["ci90"]
    else:                                                # labeval: band_native aggregate (cases where it was run)
        ratio, ci = r["aggregate"]["band_native"]["ratio"], r["aggregate"]["band_native"]["ci90"]
    out[k] = dict(native4=float(np.mean(ref)), second_native4=float(np.mean(band)) if len(band) == len(ref) else None,
                  band_ratio=ratio, band_ci90=ci, cases=len(ref), source=str(G / p / "report.json"))
f = json.loads(Path("/home/user/evalwork/vortex_eval/suite/work/report.json").read_text())
slices = f["reward"]
out["fedvortex"] = dict(native64=f["reward"]["native64_primary"],
                        native4=10 ** (-2 * f["reward"]["independent_native_reward_4member"]),
                        aggregate_band_ratio=f.get("aggregate_band"), cases=15,
                        source="/home/user/evalwork/vortex_eval/suite/work/report.json (native64, 16 4-member slices)")
Path(sys.argv[1]).write_text(json.dumps(out, indent=1) + "\n")
for k, v in out.items():
    print(k, {a: (round(b, 4) if isinstance(b, float) else b) for a, b in v.items() if a != "source"})
