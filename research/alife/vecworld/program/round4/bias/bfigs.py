"""bfigs -- figures of the round-4 study `bias` from results/combined.json and results/windows/ (local, matplotlib).

usage: python -B bfigs.py RESULTS_DIR
-> RESULTS_DIR/fig_ceiling_c1.png   closure ceiling (fixed family G) vs horizon, c = 1, one panel per objective,
                                    one line per encoder (receptive field), hand designs for reference
   RESULTS_DIR/fig_agreement.png    R^2 of each hand design from the learned latent (c = 1 and N8 at c = 2, 4)
   RESULTS_DIR/fig_windows.png      learned linear windows (L arm, c = 1, seed 0, fitted on A), raw units, c0 + c1
"""
import glob
import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

R = sys.argv[1]
C = json.load(open(os.path.join(R, "combined.json")))
HZ = C["horizons"]
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
plt.rcParams.update({"font.size": 9, "axes.edgecolor": "#c3c2b7", "axes.labelcolor": INK2, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.facecolor": SURF, "figure.facecolor": SURF, "text.color": INK,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False,
                     "axes.spines.right": False, "legend.frameon": False})
OBJ = [("clos", "closure (global head)"), ("local", "local law"), ("pib", "predictive bottleneck"), ("recon", "reconstruction")]
ENC = [("N0", "N, block only"), ("N4", "N, 4 px halo"), ("N8", "N, 8 px halo"), ("N16", "N, 16 px halo"), ("U", "U, unconstrained")]

# ----------------------------------------------------------------------------- ceilings
fig, axs = plt.subplots(1, 4, figsize=(13, 3.4), sharey=True)
for ax, (o, ot) in zip(axs, OBJ):
    for i, (e, et) in enumerate(ENC):
        r = C["configs"].get(f"{e}_{o}_c1")
        if r:
            ax.plot(HZ, r["ceiling_G"], color=SERIES[i], lw=2, marker="o", ms=4, label=et)
    for k, ls in (("mass", "--"), ("tent", ":")):
        if k in C["hand"]:
            ax.plot(HZ, C["hand"][k]["G"]["ceiling"], color=INK2, lw=1.2, ls=ls, label=f"hand: block {k}" if k == "mass" else "hand: tent")
    ax.set_xscale("log", base=2)
    ax.set_xticks(HZ, [str(h) for h in HZ])
    ax.set_title(ot, color=INK, fontsize=10)
    ax.set_xlabel("horizon h (ticks)")
axs[0].set_ylabel("closure ceiling c(h), family G")
axs[0].set_ylim(-0.02, 1.02)
from matplotlib.lines import Line2D  # noqa: E402
hd = [Line2D([], [], color=SERIES[i], lw=2, marker="o", ms=4, label=et) for i, (_, et) in enumerate(ENC)]
hd += [Line2D([], [], color=INK2, lw=1.2, ls="--", label="hand: block mass"), Line2D([], [], color=INK2, lw=1.2, ls=":", label="hand: tent")]
fig.legend(handles=hd, loc="lower center", ncol=7, fontsize=8)
fig.suptitle("Learned level 1 (c = 1 per block): closure ceiling vs horizon, mean of 2 seeds x 2 cross-fit halves", color=INK, fontsize=10)
fig.tight_layout(rect=(0, 0.08, 1, 1))
fig.savefig(os.path.join(R, "fig_ceiling_c1.png"), dpi=130)
plt.close(fig)

# ----------------------------------------------------------------------------- agreement heatmap
rows = []
for o, _ in OBJ:
    for e, _ in ENC:
        rows.append(f"{e}_{o}_c1")
for o, _ in OBJ:
    for c in (2, 4):
        rows.append(f"N8_{o}_c{c}")
rows = [r for r in rows if r in C["configs"]]
hand = ["mass", "chan", "view", "tent", "objmass", "objfield"]
M = np.array([[C["configs"][r]["agreement"].get(k, {}).get("R2_H_from_Z", np.nan) for k in hand] for r in rows])
M2 = np.array([[C["configs"][r]["agreement"].get(k, {}).get("R2_Z_from_H", np.nan) for k in hand] for r in rows])
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
cmap = LinearSegmentedColormap.from_list("seqblue", ["#f4f8fd"] + SEQ)
fig, axs = plt.subplots(1, 2, figsize=(10, 0.28 * len(rows) + 1.6))
for ax, A, t in ((axs[0], M, "R^2(hand | learned): the latent contains the hand design"),
                 (axs[1], M2, "R^2(learned | hand): the hand design explains the latent")):
    ax.imshow(np.clip(A, 0, 1), cmap=cmap, vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(hand)), hand, rotation=30)
    ax.set_yticks(range(len(rows)), rows if ax is axs[0] else [""] * len(rows))
    ax.grid(False)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if np.isfinite(A[i, j]):
                ax.text(j, i, f"{A[i, j]:.2f}", ha="center", va="center", fontsize=6.5,
                        color="#ffffff" if A[i, j] > 0.55 else INK)
    ax.set_title(t, fontsize=9, color=INK)
fig.tight_layout()
fig.savefig(os.path.join(R, "fig_agreement.png"), dpi=130)
plt.close(fig)

# ----------------------------------------------------------------------------- windows
wd = os.path.join(R, "windows")
objs = ["clos", "recon", "local"]
hs = [0, 4, 8, 16]
fig, axs = plt.subplots(len(objs), len(hs), figsize=(2.3 * len(hs), 2.3 * len(objs)))
for i, o in enumerate(objs):
    for j, h in enumerate(hs):
        ax = axs[i, j]
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        p = os.path.join(wd, f"L{h}_{o}_c1_s0__fitA.npz")
        if not os.path.exists(p):
            continue
        d = np.load(p)
        Wr = d["W"][0] / d["sd"][:, None, None]
        img = Wr.sum(0)
        s = np.sign(img[h:h + 16, h:h + 16].sum()) or 1.0
        img = s * img
        v = np.abs(img).max()
        ax.imshow(img, cmap="RdBu_r", vmin=-v, vmax=v)
        ax.add_patch(plt.Rectangle((h - 0.5, h - 0.5), 16, 16, fill=False, ec=INK2, lw=0.8, ls="--"))
        key = f"L{h}_{o}_c1_s0__fitA"
        st = C["windows"].get(key, {}).get("per_channel", [{}])[0]
        ax.set_title(f"L{h} {o}: cos blk {st.get('cos_block_mass', np.nan):.2f}", fontsize=8, color=INK)
fig.suptitle("Learned linear windows (c0 + c1, raw units, sign fixed; dashed = the 16-px block)", fontsize=9, color=INK)
fig.tight_layout()
fig.savefig(os.path.join(R, "fig_windows.png"), dpi=130)
plt.close(fig)
print("figures written to", R)
