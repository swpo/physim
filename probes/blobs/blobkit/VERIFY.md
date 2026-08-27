# blobkit VERIFY — packaging verification transcript

Date: 2026-08-27. Tree: `/Users/spoho/Documents/prime/test/physim` @ git `b671958`.
Fresh venv: `/tmp/blobkit_v1_venv` (uv, **python 3.11.14, numpy 2.4.6, scipy 1.17.1**).
Source-tree env for cross-checks: python 3.13.5, numpy 2.4.0, scipy 1.16.3.
All driver scripts + raw outputs: `/tmp/blobkit_v3/` (copies of key JSON results in `verify/`).

## V1 — fresh-venv install PASS

```
uv venv -p 3.11 /tmp/blobkit_v1_venv
uv pip install --python .../bin/python ./probes/blobs/blobkit
python -c "import blobkit; blobkit.verify_locks(); from blobkit.worlds import load; g=load('m0')"
-> version: 0.1.0 | locks ok: True n_checked: 30 | m0 id: gt_m0 acts: 1 chans: 2
```

- All 13 submodules import clean (`blobkit.{genome,assays_v1,metrics_v1,hier_metrics,metrics_v2,assay_v2,worlds,operators,soup,soup.sim_v1,soup.sim_cpu,soup.sim_gpu,soup.backend}`).
- Wheel audit: `pip wheel` -> 36 entries; all 15 world JSONs + `_extraction.json` + `stamp_A4_dx05.npz` + `_locks.json` present. Nothing missing.
- `genome.load_stamp_A4()` resolves from packaged data (u0 = -0.70354 ✓).
- Lock-drift drill: appending one comment line to installed `metrics_v2.py` ->
  `verify_locks()` flags exactly that file, raises `ImportWarning` (and
  `RuntimeError` under `strict=True`); restoring the byte content goes green again.
- CLI: `python -m blobkit.assay_v2 m0 --seed 7 --t0 500 --cap 1000` runs,
  prints the locked summary line, appends a `kind="assay_v2"` row to
  `$BLOBKIT_RESULTS` (row verified).
- Functional smokes: `operators.mutate`/`_block_merge` produce validating
  genomes; `assays_v1.a1_poke(m0)` -> class `persist`.

## V2 — numerics parity vs the locked reference PASS

Reference = `probes/blobs/l0/complexity/` locked artifacts
(`v2_scores_all.json`, `runs_v2/*.npz`, results.json rows; lock
`v2_lock_hashes.txt`).

### V2.0 bitwise simulator parity (strongest gate)

Same-venv, tree modules (their own interface) vs blobkit modules, same seeds:

| world | seed | T | field tensor F | records (ts/blobs/mass/patches/orgs/memf/snaps) | battery interest |
|---|---|---|---|---|---|
| m4 | 1 | 500 | bitwise == | all == | 11.665401 == |
| ds3_014 | 9 | 750 | bitwise == | all == | 30.748217 == |
| mv3 (kicked) | 1 | 750 | bitwise == | all == | 37.728556 == |

Kicked-IC cross-check (mv3 KICKS wiring): tree `init_soup(kicks=…)` and blobkit
produce bit-identical initial fields.

### V2.0b CROSS-ENV bitwise parity

blobkit in the fresh venv (py3.11/np2.4.6) re-simulated m4 seed 1 to T=2500 and
was compared against the LOCKED archived npz (`runs_v2/v2_m4_s1.npz`, produced
2026-08-24 on py3.13/np2.4.0): every record stream bit-identical
({"T": true, "ts": true, "blobs": true, "mass": true, "patches": true, "orgs": true, "memf": true, "snaps": true}). The packaged numerics are stable across the
python/numpy versions that matter for deployment.

### V2.1 assay_v2 via blobkit — m0 seed 7 (brief target: 2.8 @ 2500 exact)

```
blobkit assay_v2.run_assay(worlds.load("m0"), seed=7)
-> interest 2.80 @ T=2500, why=static, C1..C8 = 0.05/0/0/0.25/0/0/0/0
reference v2_scores_all.json m0 (all seeds): int2 2.8 @ 2500        EXACT ✓
```

### V2.2 battery recompute over the ENTIRE locked run archive — 31/31 EXACT

Every `runs_v2/v2_*.npz` (10 worlds × seeds 1-3 + ds3_014 s9) re-scored with
`blobkit.metrics_v2.full_battery` + packaged genomes, compared field-by-field
(int2, T, all 8 C components, nsi, stages, mem grade, org_model, box flags)
against `v2_scores_all.json`: **31/31 rows match exactly**, including
`ds3_014_s9 -> 77.06 @ T=10000` (the locked champion reference).

### V2.3 assay_v2 via blobkit — ds3_014 seed 9 full adaptive run (brief target: T=10000, interest in [74, 81])

```
blobkit assay_v2.run_assay(worlds.load("ds3_014"), seed=9)
trajectory: 2500 -> 66.27 (fired a_mem+b_org) -> 5000 -> 73.34 (fired b_org)
            -> 10000 -> 77.06 (nothing fired, converged), n_extensions=2
final: T=10000, interest 77.06, wall 1945 s
reference (v2_scores_all.json ds3_014_s9): int2 77.06 @ T=10000     EXACT ✓
acceptance band [74, 81]                                             PASS ✓
C: 0.55/0.6468/0.6301/1.0/0.787/1.0/0.9053/0.5  (== reference to 4 dp)
flags: box_limit true, span 1.0, persist 0.864  (== reference)
```

The adaptive horizon fired the same criteria at the same checkpoints as the
locked validation runs (a_mem+b_org @2500, b_org @5000, converge @10000) —
the packaged assay reproduces the reference decision path, not just the score.

## V3 — worlds registry vs source-tree builds PASS (15/15 identical, funnel field-by-field)

Both drivers ran in the same interpreter: the tree side rebuilt every world
with the CURRENT builders (`complexity/worlds.py`, incl. `machinev3/lib.py`
`build_world("mimic", 0.6)` for mv3 and the stage-3 encounter extraction for
pred/coex) and byte-decoded the champion/part JSONs; the blobkit side used
`blobkit.worlds.load` only. For every world: full genome deep-compare AND the
G0 funnel record (`funnel.funnel(g)`: g0b discs, g0a margin + k, tails,
wavelengths, stage) compared field by field.

| world | genome identical | funnel identical | stage | g0a margin |
|---|---|---|---|---|
| m0 | ✓ | ✓ | pass | -0.301553 |
| m4 | ✓ | ✓ | pass | -0.191274 |
| xv | ✓ | ✓ | pass | -0.201070 |
| bf | ✓ | ✓ | pass | -0.005000 |
| pred | ✓ | ✓ | pass | -0.006693 |
| coex | ✓ | ✓ | pass | -0.008006 |
| mv3 | ✓ | ✓ | pass | -0.181141 |
| ds3_014 | ✓ | ✓ | pass | -0.007469 |
| ds3_017 | ✓ | ✓ | pass | -0.005000 |
| ds6_000 | ✓ | ✓ | pass | -0.004566 |
| g0_jit_11 | ✓ | ✓ | pass | -0.007469 |
| engine_10748 | ✓ | ✓ | pass | -0.181141 |
| rail_111_17 | ✓ | ✓ | pass | -0.007469 |
| s2_128_26 | ✓ | ✓ | pass | -0.311916 |
| s2_118_41 | ✓ | ✓ | pass | -0.299334 |

Total field diffs: **0**. KICKS dict identical. Additionally the 7 packaged GT
worlds are byte-comparable (json-equal) to the independent 2026-02-25 freeze
`gpu/data/gt_worlds.json`, and `gpu/tests/gt_worlds.py check_vs_builders()`
confirmed frozen==live builders on this tree before extraction.

## V4 — GPU backend: lazy import PASS (no GPU locally; execution skipped as instructed)

In the fresh venv (jax NOT installed):
- `import blobkit.soup.sim_gpu` succeeds (module import is jax-free).
- `get_backend("gpu")` builds the namespace without importing jax.
- Calling any GPU entry point (`batch_keys`, `init_soup`) raises
  `ImportError: blobkit.soup.sim_gpu needs jax. Install the gpu extra: pip
  install 'blobkit[gpu]' (or jax[cuda12]==0.4.38).`
- GPU numerics themselves are unchanged from the gate-certified blobgpu
  modules (see `probes/blobs/gpu/GATES.md`); the merge edits E15-E21 touch
  imports only (MANIFEST). Re-run `gpu/tests/gate_parity.py`-equivalents on
  the next pod deployment as usual.

## Environment note

The fleet reference results were produced on py3.13.5/numpy 2.4.0; this venv
is py3.11.14/numpy 2.4.6. V2.0b shows the locked kernel is BITWISE stable
across that gap (m4 s1, 125k steps, every record stream). Parity should be
re-gated per V2.1/V2.2 whenever numpy majors change.

## Verdict

| gate | result |
|---|---|
| V1 fresh-venv pip install + verify_locks + worlds.load | **PASS** |
| V1b lock-drift ImportWarning / strict RuntimeError / SKIP env | **PASS** |
| V1c wheel data audit (15 worlds + stamp + lock table) | **PASS** |
| V2.0 bitwise sim parity (m4, ds3_014, mv3; state+records+battery) | **PASS** |
| V2.0b cross-env bitwise vs locked npz (np 2.4.0 -> 2.4.6) | **PASS** |
| V2.1 m0 seed 7 == 2.8 @ 2500 | **PASS (exact)** |
| V2.2 recompute vs v2_scores_all.json | **PASS 31/31 exact** |
| V2.3 ds3_014 seed 9: T=10000, interest in [74,81] | **PASS (77.06, exact vs ref)** |
| V3 worlds registry == source-tree builds (genome + funnel) | **PASS 15/15, 0 field diffs** |
| V4 sim_gpu lazy import without jax | **PASS** (GPU execution skipped: no local GPU) |

blobkit 0.1.0 is certified equivalent to the source-tree blob core.
Raw artifacts: `verify/*.json` (this repo) and `/tmp/blobkit_v3/`.
