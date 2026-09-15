# World generation and provenance

Blobkit provides simulation, mutation and recombination, metrics, evolutionary
search, scheduling, checkpoints, and harvesting. Concrete recipes and migration
entry points live in `generators/physim/`. Physim evaluation imports the same
simulator without importing the search engine or generator checkout.

## Recipes are Python

A recipe file defines `build_recipe()` returning `blobkit.generation.SearchRecipe`.
The example `generators/physim/recipes/small_search.py` evaluates six candidates
over three generations, including the seed generation. It uses short CPU
simulations and a custom mass metric as a workflow demonstration.

```sh
blobkit generate generators/physim/recipes/small_search.py --registry outputs/small-search
blobkit registry verify outputs/small-search
```

| Hook | Contract |
|---|---|
| `evaluate` | `(genome, seed) -> metrics` dictionary |
| `score` | `(metrics) -> finite scalar` used by selection |
| `propose` | `(population, rng) -> Proposal` or `None` for a rejected proposal |
| `select` | `(eligible_candidates, population_size) -> selected candidates` |
| `harvest` | `(candidate) -> bool` |

`SimulationEvaluator(metric, horizon, backend, options)` runs a simulation and
passes its record to your metric. `AssayEvaluator` supplies the existing adaptive
assay; `BatchAssayEvaluator` uses the padded JAX ladder. `Variation` wraps the
existing mutation and cross-edge recombination operators. Python callbacks can
replace these defaults with new metrics, operators, diversity selectors, and
harvest criteria. Expected physical failures can raise `RejectedCandidate`;
unexpected exceptions propagate and preserve the preceding checkpoint.

`run_search(registry, recipe, map_fn=executor.map)` supports external scheduling;
indexed results are restored to proposal order before selection. An evaluator
with `evaluate_many(jobs)` can supply native batching when no map is passed.
The CLI's `--workers N` uses local processes. This scheduler does not provision
GPUs. Existing fleet bundles remain available for the historical island protocol.

## Checkpoint and replay

The returned report contains immutable recipe, run, checkpoint, result, and
harvested-world IDs. `--stop-after 0` checkpoints the seed generation;
`--resume CHECKPOINT_ID` continues the same run. Resume rejects changed recipes,
callback state, source code, and recorded dependencies. An interrupted generation
is recomputed; completed generations are retained. Callbacks should be pure with
respect to their arguments, using the supplied RNG/seed for randomness. Adaptive
strategies should derive their decisions from explicit candidate inputs rather
than hidden mutable callback state.

Recipe records archive the entrypoint, callback sources and declared state,
seed genomes, settings, package/source identities, and parameters. Add auxiliary
source or input files through `source_files`. Add extra installed distribution
names through `dependencies` to record their actual versions. Imported helpers
outside the archived files and installed packages must be declared there.
Reading the registry does not execute Python. To inspect and explicitly replay:

```sh
blobkit registry export-recipe outputs/small-search RECIPE_ID /tmp/exported-recipe
blobkit generate /tmp/exported-recipe/small_search.py --registry outputs/replayed-search
```

Use the recorded package versions and archived inputs when replaying. A different
seed or parameter set produces another recipe identity; separate executions have
distinct run identities. CPU and GPU noise streams and hardware reductions can
differ, so records do not promise universal bitwise reproduction.

## Registry objects

`blobkit.registry.Registry` stores immutable genomes, recipe code artifacts,
generation runs, candidate measurements and parents, checkpoints, and harvested
world records. `registry.load_genome(world_id)` returns a fresh genome for
simulation. `add_source_world(...)` records imported worlds and available
provenance without inventing missing historical steps. `catalog()` provides a
browsing projection. Copying the directory preserves all IDs and references.

Harvested genomes still need a numerical profile, prepared state, apparatus, and
validation to become Physim evaluation bundles. Their existing physical
world/preparation/suite identities remain separate; registry records link to them.
Optional prepared-state NPZs and other evidence can be archived as exact artifact
bytes. Registry artifacts and recipe sources are never automatically executed or
loaded into the evaluation sandbox.
