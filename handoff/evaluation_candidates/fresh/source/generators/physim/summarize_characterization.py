"""Verify fresh run artifacts and collect evidence without assigning registry priorities."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import blobkit
import numpy as np
from blobkit.registry import Registry
from characterize import ROOT, digest, write_json


def summarize(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    registry = Registry(ROOT / "registry")
    world_rows = {w["name"]: w for w in registry.catalog()["worlds"]}
    runs, responses, rotations, inventory = [], [], [], []
    expected_runs = {
        f"{world}_s{seed}"
        for world in ("m4", "xv", "bf", "mv3", "ds6_000", "m0", "p4g2_044")
        for seed in (11001, 11002)
    }
    expected_rotors = {"xv_pair_coupled_s12001", "xv_pair_coupled_s12002", "xv_pair_decoupled_s12001"}
    aliases = {
        "rotor_check.py": "generators/physim/rotor_check.py",
        "probe_candidates.py": "generators/physim/probe_candidates.py",
        "genome.py": "packages/blobkit/blobkit/genome.py",
        "sim_cpu.py": "packages/blobkit/blobkit/soup/sim_cpu.py",
        "devices.py": "environments/physim/physim/devices.py",
    }
    source_pins = {}

    def verify_sources(pins):
        for name, expected in pins.items():
            relative = aliases.get(name, name)
            assert digest(output / "source" / relative) == expected, relative
            source_pins[relative] = expected

    for protocol in source.glob("*/protocol.json"):
        verify_sources(json.loads(protocol.read_text())["sources"])
    for run in sorted(source.glob("*/summary.json")):
        row = json.loads(run.read_text())
        folder = run.parent
        g = json.loads((folder / "genome.json").read_text())
        assert g == registry.load_genome(world_rows[row["world"]]["id"]), folder
        with np.load(folder / "fields.npz", allow_pickle=False) as data:
            assert data["F"].dtype == np.float32
            assert np.isfinite(data["F"]).all()
            assert data["t"][-1] == row["T"] == 2500
            assert data["F"].shape[1] == len(g["acts"]) + len(g["chans"])
        summary = row["summary"]
        assert digest(folder / "fields.npz") == row["full_field_sha256"]
        assert row["status"] == "ok" and not summary["d9"]["partial"]
        runs.append(
            dict(
                world=row["world"],
                seed=row["seed"],
                status=row["status"],
                horizon=row["T"],
                moving_fraction=summary["d4"]["mv"],
                organisms=summary["d1"]["n_org_end"],
                C9=summary["d9"]["C9"],
                spatial_class=summary["d9"]["cls"],
                partial=summary["d9"]["partial"],
                v3_weight=summary["v3_weight"],
                occupancy=row["final_activator_occupancy"],
                box_limit=summary["flags"]["box_limit"],
                extension_triggers=[k for k in ("a_mem", "b_org", "c_acf") if row["horizon_diagnostics"][k]],
            )
        )
    for path in sorted(source.glob("*/responses/samples.npz")):
        response_summary = json.loads(path.with_name("summary.json").read_text())
        pins = dict(response_summary["source_sha256"])
        with np.load(path.parent.parent / "final_state.npz", allow_pickle=False) as data:
            assert hashlib.sha256(data["F"].tobytes()).hexdigest() == pins.pop("initial_fields")
        verify_sources(pins)
        with np.load(path, allow_pickle=False) as data:
            sample, times = data["samples"], data["times"]
            arms, seeds = data["arms"].tolist(), data["seeds"].tolist()
        assert sample.shape[:3] == (len(arms), 3, 5) and sample.shape[-1] == 13
        assert seeds == [22001, 22002, 22003] and times.tolist() == [0, 5, 10, 25, 50]
        assert np.isfinite(sample).all()
        for i, arm in enumerate(arms):
            if arm.startswith("pulse_"):
                assert np.array_equal(sample[i, :, 0], sample[0, :, 0])
            if arm == "erase_trail":
                assert np.array_equal(sample[i, :, 0, 0], sample[0, :, 0, 0])
        for i in range(1, 3):
            assert np.array_equal(sample[0, i, 0], sample[0, 0, 0])
            assert not np.array_equal(sample[0, i, -1], sample[0, 0, -1])
        rms = lambda value: np.sqrt(np.mean(value**2, axis=(-1, -2)))
        pairs = list(itertools.combinations(range(3), 2))
        between = np.array([rms(sample[0, i, -1] - sample[0, j, -1]) for i, j in pairs])
        row = dict(
            preparation=path.parent.parent.name,
            trajectories=len(arms) * len(seeds),
            baseline_drift_rms=float(rms(sample[0, :, -1] - sample[0, :, 0]).mean()),
            independent_difference_rms=float(between.mean()),
            pulse_005_rms=float(rms(sample[arms.index("pulse_0.05"), :, -1] - sample[0, :, -1]).mean()),
            pulse_03_rms=float(rms(sample[arms.index("pulse_0.3"), :, -1] - sample[0, :, -1]).mean()),
        )
        if "erase_trail" in arms:
            effect = np.sqrt(np.mean((sample[arms.index("erase_trail"), :, -1, 0] - sample[0, :, -1, 0]) ** 2, axis=-1))
            noise = np.array([np.sqrt(np.mean((sample[0, i, -1, 0] - sample[0, j, -1, 0]) ** 2)) for i, j in pairs])
            row["memory_causal_test"] = dict(
                activator_effect_mean=float(effect.mean()),
                activator_effect_range=[float(effect.min()), float(effect.max())],
                independent_difference_mean=float(noise.mean()),
                ratio_of_means=float(effect.mean() / noise.mean()),
            )
        responses.append(row)
    for path in sorted(source.glob("*/rotation.json")):
        row = json.loads(path.read_text())
        with np.load(path.with_name("fields.npz"), allow_pickle=False) as data:
            assert data["F"].dtype == np.float32 and np.isfinite(data["F"]).all()
            assert data["t"][-1] == 2500
        rotations.append({k: v for k, v in row.items() if k not in {"t", "angle_unwrapped", "separation"}})
    initial_pair = None
    for name in sorted(expected_rotors):
        folder = source / name
        if not (folder / "rotation.json").exists():
            continue
        g = json.loads((folder / "genome.json").read_text())
        original = registry.load_genome(world_rows["xv"]["id"])
        if "decoupled" in name:
            original["W"][0][1] = original["W"][1][0] = 0.0
            original["id"] += "_cross_drive_removed"
        assert g == original
        with np.load(folder / "fields.npz", allow_pickle=False) as data:
            if initial_pair is None:
                initial_pair = data["F"][0]
            else:
                assert np.array_equal(initial_pair, data["F"][0])
    for path in sorted(source.rglob("*")):
        if path.is_file() and path.name != "progress.json":
            inventory.append(
                dict(path=path.relative_to(ROOT).as_posix(), bytes=path.stat().st_size, sha256=digest(path))
            )
    result = dict(
        package_integrity=blobkit.verify_locks(strict=True),
        verified_archived_sources=source_pins,
        simulations=runs,
        responses=responses,
        rotations=rotations,
        trajectory_count=sum(r["trajectories"] for r in responses),
        checks="Genomes match preserved registry records (rotor control differs only in cross-drive and name); all fields finite f32; fixed horizons; source hashes match archived code; sensor shapes; paired initial states; distinct independent-noise continuations; all three rotors start from identical fields.",
        complete_battery=(
            {p.parent.name for p in source.glob("*/summary.json")} == expected_runs
            and {p.parent.name for p in source.glob("*/rotation.json")} == expected_rotors
            and {r["preparation"] for r in responses}
            == expected_runs | (expected_rotors - {"xv_pair_decoupled_s12001"})
        ),
    )
    write_json(output / "measurements.json", result)
    write_json(output / "inventory.json", inventory)
    print(
        json.dumps(
            dict(
                simulations=len(runs),
                prepared_pair_runs=len(rotations),
                sensor_experiments=result["trajectory_count"],
                complete=result["complete_battery"],
            )
        )
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summarize(args.source, args.output)
