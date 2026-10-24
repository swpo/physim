"""Run fl_forager_gene2 and save snapshots (matter, log g) every --every steps for offline audit.

python threads/flow-lenia/scripts/record_gene.py WORLD OUT.npz --seed 0 --steps 12000 --every 20 --set k=v
"""
import argparse, ast, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from labkit.world import load_world  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("world"); ap.add_argument("out")
ap.add_argument("--seed", type=int, default=0); ap.add_argument("--steps", type=int, default=12000)
ap.add_argument("--every", type=int, default=20); ap.add_argument("--set", nargs="*", default=[])
a = ap.parse_args()
W = load_world(a.world)
for kv in a.set:
    k, v = kv.split("=", 1)
    try: v = ast.literal_eval(v)
    except Exception: pass
    W.CFG[k] = v
s = W.init(a.seed, tuple(W.META["size"]))
Ms, Gs, ts = [], [], []
for t in range(a.steps + 1):
    if t: s = W.step(s)
    if t % a.every == 0:
        A = s["A"].sum(0)
        Ms.append(A.astype(np.float16)); Gs.append(np.where(A > 1e-3, s["P"][0], 0).astype(np.float16)); ts.append(t)
np.savez_compressed(a.out, matter=np.stack(Ms), logg=np.stack(Gs), t=np.array(ts), phi_final=s["phi"].astype(np.float16))
Path(a.out.replace(".npz", ".json")).write_text(json.dumps({"events": s["events"], "parents": s["parents"], "born": s["born"],
                                                         "cfg": {k: v for k, v in W.CFG.items() if isinstance(v, (int, float, str, bool, type(None)))}}))
A = s["A"].sum(0); m = A > 1e-3
print(f"seed {a.seed} {a.set}: events {len(s['events'])} final mean log g {(A[m]*s['P'][0][m]).sum()/A[m].sum():.3f}", flush=True)
