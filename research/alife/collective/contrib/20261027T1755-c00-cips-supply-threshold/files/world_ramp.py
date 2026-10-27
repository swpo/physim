"""Wrapper around c40's layered CIPS world (20261026T1100-c40-cips-layered-divide-claim/world.py, unchanged).

One thing changes: the fuel regrowth rate kF follows a piecewise-linear schedule in time
(WORLD_P "sched": [[t_rel, kF], ...], constant beyond the ends), applied by setting s["par"]["kF"]
before each call of the claim's own step(). Everything else is the claim's step().

Optional WORLD_P keys (all ignored by the claim's own code):
  state     : npz with e, p, F, s, t saved by this wrapper; the run branches from it (t_rel = 0 there)
  sched     : [[t_rel, kF], ...] piecewise-linear kF(t_rel); default: the claim's kF throughout
  log       : path of a jsonl log (one record per log_every steps + one per tracker event)
  log_every : steps between log records (default 100 = 10 t)
  save_at   : list of t_rel at which to save the full state (npz) to save_prefix + f"_{t_rel:g}.npz"
  snap_every: steps between float16 snapshots of e written to snap_dir (0: none)
Tracking: components of e > 0.5 (8-connected, periodic), matched between log records by pixel overlap.
"""
import importlib.util
import json
import os

import numpy as np
from scipy import ndimage

CLAIM = "/home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py"
_spec = importlib.util.spec_from_file_location("cips_claim_world", CLAIM)
W0 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(W0)

X = json.loads(os.environ.get("WORLD_P", "{}"))
META = dict(W0.META)
META["name"] = "cips-layered-divide-kFramp"
META["parent"] = "collective/contrib/20261026T1100-c40-cips-layered-divide-claim"
META["mutation"] = "kF follows a piecewise-linear schedule (supply ramp); claim step() unchanged"


def kF_at(sched, tr):
    if not sched:
        return W0.P["kF"]
    ts = [a for a, _ in sched]
    ks = [b for _, b in sched]
    return float(np.interp(tr, ts, ks))


def plabel(mask):
    """8-connected labels with periodic wrap (labels joined across the edges)."""
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    if n == 0:
        return lab, 0
    par = np.arange(n + 1)

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            par[max(ra, rb)] = min(ra, rb)

    H, W = mask.shape
    pairs = []
    for sh in (-1, 0, 1):   # rows: last row vs first row (with diagonal neighbours)
        pairs.append((lab[-1, :], np.roll(lab[0, :], sh)))
        pairs.append((lab[:, -1], np.roll(lab[:, 0], sh)))
    for a, b in pairs:
        m = (a > 0) & (b > 0)
        for x, y in set(zip(a[m].tolist(), b[m].tolist())):
            union(x, y)
    roots = np.array([find(i) for i in range(n + 1)])
    u, inv = np.unique(roots, return_inverse=True)
    lab2 = inv[lab]  # root 0 -> 0 because label 0 is its own root and the smallest
    return lab2.reshape(lab.shape), len(u) - 1


def _write(s, rec):
    if s["_log"]:
        with open(s["_log"], "a") as fh:
            fh.write(json.dumps(rec) + "\n")


def init(seed, size):
    s = W0.init(seed, size)
    if X.get("state"):
        z = np.load(X["state"])
        for k in ("e", "p", "F", "s"):
            s[k] = z[k].astype(float).copy()
        s["t"] = float(z["t"])
    s["_t0"] = s["t"]
    s["_k"] = 0
    s["_sched"] = X.get("sched")
    s["_log"] = X.get("log")
    s["_every"] = int(X.get("log_every", 100))
    s["_save"] = sorted(X.get("save_at", []))
    s["_saveprefix"] = X.get("save_prefix", "state")
    s["_snap"] = int(X.get("snap_every", 0))
    s["_snapdir"] = X.get("snap_dir")
    if s["_snapdir"]:
        os.makedirs(s["_snapdir"], exist_ok=True)
    s["_prev"] = None
    s["_ids"] = {}
    s["_next"] = 1
    s["par"]["kF"] = kF_at(s["_sched"], 0.0)
    if s["_log"]:
        open(s["_log"], "w").close()
        _write(s, {"type": "meta", "t0": s["_t0"], "sched": s["_sched"], "state": X.get("state"), "seed": seed})
    _track(s)
    return s


def _track(s):
    e = s["e"]
    lab, n = plabel(e > 0.5)
    tr = s["_k"] * s["par"]["dt"]
    kF = s["par"]["kF"]
    ids = {}
    events = []
    if s["_prev"] is None:
        for c in range(1, n + 1):
            ids[c] = s["_next"]; s["_next"] += 1
    else:
        plab, pids = s["_prev"]
        m = (plab > 0) & (lab > 0)
        pairs = set(zip(plab[m].tolist(), lab[m].tolist()))
        fwd, bwd = {}, {}
        for a, b in pairs:
            fwd.setdefault(a, set()).add(b)
            bwd.setdefault(b, set()).add(a)
        for c in range(1, n + 1):
            ps = bwd.get(c, set())
            if len(ps) == 1 and len(fwd[next(iter(ps))]) == 1:
                ids[c] = pids[next(iter(ps))]
            else:
                ids[c] = s["_next"]; s["_next"] += 1
                if len(ps) == 0:
                    events.append({"ev": "birth", "id": ids[c]})
                elif len(ps) == 1:
                    events.append({"ev": "split_child", "id": ids[c], "parent": pids[next(iter(ps))]})
                else:
                    events.append({"ev": "merge_child", "id": ids[c], "parents": [pids[a] for a in ps]})
        for a, pid in pids.items():
            if a not in fwd:
                events.append({"ev": "death", "id": pid})
    s["_prev"] = (lab, ids)
    areas = ndimage.sum(np.ones_like(e), lab, index=np.arange(1, n + 1)) if n else []
    emax = ndimage.maximum(e, lab, index=np.arange(1, n + 1)) if n else []
    Fin = ndimage.mean(s["F"], lab, index=np.arange(1, n + 1)) if n else []
    smean = ndimage.mean(s["s"], lab, index=np.arange(1, n + 1)) if n else []
    body = lab > 0
    rec = {"type": "rec", "t": round(s["t"], 3), "t_rel": round(tr, 3), "kF": kF, "n": int(n),
           "ids": [ids[c] for c in range(1, n + 1)], "areas": [int(a) for a in areas],
           "emax": [round(float(x), 4) for x in emax], "F_in": [round(float(x), 4) for x in Fin],
           "s_in": [round(float(x), 4) for x in smean],
           "meanF": float(s["F"].mean()), "F_bath": float(s["F"][~body].mean()) if (~body).any() else None,
           "e_total": float(e.sum()), "e_max": float(e.max()), "e_std": float(e.std()),
           "body_area": int(body.sum())}
    _write(s, rec)
    for ev in events:
        ev.update({"type": "event", "t_rel": round(tr, 3), "kF": kF})
        _write(s, ev)


def step(s):
    tr = s["_k"] * s["par"]["dt"]
    s["par"]["kF"] = kF_at(s["_sched"], tr)
    W0.step(s)
    s["_k"] += 1
    tr = s["_k"] * s["par"]["dt"]
    s["par"]["kF"] = kF_at(s["_sched"], tr)   # kF reported with the record is the one in force now
    if s["_k"] % s["_every"] == 0:
        _track(s)
    if s["_snap"] and s["_k"] % s["_snap"] == 0 and s["_snapdir"]:
        np.save(os.path.join(s["_snapdir"], f"e_{tr:08.1f}.npy"), s["e"].astype(np.float16))
    while s["_save"] and tr >= s["_save"][0] - 1e-6:
        ts = s["_save"].pop(0)
        np.savez(f'{s["_saveprefix"]}_{ts:g}.npz', e=s["e"], p=s["p"], F=s["F"], s=s["s"], t=s["t"])
    return s


def fields(s):
    return W0.fields(s)


def damage(s, mask):
    return W0.damage(s, mask)
