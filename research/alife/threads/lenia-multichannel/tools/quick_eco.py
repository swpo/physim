"""Quick look at a two-species world: per-species mass / cell count and a strip (A cyan-ish, B magenta-ish, food green)."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from labkit.world import load_world  # noqa: E402
from quick import ncomp  # noqa: E402

W = load_world(sys.argv[1]); out = sys.argv[2]; steps = int(sys.argv[3]); size = int(sys.argv[4])
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0
for kv in sys.argv[6:]:
    k, v = kv.split("=", 1); setattr(W, k, eval(v, dict(vars(W)) | {"np": np}))
s = W.init(seed, (size, size)); tiles = []; log = []
every = max(1, steps // 11)
for t in range(steps + 1):
    if t % every == 0:
        a, b, f = s["A"].sum(0), s["B"].sum(0), s["F"]
        log.append(f"{t}:A{a.sum():.0f}/{ncomp(s['A'][0])} B{b.sum():.0f}/{ncomp(s['B'][0])} F{f.mean():.2f}")
        rgb = np.stack([np.clip(b, 0, 1), 0.45 * np.clip(f, 0, 1), np.clip(a, 0, 1)], -1)
        tiles.append(np.pad((255 * rgb).astype(np.uint8), ((2, 2), (2, 2), (0, 0)), constant_values=60))
    if t < steps:
        s = W.step(s)
Image.fromarray(np.concatenate(tiles, 1)).save(out)
print(" ".join(log))
