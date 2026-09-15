# Blobkit polishing complete — 2026-09-13

Blobkit 0.3.5 is an independently installable local release candidate. The wheel
and source archive are in `dist/blobkit-polished/`; neither has been published.
`distributions.json` records their hashes. A wheel rebuilt from the source archive
has identical extracted contents, including all 15 genomes, stamp data, fleet
templates, license, CLI, and both integrity tables. The source archive includes
the complete tests and pytest configuration.

## Changes

- CPU installation requires only NumPy and SciPy. Optional `accelerator`, `gpu`,
  `plot`, and `test` extras cover JAX, CUDA, PNG output, and release checks.
- `blobkit`, `blobkit --accelerator`, and `blobkit --gpu` report installation
  integrity and available devices. The GPU check fails on CPU fallback.
- Fleet source bundles retain the installed package's dependency markers,
  Python constraint, extras, license, data, and CLI. Generated instructions use
  the local source package and the correct batch launcher. The final generated
  source builds successfully; runtime bytes and dependency metadata match the
  release wheel (`final_fleet_verification.json`).
- Batch and initial-state validation rejects invalid horizons, mismatched or
  nonfinite fields, and invalid dtypes before device work. Empty batches need no
  JAX installation. The numerical stepping algorithms are unchanged.
- The current source-integrity table covers 50 installed files. The original
  0.3.4 table is preserved separately so historical differences remain visible.
- CPU/package tests run in CI. `scripts/blobkit/check_install.py` validates a
  wheel in a fresh environment outside the checkout, optionally including plots.

## Verification

All 58 test cases have passing coverage across CPU and CUDA runs:

| Check | Result | Receipt |
|---|---|---|
| Final wheel, clean Python 3.12 CPU and plotting | 40 passed | `clean_final.log`, `clean-final-tests.xml` |
| Full CPU reference assay and injected backend | 1 passed | `cpu_reference.log` |
| CUDA kernels, padding, chunking, full grids, recording | 15 passed | `gpu-tests.xml` |
| Corrected CUDA assay repacking and retained-padding cases | 2 passed | `gpu/final-tests.xml`, `gpu/release-gpu-tests.xml` |
| Final wheel CUDA, package, and integrity checks | 21 passed | `gpu/release-gpu-tests.xml` |
| Final wheel, Python 3.10 CPU | 39 passed, optional plotting skipped | `gpu/release-python310-tests.xml` |
| Python 3.13 CPU installation before two added burn-in checks | 38 passed | `clean_py313.log` |
| Physim reference score | Exactly 0.8271209896216252 | `physim_reference.json` |

The first CUDA run exposed two test fixtures whose horizons ended at or before
the metric's fixed 500-unit burn-in. Their single-world reference failed before
comparison. The fixtures now use 1,250/2,500, both comparisons pass, and explicit
validation prevents invalid horizons from reaching the batch execution path.
The original failed log is retained for the audit trail.

Seven reference CPU/genome/metric files remain byte-identical. Eight GPU stepping
and packing functions have identical syntax trees (`science_identity.json`).
The short cross-backend tests use noise-free trajectories and stated tolerances;
CPU and JAX noise streams differ. These checks do not claim equivalence of every
long chaotic trajectory or performance certification of the recording prototypes.

Ruff lint and formatting checks and `git diff --check` pass. The generic
environment contract results are in `generic_contracts.log`.

## Compute cleanup

The NVIDIA A100 80GB rental `aee17f876964457e86c17aad4396ca65` was terminated at
14:10:07 UTC after 23 minutes 33 seconds. All requested logs were downloaded and
the final GPU-tested wheel hash matches the delivered wheel. The cleanup
backstop was then cancelled; unrelated instances were left untouched.

Estimated compute cost is $0.471 at the quoted $1.20/hour. Prime's history output
contains an ambiguous raw `total_cost` value, so this is an elapsed-time estimate,
not a claimed invoice total. `pod_termination.json` preserves the provider
receipt; `completion.json` records the calculation and all passing test names.

Publication, the Hugging Face upload, and the eventual upstream PR remain the
separate release steps described in `RELEASING.md`.
