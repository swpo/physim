"""Particle-level lineage for clan-carrying worlds.

    python lineage.py WORLD TAG NSTEPS [every=100] [smin=15] [seed=0] [key=val ...]

Every `every` steps, matter particles (type > 0) are linked within r_link and grouped into
clusters of >= smin particles. Each particle carries a clan label that new matter inherits
from its catalyst (inside the world). A cluster's parent is the majority clan of its
particles; per parent, the largest cluster continues the individual and the others are
births (generation + 1). Particles are then relabelled with their cluster's individual id,
so labels always point to the most recent individual. Outputs screens/TAG_lineage.png,
screens/TAG_clans.png and scratch/TAG_lineage.json.
"""
import ast
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from labkit.world import load_world  # noqa: E402
from labkit import render as R  # noqa: E402


KINDS = []


def clusters(x, L, r_link, smin):
    tree = cKDTree(x % L, boxsize=L)
    pr = tree.query_pairs(r_link, output_type="ndarray")
    n = len(x)
    g = coo_matrix((np.ones(len(pr)), (pr[:, 0], pr[:, 1])), shape=(n, n))
    nc, lab = connected_components(g, directed=False)
    size = np.bincount(lab, minlength=nc)
    keep = np.flatnonzero(size >= smin)
    return [np.flatnonzero(lab == k) for k in keep]


def run(W, s, nsteps, every, smin, r_link=0.35, log=print):
    L = s["p"]["L"]
    ind = {}      # individual id -> dict(parent, gen, birth, last, sizes)
    next_id = [1]
    s["clan"][:] = 0
    snaps, pops = [], []
    kinds = s.setdefault("_kinds", [])
    t0 = time.time()
    for n in range(0, nsteps + 1):
        if n % every == 0:
            mat = np.flatnonzero(s["t"] > 0)
            cl = clusters(s["x"][mat], L, r_link, smin) if len(mat) else []
            byparent = {}
            for c in cl:
                idx = mat[c]
                lab = s["clan"][idx]
                lab = lab[lab > 0]
                par = int(np.bincount(lab).argmax()) if len(lab) else 0
                byparent.setdefault(par, []).append(idx)
            frame = n // every
            for par, lst in byparent.items():
                lst.sort(key=len, reverse=True)
                for k, idx in enumerate(lst):
                    if par > 0 and par in ind and k == 0:
                        iid = par
                    else:
                        iid = next_id[0]
                        next_id[0] += 1
                        gen = ind[par]["gen"] + 1 if par in ind else 0
                        ind[iid] = {"parent": par if par in ind else 0, "gen": gen, "birth": frame,
                                    "last": frame, "sizes": []}
                    ind[iid]["last"] = frame
                    ind[iid]["sizes"].append(len(idx))
                    if "g" in s:
                        ind[iid].setdefault("kind", []).append(round(float(s["g"][idx].mean()), 2))
                    s["clan"][idx] = iid
            pops.append(len(cl))
            if "g" in s:
                kinds.append([sum(1 for c in cl if s["g"][mat[c]].mean() < 0.5), sum(1 for c in cl if s["g"][mat[c]].mean() >= 0.5)])
            snaps.append((n * W.META["dt"], s["x"].copy(), s["t"].copy(), s["clan"].copy()))
        if n < nsteps:
            s = W.step(s)
    log(f"lineage run {time.time() - t0:.0f}s, individuals {len(ind)}")
    return ind, snaps, pops


def figures(ind, snaps, pops, every, dt, L, tag, title, min_life=5):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    T = len(pops)
    tt = np.arange(T) * every * dt
    life = {i: d["last"] - d["birth"] + 1 for i, d in ind.items()}
    keep = [i for i in ind if life[i] >= min_life]
    keepset = set(keep)
    # order by depth-first traversal so clades sit together
    kids = {}
    for i in keep:
        p = ind[i]["parent"]
        while p and p not in keepset:
            p = ind[p]["parent"]
        kids.setdefault(p, []).append(i)
    order = []

    def dfs(i):
        order.append(i)
        for k in sorted(kids.get(i, []), key=lambda k: ind[k]["birth"]):
            dfs(k)
    for r in sorted(kids.get(0, []), key=lambda k: ind[k]["birth"]):
        dfs(r)
    y = {i: k for k, i in enumerate(order)}
    gmax = max([ind[i]["gen"] for i in keep] + [1])
    cmap = plt.get_cmap("viridis")
    fig, ax = plt.subplots(1, 2, figsize=(13, max(4, min(14, 0.06 * len(order) + 3))),
                           gridspec_kw={"width_ratios": [3, 1]})
    for i in order:
        d = ind[i]
        ax[0].plot([d["birth"] * every * dt, d["last"] * every * dt], [y[i], y[i]], color=cmap(d["gen"] / gmax), lw=1.5)
        p = d["parent"]
        while p and p not in keepset:
            p = ind[p]["parent"]
        if p:
            ax[0].plot([d["birth"] * every * dt] * 2, [y[p], y[i]], color="0.6", lw=0.6)
    ax[0].set_xlabel("time"); ax[0].set_ylabel("individual (depth-first order)")
    ax[0].set_title(f"{title}\nparticle-level lineage: {len(keep)} individuals living >= {min_life} samples, "
                    f"max generation {max([ind[i]['gen'] for i in keep] + [0])} (colour)", fontsize=9)
    ax[1].plot(tt, pops, label="all")
    if KINDS:
        kk = np.array(KINDS)
        ax[1].plot(tt[:len(kk)], kk[:, 0], label="kind 0 cells"); ax[1].plot(tt[:len(kk)], kk[:, 1], label="kind 1 cells")
        ax[1].legend(fontsize=8)
    ax[1].set_title("clusters (>= smin particles)"); ax[1].set_xlabel("time")
    fig.tight_layout(); fig.savefig(f"screens/{tag}_lineage.png", dpi=80); plt.close(fig)
    # clan-coloured particle sheet: colour = root founder of each particle's individual
    root = {}
    for i in ind:
        r = i
        while ind[r]["parent"]:
            r = ind[r]["parent"]
        root[i] = r
    roots = sorted(set(root.values()))
    rk = {r: k for k, r in enumerate(roots)}
    pick = np.unique(np.linspace(0, len(snaps) - 1, 12).round().astype(int))
    ims, labs = [], []
    for k in pick:
        tm, x, t, clan = snaps[k]
        col = np.array([rk.get(root.get(int(c), -1), -1) for c in clan])
        m = t > 0
        ims.append(R.particle_canvas(x[m], (col[m] % 7) + 1, (0, 0, L, L), 240, radius=1.0))
        labs.append(f"t={tm:g}")
    R.contact_sheet(ims, labs, ncols=6, title=f"{tag}: matter coloured by founding clan (food hidden)").save(f"screens/{tag}_clans.png")


def main():
    wp, tag, nsteps = sys.argv[1], sys.argv[2], int(sys.argv[3])
    every, smin, seed, over = 100, 15, 0, {}
    for a in sys.argv[4:]:
        k, v = a.split("=", 1)
        if k == "every":
            every = int(v)
        elif k == "smin":
            smin = int(v)
        elif k == "seed":
            seed = int(v)
        else:
            over[k] = ast.literal_eval(v)
    W = load_world(wp)
    s = W.init(seed, W.META["size"], **over)
    ind, snaps, pops = run(W, s, nsteps, every, smin)
    KINDS[:] = s.get("_kinds", [])
    title = f"{W.META['name']} seed {seed} " + " ".join(a for a in sys.argv[4:] if not a.startswith(("every", "smin", "seed")))
    figures(ind, snaps, pops, every, W.META["dt"], s["p"]["L"], tag, title[:120])
    life = {i: d["last"] - d["birth"] + 1 for i, d in ind.items()}
    good = {i: d for i, d in ind.items() if life[i] >= 5}
    gens = [d["gen"] for d in good.values()]
    births = sum(1 for d in good.values() if d["parent"])
    print(f"{tag}: individuals(life>=5) {len(good)}, births {births}, max gen {max(gens + [0])}, "
          f"final clusters {pops[-1]}, gen hist {np.bincount(gens).tolist() if gens else []}")
    if KINDS:
        print("kind counts (0,1) at 10 times:", [KINDS[i] for i in np.linspace(0, len(KINDS) - 1, 10).astype(int)])
    Path(f"scratch/{tag}_lineage.json").write_text(json.dumps({str(k): v for k, v in ind.items()}))


if __name__ == "__main__":
    main()
