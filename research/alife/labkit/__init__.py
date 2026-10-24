"""labkit: shared world format, numerics and evidence packs for the ALife agent lab.

Bytecode: importing labkit turns bytecode caching off for the whole process
(sys.dont_write_bytecode) before any other labkit module or world file is imported, so
neither labkit's modules nor world files write __pycache__ (judges run labkit from inside
read-only mirrors). This file itself is compiled, and its cache written, by the import
system before its first line runs; if that just happened, the file (and the __pycache__
directory, when that leaves it empty) is removed again below, so runs leave nothing
behind. To avoid even that transient write, run inside mirrors with
`python -B -m labkit.run ...` or PYTHONDONTWRITEBYTECODE=1.
"""
import sys

_writing = not sys.dont_write_bytecode
sys.dont_write_bytecode = True  # must stay above every other import of the package


def _drop_own_cache(max_age=10.0):
    """Remove this file's __pycache__ entry if the import system wrote it just now (best effort;
    an older valid cache is left alone, and so is a non-empty __pycache__ directory)."""
    import os
    import time

    pyc, src = globals().get("__cached__"), globals().get("__file__")
    if not pyc or not src or not src.endswith(".py") or os.path.abspath(pyc) == os.path.abspath(src):
        return
    try:
        if time.time() - os.stat(pyc).st_mtime < max_age:
            os.remove(pyc)
            os.rmdir(os.path.dirname(pyc))
    except OSError:
        pass


if _writing:
    _drop_own_cache()
del _writing, _drop_own_cache

from .world import load_world  # noqa: E402

__all__ = ["load_world"]
