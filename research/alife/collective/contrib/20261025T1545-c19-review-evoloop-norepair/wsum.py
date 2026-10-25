"""c19: tally wound.py results: loops tested, twins alive, wounded alive, cells removed (mean)."""
import json, glob
rows = []
for f in sorted(glob.glob("results/*.json")):
    d = json.load(open(f)); L = d["loops"]
    rows.append({"file": f.split("/")[-1], "mode": d["mode"], "k": d["kcells"] if d["mode"] == "core" else None, "seed": d["seed"], "loops": len(L),
                 "twin_alive": sum(x["twin"]["hole_alive"] for x in L), "wounded_alive": sum(x["ablated"]["hole_alive"] for x in L),
                 "both_alive": sum(x["twin"]["hole_alive"] and x["ablated"]["hole_alive"] for x in L),
                 "mean_cells_removed": round(sum(x["cells_removed"] for x in L) / max(len(L), 1), 1), "mean_loop_cells": round(sum(x["loop_cells"] for x in L) / max(len(L), 1))})
json.dump(rows, open("wound_summary.json", "w"), indent=1)
for r in rows: print(r)
