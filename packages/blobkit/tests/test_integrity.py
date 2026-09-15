import shutil
from pathlib import Path

import blobkit
import pytest


def test_release_table_matches_installed_files():
    result = blobkit.verify_locks(strict=True)
    assert result["ok"]
    assert result["version"] == blobkit.__version__


def test_historical_table_is_preserved():
    result = blobkit.verify_locks(reference="0.3.4", quiet=True)
    assert result["version"] == "0.3.4"
    assert not result["ok"]
    assert "genome.py" not in result["drift"]
    assert "soup/sim_cpu.py" not in result["drift"]


def test_missing_and_modified_files_fail_strictly(tmp_path, monkeypatch):
    source = Path(blobkit.__file__).parent
    shutil.copytree(source, tmp_path / "blobkit")
    package = tmp_path / "blobkit"
    monkeypatch.setattr(blobkit, "_PKG", str(package))
    monkeypatch.setattr(blobkit, "_LOCK_TABLE", str(package / "_locks.json"))
    (package / "genome.py").write_text("changed")
    (package / "soup/sim_cpu.py").unlink()
    result = blobkit.verify_locks(quiet=True)
    assert set(result["drift"]) == {"genome.py", "soup/sim_cpu.py"}
    with pytest.raises(RuntimeError, match="integrity mismatch"):
        blobkit.verify_locks(strict=True)
    with pytest.warns(RuntimeWarning, match="integrity mismatch"):
        blobkit.verify_locks()
