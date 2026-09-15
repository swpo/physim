"""A release must preserve the registry and include every declared evaluation."""

import importlib.util
import json
import os
import tomllib
from pathlib import Path

import pytest
from blobkit.registry import Registry
from physim.bundles import Bundle, digest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("world_release", ROOT / "scripts/physim/prepare_world_release.py")
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


@pytest.fixture(scope="module")
def staged(tmp_path_factory):
    bundle = Path(os.environ.get("PHYSIM_TEST_BUNDLE", ROOT / "dist/residency-reference-bundle"))
    if not bundle.is_dir():
        pytest.skip("Set PHYSIM_TEST_BUNDLE to the verified p4g2_044 evaluation bundle")
    output = tmp_path_factory.mktemp("world-release") / "snapshot"
    config = tomllib.loads((ROOT / "configs/physim/release.toml").read_text())
    report = release.stage_release(
        registry_root=ROOT / "registry",
        bundle_paths=[bundle],
        output=output,
        release=config,
    )
    return output, report


def test_release_contains_all_worlds_and_all_evaluations_with_original_identities(staged):
    output, report = staged
    assert Registry(output / "registry").verify() == Registry(ROOT / "registry").verify()
    assert report["availability"]["counts"] == {"eval-ready": 3, "preserved": 21}
    worlds = [json.loads(line) for line in (output / "worlds.jsonl").read_text().splitlines()]
    assert len(worlds) == 24
    assert len({row["genome"] for row in worlds}) == 19
    assert all((row["bundle_path"] is not None) == (row["status"] == "eval-ready") for row in worlds)
    for row in worlds:
        assert (output / row["record_path"]).is_file()
        assert (output / row["genome_path"]).is_file()
    entries = [json.loads(line) for line in (output / "catalog.jsonl").read_text().splitlines()]
    assert {e["world_name"]: (e["public_ports"], e["case_count"]) for e in entries} == {
        "p4g2_044": (12, 15),
        "bf_trail_lab": (4, 11),
        "xv_rotor_lab": (6, 11),
    }
    for entry in entries:
        assert Bundle(output / entry["bundle_path"]).references() == entry["references"]
    for row in report["files"]:
        assert digest(output / row["path"]) == row["sha256"]
    for kind in ("genome", "recipe", "generation-run", "world-record", "candidate", "checkpoint", "artifact"):
        for source in (ROOT / "registry" / kind).glob("*"):
            assert (output / "registry" / kind / source.name).read_bytes() == source.read_bytes()


def test_release_refuses_to_omit_an_eval_ready_bundle(tmp_path):
    config = tomllib.loads((ROOT / "configs/physim/release.toml").read_text())
    with pytest.raises(ValueError, match="does not preserve a complete evaluation bundle"):
        release.stage_release(registry_root=ROOT / "registry", bundle_paths=[], output=tmp_path / "bad", release=config)
