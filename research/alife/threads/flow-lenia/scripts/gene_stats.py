"""Trait trajectory for fl_forager_gene: mass-weighted mean/sd of log g, bodies, matter.

python threads/flow-lenia/scripts/gene_stats.py WORLD OUT --steps 8000 --every 100 --seeds 0 1 2 --set k=v
Writes OUT.json (per seed series + genealogy). Plot with gene_plot.py.
"""
import argparse, ast, json, sys
from pathlib import Path
import numpy as np
from scipy import ndimage
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from labkit.world import load_world  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("world"); ap.add_argument("out")
ap.add_argument("--steps", type=int, default=8000); ap.add_argument("--every", type=int, default=100)
ap.add_argument("--seeds", type=int, nargs="+", default=[0]); ap.add_argument("--set", nargs="*", default=[])
ap.add_argument("--size", type=int, nargs=2)
a = ap.parse_args()
runs = {}
for sd in a.seeds:
    W = load_world(a.world)
    for kv in a.set:
        k, v = kv.split("=", 1)
        try: v = ast.literal_eval(v)
        except Exception: pass
        W.CFG[k] = v
    s = W.init(sd, tuple(a.size or W.META["size"]))
    r = {"t": [], "mean": [], "sd": [], "bodies": [], "matter": [], "body_g": []}
    for t in range(a.steps + 1):
        if t: s = W.step(s)
        if t % a.every == 0:
            A = s["A"].sum(0); lg = s["P"][0]; m = A > 1e-3
            w = A[m] / A[m].sum()
            mu = float((w * lg[m]).sum()); r["t"].append(t); r["mean"].append(mu)
            r["sd"].append(float(np.sqrt((w * (lg[m] - mu) ** 2).sum())))
            lab, n = ndimage.label(ndimage.gaussian_filter(A, 1, mode="wrap") > 0.15)
            if n:
                mass = ndimage.sum(A, lab, range(1, n + 1)); gm = ndimage.sum(A * lg, lab, range(1, n + 1))
                ok = mass > 2
                r["body_g"].append((gm[ok] / mass[ok]).round(3).tolist()); r["bodies"].append(int(ok.sum()))
            else:
                r["body_g"].append([]); r["bodies"].append(0)
            r["matter"].append(float(A.sum()))
    r["parents"] = s["parents"]; r["born"] = s["born"]; r["gval"] = s["gval"]
    runs[sd] = r
    print(sd, "final mean log g %.3f sd %.3f bodies %d matter %.0f mutations %d" % (r["mean"][-1], r["sd"][-1], r["bodies"][-1], r["matter"][-1], len(r["parents"]) - 1), flush=True)
Path(a.out + ".json").write_text(json.dumps({"args": vars(a), "runs": runs}))
