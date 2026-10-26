"""Audit figure and table: cut vs twin after a 40% front cut at t=8 on fresh seeds (cutprobe.py output).
Rows: seed 6 (dies), seed 9 (repolarises), seed 6 at dt/2 (survives); columns t=8..13; layer s in colour,
phi=1/2 contour in cyan, polarity rho=0.3 contour in white. Table: area, polarity and speed after the cut."""
import os, json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, "runs")
rows = [("seed 6 cut", "cut_s6_cut"), ("seed 6 twin", "cut_s6_twin"), ("seed 9 cut", "cut_s9_cut"), ("seed 6 dt/2 cut", "cut_s6_dthalf_cut")]
ts = [8.0, 9.0, 10.0, 11.0, 12.0, 13.0]
fig, ax = plt.subplots(len(rows), len(ts), figsize=(2.2 * len(ts), 2.3 * len(rows)))
for i, (lab, f) in enumerate(rows):
    for j, t in enumerate(ts):
        a = ax[i, j]; a.set_xticks([]); a.set_yticks([])
        p = os.path.join(R, f"{f}_t{t:.1f}.npz")
        if not os.path.exists(p): a.set_title(f"{lab} t={t:.0f} (n/a)", fontsize=7); continue
        d = np.load(p); a.imshow(d["s"], cmap="viridis", vmin=0, vmax=0.4, origin="lower")
        if d["phi"].max() > 0.5: a.contour(d["phi"], [0.5], colors="c", linewidths=0.7)
        if (d["rho"] * (d["phi"] > 0.5)).max() > 0.3: a.contour(d["rho"] * (d["phi"] > 0.5), [0.3], colors="w", linewidths=0.6)
        a.set_title(f"{lab} t={t:.0f}", fontsize=7)
plt.tight_layout(); plt.savefig(os.path.join(H, "audit_cuts.png"), dpi=70)
out = []
for name in ("cut_s6", "cut_s7", "cut_s8", "cut_s9", "cut_s6_dthalf"):
    p = os.path.join(R, name + ".json")
    if not os.path.exists(p): continue
    d = json.load(open(p))
    for arm in ("cut", "twin"):
        r = d[arm]; t = np.array([x["t"] for x in r]); A = np.array([x["area"] for x in r]); pol = np.array([x["pol"] for x in r])
        cx = np.array([x["cx"] for x in r]); cy = np.array([x["cy"] for x in r]); L = 5.0
        dxy = np.c_[(np.diff(cx) + L / 2) % L - L / 2, (np.diff(cy) + L / 2) % L - L / 2]; sp = np.hypot(*dxy.T) / np.diff(t)
        late = t[1:] >= max(t[-1] - 2, 11)
        dead = A[-1] < 0.05
        out.append(f"{name:16s} {arm:4s} t_end {t[-1]:5.2f}  area min/end {A.min():.2f}/{A[-1]:.2f}  polarity min(t 8-11) {pol[(t>=8)&(t<=11)].min():.3f} end {pol[-1]:.3f}  speed last 2 t {np.nanmedian(sp[late]) if late.any() and not dead else 0:.3f}  {'DEAD at t=%.2f' % t[np.argmax(A < 0.05)] if dead else 'alive'}")
open(os.path.join(H, "audit_table.txt"), "w").write("\n".join(out) + "\n"); print("\n".join(out))
