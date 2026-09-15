import importlib
import json
import subprocess
import sys

import numpy as np
import pytest
from blobkit import genome, worlds
from blobkit.soup import sim_cpu


@pytest.mark.parametrize("name", worlds.names())
def test_packaged_world_is_valid_and_independent(name):
    first = worlds.load(name)
    assert genome.validate(first) == []
    first["acts"][0]["lam"] = -10000
    assert worlds.load(name)["acts"][0]["lam"] != -10000


def test_stamp_is_packaged():
    stamp = genome.load_stamp_A4()
    assert stamp is not None


def test_optional_plot_extra_writes_png(tmp_path):
    pytest.importorskip("matplotlib")
    from blobkit.hier_metrics import save_strip

    target = tmp_path / "fields.png"
    save_strip([np.eye(8), np.zeros((8, 8))], target, titles=["one", "two"])
    assert target.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


def test_import_does_not_load_jax():
    subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "import sys; import blobkit; "
            "import blobkit.soup.sim_gpu; import blobkit.assay_batch; "
            "assert 'jax' not in sys.modules",
        ],
        check=True,
    )


def test_all_public_modules_import():
    import blobkit

    for name in blobkit._SUBMODULES:
        importlib.import_module("blobkit." + name)


def canonical(value):
    from blobkit.assay_v2 import js

    def strip(item):
        if isinstance(item, dict):
            return {key: strip(value) for key, value in item.items() if key not in ("wall_total", "wall_s", "wall_sim")}
        if isinstance(item, (list, tuple)):
            return [strip(value) for value in item]
        return item

    return json.dumps(strip(js(value)), sort_keys=True)


@pytest.mark.parametrize("name", ["m4", "mv3"])
def test_cpu_chunking_preserves_fields_and_records(name):
    g = worlds.load(name)
    states = [sim_cpu.init_soup(g, L=64, seed=3, workers=1, kicks=worlds.kicks_for(g)) for _ in range(2)]
    sim_cpu.advance(states[0], 50)
    for time in (25, 50):
        sim_cpu.advance(states[1], time)
    np.testing.assert_array_equal(states[0]["F"], states[1]["F"])
    assert canonical(sim_cpu.snapshot_rec(states[0])) == canonical(sim_cpu.snapshot_rec(states[1]))


@pytest.mark.slow
def test_reference_assay_and_injected_cpu_backend_agree():
    from blobkit.assay_v2 import run_assay
    from blobkit.assay_v2b import run_assay_b
    from blobkit.soup import get_backend

    g = worlds.load("m0")
    kw = dict(seed=7, t0=2500, cap=2500, workers=1, verbose=False, results_path=None)
    original = run_assay(g, **kw)
    injected = run_assay_b(g, backend=get_backend("cpu"), **kw)
    assert canonical(original) == canonical(injected)
    assert original["interest"] == pytest.approx(2.8, abs=1e-12)
