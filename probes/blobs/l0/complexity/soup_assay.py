"""soup_assay.py — S1 driver: build world -> soup run -> battery -> save.
Usage: python3 soup_assay.py <world|genome.json> [--seed N] [--T x] [--L x]
       [--tag name] [--dtype f32|f64] [--workers n]
Writes runs/<tag>_s<seed>.npz (raw) + appends a summary row to results.json.
"""
import argparse, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stage2", "lib"))
import worlds, soup_sim
import genome as G

RESULTS = os.path.join(HERE, "results.json")


def js(o):
    if isinstance(o, dict):
        return {k: js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [js(v) for v in o]
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("world")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--T", type=float, default=5000.0)
    ap.add_argument("--L", type=float, default=128.0)
    ap.add_argument("--tag", default=None)
    ap.add_argument("--dtype", default="f32")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--nsoup", type=int, default=12)
    ap.add_argument("--metrics", default="metrics_dev")
    a = ap.parse_args()
    if a.world in worlds.WORLDS:
        g = worlds.WORLDS[a.world]()
    else:
        g = json.load(open(a.world))
    tag = a.tag or g.get("id", a.world)
    t0 = time.time()
    rec = soup_sim.run_soup(g, L=a.L, T=a.T, seed=a.seed, dtype=a.dtype,
                            workers=a.workers, n_soup=a.nsoup)
    path = os.path.join(HERE, "runs", f"{tag}_s{a.seed}.npz")
    soup_sim.save_run(rec, path)
    M = __import__(a.metrics)
    out = M.full_battery(rec)
    row = dict(kind="soup_assay", world=g.get("id"), tag=tag, seed=a.seed,
               T=a.T, L=a.L, dtype=a.dtype, status=rec["status"],
               wall_sim=rec["wall_s"], wall_total=round(time.time() - t0, 1),
               metrics=a.metrics, battery=js(out))
    G.append_result(row, path=RESULTS)
    print(json.dumps(dict(tag=tag, seed=a.seed, status=rec["status"],
                          interest=out["interest"],
                          C={k: round(v, 3) for k, v in out["C"].items()},
                          wall=row["wall_total"])))


if __name__ == "__main__":
    main()
