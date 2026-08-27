"""verify_v02/g1_run.py — G1: run_assay_b(backend=cpu) vs LOCKED run_assay.
Bitwise battery+horizon identity (wall-clock fields stripped). One world per call.
Usage: g1_run.py <world> <seed>"""
import json, os, sys, time

os.environ.setdefault("BLOBKIT_RESULTS", "")
import blobkit.assay_v2 as A
import blobkit.assay_v2b as AB
from blobkit.soup.backend import get_backend
from blobkit import worlds

STRIP = {"wall_total", "wall_s", "wall_sim"}

def strip_wall(o):
    if isinstance(o, dict):
        return {k: strip_wall(v) for k, v in o.items() if k not in STRIP}
    if isinstance(o, (list, tuple)):
        return [strip_wall(v) for v in o]
    return o

def canon(out):
    return json.dumps(strip_wall(A.js(out)), sort_keys=True)

def main():
    world, seed = sys.argv[1], int(sys.argv[2])
    g = worlds.WORLDS[world]()
    kicks = worlds.KICKS.get(g["id"])
    t0 = time.time()
    ref = A.run_assay(worlds.WORLDS[world](), seed=seed, kicks=kicks,
                      results_path=None, verbose=True)
    t1 = time.time()
    new = AB.run_assay_b(worlds.WORLDS[world](), seed=seed, kicks=kicks,
                         results_path=None, verbose=True,
                         backend=get_backend("cpu"))
    t2 = time.time()
    cr, cn = canon(ref), canon(new)
    res = dict(world=world, seed=seed, gate="G1",
               match_bitwise=(cr == cn),
               ref=dict(interest=ref["interest"], T=ref["horizon"]["T_used"],
                        why=ref["horizon"]["why_stopped"], wall=round(t1-t0,1)),
               new=dict(interest=new["interest"], T=new["horizon"]["T_used"],
                        why=new["horizon"]["why_stopped"], wall=round(t2-t1,1)),
               canon_chars=len(cr))
    if cr != cn:
        for i, (a, b) in enumerate(zip(cr, cn)):
            if a != b:
                res["first_diff"] = dict(pos=i, ref=cr[max(0,i-80):i+80],
                                         new=cn[max(0,i-80):i+80])
                break
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       f"G1_{world}_s{seed}.json")
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "first_diff"}))
    sys.exit(0 if res["match_bitwise"] else 1)

if __name__ == "__main__":
    main()
