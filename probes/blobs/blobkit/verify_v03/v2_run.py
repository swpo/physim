"""verify_v03/v2_run.py — V2 throughput gate (honest, CPU-JAX f32).
32 mixed union4 genomes (deterministic sample across T_used strata), seed 1:
run_assay_batch (ONE 32-lane batch) vs sequential run_assay_b singles on the
same jax backend. Report wall ratio + worlds/hour both ways. Target >=2.5x
on CPU-JAX; GPU-device verification deferred to next pod. Writes V2.json.

Note: CPU-JAX understates the batched win vs a real GPU — batching B worlds
multiplies CPU FLOPs ~linearly (cores saturate) while a GPU amortizes launch
overhead into idle SM capacity (the accelerating-blobs 396 w/h figure).
The CPU-JAX ratio comes from (a) padding-shared jit compiles amortized once
per struct signature instead of once per world, (b) one chunk-loop dispatch
stream for B worlds, (c) threaded host records overlapping async dispatch.
"""
import argparse, json, os, sys, time
os.environ.setdefault("BLOBKIT_RESULTS", "")
import blobkit.assay_v2b as AB
from blobkit.soup.backend import get_backend
from blobkit.assay_batch import run_assay_batch

HERE = os.path.dirname(os.path.abspath(__file__))
U4 = os.environ.get("V2_UNION4",
                    "/Users/spoho/Documents/prime/test/physim/probes/blobs/l0/"
                    "deepsearch/final_cpu_harvest/union4_final_cpu.json")
N_LANES = int(os.environ.get("V2_LANES", "32"))
SEED = 1

def pick_genomes():
    """Deterministic mixed sample: keys sorted, stratified by T_used so the
    ladder exercises extensions (not just rung-1 exits). Strata scale with
    N_LANES (fractions of the 20/6/4/2 @32 reference mix)."""
    u4 = json.load(open(U4))
    strata = {2500.0: [], 5000.0: [], 10000.0: [], 20000.0: []}
    for k in sorted(u4):
        c = u4[k]
        strata.setdefault(c.get("T_used"), []).append((k, c))
    ref = {2500.0: 20, 5000.0: 6, 10000.0: 4, 20000.0: 2}   # @32
    want = {t: max(1, round(n * N_LANES / 32)) for t, n in ref.items()}
    picked = []
    for tuu in (20000.0, 10000.0, 5000.0, 2500.0):    # rare strata first
        picked += strata.get(tuu, [])[:want[tuu]]
    for tuu in (2500.0, 5000.0, 10000.0, 20000.0):    # top up to N_LANES
        for item in strata.get(tuu, []):
            if len(picked) >= N_LANES:
                break
            if item not in picked:
                picked.append(item)
    picked = picked[:N_LANES]
    gens = []
    for k, c in picked:
        g = dict(c["genome"])
        g["id"] = c["cand"]
        gens.append((k, g, c.get("T_used")))
    return gens

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cpu-jax",
                    help="label for the report (cpu-jax | H100 | ...); the "
                         "SAME script runs unchanged on the GPU pod")
    ap.add_argument("--skip-singles", action="store_true",
                    help="batch-only timing (pod quick mode): no sequential "
                         "baseline, no ratio; still emits PERF_REFERENCE")
    args = ap.parse_args()

    gens = pick_genomes()
    jobs = [(g, SEED) for _, g, _ in gens]
    print(f"[v2] {len(jobs)} lanes; T_used mix:",
          {t: sum(1 for *_, tt in gens if tt == t)
           for t in (2500.0, 5000.0, 10000.0, 20000.0)})

    # [0.3.2] nf-bucket partition (padding waste fix): one call per bucket,
    # lanes ordered by expected T (harvest T_used stamp) within the bucket.
    from blobkit.assay_batch import nf_bucket
    tstamp = {g["id"]: (t or 2500.0) for _, g, t in gens}
    buckets = {}
    for j in jobs:
        buckets.setdefault(nf_bucket(j[0]), []).append(j)
    for b in buckets:
        buckets[b].sort(key=lambda j: -tstamp.get(j[0]["id"], 2500.0))
    print(f"[v2] nf buckets: " +
          str({b: len(v) for b, v in sorted(buckets.items())}))

    t0 = time.time()
    outs_by_id = {}
    for b in sorted(buckets):
        bouts = run_assay_batch(buckets[b], dtype="f32", verbose=False)
        for (g, _s), o in zip(buckets[b], bouts):
            outs_by_id[g["id"]] = o
    outs = [outs_by_id[g["id"]] for g, _s in jobs]
    wall_batch = time.time() - t0
    wph_batch = 3600 * len(jobs) / wall_batch
    print(f"[v2] batch done in {wall_batch:.1f}s = {wph_batch:.1f} w/h "
          f"({len(buckets)} nf-bucket calls)")

    wall_seq = ratio = wph_seq = None
    agree = "n/a"
    if not args.skip_singles:
        gpu = get_backend("gpu")
        t0 = time.time()
        singles = []
        for i, (g, s) in enumerate(jobs):
            r = AB.run_assay_b(g, seed=s, results_path=None, verbose=False,
                               backend=gpu, workers=0)
            singles.append(r)
            print(f"[v2] single {i+1}/{len(jobs)} {g['id']} "
                  f"T={r['horizon']['T_used']:.0f}", flush=True)
        wall_seq = round(time.time() - t0, 1)
        ratio = round(wall_seq / wall_batch, 2)
        wph_seq = round(3600 * len(jobs) / wall_seq, 1)
        agree = sum(1 for b, s in zip(outs, singles)
                    if (b["horizon"]["T_used"] == s["horizon"]["T_used"]
                        and b["horizon"]["why_stopped"]
                        == s["horizon"]["why_stopped"]))
        agree = f"{agree}/{len(jobs)}"

    binding = args.device != "cpu-jax"
    res = dict(gate="V2", device=args.device, dtype="f32", lanes=len(jobs),
               nf_buckets={str(b): len(v) for b, v in sorted(buckets.items())},
               wall_batch_s=round(wall_batch, 1),
               wall_sequential_s=wall_seq, ratio=ratio,
               worlds_per_hour_batch=round(wph_batch, 1),
               worlds_per_hour_seq=wph_seq,
               decision_agree=agree,
               T_batch=[o["horizon"]["T_used"] for o in outs],
               T_seq=([o["horizon"]["T_used"] for o in singles]
                      if not args.skip_singles else None),
               target=2.5,
               binding=binding,
               pass_=(ratio is not None and ratio >= 2.5),
               note=("cpu-jax runs are LOCAL REFERENCE ONLY (controller "
                     "directive): batching B worlds multiplies CPU FLOPs "
                     "~linearly, so the local ratio understates the GPU win. "
                     "The BINDING throughput gate is this same script on the "
                     "H100 pod (--device H100; post reference 396 w/h "
                     "pop-96). f32 decision agreement is expected, not "
                     "bitwise-gated (V1 is the f64 identity gate)."))
    json.dump(res, open(os.path.join(HERE, "V2.json"), "w"), indent=1)

    # retrospective L5: deploy-smoke perf floor for make_bundle 0.3
    perf = dict(device=args.device, dtype="f32", B=len(jobs),
                worlds_per_hour=round(wph_batch, 1),
                measured_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                           time.gmtime()),
                binding=binding,
                note=("make_bundle 0.3 deploy smoke reads this as the perf "
                      "floor (fail-below). cpu-jax entries are reference "
                      "only; the floor binds when device is a GPU."))
    json.dump(perf, open(os.path.join(HERE, "PERF_REFERENCE.json"), "w"),
              indent=1)
    print(json.dumps({k: v for k, v in res.items()
                      if k not in ("T_batch", "T_seq")}))
    sys.exit(0 if (res["pass_"] or not binding) else 1)

if __name__ == "__main__":
    main()
