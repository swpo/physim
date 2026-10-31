"""Summary of rotdiv.py runs: division-axis statistics per condition. usage: rotsum.py COND=run1,run2 [COND=...]

Angles are mod 180 from the grid x axis. d_diag = distance to the nearest grid diagonal (0..45; uniform under
isotropy, P(d_diag <= 15) = 1/3). cos4 = cos(4 a): -1 on a diagonal, +1 on an axis, mean 0 (sd 1/sqrt(2n)) under
isotropy. "IC frame" uses a - theta (the directions the initial field's diagonals were rotated to).
"""
import json, sys
from math import comb
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent / "out"


def d_diag(a):
    r = np.asarray(a) % 90
    return 45 - np.minimum(r, 90 - r)


def binom_tail(k, n, p=1 / 3):
    return sum(comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


def stats(a, theta=0.0):
    a = np.asarray([x for x in a if x is not None], float)
    if a.size == 0:
        return dict(n=0)
    dd = d_diag(a)
    k = int((dd <= 15).sum())
    return dict(n=int(a.size), within15_diag=f"{k}/{a.size}", p_within15=round(binom_tail(k, a.size), 4),
                mean_d_diag=round(float(dd.mean()), 1), mean_cos4=round(float(np.cos(np.radians(4 * a)).mean()), 2),
                mean_cos4_ICframe=round(float(np.cos(np.radians(4 * (a - theta))).mean()), 2),
                null_sd_cos4=round(1 / np.sqrt(2 * a.size), 2))


rows = {}
for arg in sys.argv[1:]:
    cond, runs = arg.split("=")
    D = [json.loads((OUT / f"{r}.json").read_text()) for r in runs.split(",") if (OUT / f"{r}.json").exists()]
    if not D:
        continue
    th = D[0]["theta"]
    divs = [d for x in D for d in x["persistent_divisions"]]
    el = [ang for x in D for r in x["rings"] for _, ang in r["elongated_axes"]]
    row = dict(runs=[f"s{x['seed']}" for x in D], theta=th, iso=D[0]["iso"],
               nucleations=[len(x["births"]) for x in D],
               persistent_div_times=[[d["t"] for d in x["persistent_divisions"]] for x in D],
               splits_merges=[(x["n_splits"], x["n_merges"]) for x in D],
               bodies_t3000_4000_5000_6000=[[c[1] for c in x["counts"] if round(c[0]) in (3000, 4000, 5000, 6000)] for x in D],
               layer=[x["layer_pass"] for x in D], cpu_s=[x["cpu_s"] for x in D],
               daughter_axis_0t=stats([d.get("daughter_axis_0t") for d in divs], th),
               daughter_axis_100t=stats([d.get("daughter_axis_100t") for d in divs], th),
               parent_long_axis_10t_before=stats([d.get("parent_long_axis_10t_before") for d in divs], th),
               parent_long_axis_100t_before=stats([d.get("parent_long_axis_100t_before") for d in divs], th),
               all_split_events_axis=stats([s[1] for x in D for s in x["all_splits"]], th),
               elongated_long_axes_every250t=stats(el, th),
               angles_daughter_0t=[round(d["daughter_axis_0t"]) for d in divs if "daughter_axis_0t" in d],
               angles_parent_100t_before=[round(d["parent_long_axis_100t_before"]) for d in divs if "parent_long_axis_100t_before" in d],
               parent_aspect_10t_before=[d.get("parent_aspect_10t_before") for d in divs])
    rows[cond] = row
    print(cond, json.dumps(row))
json.dump(rows, open(OUT / "summary.json", "w"), indent=1)
