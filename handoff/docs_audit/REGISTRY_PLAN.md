# World registry plan

This is a proposed design for the documentation/repository refresh. No registry has been created or published.

**Use GitHub for code, schemas, and documentation; use a Hugging Face dataset repository for released world bundles and a small browsable catalog.** Begin with the existing prepared `p4g2_044` example. Keep the bundle format independent of the hosting provider and support loading an already downloaded directory.

The first release needs a catalog, manifests, a downloader/validator, and one reproducible example. It does not need a registry service, a database, a leaderboard service, or a new world-generation campaign.

## 1. What already exists

| Existing piece | Reuse | Missing layer |
|---|---|---|
| [`blobkit.worlds`](../../probes/blobs/blobkit/blobkit/worlds.py) | Packaged genome loading, 15 named genomes, protocol overrides, provenance/lock conventions | Remote revision resolution, prepared instances, prediction suites, download profiles, and release metadata |
| [`physim/blobdata`](../../environments/physim/physim/blobdata) | The three selected evolved genomes, including `p4g2_044` | One authoritative lookup; these are separate from the blobkit registry roster |
| [Prepared origin](../../probes/blobs/agentenv/round6/worked_example/p4g2_044/origin.py) | Exact field identity, apparatus setup, independent-noise policy | A self-contained data bundle instead of cache/study-file lookups |
| [Case compiler](../../probes/blobs/agentenv/round6/worked_example/p4g2_044/cases/build_cases.py) and retained truth manifests | Physically motivated programs, fixed score groups, observation provenance | A versioned suite manifest that the grader accepts as an input |
| Native-run manifests and reports | Predictor snapshots, observations, configs, validity, cost, and scores | A small consistent result record referencing the released world/preparation/suite |

Only `p4g2_044` currently has the complete prepared prediction-suite path. The other selected genomes and the many search candidates should not acquire an “evaluation ready” label merely by appearing in a catalog.

## 2. Four identities, one small bundle format

These objects can initially live in one release manifest. Keeping their identities separate prevents a sensor change, a new preparation, or a scoring revision from silently changing the meaning of an old result.

| Object | Defines | Identity changes when |
|---|---|---|
| **World** | Field equations/genome, required simulator implementation and numerical profile | Physical law or numerical realization changes |
| **Preparation** | World reference, exact initial fields, apparatus/source configuration, time origin, and experiment-noise policy | The physical start, instruments, control mapping, or noise law changes |
| **Evaluation suite** | Preparation reference, prediction API, action/query programs, fixed score groups/scales, truth evidence, and aggregation | Programs, interface semantics, truth set, or grading definition changes |
| **Run** | Suite reference, predictor and observations, model/harness/settings, budgets, validity, costs, and scores | A new attempt is made; retries remain separate runs |

A human-readable name such as `p4g2_044` remains useful. A released manifest also records exact content hashes and code revisions. A reported result resolves to these exact references, not whatever a mutable `latest` alias points to later.

Do not use an equation-search score as a prediction-evaluation score. Generation descriptors, physical characterization, suite coverage, and model performance answer different questions and should have separate fields.

## 3. Hosting choice

| Option | Fit | Recommendation |
|---|---|---|
| **HF dataset repository + GitHub code/docs** | Dataset repositories provide file revision history and public/private visibility; dataset cards supply a rendered overview and metadata. | Preferred for the reusable world catalog and released data. [HF repository guidance](https://huggingface.co/docs/hub/datasets-adding), [dataset cards](https://huggingface.co/docs/hub/datasets-cards) |
| **GitHub release assets + code/docs** | Tagged software releases can include downloadable binary assets. Each asset must be below 2 GiB. | Viable for the first small demo or as a mirror. It needs the same Physim manifests and validation; it does not remove the packaging work. [GitHub releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) |
| **Object storage behind the same manifests** | Can hold larger or more operational data without putting it in the source repository. | Leave as a later storage adapter if volume or access needs justify it. Keep identity, validation, and the public catalog independent of a bucket URL. |

Use a separate proposed dataset repository such as `<owner>/physim-worlds`; choose the owner at publication time. Do not repurpose the existing rollout-trace dataset as the world registry. Put run records and large trace bundles in a separate results dataset if needed.

A small JSONL catalog can drive the HF data viewer and website cards. Keep numerical arrays in bounded NPZ files loaded with `allow_pickle=False`; a custom simulation array need not become a table merely to appear in the viewer. The catalog contains metadata and artifact references, while the loader downloads the referenced numerical files. HF documents JSON/JSONL and Parquet as supported tabular formats; custom structures may not be recognized by the viewer. [Supported dataset formats](https://huggingface.co/docs/hub/datasets-adding#file-formats)

Pin downloads to a full repository commit and select only the requested bundle/profile. HF's download API supports explicit revisions and file filters. Inspect the manifest's file sizes before fetching, then verify every listed hash. [Versioned and filtered downloads](https://huggingface.co/docs/huggingface_hub/guides/download)

Storage allocation should follow the actual release manifest. Do not upload the entire research tree or assume unlimited free storage; public storage is best-effort on free accounts and larger volumes depend on the account's plan. [HF storage policy](https://huggingface.co/docs/hub/storage-limits)

## 4. Minimal release contents

Proposed layout, illustrated for the public reference example:

```text
README.md                         dataset card and supported usage
catalog.jsonl                     one row per released bundle
bundles/p4g2_044/<revision>/
  manifest.json                  typed identities, versions, files, hashes
  world.json                     genome and numerical profile
  preparation.npz                exact initial field array
  apparatus.json                 probe/source setup and control mapping
  suite.json                     contract, cases, groups, truth references
  truth/*.npz                    reference-case realizations
  checks.json                    validation results and reproduction scope
  world-card.md                  physical description and measured coverage
  preview.mp4                    optional, separately downloadable
```

This layout is a data format, not a requirement to execute Python supplied by a dataset repository. Simulator, case-generation, and grading code belong in the installed, versioned source package. The runtime validates the bundle before allocating large arrays or starting simulation.

The manifest should contain:

- Schema version; bundle/world/preparation/suite identifiers; release status; code/data/media license identifiers; a citation or source reference.
- Genome file hash; simulator source/release reference; backend, dtype, spatial grid, boundary conditions, timestep, and relevant numerical settings. Record enough to state whether reproduction is exact or within a declared tolerance.
- Initial field shape/dtype/hash; preparation recipe or source reference; public time origin; apparatus/source data hash; noise coefficient and experiment-noise policy.
- Prediction-contract version and roster; valid action/time ranges; suite/case digests; fixed score-group and scale definitions; scientific aggregation; truth count and provenance. Runtime/inference budgets are named run profiles, not implicit physical properties.
- For each file: relative path, bytes, SHA-256, role, and download profile. Reject traversal, missing files, unexpected array types/shapes, and mismatched hashes.
- Evidence references for physical characterization, interface checks, score controls, and reproduction. A short description of what is demonstrated and what remains untested is enough; campaign narration is unnecessary.

Manifest and catalog generation should have one source of truth. The website renders its world cards from that metadata plus an edited physical explanation, instead of maintaining a second roster by hand.

## 5. Public reference material and held-out evaluation

The existing worked world is a **public reference example**: publishing its fields, equations, cases, and truths can make the workflow reproducible. Results on it should be described as reference/development results, not evidence of unfamiliar-world generalization.

For a future held-out challenge, keep unreleased preparations, mappings, selected test programs, and truths in a separate access-controlled grader store. A folder named `private/` inside a public dataset is still public. The agent receives its contract, experiment outputs, and own artifact; the trusted experiment/grading host resolves the other data.

The public/private split is a property of a released suite and its intended use. It should not prevent openly publishing physical reference worlds. Once a world or preparation has been described and released, record that exposure and reserve distinct worlds/preparations for claims that require unfamiliarity.

Do not publish hidden-test seeds or truth references in agent-visible run configuration. Reproducibility for maintainers and independent benchmark reproduction can use the privileged bundle; the evaluated agent's filesystem and tool access remain narrower.

## 6. First bundle: preserve the current example exactly

The present origin loader reads `snapF_1700` from a **794,707,121-byte** historical cache. The actual initial field is `(12, 256, 256)` float32: **3,145,728 bytes, or 3 MiB, uncompressed**. A focused bundle can extract that array and the required setup metadata instead of requiring the full cache. Final compressed and complete-bundle sizes must be measured after extraction; the 3 MiB figure is only the field array.

Preserve:

- The current genome, exact initial-field hash, probe/source setup, and original-time-1700 to public-time-zero rebasing.
- Fresh independent noise from the start of each experiment. Do not restore a cached future-noise stream as the grading convention.
- The current 50-unit horizon, 12 ports, device slot counts 13/19, global slot count 2, and action timing semantics.
- All 15 programs, their declared selectors/scales, and the retained truth arrays. A later expanded suite gets a new suite identity.
- The current scientific results as regression evidence. The persistence predictor's native 15-case error is approximately 0.8271209896; reproduction must identify the same suite and forecast conditions.

Extract apparatus metadata into an explicit record rather than depending on a research report's JSON layout or undocumented seed-derived reconstruction. Package the existing origin builder as a migration/export tool; the supported loader should read the released bundle directly.

## 7. Reader and contributor workflows

Proposed capabilities, **not existing commands**:

| Workflow | Behavior |
|---|---|
| Browse | List world IDs, a short description, bundle size, physical characterization, and whether a prediction suite exists. No simulation starts. |
| Fetch | Resolve an exact revision; show required bytes; download only the selected preparation/suite/media profile; verify hashes. |
| Inspect offline | Show the manifest, schema, source references, and reproduction requirements from a local bundle. |
| Run the reference example | Execute a supplied simple predictor and score it on the reference suite, without a model API key. A separate explicit command performs new native experiments. |
| Run a model | Use the same released suite with a named harness/config, declared experiment and inference budgets, and a new output directory. |
| Contribute a world | Supply a genome and reproducible preparation, then physical characterization and observable evidence. Add a prediction suite only when its programs and scoring are supported by those phenomena. |

Admission should follow the physics. A search candidate becomes a usable world after reproducibility and characterization; a prepared instance gains a prediction suite after its cases and score controls are checked. Model performance is recorded afterward and does not determine which phenomena are retained.

Use explicit capability/status metadata such as `simulation_available`, `preparation_reproducible`, and `prediction_suite_available`. This avoids presenting every generated genome as an equally validated benchmark task. Failed candidates and incomplete studies can stay in the research archive.

## 8. Implementation sequence

1. **Define the manifest and resolve the source boundary.** Keep the existing `blobkit` simulation and genome loader. Add preparation/suite loading to the current evaluator package. Establish the code/data licenses and release source set.
2. **Export one focused bundle.** Produce exact-state data, apparatus metadata, suite/truth references, and hashes from the existing example. Retain the original research files unchanged.
3. **Implement local loading first.** Remove the current supported path's need for `sys.path` injection, study JSON paths, hardcoded cache locations, and dated local image assumptions. Fail clearly when a required bundle is absent.
4. **Prove reproduction.** From a clean install, load the bundle, run public interface checks and a scripted predictor, and reproduce the declared score. Check the independent-noise, action-timing, and query-shape semantics against the existing tests. No paid model is needed for this release check.
5. **Add HF resolution and publish the reference release.** Download by exact revision into a verified cache. The release gets a dataset card, license/citation, complete manifest, and one-click links from the docs. Publication is a later action, not part of this audit.
6. **Connect the website and expand carefully.** Render world cards from the catalog. Add further worlds only with their own preparation/evidence. Introduce a held-out suite when its access and exposure policy is defined.

Before release, the owner must choose the publishing namespace and intended code/data licenses, and decide which future preparations are public references versus held-out challenge material. The technical plan can be implemented locally before those publication choices are finalized.
