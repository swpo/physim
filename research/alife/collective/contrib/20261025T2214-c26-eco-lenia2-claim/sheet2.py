# species-coloured sheet from a labkit pack's frames.npz: A core (red), B core (blue), food (green)
import sys, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
z = np.load(sys.argv[1]); keys = list(z.keys())
F = z["render"]
t = z["render_f"] * 2.0
idx = np.linspace(0, len(F) - 1, 12).astype(int)
fig, ax = plt.subplots(2, 6, figsize=(15, 5.3))
for a, i in zip(ax.ravel(), idx):
    f = F[i]
    a.imshow(np.stack([np.clip(f[0], 0, 1), np.clip(f[6], 0, 1) * 0.45, np.clip(f[3], 0, 1)], -1))
    a.set_title(f"t={float(t[i]):.0f}", fontsize=9); a.axis("off")
plt.suptitle(sys.argv[3] if len(sys.argv) > 3 else sys.argv[1], fontsize=9)
plt.tight_layout(); plt.savefig(sys.argv[2], dpi=65)
