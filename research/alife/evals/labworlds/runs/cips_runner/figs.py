"""Figures (lab env): prep | noise | envelope. usage: figs.py WHAT"""
import json, sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).resolve().parent))
from plabel import plabel
OUT = Path(__file__).resolve().parent / "out"
FIELDS = ("e", "p", "F", "s")
info = json.loads((OUT / "prep.json").read_text())
z = np.load(OUT / "prep.npz"); st = {f: z[f] for f in FIELDS}


def nodes(a):
    for k, c in (("device0", "c"), ("device1", "lime")):
        p = np.asarray(info["nodes"][k]); a.scatter(p[:, 1], p[:, 0], s=5, c=c)


what = sys.argv[1]
if what == "prep":
    fig, ax = plt.subplots(1, 4, figsize=(13, 3.5))
    for a, f in zip(ax, FIELDS):
        im = a.imshow(st[f], cmap="magma"); fig.colorbar(im, ax=a, shrink=0.8); nodes(a); a.set_title(f, fontsize=9); a.axis("off")
    fig.suptitle(f"prepared state N={info['N']} seed {info['seed']} t={info['t_prep']} ({info['bodies']} bodies); device0 cyan, device1 green", fontsize=9)
    fig.tight_layout(); fig.savefig(OUT / "prep.png", dpi=80)
elif what == "noise":
    res = json.loads((OUT / "noise.json").read_text())
    keys = [k for k in res if "/seed" in k]
    fig, ax = plt.subplots(2, len(keys) + 1, figsize=(2.9 * (len(keys) + 1), 6))
    ax[0, 0].imshow(st["e"], cmap="magma", vmin=0, vmax=1); ax[0, 0].set_title(f"e at prep ({info['bodies']} bodies)", fontsize=8)
    ax[1, 0].imshow(st["s"], cmap="viridis", vmin=0, vmax=45); ax[1, 0].set_title("s at prep", fontsize=8)
    for j, k in enumerate(keys, 1):
        lvl, seed = k.split("/")
        F = np.load(OUT / f"noise_{lvl}_{seed}_final.npy")
        ax[0, j].imshow(F[0], cmap="magma", vmin=0, vmax=1); ax[0, j].set_title(f"e 50 tu, noise {lvl} {seed}: {res[k]['final_bodies']}", fontsize=8)
        ax[1, j].imshow(F[3], cmap="viridis", vmin=0, vmax=45); ax[1, j].set_title(f"s 50 tu, noise {lvl} {seed}", fontsize=8)
    for a in ax.ravel(): a.axis("off")
    fig.tight_layout(); fig.savefig(OUT / "noise.png", dpi=70)
elif what == "envelope":
    rows = [r for r in json.loads((OUT / "envelope.json").read_text()) if r["port"] != "none"]
    fig, ax = plt.subplots(len(FIELDS), len(rows) // len(FIELDS), figsize=(3.0 * (len(rows) // len(FIELDS)), 3.0 * len(FIELDS)), squeeze=False)
    for r in rows:
        i = FIELDS.index(r["port"]); j = [q["gain"] for q in rows if q["port"] == r["port"]].index(r["gain"])
        a = ax[i, j]; a.axis("off")
        p = OUT / f"envelope_{r['port']}_g{r['gain']:g}.npy"
        if r["finite"] and p.exists():
            F = np.load(p); pi = FIELDS.index(r["port"])
            im = a.imshow(F[pi], cmap="magma"); fig.colorbar(im, ax=a, shrink=0.7)
            a.contour(F[0], levels=[0.5], colors="c", linewidths=0.5)
        a.set_title(f"{r['port']} gain {r['gain']:g}: finite {r['finite']}, bodies {r.get('final_bodies')}", fontsize=7)
    fig.suptitle("envelope: amp 3 for 50 tu at device0, injected field after 50 tu (cyan: e=0.5 contour)", fontsize=8)
    fig.tight_layout(); fig.savefig(OUT / "envelope.png", dpi=70)
