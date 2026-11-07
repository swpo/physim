"""Rendering helpers (run with the labenv python: matplotlib). Matter A (C, H, W) -> RGB.
  python render.py sheet OUT.png FRAMES_DIR i1 i2 ...    contact sheet of search snapshots
"""
import sys
import os
import numpy as np

PAL = {1: [[1.0, 0.85, 0.3]], 2: [[0.15, 0.85, 1.0], [1.0, 0.45, 0.1]],
       3: [[0.2, 0.9, 1.0], [1.0, 0.4, 0.1], [0.9, 0.2, 1.0]]}


def to_rgb(A, scale=0.6):
    """A: (C, H, W). Saturating additive colour mix on black: 1 - exp(-sum_c A_c col_c / scale)."""
    A = np.asarray(A, float) / 127.5 if np.asarray(A).dtype == np.uint8 else np.asarray(A, float)
    C = A.shape[0]
    cols = np.array(PAL.get(C, PAL[3])[:C])
    x = np.tensordot(A, cols, axes=(0, 0)) / scale       # (H, W, 3)
    return 1.0 - np.exp(-x)


def sheet(out, fdir, ids, labels=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = []
    for i in ids:
        d = np.load(os.path.join(fdir, f"{i}.npz"))
        ks = sorted(d.files, key=lambda s: int(s[1:]))
        rows.append([(k, to_rgb(d[k])) for k in ks])
    nc = max(len(r) for r in rows)
    fig, axs = plt.subplots(len(rows), nc, figsize=(1.6 * nc, 1.6 * len(rows)), squeeze=False)
    for r, (i, row) in enumerate(zip(ids, rows)):
        for c in range(nc):
            ax = axs[r, c]
            ax.set_xticks([]); ax.set_yticks([])
            if c < len(row):
                ax.imshow(row[c][1], interpolation="nearest")
                ax.set_title(f"{i} {row[c][0]}" if labels is None else f"{labels[r]} {row[c][0]}", fontsize=5)
    plt.tight_layout(pad=0.2)
    fig.savefig(out, dpi=110, facecolor="black")


if __name__ == "__main__":
    if sys.argv[1] == "sheet":
        sheet(sys.argv[2], sys.argv[3], [int(x) for x in sys.argv[4:]])


def grid(out, fdir, ids, key="t2000", ncol=8, labels=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    nrow = (len(ids) + ncol - 1) // ncol
    fig, axs = plt.subplots(nrow, ncol, figsize=(1.5 * ncol, 1.6 * nrow), squeeze=False)
    for ax in axs.ravel():
        ax.set_axis_off()
    for n, i in enumerate(ids):
        d = np.load(os.path.join(fdir, f"{i}.npz"))
        ax = axs.ravel()[n]
        k = key if key in d.files else sorted(d.files, key=lambda q: int(q[1:]))[-1]
        ax.imshow(to_rgb(d[k]), interpolation="nearest")
        ax.set_title(str(i) if labels is None else labels[n], fontsize=6, color="white")
    plt.tight_layout(pad=0.2)
    fig.savefig(out, dpi=110, facecolor="black")
