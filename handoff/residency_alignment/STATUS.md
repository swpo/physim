# Residency organization alignment

Local alignment is complete against Prime Intellect's residency-environments
commit `01d9f5f80572b7ec82575b10d45a800ed844e496`. The code remains uncommitted; no
package, dataset, or upstream PR was published by this task.

## Changes

- `environments/physim/` is a standard installable Verifiers v1 taskset. `physim`
  exports its single taskset; `physim_r6` and the scaling variant remain compatible.
- `generators/physim/`, `scripts/physim/`, and `configs/physim/` hold generation,
  support, and configuration, matching upstream's split.
- `packages/blobkit/` is the active, independently versioned simulator package.
  This is a local workspace extension. Upstream's separate `kernelguard` dependency
  is the precedent; it does not establish an upstream `packages/` convention.
- Older engines, servers, tasksets, and obsolete tools moved into
  `probes/legacy/physim/`. Research inputs and the original blobkit tree remain
  intact. The installed wheel imports no research tree.
- Python 3.12, uv workspace installs, package metadata, the full-eval convention,
  Ruff, generic upstream package checks, and local CI now use the new layout.
- Apache-2.0 code and CC-BY-4.0 reference-data licenses were applied. The staged
  HF candidate targets `seanpohorence/physim-worlds`.

## Verification

- All 100 existing local regression checks passed: 29 scheduler/native, 30 scoring,
  10 experiments, 16 Verifiers integration, and 15 bundle/cache/reference checks.
- Both unmodified upstream package checks passed. The first build attempt could
  not reach PyPI in the sandbox; retrying from the populated offline cache passed.
- All 16 extraction/parity checks passed. Scientific source bytes, prepared data,
  all retained truth files, and world/preparation/suite/bundle identities match.
- Four distributions built and passed payload inspection. They contain licenses;
  Physim excludes legacy engines, private arrays, and research output.
- A fresh Python 3.12 installation outside the checkout loaded both taskset IDs,
  reproduced persistence score `0.8271209896216252`, and ran a native 0.06-tu experiment.
- Verifiers 0.3.1 resolved the evaluation config through its real eval CLI dry-run.
- Both Docker images built from the new paths. The example passed all seven public
  gates and all 15 grading cases, reproducing zero score `1.0845872705112614`.
- Ruff lint/format passed. Documentation build and link/evidence checks passed
  across 67 HTML pages, including 12 current pages and 676 local links.

No model API calls were made. A real model eval smoke remains a pre-PR check.
The scientific reference files are excluded from reformatting because manifests
bind their bytes. Blobkit's old 0.3.4 lock record still reports the same two known
GPU/batched-assay differences; this task does not recertify those workflows.

## Upstream boundary

The first PR should carry the installable environment, eval config, and necessary
Docker/build support. Blobkit must first become independently installable through
publication or an agreed immutable source dependency. The one-time generator
migration depends on this repository's preserved research inputs and should remain
here until a separate portable generator contract is prepared. Our local regression
suite, research archive, package workspace, and CI do not belong wholesale in Prime's repo.

See `REPOSITORY.md` for rationale and `RELEASING.md` for publication steps.
`completion.json` links the detailed build, parity, clean-install, and Docker receipts.
`before/` and `source_before.json` preserve the pre-move source for review.
