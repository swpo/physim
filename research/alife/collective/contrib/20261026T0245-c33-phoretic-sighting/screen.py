"""screen.py: run the world with WORLD_P overrides and save particle snapshots (A red, B blue)."""
import sys, os, time, json, importlib.util, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
wp, out, frames, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 0
spec = importlib.util.spec_from_file_location("w", wp); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, (128, 128)); snaps = []; allx = []; T0 = time.time(); keep = np.linspace(0, frames, 7).astype(int)
for f in range(frames + 1):
    allx.append(s["x"].astype(np.float32).copy())
    if f in keep: snaps.append((s["t"], s["x"].copy()))
    if f < frames: s = w.step(s)
L = w.P["L"]; fig, ax = plt.subplots(1, len(snaps), figsize=(3 * len(snaps), 3.2))
for a, (t, x) in zip(ax, snaps):
    for k, col in ((0, "red"), (1, "blue")):
        m = s["sp"] == k; a.scatter(x[m, 0], x[m, 1], s=0.6, c=col)
    a.set_xlim(0, L); a.set_ylim(0, L); a.set_aspect(1); a.set_xticks([]); a.set_yticks([]); a.set_title(f"t={t:.0f}")
fig.suptitle(os.environ.get("WORLD_P", "{}"), fontsize=8); fig.tight_layout(); fig.savefig(out, dpi=90)
np.savez_compressed(out.replace(".png", ".npz"), x=np.array(allx), sp=s["sp"], L=L, dt=w.P["dt"] * w.P["sub"])
print(out, "wall", round(time.time() - T0, 1))
