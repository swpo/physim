"""blobkit — the certified physim blob core, packaged.

Verbatim-locked modules from the source tree (probes/blobs/...): the L0
genome format + IMEX-FFT simulator, the assay batteries (v1 nonlinear probes;
v2 locked adaptive-horizon soup assay), the locked metrics batteries, the S1
soup simulators (CPU locked kernel + JAX GPU port), the variation operators,
and a packaged registry of every certified world/champion/part genome.

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

__version__ = "0.3.3"

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


def verify_locks(strict=False, quiet=False):
    """SHA256 self-check of the locked files against the shipped lock table.

    Returns {"ok": bool, "drift": {relpath: reason}, "n_checked": int}.
    Drift -> loud ImportWarning (or RuntimeError if strict=True). A drifted
    install means the certified numerics can no longer be trusted verbatim.
    """
    with open(_LOCK_TABLE) as f:
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
           "locked_at": table.get("locked_at")}
    if drift:
        msg = ("blobkit LOCK DRIFT — certified files changed since packaging: "
               + "; ".join(f"{k}: {v}" for k, v in drift.items())
               + ". Set BLOBKIT_SKIP_LOCK=1 only if you know why.")
        if strict:
            raise RuntimeError(msg)
        if not quiet:
            warnings.warn(msg, ImportWarning, stacklevel=2)
    return out


if os.environ.get("BLOBKIT_SKIP_LOCK") != "1":
    verify_locks()

_SUBMODULES = ("genome", "assays_v1", "metrics_v1", "hier_metrics",
               "metrics_v2", "assay_v2", "assay_v2b", "assay_batch",
               "worlds", "operators", "soup", "deploy_tools")


def __getattr__(name):
    if name in _SUBMODULES:
        import importlib
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(list(globals()) + list(_SUBMODULES))
