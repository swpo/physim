import sys, importlib.util, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
seed, T, out = int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
s = W.init(seed, W.META["size"]); times = np.linspace(0, T, 7); snaps = []
k = 0
while True:
    if len(snaps) < len(times) and s["t"] >= times[len(snaps)] - 1e-9:
        lab, nb = W.plabel(s["phi"] > 0.5); snaps.append((s["t"], s["phi"].copy(), (s["rho"] * (s["phi"] > 0.5)).copy(), s["s"].copy(), nb))
        print(f"t={s['t']:.2f} bodies={nb} area={float((s['phi']>0.5).mean()):.3f}", flush=True)
    if s["t"] >= T - 1e-9: break
    s = W.step(s)
fig, ax = plt.subplots(2, len(snaps), figsize=(2.6*len(snaps), 5.4))
for j, (t, phi, rho, S, nb) in enumerate(snaps):
    ax[0, j].imshow(rho, origin="lower", cmap="viridis", vmin=0, vmax=1.2); ax[0, j].contour(phi, [0.5], colors="w", linewidths=0.5); ax[0, j].set_title(f"rho t={t:.1f} n={nb}", fontsize=8)
    ax[1, j].imshow(S, origin="lower", cmap="magma", vmin=0, vmax=0.6); ax[1, j].set_title("layer s", fontsize=8)
    for a in ax[:, j]: a.set_xticks([]); a.set_yticks([])
plt.tight_layout(); plt.savefig(out, dpi=75)
