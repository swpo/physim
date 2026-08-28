
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
| V2 | throughput union4 mixed lanes (stratified T_used) batched vs sequential singles + PERF_REFERENCE.json emission (deploy-smoke perf floor). LOCAL CPU-JAX = reference only (batching multiplies CPU FLOPs ~linearly; understates GPU win); BINDING gate = same script `--device H100` on the pod (target >=2.5x; post ref 396 w/h pop-96) | local run in flight at packaging time (V2.json/V2.log land in verify_v03/); binding H100 run = next pod |
| V3a | relock: 44 files (41 + 3 new; re-locked deploy_tools + fleet pod_lib), clean import verify_locks ok | **PASS** (V3a.json) |
| V3b | fresh-venv (`/tmp/bk03fresh`) pip install 0.3.0: locks green, run_assay_batch present, jax stays lazy | **PASS** (V3b.log) |
| V3c | gpu_batch bundle emission from the fresh venv + offline unit runs (grouping, async collect, g0import) | **PASS** (V3c.json) |
