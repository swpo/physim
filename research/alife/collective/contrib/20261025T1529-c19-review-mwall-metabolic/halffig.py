"""c19: half-domain feed cut (left half, x < 64, from t=60000) vs the fed twin, seed 5: wall (render ch 3) in green,
catalyst (ch 1) in blue, M (ch 5) in red; the dashed line marks the cut boundary."""
import json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
runs = [("fed", "fed/seed5"), ("left half starved", "halfstarve/seed5")]; times = [59000, 61000, 70000, 85000, 100000]
fig, ax = plt.subplots(2, len(times), figsize=(2.3 * len(times), 5))
for r, (lab, d) in enumerate(runs):
    F = np.load(d + "/frames.npz"); RF = F["render_f"] * json.load(open(d + "/metrics.json"))["steps_per_frame"]; R = F["render"].astype(np.float32)
    for c, t in enumerate(times):
        i = int(np.argmin(np.abs(RF - t)))
        rgb = np.clip(np.stack([R[i, 5], R[i, 3], R[i, 1] / max(R[:, 1].max(), 1e-6)], -1), 0, 1)
        a = ax[r, c]; a.imshow(rgb); a.axvline(63.5, ls="--", c="w", lw=0.6); a.set_title(f"{lab} t={RF[i]:.0f}", fontsize=7); a.set_xticks([]); a.set_yticks([])
plt.tight_layout(); plt.savefig("halfstarve_s5.png", dpi=75)
