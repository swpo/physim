# blobkit VERIFY_V02 — 0.2.0 gate transcript (backend injection + shared sim driver)

Date: 2026-08-28. Package: `probes/blobs/blobkit` 0.1.0 -> 0.2.0 (additive;
running CPU fleet + its deploy/ bundle untouched).
Dev venv: `/tmp/bk02venv` (py3.11.14, numpy 2.4.6, scipy 1.17.1, jax 0.4.38 CPU).
Fresh-install venv: `/tmp/bk02fresh`. Artifacts: `verify_v02/`.
Pre-refactor baselines: `/tmp/bkpre/blobkit_pre` (full 0.1 package copy),
`/tmp/sim_gpu_pre.py` — both sha-verified == 0.1 locked `sim_gpu.py`
(`c148457699f1`).

## Gate table

| gate | what | result |
|---|---|---|
| G1 | interface identity (CPU): `assay_v2b.run_assay_b(g, backend=cpu)` vs LOCKED `assay_v2.run_assay` — full battery + horizon, bitwise (wall fields stripped) | **PASS 3/3** |
| G2 | driver refactor identity (CPU-JAX f64): sim_gpu-with-driver vs pre-refactor copy — exact record streams + final F | **PASS 2/2** |
| G3 | lock integrity: relock 41 files, verify_locks green, drift drill | **PASS** |
| G4 | fresh-venv install 0.2.0 + make_bundle smoke (pod_smoke 3 candidates, cpu backend) | **PASS** |

**Caveat (by design, no local GPU): G2 proves refactor-identity on the CPU-JAX
backend only. The GPU-DEVICE gates (blobgpu GATES.md parity battery + this G2
on-device) rerun at the next pod deployment before any GPU-backed production
run.**

## G1 — backend-injection identity (bit-identical assay)

`run_assay_b` is a verbatim port of the locked `run_assay` with the sim
namespace injected (`backend=None -> get_backend("cpu")`). Comparison:
`json.dumps(js(out), sort_keys=True)` over the ENTIRE battery dict (C, D,
interest, flags, horizon decisions/trajectory, summary), wall-clock fields
stripped. Driver: `verify_v02/g1_run.py`; results `G1_<world>_s<seed>.json`.

| world | seed | interest | T_used | why | bitwise | locked ref |
|---|---|---|---|---|---|---|
| m0 | 7 | 2.8000000000000003 | 2500 | static | **==** | 2.8 @ 2500 (v2_scores) ✓ |
| ds3_014 | 9 | 77.0636234293702 | 10000 | converged | **==** | 77.06 @ 10000 ✓ |
| mv3 (kicked) | 1 | 53.426246534614485 | 20000 | cap | **==** | 53.43 @ 20000 ✓ |

Decision paths reproduced exactly (ds3_014: a_mem+b_org @2500 -> b_org @5000
-> converged @10000; mv3: c_acf @2500 -> b_org @5000/10000 -> cap @20000).
The one intentional addition: the results-row (`results_path`) gains a
`backend` field — not part of the returned battery, G1-invisible.

## G2 — shared driver refactor identity (CPU-JAX, f64)

`soup/driver.py` (L2) now owns the chunk loop; `sim_gpu.advance_gpu` /
`advance_gpu_batch` are shells over `driver.run_chunks` (edit E23). Stepper,
packing, `_pull`, init fns byte-untouched. Comparison vs `/tmp/bkpre`
pre-refactor module, dtype f64, chunked continuation 250tu -> 500tu
(exercises record cadence, CREC/snapshot scheduling, chunk boundaries):
exact structural compare (bitwise for every array) over
ts/blobs/mass/ct/patches/orgs/memf/snaps/T/status/t_step (+ final F tensor,
single case). Driver: `verify_v02/g2_run.py`; result `G2_driver_identity.json`.

| case | worlds | mode | match |
|---|---|---|---|
| A | m4 s1 | advance_gpu, single, +final F | **all ==** |
| B | m4 s1 + mv3 s1 (kicks) | advance_gpu_batch, overlap=True | **all ==** |

Contract audit (record-failure `_t_stopped`, recorded_at ordering, batch
t_step finalization, redundant-pull unification): `driver_contract_audit.txt`.
0.3 seams left in the driver per design input: backend-provided `record_fn`
(device-side reduction slot) and `reseed_hook` no-op stub (continuous
batching). Not implemented — seams only.

## G3 — lock integrity

`_locks.json` regenerated: 28 hashes unchanged from 0.1.0; re-locked
`soup/backend.py` (E24 workers-tolerant gpu init), `soup/sim_gpu.py` (E23);
added 11 files (assay_v2b, soup/driver, deploy_tools, data/fleet/* templates).
n_checked 30 -> 41; `verify_locks()` green in dev venv AND fresh venv.
Drift drill (scratch copy): appending one comment to installed
`soup/driver.py` -> flags exactly that file, ImportWarning fires,
`strict=True` raises RuntimeError; restore -> green. `G3_locks.json`.

## G4 — fresh venv + fleet bundle smoke

`python -m blobkit.deploy_tools /tmp/fleetbundle` (module CLI) from the
relocked package:
- receipt: wheel `blobkit-0.2.0-py3-none-any.whl`, 16 seeds, 124 files,
  `bundle_hashes.txt` manifest (`G4_bundle_receipt.json`).
- fresh venv `uv venv -p 3.11` + wheel install: `blobkit 0.2.0`,
  `verify_locks() ok n=41`; `assay_v2b`/`soup.driver`/`deploy_tools` import;
  `get_backend("gpu")` builds WITHOUT jax; calling its `init_soup` (with the
  workers kwarg + an unknown future kwarg accepted) raises the clean
  ImportError with install advice.
- bundle `pod_smoke.py` with the fresh venv python, `sim_backend: "cpu"`
  (island_config from generated template — lanes OFF fields present):
  3/3 candidates ok, archive inserts ok, **SMOKE PASS rc=0**
  (`G4_formal.log`; first-generation preview run in `G4_preview.log`):

| cand | status | interest | T | cell |
|---|---|---|---|---|
| smoke_m0 | ok | 2.8000000000000003 | 2500 | 1\|constant\|still\|frozen\|s1\|g0 |
| smoke_mint | ok | 36.398982074406604 | 5000 | 1\|constant\|mobile\|liquid\|s1\|g2 |
| smoke_elite | ok | 74.2048566698709 | 5000 | 4\|grow\|rotor\|liquid\|s2\|g2 |

(smoke_mint/smoke_elite are rng/op-dependent fresh candidates, not locked
references; the locked-reference leg is smoke_m0 == 2.8 exactly.)
Generated `pod_run.sh` carries the thread-pin exports (OMP/OPENBLAS/MKL/
VECLIB/NUMEXPR=1); config template ships `sim_backend:"cpu"`,
`l192_per_gen:0`, `longh_top:0` with lane->GPU pointer notes.

## Wall notes

run_assay_b CPU walls tracked ref within noise (m0 155s vs 102s ref on a
contended box; ds3_014 2830s vs 3217s; mv3 3466s vs 4364s — b-side ran while
fewer background jobs were live). No systematic overhead from the namespace
indirection.

## Pending on next pod deployment (GPU device)

1. blobgpu GATES.md parity battery on-device (unchanged since 0.1).
2. G2 rerun on-device (driver refactor identity with a real GPU).
3. `run_assay_gpu` descriptor-level check vs CPU seeds (noise streams differ
   by design; expect seed-level equivalence, not bitwise).
