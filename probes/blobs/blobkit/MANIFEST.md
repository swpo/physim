# blobkit MANIFEST — provenance, locks, edits

Packaged 2026-08-27 from the physim source tree at
`/Users/spoho/Documents/prime/test/physim` (git b671958).
Originals stay in place; blobkit is purely additive. Verification transcript: `VERIFY.md`.

## Code modules

"Locked" = the file participates in `blobkit.verify_locks()` (SHA256 self-check
against `blobkit/_locks.json`; drift -> loud ImportWarning; `BLOBKIT_SKIP_LOCK=1`
bypasses). Upstream lock hashes (source tree `l0/complexity/v2_lock_hashes.txt`):
metrics_v2 `bcfd5d00…`, assay_v2 `1eb45780…`, soup_sim_v2 `8541dedd…` — verified
byte-identical to the sources copied here before edits were applied.

| blobkit file | source (repo-relative) | src mtime | src sha256 (12) | pkg sha256 (12) | locked | edits |
|---|---|---|---|---|---|---|
| `blobkit/genome.py` | `probes/blobs/l0/stage2/lib/genome.py` (identical in l0/lib, stage3/lib, deploy libs) | 2026-08-20 | `914fad08dffd` | `8f63c563b5be` | yes | E1, E2 |
| `blobkit/assays_v1.py` | `probes/blobs/l0/stage2/lib/assays.py` (stage-2 variant; stage3/lib adds V4 a2_cross, not packaged) | 2026-08-20 | `1883fdac243e` | `27c1af44a5ce` | yes | E3 |
| `blobkit/metrics_v1.py` | `probes/blobs/l0/complexity/metrics_v1.py` (LOCKED 2026-02-20 battery) | 2026-08-23 | `62d90c53840b` | `65e2d6305b52` | yes | E4, E5, E6 |
| `blobkit/hier_metrics.py` | `probes/search/hier_metrics.py` (== deploy/lib copy) | 2026-08-17 | `bf8a901683cd` | `bf8a901683cd` | yes | none (verbatim) |
| `blobkit/metrics_v2.py` | `probes/blobs/l0/complexity/metrics_v2.py` (LOCKED, sha `bcfd5d00…`) | 2026-08-25 | `bcfd5d00ea58` | `18b50bc7344a` | yes | E7, E8, E9 |
| `blobkit/assay_v2.py` | `probes/blobs/l0/complexity/assay_v2.py` (LOCKED, sha `1eb45780…`) | 2026-08-25 | `1eb457801efc` | `a8672a92a5de` | yes | E12, E13, E14, E14b |
| `blobkit/soup/sim_v1.py` | `probes/blobs/l0/complexity/soup_sim.py` (phase-5 S1 simulator; sim_cpu imports its helpers) | 2026-08-23 | `562aeb5d6c51` | `7f8f4f465a1a` | yes | E10 |
| `blobkit/soup/sim_cpu.py` | `probes/blobs/l0/complexity/soup_sim_v2.py` (LOCKED, sha `8541dedd…`) | 2026-08-24 | `8541deddb8d3` | `4cf2d9ea8d39` | yes | E11 |
| `blobkit/soup/sim_gpu.py` | MERGE of `probes/blobs/gpu/blobgpu/core.py` + `probes/blobs/gpu/blobgpu/packing.py` + `probes/blobs/gpu/blobgpu/soup.py` (gates: GATES.md in gpu/) | 2026-08-25 | core `282b8a268013` / packing `36eebc31a594` / soup `779577bd1e7d` | `c148457699f1` | yes | E15–E21 |
| `blobkit/soup/backend.py` | NEW (thin selector; no numerics) | — | — | `94ffb36141a0` | yes | new file |
| `blobkit/worlds.py` | REWRITE of `probes/blobs/l0/complexity/worlds.py` (data extracted, see below) | 2026-08-23 | `b55ddc1b5361` | `9435f8964f3a` | yes | R1 |
| `blobkit/operators.py` | `probes/blobs/l0/evolve/operators_lib.py` (l0-evolver operators on lib format) | 2026-08-20 | `fcca88b546b1` | `0e117f421546` | yes | E22 |
| `blobkit/soup/__init__.py` | NEW (re-export get_backend) | — | — | `c815014522d3` | yes | new file |
| `blobkit/__init__.py` | NEW (__version__, verify_locks) | — | — | `ef8b70134282` | no (checks the others) | new file |

## Edit log (every deviation from verbatim)

All edits are import/path plumbing only — no numerics, constants, or control
flow were touched. Each edit is also marked inline with `[blobkit edit E#]`.

### blobkit/assay_v2.py
- **E12** — 3 sys.path hacks + absolute imports -> package-relative (soup_sim_v2 -> soup.sim_cpu)
- **E13** — in-function metrics_v1 imports -> package-relative
- **E14** — CLI main(): sys.path hack + absolute worlds import -> package-relative registry
- **E14b** — default results.json next to module (site-packages!) -> cwd, BLOBKIT_RESULTS env override

### blobkit/assays_v1.py
- **E3** — absolute sibling import -> package-relative

### blobkit/genome.py
- **E1** — tree-walk CDATA (../composite/data) -> packaged blobkit/data; L0DIR removed
- **E2** — append_result default path: l0/results.json (tree) -> ./results.json (cwd)

### blobkit/metrics_v1.py
- **E4** — absolute-path sys.path hack to probes/search -> package-relative hier_metrics
- **E5** — self-import inside window_mask -> package-relative
- **E6** — in-function hier_metrics import -> package-relative

### blobkit/metrics_v2.py
- **E7** — two sys.path hacks + absolute imports of metrics_v1 -> package-relative
- **E8** — absolute hier_metrics import -> package-relative
- **E9** — in-function metrics_v1 import -> package-relative

### blobkit/operators.py
- **E22** — absolute sibling import -> package-relative

### blobkit/soup/sim_cpu.py
- **E11** — sys.path hack + absolute soup_sim import -> package-relative genome/.sim_v1

### blobkit/soup/sim_gpu.py
- **E15** — core.py module-level `import jax`/`HI` -> lazy _jax() helper; enable_x64 lazy
- **E16** — diffusion_E: lazy jnp
- **E17** — batch_keys: lazy jax/jnp
- **E18** — make_stepper: bind jax/jnp/HI lazily at build time (closures capture)
- **E19** — packing.py duplicate `import numpy as np` dropped in merged module
- **E20** — soup.py tree-walk sys.path hacks (l0/complexity + stage2/lib) -> package-relative sim_cpu/sim_v1; module-level jax import removed; packing/core imports now same-module (merged)
- **E21** — _attach_gpu: lazy jnp; enable_x64 now same-module (was .core import)

### blobkit/soup/sim_v1.py
- **E10** — sys.path hack to l0/stage2/lib -> package-relative genome

### blobkit/worlds.py
- **R1** — REWRITE: tree-walking builders -> packaged-data registry (load/names/WORLDS/KICKS/GT_SET; BLOBKIT_DATA override)

## Data

| blobkit data | source | note |
|---|---|---|
| `data/stamp_A4_dx05.npz` | `probes/blobs/composite/data/stamp_A4_dx05.npz` | byte-identical copy (genome.load_stamp_A4) |
| `data/worlds/m0.json` | built:complexity/worlds.py:m0 | ground truth, id `gt_m0`; built 2026-08-27 by tools/extract_worlds.py via the live tree builders (worlds.py + machinev3/lib.py + stage3 encounter jobs), genome_json round-trip — verified identical to the 2026-02-25 freeze `gpu/data/gt_worlds.json` |
| `data/worlds/m4.json` | built:complexity/worlds.py:m4 | ground truth, id `gt_m4`; built 2026-08-27 by tools/extract_worlds.py via the live tree builders (worlds.py + machinev3/lib.py + stage3 encounter jobs), genome_json round-trip — verified identical to the 2026-02-25 freeze `gpu/data/gt_worlds.json` |
| `data/worlds/xv.json` | built:complexity/worlds.py:xv | ground truth, id `gt_xv`; built 2026-08-27 by tools/extract_worlds.py via the live tree builders (worlds.py + machinev3/lib.py + stage3 encounter jobs), genome_json round-trip — verified identical to the 2026-02-25 freeze `gpu/data/gt_worlds.json` |
| `data/worlds/bf.json` | built:complexity/worlds.py:bf | ground truth, id `gt_bf`; built 2026-08-27 by tools/extract_worlds.py via the live tree builders (worlds.py + machinev3/lib.py + stage3 encounter jobs), genome_json round-trip — verified identical to the 2026-02-25 freeze `gpu/data/gt_worlds.json` |
| `data/worlds/pred.json` | built:complexity/worlds.py:pred | ground truth, id `gt_pred`; built 2026-08-27 by tools/extract_worlds.py via the live tree builders (worlds.py + machinev3/lib.py + stage3 encounter jobs), genome_json round-trip — verified identical to the 2026-02-25 freeze `gpu/data/gt_worlds.json` |
| `data/worlds/coex.json` | built:complexity/worlds.py:coex | ground truth, id `gt_coex`; built 2026-08-27 by tools/extract_worlds.py via the live tree builders (worlds.py + machinev3/lib.py + stage3 encounter jobs), genome_json round-trip — verified identical to the 2026-02-25 freeze `gpu/data/gt_worlds.json` |
| `data/worlds/mv3.json` | built:complexity/worlds.py:mv3 | ground truth, id `gt_mv3`; built 2026-08-27 by tools/extract_worlds.py via the live tree builders (worlds.py + machinev3/lib.py + stage3 encounter jobs), genome_json round-trip — verified identical to the 2026-02-25 freeze `gpu/data/gt_worlds.json` |
| `data/worlds/ds3_014.json` | `probes/blobs/l0/complexity/genomes_v2/ds3_014.json` | byte-decoded canonical JSON, id `ds3_014` |
| `data/worlds/ds3_017.json` | `probes/blobs/l0/complexity/genomes_v2/ds3_017.json` | byte-decoded canonical JSON, id `ds3_017` |
| `data/worlds/ds6_000.json` | `probes/blobs/l0/complexity/genomes_v2/ds6_000.json` | byte-decoded canonical JSON, id `ds6_000` |
| `data/worlds/g0_jit_11.json` | `probes/blobs/l0/deepsearch/deploy/seeds/g0_jit_11.json` | byte-decoded canonical JSON, id `g0_jit_11` |
| `data/worlds/engine_10748.json` | `probes/blobs/l0/stage3/engine_10748.json` | byte-decoded canonical JSON, id `engine_10748` |
| `data/worlds/rail_111_17.json` | `probes/blobs/l0/deepsearch/seeds/rail_111_17.json` | byte-decoded canonical JSON, id `rail_111_17` |
| `data/worlds/s2_128_26.json` | `probes/blobs/l0/deepsearch/seeds/s2_128_26.json` | byte-decoded canonical JSON, id `s2_128_26` |
| `data/worlds/s2_118_41.json` | `probes/blobs/l0/deepsearch/seeds/s2_118_41.json` | byte-decoded canonical JSON, id `s2_118_41` |
| `data/worlds/_extraction.json` | tools/extract_worlds.py | extraction receipt (source per world + KICKS at extraction time) |

Champion source notes: `ds3_014/ds3_017/ds6_000` are the complexity-battery
validation copies (`l0/complexity/genomes_v2/`), byte-identical to the
deepsearch deploy seeds except the deploy copies carry an extra `vtags` key
(deepsearch bookkeeping, not part of the certified genome). `g0_jit_11` exists
only under `l0/deepsearch/deploy/seeds/`. `s2_128_26.json` equals the
`s2_128_26_uni` genome inside `l0/stage2/merged_results.json` up to the `id`
field (seed file id `s2_128_26`, merged-results id `u`); machinev3's mv3 build
consumes the merged-results copy and is captured here as the built `mv3` world,
so both conventions are preserved.

`KICKS` (mv3 engine act kicked 0.5 px — its certified launch convention) is
carried verbatim into `blobkit.worlds.KICKS`.

## Promotion rule (future certified components)

A component enters blobkit only when ALL of:
1. **Certified upstream**: it has a lock/scorecard in the source tree (hash
   table or gate transcript) — blobkit packages certainties, not experiments.
2. **Verbatim + plumbing-only edits**: copies differ from source only by
   import/path edits, each marked `[blobkit edit E#]` inline and logged here
   with the exact old->new intent. Any numerics change = a NEW module name
   (metrics_v3, sim_cpu_v3, ...), never an in-place edit.
3. **Data extracted, not tree-walked**: no module may read outside the
   package dir (importlib/data/ + env overrides only).
4. **Parity-gated**: before the version bump, rerun VERIFY.md's battery —
   numerics parity vs the locked reference outputs (bitwise for simulators,
   field-by-field for metrics/funnel), fresh-venv install, lazy-GPU import.
5. **Lock table updated**: `_locks.json` regenerated, `verify_locks()` green,
   version bumped (patch = data-only additions, minor = new modules).

## Known non-goals (0.1.0)

- `soup/sim_gpu.py` merges blobgpu core+packing+soup; `anchors.py` (bond-anchor
  drivers) was NOT promoted (probe-grade, reads tree data).
- stage-3 `assays.py` V4 additions (a2_cross etc.) not promoted — they were
  certified for the stage-3 encounter screen only; promote separately if needed.
- funnel/sampler (G0 screens) not in scope for this brief; the V3 gate ran the
  tree funnel against packaged genomes instead.

## 0.2.0 — backend injection + shared sim driver (2026-08-28)

Design (fixed): share the science, duplicate the kernels, prove kernel
equality with gates, not shared code.
- L3 science (genome/metrics/assay decisions): single copy (was already true).
- L2 sim driver (chunk loop, record cadence, snapshot scheduling, early
  exits): single copy — NEW `soup/driver.py`.
- L1 physics kernels: scipy-FFT (`soup/sim_cpu.py`, LOCKED) and jax
  (`soup/sim_gpu.py`) — two implementations ON PURPOSE; equality via parity
  gates (VERIFY.md V2 / gpu GATES.md / VERIFY_V02.md G2).
- L3<->L2 interface: the 4-function namespace `init_soup/advance/
  snapshot_rec/save_run` == `blobkit.soup.backend.get_backend(name)`.

Verification transcript: `VERIFY_V02.md` (gates G1-G4, artifacts in
`verify_v02/`). The 0.1.0 verification (VERIFY.md) remains valid for all
files whose hashes did not change.

### New modules (0.2 lock entries)

| blobkit file | role | provenance |
|---|---|---|
| `blobkit/assay_v2b.py` | backend-injected assay entry: `run_assay_b(genome, backend=None, ...)` + `run_assay_gpu` | VERBATIM port of `assay_v2.run_assay` (LOCKED, untouched) with the sim namespace injected instead of hard-bound; shares `js`/`horizon_criteria`/constants by import. G1: bit-identical battery+horizon vs locked `run_assay` (m0 s7, ds3_014 s9, mv3 s1). Adds one non-science field: results row gains `backend` name. |
| `blobkit/soup/driver.py` | L2 shared sim driver: `run_chunks(worlds, steps_target, step_fn, pull_fn, record_fn, ...)` | Chunk-loop shell LIFTED from the pre-0.2 `sim_gpu.advance_gpu`/`advance_gpu_batch` (loop, REC record cadence, CREC/snapshot full-pull scheduling, early exits, `_t_stopped` contract, amortized wall). No numerics, no measurement code. Two 0.3 seams (design input, logged): `record_fn` is backend-provided (device-side reduction variant can slot in) and `reseed_hook` no-op stub (continuous batching). |
| `blobkit/deploy_tools.py` | fleet bundle generator: `make_bundle(out_dir, backend=, extra_seeds=)` + CLI | NEW. Emits wheel (or pip-installable `pkg/`) + adapted `pod_lib.py` + verbatim fleet scripts + shims + generated `pod_run.sh` (thread pins) + `island_config.template.json` (`sim_backend` field; lanes OFF) + seeds from the packaged registry. Retires the legacy tree-snapshot deploy bundle for FUTURE runs; the RUNNING CPU fleet and its deploy/ bundle are untouched. |
| `blobkit/data/fleet/pod_lib.py` | bundle template (adapted) | from `l0/deepsearch/deploy/pod_lib.py`; edits marked `[fleetbundle F1]` (imports genome/assay from the blobkit wheel) and `[fleetbundle F2]` (assay via `assay_v2b.run_assay_b(backend=sim_backend(cfg))`; `sim_backend` config helper; results rows carry `sim_backend`). Everything else verbatim. |
| `blobkit/data/fleet/{pod_gen,pod_worker,pod_smoke,merge_islands}.py` | bundle templates (verbatim) | byte-identical copies of the fleet-certified `l0/deepsearch/deploy/` scripts: pod_gen `f1015e176dde`, pod_worker `fb8e6e0205f5`, pod_smoke `d3851198f438`, merge_islands `315c1414c348`. |
| `blobkit/data/fleet/{funnel,sampler,ds2_ops}.py` | bundle templates (verbatim) | byte-identical copies of `deploy/lib/`: funnel `7d049f1219f8`, sampler `c65ca23aba63`, ds2_ops `c79ced9a00ab`. Certified for the fleet but NOT yet promoted to package modules (they keep flat `import genome` imports and ride as data; promotion = separate brief). `lib/genome.py` + `lib/operators_lib.py` in generated bundles are alias shims onto `blobkit.genome`/`blobkit.operators` (deploy copies were verbatim-identical to the packaged sources: `914fad08dffd`/`fcca88b546b1`, see 0.1 table). |

### Edits to existing files (0.2)

- **E23** — `soup/sim_gpu.py`: `advance_gpu` + `advance_gpu_batch` chunk loops
  replaced by calls into `driver.run_chunks` (new `_record_host` record_fn +
  `_driver_kw` plumbing; `from . import driver as DRV`). NO numerics change:
  stepper, packing, `_pull`, init fns byte-untouched; G2 gates bit-identical
  record streams + final fields vs the pre-refactor module (CPU-JAX f64;
  GPU-device rerun pending next pod deployment). Driver unifications that are
  invisible to records (skipped redundant pulls at chunk boundaries) are
  documented in driver.py's docstring.
- **E24** — `soup/backend.py`: gpu `init_soup` wrapper now accepts+ignores
  `workers` AND arbitrary future CPU-only kwargs (`**cpu_only`) — the pod
  fiasco's API-drift lesson, enforced in-package. Backend namespaces also
  used by `assay_v2b` (results row `backend` field).
- `__init__.py`: `__version__` 0.1.0 -> 0.2.0; `assay_v2b`, `deploy_tools`
  registered as lazy submodules.
- `pyproject.toml`: version 0.2.0; package-data + `data/fleet/*`.
- `_locks.json`: regenerated. 28 hashes unchanged from 0.1.0; re-locked:
  `soup/backend.py` (E24), `soup/sim_gpu.py` (E23); added: the 11 new files
  above (n_checked 30 -> 41).

### CPU advance: driver adoption deferred (relock note)

`soup/sim_cpu.py` is LOCKED (upstream soup_sim_v2 `8541dedd…`) and was NOT
touched in 0.2: its `advance` keeps the original inline chunk loop, which the
driver's shell is provably equivalent to (it was lifted from the GPU port of
that same loop; G2). At the NEXT RELOCK WINDOW (first version that re-locks
sim_cpu for its own reasons) `sim_cpu.advance` adopts `driver.run_chunks`
with a CPU step_fn/pull_fn, gated by the same bitwise battery (V2.0-style)
before the swap. Until then the CPU loop is the one intentional L2
duplicate, and it is frozen.

### Deploy bundles: legacy pattern retired for future runs

Future fleets: `python -m blobkit.deploy_tools <out_dir> [--backend gpu]`.
Generated `pod_run.sh` pins OMP/OPENBLAS/MKL/VECLIB/NUMEXPR to 1 thread
(process-level parallelism only — the thrash lesson). Generated
`island_config.template.json` defaults `l192_per_gen=0, longh_top=0` with a
note pointing the L192/long-horizon lanes at the GPU backend
(`sim_backend: "gpu"`); set 2/3 to restore legacy CPU-lane behavior.
The RUNNING fleet keeps its frozen `deploy/` bundle to completion.

## Check taxonomy (adopted 2026-08-28)


A) POOR MAN'S CI (fast, runs everywhere, forever):
   - verify_locks(): hash table check, <1s, at install + before every run
   - import/version smoke: blobkit.__version__, backend surface exists
   -> These stay in every pod bootstrap script permanently. Cost ~seconds.

B) ONE-TIME SOFTWARE CERTIFICATION (per code version, then done):
   - v02: G1 bitwise interface identity, G2 driver refactor identity
   - v03: V1 batched-ladder decision identity, (V2 local throughput reference)
   - device gates when an engine first meets real hardware class (D1/D3 7-world
     + champion distributional)
   -> Run ONCE per (code version x engine class). 0.3's certification does NOT
      re-run 0.2's gates except transitively (locks prove 0.2 files unchanged).
      A future H100->H200 or CUDA-major bump = one cheap re-gate of the device
      suite, not the full ladder.

C) PER-DEPLOY BEST-PRACTICE CHECKS (every fresh pod, ~2-5 min):
   - locks + import smoke (A)
   - pod_smoke.py: 3-candidate mini-gen against the packaged registry (catches
     env/driver/CUDA/wheel mismatches on THAT box)
   - one known-anchor world (m0 s7 = 2.8) as a numerics canary
   -> Cheap insurance per box; NOT re-certification.

WHAT WAS CONFLATED IN OUR FLOW (honest): the research run kept absorbing (B)
because the software was being built DURING the campaign. Post-0.3, the split
is clean: B is done offline once, C is scripted into make_bundle's generated
bootstrap, and research runs start from a certified wheel + 2-minute deploy
check, no gate theater.

## 0.3.0 — batched-ladder assay driver (2026-08-28)

The mode the GPU port was built for (docs/blobs/accelerating-blobs.html):
a generation is ONE tensor. 0.2 gave future fleets the GPU per single world
(kernel-level wins only: device-side 250-step chunk loop, donate_argnums,
precomputed exp(-D k^2 dt), unbroken XLA fusion — the deployed 3-pod
continuation runs this and shows GPU 99%-util-on-tiny-kernels, ~80-100
min/gen). 0.3 adds the population-level wins the optimization log certified
and the deployed mode misses: #1 batched population tensor (one jit for B
worlds), #2 activator-only pulls on the record path, #3 threaded host
records + JAX async-dispatch overlap. CUDA graphs stay rejected; the kernel
is cuFFT-bound (roofline) — wins come from batching + host overlap, not
micro-tuning.

### New modules (0.3 lock entries)

| blobkit file | role | provenance |
|---|---|---|
| `blobkit/assay_batch.py` | rung-synchronized batched ladder: `run_assay_batch(jobs) -> [out...]` | NEW driver layer. Stepping = the CERTIFIED batch machinery only (`init_soup_gpu_batch`/`advance_gpu_batch`/`_attach_gpu`/`_pull`; zero new stepping code). Science = LOCKED imports (`metrics_v2.full_battery`, `assay_v2.horizon_criteria`, `T0_DEFAULT/T_CAP`, `lean_summary`); decision branch is a line-for-line mirror of `assay_v2b.run_assay_b`. Per-lane t0/cap (confirm floors / longH caps) on the shared doubling grid; repack at rung boundaries with B padded to {4,8,16,32}; module-level stepper cache (jit stability); per-lane battery errors contained (`assay_error` rows, batch survives). Results rows = `run_assay_b` schema + `lane`/`batched` + provenance (`blobkit`/`locks`/`engine`). |
| `blobkit/data/fleet/pod_worker_batch.py` | bundle template: batched shard evaluator | NEW. Emitted by `make_bundle(backend="gpu_batch")`. One call = a whole tag's shards -> funnel/size-cap prefilter (verbatim `pod_lib.evaluate` rules) -> grouped by (L, doubling-grid class) -> `run_assay_batch` (<= `batch_lanes` lanes/call) -> rows identical to `pod_lib.evaluate` + lane metadata. Seeds are per-lane, so s1 screens + s2/s3 confirms share tensors. |
| `blobkit/data/fleet/pod_gen_batch.py` | bundle template: 0.3 driver overlay (async confirms + g0 import) | NEW. `collect <gen>`: folds gen<N pending s2/s3/lane confirm shards into gen N's sweep (island_config `confirms:"async"`; one batch call/gen, elites enter the block library one gen late — MAP-Elites order-tolerant). `g0import <archive>`: seed the island archive from a fully-confirmed donor (island_config `g0:"import"`; refuses to overwrite a non-empty archive). `pod_gen.py` itself stays byte-verbatim. |

### Edits to existing files (0.3)

- **E25** — `deploy_tools.py`: `make_bundle` backend choice gains
  `"gpu_batch"`: emits `pod_worker_batch.py` + `pod_gen_batch.py` +
  generated `pod_run_batch.sh` (batched main loop; sync and async-confirm
  paths; g0-import note) and extends the config template
  (`batch_lanes=32`, `batch_dtype="f32"`, `battery_procs=8`,
  `confirms="sync"`, `g0="eval"`). cpu/gpu bundles byte-unchanged.
- **F3** — `data/fleet/pod_lib.py`: `sim_backend()` maps `"gpu_batch"` ->
  `"gpu"` namespace for single-world paths (pod_smoke, legacy pod_worker);
  the batched ladder itself enters via `pod_worker_batch` ->
  `blobkit.assay_batch`. No other changes.
- `__init__.py`: `__version__` 0.2.0 -> 0.3.0; `assay_batch` registered as
  lazy submodule.
- `pyproject.toml`: version 0.3.0.
- `_locks.json`: regenerated (44 files; re-locked deploy_tools.py +
  data/fleet/pod_lib.py; added the 3 new files).

### Design notes (assay_batch)

- RUNG SYNC: all lanes double together (T = t0_min * 2^k); a lane whose t0
  floor is above the current rung rides the tensor undecided (chunk-safe
  continuation = its record stream is unchanged). Lanes exit individually;
  survivors repack; ballast rows (state duplicates, never recorded) pad B
  to the next ladder size. Padding inertness + per-world absolute-step
  threefry folds + bit-preserving host roundtrips make every lane's
  trajectory equal its single-world run bit-for-bit (same backend/dtype).
- DECISION FIDELITY: no criterion, constant, or branch is reimplemented —
  the module imports the locked functions and mirrors `run_assay_b`'s loop
  body per lane (V1-gated, see VERIFY_V03.md).
- KNOWN non-science divergences vs singles rows (documented in module
  docstring): `wall_total` shares the batch clock, `wall_sim` is the
  driver's amortized per-world share, `save_npz` becomes `save_npz_map`.
- The 0.2 driver seams this consumes: `record_fn` stays host-side verbatim
  `_record`; `reseed_hook` remains unused (continuous batching stays a
  future brief — rung-synchronized repack was chosen over mid-flight
  refill for decision-grid identity).

### Verification (VERIFY_V03.md, artifacts verify_v03/)

| gate | what | result |
|---|---|---|
| W1 | mechanical smoke: 2 m0 lanes f32 + pad-to-4 ballast + pool battery (interest 2.80 == locked m0 ref); 4-lane heterogeneous covered by V1a | **PASS** (W1.json, smoke4.txt) |
| V1a | decision identity f32: ONE batch [m0 s7, m4 s1, mv3 s1, bf s1] t0=1250 cap=2500 vs run_assay_b singles (same backend+dtype) — bitwise canon | **PASS 4/4 bitwise** |
| V1b | f64 [m0 s7, mv3 s1] t0=2500 cap=5000 | **PASS 2/2 bitwise** |
| V1c | f32 [m0 s7, mv3 s1] B_pad=(2,) ballast path | **PASS 2/2 bitwise** |
| V1d | f32 per-lane t0 floors force multi-rung: repack 2->1 under live lane, mv3 rides its floor to a 5000 decision | **PASS 2/2 bitwise** |
| V1e | as V1d, repack disabled (exited row = inert ballast) | **PASS 2/2 bitwise** (mv3 out identical to V1d's — repack and ballast paths agree bit-for-bit) |
| V2 | throughput union4 mixed lanes (stratified T_used) batched vs sequential singles + PERF_REFERENCE.json emission (deploy-smoke perf floor). LOCAL CPU-JAX = reference only (batching multiplies CPU FLOPs ~linearly; understates GPU win); BINDING gate = same script `--device H100` on the pod (target >=2.5x; post ref 396 w/h pop-96) | local ref recorded: 0.7x (8 lanes; batch 5.1 w/h vs seq 7.2 w/h — CPU pays the padding FLOPs, no launch-overhead pool to amortize; anticipated). Decisions 7/8 (1 f32 engine-noise threshold flip at T=2500; distribution-gated regime). PERF_REFERENCE.json emitted (binding=false). BINDING: `v2_run.py --device H100` on the pod |
| V3a | relock: 44 files (41 + 3 new; re-locked deploy_tools + fleet pod_lib), clean import verify_locks ok | **PASS** (V3a.json) |
| V3b | fresh-venv (`/tmp/bk03fresh`) pip install 0.3.0: locks green, run_assay_batch present, jax stays lazy | **PASS** (V3b.log) |
| V3c | gpu_batch bundle emission from the fresh venv + offline unit runs (grouping, async collect, g0import) | **PASS** (V3c.json) |

## 0.3.1 — GPU teardown hardening (2026-08-28, hotfix)

Fleet-blocking bug caught at device gates: `run_assay_batch` hung at
teardown on the GPU pod. py-spy: MainThread in `executor.shutdown->join`,
worker thread in `terminate_broken->...->queue join` — the battery pool
BROKE (fork-after-jax/CUDA-init killed a worker) and a broken executor's
`shutdown(wait=True)` deadlocks on its feeder queue. Local CPU boxes never
saw it (fork works there).

Fixes (assay_batch.py + new `_batteryproc.py`; no science changes):
- battery pool now uses the SPAWN mp context (mandatory; fork after CUDA
  init is undefined);
- the pool worker moved to `blobkit/_batteryproc.py`, a deliberately tiny
  module whose import chain is numpy/scipy-only: spawned workers import the
  worker's module — they must NEVER pull jax/sim_gpu;
- `_shutdown_pool`: checks the executor's broken flag UP FRONT (a deadlock
  hangs rather than raises) and falls back to
  `shutdown(wait=False, cancel_futures=True)`;
- broken pool mid-run: the rung finishes serially in-process (correctness
  first), the pool is retired non-blockingly, remaining rungs run inline.

Tests (dev venv): spawn-pool battery == inline battery on a real record;
simulated-broken-flag shutdown returns promptly; sabotaged-pool end-to-end
(`BrokenProcessPool` on first map) -> serial fallback -> results correct ->
non-waiting shutdown. V1a rerun on 0.3.1: PASS 4/4 bitwise (V1a.json).
Locks: 45 files (re-locked assay_batch.py, added `_batteryproc.py`);
verify_locks green on clean import; version 0.3.1.
