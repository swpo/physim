"""Figures for rotdiv.py runs. usage: rotfig.py RUN [RUN ...] (names in out/, e.g. base_s5 r30_s5 ...)"""
import json, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent / "out"
L = 192.0
runs = sys.argv[1:]
J = {r: json.loads((OUT / f"{r}.json").read_text()) for r in runs if (OUT / f"{r}.json").exists()}
S = {r: np.load(OUT / f"{r}_snaps.npz") for r in J}


def rot(p, th):
    c = L / 2
    y, x = p[0] - c, p[1] - c
    t = np.radians(th)
    return ((c + np.sin(t) * x + np.cos(t) * y) % L, (c + np.cos(t) * x - np.sin(t) * y) % L)


# 1. initial field and nucleation pattern under rotation
seeds = sorted({J[r]["seed"] for r in J if J[r]["iso"] == 0})
conds = [c for c in ("base", "r30", "r45") if any(r.startswith(c + "_") for r in J)]
fig, ax = plt.subplots(len(seeds), 2 * len(conds), figsize=(3.0 * 2 * len(conds), 3.1 * len(seeds)), squeeze=False)
for i, sd in enumerate(seeds):
    base = J.get(f"base_s{sd}")
    for j, c in enumerate(conds):
        r = f"{c}_s{sd}"
        if r not in J:
            continue
        th = J[r]["theta"]
        ax[i, j].imshow(S[r]["e_t0"].astype(float), cmap="viridis", origin="lower", extent=(0, L, 0, L))
        ax[i, j].set_title(f"s{sd} {c}: e at t=0", fontsize=9)
        ax[i, len(conds) + j].imshow(S[r]["e_t1000"].astype(float), cmap="magma", origin="lower", extent=(0, L, 0, L), vmin=0, vmax=1)
        ax[i, len(conds) + j].set_title(f"s{sd} {c}: e at t=1000\nx: nucleations; o: base nucleations rotated {th:g} deg", fontsize=7)
        for t, y, x in J[r]["nucleation_sites"]:
            ax[i, len(conds) + j].plot(x, y, "x", color="cyan", ms=6)
        if base:
            for t, y, x in base["nucleation_sites"]:
                yr, xr = rot((y, x), th)
                ax[i, len(conds) + j].plot(xr, yr, "o", mfc="none", mec="white", ms=9)
for a in ax.ravel():
    a.set_xticks([]); a.set_yticks([])
fig.tight_layout(); fig.savefig(OUT / "ic_rotation.png", dpi=90); plt.close(fig)

# 2. division axes over the final state
n = len(J)
cols = 4
rows = int(np.ceil(n / cols))
fig, ax = plt.subplots(rows, cols, figsize=(3.4 * cols, 3.6 * rows), squeeze=False)
for k, r in enumerate(J):
    a = ax.ravel()[k]
    tl = max(int(k[3:]) for k in S[r].files if k.startswith("e_t"))
    a.imshow(S[r][f"e_t{tl}"].astype(float),
             cmap="gray", origin="lower", extent=(0, L, 0, L), vmin=0, vmax=1)
    for d in J[r]["persistent_divisions"]:
        if "daughter_axis_0t" not in d:
            continue
        y, x = d["parent_centroid"]
        t = np.radians(d["daughter_axis_0t"])
        col = plt.cm.autumn(min((d["t"] - 2000) / 4000, 1.0)) if d["t"] < 6000 else "cyan"
        a.plot([x - 14 * np.cos(t), x + 14 * np.cos(t)], [y - 14 * np.sin(t), y + 14 * np.sin(t)], "-", color=col, lw=2.5)
    th = J[r]["theta"]
    for base_ang, sty in ((45, ":"), (135, ":")):
        tt = np.radians(base_ang + th)
        a.plot([96 - 90 * np.cos(tt), 96 + 90 * np.cos(tt)], [96 - 90 * np.sin(tt), 96 + 90 * np.sin(tt)], sty, color="deepskyblue", lw=0.8)
    a.set_title(f"{r}: e at {tl} t; division axes\n(dotted: IC diagonals rotated {th:g} deg)", fontsize=8)
    a.set_xlim(0, L); a.set_ylim(0, L); a.set_xticks([]); a.set_yticks([])
for a in ax.ravel()[n:]:
    a.axis("off")
fig.tight_layout(); fig.savefig(OUT / "division_axes.png", dpi=90); plt.close(fig)

# 3. angle histograms per condition (pooled seeds)
groups = {}
for r in J:
    groups.setdefault(r.rsplit("_s", 1)[0], []).append(r)
fig, ax = plt.subplots(1, len(groups), figsize=(3.3 * len(groups), 2.8), squeeze=False)
for a, (g, rs) in zip(ax[0], groups.items()):
    th = J[rs[0]]["theta"]
    ang = [d["daughter_axis_0t"] for r in rs for d in J[r]["persistent_divisions"] if "daughter_axis_0t" in d]
    pang = [d["parent_long_axis_100t_before"] for r in rs for d in J[r]["persistent_divisions"] if "parent_long_axis_100t_before" in d]
    a.hist([ang, pang], bins=np.arange(0, 181, 7.5), label=["daughter axis at split", "parent long axis 100 t before"], color=["C0", "C1"])
    for x in (45, 135):
        a.axvline(x, color="k", ls="-", lw=0.8)
        if th:
            a.axvline((x + th) % 180, color="C3", ls="--", lw=0.8)
    a.set_title(f"{g} (theta {th:g}, iso {J[rs[0]]['iso']}): n={len(ang)}", fontsize=8)
    a.set_xlim(0, 180); a.set_xlabel("angle from grid x axis (deg)", fontsize=8)
ax[0, 0].legend(fontsize=6)
fig.tight_layout(); fig.savefig(OUT / "angle_hist.png", dpi=90); plt.close(fig)
print("figures written")
