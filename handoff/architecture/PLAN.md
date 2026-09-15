# Accepted repository ownership plan

Accepted by the user on 2026-09-15. This supersedes the provisional plan to
contribute Blobkit's source to Prime's residency-environments repository.

## Source ownership

- The personal `swpo/physim` repository owns Blobkit's source, package releases,
  general simulation and CPU/GPU implementations, metrics, evolutionary search,
  harvesting, registry APIs and library tests. It also owns exploratory research,
  analyses, and the project website/documentation published through GitHub Pages.
- Prime's `residency-environments` repository will own the shared Physim taskset
  once it is accepted: agent-facing laboratory contract, reward and submission
  handling, evaluation/training configs, and Docker/runtime setup.
- Prime should also receive `generators/physim/` with runnable, evaluation-specific
  preparation, generation and validation entry points. These use installed
  Blobkit and explicit published registry inputs. They must not require hidden
  files from the personal research checkout.
- Hugging Face `seanpohorence/physim-worlds` owns published snapshots of worlds,
  preparations, suites, archived recipes, provenance and scientific artifacts.
  Local registry directories are working copies; publication creates immutable,
  explicitly referenced dataset revisions.

## Package and workflow boundaries

Blobkit remains independently installable. Physim imports its simulation API,
without importing campaign scripts or locating a neighboring source tree.
Reusable search/metrics/harvesting machinery belongs in Blobkit. The official
Physim preparation and suite recipes belong with the environment in Prime.
Exploratory campaign entry points and analysis stay with the personal project;
executed recipes and their evidence are archived with the contributed worlds.

The environment pins a public Blobkit release and each evaluation config pins a
specific HF revision and preparation. Changes to numerical semantics or scoring
must preserve old reproducibility and introduce appropriate new identities.

## Development and synchronization

Maintain one source home for each package. After the upstream merge, develop
environment changes in a local checkout of a Prime fork and submit them through
Prime's PR process. The personal research workspace consumes a pinned environment
release or commit. For work spanning both packages, use editable dependencies
across the two local checkouts; published defaults remain immutable pins.

Blobkit changes are tested and released from the personal repository, followed
by an explicit dependency update in Prime when needed. New worlds are published
on HF, followed by explicit config updates for their inclusion in evaluations.
Do not maintain independently edited copies or automatic bidirectional file sync.

Keep the current environment source here until the contribution is accepted and
the research workspace has been adapted to consume the installed environment.
Some research/migration helpers still use checkout-relative environment paths;
remove those dependencies before retiring the local source copy. Preserve
historical source artifacts and identities.

The project website remains the scientific entry point and links to the upstream
environment and HF data. Each code repository should link to the other where
needed for contributors to understand ownership and reproduction.

## Remaining contribution work

The 46-file Prime candidate includes the environment, explicit world configs,
Docker support, and portable `generators/physim/` workflows. Clean-checkout
validation now covers installed public dependencies, both complete BF/XV suite
replays and registry round trips, all three published reference scores and fresh
native experiments, and two successful stock Verifiers wiring smokes. See
`handoff/pr_preparation_20260915/REPORT.md` and its publication receipt for the
current draft PR and review status.

After acceptance, adapt the personal research workspace to consume the shared
environment and retire its transitional source copy. Maintainer review remains
necessary for Prime's external runner configuration and image provisioning.

## Registry contribution option

HF supports community pull requests to public dataset repositories without
granting contributors write access to the main branch. The
[contribution guide](../../registry/CONTRIBUTING.md) documents reviewed PRs
containing the world definition and available provenance, using published
Blobkit's existing registry API and HF's upload API.
Maintainer checks should validate registry integrity and reproducibility before
merging and rebuilding derived catalogs/release metadata. A preserved world does
not need an evaluation suite; eval-ready status requires its preparation and
suite validation. The guide is staged with each HF release and linked from the
dataset card, website, and environment data documentation. Review remains manual;
no automatic contribution validator or submission CLI has been added.

Reference: https://huggingface.co/docs/hub/repositories-pull-requests-discussions
