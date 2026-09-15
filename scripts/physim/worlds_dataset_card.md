---
pretty_name: Physim worlds and evaluation preparations
license: cc-by-4.0
task_categories:
- other
tags:
- physics
- simulation
- executable-predictors
configs:
- config_name: worlds
  default: true
  data_files:
  - split: train
    path: worlds.jsonl
- config_name: evaluations
  data_files:
  - split: train
    path: catalog.jsonl
---

# Physim worlds

This snapshot contains **{{WORLD_COUNT}} world records, {{GENOME_COUNT}} distinct
genomes, {{PRESERVED_COUNT}} preserved records, and {{EVAL_COUNT}} eval-ready
laboratory preparations**. Multiple records may share a genome. The viewer's
`train` label is a catalog partition, not a scientific training/test split.
These are disclosed development data.

## Worlds, preparations, and suites

- A **world** defines physical dynamics: its genome, parameters, and interactions.
  `worlds.jsonl` lists all records and links to their definitions and provenance.
- A **laboratory preparation** binds an exact saved physical starting state to
  its measurement/control apparatus. The apparatus belongs to this setup, not
  the world's intrinsic physics.
- An **evaluation suite** contains action/query programs, retained independent
  reference trajectories, and scoring configuration for a preparation.

One world can support multiple preparations and suites. `preserved` means its
definition and available history are archived. `eval-ready` means an exact
preparation and suite have been validated and packaged for evaluation. Availability
does not automatically select a world when running Physim.

## Evaluation preparations

| Preparation | Public ports | Grading programs | Files |
| --- | ---: | ---: | --- |
{{EVALUATION_TABLE}}

`catalog.jsonl` lists these bundles, identities, profile sizes, and runtime
requirements. Each program has two independent retained truth realizations;
model evaluation requests 64 forecast samples. Grading programs within a bundle
are separate from rollout counts.

## Download and use

Select the full 40-character commit of this dataset to reproduce a snapshot.
Replace `FULL_DATASET_COMMIT` and `BUNDLE_PATH_FROM_CATALOG` below; a mutable
branch such as `main` is not accepted by the Physim downloader.

```sh
physim catalog --repo {{DATASET_REPO}} --revision FULL_DATASET_COMMIT
physim fetch --repo {{DATASET_REPO}} --revision FULL_DATASET_COMMIT \
  --path BUNDLE_PATH_FROM_CATALOG --profile evaluation
```

The fetch command returns a verified local directory. Supply it as
`env.taskset.task.tools.bundle` to the environment. The `simulation` profile
downloads the prepared laboratory without grading truths; `evaluation` includes
them. Repeat fetch with `--offline` to use the verified cache.

To inspect general worlds and provenance, download the registry at the same
dataset commit and use blobkit:

```python
from huggingface_hub import snapshot_download
from blobkit.registry import Registry

snapshot = snapshot_download(
    "{{DATASET_REPO}}", repo_type="dataset",
    revision="FULL_DATASET_COMMIT", allow_patterns=["registry/*"],
)
registry = Registry(snapshot + "/registry")
registry.verify()
world = registry.load_genome("WORLD_RECORD_ID_FROM_WORLDS_CATALOG")
```

Use Physim 0.12.0 and blobkit 0.3.5 with Python 3.12. The reference numerical
profile pins NumPy 2.5.2 and SciPy 1.18.0. Code and Docker build instructions live
in the [code repository](https://github.com/swpo/physim). The dataset is independent
of package publication; blobkit 0.3.5 still needs a public package release or an
installable source revision for an upstream environment-only installation.

## Provenance and reproducibility

`registry/index.json` links immutable genomes, recipes, generation runs, candidate
lineage, checkpoints, and harvested records. `registry/availability.json` links
validated preparations and supporting evidence. Exact recipe sources and inputs,
simulation observations, controls, and available pilot artifacts are preserved as
content-addressed artifacts. Original descriptive paths are recorded in the JSON
records. Use `Registry.export_recipe` to materialize a recipe for inspection and
explicit execution; loading or verifying data never executes recipe code.

BF and XV's preparation inputs and recipes have been replay-checked. Their
preserved bundles are the byte-exact evaluation inputs. Some older genomes lack
their complete original evolutionary search history; their records explicitly
retain those gaps. The snapshot does not invent missing provenance.

Each bundle manifest binds world, preparation, and suite identities, numerical
source hashes, dependencies, and every payload hash. `release.json` inventories
the snapshot's files and records exporter source hashes. A dirty code checkout
is identified as such; its Git baseline is not claimed as an exact code release.

## Evaluation boundary and scope

The evaluated model receives its public interface, observations, and its own
files. The trusted evaluator keeps the bundle and grading truths outside the
agent runtime. Recipe sources and archived pilot files are for research and
reproduction, not agent inputs. These public development suites do not establish
performance on undisclosed worlds. The original reference's primary score groups
also omit some fine switch/recovery timing. New preparations or suites receive
new content identities.

## Licensing

World data are CC-BY-4.0 (`LICENSE`); archived code is Apache-2.0 (`LICENSE-CODE`).
Preserve source attribution and the content identities when reusing material.
Archived predictor artifacts can include pickle files: treat those as code-bearing
research artifacts. Evaluation bundle arrays are NPZ loaded without pickle.
