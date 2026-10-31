"""Tables of the behaviour runs (python summarize.py) -> behaviour_tables.md and behaviour_tables.json."""
import glob
import json

import numpy as np

rows = []
for j in sorted(glob.glob("runs/*_s*_N*.json")):
    r = json.load(open(j))
    m = r["meta"]
    rows.append(dict(world=m["world"], seed=m["seed"], N=m["N"], dt=m["dt"], rot=m["rot"], r=r))


def f(x, d=2):
    return "-" if x is None else (f"{x:.{d}f}" if isinstance(x, float) else str(x))


out = []
for w in ("pm", "fv"):
    R = [x for x in rows if x["world"] == w]
    out.append(f"\n## {w}: behaviour (a)\n")
    if w == "pm":
        out.append("| seed | grid | dt | rot | persistent splits | max gen | splits | merges/split | bodies final | ring median (range) | rim/out | wall A4 |")
        out.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for x in R:
            r = x["r"]
            out.append(f"| {x['seed']} | {x['N']} | {x['dt']} | {x['rot']:.0f} | {r['persistent_splits']} | {r['max_generation']} | {r['splits']} | "
                       f"{r['merge_split_ratio']} | {r['components_final']} | {f(r['ring_median_over_t'])} ({f(r['ring_range'][0])}-{f(r['ring_range'][1])}) | "
                       f"{f(r['rim_over_out_median'], 1)} | {f(r['wall_A4_mean'], 3)} |")
    else:
        out.append("| seed | grid | dt | rot | persistent splits (by 600 / 1200 / 1500) | max gen | same-sign daughters | merges same/opp | merge/split | bodies final | median path speed | moving tracks |")
        out.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for x in R:
            r = x["r"]
            out.append(f"| {x['seed']} | {x['N']} | {x['dt']} | {x['rot']:.0f} | {r['persistent_splits']} ({r['ps_by_600']} / {r['ps_by_1200']} / {r['ps_by_1500']}) | "
                       f"{r['max_generation']} | {r['daughters_same_sign']}/{r['daughters_same_sign'] + r['daughters_not_same_sign']} | "
                       f"{r['merges_same_sign']}/{r['merges_opposite_sign']} | {r['merge_split_ratio']} | {r['components_final']} | "
                       f"{f(r['motion']['median_path_speed'], 3)} | {r['motion']['moving_tracks']} |")
    out.append(f"\n## {w}: direction statistics (b), A4 = <cos 4 theta> (+1 grid axes, -1 diagonals; +-se)\n")
    out.append("| seed | grid | dt | rot | division axis, persistent | division axis, all splits | motion direction | elongation axis (aspect>1.5) |" + (" wall normal |" if w == "pm" else ""))
    out.append("|---|---|---|---|---|---|---|---|" + ("---|" if w == "pm" else ""))
    for x in R:
        r = x["r"]
        cell = lambda d: f"{f(d['A4'])} +-{f(d['se'])} (n {d['n']})"
        out.append(f"| {x['seed']} | {x['N']} | {x['dt']} | {x['rot']:.0f} | {cell(r['division_axis_persistent'])} | {cell(r['division_axis_all_splits'])} | "
                   f"{cell(r['motion_direction'])} | {cell(r['elongation_axis'])} |" + (f" {f(r['wall_A4_mean'], 3)} |" if w == "pm" else ""))
    # pooled by rotation at the native grid and dt
    out.append("\nPooled at the native grid and dt (mean over seeds of A4; seed spread = min..max):\n")
    for rot in (0.0, 45.0):
        S = [x["r"] for x in R if x["N"] == 128 and x["rot"] == rot and abs(x["dt"] - (1.0 if w == "pm" else 0.02)) < 1e-12]
        if not S:
            continue
        line = [f"rot {rot:.0f} ({len(S)} seeds):"]
        for k in ("division_axis_all_splits", "motion_direction", "elongation_axis"):
            v = [s[k]["A4"] for s in S if s[k]["A4"] is not None]
            line.append(f"{k} {np.mean(v):.3f} [{min(v):.3f}..{max(v):.3f}]")
        if w == "pm":
            v = [s["wall_A4_mean"] for s in S]
            line.append(f"wall {np.mean(v):.3f} [{min(v):.3f}..{max(v):.3f}]")
        out.append("- " + "; ".join(line))
open("behaviour_tables.md", "w").write("\n".join(out) + "\n")
json.dump([dict(world=x["world"], seed=x["seed"], N=x["N"], dt=x["dt"], rot=x["rot"],
                **{k: v for k, v in x["r"].items() if k not in ("meta",)}) for x in rows],
          open("behaviour_tables.json", "w"), indent=1)
print("\n".join(out))
