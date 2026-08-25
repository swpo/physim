"""make_strips.py — seam portraits + traveler-at-seam strips (lu units)."""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

B = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(B, "strips")
SEAMS = (24.0, 72.0)   # lu; grid px = lu*2


def _seams_px(ax, vert=True):
    for s in SEAMS:
        (ax.axvline if vert else ax.axhline)(s * 2, color="cyan", lw=0.8, ls="--")


def p2_strip():
    rows = [("4_out", "w=4 out"), ("12_out", "w=12 out"), ("24_out", "w=24 out"),
            ("4_in", "w=4 in (A-side)")]
    rows = [(k, lab) for k, lab in rows
            if os.path.exists(os.path.join(B, "data", f"p2_w{k}.npz"))]
    n = len(rows)
    fig, axes = plt.subplots(n, 2, figsize=(13, 3.3 * n), squeeze=False,
                             gridspec_kw=dict(width_ratios=[1.6, 1]))
    for r, (k, lab) in enumerate(rows):
        d = np.load(os.path.join(B, "data", f"p2_w{k}.npz"))
        ky, t = d["kymo"], d["t"]
        ax = axes[r, 0]
        ax.imshow(ky, aspect="auto", origin="lower", cmap="magma",
                  extent=[0, 96, t[0], t[-1]])
        for s in SEAMS:
            ax.axvline(s, color="cyan", lw=0.8, ls="--")
        ax.set_ylabel(f"{lab}\nt (tu)")
        if r == 0:
            ax.set_title("u kymo, row y=48 lu (M0 | M4 tau5.8 | M0), seams cyan")
        if r == n - 1:
            ax.set_xlabel("x (lu)")
        ax2 = axes[r, 1]
        pos, nc = d["pos"], d["ncomp"]
        for b in range(pos.shape[1]):
            m = ~np.isnan(pos[:, b, 1])
            ax2.plot(pos[m, b, 1] % 96, t[m], ".", ms=1.5)
        for s in SEAMS:
            ax2.axvline(s, color="c", lw=0.8, ls="--")
        ax2.set_xlim(0, 96)
        ax2.set_title(f"tracks x(t); ncomp end {nc[-1]}")
        if r == n - 1:
            ax2.set_xlabel("x (lu)")
    fig.tight_layout()
    fig.savefig(os.path.join(S, "p2_traveler_at_seam.png"), dpi=110)
    plt.close(fig)
    print("p2 strip done")


def p2_frames(key="4_out"):
    d = np.load(os.path.join(B, "data", f"p2_w{key}.npz"))
    sn, st = d["snaps"], d["snap_t"]
    n = len(st)
    fig, axes = plt.subplots(1, n, figsize=(3.0 * n, 3.4))
    for i in range(n):
        ax = axes[i]
        ax.imshow(sn[i], origin="lower", cmap="magma", extent=[0, 96, 0, 96])
        for s in SEAMS:
            ax.axvline(s, color="cyan", lw=0.7, ls="--")
        ax.set_title(f"t={st[i]:g}")
        ax.set_xticks([0, 24, 48, 72, 96]); ax.set_yticks([])
    fig.suptitle(f"P2 {key}: u frames (seams cyan; M4 band = x in [24,72))")
    fig.tight_layout()
    fig.savefig(os.path.join(S, f"p2_frames_w{key}.png"), dpi=110)
    plt.close(fig)
    print("p2 frames done", key)


def p3_strip():
    fig, axes = plt.subplots(2, 2, figsize=(12, 7))
    for col, w in enumerate((8, 24)):
        f = os.path.join(B, "data", f"p3settle_w{w}.npz")
        if not os.path.exists(f):
            continue
        d = np.load(f)
        x_lu = d["x_px"] * 0.5
        ax = axes[0, col]
        ax.plot(x_lu, d["prof_u0"], "k--", lw=1, label="naive rho-blend u0")
        ax.plot(x_lu, d["prof_u"], "r-", lw=1, label="settled u (t=1000)")
        ax.set_title(f"P3 settle w={w/2:g} lu: background")
        ax.legend(fontsize=7)
        ax2 = axes[1, col]
        ax2.plot(x_lu, d["prof_u"] - d["prof_u0"], "b-", lw=1)
        ax2.set_title("settled - naive (u)")
        ax2.set_xlabel("x (lu)")
    # drift tracks overlay
    fig.tight_layout()
    fig.savefig(os.path.join(S, "p3_settle_profiles.png"), dpi=110)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    import glob
    for f in sorted(glob.glob(os.path.join(B, "data", "p3drift_*.npz"))):
        d = np.load(f)
        pos, t = d["pos"], d["t"]
        m = ~np.isnan(pos[:, 0, 1])
        lab = os.path.basename(f)[8:-4]
        ax.plot(t[m], pos[m, 0, 1] % 96, lw=1.2, label=lab)
    ax.axhline(24, color="c", ls="--", lw=0.8)
    ax.set_xlabel("t (tu)"); ax.set_ylabel("x (lu)")
    ax.set_title("P3 blob near vacuum-mismatch seam (seam-1 dashed)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(S, "p3_drift.png"), dpi=110)
    plt.close(fig)
    print("p3 strips done")


def p4_strip():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    ax = axes[0]
    cols = dict(ctrl="k", near="r", close="b", ctrlcl="gray")
    for mode, c in cols.items():
        f = os.path.join(B, "data", f"p4_{mode}.npz")
        if not os.path.exists(f):
            continue
        d = np.load(f)
        wr = np.abs(d["w_row"])
        ax.semilogy(np.arange(len(wr)) * 0.5, wr, c, lw=1, label=mode)
    ax.axvline(24, color="c", ls="--", lw=0.8)
    ax.set_title("|w| along y=48, t=1000")
    ax.set_xlabel("x (lu)"); ax.legend(fontsize=8)
    ax.set_ylim(1e-9, 1)
    for i, (mode, ctrl) in enumerate((("near", "ctrl"), ("close", "ctrlcl"))):
        f = os.path.join(B, "data", f"p4_{mode}.npz")
        ax = axes[1 + i]
        if os.path.exists(f):
            d = np.load(f)
            pos, t = d["pos"], d["t"]
            for b in range(pos.shape[1]):
                m = ~np.isnan(pos[:, b, 1])
                ax.plot(t[m], pos[m, b, 1] % 96, lw=1)
            fc = os.path.join(B, "data", f"p4_{ctrl}.npz")
            if os.path.exists(fc):
                dc = np.load(fc)
                pc = dc["pos"]
                for b in range(pc.shape[1]):
                    m = ~np.isnan(pc[:, b, 1])
                    ax.plot(dc["t"][m], pc[m, b, 1] % 96, "k--", lw=0.8)
        ax.axhline(24, color="c", ls="--", lw=0.8)
        ax.set_title(f"P4 {mode}: x(t) lu (ctrl dashed)")
        ax.set_xlabel("t (tu)")
    fig.tight_layout()
    fig.savefig(os.path.join(S, "p4_halo.png"), dpi=110)
    plt.close(fig)
    print("p4 strip done")


def p5_strip():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    cols = dict(ctrl="k", cross="r", crossn="b")
    ax = axes[0]
    for mode, c in cols.items():
        f = os.path.join(B, "data", f"p5_{mode}.npz")
        if not os.path.exists(f):
            continue
        d = np.load(f)
        ax.plot(d["t"], d["sep"], c, lw=1, label=mode)
    ax.axhline(15.40, color="g", ls=":", lw=1, label="d* ref 15.40")
    ax.set_xlabel("t (tu)"); ax.set_ylabel("sep (lu)"); ax.legend(fontsize=8)
    ax.set_title("P5 bond sep(t): pair straddling seam-1")
    ax = axes[1]
    f = os.path.join(B, "data", "p5_cross.npz")
    if os.path.exists(f):
        d = np.load(f)
        ax.imshow(d["fields"][0], origin="lower", cmap="magma",
                  extent=[0, 96, 0, 96])
        ax.axvline(24, color="c", ls="--", lw=0.8)
        ax.set_title("cross: final u (seam cyan)")
        ax.set_xlabel("x (lu)")
    fig.tight_layout()
    fig.savefig(os.path.join(S, "p5_bond.png"), dpi=110)
    plt.close(fig)
    print("p5 strip done")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    fns = dict(p2=p2_strip, p2f=p2_frames, p3=p3_strip, p4=p4_strip, p5=p5_strip)
    if which == "all":
        for f in fns.values():
            try:
                f()
            except Exception as e:
                print("skip:", type(e).__name__, e)
    else:
        fns[which]()
