"""evolve.py — l0-evolver MAP-Elites merge+mutate loop (stage 1, local).

Usage: evolve.py <n_children> [seed0] [tag] 
One CHILD per iteration: pick operator (mutate p=MUT_P else merge), pick
parent(s) from pool, build genome, funnel (cheap reject), assay battery
(sampler's lib battery = A1 panel/A2/A3) + A4 cross (only if >=2 acts
persist), insert into SHARED archive (sampler descriptor, exemplar =
most-negative margin) and into evolve/archive_x.json (descriptor + cross_sig).
Every child appended to evolve/results.json (lineage: parents + op + params).

Pool = reference genomes + iso species + ALIVE cells of shared archive
(poke class contains persist/travel) + own extended elites; refreshed each
REFRESH children. Parent pick: refs 0.3 / alive elites 0.55 / any elite 0.15.
Merge caps: n_act <= 3, n_chan <= 8 (budget).

Assay-count accounting (comparison currency, documented estimate):
a1: 1 if variant bare else 2; a2: len(d0s); a3: 2 (dial re-pokes, each is a
panel of 1-2 runs — undercount possible, same convention applied to sampler
rows in the yield comparison); a4: 1. Wall seconds logged exactly.
"""
import sys, os, json, time, fcntl, copy
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
L0DIR = os.path.dirname(BASE)
sys.path.insert(0, os.path.join(L0DIR, "lib"))
sys.path.insert(0, BASE)

import genome as G
import funnel as FU
import assays as AS
import operators_lib as OP
from assays_x import a4_cross

ARCHIVE = os.path.join(L0DIR, "archive.json")
ARCHIVE_X = os.path.join(BASE, "archive_x.json")
RESULTS = os.path.join(BASE, "results.json")

MUT_P = 0.5
MERGE_MODES = ("share_chan", "cross_edge", "slow_tanh")
REFRESH = 6


def append_result(record, path=RESULTS):
    lockp = path + ".lock"
    with open(lockp, "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            with open(path) as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        record = dict(record)
        record.setdefault("ts", time.strftime("%Y-%m-%d %H:%M:%S"))
        data.append(record)
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f)
        os.replace(tmp, path)
    return len(data)


def archive_update(path, key, margin, genome, cand_id, extra=None):
    """Atomic MAP-Elites insert (sampler's exemplar rule). Returns
    (is_new_cell, replaced_exemplar)."""
    lockp = path + ".lock"
    with open(lockp, "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            with open(path) as f:
                arch = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            arch = {}
        cell = arch.get(key)
        new = cell is None
        replaced = False
        rec = dict(margin=margin, genome=G.genome_json(genome), cand=cand_id,
                   count=(cell["count"] + 1 if cell else 1))
        if extra:
            rec.update(extra)
        if cell is not None and margin >= cell["margin"]:
            rec["margin"] = cell["margin"]
            rec["genome"] = cell["genome"]
            rec["cand"] = cell["cand"]
            for k in (extra or {}):
                if k in cell:
                    rec[k] = cell[k]
        else:
            replaced = not new
        arch[key] = rec
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(arch, f)
        os.replace(tmp, path)
    return new, replaced


# ------------------------------------------------------------------ pool
def ref_pool():
    refs = [G.ref_M0(), G.ref_M4(5.0), G.ref_M4(5.7), G.ref_M4(5.9),
            G.ref_VVW(), G.ref_XV(), G.ref_BFIELD(),
            OP.ref_iso(0.65), OP.ref_iso(0.75)]
    return refs


def load_pool():
    pool = dict(refs=ref_pool(), alive=[], any=[])
    try:
        arch = json.load(open(ARCHIVE))
    except (FileNotFoundError, json.JSONDecodeError):
        arch = {}
    for key, cell in arch.items():
        gnm = cell["genome"]
        entry = (key, gnm)
        pool["any"].append(entry)
        # poke classes live at parts[5:5+n_act] (poke_sig itself contains '|');
        # any persist/travel anywhere in the key = an alive-ish world
        if ("persist" in key) or ("travel" in key):
            pool["alive"].append(entry)
    try:
        archx = json.load(open(ARCHIVE_X))
        for key, cell in archx.items():
            if "persist" in key or "travel" in key:
                pool["alive"].append((key, cell["genome"]))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return pool


def pick_parent(pool, rng):
    r = rng.random()
    if r < 0.3 or not pool["alive"]:
        g = pool["refs"][rng.integers(len(pool["refs"]))]
        return copy.deepcopy(g), g["id"]
    if r < 0.85 or not pool["any"]:
        key, g = pool["alive"][rng.integers(len(pool["alive"]))]
    else:
        key, g = pool["any"][rng.integers(len(pool["any"]))]
    g = copy.deepcopy(g)
    return g, g.get("id", key)


# ------------------------------------------------------------------ child
def make_child(pool, rng):
    """Returns (genome|None, lineage_rec)."""
    if rng.random() < MUT_P:
        p, pid = pick_parent(pool, rng)
        child, info = OP.mutate(p, rng)
        lin = dict(op="mutate", parents=[pid],
                   params=dict(moves=info.get("moves"), fail=info.get("fail")))
        return child, lin
    mode = MERGE_MODES[rng.integers(len(MERGE_MODES))]
    for _ in range(8):
        p1, id1 = pick_parent(pool, rng)
        p2, id2 = pick_parent(pool, rng)
        if len(p1["acts"]) + len(p2["acts"]) <= 3 and \
           len(p1["chans"]) + len(p2["chans"]) <= 7:
            break
    else:
        return None, dict(op="merge_" + mode, parents=[], params=dict(fail="size_cap"))
    kw = {}
    if mode == "share_chan":
        kw["rescale"] = None if rng.random() < 0.5 else 0.5
    elif mode == "cross_edge":
        kw["eta"] = float(np.exp(rng.uniform(np.log(0.03), np.log(0.3))))
        kw["symmetric"] = bool(rng.random() < 0.8)
    else:
        kw = dict(tau_b=float(np.exp(rng.uniform(np.log(20), np.log(400)))),
                  D_b=(0.0 if rng.random() < 0.3
                       else float(np.exp(rng.uniform(np.log(0.1), np.log(3.0))))),
                  gamma=float(np.exp(rng.uniform(np.log(0.02), np.log(0.15)))
                              * (1 if rng.random() < 0.7 else -1)),
                  kap=float(np.exp(rng.uniform(np.log(0.01), np.log(0.1)))
                            * (1 if rng.random() < 0.7 else -1)),
                  thr=float(rng.uniform(0.3, 0.9)),
                  sc=float(rng.uniform(0.2, 1.0)))
    child, info = OP.MERGE_OPS[mode](p1, p2, rng=rng, **kw)
    lin = dict(op="merge_" + mode, parents=[id1, id2], params=kw)
    if child is None:
        lin["params"]["fail"] = info.get("fail")
        return None, lin
    # optional post-merge mutation (p=0.35): merge-and-mutate in one child
    if rng.random() < 0.35:
        m, mi = OP.mutate(child, rng)
        if m is not None:
            child = m
            lin["post_mutate"] = mi.get("moves")
    return child, lin


def assay_counts(recs):
    n = 0
    for i, a1 in (recs.get("a1") or {}).items():
        n += 1 if a1.get("variant") == "bare" else 2
    n += len(recs.get("a2") or [])
    if recs.get("a3") and "classes" in recs["a3"]:
        n += 2
    return n


def one_child(pool, rng, cand_id, tag, gen):
    rec = dict(kind="evo_child", cand=cand_id, tag=tag, gen=gen)
    t0 = time.time()
    child, lin = make_child(pool, rng)
    rec["lineage"] = lin
    rec["gen_s"] = round(time.time() - t0, 4)
    if child is None:
        rec["stage"] = "op_fail"
        return rec
    child["id"] = cand_id
    child["provenance"] = dict(kind="evolve", **{k: v for k, v in lin.items()})
    rec["genome"] = G.genome_json(child)
    probs = G.validate(child)
    if probs:
        rec["stage"] = "invalid"
        rec["why"] = probs
        return rec
    t0 = time.time()
    fr = FU.funnel(child)
    rec["funnel_s"] = round(time.time() - t0, 4)
    rec.update({k: fr[k] for k in fr if k != "stage"})
    rec["stage"] = fr["stage"]
    if fr["stage"] != "pass":
        return rec
    t0 = time.time()
    desc, recs = AS.battery(child, fr)
    rec["assay_s"] = round(time.time() - t0, 2)
    rec["a1"] = recs["a1"]
    rec["a2"] = recs["a2"]
    rec["a3"] = recs["a3"]
    rec["n_assays"] = assay_counts(recs)
    # A4 cross if >= 2 acts persist/travel
    alive_acts = [i for i in sorted(recs["a1"]) 
                  if recs["a1"][i]["cls"] in ("persist", "travel")]
    cross = None
    if len(alive_acts) >= 2:
        t0 = time.time()
        d0f = 0.6 if recs["a1"][alive_acts[0]].get("variant") == "dressed0.6" else 0.0
        d1f = 0.6 if recs["a1"][alive_acts[1]].get("variant") == "dressed0.6" else 0.0
        cross = a4_cross(child, alive_acts[0], alive_acts[1],
                         dress0=d0f, dress1=d1f)
        rec["a4"] = cross
        rec["a4_s"] = round(time.time() - t0, 2)
        rec["n_assays"] += 1
    cross_sig = cross["cls"] if cross else "na"
    rec["desc"] = list(map(str, desc))
    rec["cross_sig"] = cross_sig
    rec["stage"] = "assayed"
    key = "|".join(map(str, desc))
    new_s, _ = archive_update(ARCHIVE, key, fr["g0a_margin"], child, cand_id)
    keyx = key + "|" + cross_sig
    new_x, _ = archive_update(ARCHIVE_X, keyx, fr["g0a_margin"], child, cand_id,
                              extra=dict(cross_sig=cross_sig, lineage=lin))
    rec["cell"] = key
    rec["cell_x"] = keyx
    rec["new_cell_shared"] = bool(new_s)
    rec["new_cell_x"] = bool(new_x)
    return rec


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    seed0 = int(sys.argv[2]) if len(sys.argv) > 2 else 9000
    tag = sys.argv[3] if len(sys.argv) > 3 else "e1"
    pool = load_pool()
    for j in range(n):
        if j % REFRESH == 0 and j:
            pool = load_pool()
        seed = seed0 + j
        rng = np.random.default_rng(seed)
        gen = j // REFRESH
        cand_id = f"{tag}_{seed}"
        t0 = time.time()
        try:
            rec = one_child(pool, rng, cand_id, tag, gen)
        except Exception as e:
            import traceback
            rec = dict(kind="evo_child", cand=cand_id, tag=tag, gen=gen,
                       stage="error", why=repr(e), tb=traceback.format_exc()[-800:])
        rec["total_s"] = round(time.time() - t0, 2)
        append_result(rec)
        print(f"{cand_id} g{gen} {rec.get('lineage',{}).get('op','?')} "
              f"{rec['stage']} {rec.get('desc','')}{' X:'+rec['cross_sig'] if rec.get('cross_sig') and rec.get('cross_sig')!='na' else ''} "
              f"new={rec.get('new_cell_shared','-')} {rec['total_s']}s", flush=True)


if __name__ == "__main__":
    main()
