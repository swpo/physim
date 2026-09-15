# Repository cleanup status — 2026-09-13

Local implementation and validation are complete on `codex/reproducible-core`.
No model API calls were made. No code, dataset, or website was published.
The existing dirty work and historical research evidence were preserved.

## Completed

1. **Source boundary and backup.** Preserved 47 active source files and their hashes
   before edits. Only `physim/__init__.py` and the two current adapter files changed
   among those originals. The R6 scheduler, scoring, experiment service, and CPU
   kernels retain their original bytes. Five device definitions were extracted
   with identical syntax trees.
2. **Reusable packages.** Physim 0.12.0 has an explicit blobkit 0.3.5 dependency,
   a current lazy entry point, portable CLI, optional agent/Hub extras, packaged
   public specification, and versioned Docker images. The root is a UV workspace,
   with one canonical version per package and a checked lockfile. Legacy Physim
   modules stay in the source checkout and are excluded from the wheel.
3. **Exact reference bundle.** The standalone payload is 3,732,420 bytes plus its
   manifest, replacing a 794,707,121-byte cache dependency. It includes exact
   prepared fields and apparatus, 15 programs/groups, and all 30 retained native
   realizations. Separate content identities bind world, preparation, suite, and
   run. Bundle validation rejects malformed paths, files, hashes, arrays, and plans.
4. **Clean-install reproduction.** Both wheels were installed outside the checkout,
   initially with only NumPy and SciPy. The persistence control reproduces exactly
   0.8271209896216252; seven interface checks pass. A new 0.06-tu native experiment
   succeeds without the research tree, Verifiers, or model credentials. The optional
   native task also loads from its installed package, checks the bundle before
   model execution, and shares one experiment budget across prompt and service.
5. **Repository/docs organization.** README, REPOSITORY.md, RELEASING.md, examples,
   JSON schema, CI, and static docs describe the supported workflow. Historical
   sources and evidence stay at their existing paths to preserve references.
   Website world metadata is synchronized from the staged bundle catalog.
6. **Distribution tooling.** Data-only HF release directory and catalog are staged.
   Downloads require a full commit, enforce byte caps, verify selected-profile
   hashes, and atomically populate a cache that can be reverified offline. Public
   network fetching of this bundle awaits publication; mocked transport tests
   cover revision, profile, corruption, partial download, and offline behavior.

## Validation evidence

- 29 scheduler tests, including native gates: `scheduler_tests.json`.
- 30 scoring tests: `scoring_tests.json`.
- 10 experiment-service tests, 16 native task tests, 15 bundle/cache tests: passed.
- 13 source-extraction and native parity checks: `native_parity.json`.
- Clean base install, exact score, and native experiment: `clean_install.json`.
- Final installed code reproduces the exact score: `final_installed_demo.json`.
- Installed optional task/config without model calls: `installed_native_task.json`.
- Docker interface gate: 7/7 passed. Final frozen-input Docker grading: all 15
  cases complete, zero-predictor score 1.0845872705112614 with 64 forecasts:
  `docker_zero_grade_frozen.json`.
- Outer manifest JSON schema validates; UV lock and Python compilation pass.
- Documentation: 12 current pages, 67 total HTML files, 676 local links, no errors.
- Distribution contents and hashes: `wheel_inventory.json`.

The final source wheel is about 53 KB. It contains the current runtime and agent
adapter, but no truth arrays, prepared fields, legacy tasksets, or research tree.
The blobkit wheel is about 342 KB and retains its historical packaged utilities.

## Local artifacts

- Dataset candidate: `dist/hf-worlds-candidate/`.
- Bundle: `dist/hf-worlds-candidate/bundles/p4g2_044/0c133190c1c86450f56651b47e35f0d729f6a84c7c51a4bc7d91850a9a392ff2/`.
- Source/wheel products: `dist/wheels/`.
- Isolated install: `/private/tmp/physim-clean-install-20260913/`.
- Exact staged file list and candidate catalog: `release_candidate.json`.

Generated distributions and model-free test outputs are ignored. Work remains
uncommitted; review the selected source set rather than staging all historical
logs and prior untracked research output.

## Decisions still needed for publication

- Code license, including blobkit (currently marked Proprietary).
- Data license for the reference bundle.
- HF namespace; `seanpohorence/physim-worlds` was proposed, separate from rollouts.

After these choices, apply consistent license metadata, commit the reviewed code,
publish the staged dataset, capture its immutable commit, verify a real fetch and
offline rerun, and update published links. No public revision is claimed yet.

## Scope limits

This is a public-reference/development suite for one preparation, with two truths
per case. The c006/c007 fine-timing coverage limitation is unchanged. Bitwise CPU
parity was checked on this machine; other platforms need the reference check.
The old blobkit lock table still reports two pre-existing differences in the
GPU/batched-assay code. Those files are unchanged by this work and were not
recertified; the CPU kernels match their original hashes and the bundle identity.
