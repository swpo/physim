"""recompute.py — uniform battery recompute from saved npz runs.
python3 recompute.py <metrics_module> [glob]"""
import glob, json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stage2", "lib"))
import soup_sim
import genome as G
from soup_assay import js

def main():
    mn = sys.argv[1] if len(sys.argv) > 1 else "metrics_dev"
    pat = sys.argv[2] if len(sys.argv) > 2 else "gt_*_s*.npz"
    M = __import__(mn)
    for p in sorted(glob.glob(os.path.join(HERE, "runs", pat))):
        rec = soup_sim.load_run(p)
        out = M.full_battery(rec)
        tag = os.path.basename(p).rsplit("_s", 1)[0]
        seed = int(os.path.basename(p).rsplit("_s", 1)[1].split(".")[0])
        row = dict(kind="soup_assay", world=rec["world"], tag=tag, seed=seed,
                   T=float(rec["T"]), L=float(rec["L"]), dtype=rec["dtype"],
                   status=rec["status"], wall_sim=rec["wall_s"],
                   metrics=mn, battery=js(out), src="recompute")
        G.append_result(row, path=os.path.join(HERE, "results.json"))
        print(tag, seed, round(out["interest"], 1),
              {k: round(v, 2) for k, v in out["C"].items()})

if __name__ == "__main__":
    main()
