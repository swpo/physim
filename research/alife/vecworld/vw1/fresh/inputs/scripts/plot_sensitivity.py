"""media/sensitivity.png from results/sensitivity.json and sensitivity_maps.npz (matter, autodiff
input-sensitivity maps, concentration curves, autodiff vs finite differences by horizon)."""
import json
import sys

import common as CM
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LogNorm  # noqa: E402

import render_l1 as R  # noqa: E402  (VW-0 drawing helpers: to_rgb, setup_ax)

S = int(sys.argv[1]) if len(sys.argv) > 1 else 0
res = json.load(open(f"{CM.RES}/sensitivity.json"))
mp = np.load(f"{CM.RES}/sensitivity_maps.npz")
st = np.load(f"{CM.RES}/states.npz")
rec = res["per_state"][str(S)]
x = st["x"][S]
Sm = mp[f"s{S}_matter"].reshape(CM.H, CM.W)
plt.rcParams.update({"font.size": 9, "axes.edgecolor": "0.5", "axes.labelcolor": "0.9", "xtick.color": "0.8",
                     "ytick.color": "0.8", "text.color": "0.9"})
fig = plt.figure(figsize=(9.6, 6.6), dpi=100)
fig.patch.set_facecolor("black")
gs = fig.add_gridspec(2, 3, left=0.015, right=0.985, top=0.93, bottom=0.08, wspace=0.24, hspace=0.2)


def mapax(ax, img, title, norm=None, cmap=None, contour=True, cbar_label=None):
    R.setup_ax(ax)
    im = ax.imshow(img, interpolation="nearest", norm=norm, cmap=cmap)
    if contour:
        ax.contour(Sm, levels=[1e-3], colors=["#40e0ff"], linewidths=0.6)
    ax.set_title(title, color="white", fontsize=9)
    if cbar_label and norm is not None:
        ax.text(2, 125, f"log colour {norm.vmin:.2g} to {norm.vmax:.2g} {cbar_label}", color="0.9", fontsize=7,
                va="bottom", bbox=dict(facecolor="black", alpha=0.65, lw=0))
    return im


ax = fig.add_subplot(gs[0, 0])
mapax(ax, R.to_rgb(x), "level 0: matter (two channels)", contour=False)
dep1 = mp[f"s{S}_dep_N1"].reshape(CM.H, CM.W)
dep4 = mp[f"s{S}_dep_N4"].reshape(CM.H, CM.W)
mv1 = mp[f"s{S}_move_eff_N1"].reshape(CM.H, CM.W)


def top(ax, cells, col="white"):
    cells = np.asarray(cells)
    ax.scatter(cells % CM.W, cells // CM.W, s=36, facecolors="none", edgecolors="#7CFC00", lw=1.0)


fl1 = rec["N1"]["deposit"]["direct_block_mean_floor"]
vmax = rec["N1"]["deposit"]["p99_9"]
ax = fig.add_subplot(gs[0, 1])
mapax(ax, dep1, "deposit at one cell: 1 tick later", LogNorm(fl1 * 0.5, vmax), "magma", cbar_label="SD per unit")
top(ax, rec["N1"]["deposit"]["top10_cells"])
ax = fig.add_subplot(gs[0, 2])
vm = rec["N1"]["move_eff_b0.5"]["p99_9"]
mapax(ax, np.maximum(mv1, vm / 1e6), "move 0.5 out of the cell (clipped): 1 tick",
      LogNorm(vm / 1e3, vm), "magma", cbar_label="SD")
ax = fig.add_subplot(gs[1, 0])
fl4 = rec["N4"]["deposit"]["direct_block_mean_floor"]
v4 = rec["N4"]["deposit"]["p99_9"]
mapax(ax, dep4, "deposit at one cell: 4 ticks later", LogNorm(max(fl4 * 0.5, v4 / 1e7), v4), "magma",
      cbar_label="SD per unit")
top(ax, rec["N4"]["deposit"]["top10_cells"])
# concentration curves
ax = fig.add_subplot(gs[1, 1])
ax.set_facecolor("black")
cols = {1: "#ffd27f", 2: "#ff9f40", 4: "#e0503a"}
for N in (1, 2, 4):
    v = mp[f"s{S}_dep_N{N}"].astype(float)
    c = np.cumsum(np.sort(v)[::-1]) / v.sum()
    ax.plot(np.arange(1, v.size + 1) / v.size, c, color=cols[N], lw=1.5, label=f"deposit, {N} tick" + ("s" if N > 1 else ""))
v = mp[f"s{S}_move_eff_N1"].astype(float)
c = np.cumsum(np.sort(v)[::-1]) / v.sum()
ax.plot(np.arange(1, v.size + 1) / v.size, c, color="#7fd0ff", lw=1.5, label="move 0.5, 1 tick")
ff = rec["footprint_frac_A_sum_gt_1e-3"]
ax.axvline(ff, color="#40e0ff", lw=0.9, ls="--")
ax.text(ff * 1.08, 0.08, f"matter footprint\n{100 * ff:.0f}% of cells", color="#40e0ff", fontsize=7.5)
ax.axhline(0.9, color="0.5", lw=0.7, ls=":")
ax.set_xscale("log")
ax.set_xlim(1e-4, 1)
ax.set_ylim(0, 1.02)
ax.set_xlabel("fraction of cells (most sensitive first)")
ax.set_ylabel("share of summed sensitivity", fontsize=8)
ax.legend(fontsize=7, loc="upper left", frameon=True, facecolor="black", edgecolor="none", framealpha=1.0)
ax.set_title("where the sensitivity sits", color="white", fontsize=9)
# AD vs FD
ax = fig.add_subplot(gs[1, 2])
ax.set_facecolor("black")
H = res["validation_horizons"]
mk = {1e-3: "o", 1e-5: "s", 1e-7: "^"}
for kind, col in (("deposit", "#ff9f40"), ("move", "#7fd0ff")):
    for eps in res["eps"]:
        y = [np.median([res["per_state"][k]["validation"][f"N{N}_{kind}_eps{eps:g}"]["rel_err_median"]
                        for k in res["per_state"]]) for N in H]
        ax.plot(H, np.maximum(y, 1e-12), color=col, marker=mk[eps], ms=4, lw=1.0,
                label=f"{kind}, eps={eps:g}")
ax.axhline(0.1, color="0.5", lw=0.7, ls=":")
ax.set_xscale("log", base=2)
ax.set_yscale("log")
ax.set_xticks(H)
ax.set_xticklabels(H)
ax.set_xlabel("horizon (ticks)")
ax.set_ylabel("median |FD - AD| / |AD|", fontsize=8)
ax.set_title("pathwise derivative vs finite difference", color="white", fontsize=9)
ax.legend(fontsize=6.3, frameon=False, loc="lower right", ncol=1)
for a in fig.axes:
    for sp in a.spines.values():
        sp.set_color("0.4")
fig.suptitle("VW-1 A_gliders: autodiff input sensitivity of the coarse level (192 outputs in SD units; cyan: matter > 1e-3; "
             "green circles: 10 most sensitive cells)", color="white", fontsize=9)
fig.savefig(f"{CM.MEDIA}/sensitivity.png", dpi=100, facecolor="black")
print("saved")
