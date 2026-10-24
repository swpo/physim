"""Prey flee-gene trajectory in fl_predator_gene (mass-weighted mean log f over prey), predator/prey matter.

python threads/flow-lenia/scripts/pgene_stats.py WORLD OUT --steps 10000 --every 100 --seeds 0 1 2 --set k=v
"""
import argparse, ast, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from labkit.world import load_world  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("world"); ap.add_argument("out")
ap.add_argument("--steps", type=int, default=10000); ap.add_argument("--every", type=int, default=100)
ap.add_argument("--seeds", type=int, nargs="+", default=[0]); ap.add_argument("--set", nargs="*", default=[])
a = ap.parse_args()
runs = {}
for sd in a.seeds:
    W = load_world(a.world)
    for kv in a.set:
        k, v = kv.split("=", 1)
        try: v = ast.literal_eval(v)
        except Exception: pass
        W.CFG[k] = v
    s = W.init(sd, tuple(W.META["size"]))
    r = {"t": [], "mean": [], "sd": [], "prey": [], "pred": []}
    for t in range(a.steps + 1):
        if t: s = W.step(s)
        if t % a.every == 0:
            A = s["A"][0] + s["A"][1]; lg = s["P"][0]; m = A > 1e-3
            w = A[m] / max(A[m].sum(), 1e-12)
            mu = float((w * lg[m]).sum())
            r["t"].append(t); r["mean"].append(mu); r["sd"].append(float(np.sqrt((w * (lg[m] - mu) ** 2).sum())))
            r["prey"].append(float(A.sum())); r["pred"].append(float((s["A"][2] + s["A"][3]).sum()))
    runs[sd] = r
    print(sd, "final mean log f %.3f sd %.3f prey %.0f pred %.0f mutations %d" % (r["mean"][-1], r["sd"][-1], r["prey"][-1], r["pred"][-1], len(s["parents"]) - 1), flush=True)
Path(a.out + ".json").write_text(json.dumps({"args": vars(a), "runs": runs}))
