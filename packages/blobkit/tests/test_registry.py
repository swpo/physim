import json
import shutil

import pytest
from blobkit import worlds
from blobkit.registry import Registry


def test_source_world_round_trip_and_portability(tmp_path):
    registry = Registry(tmp_path / "first")
    original = worlds.load("m0")
    identifier = registry.add_source_world(
        "m0",
        original,
        source={"kind": "historical", "recipe_status": "unknown"},
        artifacts={"notes": b"known evidence"},
    )
    original["id"] = "changed"
    assert registry.load_genome(identifier)["id"] == "gt_m0"
    shutil.copytree(registry.root, tmp_path / "moved")
    moved = Registry(tmp_path / "moved")
    assert moved.verify()["ok"]
    assert moved.load_genome(identifier) == registry.load_genome(identifier)


def test_content_identity_and_tampering(tmp_path):
    registry = Registry(tmp_path)
    identifier = registry.add_genome(worlds.load("m0"))
    assert registry.add_genome(worlds.load("m0")) == identifier
    path = registry.path(identifier)
    body = json.loads(path.read_text())
    body["payload"]["id"] = "tampered"
    path.write_text(json.dumps(body))
    with pytest.raises(ValueError, match="integrity"):
        registry.get(identifier)
    with pytest.raises(ValueError, match="mismatch"):
        registry.add_genome(worlds.load("m0"))


def test_missing_references_and_artifact_corruption_fail(tmp_path):
    registry = Registry(tmp_path)
    artifact = registry.artifact(b"recipe code")
    recipe = registry.put("recipe", {"sources": {"recipe.py": artifact}}, refs=[artifact])
    registry.path(artifact).write_bytes(b"changed")
    with pytest.raises(ValueError, match="integrity"):
        registry.verify()
    registry.path(artifact).unlink()
    with pytest.raises(FileNotFoundError):
        registry.put("generation-run", {"recipe": recipe}, refs=[artifact])


@pytest.mark.parametrize("name", ["../escape.py", "/absolute.py", "nested/../escape.py", "a\\b.py", "recipe.json"])
def test_recipe_export_rejects_unsafe_paths(tmp_path, name):
    registry = Registry(tmp_path / "registry")
    artifact = registry.artifact(b"print('never executed')")
    identifier = registry.put("recipe", {"sources": {name: artifact}}, refs=[artifact])
    with pytest.raises(ValueError):
        registry.export_recipe(identifier, tmp_path / "export")
    assert not (tmp_path / "export").exists()
