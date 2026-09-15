"""pod_gen.py — island generation driver (pod-local, synchronous gens).

Commands:
  init           gen-0: eval all seeds/*.json under assay_v2 (island archive).
  breed <gen>    build gen jobs from island archive per island_config mix.
  ingest <gen>   insert screens; write seed2 shards (t0 floor = seed1 T_used);
                 select L192 lane (box-flagged, cap/gen) + longH lane (top-3).
  ingest2 <gen>  attach seed2; write seed3 shards for seed2-passers.
  ingest3 <gen>  attach seed3 (block library needs seed2_ok AND seed3_ok).
  lanes <gen>    write L192/longH confirm shards selected at ingest.
  status         table.
Shard files: out/jobs/<tag>_w{i}.json. Workers: pod_worker.py.
"""
import copy, glob, json, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pod_lib as PL
sys.path.insert(0, os.path.join(HERE, "lib"))
import genome as G
import operators_lib as OP
import ds2_ops as OPS2
import sampler as SA
import funnel as FU

SEEDS_DIR = os.path.join(HERE, "seeds")


def state(P):
    try:
        return json.load(open(P["state"]))
    except Exception:
        return dict(gen=0, gen_stats=[])


def save_state(st, P):
    json.dump(PL.js(st), open(P["state"], "w"), indent=1)


def cost_proxy(job):
    g = job["genome"]
    base = len(g["acts"]) + len(g["chans"])
    if job.get("L"):
        base *= (job["L"] / 128.0) ** 2
    if job.get("cap") and job["cap"] > 20000:
        base *= 1.5
    return base


def write_shards(jobs, tag, cfg):
    P = PL.paths(cfg)
    nw = int(cfg["n_workers"])
    jobs = sorted(jobs, key=cost_proxy, reverse=True)
    shards = [[] for _ in range(nw)]
    loads = [0.0] * nw
    for j in jobs:
        i = int(np.argmin(loads))
        shards[i].append(j)
        loads[i] += cost_proxy(j)
    outp = []
    for i, sh in enumerate(shards):
        if not sh:
            continue
        p = os.path.join(P["jobs"], f"{tag}_w{i}.json")
        json.dump(PL.js(sh), open(p, "w"))
        outp.append(p)
    print(f"{tag}: {len(jobs)} jobs -> {len(outp)} shards, "
          f"loads {['%.0f' % l for l in loads]}", flush=True)
    return outp


def load_seeds():
    out = []
    for p in sorted(glob.glob(os.path.join(SEEDS_DIR, "*.json"))):
        g = json.load(open(p))
        gid = g.get("id") or os.path.basename(p)[:-5]
        g["id"] = gid
        out.append(g)
    return out


def cmd_init(cfg):
    isl = cfg["island"]
    jobs = []
    for g in load_seeds():
        jobs.append(dict(cand=f'p{isl}g0_{g["id"]}', gen=0, op="seed",
                         kind="screen", parents=[g["id"]],
                         origin=g.get("provenance", {}).get("kind", "seed"),
                         genome=G.genome_json(OPS2.ensure_vtags(g, origin=g["id"]))))
    return write_shards(jobs, "g0", cfg)


def arch(P):
    try:
        return json.load(open(P["archive"]))
    except Exception:
        return {}


def pick_elite(a, rng, top=8):
    keys = sorted(a)
    if not keys:
        return None, None
    if top and rng.random() < 0.5:
        ks = sorted(keys, key=lambda k: -a[k]["interest"])[:top]
        k = ks[rng.integers(len(ks))]
    else:
        k = keys[rng.integers(len(keys))]
    return k, a[k]


def base_blocks():
    bl = [G.ref_M0(), G.ref_M4(5.7), G.ref_XV(), G.ref_BFIELD(),
          OP.ref_iso(0.65), OP.ref_iso(0.75)]
    for p in glob.glob(os.path.join(SEEDS_DIR, "blk_*.json")):
        bl.append(json.load(open(p)))
    return [OPS2.ensure_vtags(b, origin=b.get("id", "ref")) for b in bl]


def blocks_for(gen, a):
    """3-seed rule: block library needs seed2_ok AND seed3_ok (+1 gen old)."""
    blocks = base_blocks()
    for key, meta in a.items():
        first = meta.get("first_gen", meta.get("gen", 0))
        if (meta.get("seed2_ok") and meta.get("seed3_ok")
                and gen - first >= 1 and meta.get("genome")):
            b = copy.deepcopy(meta["genome"])
            b["id"] = f'blk_{meta["cand"]}'
            blocks.append(b)
    return blocks


def sample_immigrant(rng, max_tries=400):
    for _ in range(max_tries):
        g, why = SA.sample_uniform(rng)
        if why is not None:
            continue
        if FU.funnel(g)["stage"] == "pass":
            return g
    return None


def cmd_breed(gen, cfg):
    isl = cfg["island"]
    P = PL.paths(cfg)
    rng = np.random.default_rng(cfg["rng_base"] + 1000 * isl + gen)
    a = arch(P)
    if not a:
        print("EMPTY ARCHIVE — run init+ingest first")
        return
    mix, mmix = cfg["mix"], cfg["merge_mix"]
    blocks = blocks_for(gen, a)
    jobs, k = [], 0

    def push(child, op, parents, params, cell_src=None):
        nonlocal k
        cand = f"p{isl}g{gen}_{k:03d}"
        child["id"] = cand
        jobs.append(dict(cand=cand, gen=gen, op=op, kind="screen",
                         parents=parents, cell_src=cell_src, params=params,
                         genome=G.genome_json(child)))
        k += 1

    unary = ([("mutate",)] * mix["mutate"] + [("mint_bilin",)] * mix["mint_bilin"]
             + [("delete_bilin",)] * mix["delete_bilin"]
             + [("add_chan",)] * mix["add_chan"] + [("dup_act",)] * mix["dup_act"])
    for (op,) in unary:
        for _try in range(80):
            key, cell = pick_elite(a, rng)
            if cell is None:
                break
            p = OPS2.ensure_vtags(copy.deepcopy(cell["genome"]),
                                  origin=cell["cand"])
            p["id"] = cell["cand"]
            if op == "mutate":
                child, info = OPS2.mutate_v2(p, rng)
            elif op == "mint_bilin":
                child, info = OPS2.mint_bilin(p, rng, f"v{isl}_{gen}_{k:03d}")
            elif op == "delete_bilin":
                if not p.get("bilin"):
                    continue
                child, info = OPS2.delete_bilin(p, rng)
            elif op == "add_chan":
                child, info = OPS2.add_chan(p, rng, max_fields=PL.MAX_FIELDS)
            else:
                child, info = OPS2.dup_act(p, rng, max_act=PL.MAX_ACT,
                                           max_fields=PL.MAX_FIELDS)
            if child is None:
                continue
            push(child, op, [cell["cand"]], info, cell_src=key)
            break

    merge_plan = (["cross_edge"] * mmix["cross_edge"]
                  + ["slow_tanh"] * mmix["slow_tanh"]
                  + ["share_chan"] * mmix["share_chan"])
    for mode in merge_plan:
        for _try in range(150):
            key, cell = pick_elite(a, rng)
            if cell is None:
                break
            p1 = copy.deepcopy(cell["genome"])
            p1["id"] = cell["cand"]
            if rng.random() < 0.6:
                p2 = copy.deepcopy(blocks[rng.integers(len(blocks))])
            else:
                _k2, c2 = pick_elite(a, rng, top=None)
                p2 = copy.deepcopy(c2["genome"])
                p2["id"] = c2["cand"]
            na = len(p1["acts"]) + len(p2["acts"])
            nf = na + len(p1["chans"]) + len(p2["chans"])
            md = mode
            if na > PL.MAX_ACT or nf > PL.MAX_FIELDS:
                continue
            if md == "slow_tanh" and nf + 1 > PL.MAX_FIELDS:
                md = "cross_edge"
            kw = {}
            if md == "share_chan":
                kw["rescale"] = None if rng.random() < 0.5 else 0.5
            elif md == "cross_edge":
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
            child, info = OPS2.merge_v2(md, p1, p2, rng=rng, **kw)
            if child is None:
                continue
            post = bool(rng.random() < 0.35)
            if post:
                m, _mi = OPS2.mutate_v2(child, rng)
                if m is not None:
                    child = m
            push(child, "merge_" + md, [p1["id"], p2.get("id", "?")],
                 dict(post_mut=post, **PL.js(kw)), cell_src=key)
            break

    for _ in range(mix["immigrate"]):
        g = sample_immigrant(rng)
        if g is None:
            continue
        g = OPS2.ensure_vtags(g, origin="imm")
        push(g, "immigrate", None, None)

    return write_shards(jobs, f"g{gen}", cfg)


def rows(P):
    try:
        return json.load(open(P["results"]))
    except Exception:
        return []


def cmd_ingest(gen, cfg):
    P = PL.paths(cfg)
    rws = [r for r in rows(P) if r.get("kind") == "ds2_eval"
           and r.get("gen") == gen and r.get("phase") == "screen"]
    seen, ev, opstat, scores = set(), dict(new=0, improved=0, held=0, dead=0), {}, []
    s2jobs = []
    for r in rws:
        if r["cand"] in seen:
            continue
        seen.add(r["cand"])
        event, cell = PL.archive_insert(r, P)
        if event in ("new", "improved"):
            with PL.locked_json(P["archive"], {}) as c:
                if event == "new":
                    c.data[cell]["first_gen"] = gen
                c.data[cell]["gen"] = gen
                c.write()
            s2jobs.append(dict(cand=r["cand"] + "_s2", gen=gen, op="seed2",
                               kind="seed2", seed=cfg["seed2"],
                               t0=r.get("T_used"), parents=[r["cand"]],
                               genome=r["genome"]))
        ev[event] = ev.get(event, 0) + 1
        op = r.get("op") or "?"
        s = opstat.setdefault(op, dict(n=0, ok=0, best=0.0, events=0))
        s["n"] += 1
        s["ok"] += int(r.get("status") == "ok")
        s["best"] = max(s["best"], r.get("interest", 0) or 0)
        s["events"] += int(event in ("new", "improved"))
        if r.get("interest") is not None:
            scores.append((r["cand"], r["interest"], r))
    scores.sort(key=lambda z: -z[1])
    # ---- lanes
    lane_jobs = []
    a = arch(P)
    boxed = [r for _, _, r in scores
             if (r.get("flags") or {}).get("box_limit")
             and (r.get("interest") or 0) > 30.0]
    for r in boxed[:cfg.get("l192_per_gen", 2)]:
        lane_jobs.append(dict(cand=r["cand"] + "_L192", gen=gen, op="l192",
                              kind="lane", seed=r.get("seed", 1), L=192.0,
                              t0=r.get("T_used"), parents=[r["cand"]],
                              genome=r["genome"]))
    for cand, interest, r in scores[:cfg.get("longh_top", 3)]:
        if (r.get("horizon") or {}).get("why") == "cap" or \
           (r.get("T_used") or 0) >= 20000:
            lane_jobs.append(dict(cand=cand + "_LH", gen=gen, op="longh",
                                  kind="lane", seed=r.get("seed", 1),
                                  cap=40000.0, t0=r.get("T_used"),
                                  parents=[cand], genome=r["genome"]))
    walls = [(r.get("wall_assay", 0) or 0) for r in rws]
    minted_rows = [r for r in rws if r.get("minted")]
    stat = dict(gen=gen, n=len(seen), events=ev, opstat=opstat,
                n_extended=sum(1 for r in rws if r.get("extended")),
                mean_I=float(np.mean([s for _, s, _ in scores])) if scores else 0,
                max_I=scores[0][1] if scores else 0,
                max_cand=scores[0][0] if scores else None,
                wall_assay_total=round(float(np.sum(walls)), 1),
                census=dict(minted_rows=len(minted_rows),
                            minted_ok=sum(1 for r in minted_rows
                                          if r.get("status") == "ok"),
                            minted_best=max([r.get("interest", 0) or 0
                                             for r in minted_rows], default=0),
                            cells_with_minted=sum(1 for v in arch(P).values()
                                                  if v.get("minted"))))
    st = state(P)
    st["gen_stats"] = [s for s in st.get("gen_stats", [])
                       if s["gen"] != gen] + [stat]
    st["gen"] = gen
    save_state(st, P)
    print(json.dumps(PL.js(stat), indent=1), flush=True)
    if s2jobs:
        write_shards(s2jobs, f"s2g{gen}", cfg)
    if lane_jobs:
        write_shards(lane_jobs, f"laneg{gen}", cfg)


def cmd_ingest2(gen, cfg):
    P = PL.paths(cfg)
    rws = [r for r in rows(P) if r.get("kind") == "ds2_eval"
           and r.get("gen") == gen and r.get("phase") == "seed2"]
    s3jobs, n_ok = [], 0
    for r in rws:
        key, ok = PL.archive_seedk(r, 2, P)
        if key is None:
            continue
        n_ok += int(bool(ok))
        if ok:
            a = arch(P)
            cell = a.get(key)
            if cell and cell["cand"] + "_s2" == r["cand"]:
                s3jobs.append(dict(cand=cell["cand"] + "_s3", gen=gen,
                                   op="seed3", kind="seed3",
                                   seed=cfg["seed3"], t0=r.get("T_used"),
                                   parents=[cell["cand"]],
                                   genome=cell["genome"]))
    print(f"seed2 g{gen}: {len(rws)} rows, ok={n_ok}", flush=True)
    if s3jobs:
        write_shards(s3jobs, f"s3g{gen}", cfg)


def cmd_ingest3(gen, cfg):
    P = PL.paths(cfg)
    rws = [r for r in rows(P) if r.get("kind") == "ds2_eval"
           and r.get("gen") == gen and r.get("phase") == "seed3"]
    n_ok = 0
    for r in rws:
        key, ok = PL.archive_seedk(r, 3, P)
        n_ok += int(bool(ok))
    print(f"seed3 g{gen}: {len(rws)} rows, ok={n_ok}", flush=True)


def cmd_status(cfg):
    P = PL.paths(cfg)
    st = state(P)
    for s in st.get("gen_stats", []):
        print(f'g{s["gen"]}: n={s["n"]} ev={s["events"]} ext={s.get("n_extended")} '
              f'meanI={s["mean_I"]:.1f} maxI={s["max_I"]:.1f} ({s["max_cand"]}) '
              f'wall={s["wall_assay_total"]/3600:.1f}h census={s.get("census")}')
    a = arch(P)
    print(f"archive: {len(a)} cells "
          f"({sum(1 for v in a.values() if v.get('minted'))} minted, "
          f"{sum(1 for v in a.values() if v.get('seed2_ok') and v.get('seed3_ok'))} "
          f"block-eligible)")
    for k in sorted(a, key=lambda k: -a[k]["interest"])[:15]:
        c = a[k]
        print(f'  {k:38s} I={c["interest"]:5.1f} '
              f's2={int(bool(c.get("seed2_ok")))} s3={int(bool(c.get("seed3_ok")))} '
              f'{c["cand"]}')


if __name__ == "__main__":
    cfg = PL.config()
    cmd = sys.argv[1]
    if cmd == "init":
        cmd_init(cfg)
    elif cmd == "breed":
        cmd_breed(int(sys.argv[2]), cfg)
    elif cmd == "ingest":
        cmd_ingest(int(sys.argv[2]), cfg)
    elif cmd == "ingest2":
        cmd_ingest2(int(sys.argv[2]), cfg)
    elif cmd == "ingest3":
        cmd_ingest3(int(sys.argv[2]), cfg)
    elif cmd == "status":
        cmd_status(cfg)
