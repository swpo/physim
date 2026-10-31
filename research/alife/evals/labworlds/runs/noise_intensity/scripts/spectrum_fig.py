import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "out"
d = json.loads((OUT / "spectrum.json").read_text())
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
cols = {"None": "k", "1.0": "tab:blue", "2.0": "tab:orange", "4.0": "tab:red"}
ls = {96: ":", 128: "-", 192: "--", 256: "-."}
for ax, form in zip(axes, ("intensity", "per-point (legacy)")):
    for key, c in d["curves"].items():
        f, N, ell = key.split("|")
        if f != form:
            continue
        k, S = np.array(c["k"]), np.array(c["S"])
        ax.loglog(k, S, ls[int(N)], color=cols[ell], lw=1.2,
                  label=f"N={N} (dx {128 / int(N):.2f}), ell={'white' if ell == 'None' else ell}")
    ax.set_title(f"additive noise, {form}: S(k) / sd^2")
    ax.set_xlabel("k (rad per world unit)")
    ax.axvspan(2 * np.pi / 128 * 0.9, 2 * 2 * np.pi / 128 * 1.05, color="0.9", zorder=-1)
    ax.set_ylim(1e-4, 500)
    ax.grid(alpha=0.3, which="both")
axes[0].set_ylabel("continuum spectral density / sd^2 (box 128 world units)")
axes[1].legend(fontsize=6, ncol=2, loc="lower left")
fig.tight_layout()
fig.savefig(OUT / "spectrum.png", dpi=110)
