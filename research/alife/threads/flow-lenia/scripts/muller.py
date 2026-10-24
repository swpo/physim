"""Genotype mass over time (stacked, Muller-style ordering by ancestry) from evo_stats JSON with gids.

python threads/flow-lenia/scripts/muller.py evo/mut.json evo/mut_muller.png
"""
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

d = json.load(open(sys.argv[1]))
for seed, r in d["runs"].items():
    par = r["parents"]; born = r["born"]
    G = len(par)
    t = np.array(r["t"]) * 0.2
    M = np.zeros((G, len(t)))
    for k, gm in enumerate(r["gid_mass"]):
        for g, m in gm.items():
            M[int(g), k] = m
    # depth-first order so that clades are contiguous
    kids = {g: [] for g in range(G)}
    for g in range(1, G):
        kids[par[g]].append(g)
    order, stack = [], [0]
    while stack:
        g = stack.pop()
        order.append(g)
        stack.extend(sorted(kids[g], reverse=True))
    depth = np.zeros(G, int)
    for g in range(1, G):
        depth[g] = depth[par[g]] + 1
    alive_max = M.max(1)
    cmap = plt.get_cmap("tab20")
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.5), gridspec_kw={"width_ratios": [2, 1]})
    ax[0].stackplot(t, M[order], colors=[cmap(g % 20) for g in order], lw=0)
    ax[0].set_xlabel("time"); ax[0].set_ylabel("matter")
    ax[0].set_title(f"seed {seed}: matter per genotype ({G - 1} mutations; colour = genotype id)")
    # phylogeny: x = birth time, y = order, line until last time with mass > 1
    ypos = {g: i for i, g in enumerate(order)}
    for g in range(G):
        alive = np.nonzero(M[g] > 1)[0]
        end = t[alive[-1]] if len(alive) else born[g] * 0.2
        x0 = born[g] * 0.2
        ax[1].plot([x0, end], [ypos[g]] * 2, color=cmap(g % 20), lw=1 + 3 * alive_max[g] / max(alive_max.max(), 1))
        if g:
            ax[1].plot([x0, x0], [ypos[par[g]], ypos[g]], color="0.6", lw=0.6)
    ax[1].set_xlabel("time"); ax[1].set_ylabel("genotype (depth-first)")
    ax[1].set_title(f"phylogeny (max depth {depth.max()}); width ~ peak matter")
    fig.tight_layout(); fig.savefig(sys.argv[2], dpi=80)
    final = M[:, -1]
    top = np.argsort(-final)[:5]
    print(seed, "genotypes", G, "max depth", depth.max(), "final top", [(int(g), int(depth[g]), round(final[g])) for g in top])
