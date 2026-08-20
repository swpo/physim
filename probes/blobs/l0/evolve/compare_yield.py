"""compare_yield.py — the research question, quantified.

"Does merge-and-mutate find things jitter-sampling does not?"

Currency: shared MAP-Elites descriptor cells (8-tuple, ../archive.json
convention) discovered per 100 ASSAY RUNS, chronological first-touch credit.
Both results files replayed merged by timestamp; a cell is credited to the
strategy of the FIRST row that lands in it. Assay-run accounting (same
convention both sides, documented undercount for a3):
  a1: 1 if best-variant bare else 2 (per act); a2: n(d0s); a3: +2 if ran;
  a4 (evolver only): +1. Funnel-only rows cost ~0 assays but are counted as
  candidates (funnel pass-rates reported separately).

Outputs: data/compare_yield.json + printed table.
  per strategy: n_children/candidates, funnel pass rate, n_assays total,
  cells_first_touched (list), cells/100 assays, ALIVE cells/100 assays,
  cross-signature classes found (evolver only), lineage-op breakdown.
"""
import os, sys, json
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
L0DIR = os.path.dirname(BASE)

sam = json.load(open(os.path.join(L0DIR, "results.json")))
evo = json.load(open(os.path.join(BASE, "results.json")))

rows = []
for r in sam:
    if r.get("kind") == "candidate":
        strat = "sampler_" + r.get("strategy", "?")
        rows.append((r.get("ts", ""), strat, r))
for r in evo:
    if r.get("kind") == "evo_child":
        op = r.get("lineage", {}).get("op", "?")
        strat = "evolver_mutate" if op == "mutate" else \
                ("evolver_merge" if op.startswith("merge") else "evolver_?")
        rows.append((r.get("ts", ""), strat, r))
rows.sort(key=lambda x: x[0])


def n_assays(r):
    if "n_assays" in r:
        n = r["n_assays"]
        return n
    n = 0
    a1 = r.get("a1") or {}
    for k, v in a1.items():
        n += 1 if v.get("variant") == "bare" else 2
    n += len(r.get("a2") or [])
    a3 = r.get("a3")
    if a3 and "classes" in a3:
        n += 2
    return n


seen = set()
stats = defaultdict(lambda: dict(n=0, funnel_pass=0, assays=0, cells=[],
                                 alive_cells=[], ops=Counter(), cross=Counter(),
                                 stages=Counter()))
for ts, strat, r in rows:
    s = stats[strat]
    s["n"] += 1
    s["stages"][r.get("stage", "?")] += 1
    if r.get("stage") in ("pass", "assayed"):
        s["funnel_pass"] += 1
    s["assays"] += n_assays(r)
    if strat.startswith("evolver"):
        s["ops"][r.get("lineage", {}).get("op", "?")] += 1
        if r.get("cross_sig") and r["cross_sig"] != "na":
            s["cross"][r["cross_sig"]] += 1
    cell = r.get("cell")
    if cell and cell not in seen:
        seen.add(cell)
        s["cells"].append(cell)
        if "persist" in cell or "travel" in cell:
            s["alive_cells"].append(cell)

out = {}
print(f"{'strategy':<18}{'n':>5}{'funnel%':>9}{'assays':>8}"
      f"{'cells':>7}{'/100a':>8}{'alive':>7}{'/100a':>8}")
for strat in sorted(stats):
    s = stats[strat]
    c100 = 100.0 * len(s["cells"]) / max(s["assays"], 1)
    a100 = 100.0 * len(s["alive_cells"]) / max(s["assays"], 1)
    print(f"{strat:<18}{s['n']:>5}{100*s['funnel_pass']/max(s['n'],1):>8.0f}%"
          f"{s['assays']:>8}{len(s['cells']):>7}{c100:>8.2f}"
          f"{len(s['alive_cells']):>7}{a100:>8.2f}")
    out[strat] = dict(n=s["n"], stages=dict(s["stages"]),
                      funnel_pass=s["funnel_pass"], assays=s["assays"],
                      cells_first=s["cells"], alive_cells_first=s["alive_cells"],
                      cells_per100=c100, alive_per100=a100,
                      ops=dict(s["ops"]), cross=dict(s["cross"]))

# evolver-exclusive cells: in evolver first-touch AND never touched by sampler at all
sam_cells = set()
for ts, strat, r in rows:
    if strat.startswith("sampler") and r.get("cell"):
        sam_cells.add(r["cell"])
for strat in out:
    if strat.startswith("evolver"):
        out[strat]["cells_sampler_never_touched"] = \
            [c for c in out[strat]["cells_first"] if c not in sam_cells]
        print(f"{strat}: cells sampler never touched: "
              f"{len(out[strat]['cells_sampler_never_touched'])}")

os.makedirs(os.path.join(BASE, "data"), exist_ok=True)
with open(os.path.join(BASE, "data", "compare_yield.json"), "w") as f:
    json.dump(out, f, indent=1)
print("written data/compare_yield.json")
