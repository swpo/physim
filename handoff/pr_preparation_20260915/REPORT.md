# Physim contribution and documentation update — 2026-09-15

The Prime candidate contains 46 files: the Physim environment, portable world
preparation/validation workflows, explicit evaluation configs, and Docker/build
support. Blobkit remains a separately released dependency in the personal repo.
The candidate is based on upstream `01d9f5f80572b7ec82575b10d45a800ed844e496`.

## Verification

- A clean Prime checkout installs public Blobkit 0.3.5 and current Verifiers 0.3.1
  with the reference NumPy 2.5.2/SciPy 1.18.0 numerical profile.
- All three published preparations pass reference scores and fresh native
  experiments. The simulation package imports from the installed wheel.
- Both BF and XV restore exact inputs from the pinned HF registry. Their complete
  11-program workflows generate fresh development trajectories, grading truths,
  diagnostic forecasts, reference checks, and local registry exports.
- All 30 scientific files match the published data byte for byte, including all
  22 truth archives. World, preparation, and suite identities are unchanged;
  manifest hashes differ because replay provenance/check metadata changes.
- BF's fresh mechanism check reproduces its recorded effect and zero response
  when bilinear feedback is removed. Both registry round trips pass. The small
  evolutionary-search example completes and verifies its lineage/checkpoints.
- Two fresh four-turn DeepSeek V4 Flash rollouts complete with no infrastructure
  errors. Neither delivers a predictor; both receive zero reward. Total cost is
  $0.0027, and no smoke containers remain. No GPUs were rented.
- Prime's two generic package checks and full-repository Ruff lint/format pass.
  Upstream tests and CI are unchanged; no per-environment tests were added.
- The personal source set passes 93 package/registry/CPU tests. Existing local
  scientific checks pass: 23 scheduler, 30 scorer, 10 exploration, 20 Verifiers,
  and all 15 bundle checks with the explicit published reference fixture.

## Documentation reviewed

The site now consistently describes three eval-ready preparations, variable port
counts, explicit world selection, generous run budgets, and the completed-rollout
zero-reward policy. Historical results remain labeled with their original scope;
BF/XV pilot findings link to the scientific report. The contribution guide is
linked from the site and environment docs.

A small immutable genome snapshot makes documentation builds independent of the
old environment fixture. The rebuilt site passes checks for 67 HTML pages and
679 local links; the runnable example returns the expected finite arrays. The
publication checkout also passes those checks without optional research outputs.

The personal source set includes Blobkit, registry snapshots, reusable code,
scientific reports and figures, documentation sources and generated Pages files.
Raw untracked run outputs, process logs, and large local inventories remain local.
The environment copy stays temporarily until the Prime contribution is accepted
and the research workspace consumes the upstream package.

Machine-readable evidence is stored alongside this report. New replay data are
local verification outputs; the published HF scientific snapshot is unchanged.
