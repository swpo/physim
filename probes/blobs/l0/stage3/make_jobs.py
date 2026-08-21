"""stage3/make_jobs.py — generate stage-3 job shards from the stage-2 harvest.

Tiers (priority order; pods run shards in filename order):
  P1 jobs_census_XX.json  — kicked act-indexed A1 census. Tier-1 targets:
     all alive archive-cell exemplars + onset/near-onset candidates + the
     rest of alive candidates (tier 2) up to --census-cap (default: ALL alive).
  P2 jobs_island.json     — s2_107_48 speed island: one-dial scans +-5/10%
     on every chan tau/D + cross-W + Du(act1) + 12 sigma=0.08 jitters.
  P3 jobs_plateau.json    — uni_3034 design rule (thr/sc/W/K_tanh/slow-chan
     one-dial scans; extended d0 grid pair runs) + stack probes (uni_3034,
     s2_128_26, M4 control) + mech attribution for s2_128_26 (radial +
     per-channel ablation pairs).
  P4 jobs_encounter.json  — 3-flavor encounter tables on T1-line genomes.
"""
import argparse, copy, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "lib"))
import genome as G

S2 = os.path.join(os.path.dirname(HERE), "stage2")


def load():
    M = json.load(open(os.path.join(S2, "merged_results.json")))
    A = json.load(open(os.path.join(S2, "merged_archive.json")))
    return M, A


def is_alive(r):
    return r.get("a1") and any(v["cls"] in ("persist", "travel")
                               for v in r["a1"].values())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--census-cap", type=int, default=10000)
    ap.add_argument("--census-shards", type=int, default=12)
    ap.add_argument("--outdir", default=HERE)
    args = ap.parse_args()
    M, A = load()
    byc = {r["cand"]: r for r in M}

    # ---------------- P1 census targets
    targets, seen = [], set()
    def add(r, why):
        if r["cand"] in seen or not r.get("genome"):
            return
        seen.add(r["cand"])
        targets.append(dict(kind="census", cand=r["cand"],
                            ref=r["genome"]["provenance"].get("ref", "uni"),
                            why=why, genome=r["genome"],
                            fold_dist=r.get("fold_dist"),
                            margin=r.get("g0a_margin"),
                            acts=list(range(len(r["genome"]["acts"])))))
    # alive archive exemplars first
    for k, v in A.items():
        if "persist" in k or "travel" in k:
            r = byc.get(v.get("cand"))
            if r is not None:
                add(r, "cell_exemplar")
    # onset/near-onset
    for r in M:
        if r.get("desc") and r["desc"][7] in ("onset", "near_onset"):
            add(r, "onset")
    # rest of alive
    for r in M:
        if is_alive(r):
            add(r, "alive")
        if len(targets) >= args.census_cap:
            break
    ns = args.census_shards
    shards = [targets[i::ns] for i in range(ns)]
    for i, sh in enumerate(shards):
        p = os.path.join(args.outdir, f"jobs_census_{i:02d}.json")
        json.dump(sh, open(p, "w"))
        print(f"P1 {p}: {len(sh)} genomes")

    # ---------------- P2 speed island around s2_107_48
    base = byc["s2_107_48_jit"]["genome"]
    jobs = [dict(kind="census", cand="isl_base", ref="rh1_7000", why="island",
                 genome=base, acts=[0, 1])]
    def variant(tag, mut):
        g = copy.deepcopy(base)
        mut(g)
        # u0 continuation (dials do not move the cubic here, but keep safe)
        for a in g["acts"]:
            rr = G.cubic_roots(a["lam"], a["k1"])
            if rr:
                a["u0"] = min(rr, key=lambda x: abs(x - a["u0"]))
        jobs.append(dict(kind="census", cand=f"isl_{tag}", ref="rh1_7000",
                         why="island", genome=g, acts=[0, 1]))
    for ci in range(len(base["chans"])):
        for f in (0.9, 0.95, 1.05, 1.1):
            variant(f"tau{ci}_{f}", lambda g, ci=ci, f=f: g["chans"][ci].__setitem__("tau", g["chans"][ci]["tau"] * f))
    for f in (0.9, 1.1):
        variant(f"W01_{f}", lambda g, f=f: g["W"][0].__setitem__(1, g["W"][0][1] * f))
        variant(f"Du1_{f}", lambda g, f=f: g["acts"][1].__setitem__("Du", g["acts"][1]["Du"] * f))
    rng = np.random.default_rng(777)
    import sampler as SA
    for j in range(12):
        g = copy.deepcopy(base)
        g, why = SA.jitter_genome(rng, g, sigma=0.08, sigma_d=0.3)
        if why:
            continue
        jobs.append(dict(kind="census", cand=f"isl_jit{j}", ref="rh1_7000",
                         why="island", genome=g, acts=[0, 1]))
    p = os.path.join(args.outdir, "jobs_island.json")
    json.dump(jobs, open(p, "w"))
    print(f"P2 {p}: {len(jobs)} jobs")

    # ---------------- P3 plateau design rule + stacks + mech
    res1 = json.load(open(os.path.join(os.path.dirname(HERE), "results.json")))
    g3034 = [r for r in res1 if r.get("cand") == "s1v3_uni_3034"][0]["genome"]
    g28 = byc["s2_128_26_uni"]["genome"]
    jobs = []
    D0_GRID = [8, 10, 12, 14, 16, 18, 20, 24, 28]
    def pjob(tag, g, act=0, d0s=None):
        jobs.append(dict(kind="pair_grid", cand=f"pl_{tag}", genome=g, act=act,
                         d0s=d0s or D0_GRID, T=800.0))
    pjob("base3034", g3034)
    def pvar(tag, mut):
        g = copy.deepcopy(g3034)
        mut(g)
        pjob(tag, g)
    for f in (0.6, 0.8, 1.2, 1.4):
        pvar(f"thr_{f}", lambda g, f=f: g["chans"][2].__setitem__("thr", g["chans"][2]["thr"] * f))
        pvar(f"K2_{f}", lambda g, f=f: g["K"][0].__setitem__(2, g["K"][0][2] * f))
    for f in (0.5, 0.75, 1.5, 2.0):
        pvar(f"sc_{f}", lambda g, f=f: g["chans"][2].__setitem__("sc", g["chans"][2]["sc"] * f))
    for f in (0.5, 2.0):
        pvar(f"tau1_{f}", lambda g, f=f: g["chans"][1].__setitem__("tau", g["chans"][1]["tau"] * f))
        pvar(f"D1_{f}", lambda g, f=f: g["chans"][1].__setitem__("D", g["chans"][1]["D"] * f))
    # mech attribution for s2_128_26: per-channel K ablations, pair d0=12
    pjob("base28", g28, act=0, d0s=[8, 10, 12, 14, 16, 20])
    for ci in range(3):
        g = copy.deepcopy(g28)
        g["K"][0][ci] = 0.0
        pjob(f"abl28_K{ci}0", g, act=0, d0s=[12])
    # radial profiles
    jobs.append(dict(kind="radial", cand="rad_3034", genome=g3034, act=0,
                     variant="bare"))
    jobs.append(dict(kind="radial", cand="rad_28", genome=g28, act=0,
                     variant="bare"))
    jobs.append(dict(kind="radial", cand="rad_M4", genome=G.ref_M4(5.7), act=0,
                     variant="dressed"))
    # stacks: plateau cargo candidates + M4 shuttle positive control
    for tag, g, sp in (("stack_3034", g3034, 27.9), ("stack_28", g28, 14.1),
                       ("stack_M4ctrl", G.ref_M4(5.7), 14.9)):
        for n in (2, 3):
            jobs.append(dict(kind="stack", cand=f"{tag}_n{n}", genome=g, act=0,
                             n=n, spacing=sp, T=2000.0))
        jobs.append(dict(kind="stack", cand=f"{tag}_n3_noise", genome=g, act=0,
                         n=3, spacing=sp, T=2000.0, noise=2e-3, seed=1))
    p = os.path.join(args.outdir, "jobs_plateau.json")
    json.dump(jobs, open(p, "w"))
    print(f"P3 {p}: {len(jobs)} jobs")

    # ---------------- P4 encounters on 3-act all-alive cells
    cells3 = [k for k in A if k.startswith("3|") and
              k.count("persist") + k.count("travel") >= 3]
    jobs = []
    added = 0
    for k in sorted(cells3, key=lambda k: -A[k]["count"]):
        v = A[k]
        g = v["genome"]
        jobs.append(dict(kind="encounter", cand=f"enc_{v['cand']}", cell=k,
                         genome=g, pairs=[[0, 1], [0, 2], [1, 2]],
                         same=[0, 1, 2], d0s=[8, 12, 16], T=400.0))
        added += 1
        if added >= 6:
            break
    p = os.path.join(args.outdir, "jobs_encounter.json")
    json.dump(jobs, open(p, "w"))
    print(f"P4 {p}: {len(jobs)} genomes x (3 cross pairs + 3 same) x 3 d0")


if __name__ == "__main__":
    main()
