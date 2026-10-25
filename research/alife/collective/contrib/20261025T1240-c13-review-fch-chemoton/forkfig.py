"""c13: amphiphile u+1 at matching times in the fed run, the global feed cut and the local feed cut (seed 7),
and fed vs global cut (seed 8). Full frames, fixed scale; the local-cut disk is outlined."""
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
rows = [("fed s7", "rerun/seed7"), ("global cut s7", "rerun_starve/seed7"), ("local cut s7 (disk)", "rerun_local/seed7"),
        ("fed s8", "rerun/seed8"), ("global cut s8", "rerun_starve/seed8")]
ts = [297, 400, 500, 600, 900]
fig, ax = plt.subplots(len(rows), len(ts), figsize=(2.2 * len(ts), 2.3 * len(rows)))
for i, (lab, p) in enumerate(rows):
    d = np.load(p + "/frames.npz"); R = d["render"]; f = d["render_f"] * 3.0
    for j, t in enumerate(ts):
        a = ax[i, j]; a.set_xticks([]); a.set_yticks([])
        if t > f.max() + 5: a.axis("off"); continue
        k = int(np.argmin(abs(f - t))); a.imshow(R[k, 0], vmin=0, vmax=2.2, cmap="magma")
        a.contour(R[k, 2], levels=[0.3], colors="c", linewidths=0.6)
        if "local" in lab: a.add_patch(plt.Circle((123, 44), 48, fill=False, ec="w", ls="--", lw=0.8))
        a.set_title(f"{lab} t={f[k]:.0f}", fontsize=7)
plt.suptitle("u+1 (magma), catalyst K=0.3 contour (cyan); feed cut at t=300", fontsize=9)
plt.tight_layout(); plt.savefig("fork_c13.png", dpi=80)
