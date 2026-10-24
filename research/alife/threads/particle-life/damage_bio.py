"""Damage biography at particle resolution.

    python damage_bio.py WORLD TAG T_DAMAGE [frac=0.5] [seed=0] [key=val ...]

Runs to T_DAMAGE steps, picks the two largest cells, cuts away the matter of one of them on one
side of a line through its centre so that `frac` of its particles become food, leaves the other
untouched as a control, and draws zoomed particle views of both every 100 steps for 30 samples.
Membrane fraction of each cell over time is drawn underneath.
"""
import ast
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from labkit.world import load_world  # noqa: E402
from labkit import render as R  # noqa: E402
from lineage import clusters  # noqa: E402


def main():
    wp, tag, tdam = sys.argv[1], sys.argv[2], int(sys.argv[3])
    frac, seed, over = 0.5, 0, {}
    for a in sys.argv[4:]:
        k, v = a.split("=", 1)
        if k == "frac":
            frac = float(v)
        elif k == "seed":
            seed = int(v)
        else:
            over[k] = ast.literal_eval(v)
    W = load_world(wp)
    s = W.init(seed, W.META["size"], **over)
    L = s["p"]["L"]
    for _ in range(tdam):
        s = W.step(s)
    mat = np.flatnonzero(s["t"] > 0)
    cl = sorted(clusters(s["x"][mat], L, 0.35, 15), key=len, reverse=True)
    cells = [mat[c] for c in cl[:2]]
    centres = []
    for c in cells:
        ang = s["x"][c] / L * 2 * np.pi
        centres.append((np.arctan2(np.sin(ang).mean(0), np.cos(ang).mean(0)) / (2 * np.pi) * L) % L)
    # cut: erase particles of cell 0 with projection on a random direction above the frac quantile
    c0, cen = cells[0], centres[0]
    d = (s["x"][c0] - cen + L / 2) % L - L / 2
    proj = d @ np.array([1.0, 0.3]) / np.hypot(1, 0.3)
    hit = c0[proj > np.quantile(proj, 1 - frac)]
    s["t"][hit] = 0
    s["v"][hit] = 0
    if "clan" in s:
        s["clan"][hit] = 0
    n_before = [len(c) for c in cells]
    ims, labs, memb = [], [], [[], []]
    half = 1.6
    for k in range(30):
        for j, cen in enumerate(centres):
            # follow the cell: recentre on matter near the previous centre
            m = np.flatnonzero(s["t"] > 0)
            dd = (s["x"][m] - cen + L / 2) % L - L / 2
            near = m[np.hypot(dd[:, 0], dd[:, 1]) < 1.2]
            if len(near):
                cen = (cen + np.mean(dd[np.hypot(dd[:, 0], dd[:, 1]) < 1.2], 0)) % L
                centres[j] = cen
                memb[j].append(float((s["t"][near] == 2).mean()))
            else:
                memb[j].append(np.nan)
            if k % 3 == 0:
                rel = (s["x"] - cen + L / 2) % L - L / 2
                sel = (np.abs(rel) < half).all(1)
                ims.append(R.particle_canvas(rel[sel] + half, s["t"][sel], (0, 0, 2 * half, 2 * half), 150, radius=2.0))
                labs.append(f"{'cut' if j == 0 else 'ctrl'} +{k * 100 * W.META['dt']:g}")
        for _ in range(100):
            s = W.step(s)
    order = [i for k in range(10) for i in (2 * k,)] + [i for k in range(10) for i in (2 * k + 1,)]
    R.contact_sheet([ims[i] for i in order], [labs[i] for i in order], ncols=10,
                    title=f"{tag}: top row cut cell ({len(hit)}/{n_before[0]} particles -> food at t={tdam * W.META['dt']:g}), "
                          f"bottom row undamaged control ({n_before[1]}); white food, cyan C, orange M").save(f"screens/{tag}.png")
    print(tag, "membrane fraction cut:", np.round(memb[0][::3], 2).tolist())
    print(tag, "membrane fraction ctrl:", np.round(memb[1][::3], 2).tolist())


if __name__ == "__main__":
    main()
