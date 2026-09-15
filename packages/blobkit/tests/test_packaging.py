import importlib.metadata as metadata
import json

import numpy as np
import pytest
from blobkit import deploy_tools, worlds
from blobkit.assay_batch import run_assay_batch
from blobkit.soup.sim_gpu import init_soup_gpu_batch


@pytest.mark.parametrize("backend", ["cpu", "gpu", "gpu_batch"])
def test_fleet_bundle_preserves_install_metadata_and_data(tmp_path, backend):
    out = tmp_path / "fleet"
    receipt = deploy_tools.make_bundle(str(out), backend=backend, wheel=False)
    assert receipt["n_seeds"] == len(worlds.names()) + 1
    assert "Apache License" in (out / "pkg/LICENSE").read_text()
    assert (out / "pkg/README.md").is_file()
    assert (out / "pkg/blobkit/cli.py").is_file()
    text = (out / "pkg/pyproject.toml").read_text()
    dist = metadata.distribution("blobkit")
    assert json.dumps(dist.metadata["Requires-Python"]) in text
    for dependency in dist.requires:
        assert json.dumps(dependency) in text
    for line in (out / "bundle_hashes.txt").read_text().splitlines():
        checksum, name = line.split("  ", 1)
        assert deploy_tools._sha256(out / name) == checksum
    with pytest.raises(FileExistsError):
        deploy_tools.make_bundle(str(out), wheel=False)
    if backend == "gpu_batch":
        assert (out / "pod_worker_batch.py").is_file()
        assert json.loads((out / "island_config.template.json").read_text())["sim_backend"] == backend


def test_invalid_backend_cannot_replace_output(tmp_path):
    out = tmp_path / "keep"
    out.mkdir()
    (out / "sentinel").write_text("keep")
    with pytest.raises(ValueError):
        deploy_tools.make_bundle(str(out), backend="typo", overwrite=True)
    assert (out / "sentinel").read_text() == "keep"


def test_empty_assay_batch_needs_no_jax():
    assert run_assay_batch([]) == []


@pytest.mark.parametrize("value", [0, -25, float("nan"), float("inf"), 26, 250, 500])
def test_invalid_horizon_rejected_before_device_initialization(value):
    with pytest.raises(ValueError, match="t0 and cap"):
        run_assay_batch([dict(genome=worlds.load("m0"), t0=value, cap=100)])


def test_initial_state_list_must_match_jobs():
    with pytest.raises(ValueError, match="one entry per job"):
        init_soup_gpu_batch([(worlds.load("m0"), 1)], ics=[])


@pytest.mark.parametrize("kind", ["nan", "complex", "shape"])
def test_invalid_initial_fields_rejected_before_device_initialization(kind):
    g = worlds.load("m0")
    ic = np.zeros((3, 128, 128))
    if kind == "nan":
        ic[0, 0, 0] = np.nan
    elif kind == "complex":
        ic = ic.astype(complex)
    else:
        ic = ic[:2]
    with pytest.raises(ValueError, match="lane 0 ic"):
        init_soup_gpu_batch([(g, 1)], L=64, ics=[ic])
