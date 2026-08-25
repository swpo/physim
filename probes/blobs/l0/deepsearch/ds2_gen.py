"""ds2_gen.py — deepsearch v2 generation driver.

seed_import      free gen-0: archive_v2 seeded from v1 archive holders (their
                 metrics_v1 screen scores stay valid while metrics=v1) + GT
                 rows. Confirmed-at-T5000 holders and GTs enter seed2_ok=True
                 (block-eligible); unconfirmed enter seed2_ok=False (breedable
                 as parents, NOT as blocks until they earn a 2nd seed).
init_full        gen-0 re-eval jobs for ALL seed genomes (pod run: required
                 when metrics flips to v2 — scores/keys not comparable).
breed <gen>      v2 mix from ds2_config.json:
                 mutate 5 | mint_bilin 3 | delete_bilin 1 | add_chan 2 |
                 dup_act 2 | merge 6 (3 cross / 2 slow_tanh / 1 share) |
                 immigrate 5 (~20%, funnel-passed uniform randoms).
ingest <gen>     insert screens into archive_v2; per-op stats + vertex census;
                 writes seed2 shards for this gen's new/improved holders.
ingest2 <gen>    attach seed2 rows (block-library gate) + census update.
confirm [n]      T=confirm jobs for top-n unconfirmed holders.
status           per-gen table + vertex census.
"""
import copy, glob, json, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ds_lib as DL
import ds2_lib as D2
import ds2_ops as OPS2
import genome as G
import operators_lib as OP
import sampler as SA
import funnel as FU

GT_TAGS = ["m0", "m4", "xv", "bf", "pred", "coex", "mv3"]


def state():
    try:
        return json.load(open(D2.STATE2))
    except Exception:
        return dict(gen=0, gen_stats=[])


def save_state(st):
    json.dump(DL.js(st), open(D2.STATE2, "w"), indent=1)


def cost_proxy(job):
    g = job["genome"]
    return len(g["acts"]) + len(g["chans"])


def write_shards(jobs, tag, n_workers=None):
    cfg = D2.config()
    nw = n_workers or cfg["n_workers"]
    jobs = sorted(jobs, key=cost_proxy, reverse=True)
    shards = [[] for _ in range(nw)]
    loads = [0.0] * nw
    for j in jobs:
        i = int(np.argmin(loads))
        shards[i].append(j)
        loads[i] += cost_proxy(j)
    paths = []
    for i, sh in enumerate(shards):
        if not sh:
            continue
        p = os.path.join(D2.JOBS2, f"{tag}_w{i}.json")
        json.dump(DL.js(sh), open(p, "w"))
        paths.append(p)
    print(f"{tag}: {len(jobs)} jobs -> {len(paths)} shards, "
          f"loads {['%.0f' % l for l in loads]}")
    return paths


# ------------------------------------------------------------- seed pool
def gt_genomes():
    sys.path.insert(0, os.path.join(D2.L0, "complexity"))
    import worlds
    return {k: worlds.WORLDS[k]() for k in GT_TAGS}


def v1_archive():
    try:
        return json.load(open(DL.ARCHIVE))
    except Exception:
        return {}


NAMED_SEEDS = ["ds3_017", "ds3_014", "ds6_000"]   # brief-mandated seeds


def named_seed_rows():
    """Screen rows for brief-named seeds not (or no longer) in v1 archive
    (ds3_017 was displaced by its own mutant ds5_003 but is confirm=75.1)."""
    try:
        rows = json.load(open(DL.RESULTS))
    except Exception:
        return {}
    out = {}
    for r in rows:
        if (r.get("kind") == "ds_eval" and r.get("phase") == "screen"
                and r.get("cand") in NAMED_SEEDS and r.get("genome")):
            out[r["cand"]] = r
    return out


def cmd_seed_import():
    """Free gen-0 (metrics=v1 only): copy v1 holders + GTs into archive_v2."""
    cfg = D2.config()
    assert cfg["metrics"] == "v1", "seed_import is only valid under metrics=v1"
    arch1 = v1_archive()
    # brief-named seeds enter as synthetic cells if displaced from v1 archive
    named = named_seed_rows()
    v1_cands = {c["cand"] for c in arch1.values()}
    for cand, r in named.items():
        if cand in v1_cands:
            continue
        arch1[f'{r["cell"]}#named_{cand}'] = dict(
            cand=cand, gen=r.get("gen"), op=r.get("op"),
            parents=r.get("parents"), interest=r["interest"],
            summary=r.get("summary"), genome=r["genome"], origin="ds",
            confirm_interest=75.1 if cand == "ds3_017" else None)
    n_in, n_blk = 0, 0
    with DL.locked_json(D2.ARCHIVE2, {}) as c:
        for key1, cell in sorted(arch1.items(),
                                 key=lambda kv: -kv[1]["interest"]):
            if not cell.get("genome"):
                continue
            g = OPS2.ensure_vtags(copy.deepcopy(cell["genome"]),
                                  origin=cell["cand"])
            key = f'{key1.split("#")[0]}|a{len(g["acts"])}'
            if "#named_" in key1:
                key += f'#{cell["cand"]}'     # keep displaced named seed
            is_gt = cell.get("origin") == "gt"
            ci = cell.get("confirm_interest")
            blk_ok = bool(is_gt or (ci is not None
                                    and ci >= 0.6 * cell["interest"]))
            entry = dict(cand=cell["cand"], gen=0, op=cell.get("op"),
                         metrics="v1",
                         parents=cell.get("parents"),
                         interest=cell["interest"],
                         summary=cell.get("summary"), genome=G.genome_json(g),
                         origin=("gt" if is_gt else "v1_import"),
                         n_bilin=len(g.get("bilin", [])),
                         minted=D2.minted_uids(g), vtags=g["vtags"],
                         seed2_interest=ci, seed2_ok=blk_ok,
                         confirm_interest=ci,
                         first_gen=0, count=1, history=[])
            old = c.data.get(key)
            if old is None or entry["interest"] > old["interest"]:
                c.data[key] = entry
                n_in += 1
                n_blk += int(blk_ok)
        c.write()
    print(f"archive_v2 seeded: {n_in} cells ({n_blk} block-eligible)")


def cmd_init_full():
    """Pod-run gen-0: re-eval every seed genome under the CURRENT metric.
    Pool = 7 GTs + all v1 archive holders + brief-named seeds (ds3_017 was
    displaced from the v1 archive by its own mutant). With metrics=v2 the
    archive MUST be fresh (mixing guard enforces)."""
    jobs, seen = [], set()
    for k, g in gt_genomes().items():
        jobs.append(dict(cand=f"v2g0_gt_{k}", gen=0, op="gt", kind="screen",
                         origin="gt", genome=G.genome_json(g)))
    arch1 = v1_archive()
    for key1, cell in sorted(arch1.items(), key=lambda kv: -kv[1]["interest"]):
        if cell.get("origin") == "gt" or not cell.get("genome"):
            continue
        if cell["cand"] in seen:
            continue
        seen.add(cell["cand"])
        jobs.append(dict(cand=f'v2g0_{cell["cand"]}', gen=0, op="seed",
                         kind="screen", parents=[cell["cand"]],
                         genome=cell["genome"]))
    for cand, r in named_seed_rows().items():
        if cand in seen:
            continue
        seen.add(cand)
        jobs.append(dict(cand=f"v2g0_{cand}", gen=0, op="seed",
                         kind="screen", parents=[cand], genome=r["genome"]))
    return write_shards(jobs, "g0")


# ------------------------------------------------------------------ breed
def arch2():
    try:
        return json.load(open(D2.ARCHIVE2))
    except Exception:
        return {}


def pick_elite(arch, rng, top=8):
    keys = sorted(arch)
    if not keys:
        return None, None
    if top and rng.random() < 0.5:
        ks = sorted(keys, key=lambda k: -arch[k]["interest"])[:top]
        k = ks[rng.integers(len(ks))]
    else:
        k = keys[rng.integers(len(keys))]
    return k, arch[k]


def base_blocks():
    bl = [G.ref_M0(), G.ref_M4(5.7), G.ref_XV(), G.ref_BFIELD(),
          OP.ref_iso(0.65), OP.ref_iso(0.75)]
    eng = json.load(open(os.path.join(HERE, "seeds", "engine_10748.json")))
    bl.append(eng)
    return [OPS2.ensure_vtags(b, origin=b.get("id", "ref")) for b in bl]


def blocks_for(gen, arch):
    """Block library: base refs + holders that are >=1 gen old AND seed2_ok."""
    blocks = base_blocks()
    for key, meta in arch.items():
        first = meta.get("first_gen", meta.get("gen", 0))
        if meta.get("seed2_ok") and gen - first >= 1 and meta.get("genome"):
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


def cmd_breed(gen):
    cfg = D2.config()
    rng = np.random.default_rng(62000 + gen)
    arch = arch2()
    if not arch:
        print("EMPTY ARCHIVE — run seed_import / init_full+ingest first")
        return
    mix, mmix = cfg["mix"], cfg["merge_mix"]
    blocks = blocks_for(gen, arch)
    jobs, k = [], 0

    def push(child, op, parents, params, cell_src=None):
        nonlocal k
        cand = f"ds2g{gen}_{k:03d}"
        child["id"] = cand
        jobs.append(dict(cand=cand, gen=gen, op=op, kind="screen",
                         parents=parents, cell_src=cell_src, params=params,
                         genome=G.genome_json(child)))
        k += 1

    # ---- unary structural + parametric ops on elites
    unary = ([("mutate", None)] * mix["mutate"]
             + [("mint_bilin", None)] * mix["mint_bilin"]
             + [("delete_bilin", None)] * mix["delete_bilin"]
             + [("add_chan", None)] * mix["add_chan"]
             + [("dup_act", None)] * mix["dup_act"])
    for op, _ in unary:
        got = False
        for _try in range(60):
            key, cell = pick_elite(arch, rng)
            if cell is None:
                break
            p = OPS2.ensure_vtags(copy.deepcopy(cell["genome"]),
                                  origin=cell["cand"])
            p["id"] = cell["cand"]
            if op == "mutate":
                child, info = OPS2.mutate_v2(p, rng)
            elif op == "mint_bilin":
                uid = f"v{gen}_{k:03d}"
                child, info = OPS2.mint_bilin(p, rng, uid)
            elif op == "delete_bilin":
                if not p.get("bilin"):
                    continue
                child, info = OPS2.delete_bilin(p, rng)
            elif op == "add_chan":
                child, info = OPS2.add_chan(p, rng, max_fields=D2.MAX_FIELDS)
            else:
                child, info = OPS2.dup_act(p, rng, max_act=D2.MAX_ACT,
                                           max_fields=D2.MAX_FIELDS)
            if child is None:
                continue
            push(child, op, [cell["cand"]], info, cell_src=key)
            got = True
            break
        if not got:
            print(f"WARN: no candidate for {op}")

    # ---- merges (v2 wrapper: bilin preserved + vtags concat)
    merge_plan = (["cross_edge"] * mmix["cross_edge"]
                  + ["slow_tanh"] * mmix["slow_tanh"]
                  + ["share_chan"] * mmix["share_chan"])
    for mode in merge_plan:
        for _try in range(120):
            key, cell = pick_elite(arch, rng)
            if cell is None:
                break
            p1 = copy.deepcopy(cell["genome"])
            p1["id"] = cell["cand"]
            if rng.random() < 0.6:
                p2 = copy.deepcopy(blocks[rng.integers(len(blocks))])
            else:
                k2, c2 = pick_elite(arch, rng, top=None)
                p2 = copy.deepcopy(c2["genome"])
                p2["id"] = c2["cand"]
            na = len(p1["acts"]) + len(p2["acts"])
            nf = na + len(p1["chans"]) + len(p2["chans"])
            md = mode
            if na > D2.MAX_ACT or nf > D2.MAX_FIELDS:
                continue
            if md == "slow_tanh" and nf + 1 > D2.MAX_FIELDS:
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
                 dict(post_mut=post, **DL.js(kw)), cell_src=key)
            break

    # ---- immigration (plateau breaker, ~20%)
    for _ in range(mix["immigrate"]):
        g = sample_immigrant(rng)
        if g is None:
            continue
        g = OPS2.ensure_vtags(g, origin="imm")
        push(g, "immigrate", None, None)

    st = state()
    st[f"blocks_g{gen}"] = [b["id"] for b in blocks]
    save_state(st)
    return write_shards(jobs, f"g{gen}")


# ------------------------------------------------------------------ ingest
def rows_v2():
    try:
        return json.load(open(D2.RESULTS2))
    except Exception:
        return []


def cmd_ingest(gen):
    cfg0 = D2.config()
    rows = [r for r in rows_v2() if r.get("kind") == "ds2_eval"
            and r.get("gen") == gen and r.get("phase") == "screen"
            and r.get("metrics", "v1") == cfg0["metrics"]]
    seen, ev = set(), dict(new=0, improved=0, held=0, dead=0)
    opstat = {}
    scores = []
    s2jobs = []
    cfg = D2.config()
    for r in rows:
        if r["cand"] in seen:
            continue
        seen.add(r["cand"])
        event, cell = D2.archive2_insert(r)
        if event in ("new", "improved"):
            with DL.locked_json(D2.ARCHIVE2, {}) as c:
                if event == "new":
                    c.data[cell]["first_gen"] = gen
                c.data[cell]["gen"] = gen
                c.write()
            s2jobs.append(dict(cand=r["cand"] + "_s2", gen=gen, op="seed2",
                               kind="seed2", seed=cfg["seed2"],
                               t0=r.get("T_used"),      # horizon-fair gate
                               parents=[r["cand"]], cell_src=cell,
                               genome=r["genome"]))
        ev[event] = ev.get(event, 0) + 1
        op = r.get("op") or "?"
        s = opstat.setdefault(op, dict(n=0, ok=0, best=0.0, events=0))
        s["n"] += 1
        s["ok"] += int(r.get("status") == "ok")
        s["best"] = max(s["best"], r.get("interest", 0) or 0)
        s["events"] += int(event in ("new", "improved"))
        if r.get("interest") is not None:
            scores.append((r["cand"], r["interest"]))
    scores.sort(key=lambda z: -z[1])
    walls = [(r.get("wall_sim", 0) or 0) + (r.get("wall_sim_ext", 0) or 0)
             + (r.get("wall_assay", 0) or 0) for r in rows]
    n_ext = sum(1 for r in rows if r.get("extended"))
    census = D2.vertex_census(gen)
    stat = dict(gen=gen, n=len(seen), events=ev, opstat=opstat,
                n_extended=n_ext,
                mean_I=float(np.mean([s for _, s in scores])) if scores else 0,
                max_I=scores[0][1] if scores else 0,
                max_cand=scores[0][0] if scores else None,
                wall_sim_total=round(float(np.sum(walls)), 1),
                census=census)
    st = state()
    st["gen_stats"] = [s for s in st.get("gen_stats", [])
                       if s["gen"] != gen] + [stat]
    st["gen"] = gen
    save_state(st)
    print(json.dumps(DL.js(stat), indent=1))
    if s2jobs:
        write_shards(s2jobs, f"s2g{gen}")
    else:
        print("no seed2 jobs")


def cmd_ingest2(gen):
    cfg0 = D2.config()
    rows = [r for r in rows_v2() if r.get("kind") == "ds2_eval"
            and r.get("gen") == gen and r.get("phase") == "seed2"
            and r.get("metrics", "v1") == cfg0["metrics"]]
    n_ok, n_fail = 0, 0
    for r in rows:
        key, ok = D2.archive2_seed2(r)
        if key is None:
            continue
        n_ok += int(bool(ok))
        n_fail += int(not ok)
    st = state()
    for s in st.get("gen_stats", []):
        if s["gen"] == gen:
            s["seed2"] = dict(n=len(rows), ok=n_ok, fail=n_fail)
    save_state(st)
    print(f"seed2 g{gen}: {len(rows)} rows, ok={n_ok} fail={n_fail}")


def cmd_confirm(n=12):
    cfg = D2.config()
    assert cfg["metrics"] == "v1", \
        "confirm is a v1-epoch concept; under assay_v2 the 2-seed screen replaces it"
    arch = arch2()
    holders = sorted(arch.items(), key=lambda kv: -kv[1]["interest"])
    jobs = []
    for key, cell in holders:
        if cell.get("confirm_interest") is not None:
            continue
        if cell.get("origin") == "gt":
            continue
        jobs.append(dict(cand=cell["cand"] + "_cf", gen=99, op="confirm",
                         kind="confirm", T=cfg["T_confirm"],
                         parents=[cell["cand"]], cell_src=key,
                         genome=cell["genome"]))
        if len(jobs) >= n:
            break
    return write_shards(jobs, "cf2")


def cmd_status():
    st = state()
    for s in st.get("gen_stats", []):
        print(f'g{s["gen"]}: n={s["n"]} ev={s["events"]} ext={s.get("n_extended")} '
              f'meanI={s["mean_I"]:.1f} maxI={s["max_I"]:.1f} '
              f'({s["max_cand"]}) wall={s["wall_sim_total"]}s '
              f's2={s.get("seed2")}')
        for op, v in sorted(s.get("opstat", {}).items()):
            print(f'   {op:16s} n={v["n"]:2d} ok={v["ok"]:2d} '
                  f'events={v["events"]} best={v["best"]:.1f}')
    arch = arch2()
    print(f"archive_v2: {len(arch)} cells")
    for k in sorted(arch, key=lambda k: -arch[k]["interest"])[:20]:
        c = arch[k]
        print(f'  {k:30s} I={c["interest"]:5.1f} s2={c.get("seed2_ok")} '
              f'{c["cand"]} ({c.get("op")}, mint={len(c.get("minted") or [])})')
    print(json.dumps(DL.js(D2.vertex_census()), indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "seed_import":
        cmd_seed_import()
    elif cmd == "init_full":
        cmd_init_full()
    elif cmd == "breed":
        cmd_breed(int(sys.argv[2]))
    elif cmd == "ingest":
        cmd_ingest(int(sys.argv[2]))
    elif cmd == "ingest2":
        cmd_ingest2(int(sys.argv[2]))
    elif cmd == "confirm":
        cmd_confirm(int(sys.argv[2]) if len(sys.argv) > 2 else 12)
    elif cmd == "status":
        cmd_status()
