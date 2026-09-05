# Safe v3 film recovery helper

This tool captures a **GPU re-simulation / replay**. It does not recover the
exact original trace. It does not rank candidates, recompute scores, modify
h9, run an assay battery, or change the search archive.

## Validation status

- Local metadata, file-integrity, and native recorder/driver tests passed.
- The tests use a **fake stepping seam**, not a GPU or physical simulation.
- Local preflight passed on an actual spatial screen and its soup confirmation.
- **GPU smoke is still required. No real GPU capture has been certified here.**
- Root approved a 50tu smoke instead of 10–20tu because the public native
  advance API requires 25tu CREC-aligned endpoints. No driver workaround is used.

## Explicit selection

Use a JSON object with `schema: "v3-film-replay-v1"` and a nonempty `items` list.
The helper processes only those items. Root owns the final selection: about
six films TOTAL across both islands, not six per island. `selection.example.json`
is a template, not a candidate recommendation.

Each reference item needs:

```json
{
  "name": "i1-chosen-confirm",
  "island_dir": "/home/ubuntu/isl1",
  "island": 1,
  "cand": "EXACT_SELECTED_CAND",
  "phase": "seed3",
  "seed": 959,
  "results_path": "out/results.json",
  "original": {
    "dtype": "f32",
    "environment": {
      "evidence": "Archived island config and row; historical runtime versions unknown"
    }
  }
}
```

- `name` is a unique safe output name. No suffix stripping or genome-level dedup.
- `island_dir` is the original worker's `HERE` directory or its relocated copy.
  Job `ic_npz` paths are relative to this root, NOT to the shard directory.
- `phase` matches job `kind`, not row `kind`. `row.kind` is usually `ds2_eval`.
- Seed is the actual integer RNG seed, not the number in `_s2` or `_s3`.
  Screen jobs often omit seed; the matching island config supplies it.
- `results_path`, `config_path` (default `island_config.json`), `jobs_dir`
  (default `out/jobs`), and `job_path` are relative to `island_dir` unless absolute.
- Matching uses exact island/cand/phase/seed. Multiple result rows require
  `row_index`. Differing matching jobs require `job_path` and optional `job_index`.
  Identical shard copies are recorded and deduplicated.
- Job discovery ignores only structurally valid AppleDouble `._*.json` sidecars
  (macOS extended-attribute files). Their paths/hashes are recorded. A hidden
  filename alone is not enough: malformed sidecars and corrupt real JSON shards
  still fail. All JSON read/decode errors include the resolved file path.
- Optional `row_sha256`, `genome_sha256`, and `ic_sha256` pin expected hashes.
  Row/genome hashes use sorted, compact JSON, `ensure_ascii=True`, no NaN.
- Instead of looking up a row or job, supply frozen **complete** `row` and/or
  `job` objects inside the item. They must still match. Inline objects are
  explicitly identified as supplied evidence, not silently discovered data.
- Original `T_used` comes from the selected row. There is no 10,000tu default,
  no 20,000tu cap, no using `job.t0` as a starting time, and no partial success
  labeled as a full film. Only original `status: "ok"` rows are accepted.
- Production snapshots are `0, 250, 500, ...` through original `T_used`.
  A final off-250 endpoint is also included if it is on the 25tu CREC grid.
  Other endpoints fail preflight rather than being silently rounded.

### Spatial IC versus soup

The exact job's `ic_npz` decides the IC kind. A truthy `row.ic_merge` must
agree with an available spatial IC. The full `ic` array must be finite,
floating, and `(na+nc, N, N)`, where `N=L/0.5`. The native `ics=[ic]` hook
applies it **before device packing** and casts to the explicit simulation dtype.

A spatial-origin candidate's seed-2/seed-3 confirmation normally has **no**
`ic_npz` and therefore replays as soup. Do not attach the base screen's IC.
For example, the harvested `p1g2_051` screen is spatial, but its
`p1g2_051_s3` job is soup with seed959. Genome `id` can remain the base name.

If the exact IC is missing, the item gets a `skipped_missing_ic` report and the
invocation exits nonzero. It is never filmed as soup. A relocated absolute IC
requires both `ic_path` and its expected `ic_sha256`. No basename search or
parent reconstruction is attempted. Old atlas absolute IC paths need this
explicit relocation. Ordinary run NPZ activator snapshots and coarse memory
fields are not a replacement for a missing full-state IC.

### Original backend and dtype

- `batched=true` identifies GPU execution in these fleet rows.
- Early `ic_merge=true, batched=false` rows are CPU fallback executions even
  when their inherited `sim_backend` says `gpu_batch`.
- CPU originals are refused unless that item has `allow_backend_change: true`.
  Their manifests then flag CPU->GPU noise-stream change. This is a new GPU
  realization, not a CPU trace recreation or a score reconfirmation.
- Simulation dtype must resolve explicitly to `f32` or `f64` from the row,
  `original.dtype`, or matching batch config. Conflicts fail. The known CPU
  IC fallback has an evidenced f32 default.
- An IC file or native recorded snapshot being float64 does NOT imply f64
  simulation. The original GPU IC can be f64 on disk and cast to f32 in the engine.
- `original.L`, `original.T_used`, and `original.backend`, if supplied, must
  agree with job/row/known worker behavior. Original environment details go
  in `original.environment`; unknown versions must remain labeled unknown.
- This is a fleet-protocol helper: dx0.5, dt0.02, noise0.002, 12 soup seeds,
  native 0.5px kicks. Nonstandard noise/n_soup/kicks/gpu_seed jobs are refused.

## Native capture path

One selected world runs at a time. The default is the native host recorder,
synchronous apply, and `overlap=False`. It creates no extra record process pool.
The original config's record mode and the actual replay mode are both saved.
If explicitly needed, `--record-mode device --apply-mode async` installs only
the existing native `devrec_proto`/`asyncapply_proto` hooks. Those optional
paths were reviewed and their pure record extraction was tested locally;
the installed GPU/prototype combination still needs its own smoke.

For every frame target, including zero, the helper calls
`init_soup_gpu_batch` / `advance_gpu_batch` / `snapshot_rec_gpu`. It checks:

1. The simulator stayed `ok` and reached the exact target.
2. The native snapshot exists at that target.
3. The snapshot equals freshly read native device activators, not cached `S['F']`.
4. All frames are finite; at least two frames differ.
5. `rec_ts` and total segmented-blob `rec_ct` cover the full 5tu native record grid.
6. Saved NPZ and manifest hashes/arrays validate on readback.

GPU backend and device-array dtype are checked. No GPU means failure, not a
silent local CPU simulation. Blobkit locks are checked strictly by default.
Only soup, recorder, genome, and runtime code are used; no h9/scoring code is imported.

### Narrow, explicit 0.3.5 source-pin exception

The shipped 0.3.5 wheel has a stale 0.3.4 lock table. The approved IC-hook
promotion (commit `9a07779`, build mirrors `4239d7a`) changed only two locked
wrappers: `assay_batch.py` and `soup/sim_gpu.py`. Default strict capture correctly
refuses this wheel. Neither the helper nor its author edits `_locks.json`.

Root approved **optional** `--source-pins source_pins.blobkit-0.3.5.json` for
re-simulations only. Root must verify this manifest against the deployed sources
before opting in. The helper accepts only the exact reviewed pin document
(its canonical SHA256 is fixed in the helper), checks all47 locked files plus
`__init__.py` against full wheel-derived SHA256s, checks the untouched lock-table
hash and module version, and tolerates exactly the two known stale-table entries.
Unknown manifests, bytes, versions, table changes, or additional drift fail.
The original lock mismatch and expected/actual full hashes stay in the report
and film provenance. This is **not** a new locked-numerics certification.
`--plan-only --source-pins ...` checks these sources without importing JAX.

## Commands for ROOT to run on an already free GPU

These are start instructions, **not commands executed by this helper's author**.
Use the existing pod's project interpreter. Do not install packages or rent a
new GPU for this helper. Put `film_capture.py` and the final per-pod selection
in a durable operations directory. Do not reuse `/tmp/podcode/filmcap.py`.

```sh
# Replace these values with the actual existing native interpreter and paths.
PY=/path/to/existing/project/environment/bin/python
OPS=/durable/path/film
SEL=$OPS/selection.island1.json
OUT=$OPS/output-island1
PINS=$OPS/source_pins.blobkit-0.3.5.json
# The pin flags below require root's explicit approval/verification.
# Omit --source-pins and its value to retain strict legacy-lock-only behavior.

# No JAX import, no simulation. Run after freezing the intended row/job/config.
"$PY" "$OPS/film_capture.py" "$SEL" "$OUT" --source-pins "$PINS" --plan-only

# FIRST: three frames at 0,25,50tu, only the first explicitly selected item.
# GNU timeout is the HARD bound; --max-wall-seconds is only a boundary check.
timeout --signal=TERM --kill-after=15s 180s env XLA_PYTHON_CLIENT_PREALLOCATE=false \
  "$PY" "$OPS/film_capture.py" "$SEL" "$OUT" --source-pins "$PINS" --smoke --max-wall-seconds 120

# If a selected spatial IC needs its own path smoke, name it explicitly:
timeout --signal=TERM --kill-after=15s 180s env XLA_PYTHON_CLIENT_PREALLOCATE=false \
  "$PY" "$OPS/film_capture.py" "$SEL" "$OUT" --source-pins "$PINS" --smoke --only EXACT_SELECTION_NAME \
  --max-wall-seconds 120

# Only AFTER smoke passes and root approves remaining time/cost.
# These bounds are examples, NOT permission to exceed the remaining pod budget.
timeout --signal=TERM --kill-after=15s 900s env XLA_PYTHON_CLIENT_PREALLOCATE=false \
  "$PY" "$OPS/film_capture.py" "$SEL" "$OUT" --source-pins "$PINS" --max-wall-seconds 840
```

Root should start these as bounded independent work and retain the PID/log.
Do not block backups waiting for films. Back up result/job/config/IC evidence
first. If the cost deadline is near, skip unfinished films, back up partial
reports, and release the pod. A hard timeout may interrupt native code or NPZ
compression before the report can be finalized; `running` is NOT success.
GNU timeout normally exits124 on deadline, or137 after a hard kill.

## Output, integrity, and rendering

Each invocation saves `reports/<timestamp-id>/{selection,plan,report}.json`.
The report is updated at each frame boundary. Completed films live under:

- `OUTPUT/smoke/NAME/` for short test captures;
- `OUTPUT/capture/NAME/` for complete original-horizon re-simulations.

Each completed directory contains:

| File | Content |
|---|---|
| `film.npz` | House renderer schema; activator frames and full count timeline |
| `manifest.json` | Self-hash, artifact SHA256/bytes, original provenance, actual numerical environment, validation |
| `request.json` | Exact resolved selection/row/job/config and capture contract |
| `genome.json` | Full selected genome with canonical SHA256 in request/manifest |
| `initial_state.npz` | Full actual starting fields (`ic` key), with array/file hashes |
| `source_ic.npz` | Spatial inputs only: exact original IC file bytes, copied and hashed |

NPZ keys include `frames`, `ts`, `rec_ts`, `rec_ct`, `na`, `name`, `genome`
(JSON string), `status`, `T`, `seed`, `L`, `original_T_used`, `original_backend`,
`replay_label`, `interest`, and `C9`. Frames retain explicit simulation dtype;
there is no default float64 simulation and no float16 storage quantization.
`rec_ct` is total segmented blob count, NOT `rec['ct']` time or organism count.
Original scores are annotations only; no score is computed for the replay.
The NPZ `name` includes a GPU re-simulation label so even the house renderer's
default title is labeled. `capture_name` retains the stable output name.

A complete directory is published by atomic rename from a private
`.NAME.partial-*` directory. Missing/failed frames never publish a complete
manifest. Partial directories remain for diagnosis; they are not checkpoints.
The helper does not resume simulations.

A repeat skips a film ONLY after verifying the manifest self-hash, matching
request hash, artifact bytes/SHA256, exact array grids/dtypes, changing frames,
and initial-state equality. It does not overwrite an invalid existing film.
Any helper/selected-source/config/job/path content change can invalidate the
request hash. Freeze inputs for a repeat. Use a new output name/root for a
changed request; preserve old evidence. This is strict reuse, not resumability.

Exit0 means every intended item passed (or every preflight item planned).
For `--smoke`, only its first filtered item is intended. Any missing IC,
failed intended capture, empty selection, budget failure, or corrupt existing
film causes nonzero exit. Partial success is not overall success.

Render later, preferably after backup, with the unchanged house renderer:

```sh
"$PY" probes/blobs/l0/deepsearch/v2_analysis/films/render_film.py \
  OUTPUT/capture/NAME/film.npz OUTPUT/NAME.mp4 \
  --title "NAME — GPU re-simulation, not original trace" --fps 2.5
```

Create the MP4 parent directory first. Rendering needs matplotlib, ffmpeg and
libx264. The renderer casts to f32 and uses per-film percentile color limits;
its colors are not a calibrated comparison of different worlds.

## Storage and time estimate

For L128, four activators, and f32 frames, each raw frame is 1MiB:

| Original T_used | Frames | Raw frame payload |
|---:|---:|---:|
| 2,500tu | 11 | 11MiB |
| 5,000tu | 21 | 21MiB |
| 10,000tu | 41 | 41MiB |
| 20,000tu | 81 | 81MiB |
| 40,000tu | 161 | 161MiB |

Six 20,000tu films are about486MiB of raw f32 frames, plus initial/source ICs
and small metadata. Compression may reduce this; do not count on a fixed ratio.
f64 doubles frame storage. L192 multiplies it by2.25. Native record snapshots
upcast to f64 in host RAM, so peak host memory is larger than saved f32 payload.

Runtime is unknown until the actual GPU smoke/progress. A 20,000tu replay is
1,000,000 native steps. Short smoke includes compilation and is not a stable
throughput benchmark. Use the later 250tu progress intervals to estimate
remaining wall time, with margin for compression. This one-lane safe path is
not the campaign's padded multi-lane throughput benchmark.

## Local tests (no GPU or physical simulation)

From this repository root, using its own environment:

```sh
.venv/bin/python -m unittest discover \
  -s probes/blobs/l0/deepsearch/v3_pilot/film_recovery \
  -p test_film_capture.py -v
```

The test suite uses installed editable blobkit (or set `PYTHONPATH` to
`probes/blobs/blobkit` in the same project environment). Do not install project
dependencies into an agent kernel. Tests cover exact-job matching, CPU/GPU and
dtype inference, spatial IC validation, manifest corruption, missing/stale
frames, early stop, soft budgets, empty/partial failures, idempotent integrity,
and native pure async extraction parity. They do NOT certify JAX/GPU execution.
