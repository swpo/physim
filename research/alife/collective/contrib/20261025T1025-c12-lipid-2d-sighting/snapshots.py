import sys, time, os, numpy as np, importlib.util, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
nf = int(sys.argv[1]); tag = sys.argv[2]
s = w.init(0, (128, 128)); t0 = time.time(); snaps = []
for f in range(nf):
    s = w.step(s)
    if f % max(1, nf // 5) == 0 or f == nf - 1: snaps.append((f, s["x"].copy()))
print("time", time.time() - t0)
fig, ax = plt.subplots(1, len(snaps), figsize=(4 * len(snaps), 4))
for a, (f, x) in zip(ax, snaps):
    a.scatter(x[s["typ"] > 0, 0], x[s["typ"] > 0, 1], s=1, c="orange"); a.scatter(x[s["typ"] == 0, 0], x[s["typ"] == 0, 1], s=2, c="b")
    a.set_title(f"frame {f}"); a.set_aspect(1); a.set_xlim(0, w.P["L"]); a.set_ylim(0, w.P["L"])
plt.tight_layout(); plt.savefig(f"q_{tag}.png", dpi=60)
np.save(f"x_{tag}.npy", s["x"])
fig, ax = plt.subplots(1, 2, figsize=(12, 6)); x = s["x"]
for a, (x0, y0) in zip(ax, [(0, 0), (40, 40)]):
    m = (x[:, 0] > x0) & (x[:, 0] < x0 + 40) & (x[:, 1] > y0) & (x[:, 1] < y0 + 40)
    for t, col, sz in ((1, "orange", 12), (0, "b", 18)):
        mm = m & ((s["typ"] > 0) if t else (s["typ"] == 0)); a.scatter(x[mm, 0], x[mm, 1], s=sz, c=col)
    a.set_aspect(1)
plt.tight_layout(); plt.savefig(f"z_{tag}.png", dpi=60)
