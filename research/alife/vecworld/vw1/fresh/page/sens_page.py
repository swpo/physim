"""Page figure: three maps of state 0 (matter; deposit sensitivity after 1 tick; clipped 0.5 move after 1 tick),
from inputs/results/sensitivity_maps.npz and states.npz. Same data and colour scales as inputs/media/sensitivity.png,
with larger labels and no dense panels, for a phone-width page."""
import json
import sys
sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/fresh/inputs/scripts")
import common as CM
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import render_l1 as R

S = 0
res = json.load(open(f"{CM.RES}/sensitivity.json"))
mp = np.load(f"{CM.RES}/sensitivity_maps.npz")
st = np.load(f"{CM.RES}/states.npz")
rec = res["per_state"][str(S)]
x = st["x"][S]
Sm = mp[f"s{S}_matter"].reshape(CM.H, CM.W)
dep1 = mp[f"s{S}_dep_N1"].reshape(CM.H, CM.W)
mv1 = mp[f"s{S}_move_eff_N1"].reshape(CM.H, CM.W)
fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.55), dpi=100)
fig.patch.set_facecolor("black")
fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.03, wspace=0.04)
titles = ["level 0: matter", "deposit 1 unit at a cell", "move 0.5 out of a cell"]
fl1 = rec["N1"]["deposit"]["direct_block_mean_floor"]
vmax = rec["N1"]["deposit"]["p99_9"]
vm = rec["N1"]["move_eff_b0.5"]["p99_9"]
imgs = [(R.to_rgb(x), None, None), (dep1, LogNorm(fl1 * 0.5, vmax), "magma"),
        (np.maximum(mv1, vm / 1e6), LogNorm(vm / 1e3, vm), "magma")]
for ax, t, (img, norm, cmap) in zip(axs, titles, imgs):
    R.setup_ax(ax)
    ax.imshow(img, interpolation="nearest", norm=norm, cmap=cmap)
    if norm is not None:
        ax.contour(Sm, levels=[1e-3], colors=["#40e0ff"], linewidths=0.7)
    ax.set_title(t, color="white", fontsize=13, pad=6)
fig.savefig("/home/user/evalwork/vecworld/vw1/fresh/page/sensitivity_page.png", dpi=100, facecolor="black")
print("ok", fl1, vmax, vm)
