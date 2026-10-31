"""Views for the rods runner (lab env python: matplotlib).

  prep      prepared state (phi, |Q|, s, c, om) with device 0/1 nodes and the shifted (wrong-geometry) nodes
  ends      phi and c at the end of the 50 tu window, member 0 and 1 of every saved arm for one program
  envelope  end state of each passing envelope run
"""
import json, sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
PREP = Path("/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/out")
FIELDS = ("phi", "q1", "q2", "s", "c", "om")


def lattice(kind, n_rings=3):
    R = n_rings - 1
    if kind == "square":
        return np.array([(iy, ix) for iy in range(-R, R + 1) for ix in range(-R, R + 1) if abs(iy) + abs(ix) <= R], float)
    v1, v2 = np.array([0.0, 1.0]), np.array([np.sqrt(3) / 2, 0.5])
    return np.array([a * v1 + b * v2 for a in range(-R, R + 1) for b in range(-R, R + 1)
                     if max(abs(a), abs(b), abs(a + b)) <= R], float)


def rot(t):
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])


def nodes(info, shift=(0, 0)):
    c0 = np.array(info["sites"]["centre"]) + 0.5 + shift
    c1 = np.array(info["sites"]["other"]) + 0.5 + shift
    return [(c0 + 3.0 * lattice("square") @ rot(0.3).T) % 128, (c1 + 6.0 * lattice("hex") @ rot(1.1).T) % 128]


def show(ax, img, title, cmap="viridis", vmin=None, vmax=None):
    ax.imshow(img, origin="upper", cmap=cmap, vmin=vmin, vmax=vmax, extent=(0, 128, 128, 0))
    ax.set_title(title, fontsize=8)
    ax.set_xticks([]); ax.set_yticks([])


def prep():
    z = np.load(PREP / "prep_s0.npz")
    info = json.loads((PREP / "prep_s0.json").read_text())
    fig, axs = plt.subplots(1, 4, figsize=(16, 4.4))
    show(axs[0], z["phi"], "phi (prepared, native t=300)", "RdBu_r", -1, 1)
    show(axs[1], np.hypot(z["q1"], z["q2"]), "|Q|", "magma", 0, 0.6)
    show(axs[2], z["s"], "s", "viridis", 0, 0.6)
    show(axs[3], z["c"], "c", "viridis", 0, 3)
    for ax in axs:
        for (p, col) in zip(nodes(info), ("k", "m")):
            ax.plot(p[:, 1], p[:, 0], "o", ms=2.5, color=col)
        for p in nodes(info, (0, 3)):
            ax.plot(p[:, 1], p[:, 0], "x", ms=2.5, color="orange")
    fig.suptitle("prepared state; device0 black (13-node square, spacing 3), device1 magenta (19-node hex, spacing 6), "
                 "shifted +3 in x orange", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "prep_devices.png", dpi=110)


def ends(program):
    files = sorted(OUT.glob(f"{program}_*.npz"))
    files = [f for f in files if not f.stem.startswith("envelope")]
    info = json.loads((PREP / "prep_s0.json").read_text())
    fig, axs = plt.subplots(len(files), 4, figsize=(12, 3.1 * len(files)))
    axs = np.atleast_2d(axs)
    for r, f in enumerate(files):
        z = np.load(f)
        S = z["snaps"]
        b = z["bodies"]
        for k in range(2):
            show(axs[r, 2 * k], S[k, 0], f"{f.stem} m{k} phi t=50tu ({b[k, 0]}->{b[k, -1]} bodies)", "RdBu_r", -1, 1)
            show(axs[r, 2 * k + 1], S[k, 4], f"{f.stem} m{k} c", "viridis", 0, 3)
            for ax in axs[r, 2 * k:2 * k + 2]:
                p = nodes(info)[0]
                ax.plot(p[:, 1], p[:, 0], "o", ms=1.5, color="k")
    fig.tight_layout()
    fig.savefig(OUT / f"ends_{program}.png", dpi=80)


def envelope():
    files = sorted(OUT.glob("envelope_*.npz"))
    fig, axs = plt.subplots(len(files), 4, figsize=(12, 3.1 * len(files)))
    axs = np.atleast_2d(axs)
    for r, f in enumerate(files):
        F = np.load(f)["F"]
        show(axs[r, 0], F[0], f"{f.stem} phi", "RdBu_r", -1.1, 1.1)
        show(axs[r, 1], np.hypot(F[1], F[2]), "|Q|", "magma", 0, 1)
        show(axs[r, 2], F[3], "s", "viridis", 0, None)
        show(axs[r, 3], F[4], "c", "viridis", 0, None)
    fig.tight_layout()
    fig.savefig(OUT / "envelope_ends.png", dpi=80)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "prep":
        prep()
    elif cmd == "ends":
        ends(sys.argv[2])
    elif cmd == "envelope":
        envelope()
