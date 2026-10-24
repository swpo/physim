"""Quick screening: run a world with parameter overrides, save a dimmed-substrate strip and stats.

python threads/autopoiesis/screen.py WORLD OUT.png steps nframes key=val ...
"""
import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, "."); from labkit.world import load_world

COL = np.array([[0.12, 0.25, 0.3], [1.0, 0.55, 0.1], [0.95, 0.2, 0.55], [0.45, 0.95, 0.3], [0.95, 0.9, 0.25]])


def img(F):
    rgb = np.tensordot(np.clip(F[:len(COL)], 0, None).transpose(1, 2, 0) / np.maximum(F.reshape(len(F), -1).max(1), 1e-9)[None, None, :len(COL)], COL[:len(F)], axes=1)
    return (np.clip(rgb, 0, 1) * 255).astype(np.uint8)


def stats(W, s):
    if hasattr(W, "stats"):
        return W.stats(s)
    return {}


def run(path, out, steps, nfr, over, seed=0, size=None):
    W = load_world(path)
    for kv in over:
        k, v = kv.split("=")
        if k == "size":
            size = (int(v), int(v)); continue
        if k == "seed":
            seed = int(v); continue
        W.P[k] = type(W.P[k])(eval(v)) if not isinstance(W.P[k], str) else v
    s = W.init(seed, tuple(size or W.META["size"]))
    tiles, st = [], []
    every = max(1, steps // nfr)
    for t in range(steps + 1):
        if t:
            s = W.step(s)
        if t % every == 0:
            F = np.asarray(W.fields(s), np.float32)
            tiles.append(img(F))
            st.append(stats(W, s))
    sc = max(1, 192 // tiles[0].shape[0])
    strip = np.concatenate([np.pad(np.kron(t, np.ones((sc, sc, 1), np.uint8)), ((2, 2), (2, 2), (0, 0)), constant_values=60) for t in tiles], 1)
    Image.fromarray(strip).save(out)
    return st


if __name__ == "__main__":
    a = sys.argv
    st = run(a[1], a[2], int(a[3]), int(a[4]), a[5:])
    for i, x in enumerate(st):
        print(i, json.dumps(x))
