"""K2 biomass share (sum K2 / sum (K1+K2)) over time for membrane_evo arms (labkit frames.npz; channels K1, K2). usage: k2share.py out.png label=dir ..."""
import sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, runs = sys.argv[1], [a.split("=", 1) for a in sys.argv[2:]]
fig, ax = plt.subplots(figsize=(7, 3.6))
for k, (lab, d) in enumerate(runs):
    F = np.load(d + "/frames.npz"); R, fr = F["render_f"], F["render"]  # render_f = frame index, render = fields
    R = F["render"]; t = F["render_f"] * 250
    sh = R[:, 1].sum(axis=(1, 2)) / np.maximum(R[:, 0].sum(axis=(1, 2)) + R[:, 1].sum(axis=(1, 2)), 1e-9)
    ax.plot(t, sh, color=f"C{k // 2}", ls="-" if "up" in lab else ":", label=lab)
    print(lab, "K2 share at t=20k/30k/40k:", round(float(sh[len(sh) // 2]), 3), round(float(sh[3 * len(sh) // 4]), 3), round(float(sh[-1]), 3))
ax.set_xlabel("t"); ax.set_ylabel("K2 biomass share"); ax.legend(fontsize=7); ax.set_title("membrane_evo: up arm (b2 = 1.3 b, solid) vs identical-event twin (b2 = b, dotted)", fontsize=9)
plt.tight_layout(); plt.savefig(out, dpi=80)
