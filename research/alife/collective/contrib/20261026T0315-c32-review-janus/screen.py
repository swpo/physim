"""screen.py <world.py> <out.png> <frames> [seed]: run with WORLD_P overrides, save 7 particle snapshots
(A red, B blue, food grey) and every frame's positions and species to <out>.npz."""
import sys, os, time, importlib.util, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
wp, out, frames, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 0
spec = importlib.util.spec_from_file_location("w", wp); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, (128, 128)); snaps = []; allx = []; allsp = []; T0 = time.time(); keep = np.linspace(0, frames, 7).astype(int)
for f in range(frames + 1):
    allx.append(s["x"].astype(np.float32).copy()); allsp.append(s["sp"].astype(np.int8).copy())
    if f in keep: snaps.append((s["t"], s["x"].copy(), s["sp"].copy()))
    if f < frames: s = w.step(s)
L = w.P["L"]; fig, ax = plt.subplots(1, len(snaps), figsize=(3 * len(snaps), 3.2))
for a, (t, x, sp) in zip(ax, snaps):
    for k, col, sz in ((2, "0.8", 0.3), (0, "red", 0.6), (1, "blue", 0.6)):
        m = sp == k; a.scatter(x[m, 0], x[m, 1], s=sz, c=col)
    a.set_xlim(0, L); a.set_ylim(0, L); a.set_aspect(1); a.set_xticks([]); a.set_yticks([])
    a.set_title(f"t={t:.0f} A{(sp == 0).sum()} B{(sp == 1).sum()}", fontsize=8)
fig.suptitle(os.environ.get("WORLD_P", "{}"), fontsize=8); fig.tight_layout(); fig.savefig(out, dpi=90)
np.savez_compressed(out.replace(".png", ".npz"), x=np.array(allx), sp=np.array(allsp), L=L, dt=w.P["dt"] * w.P["sub"])
print(out, "wall", round(time.time() - T0, 1))
