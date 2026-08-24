"""gen.py — deepsearch generation driver (synchronous generations).
init            gen-0 jobs: 7 GT battery-recomputes (free, truncated saved runs)
                + 8 elite screens + 20 jitters around all 15 seeds.
breed <gen>     build generation <gen> jobs from archive (10 mutate + 14 merge).
ingest <gen>    insert该 gen's screen rows into archive; update state/blocks.
confirm [n]     T=5000 confirm jobs for top-n unconfirmed holders (default 12).
status          lean per-gen table.
Shards: jobs/g<gen>_w{0..3}.json (round-robin by cost proxy).
"""
import copy, glob, json, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ds_lib as DL
import genome as G
import operators_lib as OP

SEEDS_DIR = os.path.join(HERE, "seeds")
JOBS = os.path.join(HERE, "jobs")
GT_RUNS = os.path.join(DL.L0, "complexity", "runs")
N_MUT, N_MERGE, N_WORKERS = 10, 14, 4
GT_TAGS = ["m0", "m4", "xv", "bf", "pred", "coex", "mv3"]


def load_seeds():
    out = {}
    for p in sorted(glob.glob(os.path.join(SEEDS_DIR, "*.json"))):
        g = json.load(open(p))
        out[g["id"]] = g
    return out


def gt_genomes():
    sys.path.insert(0, os.path.join(DL.L0, "complexity"))
    import worlds
    return {k: worlds.WORLDS[k]() for k in GT_TAGS}


def base_blocks():
    """Primitive merge blocks (always available)."""
    bl = [G.ref_M0(), G.ref_M4(5.7), G.ref_XV(), G.ref_BFIELD(),
          OP.ref_iso(0.65), OP.ref_iso(0.75)]
    eng = json.load(open(os.path.join(SEEDS_DIR, "engine_10748.json")))
    bl.append(eng)
    return bl


def state():
    try:
        return json.load(open(DL.STATE))
    except Exception:
        return dict(gen=-1, blocks=[], gen_stats=[])


def save_state(st):
    json.dump(DL.js(st), open(DL.STATE, "w"), indent=1)


def cost_proxy(job):
    if job.get("gt_npz"):
        return 0.5
    g = job["genome"]
    return len(g["acts"]) + len(g["chans"])


def write_shards(jobs, gen):
    jobs = sorted(jobs, key=cost_proxy, reverse=True)
    shards = [[] for _ in range(N_WORKERS)]
    loads = [0.0] * N_WORKERS
    for j in jobs:
        i = int(np.argmin(loads))
        shards[i].append(j)
        loads[i] += cost_proxy(j)
    paths = []
    for i, sh in enumerate(shards):
        p = os.path.join(JOBS, f"g{gen}_w{i}.json")
        json.dump(DL.js(sh), open(p, "w"))
        paths.append(p)
    print(f"gen {gen}: {len(jobs)} jobs -> {len(paths)} shards, "
          f"cost proxies {['%.0f' % l for l in loads]}")
    return paths


# ------------------------------------------------------------------ init
def cmd_init():
    rng = np.random.default_rng(20260223)
    jobs = []
    gts = gt_genomes()
    for k in GT_TAGS:
        jobs.append(dict(cand=f"g0_gt_{k}", gen=0, op="gt", kind="screen",
                         T=DL.T_SCREEN,
                         gt_npz=os.path.join(GT_RUNS, f"gt_{k}_s1.npz"),
                         genome=G.genome_json(gts[k])))
    seeds = load_seeds()
    elite_only = [k for k in seeds if k not in
                  ("pred_101_58", "coex_116_46")]      # those two ARE gts
    for k in elite_only:
        jobs.append(dict(cand=f"g0_seed_{k}", gen=0, op="seed", kind="screen",
                         parents=[k], genome=seeds[k]))
    pool = dict(list(gts.items()) + list(seeds.items()))
    names = sorted(pool)
    for i in range(20):
        pk = names[i % len(names)]
        child, info = OP.mutate(copy.deepcopy(pool[pk]), rng)
        tries = 0
        while child is None and tries < 5:
            child, info = OP.mutate(copy.deepcopy(pool[pk]), rng)
            tries += 1
        if child is None:
            continue
        child["id"] = f"g0_jit_{i:02d}"
        jobs.append(dict(cand=f"g0_jit_{i:02d}", gen=0, op="mutate",
                         kind="screen", parents=[pk],
                         params=dict(moves=info.get("moves")), genome=child))
    return write_shards(jobs, 0)


# ------------------------------------------------------------------ breed
def elites():
    try:
        arch = json.load(open(DL.ARCHIVE))
    except Exception:
        arch = {}
    return arch


def pick_elite(arch, rng, top=None):
    keys = sorted(arch)
    if not keys:
        return None, None
    if top and rng.random() < 0.5:
        ks = sorted(keys, key=lambda k: -arch[k]["interest"])[:top]
        k = ks[rng.integers(len(ks))]
    else:
        k = keys[rng.integers(len(keys))]
    return k, arch[k]


def cmd_breed(gen):
    rng = np.random.default_rng(31000 + gen)
    st = state()
    arch = elites()
    if not arch:
        print("EMPTY ARCHIVE — run ingest first")
        return
    blocks = base_blocks()
    blk_ids = [b["id"] for b in blocks]
    for cell, meta in arch.items():
        first_gen = meta.get("first_gen", meta.get("gen", 0))
        if gen - first_gen >= 2 and meta["genome"] is not None:
            b = copy.deepcopy(meta["genome"])
            b["id"] = f'blk_{meta["cand"]}'
            blocks.append(b)
            blk_ids.append(b["id"])
    st["blocks_g%d" % gen] = blk_ids
    jobs, k, mtries = [], 0, 0
    while len(jobs) < N_MUT and mtries < 200:
        mtries += 1
        key, cell = pick_elite(arch, rng, top=8)
        p = copy.deepcopy(cell["genome"])
        child, info = OP.mutate(p, rng)
        if child is None:
            continue
        cand = f"ds{gen}_{k:03d}"
        child["id"] = cand
        jobs.append(dict(cand=cand, gen=gen, op="mutate", kind="screen",
                         parents=[cell["cand"]], cell_src=key,
                         params=dict(moves=info.get("moves")), genome=child))
        k += 1
    tries = 0
    while len(jobs) < N_MUT + N_MERGE and tries < 400:
        tries += 1
        key, cell = pick_elite(arch, rng, top=8)
        p1 = copy.deepcopy(cell["genome"])
        if rng.random() < 0.6:
            p2 = copy.deepcopy(blocks[rng.integers(len(blocks))])
        else:
            k2, c2 = pick_elite(arch, rng)
            p2 = copy.deepcopy(c2["genome"])
            p2.setdefault("id", c2["cand"])
        na = len(p1["acts"]) + len(p2["acts"])
        nf = na + len(p1["chans"]) + len(p2["chans"])
        if na > DL.MAX_ACT or nf > DL.MAX_FIELDS:
            continue
        mode = ("share_chan", "cross_edge", "slow_tanh")[rng.integers(3)]
        if mode == "slow_tanh" and nf + 1 > DL.MAX_FIELDS:
            mode = "cross_edge"      # slow_tanh adds a channel; stay in cap
        kw = {}
        if mode == "share_chan":
            kw["rescale"] = None if rng.random() < 0.5 else 0.5
        elif mode == "cross_edge":
            kw["eta"] = float(np.exp(rng.uniform(np.log(0.03), np.log(0.3))))
            kw["symmetric"] = bool(rng.random() < 0.8)
        else:
            kw = dict(tau_b=float(np.exp(rng.uniform(np.log(20), np.log(400)))),
                      D_b=(0.0 if rng.random() < 0.3 else
                           float(np.exp(rng.uniform(np.log(0.1), np.log(3.0))))),
                      gamma=float(np.exp(rng.uniform(np.log(0.02), np.log(0.15)))
                                  * (1 if rng.random() < 0.7 else -1)),
                      kap=float(np.exp(rng.uniform(np.log(0.01), np.log(0.1)))
                                * (1 if rng.random() < 0.7 else -1)),
                      thr=float(rng.uniform(0.3, 0.9)),
                      sc=float(rng.uniform(0.2, 1.0)))
        child, info = OP.MERGE_OPS[mode](p1, p2, rng=rng, **kw)
        if child is None:
            continue
        post = bool(rng.random() < 0.35)
        if post:
            m, mi = OP.mutate(child, rng)
            if m is not None:
                child = m
        cand = f"ds{gen}_{k:03d}"
        child["id"] = cand
        jobs.append(dict(cand=cand, gen=gen, op="merge_" + mode, kind="screen",
                         parents=[p1.get("id", cell["cand"]),
                                  p2.get("id", "?")],
                         cell_src=key, params=dict(post_mut=post, **kw),
                         genome=child))
        k += 1
    save_state(st)
    return write_shards(jobs, gen)


# ------------------------------------------------------------------ ingest
def cmd_ingest(gen):
    rows = [r for r in json.load(open(DL.RESULTS))
            if r.get("kind") == "ds_eval" and r.get("gen") == gen
            and r.get("phase") == "screen"]
    seen, ev = set(), dict(new=0, improved=0, held=0, dead=0)
    scores = []
    for r in rows:
        if r["cand"] in seen:
            continue
        seen.add(r["cand"])
        if r.get("origin") == "gt" or r.get("op") == "gt":
            r = dict(r, origin="gt")
        event, cell = DL.archive_insert(r)
        if event in ("new", "improved"):
            with DL.locked_json(DL.ARCHIVE, {}) as c:
                if event == "new":
                    c.data[cell]["first_gen"] = gen
                c.data[cell]["gen"] = gen
                c.write()
        ev[event] = ev.get(event, 0) + 1
        if r.get("interest") is not None:
            scores.append((r["cand"], r["interest"]))
    st = state()
    scores.sort(key=lambda z: -z[1])
    walls = [r.get("wall_sim", 0) or 0 for r in rows]
    stat = dict(gen=gen, n=len(seen), events=ev,
                mean_I=float(np.mean([s for _, s in scores])) if scores else 0,
                max_I=scores[0][1] if scores else 0,
                max_cand=scores[0][0] if scores else None,
                wall_sim_total=round(float(np.sum(walls)), 1))
    st["gen_stats"] = [s for s in st.get("gen_stats", [])
                       if s["gen"] != gen] + [stat]
    st["gen"] = gen
    save_state(st)
    print(json.dumps(stat, indent=1))


# ------------------------------------------------------------------ confirm
def cmd_confirm(n=12):
    arch = elites()
    holders = sorted(arch.items(), key=lambda kv: -kv[1]["interest"])
    jobs = []
    for key, cell in holders:
        if cell.get("confirm_interest") is not None:
            continue
        if cell.get("origin") == "gt":
            continue
        jobs.append(dict(cand=cell["cand"] + "_cf", gen=99, op="confirm",
                         kind="confirm", T=DL.T_CONFIRM,
                         parents=[cell["cand"]], cell_src=key,
                         genome=cell["genome"]))
        if len(jobs) >= n:
            break
    return write_shards(jobs, "cf")


def cmd_status():
    st = state()
    for s in st.get("gen_stats", []):
        print(f'g{s["gen"]}: n={s["n"]} events={s["events"]} '
              f'meanI={s["mean_I"]:.1f} maxI={s["max_I"]:.1f} '
              f'({s["max_cand"]}) wall={s["wall_sim_total"]}s')
    arch = elites()
    print(f"archive: {len(arch)} cells")
    for k in sorted(arch, key=lambda k: -arch[k]["interest"]):
        c = arch[k]
        cf = c.get("confirm_interest")
        print(f'  {k:24s} I={c["interest"]:5.1f}'
              + (f" cf={cf:5.1f}" if cf is not None else "        ")
              + f' {c["cand"]} (g{c.get("first_gen", "?")}, {c.get("op")})')


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "init":
        cmd_init()
    elif cmd == "breed":
        cmd_breed(int(sys.argv[2]))
    elif cmd == "ingest":
        cmd_ingest(int(sys.argv[2]))
    elif cmd == "confirm":
        cmd_confirm(int(sys.argv[2]) if len(sys.argv) > 2 else 12)
    elif cmd == "status":
        cmd_status()
