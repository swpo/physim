"""c47: crops of the envelope A around (y, x) every DS time units from t0 (world.py, seed). usage: python zoom.py SEED T0 Y X OUT.png [DS=5] [N=12]"""
import sys, os, importlib.util, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py"))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, t0, y, x, out = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
DS = float(sys.argv[6]) if len(sys.argv) > 6 else 5.0; N = int(sys.argv[7]) if len(sys.argv) > 7 else 12
s = w.init(seed, w.META["size"])
while s["t"] < t0: w.step(s)
fig, ax = plt.subplots(2, N, figsize=(1.3 * N, 2.8)); r = 16
for j in range(N):
    F = w.fields(s); A = np.roll(np.roll(F[0], r - y, 0), r - x, 1)[:2 * r, :2 * r]; E = np.roll(np.roll(F[1], r - y, 0), r - x, 1)[:2 * r, :2 * r]
    ax[0, j].imshow(A, cmap="magma", vmin=0, vmax=1.6); ax[0, j].set_title(f"t={s['t']:.0f}", fontsize=7); ax[0, j].axis("off")
    ax[1, j].imshow(E, cmap="viridis", vmin=0, vmax=1); ax[1, j].axis("off")
    tn = s["t"] + DS
    while s["t"] < tn: w.step(s)
fig.suptitle(f"seed {seed}: envelope A (top) and pump energy E (bottom), 32x32 crop at ({y},{x})", fontsize=8)
fig.tight_layout(); fig.savefig(out, dpi=70)
