"""Composable evolutionary search with archived recipes and resumable generations.

Callbacks are Python code: evaluate(genome, seed) -> metrics, score(metrics) ->
float, propose(population, rng) -> Proposal | None, select(candidates, size) ->
candidates, and harvest(candidate) -> bool. Callbacks should be deterministic
from their arguments and declared state. Evaluation schedulers implement map.
"""

from __future__ import annotations

import copy
import dataclasses
import inspect
import json
import math
import platform
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from functools import partial
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Callable

import numpy as np

from .registry import Registry, canonical, checksum


class RejectedCandidate(ValueError):
    """An expected physical rejection, distinct from a broken callback."""


@dataclass
class Candidate:
    id: str
    genome_id: str
    genome: dict
    metrics: dict
    score: float | None
    generation: int
    seed: int
    parents: tuple[str, ...] = ()
    operation: dict = field(default_factory=dict)
    rejection: str | None = None


@dataclass
class Proposal:
    genome: dict
    parents: tuple[str, ...]
    operation: dict = field(default_factory=dict)


@dataclass(frozen=True)
class SearchConfig:
    generations: int = 10
    offspring: int = 16
    population: int = 8
    seed: int = 0
    max_attempts: int = 100

    def __post_init__(self):
        for name in ("generations", "offspring", "population", "seed", "max_attempts"):
            value = getattr(self, name)
            minimum = 0 if name in ("generations", "seed") else 1
            if type(value) is not int or value < minimum:
                raise ValueError(f"{name} must be an integer >= {minimum}")
        if self.seed >= 2**32:
            raise ValueError("seed must be less than 2**32")


@dataclass(frozen=True)
class MetricScore:
    name: str = "interest"

    def __call__(self, metrics):
        return float(metrics[self.name])


@dataclass(frozen=True)
class TopK:
    """Elitist selection with at most one candidate per exact genome."""

    def __call__(self, candidates, size):
        selected, seen = [], set()
        for candidate in sorted(candidates, key=lambda c: (-c.score, c.genome_id, c.seed)):
            if candidate.genome_id not in seen:
                selected.append(candidate)
                seen.add(candidate.genome_id)
            if len(selected) == size:
                break
        return selected


@dataclass(frozen=True)
class HarvestAbove:
    threshold: float = 0.0

    def __call__(self, candidate):
        return candidate.score >= self.threshold


@dataclass(frozen=True)
class Variation:
    """Reuse Blobkit mutation and cross-edge recombination, with bounded size."""

    recombination_probability: float = 0.2
    max_fields: int = 24
    mutation_options: dict = field(default_factory=dict)
    recombination_options: dict = field(default_factory=lambda: {"eta": 0.1})

    def __post_init__(self):
        if not 0 <= self.recombination_probability <= 1 or self.max_fields < 1:
            raise ValueError("Invalid variation probability or field limit")

    def __call__(self, population, rng):
        from . import operators

        first = population[int(rng.integers(len(population)))]
        if len(population) > 1 and rng.random() < self.recombination_probability:
            choices = [c for c in population if c.id != first.id]
            second = choices[int(rng.integers(len(choices)))]
            if sum(len(c.genome[part]) for c in (first, second) for part in ("acts", "chans")) > self.max_fields:
                return None
            child, info = operators.merge_cross_edge(first.genome, second.genome, rng=rng, **self.recombination_options)
            parents = (first.id, second.id)
        else:
            child, info = operators.mutate(first.genome, rng, **self.mutation_options)
            parents = (first.id,)
        if child is None or len(child["acts"]) + len(child["chans"]) > self.max_fields:
            return None
        return Proposal(child, parents, info)


@dataclass(frozen=True)
class AssayEvaluator:
    """Default adaptive characterization; CPU or JAX through the same API."""

    backend: str = "cpu"
    options: dict = field(default_factory=dict)

    def __call__(self, genome, seed):
        from .assay_v2b import run_assay_b
        from .soup import get_backend

        result = run_assay_b(
            genome, seed=seed, backend=get_backend(self.backend), results_path=None, verbose=False, **self.options
        )
        return _assay_metrics(result)


@dataclass(frozen=True)
class BatchAssayEvaluator:
    """Use the existing padded JAX ladder for a whole generation's jobs."""

    options: dict = field(default_factory=dict)

    def __call__(self, genome, seed):
        return self.evaluate_many([(genome, seed)])[0]

    def evaluate_many(self, jobs):
        from .assay_batch import run_assay_batch

        results = run_assay_batch(jobs, results_path=None, **self.options)
        outcomes = []
        for row in results:
            try:
                outcomes.append(_assay_metrics(row))
            except RejectedCandidate as error:
                outcomes.append(error)
        return outcomes


def _assay_metrics(result):
    from .assay_v2 import js

    why = result.get("horizon", {}).get("why_stopped")
    if "assay_error" in result or "interest" not in result or why not in ("static", "converged", "cap"):
        raise RejectedCandidate(str(result.get("assay_error", why)))
    horizon = {k: v for k, v in result["horizon"].items() if k != "wall_total"}
    return js(dict(interest=result["interest"], horizon=horizon, components=result["C"], flags=result.get("flags", {})))


@dataclass(frozen=True)
class SimulationEvaluator:
    """Measure one simulation using a user-supplied metric(record) function."""

    metric: Callable
    horizon: float = 100.0
    backend: str = "cpu"
    options: dict = field(default_factory=dict)

    def __post_init__(self):
        if not math.isfinite(self.horizon) or self.horizon <= 0 or self.horizon % 25:
            raise ValueError("Simulation horizon must be positive and on the 25-unit recording grid")

    def __call__(self, genome, seed):
        from .soup import get_backend

        backend = get_backend(self.backend)
        state = backend.init_soup(genome, seed=seed, **self.options)
        status = backend.advance(state, self.horizon)
        if status != "ok":
            raise RejectedCandidate(str(status))
        return self.metric(backend.snapshot_rec(state))


@dataclass
class SearchRecipe:
    name: str
    seeds: list[dict]
    config: SearchConfig = field(default_factory=SearchConfig)
    evaluate: Callable = field(default_factory=AssayEvaluator)
    score: Callable = field(default_factory=MetricScore)
    propose: Callable = field(default_factory=Variation)
    select: Callable = field(default_factory=TopK)
    harvest: Callable = field(default_factory=HarvestAbove)
    parameters: dict = field(default_factory=dict)
    source_files: dict[str, str | Path] = field(default_factory=dict)
    entrypoint: str | None = None
    description: str = ""
    dependencies: tuple[str, ...] = ()


def implementation():
    import blobkit

    blobkit.verify_locks(strict=True)
    packages = {name: version(name) for name in ("blobkit", "numpy", "scipy")}
    try:
        packages["jax"] = version("jax")
    except PackageNotFoundError:
        pass
    return dict(
        packages=packages,
        source_table_sha256=checksum((Path(blobkit.__file__).parent / "_locks.json").read_bytes()),
        python=platform.python_version(),
    )


def _describe(value, registry, sources):
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, (tuple, list)):
        return [_describe(v, registry, sources) for v in value]
    if isinstance(value, dict):
        if not all(isinstance(k, str) for k in value):
            raise TypeError("Recipe state needs string dictionary keys")
        return {k: _describe(v, registry, sources) for k, v in value.items()}
    target = value if inspect.isfunction(value) else type(value)
    source = inspect.getsourcefile(target)
    if source is None:
        raise TypeError("Recipe callbacks need inspectable Python source")
    data = Path(source).read_bytes()
    source_id = registry.artifact(data)
    source_name = "hooks/" + checksum(data)[:16] + "_" + Path(source).name
    sources[source_name] = source_id
    if dataclasses.is_dataclass(value):
        state = {f.name: getattr(value, f.name) for f in dataclasses.fields(value)}
    elif inspect.isfunction(value):
        state = dict(
            defaults=value.__defaults__,
            keyword_defaults=value.__kwdefaults__,
            closure=inspect.getclosurevars(value).nonlocals,
        )
    elif callable(value):
        state = vars(value)
    else:
        raise TypeError(f"Unsupported recipe state: {type(value).__name__}")
    return dict(
        module=target.__module__,
        qualname=target.__qualname__,
        source=source_id,
        state=_describe(state, registry, sources),
    )


def register_recipe(registry, recipe):
    """Snapshot code, callback state, seed genomes, parameters, and implementation."""
    if not recipe.name or not recipe.seeds:
        raise ValueError("A recipe needs a name and seed genomes")
    sources = {name: registry.artifact(Path(path).read_bytes()) for name, path in recipe.source_files.items()}
    if recipe.entrypoint is not None and recipe.entrypoint not in sources:
        raise ValueError("The recipe entrypoint must name an archived source file")
    seeds = [registry.add_genome(g) for g in recipe.seeds]
    hooks = {
        name: _describe(getattr(recipe, name), registry, sources)
        for name in ("evaluate", "score", "propose", "select", "harvest")
    }
    payload = dict(
        name=recipe.name,
        description=recipe.description,
        seeds=seeds,
        config=dataclasses.asdict(recipe.config),
        parameters=recipe.parameters,
        hooks=hooks,
        sources=sources,
        entrypoint=recipe.entrypoint,
        implementation={
            **implementation(),
            "recipe_dependencies": {name: version(name) for name in recipe.dependencies},
        },
    )
    return registry.put("recipe", payload, refs=[*seeds, *sources.values()])


def _candidate(registry, identifier):
    row = registry.get(identifier, kind="candidate")["payload"]
    return Candidate(
        id=identifier,
        genome_id=row["genome"],
        genome=registry.load_genome(row["genome"]),
        metrics=row["metrics"],
        score=row["score"],
        generation=row["generation"],
        seed=row["seed"],
        parents=tuple(row["parents"]),
        operation=row["operation"],
        rejection=row["rejection"],
    )


def _measure(evaluate, job):
    index, genome, seed = job
    try:
        metrics = evaluate(genome, seed)
    except RejectedCandidate as error:
        metrics = error
    return index, metrics


@dataclass(frozen=True)
class SearchResult:
    run_id: str
    recipe_id: str
    checkpoint_id: str
    result_id: str
    population: tuple[str, ...]
    worlds: tuple[str, ...]
    complete: bool


def run_search(registry: Registry, recipe: SearchRecipe, *, resume=None, stop_after=None, map_fn=None):
    """Execute generations 0..N and commit a checkpoint after each generation.

    ``resume`` is a checkpoint ID. An interrupted generation is recomputed from
    its deterministic seeds. ``stop_after`` pauses after that generation without
    changing the recipe. ``map_fn`` can be Executor.map or an equivalent scheduler;
    indexed results are restored to proposal order before selection. A batch
    evaluator's evaluate_many method is used when map_fn is omitted.
    """
    recipe_id = register_recipe(registry, recipe)
    config = recipe.config
    if stop_after is not None and (type(stop_after) is not int or not 0 <= stop_after <= config.generations):
        raise ValueError("stop_after must be a generation within this recipe")
    stop = config.generations if stop_after is None else stop_after
    checkpoint_id, population, worlds = None, [], []
    if resume is not None:
        checkpoint = registry.get(resume, kind="checkpoint")["payload"]
        if checkpoint["recipe"] != recipe_id:
            raise ValueError("Checkpoint recipe, code, parameters, or dependencies changed")
        run_id, start = checkpoint["run"], checkpoint["generation"] + 1
        if stop < start - 1:
            raise ValueError("stop_after precedes the checkpoint")
        checkpoint_id = resume
        population = [_candidate(registry, c) for c in checkpoint["population"]]
        worlds = checkpoint["worlds"]
    else:
        run_id = registry.put(
            "generation-run",
            dict(recipe=recipe_id, execution=str(uuid.uuid4()), started_at=datetime.now(timezone.utc).isoformat()),
            refs=[recipe_id],
        )
        start = 0
    for generation in range(start, stop + 1):
        from .genome import genome_json, validate

        proposals = []
        if generation == 0:
            proposals = [Proposal(copy.deepcopy(g), (), {"kind": "seed"}) for g in recipe.seeds]
        else:
            rng = np.random.default_rng(np.random.SeedSequence([config.seed, generation, 0]))
            for _ in range(config.offspring * config.max_attempts):
                proposal = recipe.propose(copy.deepcopy(population), rng)
                if proposal is None:
                    continue
                if not proposal.parents or not set(proposal.parents) <= {c.id for c in population}:
                    raise ValueError("Proposal parents must reference the selected population")
                proposal.genome = genome_json(proposal.genome)
                canonical(proposal.genome)
                if validate(proposal.genome):
                    continue
                proposals.append(proposal)
                if len(proposals) == config.offspring:
                    break
            if len(proposals) != config.offspring:
                raise RuntimeError("Could not produce enough valid offspring within max_attempts")
        seeds = [
            int(np.random.SeedSequence([config.seed, generation, i, 1]).generate_state(1)[0])
            for i in range(len(proposals))
        ]
        jobs = [(i, copy.deepcopy(p.genome), seeds[i]) for i, p in enumerate(proposals)]
        if map_fn is None and hasattr(recipe.evaluate, "evaluate_many"):
            outcomes = list(enumerate(recipe.evaluate.evaluate_many([(g, seed) for _, g, seed in jobs])))
        else:
            outcomes = list((map_fn or map)(partial(_measure, recipe.evaluate), jobs))
        if sorted(i for i, _ in outcomes) != list(range(len(jobs))):
            raise ValueError("Evaluation scheduler must return exactly one indexed result per job")
        candidates = []
        for index, metrics in sorted(outcomes):
            proposal, seed = proposals[index], seeds[index]
            rejection = str(metrics) if isinstance(metrics, RejectedCandidate) else None
            if rejection is not None:
                metrics, score = {}, None
            else:
                if not isinstance(metrics, dict):
                    raise TypeError("Evaluator must return a metrics dictionary")
                # Round-trip strips mutable aliases and requires finite JSON data.
                from .assay_v2 import js

                metrics = json.loads(canonical(js(metrics)))
                score = float(recipe.score(copy.deepcopy(metrics)))
                if not math.isfinite(score):
                    raise ValueError("Search fitness must be finite")
            genome_id = registry.add_genome(proposal.genome)
            payload = dict(
                run=run_id,
                recipe=recipe_id,
                generation=generation,
                index=index,
                seed=seed,
                genome=genome_id,
                parents=list(proposal.parents),
                operation=proposal.operation,
                metrics=metrics,
                score=score,
                rejection=rejection,
            )
            identifier = registry.put("candidate", payload, refs=[run_id, recipe_id, genome_id, *proposal.parents])
            candidate = _candidate(registry, identifier)
            candidates.append(candidate)
            if rejection is None and recipe.harvest(copy.deepcopy(candidate)):
                world_id = registry.put(
                    "world-record",
                    dict(
                        name=f"{recipe.name}/g{generation}/{index}",
                        genome=genome_id,
                        run=run_id,
                        recipe=recipe_id,
                        candidate=identifier,
                        metrics=metrics,
                        score=score,
                        parents=list(proposal.parents),
                        preparation=None,
                        evaluation_bundle=None,
                    ),
                    refs=[run_id, recipe_id, genome_id, identifier, *proposal.parents],
                )
                worlds.append(world_id)
        eligible = [c for c in population + candidates if c.rejection is None]
        selected = list(recipe.select(copy.deepcopy(eligible), config.population))
        selected_ids = [c.id for c in selected]
        available = {c.id: c for c in eligible}
        if not selected_ids or len(selected_ids) > config.population or len(set(selected_ids)) != len(selected_ids):
            raise ValueError("Selection must return 1..population distinct candidates")
        if not set(selected_ids) <= available.keys():
            raise ValueError("Selection returned an unknown candidate")
        population = [available[c] for c in selected_ids]
        checkpoint_id = registry.put(
            "checkpoint",
            dict(
                run=run_id,
                recipe=recipe_id,
                generation=generation,
                previous=checkpoint_id,
                population=selected_ids,
                candidates=[c.id for c in candidates],
                worlds=worlds,
            ),
            refs=[run_id, recipe_id, *selected_ids, *[c.id for c in candidates], *worlds]
            + ([checkpoint_id] if checkpoint_id else []),
        )
    complete = stop == config.generations
    result_id = registry.put(
        "generation-result",
        dict(
            run=run_id,
            recipe=recipe_id,
            checkpoint=checkpoint_id,
            complete=complete,
            population=[c.id for c in population],
            worlds=worlds,
        ),
        refs=[run_id, recipe_id, checkpoint_id, *worlds],
    )
    return SearchResult(
        run_id, recipe_id, checkpoint_id, result_id, tuple(c.id for c in population), tuple(worlds), complete
    )


def run_recipe_file(path, registry, *, resume=None, stop_after=None, workers=1):
    """Explicitly execute a local recipe module and archive its entrypoint."""
    import importlib.util
    import sys
    from concurrent.futures import ProcessPoolExecutor

    if type(workers) is not int or workers < 1:
        raise ValueError("workers must be a positive integer")
    path = Path(path).resolve()
    module_name = "blobkit_recipe_" + checksum(path.read_bytes())[:16]
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ValueError("Recipe must be a Python module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    recipe = module.build_recipe()
    if not isinstance(recipe, SearchRecipe):
        raise TypeError("build_recipe() must return SearchRecipe")
    recipe.source_files = {**recipe.source_files, path.name: path}
    recipe.entrypoint = path.name
    if workers == 1:
        result = run_search(Registry(registry), recipe, resume=resume, stop_after=stop_after)
    else:
        # Each spawned worker loads the recipe module so custom hooks unpickle.
        with ProcessPoolExecutor(
            max_workers=workers, initializer=_load_recipe_worker, initargs=(str(path), module_name)
        ) as pool:
            result = run_search(Registry(registry), recipe, resume=resume, stop_after=stop_after, map_fn=pool.map)
    return dataclasses.asdict(result)


def _load_recipe_worker(path, name):
    import importlib.util
    import sys

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
