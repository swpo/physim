import copy
import json
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pytest
from blobkit import worlds
from blobkit.generation import (
    AssayEvaluator,
    BatchAssayEvaluator,
    Candidate,
    HarvestAbove,
    MetricScore,
    Proposal,
    RejectedCandidate,
    SearchConfig,
    SearchRecipe,
    SimulationEvaluator,
    Variation,
    register_recipe,
    run_search,
)
from blobkit.registry import Registry


def coefficients(genome, seed):
    return {"quality": float(genome["chans"][0]["tau"]), "seed": seed}


def mass_metric(record):
    return {
        "quality": float(np.mean([values[-1] for values in record["mass"].values()])),
        "horizon": float(record["T"]),
    }


def step(population, rng):
    parent = population[int(rng.integers(len(population)))]
    genome = copy.deepcopy(parent.genome)
    genome["chans"][0]["tau"] += float(rng.uniform(0.1, 1))
    return Proposal(genome, (parent.id,), {"kind": "tau-step"})


def reversed_map(fn, jobs):
    return reversed([fn(job) for job in jobs])


def make_recipe():
    return SearchRecipe(
        "test-evolution",
        [worlds.load("m0"), worlds.load("m4")],
        config=SearchConfig(generations=2, offspring=3, population=2, seed=13),
        evaluate=coefficients,
        score=MetricScore("quality"),
        propose=step,
        harvest=HarvestAbove(0),
        source_files={"recipe.py": __file__},
        entrypoint="recipe.py",
    )


def trajectory(registry, result):
    rows = [r["payload"] for r in registry.records("candidate") if r["payload"]["run"] == result.run_id]
    return [
        (r["generation"], r["index"], r["genome"], r["metrics"], r["score"])
        for r in sorted(rows, key=lambda r: (r["generation"], r["index"]))
    ]


def test_search_resume_reordering_and_harvest_lineage(tmp_path):
    registry = Registry(tmp_path)
    recipe = make_recipe()
    original = copy.deepcopy(recipe.seeds)
    full = run_search(registry, recipe)
    paused = run_search(registry, recipe, stop_after=0)
    resumed = run_search(registry, recipe, resume=paused.checkpoint_id, map_fn=reversed_map)
    assert full.complete and resumed.complete and not paused.complete
    assert full.run_id != resumed.run_id
    assert trajectory(registry, full) == trajectory(registry, resumed)
    assert len(full.worlds) == 8
    assert recipe.seeds == original
    for world in full.worlds:
        row = registry.get(world)["payload"]
        candidate = registry.get(row["candidate"])["payload"]
        assert candidate["run"] == full.run_id
        assert row["recipe"] == full.recipe_id
        assert registry.load_genome(world) == registry.load_genome(candidate["genome"])
        for parent in row["parents"]:
            assert registry.get(parent)["payload"]["generation"] < candidate["generation"]
    assert registry.verify()["ok"]
    export = registry.export_recipe(full.recipe_id, tmp_path / "export")
    assert (export / "recipe.py").read_bytes() == open(__file__, "rb").read()


def test_custom_python_metric_with_real_simulation(tmp_path):
    recipe = make_recipe()
    recipe.seeds = recipe.seeds[:1]
    recipe.config = SearchConfig(generations=1, offspring=1, population=1)
    recipe.evaluate = SimulationEvaluator(
        mass_metric, horizon=25, options={"L": 32, "workers": 1, "n_soup": 1, "noise": 0}
    )
    registry = Registry(tmp_path)
    result = run_search(registry, recipe)
    assert result.complete
    rows = trajectory(registry, result)
    assert len(rows) == 2
    assert all(row[3]["horizon"] == 25 for row in rows)
    harvested = registry.load_genome(result.worlds[-1])
    assert mass_metric_from_genome(harvested)["horizon"] == 25


def mass_metric_from_genome(genome):
    return SimulationEvaluator(mass_metric, horizon=25, options={"L": 32, "workers": 1, "n_soup": 1, "noise": 0})(
        genome, 1
    )


def test_process_scheduler_matches_serial(tmp_path):
    recipe = make_recipe()
    registry = Registry(tmp_path)
    serial = run_search(registry, recipe)
    with ProcessPoolExecutor(max_workers=2) as pool:
        parallel = run_search(registry, recipe, map_fn=pool.map)
    assert trajectory(registry, serial) == trajectory(registry, parallel)


def test_resume_rejects_changed_recipe_or_source(tmp_path):
    registry, recipe = Registry(tmp_path / "registry"), make_recipe()
    source = tmp_path / "recipe.py"
    source.write_text("# first version\n")
    recipe.source_files = {"recipe.py": source}
    paused = run_search(registry, recipe, stop_after=0)
    recipe.parameters["new"] = True
    with pytest.raises(ValueError, match="changed"):
        run_search(registry, recipe, resume=paused.checkpoint_id)
    recipe.parameters.clear()
    source.write_text("# second version\n")
    with pytest.raises(ValueError, match="changed"):
        run_search(registry, recipe, resume=paused.checkpoint_id)


def broken_metric(genome, seed):
    raise RuntimeError("metric bug")


def rejected_metric(genome, seed):
    if genome["id"] == "gt_m4":
        raise RejectedCandidate("expected physical rejection")
    return coefficients(genome, seed)


def test_physical_rejection_is_recorded_but_programming_errors_propagate(tmp_path):
    recipe, registry = make_recipe(), Registry(tmp_path)
    recipe.evaluate = rejected_metric
    run_search(registry, recipe, stop_after=0)
    assert sum(r["payload"]["rejection"] is not None for r in registry.records("candidate")) == 1
    recipe.evaluate = broken_metric
    with pytest.raises(RuntimeError, match="metric bug"):
        run_search(registry, recipe)


def test_scheduler_cannot_drop_results(tmp_path):
    with pytest.raises(ValueError, match="exactly one"):
        run_search(Registry(tmp_path), make_recipe(), map_fn=lambda fn, jobs: [])


def nonfinite_metric(genome, seed):
    return {"quality": float("nan")}


def test_nonfinite_metrics_fail(tmp_path):
    recipe = make_recipe()
    recipe.evaluate = nonfinite_metric
    with pytest.raises(ValueError, match="JSON"):
        run_search(Registry(tmp_path), recipe)


@pytest.mark.parametrize(
    "options", [{"generations": -1}, {"population": 0}, {"offspring": True}, {"seed": -1}, {"max_attempts": 0}]
)
def test_invalid_search_budgets(options):
    with pytest.raises(ValueError):
        SearchConfig(**options)


def test_default_mutation_and_recombination_use_existing_operators():
    population = [Candidate(str(i), str(i), worlds.load(name), {}, 1, 0, i) for i, name in enumerate(("m0", "m4"))]
    before = copy.deepcopy(population)
    from blobkit.genome import validate

    for probability, parent_count in ((0, 1), (1, 2)):
        proposal = Variation(recombination_probability=probability)(population, np.random.default_rng(5))
        assert proposal is not None
        assert len(proposal.parents) == parent_count
        assert not validate(proposal.genome)
    assert population == before


def test_registry_reads_do_not_import_generation_or_jax(tmp_path):
    code = "from blobkit.registry import Registry; import sys; Registry(sys.argv[1]).verify(); assert 'blobkit.generation' not in sys.modules; assert 'jax' not in sys.modules"
    subprocess.run([sys.executable, "-c", code, str(tmp_path)], check=True)


def test_hook_state_changes_recipe_identity(tmp_path):
    registry, recipe = Registry(tmp_path), make_recipe()
    first = register_recipe(registry, recipe)
    recipe.harvest = HarvestAbove(100)
    assert register_recipe(registry, recipe) != first


def test_installed_cli_recipe_export_replay_and_process_workers(tmp_path):
    source = tmp_path / "recipe.py"
    source.write_text(
        "from blobkit import worlds\n"
        "from blobkit.generation import SearchRecipe, SearchConfig, MetricScore\n"
        "def measure(genome, seed):\n"
        "    return {'quality': genome['chans'][0]['tau']}\n"
        "def build_recipe():\n"
        "    return SearchRecipe('cli', [worlds.load('m0'), worlds.load('m4')], "
        "config=SearchConfig(generations=1, offspring=1), evaluate=measure, score=MetricScore('quality'))\n"
    )
    root = tmp_path / "registry"

    def cli(*args):
        return json.loads(subprocess.check_output([sys.executable, "-m", "blobkit.cli", *map(str, args)], text=True))

    first = cli("generate", source, "--registry", root, "--workers", 2)
    exported = tmp_path / "exported"
    cli("registry", "export-recipe", root, first["recipe_id"], exported)
    second = cli("generate", exported / "recipe.py", "--registry", root)
    assert first["recipe_id"] == second["recipe_id"]
    assert first["run_id"] != second["run_id"]
    assert cli("registry", "verify", root)["ok"]


def test_evaluation_runtime_does_not_import_generation():
    pytest.importorskip("physim")
    code = (
        "import sys; sys.modules['blobkit.generation'] = None; sys.modules['blobkit.registry'] = None; "
        "from physim.bundles import implementation_identity; "
        "assert implementation_identity()['blobkit_version']"
    )
    subprocess.run([sys.executable, "-c", code], check=True)


@pytest.mark.slow
def test_default_assay_adapter_with_real_cpu():
    result = AssayEvaluator(options={"L": 64, "workers": 1, "t0": 1250, "cap": 1250})(worlds.load("m0"), 7)
    assert np.isfinite(result["interest"])
    assert result["horizon"]["T_used"] == 1250
    assert "wall_total" not in result["horizon"]
    json.dumps(result, allow_nan=False)


@pytest.mark.accelerator
def test_simulation_adapter_with_jax(accelerator, tmp_path):
    recipe = make_recipe()
    recipe.seeds = recipe.seeds[:1]
    recipe.config = SearchConfig(generations=0)
    recipe.evaluate = SimulationEvaluator(
        mass_metric, horizon=25, backend="gpu", options={"L": 32, "n_soup": 1, "noise": 0}
    )
    result = run_search(Registry(tmp_path), recipe)
    assert result.complete


@pytest.mark.accelerator
@pytest.mark.slow
def test_batch_assay_adapter_with_jax(accelerator):
    results = BatchAssayEvaluator(options={"L": 64, "t0": 1250, "cap": 1250, "battery_procs": 0}).evaluate_many(
        [(worlds.load("m0"), 7)]
    )
    assert len(results) == 1
    assert isinstance(results[0], dict)
    assert np.isfinite(results[0]["interest"])
