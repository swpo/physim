"""Per-channel crops + a line profile through one cell (from a pack's frames.npz).
python chanview.py PACK OUT.png [frame_index] [cy cx half]"""
import sys, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
z = np.load(sys.argv[1] + "/frames.npz"); R = z["render"].astype(np.float32)
k = int(sys.argv[3]) if len(sys.argv) > 3 else -1
F = R[k]; C, H, W = F.shape
if len(sys.argv) > 6:
    cy, cx, half = map(int, sys.argv[4:7])
else:
    from scipy import ndimage
    lab, n = ndimage.label(F[1] > 0.5 * F[1].max())
    cy, cx = [int(v) for v in ndimage.center_of_mass(F[1], lab, 1 + np.argmax(np.bincount(lab.ravel())[1:]))]
    half = 16
F = np.roll(np.roll(F, H // 2 - cy, 1), W // 2 - cx, 2)[:, H // 2 - half:H // 2 + half, W // 2 - half:W // 2 + half]
names = sys.argv[8:] or [f"c{i}" for i in range(C)]
fig, ax = plt.subplots(1, C + 1, figsize=(3 * (C + 1), 3))
for c in range(C):
    ax[c].imshow(F[c], cmap="magma"); ax[c].set_title(f"ch{c} max {F[c].max():.2f}"); ax[c].axis("off")
for c in range(C):
    ax[C].plot(F[c, half, :] / max(F[c].max(), 1e-9), label=f"ch{c}")
ax[C].legend(fontsize=7); ax[C].set_title("row profile (norm)")
fig.tight_layout(); fig.savefig(sys.argv[2], dpi=70)
