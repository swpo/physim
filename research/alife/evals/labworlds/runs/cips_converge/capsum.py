"""Compact comparison of capab.py runs. usage: capsum.py NAME [NAME ...]"""
import json, sys
from pathlib import Path
import numpy as np
OUT = Path(__file__).resolve().parent / "out" / "cap"
rows = []
for n in sys.argv[1:]:
    d = json.loads((OUT / f"{n}.json").read_text())
    cnt = {round(c[0]): c[1] for c in d["counts"]}
    axes = [a for r in d["rings"] for a in r["elongated_axes"]]
    diag = [min(abs(ang - 45), abs(ang - 135)) <= 15 for _, ang in axes]
    rc = [r["rim_core_median"] for r in d["rings"] if r["rim_core_median"]]
    ro = [r["rim_out_median"] for r in d["rings"] if r["rim_out_median"]]
    last = d["cut"]["log"][-1]
    rows.append(dict(run=n, dt=d["dt"], N=d["N"], bodies_t1000_2000_3000_4000_5000=[cnt.get(t) for t in (1000, 2000, 3000, 4000, 5000)],
                     nucleations=len(d["births"]), first_nucleation=min(d["births"]) if d["births"] else None,
                     splits=d["splits"], persistent_splits=[p["t"] for p in d["persistent_splits"]], merges=d["merges"], deaths=d["deaths"],
                     layer_pass=d["layer_pass"], rim_core_median_range=[round(min(rc), 2), round(max(rc), 2)] if rc else None,
                     rim_out_median_range=[round(min(ro), 1), round(max(ro), 1)] if ro else None,
                     elongated_samples=len(axes), frac_axis_within15_of_diagonal=round(float(np.mean(diag)), 2) if diag else None,
                     cut=dict(t_cut=d["cut"]["t_cut"], radius=round(d["cut"]["radius_wu"], 1), target_died_at=d["cut"]["died_at"],
                              target_area_cut_end=last["target_area_cut"], target_area_fed_end=last["target_area_fed"],
                              outside_cut_end=last["bodies_outside_cut"], outside_fed_end=last["bodies_outside_fed"]),
                     cpu_s=round(d["cpu_main_s"] + d["cpu_cut_s"])))
for r in rows:
    print(json.dumps(r))
