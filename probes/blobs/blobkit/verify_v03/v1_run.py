"""verify_v03/v1_run.py — V1 decision-identity gate (CPU-JAX).

run_assay_batch (ONE batch) vs run_assay_b singles on the SAME jax backend +
dtype. Identity = bitwise canon of the full out dict (wall fields stripped).

Course-corrected sizing (controller, 2026-08-28: local CPU-JAX walls are
expected slow; full-ladder long-world identity runs on the GPU pod): the
ladder is exercised at t0=1250, cap=2500 — legal parameters of the LOCKED
run_assay_b — so extension/repack/cap paths all run at half cost. Decision
logic is scale-free (same code at any t0/cap).

  V1a f32 t0=1250 cap=2500: [m0 s7, m4 s1, mv3 s1, bf s1]  B_pad=(2,4)
           4 heterogeneous genomes (incl. bilin bf, 8-field mv3) in ONE
           tensor; at this t0 no criterion fires -> rung-1 exit identity
           for all four (batch init + pooled battery + finalize).
  V1b f64 t0=2500 cap=5000: [m0 s7, mv3 s1]  B_pad=(1,2)
           mv3 fires a_mem at 2500 (0.2 G1) -> extension; m0 exits static
           -> REPACK 2->1 at the rung boundary; mv3 caps at 5000. f64
           identity chain anchor (0.2 G1/G2: jax-f64 singles == locked CPU
           assay bitwise at noise=0; descriptor-level with noise).
  V1c f32 t0=2500 cap=5000: [m0 s7, mv3 s1]  B_pad=(2,)
           same ladder, repack DISABLED by B_pad -> exited m0 row rides as
           inert BALLAST while mv3 extends: no-cross-talk identity for the
           in-place path.

Usage: v1_run.py a|b|c   (writes V1a.json / V1b.json / V1c.json)
"""
import json, os, sys, time
from functools import partial
from types import SimpleNamespace
os.environ.setdefault("BLOBKIT_RESULTS", "")
import blobkit.assay_v2 as A
import blobkit.assay_v2b as AB
from blobkit.soup.backend import get_backend
from blobkit import worlds
from blobkit.assay_batch import run_assay_batch

HERE = os.path.dirname(os.path.abspath(__file__))
STRIP = {"wall_total", "wall_s", "wall_sim"}

def strip_wall(o):
    if isinstance(o, dict):
        return {k: strip_wall(v) for k, v in o.items() if k not in STRIP}
    if isinstance(o, (list, tuple)):
        return [strip_wall(v) for v in o]
    return o

def canon(out):
    return json.dumps(strip_wall(A.js(out)), sort_keys=True)

def backend_dtype(dtype):
    ns = get_backend("gpu")
    return SimpleNamespace(name="gpu",
                           init_soup=partial(ns.init_soup, dtype=dtype),
                           advance=ns.advance, snapshot_rec=ns.snapshot_rec,
                           save_run=ns.save_run)

def run_gate(name, specs, dtype, B_pad, T0, CAP):
    """specs: (world, seed) or (world, seed, t0_lane, cap_lane)."""
    jobs, kicks_map, lane_tc = [], {}, []
    for spec in specs:
        w, s = spec[0], spec[1]
        tl, cl = (spec[2], spec[3]) if len(spec) > 2 else (T0, CAP)
        lane_tc.append((tl, cl))
        g = worlds.WORLDS[w]()
        jobs.append(dict(genome=g, seed=s, t0=tl, cap=cl))
        k = worlds.KICKS.get(g["id"])
        if k:
            kicks_map[g["id"]] = k

    t0 = time.time()
    outs = run_assay_batch(jobs, dtype=dtype, kicks_map=kicks_map,
                           t0=T0, cap=CAP, B_pad=B_pad, verbose=True)
    t_batch = time.time() - t0

    be = backend_dtype(dtype)
    singles, t_single = [], 0.0
    for spec, (tl, cl) in zip(specs, lane_tc):
        w, s = spec[0], spec[1]
        g = worlds.WORLDS[w]()
        t0 = time.time()
        ref = AB.run_assay_b(g, seed=s, kicks=worlds.KICKS.get(g["id"]),
                             t0=tl, cap=cl, results_path=None, verbose=True,
                             backend=be, workers=0)
        t_single += time.time() - t0
        singles.append(ref)

    lanes, all_ok = [], True
    for (w, s), bo, ro in zip([(sp[0], sp[1]) for sp in specs], outs, singles):
        cb, cr = canon(bo), canon(ro)
        ok = cb == cr
        all_ok &= ok
        lane = dict(world=w, seed=s, match_bitwise=ok,
                    batch=dict(interest=bo["interest"],
                               T=bo["horizon"]["T_used"],
                               why=bo["horizon"]["why_stopped"],
                               n_ext=bo["horizon"]["n_extensions"]),
                    single=dict(interest=ro["interest"],
                                T=ro["horizon"]["T_used"],
                                why=ro["horizon"]["why_stopped"],
                                n_ext=ro["horizon"]["n_extensions"]),
                    canon_chars=len(cr))
        if not ok:
            for i, (a, b) in enumerate(zip(cb, cr)):
                if a != b:
                    lane["first_diff"] = dict(pos=i,
                                              batch=cb[max(0, i-80):i+80],
                                              single=cr[max(0, i-80):i+80])
                    break
        lanes.append(lane)
    res = dict(gate=f"V1{name}", dtype=dtype, backend="cpu-jax",
               t0=T0, cap=CAP, B_pad=list(B_pad),
               pass_=all_ok, wall_batch=round(t_batch, 1),
               wall_singles=round(t_single, 1), lanes=lanes,
               note=("bitwise identity vs run_assay_b(backend=gpu) singles "
                     "on the same jax backend+dtype; t0/cap reduced (legal "
                     "locked-assay params) per controller directive — "
                     "standard-ladder long-world identity reruns on the GPU "
                     "pod. Singles chain to the locked CPU assay via 0.2 "
                     "G1/G2 + gpu GATES.md."))
    json.dump(res, open(os.path.join(HERE, f"V1{name}.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "lanes"}))
    for l in lanes:
        print(l["world"], l["seed"], "match:", l["match_bitwise"],
              l["batch"], l["single"])
    return all_ok

def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "a"
    if which == "a":
        ok = run_gate("a", [("m0", 7), ("m4", 1), ("mv3", 1), ("bf", 1)],
                      "f32", (2, 4), 1250.0, 2500.0)
    elif which == "b":
        ok = run_gate("b", [("m0", 7), ("mv3", 1)], "f64", (1, 2),
                      2500.0, 5000.0)
    elif which == "c":
        ok = run_gate("c", [("m0", 7), ("mv3", 1)], "f32", (2,),
                      2500.0, 5000.0)
    elif which == "d":
        # DETERMINISTIC repack + t0-floor coverage: m0 decides at 2500
        # (static, exits) -> repack 2->1 while mv3 rides BELOW ITS FLOOR to
        # its first decision at 5000. Single ref: run_assay_b(t0=5000).
        # Exercises: per-lane t0, repack under live lane, chunk-safe
        # continuation across the rung boundary. Criteria-independent.
        ok = run_gate("d", [("m0", 7, 2500.0, 2500.0),
                            ("mv3", 1, 5000.0, 5000.0)],
                      "f32", (1, 2), 2500.0, 5000.0)
    elif which == "e":
        # DETERMINISTIC ballast coverage: same ladder, B_pad=(2,) disables
        # the repack -> m0's exited row keeps stepping as inert ballast
        # while mv3 rides. No-cross-talk identity for the in-place path.
        ok = run_gate("e", [("m0", 7, 2500.0, 2500.0),
                            ("mv3", 1, 5000.0, 5000.0)],
                      "f32", (2,), 2500.0, 5000.0)
    else:
        raise SystemExit(f"unknown gate {which}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
