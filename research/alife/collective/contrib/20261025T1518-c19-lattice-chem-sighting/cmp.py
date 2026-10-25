"""c19: lattice-chem at t=4000, seed 0, 96^2: A and M with the orientation bonus (lam=25) and without (lam=0)."""
import os, sys, importlib.util, json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(2, 3, figsize=(10, 6.8))
for r, lam in enumerate([25.0, 0.0]):
    os.environ["WORLD_P"] = json.dumps({"lam": lam})
    spec = importlib.util.spec_from_file_location("w", sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
    s = w.init(0, (96, 96))
    for t in range(4000): w.step(s)
    f = w.fields(s); z = slice(24, 72)
    rgb = np.stack([f[0] / f[0].max(), f[2] / f[2].max() * 0.6, f[1] / f[1].max()], -1)
    ax[r, 0].imshow(rgb); ax[r, 0].set_title(f"lam={lam:g}, t=4000: R=A, G=X, B=M", fontsize=9)
    ax[r, 1].imshow(f[0][z, z], cmap="Reds"); ax[r, 1].set_title("A (autocatalyst), 48x48 crop", fontsize=9)
    ax[r, 2].imshow(f[1][z, z], cmap="Blues"); ax[r, 2].set_title("M (membrane), same crop", fontsize=9)
    for a in ax[r]: a.set_xticks([]); a.set_yticks([])
plt.tight_layout(); plt.savefig(sys.argv[2], dpi=70)
