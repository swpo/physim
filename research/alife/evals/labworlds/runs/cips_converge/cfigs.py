"""Figures. usage: figs.py traces REF NULL OUT.png | figs.py det N OUT.png | figs.py cap NAME_A NAME_B OUT.png"""
import json, sys
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
args = sys.argv[1:]; sys.argv = sys.argv[:1]
import cconv as K

PANELS = [("device0", 0, 0, "device0 node0 e"), ("device0", 2, 0, "device0 node0 F"), ("device0", 3, 4, "device0 node4 s"),
          ("device1", 0, 0, "device1 node0 e"), ("global", 0, 1, "global var e"), ("global", 2, 0, "global mean F")]


def traces(ref, null, out):
    fig, ax = plt.subplots(2, len(PANELS), figsize=(2.6 * len(PANELS), 5.2))
    for r, cid in enumerate(K.CASES):
        T = K.load(f"{cid}:{ref}:T")[0]; A = K.load(f"{cid}:{ref}:A")[0]; X = K.load(f"{cid}:{null}")[0]
        for a, (sensor, port, slot, title) in zip(ax[r], PANELS):
            qi = K.SENSORS.index(sensor)
            a.plot(K.TIMES, A[qi][:, :, port, slot].T, color="0.5", lw=0.6)
            a.plot(K.TIMES, X[qi][:, :, port, slot].T, color="tab:red", lw=0.6)
            a.plot(K.TIMES, T[qi][:, :, port, slot].T, color="k", lw=0.9, ls=":")
            a.set_title(f"{cid} {title}", fontsize=7); a.tick_params(labelsize=6)
    ax[0, 0].legend([plt.Line2D([], [], color=c, ls=l) for c, l in (("0.5", "-"), ("tab:red", "-"), ("k", ":"))],
                    [f"native A {ref}", f"null {null}", "truth T"], fontsize=5)
    fig.suptitle(f"8 members each; c001 sham, c002 fuel pulse at device0 (t=5-15 tu); x: public tu", fontsize=8)
    fig.tight_layout(); fig.savefig(out, dpi=80)


def det(N, out):
    tab = json.loads((K.OUT / f"dettable_N{N}.json").read_text())
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    for a, cid in zip(ax, K.CASES):
        for pair, ls in zip([k for k in tab[cid] if k.startswith("dt")], ("-", "--", ":")):
            for g, v in tab[cid][pair]["by_time_device0"].items():
                a.plot(K.TIMES, v, ls=ls, label=f"{pair} {g}", lw=0.9)
        a.set_title(f"{cid}: device0 |offset| / member spread, zero-noise runs", fontsize=8)
        a.set_xlabel("tu", fontsize=7); a.legend(fontsize=5, ncol=2); a.tick_params(labelsize=6)
    fig.tight_layout(); fig.savefig(out, dpi=80)


if __name__ == "__main__" and args[0] in ("traces", "det"):
    {"traces": lambda: traces(args[1], args[2], args[3]), "det": lambda: det(int(args[1]), args[2])}[args[0]]()


def cap(names, out, times=(1000, 2000, 3000, 4000, 5000)):
    """Rows: runs (capab.py names); columns: e at the given times, then the local cut arm and its fed twin at the end."""
    rows = []
    for n in names:
        z = np.load(K.OUT / "cap" / f"{n}_final.npz"); info = json.loads((K.OUT / "cap" / f"{n}.json").read_text())
        rows.append((n, z, info))
    cut_keys = sorted([k for k in rows[0][1].files if k.startswith("cut_t")], key=lambda k: int(k[5:]))
    cols = len(times) + 2
    fig, ax = plt.subplots(len(rows), cols, figsize=(1.9 * cols, 2.0 * len(rows)), squeeze=False)
    for r, (n, z, info) in enumerate(rows):
        for j, t in enumerate(times):
            k = f"t{t}"
            if k in z.files:
                e = z[k][0]; n_b = [c[1] for c in info["counts"] if abs(c[0] - t) < 1e-6]
                ax[r, j].imshow(e, cmap="magma", vmin=0, vmax=1, extent=(0, 192, 192, 0))
                ax[r, j].set_title(f"{n} t={t}" + (f" n={n_b[0]}" if n_b else ""), fontsize=5)
            ax[r, j].axis("off")
        last = cut_keys[-1]; tl = int(last[5:])
        for j, (key, lab) in enumerate(((f"fed_t{tl}", "fed twin"), (last, "local cut"))):
            a = ax[r, len(times) + j]
            if key in z.files:
                a.imshow(z[key], cmap="magma", vmin=0, vmax=1, extent=(0, 192, 192, 0))
                d = z["disk"]; a.contour(np.linspace(0, 192, d.shape[1]), np.linspace(0, 192, d.shape[0]), d.astype(float), [0.5], colors="w", linewidths=0.5)
            a.set_title(f"{lab} t={tl} (cut died {info['cut']['died_at']})", fontsize=5); a.axis("off")
    fig.tight_layout(); fig.savefig(out, dpi=90)


if __name__ == "__main__" and args and args[0] == "cap":
    cap(args[1].split(","), args[2])
