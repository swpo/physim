import sys, os, importlib.util, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
os.environ["WORLD_P"] = sys.argv[1]; T = int(sys.argv[2]); L = int(sys.argv[3]); out = sys.argv[4]; seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0
spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, (L, L)); snaps = []
for t in range(T + 1):
    if t % (T // 4) == 0: snaps.append((t, w.fields(s).copy())); print(t, w.stats(s), flush=True)
    w.step(s)
fig, ax = plt.subplots(len(snaps), 3, figsize=(10, 3.3 * len(snaps)))
for r, (t, f) in enumerate(snaps):
    rgb = np.stack([f[0] / max(f[0].max(), 1), f[2] / max(f[2].max(), 1) * 0.6, f[1] / max(f[1].max(), 1)], -1)
    ax[r, 0].imshow(rgb); ax[r, 0].set_title(f"t={t} R=A G=X B=M", fontsize=8)
    c = L // 2; z = slice(c - 24, c + 24)
    ax[r, 1].imshow(f[0][z, z], cmap="Reds"); ax[r, 1].set_title("A zoom", fontsize=8)
    ax[r, 2].imshow(f[1][z, z], cmap="Blues"); ax[r, 2].set_title("M zoom", fontsize=8)
    for a in ax[r]: a.set_xticks([]); a.set_yticks([])
plt.tight_layout(); plt.savefig(out, dpi=65)
