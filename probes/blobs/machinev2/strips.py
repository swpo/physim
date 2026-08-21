"""strips.py — layout + film-frame renderers for machine-v2 (matplotlib)."""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))

def lane_layout(ax, L, x1, fork_x0, lane_y=48.0, dy_max=18.0, branch=-1, x0_eta=8.0):
    ax.axhline(lane_y, color="steelblue", lw=2, alpha=0.6, label="carrier lane (M rail)")
    xs = np.linspace(0, L, 200)
    yb = lane_y + np.clip(2.0*(xs-fork_x0), -dy_max, dy_max)*(xs>fork_x0)*branch
    ax.plot(xs, np.where(xs>fork_x0, yb, np.nan), color="darkorange", lw=2, alpha=0.7,
            label="cargo fork branch")
    ax.axvspan(x0_eta, x1, color="green", alpha=0.08, label="eta zone (tow ON)")
    ax.axvline(x1, color="green", ls="--", lw=1)

def track_film(track_npz, out_png, L, x1, fork_x0, title="", lane_y=48.0,
               branch=-1, dy_max=18.0, n_frames=8):
    d = np.load(track_npz)
    t = d["t"]; p1 = d["pos1"]; p2 = d["pos2"]
    idx = np.linspace(0, len(t)-1, n_frames).astype(int)
    fig, axes = plt.subplots(n_frames, 1, figsize=(10, 1.6*n_frames), sharex=True)
    for k, i in enumerate(idx):
        ax = axes[k]
        lane_layout(ax, L, x1, fork_x0, lane_y, dy_max, branch)
        if p1.shape[1]:
            ax.plot(p1[i,:,1] % L, p1[i,:,0] % L, "s", color="crimson", ms=8, label="carrier M")
        if p2.shape[1]:
            ax.plot(p2[i,:,1] % L, p2[i,:,0] % L, "o", color="black", ms=7, mfc="gold", label="cargo S")
        ax.set_ylim(lane_y-30, lane_y+30); ax.set_xlim(0, L)
        ax.set_ylabel(f"t={t[i]:.0f}")
        if k == 0:
            ax.legend(loc="upper right", fontsize=7, ncol=4)
            ax.set_title(title, fontsize=10)
    axes[-1].set_xlabel("x (px)")
    fig.tight_layout(); fig.savefig(out_png, dpi=110); plt.close(fig)
    return out_png
