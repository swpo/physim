import sys, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
tdir = "/Users/spoho/Documents/prime/test/physim/probes/blobs/transport"

fig, axes = plt.subplots(2, 3, figsize=(15, 9))
for ax, jid, ch in ((axes[0,0], "park_B_ridge", 1), (axes[0,1], "Ap065_drift_eps0.01", 0),
                    (axes[0,2], "Bcurve_eps0.0075", 1), (axes[1,0], "wall16_persist", 0),
                    (axes[1,1], "conv_probe", 1), (axes[1,2], "Bflip_eps0.0125_s0", 1)):
    d = np.load(f"{tdir}/data/{jid}.npz")
    F = d["Ffinal"]
    im = ax.imshow(F[ch].T, origin="lower", cmap="magma")
    ax.set_title(f"{jid} u{ch+1} final", fontsize=9)
    plt.colorbar(im, ax=ax, fraction=0.04)
plt.tight_layout()
plt.savefig(f"{tdir}/strips/fig0_final_fields.png", dpi=110)
print("saved")
