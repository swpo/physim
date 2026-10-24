"""Driver for ad9-ledger: run, save ledger/series JSON and a frame stack for movies.
python evo_run.py out_dir --seed s --steps N --size S [--set k=v ...]"""
import argparse, json, sys, time
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from labkit.world import load_world
ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--world", default="worlds/ad9-ledger/world.py")
ap.add_argument("--seed", type=int, default=0); ap.add_argument("--steps", type=int, default=16000)
ap.add_argument("--size", type=int, default=128); ap.add_argument("--nframes", type=int, default=120)
ap.add_argument("--set", nargs="*", default=[])
a = ap.parse_args(); W = load_world(Path(__file__).parent / a.world)
for kv in a.set:
    k, v = kv.split("="); W.P[k] = type(W.P[k])(eval(v))
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
s = W.init(a.seed, (a.size, a.size)); every = max(1, a.steps // a.nframes); frames, ft = [], []
t0 = time.time()
for i in range(a.steps + 1):
    if i:
        s = W.step(s)
    if i % every == 0:
        frames.append(W.fields(s).astype(np.float16)); ft.append(s["t"])
np.savez_compressed(out / "frames.npz", render=np.stack(frames), t=np.array(ft))
L = s["ledger"]
kinds = {}
for e in L:
    kinds.setdefault(e[0], []).append(e[2] if e[0] in ("birth", "death", "kill", "nucleate") else (e[2], e[3]))
per = {k: np.bincount([x for x in v if isinstance(x, int)], minlength=7).tolist() for k, v in kinds.items()
       if k in ("birth", "death", "kill", "nucleate")}
json.dump({"params": W.P, "seed": a.seed, "steps": a.steps, "wall": time.time() - t0, "ledger": L,
           "series": s["series"], "per_rung": per,
           "counts": {k: len(v) for k, v in kinds.items()}}, open(out / "ledger.json", "w"), default=str)
ser = s["series"]
print(f"{out.name}: wall {time.time()-t0:.0f}s counts {{k: len(v) for k, v in kinds.items()}} ".replace("{k: len(v) for k, v in kinds.items()}", str({k: len(v) for k, v in kinds.items()})),
      f"final n={ser[-1][1]} meankp={ser[-1][2]:.2f} rungs={ser[-1][3]}")
