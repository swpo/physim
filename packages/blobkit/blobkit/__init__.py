"""Spatial-field simulators, assays, and a packaged world registry.

The source integrity table identifies the shipped implementation. Numerical
validation and its limits are documented separately in the package README.

    import blobkit
    blobkit.verify_locks()                 # SHA256 self-check (also on import)
    from blobkit.worlds import load
    g = blobkit.assay_v2  # etc.

Environment:
    BLOBKIT_SKIP_LOCK=1   skip the import-time lock check
    BLOBKIT_DATA=<dir>    override packaged world data (worlds/<name>.json)
    BLOBKIT_RESULTS=<p>   default results.json path for assay_v2 CLI
"""
import hashlib
import json
import os
import warnings

__version__ = "0.3.5"

_PKG = os.path.dirname(os.path.abspath(__file__))
_LOCK_TABLE = os.path.join(_PKG, "_locks.json")


def _sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def verify_locks(strict=False, quiet=False, *, reference=None):
    """SHA256 self-check of the locked files against the shipped lock table.

    Returns {"ok": bool, "drift": {relpath: reason}, "n_checked": int}.
    Drift raises RuntimeWarning (or RuntimeError if strict=True). This checks
    file integrity, not numerical accuracy. reference="0.3.4" compares against
    the preserved historical table instead of the installed release table.
    """
    if reference not in (None, "0.3.4"):
        raise ValueError("reference must be None or '0.3.4'")
    table_path = _LOCK_TABLE if reference is None else os.path.join(_PKG, "_locks_0_3_4.json")
    with open(table_path) as f:
        table = json.load(f)
    drift = {}
    for rel, want in table["files"].items():
        p = os.path.join(_PKG, rel)
        if not os.path.exists(p):
            drift[rel] = "MISSING"
            continue
        got = _sha256(p)
        if got != want:
            drift[rel] = f"sha256 {got[:12]}... != locked {want[:12]}..."
    out = {"ok": not drift, "drift": drift, "n_checked": len(table["files"]),
           "locked_at": table.get("locked_at"), "version": table.get("version")}
    if drift:
        msg = ("blobkit source integrity mismatch: "
               + "; ".join(f"{k}: {v}" for k, v in drift.items())
               + ". Set BLOBKIT_SKIP_LOCK=1 only if you know why.")
        if strict:
            raise RuntimeError(msg)
        if not quiet:
            warnings.warn(msg, RuntimeWarning, stacklevel=2)
    return out


if os.environ.get("BLOBKIT_SKIP_LOCK") != "1":
    verify_locks()

_SUBMODULES = ("genome", "assays_v1", "metrics_v1", "hier_metrics",
               "metrics_v2", "assay_v2", "assay_v2b", "assay_batch",
               "worlds", "operators", "soup", "deploy_tools", "generation", "registry")


def __getattr__(name):
    if name in _SUBMODULES:
        import importlib
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(list(globals()) + list(_SUBMODULES))
