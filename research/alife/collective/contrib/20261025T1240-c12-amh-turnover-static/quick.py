import sys, time, os, numpy as np, importlib.util, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
nf, spf, tag = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
s = w.init(0, (128, 128)); t0 = time.time(); snaps = []
for f in range(nf):
    for _ in range(spf): s = w.step(s)
    if not np.isfinite(s["phi"]).all(): print("NaN at", f); break
    if f % max(1, nf // 6) == 0 or f == nf - 1: snaps.append((f, s["phi"].copy()))
print(tag, "time", round(time.time() - t0), "umax", w.stats(s))
fig, ax = plt.subplots(1, len(snaps), figsize=(3 * len(snaps), 3.2))
for a, (f, p) in zip(ax, snaps): a.imshow(p, cmap="RdBu_r", vmin=-1.2, vmax=1.2); a.set_title(f"t={f*spf*w.P['dt']:.0f}", fontsize=8); a.axis("off")
plt.suptitle(tag + " " + os.environ.get("WORLD_P", ""), fontsize=8); plt.tight_layout(); plt.savefig(f"q_{tag}.png", dpi=60)
