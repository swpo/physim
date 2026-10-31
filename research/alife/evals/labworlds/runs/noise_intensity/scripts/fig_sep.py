"""Control ratios (median over partitions, 5-95% whiskers) and the native band vs intensity, per world and sensor."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "out"
R = json.loads((OUT / "separation.json").read_text())
names = {"pm": "phase_membrane (pulse_d0_K; ablation chi=0)", "fv": "fed vortices (pulse_d0_om; ablation adv=0)"}
fig, axes = plt.subplots(2, 4, figsize=(15, 6.5), sharex="row")
for row, world in enumerate(("pm", "fv")):
    if world not in R:
        continue
    lv = sorted(R[world], key=float)
    x = np.array([float(v) for v in lv])
    for col, s in enumerate(("agg", "device0", "device1", "global")):
        ax = axes[row, col]
        for key, c, lab in (("ablation", "tab:red", "ablation / native"), ("ignore_actions", "tab:blue", "ignore actions / native"),
                            ("dt_half_null", "tab:green", "dt/2 null / native")):
            ys = [R[world][v]["50tu"][s].get(key) for v in lv]
            ok = [i for i, y in enumerate(ys) if y]
            if not ok:
                continue
            y = np.array([ys[i] for i in ok])
            ax.errorbar(x[ok], y[:, 1], yerr=[y[:, 1] - y[:, 0], y[:, 2] - y[:, 1]], color=c, marker="o", ms=4,
                        capsize=3, label=lab)
        b = np.array([R[world][v]["50tu"][s]["band"] for v in lv])
        ax.fill_between(x, b[:, 0], b[:, 2], color="0.8", label="native vs native 5-95%")
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.axhline(1, color="0.5", lw=0.8)
        ax.set_title(f"{world} {s}", fontsize=9)
        ax.grid(alpha=0.3, which="both")
        if row == 1:
            ax.set_xlabel("noise intensity (ell = 2 world units)")
    axes[row, 0].set_ylabel(names[world].split(" (")[0] + ": score ratio")
axes[0, 0].legend(fontsize=7)
fig.suptitle("Energy-score ratio to an independent native, 50 tu window (8 members; 2000 partitions of 24 natives)", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "separation.png", dpi=105)
