# Generation and registry refactor — complete

Blobkit remains the independently installable package under `packages/blobkit/`.
The new `blobkit.generation` API implements a complete generational search with
Python evaluation, scoring, variation, selection, and harvesting hooks. It reuses
the existing simulation, mutation/recombination, and adaptive assay code.
`blobkit.registry` stores immutable genomes, recipe sources/state, runs, candidate
lineage, checkpoints, results, and harvested world records.

The CLI supports local recipe execution, process workers, pause/resume, registry
verification, and recipe export. Recipe reads and registry verification never
execute archived code. Replay is explicit. The example under
`generators/physim/recipes/` runs short real CPU simulations and custom metrics.

## Design and compatibility

- Evaluation imports the shared simulator and has no import dependency on the
  generation engine or registry. The environment installation contract is unchanged.
- Recipes own settings and custom Python policies; the package owns the reusable
  search loop, scheduling interface, checkpointing, and harvesting machinery.
- Recipe identities include source snapshots, hook state, seed genomes, settings,
  package versions, and the implementation integrity table. Extra input/source
  files and distribution dependencies can be declared explicitly.
- Search checkpoints commit complete generations. Resume preserves the run and
  rejects changed recipes or implementations. Callback determinism is part of
  the API contract; unfinished generations are recomputed.
- Existing fleet scripts remain available for their historical island protocol.
  They were not silently replaced with the new default elitist search policy.
- Harvested genomes are not automatically validated evaluation tasks. Registry
  records link the existing physical world/preparation/suite/bundle identities.
- The current unpublished candidate remains 0.3.5. New artifact hashes distinguish
  this build from the earlier polishing candidate; nothing was published.

## Registry and release staging

The local registry contains 16 sourced historical worlds, six example harvests,
19 distinct genomes, two recipe records, two generation runs, six candidates,
three checkpoints, and one completed result. The historical `p4g2_044` record
retains its original candidate measurements, parent description, and available
preparation/validation sources. Missing original search settings and checkpoints
are explicitly marked partial. No missing historical runs were invented.

The verified registry and its catalog are included in
`dist/hf-generation-candidate/` beside the unchanged reference evaluation bundle.
Archived Python source carries the code license. The website's registry and
generation pages document the workflow and link the generated catalog. Public
upload and source publication remain separate release steps.

## Verification

| Check | Result | Receipt |
|---|---|---|
| CPU, package, registry, and generation tests | 65 passed | `cpu-tests.log`, `cpu-tests.xml` |
| Existing full CPU assay through the new adapter | 1 passed | `assay-adapter.log` |
| New single-simulation and padded-assay JAX adapters | 2 passed on JAX CPU | `jax-adapters.log`, `jax-adapters.xml` |
| Fresh Python 3.12 wheel install outside checkout | 64 passed; Physim-only boundary test skipped | `clean-install.log`, `clean-tests.xml` |
| Fresh Python 3.10 wheel install outside checkout | 63 passed; optional plotting and Physim boundary skipped | `clean-python310.log`, `python310-tests.xml` |
| Generic environment package contracts | 2 passed | `generic-contracts.log` |
| Prepared Physim reference demo | Exactly 0.8271209896216252 | `physim-reference.json` |
| New native experiment from prepared state | Passed, 0.06 time units | `native-experiment.json` |
| Registry integrity and reference graph | Passed | `registry-verification.json` |
| Documentation | 678 local links checked, no errors | `docs-checks.json` |
| Ruff lint/format and git diff whitespace | Passed | Verified at completion |

The tests cover deterministic serial/process/out-of-order evaluation, pause and
resume, changed-recipe rejection, custom metrics with actual simulation,
recombination, harvesting lineage, recipe export/replay, physical rejection,
callback failure propagation, malformed budgets/results, source corruption, and
safe source export. The first test pass exposed a mistaken example metric's use
of simulator mass records; it was corrected to read per-activator series.

Every previous numerical, metric, and operator source file remains byte-identical.
Only package initialization, CLI, and the integrity table changed among existing
implementation files; `generation.py` and `registry.py` were added. Consequently
the earlier real-A100 kernel checks still apply to those unchanged kernels. This
turn exercised the new JAX adapters on CPU and rented no GPU.

The wheel and source archive are in `dist/blobkit-generation/`. A wheel rebuilt
from the source archive has identical extracted contents. The archive contains
the new tests, pytest configuration, and generation guide. Exact artifact hashes
and the source comparison are in `artifacts-and-identity.json`.
