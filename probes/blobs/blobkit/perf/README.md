# blobkit/perf — benchmark suite + throughput research

RULE: **no perf claim without a bench row.** Any "0.4 is faster" statement
must cite rows from `perf/results/rows.jsonl` produced by `perf/bench.py`
on the SAME tier/config/device-class/workload hash. Hypotheses live in
`HYPOTHESES.md`; a hypothesis is closed only by rows.

## Layout

    bench.py            benchmark harness (T1/T2/T3 + compare); CPU-JAX and
                        GPU with the same script (--device cpu|gpu)
    benchconfigs.py     frozen tier configs + lane builders (workload hash)
    data/prodmix.json.gz  127 evolved genomes sampled from the deepsearch
                        final CPU harvest, preserving the measured joint
                        (nf_bucket, T_used) distribution (n=2079)
    make_prodmix.py     provenance script that built prodmix (run once)
    results/rows.jsonl  one JSON row per benchmark run (append-only)
    results/<ts>_*.json full detail per run (calls, lanes, probe)
    HYPOTHESES.md       ranked throughput-hypothesis ledger

Environment: any Python with `blobkit` (>=0.3.2) + jax installed. Local
reference env: `probes/blobs/gpu/.venv` (jax 0.4.38 CPU). On pods use the
fleet env (`blobkit[gpu]`).

## Tiers

| tier | what | configs | minutes |
|------|------|---------|---------|
| T1 `kernel` | pure batched stepping (B x nf grid) + pull/launch/record microbenches; no assay | profiles `cpu`, `gpu` | 2-5 |
| T2 `assay-mix` | prod-distribution lane mix through the REAL `run_assay_batch` ladder incl. full battery — THE prod-like w/h number | `t2` (prod, GPU), `t2mini` (local), `t2smoke` (CI) | 5-15 |
| T3 `gen-sim` | one synthetic generation end-to-end: screens -> top-K confirm lanes with t0 floors (optional tier) | `t3` (prod), `t3mini` (local) | 15-25 |

Scale vs device: prod configs (`t2`, `t3`, profile `gpu`) use the prod
substrate (L=128 -> N=256, ladder 2500->20000) — run them on the pod. Mini
configs use the same code paths on a scaled substrate (L=64 -> N=128,
ladder 1250->5000) — laptop-sized. Mini w/h compares across VERSIONS on the
same device class; never compare mini numbers to prod numbers.

## Running

    PY=probes/blobs/gpu/.venv/bin/python          # or the pod's python
    cd probes/blobs/blobkit/perf

    $PY bench.py t1 --device cpu                  # kernel tier, local
    $PY bench.py t2 --config t2mini --device cpu  # prod-like number, local
    $PY bench.py t2 --config t2smoke --device cpu # 2-3 min CI smoke
    $PY bench.py t3 --config t3mini --device cpu  # generation sim, local

    # pod (GPU) — same script, prod configs:
    $PY bench.py t1 --device gpu
    $PY bench.py t2 --config t2 --device gpu --repeat 2
    $PY bench.py t3 --config t3 --device gpu

Useful flags: `--tag <name>` (free-text label in the row), `--repeat N`
(rep0 vs rep1 exposes cold-vs-warm compile), `--battery-procs N`,
`--instrument` (time driver seams: dispatch/pull/record/snapshot/battery;
battery runs inline, row is marked `instrumented` and is NOT a headline
number — use it to see WHERE the wall goes, not how big it is).

## Comparing two versions (one command)

Install version A, run the tier; install version B, run the SAME tier;
then:

    $PY bench.py compare --tier t2 --config t2mini --device cpu

groups rows by (tier, config, device_class, workload hash) and prints
w/h + wall + ratio vs the oldest row in each group. Rows only compare when
the workload hash matches — the hash covers genomes, seeds, t0/cap ladders,
and config; if a config's workload changes it must get a NEW name
(`t2_v2`, ...), never a silent edit.

Row schema (headline fields): `{v, ts, blobkit, locks, tier, config,
device, device_class, workload, w_h, wall_s, n_lanes, n_calls, tu_total,
tu_per_s, assay_errors, statuses, instrumented, tag}` plus tier-specific
extras (T1: `cells` us/world-step, `pull_*_ms`, `launch_us`, `record_ms`;
T2/T3 detail files carry per-call walls and per-lane horizons).

## Local baseline (blobkit 0.3.2, laptop CPU-JAX, 2026-08-29)

- T1 cpu profile (N=256): us/world-step b4 1288 / b7 2790 / b10 4107 /
  b14 5170 (cost ~linear in nf_max); B=1->8 flat on CPU (no batch
  amortization to measure here — that lives on the GPU); pulls ~4-50
  ms/chunk; launch overhead ~29 us/step; host record m0 4.6 ms (REC)
  6.3 ms (CREC), pred 10.8/14.4 ms.
- T2 t2mini (6 lanes, N=128, ladder 1250->5000, workload 69dadaa2ea68):
  34.3 w/h, wall 629 s, ladder exercised (1 lane cap-rode to 5000, one
  t0=2500 confirm floor, 4 static exits), 0 assay errors. This is the
  0.3.2 local reference row; w/h is device-class-local — the GPU t2
  baseline lands at the next pod window.

## Provenance

`data/prodmix.json.gz` was built by `make_prodmix.py` from
`probes/blobs/l0/deepsearch/final_cpu_harvest/results_evo2-*.json`
(2516 ds2_eval rows; 2079 assayed with ladder T_used). Joint distribution
and confirm-stamp statistics are quoted in `HYPOTHESES.md`. The file is
FROZEN: regenerating it changes every T2/T3 workload hash and breaks row
comparability — don't, unless you version the configs.
