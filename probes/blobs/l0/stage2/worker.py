"""stage2/worker.py — standalone L0 pod worker (V3 metrics lock).

Usage:
  python worker.py --shard-seed 42 --n 100 --out shard_42.json [--smoke]
  (--smoke: n=10, quick battery — sanity check a pod in ~5 min)

Self-contained: needs only numpy+scipy and the lib/ directory shipped alongside
(sys.path bootstrap below). NO shared state: writes ONE shard json with all
candidate records + its own archive contribution; merge happens offline via
merge_shards.py. Deterministic per shard_seed (per-candidate rng =
default_rng([shard_seed, j])).

Strategy mix per shard (controller spec): 60% jitter / 40% uniform.
Jitter pool = 5 reference genomes + stage-1 novel elites (uni_3034, uni_3050,
embedded below as JSON — no file dependency) + any elites in an optional
--elites file (evolver exports, list of genome dicts).
"""
import argparse, hashlib, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "lib"))
import genome as G
import funnel as FU
import assays as AS
import sampler as SA

# ---------------------------------------------------------------- elite pool
# Stage-1 uniform-random novel worlds (results.json s1v3, genomes verbatim).
ELITES_BUILTIN = json.loads(r"""[{"name": "uni_3034", "genome": {"id": "u", "acts": [{"lam": 3.06509236748984, "k1": 0.9178141039765751, "Du": 0.4646780660293733, "u0": -1.5756215009319972}], "chans": [{"tau": 0.3439958936345144, "D": 6.501926474638161, "g": "id", "thr": 0.0, "sc": 1.0}, {"tau": 8.02134480298441, "D": 5.843231270578901, "g": "id", "thr": 0.0, "sc": 1.0}, {"tau": 1.5022046461700351, "D": 0.3225986272482061, "g": "tanh", "thr": 0.7404632627321887, "sc": 0.22281939933976516}], "W": [[1.0], [1.0], [1.0]], "K": [[-1.062624139293391, 2.531913153517124, 0.8715703402681556]], "bilin": [], "provenance": {"kind": "uniform"}}}, {"name": "uni_3050", "genome": {"id": "u", "acts": [{"lam": 1.1127434938323055, "k1": 0.434431450435948, "Du": 0.6312370821821247, "u0": -0.7040702872788149}], "chans": [{"tau": 0.8410814400680284, "D": 28.278894932369216, "g": "tanh", "thr": 1.0654724771673956, "sc": 0.350320142666483}, {"tau": 1.1634481708794688, "D": 0.5537644244994179, "g": "tanh", "thr": 0.586331793731819, "sc": 0.9550173913090487}, {"tau": 0.6484502116883654, "D": 0.4097867360689258, "g": "id", "thr": 0.0, "sc": 1.0}], "W": [[1.0], [1.0], [1.0]], "K": [[0.9833925763906586, -1.11199714318494, 0.7283808797544582]], "bilin": [], "provenance": {"kind": "uniform"}}}]""")


def genome_hash(g):
    """Stable hash of the physics content (acts/chans/W/K/bilin, rounded)."""
    def rnd(x):
        if isinstance(x, float):
            return round(x, 10)
        if isinstance(x, list):
            return [rnd(v) for v in x]
        if isinstance(x, dict):
            return {k: rnd(v) for k, v in sorted(x.items())}
        return x
    core = dict(acts=rnd([{k: a[k] for k in ("lam", "k1", "Du", "u0")}
                          for a in g["acts"]]),
                chans=rnd([{k: c.get(k) for k in ("tau", "D", "g", "thr", "sc")}
                           for c in g["chans"]]),
                W=rnd(g["W"]), K=rnd(g["K"]), bilin=rnd(g.get("bilin", [])))
    return hashlib.sha256(json.dumps(core, sort_keys=True).encode()).hexdigest()[:16]


def make_candidate(rng, strategy, elite_pool):
    if strategy == "uniform":
        return SA.sample_uniform(rng)
    # jitter: refs + elites, equal weight per entry
    pool = list(SA.REF_NAMES) + [f"elite:{i}" for i in range(len(elite_pool))]
    pick = pool[int(rng.integers(len(pool)))]
    import copy
    if pick.startswith("elite:"):
        src = elite_pool[int(pick.split(":")[1])]
        g = copy.deepcopy(src["genome"])
        g["provenance"] = dict(kind="jitter", ref=src["name"],
                               sigma=0.15, sigma_d=0.4)
        g["id"] = f"j_{src['name']}"
        return SA.jitter_genome(rng, g, sigma=0.15, sigma_d=0.4)
    g = copy.deepcopy(G.REFS[pick]())
    g["provenance"] = dict(kind="jitter", ref=pick, sigma=0.15, sigma_d=0.4)
    g["id"] = f"j_{pick}"
    return SA.jitter_genome(rng, g, sigma=0.15, sigma_d=0.4)


def one_candidate(rng, strategy, cand_id, elite_pool, quick=False):
    rec = dict(kind="candidate", cand=cand_id, strategy=strategy)
    t0 = time.time()
    g, why = make_candidate(rng, strategy, elite_pool)
    rec["gen_s"] = round(time.time() - t0, 4)
    rec["genome"] = G.genome_json(g)
    rec["ghash"] = genome_hash(g)
    rec["fold_dist"] = AS.fold_distances(g)
    if why in ("no_real_root", "root_lost"):
        rec["stage"] = "fail_g0b"
        rec["why"] = why
        return rec
    probs = G.validate(g)
    if probs:
        rec["stage"] = "invalid"
        rec["why"] = probs
        return rec
    t0 = time.time()
    fr = FU.funnel(g)
    rec["funnel_s"] = round(time.time() - t0, 4)
    rec.update({k: fr[k] for k in fr if k != "stage"})
    rec["stage"] = fr["stage"]
    if why == "no_stable_root":
        rec["why"] = why
    if fr["stage"] != "pass":
        return rec
    t0 = time.time()
    desc, recs = AS.battery(g, fr, quick=quick)
    rec["assay_s"] = round(time.time() - t0, 2)
    rec["a1"] = recs["a1"]
    rec["a2"] = recs["a2"]
    rec["a3"] = recs["a3"]
    rec["shell_ratios"] = recs.get("shell_ratios")
    rec["desc"] = list(map(str, desc))
    rec["stage"] = "assayed"
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard-seed", type=int, required=True)
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--out", default=None)
    ap.add_argument("--jitter-frac", type=float, default=0.6)
    ap.add_argument("--elites", default=None,
                    help="optional json file: [{name, genome}, ...]")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        args.n = min(args.n, 10)
    out_path = args.out or f"shard_{args.shard_seed}.json"
    elite_pool = list(ELITES_BUILTIN)
    if args.elites and os.path.exists(args.elites):
        elite_pool += json.load(open(args.elites))
    shard = dict(kind="shard", shard_seed=args.shard_seed, n=args.n,
                 jitter_frac=args.jitter_frac, metrics="V3",
                 elites=[e["name"] for e in elite_pool],
                 host=os.uname().nodename, t_start=time.time(), records=[])
    # strategy schedule: deterministic, jitter_frac of slots
    sched_rng = np.random.default_rng([args.shard_seed, 999999])
    strategies = ["jitter" if sched_rng.random() < args.jitter_frac else "uniform"
                  for _ in range(args.n)]
    t00 = time.time()
    for j in range(args.n):
        rng = np.random.default_rng([args.shard_seed, j])
        strat = strategies[j]
        cand_id = f"s2_{args.shard_seed}_{j}_{strat[:3]}"
        t0 = time.time()
        try:
            rec = one_candidate(rng, strat, cand_id, elite_pool,
                                quick=args.smoke)
        except Exception as e:
            import traceback
            rec = dict(kind="candidate", cand=cand_id, strategy=strat,
                       stage="error", why=repr(e), tb=traceback.format_exc())
        rec["total_s"] = round(time.time() - t0, 2)
        shard["records"].append(rec)
        # SAVE-AS-YOU-GO: rewrite shard file after every candidate
        shard["t_last"] = time.time()
        tmp = out_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(shard, f)
        os.replace(tmp, out_path)
        print(f"[{j+1}/{args.n}] {cand_id} {rec['stage']} "
              f"{rec.get('desc','')} {rec['total_s']}s", flush=True)
    shard["wall_s"] = round(time.time() - t00, 1)
    tmp = out_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(shard, f)
    os.replace(tmp, out_path)
    print(f"DONE shard {args.shard_seed}: {args.n} candidates "
          f"in {shard['wall_s']/60:.1f} min -> {out_path}")


if __name__ == "__main__":
    main()
