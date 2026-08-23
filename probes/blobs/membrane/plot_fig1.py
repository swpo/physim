import sys, os, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BASE = os.path.dirname(os.path.abspath(__file__))
u0 = -0.7035399190279488
fig, axes = plt.subplots(2, 6, figsize=(19, 6.6))
Ns = [4, 5, 6, 8, 10, 12]
for j, N in enumerate(Ns):
    F = np.load(f"{BASE}/data/R1_A4s_N{N}_wn_final.npz")["F"].astype(float)
    ax = axes[0, j]
    im = ax.imshow(F[0] - u0, origin="lower", extent=[0, 96, 0, 96], cmap="magma",
                   vmin=-0.25, vmax=1.9)
    ax.set_title(f"N={N} u-field (5000tu, noise)", fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
    ax2 = axes[1, j]
    im2 = ax2.imshow(F[0] - u0, origin="lower", extent=[0, 96, 0, 96], cmap="RdBu_r",
                     vmin=-0.06, vmax=0.06)
    ax2.set_title("tail scale +-0.06", fontsize=8)
    ax2.set_xticks([]); ax2.set_yticks([])
fig.suptitle("R1 CERTIFIED: closed blob rings, A4s family (tau=2.5 Dv=1.6), T=5000tu, working noise 2e-3 — ncomp==N, bond graph = C_N throughout", fontsize=11)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(f"{BASE}/strips/fig1_R1_ring_portraits.png", dpi=110)
print("saved fig1")
