"""Merge-aware particle lineage (committee r1/r2 criteria).

    python lineage2.py WORLD TAG NSTEPS [every=100] [smin=15] [seed=0] [key=val ...]

Every `every` steps, matter (type > 0) is linked within 0.35 into clusters of >= smin particles.
- Continuation by particle overlap: a cluster continues the individual that owned the majority of
  its particles that were clustered at the previous sample. If two individuals flow into one
  cluster, the larger continues and the smaller ends with reason "merge".
- A cluster none of whose particles were clustered at the previous sample is NEW. Its parent is the
  majority clan label of its particles (clan labels are inherited through catalysis from the spore,
  and every clustered particle is relabelled with its individual's id each sample).
- A cluster built from particles of an individual that continues elsewhere is a FRAGMENT (not a birth).
- A QUALIFYING birth is a NEW cluster with a known parent that lives >= min_life samples and does
  not end by merging. Generation = parent's generation + 1 along qualifying births only.
Outputs scratch/TAG_lin2.json and screens/TAG_lin2.png (population, births/deaths, lineage tree).
"""
import ast
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from labkit.world import load_world  # noqa: E402
from lineage import clusters  # noqa: E402


def run(W, s, nsteps, every, smin, log=print):
    L = s["p"]["L"]
    N = len(s["t"])
    s["clan"][:] = 0
    owner_prev = np.zeros(N, np.int64)  # individual id owning each particle at the previous sample (0 = none)
    ind, nid = {}, [1]
    snaps, pops, t0 = [], [], time.time()
    for n in range(nsteps + 1):
        if n % every == 0:
            f = n // every
            mat = np.flatnonzero(s["t"] > 0)
            cl = [mat[c] for c in clusters(s["x"][mat], L, 0.35, smin)] if len(mat) else []
            owner = np.zeros(N, np.int64)
            claims = {}
            info = []
            for k, idx in enumerate(cl):
                prev = owner_prev[idx]
                prev = prev[prev > 0]
                if len(prev):
                    o = int(np.bincount(prev).argmax())
                    claims.setdefault(o, []).append((len(idx), k))
                    info.append(("old", o))
                else:
                    lab = s["clan"][idx]
                    lab = lab[lab > 0]
                    par = int(np.bincount(lab).argmax()) if len(lab) else 0
                    info.append(("new", par))
            ids = [None] * len(cl)
            for o, lst in claims.items():
                lst.sort(reverse=True)
                ids[lst[0][1]] = o
                for _, k in lst[1:]:
                    i = nid[0]; nid[0] += 1
                    ind[i] = {"parent": o, "kind": "fragment", "birth": f, "last": f, "end": None, "sizes": [], "gen": None}
                    ids[k] = i
            for k, (typ, par) in enumerate(info):
                if typ == "new":
                    i = nid[0]; nid[0] += 1
                    ind[i] = {"parent": par if par in ind else 0, "kind": "new", "birth": f, "last": f, "end": None,
                              "sizes": [], "gen": None}
                    ids[k] = i
            alive = set()
            for k, idx in enumerate(cl):
                i = ids[k]
                ind[i]["last"] = f
                ind[i]["sizes"].append(len(idx))
                if "g" in s:
                    ind[i].setdefault("gene", []).append(round(float(s["g"][idx].mean()), 2))
                owner[idx] = i
                s["clan"][idx] = i
                alive.add(i)
            # individuals present before but not now: merged (their particles now owned by another) or died
            for i in set(owner_prev[owner_prev > 0].tolist()) - alive:
                if ind[i]["end"] is None:
                    mine = np.flatnonzero(owner_prev == i)
                    now = owner[mine]
                    ind[i]["end"] = ("merge", f) if (now > 0).mean() > 0.5 else ("death", f)
            owner_prev = owner
            pops.append(len(cl))
            snaps.append((n * W.META["dt"], s["x"].copy(), s["t"].copy(), owner.copy()))
        if n < nsteps:
            s = W.step(s)
    log(f"lineage2 run {time.time() - t0:.0f}s")
    return ind, snaps, pops


def qualify(ind, min_life=20):
    q = {}
    for i in sorted(ind):
        d = ind[i]
        life = d["last"] - d["birth"] + 1
        merged = d["end"] is not None and d["end"][0] == "merge"
        d["qualifies"] = bool(d["kind"] == "new" and d["parent"] in ind and life >= min_life and not merged)
    for i in sorted(ind):  # ids increase with time, so parents are processed first
        d = ind[i]
        if d["kind"] == "new" and d["parent"] == 0:
            d["gen"] = 0
        elif d["qualifies"]:
            pg = ind[d["parent"]]["gen"]
            d["gen"] = (pg + 1) if pg is not None else None
        elif d["kind"] == "fragment" and d["parent"] in ind:
            d["gen"] = ind[d["parent"]]["gen"]
    return ind


def summary(ind, pops, every, dt, T):
    tt = len(pops) * every * dt
    q = [i for i, d in ind.items() if d["qualifies"]]
    deaths = sum(1 for d in ind.values() if d["end"] and d["end"][0] == "death")
    merges = sum(1 for d in ind.values() if d["end"] and d["end"][0] == "merge")
    frags = sum(1 for d in ind.values() if d["kind"] == "fragment")
    gens = [d["gen"] for d in ind.values() if d["gen"] is not None]
    return {"qualifying_births": len(q), "births_per_100t": 100 * len(q) / tt, "deaths": deaths,
            "deaths_per_100t": 100 * deaths / tt, "merges": merges, "fragments": frags,
            "max_gen": max(gens + [0]), "gen_hist": np.bincount(gens).tolist() if gens else [],
            "cells_final": pops[-1], "cells_t200": pops[min(len(pops) - 1, int(round(200 / (every * dt))))]}


def figure(ind, pops, every, dt, tag, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    tt = np.arange(len(pops)) * every * dt
    fig, ax = plt.subplots(1, 2, figsize=(13, 5), gridspec_kw={"width_ratios": [2, 1]})
    show = [i for i, d in ind.items() if d["gen"] is not None and (d["last"] - d["birth"]) >= 5]
    show.sort(key=lambda i: (ind[i]["birth"], i))
    y = {i: k for k, i in enumerate(show)}
    cmap = plt.get_cmap("viridis")
    gmax = max([ind[i]["gen"] for i in show] + [1])
    for i in show:
        d = ind[i]
        col = cmap(d["gen"] / gmax)
        ls = "-" if d["kind"] == "new" else ":"
        ax[0].plot([d["birth"] * every * dt, d["last"] * every * dt], [y[i], y[i]], ls, color=col, lw=1.6)
        if d["parent"] in y:
            ax[0].plot([d["birth"] * every * dt] * 2, [y[d["parent"]], y[i]], color="0.7", lw=0.5)
        if d["end"]:
            ax[0].plot(d["last"] * every * dt, y[i], "x" if d["end"][0] == "death" else ">", color="k", ms=3)
    ax[0].set_title(f"{title}\nmerge-aware lineage: solid = qualifying birth/founder, dotted = fragment; "
                    f"x death, > merge; colour = generation", fontsize=8)
    ax[0].set_xlabel("time")
    ax[1].plot(tt, pops); ax[1].set_title("cells (>= smin)"); ax[1].set_xlabel("time")
    fig.tight_layout(); fig.savefig(f"screens/{tag}_lin2.png", dpi=80); plt.close(fig)


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
    if "dt" in over:
        W.META["dt"] = float(over.pop("dt"))
    s = W.init(seed, W.META["size"], **over)
    ind, snaps, pops = run(W, s, nsteps, every, smin)
    qualify(ind)
    dt = W.META["dt"]
    summ = summary(ind, pops, every, dt, nsteps)
    # free spores: core particles outside clusters, mean over samples with t in [60, 200]
    free = [int((((sn[2] == 1) | (sn[2] == 3)) & (sn[3] == 0)).sum()) for sn in snaps if 60 <= sn[0] <= 200]
    summ["free_spores_60_200"] = float(np.mean(free)) if free else None
    summ["nsub_hist"] = {int(k): v for k, v in s.get("nsub_hist", {}).items()}
    summ["clips"] = s.get("n_clip", 0)
    summ["det_events"] = s.get("n_det_events", 0)
    title = f"{W.META['name']} seed {seed} dt {dt} " + " ".join(a for a in sys.argv[4:] if not a.startswith(("every", "smin", "seed")))
    figure(ind, pops, every, dt, tag, title[:110])
    print(tag, json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in summ.items()}))
    Path(f"scratch/{tag}_lin2.json").write_text(json.dumps({"summary": summ, "individuals": {str(k): v for k, v in ind.items()},
                                                            "pops": pops, "every": every, "dt": dt}))
    np.savez_compressed(f"scratch/{tag}_snaps.npz", x=np.stack([q[1] for q in snaps]).astype(np.float16),
                        t=np.stack([q[2] for q in snaps]).astype(np.int8), owner=np.stack([q[3] for q in snaps]).astype(np.int32),
                        L=s["p"]["L"], dt=every * dt)


if __name__ == "__main__":
    main()
